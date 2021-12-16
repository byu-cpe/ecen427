#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int glob = 0;
static pthread_mutex_t mtx = PTHREAD_MUTEX_INITIALIZER;

void *thread_func(void *arg) {
    int loops = *((int *)arg);
    int loc;

    for (int i = 0; i < loops; i++) {
        pthread_mutex_lock(&mtx);
        loc = glob;
        loc++;
        glob = loc;
        pthread_mutex_unlock(&mtx);
    }

    return NULL;
}

int main() {
    printf("******* Threading Example *******\n");
    pthread_t thread1;
    pthread_t thread2;
    int loops = 10000000;

    if (pthread_create(&thread1, NULL, thread_func, &loops)) {
        printf("An error occurred while creating thread.\n");
        return EXIT_FAILURE;
    }

    if (pthread_create(&thread2, NULL, thread_func, &loops)) {
        printf("An error occurred while creating thread.\n");
        return EXIT_FAILURE;
    }

    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);

    printf("glob = %d\n", glob);

    return EXIT_SUCCESS;
}