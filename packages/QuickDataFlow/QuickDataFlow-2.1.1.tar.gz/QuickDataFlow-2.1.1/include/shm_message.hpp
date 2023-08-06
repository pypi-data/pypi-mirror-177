#pragma once
#include <stdalign.h>
#include <stdint.h>
#include <vector>
#include <atomic>
#include <pthread.h>
#include <thread>
#include <mutex>
#include <shared_mutex>
#include <memory>
#include <functional>
#include <array>
#include <condition_variable>
#include <unistd.h>

#include <iostream>


namespace fshm
{
    ///
    /// \brief The MessageBuff class
    ///
    class MessageBuff
    {
        public:
            std::mutex input_message_waiter;
            std::mutex output_message_waiter;
            std::condition_variable input_message_cv;  /// for read data
            std::condition_variable output_message_cv;/// for write data
            bool input_message_ready{false};
            bool output_message_ready{false};

            std::atomic_bool input_message_complete; /// for async read data
            std::atomic_bool output_message_complete; /// for async write data

            std::vector<uint8_t> buff; /// message buffer

            const size_t& len_get() const
            {
                return len;
            }
            const size_t& q_size_in_get() const
            {
                return q_size_in;
            }
            const char* shm_in_name_get() const
            {
                return shm_in_name;
            }
            const char* shm_out_name_get() const
            {
                return shm_out_name;
            }

            /// user friendly function
            inline void push_message_async(unsigned char* src_buff)
            {
                {
                    std::lock_guard<std::mutex> lck(output_message_waiter);
                    mem_dst_element = src_buff;
                    output_message_ready = true;
                }
                output_message_cv.notify_one();
            }
            /// user friendly function
            inline bool push_message_async_is_complete()
            {
                return output_message_complete.load();
            }

            /// user friendly function
            inline void push_message_sync(unsigned char* src_buff)
            {
                while (!output_message_complete.load()) {
                    push_message_async(src_buff);
                }

                output_message_complete.store(false);
            }

            /// user friendly function for MessageBuff::read_from_input()
            /// unlock to read_from_input than notify read thread
            /// get pointer to buffer
            /// after call get_message_async you need call get_message_async_is_complete to check read data is comlete
            inline void get_message_async(unsigned char* dst_buff)
            {
                {
                    std::lock_guard<std::mutex> lck(input_message_waiter);
                    mem_src_element = dst_buff;
                    input_message_ready = true;
                }
                input_message_cv.notify_one();
            }

            /// user friendly function
            inline bool get_message_async_is_complete()
            {
                return input_message_complete.load();
            }

            /// user friendly function
            /// wait message forever
            inline void get_message_sync(unsigned char* dst_buff)
            {
                int i = 0;

                while (!input_message_complete.load()) {
                    get_message_async(dst_buff);
                    usleep(read_cycle_delay_us);
                }

                input_message_complete.store(false);
            }

            inline void clear_in_message()
            {
                clear_mem_buffer(queue_input.get());
            }

            inline void clear_out_message()
            {
                clear_mem_buffer(queue_output.get());
            }

            virtual ~MessageBuff();
            MessageBuff(MessageBuff const&) = delete;
            MessageBuff& operator=(MessageBuff const&) = delete;

            MessageBuff(const char* shm_src_name, const char* shm_dst_name,
                        const size_t q_size_in_, const size_t q_size_out_,
                        const size_t element_size_in_, const size_t element_size_out_,
                        const u_int32_t read_cycle_delay_us_ = 1000,
                        bool clear_buffer_in = true, bool clear_buffer_out = true);


        private:
            size_t len; /// size message
            unsigned char* buffPtr = nullptr; /// pointer on buff
            u_int32_t read_cycle_delay_us;

            std::atomic<unsigned char*> mem_src_element = {nullptr}; ///pointer for external src element
            std::atomic<unsigned char*> mem_dst_element = {nullptr}; ///pointer for external dst element
            const char* shm_in_name; /// name of shared memory input
            const char* shm_out_name; /// name of shared memory output
            const size_t q_size_in; /// num elements for input
            const size_t q_size_out; /// num elements for output
            const size_t element_size_in; /// size for one input element
            const size_t element_size_out; /// size for one output element

            /// struct for lock shm buffer
            struct shmemq_info {
                pthread_mutex_t lock; /// mutex for memory lock
                unsigned long read_index;
                unsigned long write_index;
                char data[1];
            };

            /// atributes for shm shared memory
            struct shmemq_t {
                unsigned long max_count;
                unsigned long max_size;
                unsigned long mmap_size;
                unsigned int element_size;
                int shmem_fd;
                struct shmemq_info* mem;
                char* name;
            };

            std::atomic_bool thr_in_event_exit{false}; /// signal for exit
            std::atomic_bool thr_out_event_exit{false}; /// signal for exit
            std::atomic_bool thr_idle_event_exit{false}; /// signal for exit

            //    std::unique_ptr<std::thread> th_reader_input{nullptr};
            //    std::unique_ptr<std::thread> th_writer_out{nullptr};
            std::thread th_reader_input;
            std::thread th_writer_out;
            //    std::thread th_client(client_shm, shm_dst_name, shm_src_name, &thr2_event_exit);
            //    std::thread th_idle(idle, &thr_idle_event_exit);

            std::unique_ptr<shmemq_t> queue_input = nullptr; /// shared memory queue input
            std::unique_ptr<shmemq_t> queue_output = nullptr; /// shared memory queue output

            std::function<void(uint32_t)> cb; /// callback function for read input data

            /// \brief generate shared memory attributes
            /// \param name name shared memory descriptor
            /// \param max_count max size of memory buffer
            /// \param element_size size for one element
            std::unique_ptr<shmemq_t> shmemq_new(char const* name, size_t q_size, size_t element_size);
            /// \brief copy data src to shred memory
            /// \param self shared memory descriptor
            /// \param src data source
            /// \param len is element size of buffer for write to memory
            bool shmemq_try_enqueue(shmemq_t* self, unsigned char* dst, unsigned int len);
            /// \brief copy shared memory to dst
            /// \param self shared memory descriptor
            /// \param dst data destination
            /// \param len is element size of buffer for read from memory
            bool shmemq_try_dequeue(shmemq_t* self, unsigned char* src, unsigned int len);
            /// thread for write to out buffer
            static void write_to_out(MessageBuff* self);
            /// thread for read from input buffer
            static void read_from_input(MessageBuff* self);
            /// clear shared memory
            void clear_shmem_attr(shmemq_t* shmem);
            /// destroy shared memory
            void shmemq_destroy(shmemq_t* self, int unlink);
            /// clear memory buffer
            void clear_mem_buffer(shmemq_t* self);
    };
}

