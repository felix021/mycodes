#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <sys/signal.h>

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t  cond  = PTHREAD_COND_INITIALIZER;

const int N = 10, nProducer = 4, nConsumer = 2;
int products[N], front, end;

int full()
{
    return (end + 1) % N == front;
}

int empty()
{
    return front == end;
}

void enque(int i)
{
    products[end] = i;
    end = (end + 1) % N;
}

int deque()
{
    int ret = products[front];
    front = (front + 1) % N;
    return ret;
}

int run = 1;

void sig_handler(int sig)
{
    run = 0;
    //printf("stop running...\n"); //WARNING: this is unsafe in sig_handler
}

void *producer(void *args)
{
    long i = (long)args;
    printf("producer %ld starts.\n", i);

    while (run)
    {
        usleep(1000000); //slow producer
        pthread_mutex_lock(&mutex);
        if (!full()) {
            printf("[%ld] produce %ld\n", i, i);
            enque(i);
            pthread_cond_broadcast(&cond);
        }
        pthread_mutex_unlock(&mutex);
        pthread_yield();
    }
    return NULL;
}

void *consumer(void *args)
{
    long i = (long)args;
    printf("consumer %ld starts.\n", i);
    while (run)
    {
        usleep(1000000); //slow consumer
        pthread_mutex_lock(&mutex);
        while (empty() && run) {
            pthread_cond_wait(&cond, &mutex);
        }
        if (!empty())
            printf("[%ld] consume %d, [%d, %d]\n", i, deque(), front, end);
        pthread_mutex_unlock(&mutex);
        pthread_yield();
    }
    return NULL;
}

int main(int argc, char *argv[])
{
    int i;

    signal(SIGINT, sig_handler);
    signal(SIGHUP, sig_handler);

    front = 0, end = 0;

    pthread_t producers[nProducer], consumers[nConsumer];

    for (i = 0; i < nProducer; i++) {
        pthread_create(producers + i, NULL, producer, (void *)(long)i);
        usleep(200000);
    }
    for (i = 0; i < nConsumer; i++) {
        pthread_create(consumers + i, NULL, consumer, (void *)(long)i);
        usleep(300000);
    }

    void *ret;

    for (i = 0; i < nProducer; i++) {
        pthread_join(producers[i], &ret);
    }
    for (i = 0; i < nConsumer; i++) {
        pthread_join(consumers[i], &ret);
    }
    pthread_mutex_destroy(&mutex);
    pthread_cond_destroy(&cond);

    return 0;
}
