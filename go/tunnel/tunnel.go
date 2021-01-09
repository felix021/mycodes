package main

import (
	"flag"
	"fmt"
	"io"
	"net"
)

type TunnelConfig struct {
	Mode   string
	Cipher string
	Secret string
	Listen string
	Remote string
	Stream CipherStreamConstructor
}

type CipherStream interface {
	Read(p []byte) (n int, err error)
	Write(p []byte) (n int, err error)
	Close() error
}

type CipherStreamConstructor func(secret string, conn net.Conn) (CipherStream, error)

var (
	config *TunnelConfig

	constructors = map[string]CipherStreamConstructor{
		"plain": func(secret string, conn net.Conn) (CipherStream, error) {
			return conn, nil
		},
		"chacha20": NewChacha20Stream,
	}
)

func parseConfig() *TunnelConfig {
	mode := flag.String("mode", "server", "server or client")
	cipher := flag.String("cipher", "chacha20", "cipher algorithm")
	secret := flag.String("secret", "helloworld", "secret for the specified algorithm")
	listen := flag.String("listen", ":7788", "IP:PORT to listen on; empty IP or 0.0.0.0 for all interfaces")
	remote := flag.String("remote", "www.baidu.com:80", "For client: server's IP:PORT; for server: destination IP:PORT")
	flag.Parse()

	if *mode != "server" && *mode != "client" {
		return nil
	}

	if _, found := constructors[*cipher]; !found {
		return nil
	}

	if *listen == "" || *remote == "" {
		return nil
	}

	c := &TunnelConfig{}
	if *mode == "server" {
		c.Mode = "server"
	} else {
		c.Mode = "client"
	}
	c.Cipher = *cipher
	c.Secret = *secret
	c.Listen = *listen
	c.Remote = *remote
	c.Stream = constructors[*cipher]
	return c
}

func Socks5Forward(client, target CipherStream) {
	forward := func(src, dest CipherStream) {
		defer src.Close()
		defer dest.Close()
		io.Copy(src, dest)
	}
	go forward(client, target)
	go forward(target, client)
}

func processor(client net.Conn) {
	dest, err := net.Dial("tcp", config.Remote)
	if err != nil {
		client.Close()
		return
	}

	var source, target CipherStream
	if config.Mode == "client" {
		source = client
		target, err = config.Stream(config.Secret, dest)
	} else {
		source, err = config.Stream(config.Secret, client)
		target = dest
	}
	if err != nil {
		client.Close()
		dest.Close()
		return
	}

	Socks5Forward(source, target)
}

func main() {
	config = parseConfig()
	if config == nil {
		flag.Usage()
		return
	}
	fmt.Printf("config = %#v\n", config)

	listener, err := net.Listen("tcp", config.Listen)
	if err != nil {
		fmt.Printf("Listen failed: %v\n", err)
		return
	}
	fmt.Printf("%s listen on %s...\n", config.Mode, config.Listen)

	for {
		remote, err := listener.Accept()
		if err != nil {
			fmt.Printf("Accept failed: %v", err)
			continue
		}
		go processor(remote)
	}
}
