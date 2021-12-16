#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void *do_work(void *arg);

int main() {
    printf("******* Threading Example *******\n");
    pthread_t thread;
    int i = 0;

    if (pthread_create(&thread, NULL, do_work, NULL)) {
        printf("An error occurred while creating thread.\n");
        return EXIT_FAILURE;
    }

    printf("Parent: Hi!\n");
    for (int i = 0; i < 10; i++) {
        printf("Parent: Doing work... (%d)\n", i);
        sleep(1);
    }

    pthread_exit(NULL);
    return EXIT_SUCCESS;
}

void *do_work(void *arg) {
    printf("Child: Hi!\n");

    for (int i = 0; i < 10; i++) {
        printf("Child: Doing work... (%d)\n", i);
        sleep(1);
    }
    pthread_exit(NULL);
}