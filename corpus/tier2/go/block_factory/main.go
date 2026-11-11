// Tier 2: the block constructor is a package variable.
package main

import (
	"crypto/cipher"
	"crypto/des"
	"fmt"
)

var newBlock = des.NewTripleDESCipher

func main() {
	key := []byte("0123456789abcdef01234567")
	block, err := newBlock(key)
	if err != nil {
		panic(err)
	}
	out := make([]byte, 16)
	cipher.NewCBCEncrypter(block, make([]byte, 8)).CryptBlocks(out, []byte("4111111111111111"))
	fmt.Printf("%x\n", out)
}
