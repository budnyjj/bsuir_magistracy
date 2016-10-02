// ...

static pthread_mutex_t mutex_task = PTHREAD_MUTEX_INITIALIZER;
static pthread_cond_t cond_task = PTHREAD_COND_INITIALIZER;

void* task(void* arg) {
    char c = *((char*)arg);
    for (size_t i = 0; i < NUM_ITERS; ++i) {
        pthread_mutex_lock(&mutex_task);
        pthread_cond_wait(&cond_task, &mutex_task);
        for (size_t j = 0; j < NUM_REPEATS; ++j) {
            putchar(c);
        }
        putchar('\n');
        pthread_cond_signal(&cond_task);
        pthread_mutex_unlock(&mutex_task);
    }
}

int main(int argc, char** argv) {
    // init thread attributes
    // ...
    // start threads
    // ...
    // start work
    pthread_mutex_lock(&mutex_task);
    pthread_cond_signal(&cond_task);
    pthread_mutex_unlock(&mutex_task);
    // join threads
    // ...
}
