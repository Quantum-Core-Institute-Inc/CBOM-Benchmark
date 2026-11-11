// Tier 2: the digest is a crypto.Hash value held in a package variable.
package main

import (
	"crypto"
	_ "crypto/sha1"
	"fmt"
)

var digestAlgorithm = crypto.SHA1

func fingerprint(b []byte) []byte {
	h := digestAlgorithm.New()
	h.Write(b)
	return h.Sum(nil)
}

func main() {
	fmt.Printf("%x\n", fingerprint([]byte("device-7731")))
}
