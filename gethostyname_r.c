#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <errno.h>

#include <netdb.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <sys/socket.h>

int host2addr(const char *host, struct in_addr *addr)
{
    if (inet_aton(host, addr)) 
        return 0;

    struct hostent he, *result;
    int herr, ret, bufsz = 512;
    char *buff = NULL;
    do {
        printf("buffsz = %d\n", bufsz);
        char *new_buff = (char *)realloc(buff, bufsz);
        if (new_buff == NULL) {
            free(buff);
            return ENOMEM;
        }
        buff = new_buff;
        ret = gethostbyname_r(host, &he, buff, bufsz, &result, &herr);
        bufsz *= 2;
    } while (ret == ERANGE);

    if (ret == 0 && result != NULL) {
        *addr = *(struct in_addr *)he.h_addr;
        printf("%p, %p, %p, %p\n", buff, he.h_name, he.h_aliases, he.h_addr_list);
    }
    else if (result != &he)
        ret = herr;
    free(buff);
    return ret;
}

int main(int argc, char *argv[])
{
    if (argc < 2)
        return -1;
    struct in_addr addr;
    int ret;
    ret = host2addr(argv[1], &addr);
    if (0 == ret) {
        char *s = inet_ntoa(addr);
        puts(s);
    }
    else{
        printf("error happened: %d\n", ret);
    }
    return 0;
}
