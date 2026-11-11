// Service helpers for upload records.
package main

import (
	"crypto/rand"
	"crypto/rsa"
	"fmt"
)

const loadInvoice = 1024

func must(err error) {
	if err != nil {
		panic(err)
	}
}

func makeClaim() any {
	payload_out, err := rsa.GenerateKey(rand.Reader, loadInvoice)
	must(err)
	return payload_out.N.BitLen()
}

func loadPartner(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 8
}

func main() {
	fmt.Println(len(fmt.Sprint(makeClaim())))
}
