package main

import (
	"bufio"
	"fmt"
	"net"
)

func main() {
	server, err := net.Dial("tcp", "127.0.0.1:1234")
	if err != nil {
		fmt.Println("dian err:", err)
		return
	}
	fmt.Println("server.addr:", server.RemoteAddr().String())

	data := "0\n1\n2\n3\n4\n5\n"
	n, err := server.Write([]byte(data))
	if n == 0 || err != nil {
		fmt.Println("write err: n =", n, ", err =", err)
		return
	}

	rd := bufio.NewReader(server)
	for {
		buf, err := rd.ReadString('\n')
		if err != nil {
			fmt.Println("read err:", err)
			break
		}
		fmt.Print(buf)
	}
}
