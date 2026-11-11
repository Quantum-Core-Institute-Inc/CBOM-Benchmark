// Tier 2: curve picked from a profile table at runtime.
package main

import (
	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/rand"
	"fmt"
)

var curves = map[string]func() elliptic.Curve{
	"compat": elliptic.P384,
}

func main() {
	profile := "compat"
	key, err := ecdsa.GenerateKey(curves[profile](), rand.Reader)
	if err != nil {
		panic(err)
	}
	fmt.Println(key.Curve.Params().BitSize)
}
