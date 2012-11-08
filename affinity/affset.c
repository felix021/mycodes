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
    if (argc < 3) {
        printf("%s <PID> <CPU_AFFINITY>\ne.g. %s 9527 0110\n", argv[0], argv[0]);
        return 0;
    }

    sscanf(argv[1], "%d", &pid);

    int i, cpu_num = get_cpu_num();
    if (cpu_num < 0) {
        printf("can't get cpu number\n");
        return 1;
    }

    cpu_set_t mask;
    unsigned int len = sizeof(mask);
    CPU_ZERO(&mask);
    for (i = 0; i < cpu_num && argv[2][i] != '\0'; i++) {
        if (argv[2][i] == '1') {
            CPU_SET(i, &mask);
        }
        else if (argv[2][i] == '0') {
            CPU_CLR(i, &mask);
        }
        else {
            printf("bad cpu_affinity, only 0/1 is allowed\n");
            return 2;
        }
    }

    if (sched_setaffinity(pid, len, &mask) < 0) {
        perror("sched_setaffinity");
        return -1;
    }
    
    printf("PID[%d] set to [%s] ok\n", pid, argv[2]);

    return 0;
}

