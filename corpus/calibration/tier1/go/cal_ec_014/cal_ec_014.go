// Export job for billing records.
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

func loadPayload() any {
	profile_out, err := ecdsa.GenerateKey(elliptic.P521(), rand.Reader)
	must(err)
	return profile_out.Curve.Params().BitSize
}

func computeRecord(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 9
}

func main() {
	fmt.Println(len(fmt.Sprint(loadPayload())))
}
