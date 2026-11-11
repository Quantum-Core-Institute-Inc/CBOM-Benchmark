// Tier 1: key agreement through the standard library, no parameters to choose.
package main

import (
	"bytes"
	"crypto/ecdh"
	"crypto/rand"
	"fmt"
)

func main() {
	curve := ecdh.X25519()
	alice, _ := curve.GenerateKey(rand.Reader)
	bob, _ := curve.GenerateKey(rand.Reader)
	s1, _ := alice.ECDH(bob.PublicKey())
	s2, _ := bob.ECDH(alice.PublicKey())
	fmt.Println(bytes.Equal(s1, s2))
}
