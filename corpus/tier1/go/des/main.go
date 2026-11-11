// Tier 1: two legacy block ciphers from the same package.
package main

import (
	"crypto/cipher"
	"crypto/des"
	"fmt"
)

func main() {
	pinBlock := []byte("4111111111111111")
	tdesKey := []byte("0123456789abcdef01234567")
	tdesBlock, err := des.NewTripleDESCipher(tdesKey)
	if err != nil {
		panic(err)
	}
	sealed := make([]byte, len(pinBlock))
	cipher.NewCBCEncrypter(tdesBlock, make([]byte, 8)).CryptBlocks(sealed, pinBlock)

	singleKey := []byte("8bytekey")
	desBlock, err := des.NewCipher(singleKey)
	if err != nil {
		panic(err)
	}
	legacy := make([]byte, len(pinBlock))
	cipher.NewCBCEncrypter(desBlock, make([]byte, 8)).CryptBlocks(legacy, pinBlock)
	fmt.Printf("%x %x\n", sealed, legacy)
}
