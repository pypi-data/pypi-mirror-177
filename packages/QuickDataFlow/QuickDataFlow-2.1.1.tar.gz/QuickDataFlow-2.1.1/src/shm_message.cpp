#include <malloc.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <fcntl.h>
#include <pthread.h>
#include <errno.h>

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <memory.h>

#include "shm_message.hpp"


using namespace std;

namespace fshm
{

    MessageBuff::~MessageBuff()
    {
        // todo
        thr_idle_event_exit.store(true);
        thr_in_event_exit.store(true);
        thr_out_event_exit.store(true);
        // empty cycle
        input_message_cv.notify_one();
        input_message_ready = true;
        output_message_cv.notify_one();
        output_message_ready = true;
        //    read_from_input(this, mem_dst_element);
        //    write_to_out(this, mem_src_element);

        if (th_reader_input.joinable()) {
            th_reader_input.join();
        }

        if (th_writer_out.joinable()) {
            th_writer_out.join();
        }

        //    if(th_idle.joinable())
        //        th_idle.join();
        shmemq_destroy(queue_input.get(), 0);
        shmemq_destroy(queue_output.get(), 0);
        //    queue_input->mem->read_index = 0;
        //    queue_output->mem->read_index = 0;
        //    free(buffPtr);
    }

    MessageBuff::MessageBuff(const char* shm_src_name, const char* shm_dst_name,
                             const size_t q_size_in_, const size_t q_size_out_,
                             const size_t element_size_in_, const size_t element_size_out_,
                             const u_int32_t read_cycle_delay_us_,
                             bool clear_buffer_in, bool clear_buffer_out) :
        input_message_complete(false), output_message_complete(false),
        shm_in_name{shm_src_name}, shm_out_name{shm_dst_name},
        q_size_in{q_size_in_}, q_size_out{q_size_out_},
        element_size_in{element_size_in_}, element_size_out{element_size_out_},
        read_cycle_delay_us{read_cycle_delay_us_}
    {
        //    buffPtr = memalign(alignof(int), len);
        queue_input = shmemq_new(shm_in_name, q_size_in, element_size_in);
        queue_output = shmemq_new(shm_out_name, q_size_out, element_size_out);

        if (clear_buffer_in) {
            clear_in_message();
        }

        if (clear_buffer_out) {
            clear_out_message();
        }

        th_reader_input = thread(read_from_input, this);
        th_writer_out = thread(write_to_out, this);
    }

    void MessageBuff::read_from_input(MessageBuff* self)
    {
        // main cycle of thread
        while (!self->thr_in_event_exit.load()) {
            // wait signal for read buffer
            std::unique_lock lck(self->input_message_waiter);
            self->input_message_cv.wait(lck, [&self]() {
                return self->input_message_ready;
            });
            // lock input message cv
            self->input_message_ready = false;

            if (self->thr_in_event_exit.load()) {
                break;
            }

            bool dequeue_result = self->shmemq_try_dequeue(self->queue_input.get(),
                                                           self->mem_src_element.load(),
                                                           self->element_size_in);
            self->input_message_complete.store(dequeue_result);
        }
    }

    void MessageBuff::write_to_out(MessageBuff* self)
    {
        // main cycle of thread
        while (!self->thr_out_event_exit.load()) {
            std::unique_lock lck(self->output_message_waiter);
            self->output_message_cv.wait(lck, [&self]() {
                return self->output_message_ready;
            });
            self->output_message_ready = false;

            if (self->thr_out_event_exit.load()) {
                break;
            }

            // unlock output_message_waiter from external process for next step
            bool enqueue_result = self->shmemq_try_enqueue(self->queue_output.get(), self->mem_dst_element.load(), self->element_size_out);
            self->output_message_complete.store(enqueue_result);
        }
    }

    void MessageBuff::clear_shmem_attr(shmemq_t* shmem)
    {
        if (shmem->shmem_fd != -1) {
            close(shmem->shmem_fd);
            shm_unlink(shmem->name);
        }

        free(shmem->name);
        delete shmem;
    }

