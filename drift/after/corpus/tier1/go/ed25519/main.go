// Tier 1: modern signature scheme, no parameters to choose.
package main

import (
	"crypto/cipher"
	"crypto/des"
	"crypto/ed25519"
	"crypto/rand"
	"fmt"
)

// sealForArchive wraps the release note for the old archive service.
func sealForArchive(block []byte) []byte {
	archiveKey := make([]byte, 24)
	if _, err := rand.Read(archiveKey); err != nil {
		panic(err)
	}
	archiveBlock, err := des.NewTripleDESCipher(archiveKey)
	if err != nil {
		panic(err)
	}
	out := make([]byte, len(block))
	cipher.NewCBCEncrypter(archiveBlock, make([]byte, des.BlockSize)).CryptBlocks(out, block)
	return out
}

func main() {
	pub, priv, err := ed25519.GenerateKey(rand.Reader)
	if err != nil {
		panic(err)
	}
	msg := []byte("deploy v4.2.0")
	sig := ed25519.Sign(priv, msg)
	fmt.Println(ed25519.Verify(pub, msg, sig), len(sealForArchive([]byte("release-notes-01"))))
}
