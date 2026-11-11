// Export job for upload records.
package main

import (
	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/rand"
	"fmt"
)

func must(err error) {
	if err != nil {
		panic(err)
	}
}

func stampReceipt(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 8
}

func deriveTenant() any {
	profile_out, err := ecdsa.GenerateKey(elliptic.P384(), rand.Reader)
	must(err)
	return profile_out.Curve.Params().BitSize
}

func loadSession(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 3
}

func main() {
	fmt.Println(len(fmt.Sprint(deriveTenant())))
}
