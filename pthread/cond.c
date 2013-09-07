#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <errno.h>
#include <sys/signal.h>
#include <sys/time.h>

void msleep(int msec)
{
    usleep(msec * 1000);
}

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t canProduce = PTHREAD_COND_INITIALIZER;
pthread_cond_t canConsume = PTHREAD_COND_INITIALIZER;

const int N = 10, nProducer = 1, nConsumer = 4;
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
    printf("stop running...\n"); //WARNING: this is unsafe in sig_handler
}

int pthread_cond_timedwait_msec(pthread_cond_t *cond, pthread_mutex_t *mutex, int msec)
{
    struct timeval now;
    struct timespec timeout;
    int usec = msec * 1000;

    gettimeofday(&now, NULL);

    now.tv_sec += usec / 1000000;
    now.tv_usec += usec % 1000000;
    if (now.tv_usec >= 1000000) {
        now.tv_usec -= 1000000;
        now.tv_sec += 1;
    }

    timeout.tv_sec = now.tv_sec;
    timeout.tv_nsec = now.tv_usec * 1000; //convert to nano-seconds
    return pthread_cond_timedwait(cond, mutex, &timeout);
}

void *producer(void *args)
{
    long i = (long)args;
    printf("producer %ld starts.\n", i);

    while (run)
    {
        msleep(1000); //slow producer
        pthread_mutex_lock(&mutex);
        while (full()) {
            int ret = pthread_cond_timedwait_msec(&canProduce, &mutex, 1500);
            printf("producer [%ld] waked up%s\n", i, ret == ETIMEDOUT ? " for ETIMEDOUT" : "");
            if (!run)
                break;
        }
        if (!full()) {
            printf("[%ld] produce %ld\n", i, i);
            enque(i);
        }
        pthread_mutex_unlock(&mutex);
        pthread_cond_signal(&canConsume);
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
        msleep(1000); //slow consumer
        pthread_mutex_lock(&mutex);
        while (empty()) {
            int ret = pthread_cond_timedwait_msec(&canConsume, &mutex, 1500);
            printf("consumer [%ld] waked up%s\n", i, ret == ETIMEDOUT ? " for ETIMEDOUT" : "");
            if (!run)
                break;
        }
        if (!empty())
            printf("[%ld] consume %d, [%d, %d]\n", i, deque(), front, end);
        pthread_mutex_unlock(&mutex);
        pthread_cond_signal(&canProduce);
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
        msleep(200);
    }
    for (i = 0; i < nConsumer; i++) {
        pthread_create(consumers + i, NULL, consumer, (void *)(long)i);
        msleep(300);
    }

    void *ret;

    for (i = 0; i < nProducer; i++) {
        pthread_join(producers[i], &ret);
        printf("producer %d stopped.\n", i);
    }
    for (i = 0; i < nConsumer; i++) {
        pthread_join(consumers[i], &ret);
        printf("consumer %d stopped.\n", i);
    }
    pthread_mutex_destroy(&mutex);
    pthread_cond_destroy(&canProduce);
    pthread_cond_destroy(&canConsume);

    return 0;
}
