// Tier 1: curve-based signing with a named curve.
package main

import (
	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/rand"
	"crypto/sha256"
	"fmt"
)

func main() {
	key, err := ecdsa.GenerateKey(elliptic.P256(), rand.Reader)
	if err != nil {
		panic(err)
	}
	digest := sha256.Sum256([]byte("webhook-body"))
	sig, err := ecdsa.SignASN1(rand.Reader, key, digest[:])
	if err != nil {
		panic(err)
	}
	fmt.Println(len(sig) > 0)
}
