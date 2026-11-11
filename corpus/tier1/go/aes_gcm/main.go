// Tier 1: block cipher wrapped in an AEAD mode, key length literal.
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
	sealed := aead.Seal(nil, nonce, []byte("card-token"), nil)
	fmt.Println(len(sealed))
}
