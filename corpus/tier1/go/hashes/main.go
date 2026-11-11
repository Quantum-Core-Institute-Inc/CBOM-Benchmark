// Tier 1: direct calls into the standard library's digest packages.
package main

import (
	"crypto/md5"
	"crypto/sha1"
	"crypto/sha256"
	"crypto/sha3"
	"fmt"
)

func main() {
	payload := []byte("invoice-2291")
	legacy := md5.Sum(payload)
	gitStyle := sha1.Sum(payload)
	content := sha256.Sum256(payload)
	sponge := sha3.Sum256(payload)
	fmt.Printf("%x %x %x %x\n", legacy, gitStyle, content, sponge)
}
