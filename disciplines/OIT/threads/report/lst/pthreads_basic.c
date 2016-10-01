#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

#define NUM_THREADS 2
#define NUM_ITERS   100
#define NUM_REPEATS 80

static pthread_t threads[NUM_THREADS];
static char thread_args[NUM_THREADS];

void* task(void* arg) {
    char c = *((char*)arg);
    for (size_t i = 0; i < NUM_ITERS; ++i) {
        for (size_t j = 0; j < NUM_REPEATS; ++j) {
            putchar(c);
        }
        putchar('\n');
    }
}

int main(int argc, char** argv) {
    // init thread attributes
    pthread_attr_t thread_attr;
    pthread_attr_init(&thread_attr);
    pthread_attr_setdetachstate(&thread_attr, PTHREAD_CREATE_JOINABLE);
    // start threads
    for (size_t i = 0; i < NUM_THREADS; ++i) {
        thread_args[i] = 'a' + i;
        int err = pthread_create(&threads[i], &thread_attr,
                                 task, (void*)&thread_args[i]);
        if (err) {
            printf("ERROR: pthread_create: %d\n", err);
            exit(-1);
        }
    }
    // join threads
    for (size_t i = 0; i < NUM_THREADS; ++i) {
        int result_value;
        void* result = &result_value;
        int err = pthread_join(threads[i], &result);
        if (err) {
            printf("ERROR: pthread_join: %d\n", err);
            exit(-1);
        }
        printf("INFO: thread %ld joined with result: %d\n", i, result_value);
    }
    printf("INFO: completed\n");
    return 0;
}