    std::unique_ptr<MessageBuff::shmemq_t> MessageBuff::shmemq_new(char const* name, size_t q_size, size_t element_size)
    {
        bool created;
        auto self = make_unique<shmemq_t>();
        self->max_count = q_size;
        self->element_size = element_size;
        self->max_size = q_size * element_size;
        self->name = strdup(name);
        self->mmap_size = self->max_size + sizeof(struct shmemq_info) - 1;
        created = false;
        self->shmem_fd = shm_open(name, O_RDWR, S_IRUSR | S_IWUSR);

        if (self->shmem_fd == -1) {
            if (errno == ENOENT) {
                self->shmem_fd = shm_open(name, O_RDWR | O_CREAT, S_IRUSR | S_IWUSR);

                if (self->shmem_fd == -1) {
                    clear_shmem_attr(self.get());
                    return nullptr;
                }

                created = true;
            } else {
                clear_shmem_attr(self.get());
                return nullptr;
            }
        }

        if (created && (-1 == ftruncate(self->shmem_fd, self->mmap_size))) {
            clear_shmem_attr(self.get());
            return nullptr;
        }

        self->mem = (struct shmemq_info*)mmap(nullptr, self->mmap_size, PROT_READ | PROT_WRITE, MAP_SHARED, self->shmem_fd, 0);

        if (self->mem == MAP_FAILED) {
            clear_shmem_attr(self.get());
            return nullptr;
        }

        if (created) {
            self->mem->read_index = self->mem->write_index = 0;
            pthread_mutexattr_t attr;
            pthread_mutexattr_init(&attr);
            pthread_mutexattr_setpshared(&attr, PTHREAD_PROCESS_SHARED);
#if ADAPTIVE_MUTEX
            // depricated
            pthread_mutexattr_settype(&attr, PTHREAD_MUTEX_ADAPTIVE_NP);
#endif
            pthread_mutex_init(&self->mem->lock, &attr);
            pthread_mutexattr_destroy(&attr);
            // TODO Need to clean up the mutex? Also, maybe mark it as robust? (pthread_mutexattr_setrobust)
        }

        printf("initialized queue %s, created = %d\n", name, created);
        return self;
    }

    bool MessageBuff::shmemq_try_enqueue(shmemq_t* self, unsigned char* src, unsigned int len)
    {
        if (len != self->element_size) {
            return false;
        }

        pthread_mutex_lock(&self->mem->lock);

        // TODO this test needs to take overflow into account
        if (self->mem->write_index - self->mem->read_index >= self->max_size) {
            pthread_mutex_unlock(&self->mem->lock);
            return false; // There is no more room in the queue
        } else {
            memcpy(&self->mem->data[self->mem->write_index % self->max_size], src, len);
            self->mem->write_index += self->element_size;
            pthread_mutex_unlock(&self->mem->lock);
            return true;
        }
    }

    bool MessageBuff::shmemq_try_dequeue(shmemq_t* self, unsigned char* dst, unsigned int len)
    {
        if (len != self->element_size) {
            return false;
        }

        pthread_mutex_lock(&self->mem->lock);

        // TODO this test needs to take overflow into account
        if (self->mem->read_index >= self->mem->write_index) {
            pthread_mutex_unlock(&self->mem->lock);
            return false; // There are no elements that haven't been consumed yet
        } else {
            memcpy(dst, &self->mem->data[self->mem->read_index % self->max_size], len);
            self->mem->read_index += self->element_size;
            pthread_mutex_unlock(&self->mem->lock);
            return true;
        }
    }

    void MessageBuff::clear_mem_buffer(shmemq_t* self)
    {
        pthread_mutex_lock(&self->mem->lock);
        self->mem->read_index = self->mem->write_index;
        pthread_mutex_unlock(&self->mem->lock);
    }

    void MessageBuff::shmemq_destroy(shmemq_t* self, int unlink)
    {
        munmap(self->mem, self->max_size);
        close(self->shmem_fd);

        if (unlink) {
            shm_unlink(self->name);
        }

        free(self->name);
    }
}



extern "C" {
    fshm::MessageBuff* MessageBuff_new(const char* shm_src_name, const char* shm_dst_name,
                                       const size_t q_size_in_, const size_t q_size_out_,
                                       const size_t element_size_in_, const size_t element_size_out_,
                                       const u_int32_t read_cycle_delay_us_ = 1000,
                                       bool clear_buffer_in = true, bool clear_buffer_out = true)
    {
        return new fshm::MessageBuff(shm_src_name, shm_dst_name, q_size_in_, q_size_out_,
                                     element_size_in_, element_size_out_, read_cycle_delay_us_,
                                     clear_buffer_in, clear_buffer_out);
    }

    void MessageBuff_delete(fshm::MessageBuff* mb)
    {
        delete mb;
    }

    const size_t MessageBuff_len_get(fshm::MessageBuff* mb)
    {
        return mb->len_get();
    }

    const size_t MessageBuff_q_size_in_get(fshm::MessageBuff* mb)
    {
        return mb->q_size_in_get();
    }

    const char* MessageBuff_in_name_get(fshm::MessageBuff* mb)
    {
        return mb->shm_in_name_get();
    }

    const char* MessageBuff_out_name_get(fshm::MessageBuff* mb)
    {
        return mb->shm_out_name_get();
    }

    void MessageBuff_push_msg_sync(fshm::MessageBuff* mb, unsigned char* buff)
    {
        mb->push_message_sync(buff);
    }

    void MessageBuff_get_msg_sync(fshm::MessageBuff* mb, unsigned char* buff)
    {
        mb->get_message_sync(buff);
    }
}
