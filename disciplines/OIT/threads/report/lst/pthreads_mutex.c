// ...

static pthread_mutex_t mutex_task = PTHREAD_MUTEX_INITIALIZER;

void* task(void* arg) {
    char c = *((char*)arg);
    for (size_t i = 0; i < NUM_ITERS; ++i) {
        pthread_mutex_lock(&mutex_task);
        for (size_t j = 0; j < NUM_REPEATS; ++j) {
            putchar(c);
        }
        putchar('\n');
        pthread_mutex_unlock(&mutex_task);
    }
}

// ...
