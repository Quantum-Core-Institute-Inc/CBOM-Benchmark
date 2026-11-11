// Tier 2: modulus size from a named constant.
package main

import (
	"crypto/rand"
	"crypto/rsa"
	"fmt"
)

const rsaBits = 1024

func newSigner() (*rsa.PrivateKey, error) {
	return rsa.GenerateKey(rand.Reader, rsaBits)
}

func main() {
	k, err := newSigner()
	if err != nil {
		panic(err)
	}
	fmt.Println(k.N.BitLen())
}
