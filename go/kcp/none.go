package main

import (
	"io"
	"log"
	"time"

	"github.com/xtaci/kcp-go"
)

func server() {
	block, _ := kcp.NewNoneBlockCrypt(nil)
	if listener, err := kcp.ListenWithOptions("127.0.0.1:12345", block, 10, 3); err == nil {
		go client()
		for {
			s, err := listener.AcceptKCP()
			if err != nil {
				log.Fatal(err)
			}
			go handleEcho(s)
		}
	} else {
		log.Fatal(err)
	}
}

func handleEcho(conn *kcp.UDPSession) {
	buf := make([]byte, 4096)
	for {
		n, err := conn.Read(buf)
		if err != nil {
			log.Println(err)
			return
		}
		n, err = conn.Write(buf[:n])
		if err != nil {
			log.Println(err)
			return
		}
	}
}

func client() {
	block, _ := kcp.NewNoneBlockCrypt(nil)

	//wait for server to start
	time.Sleep(time.Second)

	if sess, err := kcp.DialWithOptions("127.0.0.1:12345", block, 10, 3); err == nil {
		for {
			data := time.Now().String()
			buf := make([]byte, len(data))
			log.Println("send: ", data)
			if _, err := sess.Write([]byte(data)); err == nil {
				if _, err := io.ReadFull(sess, buf); err == nil {
					log.Println("recv:", string(buf))
					break
				} else {
					log.Fatal(err)
				}
			} else {
				log.Fatal(err)
			}
			time.Sleep(time.Second)
		}
	} else {
		log.Fatal(err)

	}
}

func main() {
	client()
}
