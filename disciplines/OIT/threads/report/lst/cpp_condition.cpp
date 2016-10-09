// includes and defines
static vector<thread> threads;
static mutex mutex_task;
static condition_variable cond_task;

void task(char c) {
    for (size_t i = 0; i < NUM_ITERS; ++i) {
        {
            unique_lock<mutex>(mutex_task);
            cond_task.wait(lock);
            for (size_t j = 0; j < NUM_REPEATS; ++j) {
                putchar(c);
            }
            putchar('\n');
        }
        cond_task.notify_one();
    }
}

int main(int argc, char** argv) {
    // start threads
    for (size_t i = 0; i < NUM_THREADS; ++i) {
        threads.push_back(thread(task, 'a' + i));
    }
    // start work
    this_thread::sleep_for(std::chrono::seconds(1));
    cond_task.notify_one();
    // join threads
    for (size_t i = 0; i < NUM_THREADS; ++i) {
        threads[i].join();
    }
    printf("INFO: completed\n");
    return 0;
}
