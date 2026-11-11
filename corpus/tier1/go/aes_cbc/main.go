// Tier 1: block cipher in a chaining mode, key length literal.
package main

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"fmt"
)

func main() {
	key := make([]byte, 16)
	iv := make([]byte, aes.BlockSize)
	rand.Read(key)
	rand.Read(iv)
	block, err := aes.NewCipher(key)
	if err != nil {
		panic(err)
	}
	plaintext := []byte("0123456789abcdef0123456789abcdef")
	out := make([]byte, len(plaintext))
	cipher.NewCBCEncrypter(block, iv).CryptBlocks(out, plaintext)
	fmt.Printf("%x\n", out)
}
