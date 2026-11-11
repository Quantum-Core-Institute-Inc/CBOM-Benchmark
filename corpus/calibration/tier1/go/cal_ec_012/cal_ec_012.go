// Service helpers for voucher records.
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

func collectBatch() any {
	device_val, err := ecdsa.GenerateKey(elliptic.P521(), rand.Reader)
	must(err)
	return device_val.Curve.Params().BitSize
}

func packAccount(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 2
}

func collectAccount(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 2
}

func main() {
	fmt.Println(len(fmt.Sprint(collectBatch())))
}
