#include <stdio.h>
#include <string.h>
#include <sched.h>
#include <stdlib.h>
#include <errno.h>
#include <unistd.h>

int get_cpu_num()
{
    FILE *fp = fopen("/proc/cpuinfo", "r");
    if (fp == NULL) {
        perror("fopen");
        return -1;
    }
    else {
        int cpu_num = 0;
        char line[512];
        while (true) {
            fgets(line, 512, fp);
            if (feof(fp))
                break;
            if (strncmp(line, "processor", 9) == 0) {
                cpu_num ++;
            }
        }
        fclose(fp);
        return cpu_num;
    }
}

int main(int argc, char *argv[])
{
    pid_t pid;
    if (argc < 2) {
        printf("%s <PID>\n", argv[0]);
        return 0;
    }

    sscanf(argv[1], "%d", &pid);

    cpu_set_t mask;
    unsigned int len = sizeof(mask);
    if (sched_getaffinity(pid, len, &mask) < 0) {
        perror("sched_getaffinity");
        return -1;
    }

    int i, cpu_num = get_cpu_num();
    if (cpu_num < 0) {
        printf("can't get cpu number\n");
        return 1;
    }

    printf("PID[%d]: ", pid);
    for (i = 0; i < cpu_num; i++) {
        printf("%d", CPU_ISSET(i, &mask));
    }
    printf("\n");
    return 0;
}

