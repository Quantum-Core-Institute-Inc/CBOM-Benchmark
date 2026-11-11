// Service helpers for event records.
package main

import (
	"crypto/ed25519"
	"crypto/rand"
	"fmt"
)

func must(err error) {
	if err != nil {
		panic(err)
	}
}

func computeUpload(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 9
}

func sealSession(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 6
}

func sealMetric() any {
	_, device_out, err := ed25519.GenerateKey(rand.Reader)
	must(err)
	return ed25519.Sign(device_out, []byte("shipment-640"))
}

func main() {
	fmt.Println(len(fmt.Sprint(sealMetric())))
}
