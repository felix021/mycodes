#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <netinet/udp.h>
#include <time.h>

void check(int ret, const char *msg)
{
    if (ret < 0) {
        perror(msg);
        exit(errno);
    }
}

uint32_t ip2long(const char *ipstr)
{
    uint32_t ip = 0;
    const char *p = ipstr;
    while (1) {
        if (*ipstr == '.' || *ipstr == 0) {
            ip = (ip << 8) + atoi(p);
            p = ipstr + 1;
        }
        if (*ipstr == 0) {
            break;
        }
        ipstr += 1;
    }
    return ip;
}

int main()
{
    int server, flag = 1;

    server = socket(AF_INET, SOCK_DGRAM, 0);
    check(server, "socket");

    check(setsockopt(server, SOL_SOCKET, SO_REUSEADDR, &flag, sizeof(flag)), "setsockopt");

    struct sockaddr_in server_addr, client_addr;
    memset((char *)&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family      = AF_INET;
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    server_addr.sin_port        = htons(1234);

    check(bind(server, (struct sockaddr *)&server_addr, sizeof(struct sockaddr)), "bind");

    //check(listen(server, 1024), "listen");

    char buf[65536];
    socklen_t socklen = sizeof(struct sockaddr);
    while (1) {
        int nr_recv = recvfrom(server, buf, 65535, 0, (struct sockaddr *)&client_addr, &socklen);
        if (nr_recv == 0) {
            continue;
        }
        if (nr_recv < 0) {
            perror("recvfrom");
        }
        buf[nr_recv] = 0;
        fprintf(stderr, "recvfrom (%08x, %u): %d bytes\n", ntohl(client_addr.sin_addr.s_addr), ntohs(client_addr.sin_port), nr_recv);

        int pos = 0;
        while (pos < nr_recv) {
            int nr_send = sendto(server, buf + pos, nr_recv - pos, 0, (struct sockaddr *)&client_addr, socklen);
            if (nr_send < 0) {
                perror("sendto failed, skip");
                break;
            }
            pos += nr_send;
        }
    }
    close(server);
    return 0;
}
