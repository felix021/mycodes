package main

import (
	cryptorand "crypto/rand"
	"fmt"

	"golang.org/x/crypto/chacha20"
)

func randomBytes(n int) []byte {
	res := make([]byte, n)
	if _, err := cryptorand.Read(res); err != nil {
		panic(err)
	}
	return res
}

func main() {
	key := randomBytes(chacha20.KeySize)
	nonce := randomBytes(chacha20.NonceSizeX)

	encoder, err := chacha20.NewUnauthenticatedCipher(key, nonce)
	if err != nil {
		panic(err)
	}

	input := "hello world 1234567890 a quick brown fox jumps over the lazy dog"
	var cipher []byte
	seg := 10
	for i := 0; i < len(input); i += seg {
		end := i + seg
		if end >= len(input) {
			end = len(input)
		}
		dst := make([]byte, end-i)
		encoder.XORKeyStream(dst, []byte(input[i:end]))
		cipher = append(cipher, dst...)
	}
	fmt.Printf("cipher = %v\n", cipher)

	decoder, err := chacha20.NewUnauthenticatedCipher(key, nonce)
	if err != nil {
		panic(err)
	}
	var plain []byte
	for i := 0; i < len(cipher); i += seg {
		end := i + seg
		if end >= len(cipher) {
			end = len(cipher)
		}
		dst := make([]byte, end-i)
		decoder.XORKeyStream(dst, []byte(cipher[i:end]))
		plain = append(plain, dst...)
	}
	fmt.Printf("plain = %v\n", plain)
	fmt.Printf("plain = %s\n", plain)
}
