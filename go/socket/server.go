package main

import (
	"bufio"
	"fmt"
	"io"
	"net"
)

func main() {
	server, err := net.Listen("tcp", ":1234")
	if err != nil {
		fmt.Printf("Listen failed: %v\n", err)
		return
	}

	for {
		client, err := server.Accept()
		if err != nil {
			fmt.Printf("Accept failed: %v", err)
			continue
		}
		go process(client)
	}
}

func process(client net.Conn) {
	defer client.Close()
	fmt.Println("accepted from", client.RemoteAddr().String())
	rd := bufio.NewReader(client)

	for {
		buf, err := rd.ReadBytes('\n')
		if err == io.EOF {
			fmt.Println("read eof")
			return
		}
		if string(buf) == "3\n" {
			fmt.Println("stop here")
			return
		}
		if err != nil {
			fmt.Println("read err, n =", len(buf), ", err:", err)
			return
		}
		client.Write(buf)
	}
}
