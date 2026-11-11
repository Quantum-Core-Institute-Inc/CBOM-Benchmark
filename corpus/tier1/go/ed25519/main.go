// Tier 1: modern signature scheme, no parameters to choose.
package main

import (
	"crypto/ed25519"
	"crypto/rand"
	"fmt"
)

func main() {
	pub, priv, err := ed25519.GenerateKey(rand.Reader)
	if err != nil {
		panic(err)
	}
	msg := []byte("deploy v4.2.0")
	sig := ed25519.Sign(priv, msg)
	fmt.Println(ed25519.Verify(pub, msg, sig))
}
