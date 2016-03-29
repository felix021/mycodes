#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <netinet/tcp.h>
#include <netinet/udp.h>
#include <arpa/inet.h>
#include <time.h>
#include <signal.h>
#define min(a, b) (a < b ? a : b)

void sighandler(int signo)
{
    printf("[signal] %d received\n", signo);
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
    signal(SIGHUP, sighandler);
    int ret, sockfd;
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd == -1) {
        perror("socket");
        return errno;
    }

    struct sockaddr_in server_addr;
    server_addr.sin_family      = AF_INET;
    server_addr.sin_port        = htons(1234);
    server_addr.sin_addr.s_addr = htonl(ip2long("127.0.0.1"));
    //server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    bzero((char *) &(server_addr.sin_zero), 8);

    int flag = 1;
    ret = setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &flag, sizeof(int));
    if (ret < 0) {
        perror("setsockopt SO_REUSEADDR");
        return errno;
    }
    ret = setsockopt(sockfd, IPPROTO_TCP, TCP_NODELAY, &flag, sizeof(int));
    if (ret < 0) {
        perror("setsockopt, TCP_NODELAY");
        return errno;
    }

    ret = bind(sockfd, (struct sockaddr *) &server_addr, sizeof(struct sockaddr));
    if (ret == -1) {
        perror("bind");
        return errno;
    }

    ret = listen(sockfd, 1024);
    if (ret == -1) {
        perror("listen");
        return errno;
    }

    int client = 0;
    socklen_t sin_size = sizeof(struct sockaddr_in);
    struct sockaddr_in client_addr;
    while (1) {
        client = accept(sockfd, (struct sockaddr *)&client_addr, &sin_size);
        if (client < 0) {
            perror("accept");
            continue;
        }
        fprintf(stderr, "accepted from %s\n", inet_ntoa(client_addr.sin_addr));

        char buff[1024];
        while (1) {
            ret = recv(client, buff, 1000, 0);
            if (ret == 0) {
                fprintf(stderr, "client disconnected.\n");
                break;
            }
            if (ret < 0) {
                if (errno == EINTR || errno == EAGAIN) {
                    continue;
                }
                perror("recv failed");
                break;
            }
            int total = ret, sent = 0;
            while (sent < total) {
                //ret = send(client, buff + sent, total - sent, 0);
                ret = send(client, buff + sent, 1, 0);
                if (ret < 0) {
                    if (errno == EINTR || errno == EAGAIN) {
                        continue;
                    }
                    perror("send failed");
                    sent = -1;
                    break;
                }
                sent += ret;
                usleep(50000);
            }
            if (sent < 0) {
                break;
            }
        }
        ret = close(client);
        if (ret < 0) {
            perror("close");
        }
    }

    return 0;
}
