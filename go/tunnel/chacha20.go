package main

import (
	"crypto/md5"
	"errors"
	"fmt"
	"io"
	"math/rand"
	"net"

	"golang.org/x/crypto/chacha20"
)

type Chacha20Stream struct {
	secret  string
	key     []byte
	encoder *chacha20.Cipher
	decoder *chacha20.Cipher
	conn    net.Conn
}

func mustWrite(w io.Writer, p []byte) (n int, err error) {
	for idx := 0; idx < len(p); {
		n, err := w.Write(p[idx:])
		if err != nil {
			return idx + n, err
		}
		idx += n
	}
	return len(p), nil
}

func NewChacha20Stream(secret string, conn net.Conn) (CipherStream, error) {
	s := &Chacha20Stream{
		secret: secret,
		key:    []byte(fmt.Sprintf("%x", md5.Sum([]byte(secret)))),
		conn:   conn,
	}

	var err error
	nonce := make([]byte, chacha20.NonceSizeX)
	if _, err := rand.Read(nonce); err != nil {
		return nil, err
	}
	s.encoder, err = chacha20.NewUnauthenticatedCipher(s.key, nonce)
	if err != nil {
		return nil, err
	}
	if n, err := mustWrite(s.conn, nonce); err != nil || n != len(nonce) {
		return nil, errors.New("write nonce failed: " + err.Error())
	}
	return s, nil
}

func (s *Chacha20Stream) Read(p []byte) (int, error) {
	if s.decoder == nil {
		nonce := make([]byte, chacha20.NonceSizeX)
		if n, err := io.ReadAtLeast(s.conn, nonce, len(nonce)); err != nil || n != len(nonce) {
			return n, errors.New("can't read nonce from stream: " + err.Error())
		}
		decoder, err := chacha20.NewUnauthenticatedCipher(s.key, nonce)
		if err != nil {
			return 0, errors.New("generate decoder failed: " + err.Error())
		}
		s.decoder = decoder
	}

	n, err := s.conn.Read(p)
	if err != nil || n == 0 {
		return n, err
	}

	dst := make([]byte, n)
	pn := p[:n]
	s.decoder.XORKeyStream(dst, pn)
	copy(pn, dst)
	return n, nil
}

func (s *Chacha20Stream) Write(p []byte) (int, error) {
	dst := make([]byte, len(p))
	s.encoder.XORKeyStream(dst, p)
	return mustWrite(s.conn, dst)
}

func (s *Chacha20Stream) Close() error {
	return s.conn.Close()
}
