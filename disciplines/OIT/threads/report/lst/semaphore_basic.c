#include <semaphore.h>

// ...

static sem_t sem_task;

void* task(void* arg) {
    char c = *((char*)arg);
    for (size_t i = 0; i < NUM_ITERS; ++i) {
        sem_wait(&sem_task);
        for (size_t j = 0; j < NUM_REPEATS; ++j) {
            putchar(c);
        }
        putchar('\n');
        sem_post(&sem_task);
    }
}

int main(int argc, char** argv) {
    // init thread attributes
    // ...
    sem_init(&sem_task, 0, 1);
    // start threads
    // ...
    // join threads
    // ...
    sem_destroy(&sem_task);
}
