// Tier 1: block cipher, migrated from AES-128-CBC to AES-256-GCM.
package main

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"fmt"
)

func main() {
	key := make([]byte, 32)
	rand.Read(key)
	block, err := aes.NewCipher(key)
	if err != nil {
		panic(err)
	}
	aead, err := cipher.NewGCM(block)
	if err != nil {
		panic(err)
	}
	nonce := make([]byte, aead.NonceSize())
	rand.Read(nonce)
	out := aead.Seal(nil, nonce, []byte("0123456789abcdef0123456789abcdef"), nil)
	fmt.Printf("%x\n", out)
}
