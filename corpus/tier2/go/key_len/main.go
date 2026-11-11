// Tier 2: key length from a constant, cipher built in a helper.
package main

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"fmt"
)

const keyLen = 24

func newStream(key, iv []byte) cipher.Stream {
	block, err := aes.NewCipher(key)
	if err != nil {
		panic(err)
	}
	return cipher.NewCTR(block, iv)
}

func main() {
	key := make([]byte, keyLen)
	iv := make([]byte, 16)
	rand.Read(key)
	s := newStream(key, iv)
	buf := []byte("export row 19")
	s.XORKeyStream(buf, buf)
	fmt.Printf("%x\n", buf)
}
