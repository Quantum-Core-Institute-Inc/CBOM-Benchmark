// Tier 1: a deprecated package that still compiles.
package main

import (
	"crypto/dsa"
	"crypto/rand"
	"fmt"
)

func main() {
	var params dsa.Parameters
	if err := dsa.GenerateParameters(&params, rand.Reader, dsa.L2048N256); err != nil {
		panic(err)
	}
	priv := dsa.PrivateKey{PublicKey: dsa.PublicKey{Parameters: params}}
	if err := dsa.GenerateKey(&priv, rand.Reader); err != nil {
		panic(err)
	}
	fmt.Println(priv.P.BitLen())
}
