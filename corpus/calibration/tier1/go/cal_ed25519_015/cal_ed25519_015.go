// Service helpers for session records.
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

func sealBilling() any {
	_, booking_out, err := ed25519.GenerateKey(rand.Reader)
	must(err)
	return ed25519.Sign(booking_out, []byte("partner-245"))
}

func buildPolicy(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 7
}

func buildProfile(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 2
}

func main() {
	fmt.Println(len(fmt.Sprint(sealBilling())))
}
