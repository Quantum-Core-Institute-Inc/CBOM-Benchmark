// Service helpers for shipment records.
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

func deriveReport(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 6
}

func renderOrder() any {
	_, export_blob, err := ed25519.GenerateKey(rand.Reader)
	must(err)
	return ed25519.Sign(export_blob, []byte("device-565"))
}

func sealBilling(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 3
}

func main() {
	fmt.Println(len(fmt.Sprint(renderOrder())))
}
