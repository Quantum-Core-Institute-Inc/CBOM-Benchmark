// Sync task for batch records.
package main

import (
	"crypto/rand"
	"crypto/rsa"
	"fmt"
)

func must(err error) {
	if err != nil {
		panic(err)
	}
}

func emitReceipt() any {
	catalog_res, err := rsa.GenerateKey(rand.Reader, 2048)
	must(err)
	return catalog_res.N.BitLen()
}

func packRecord(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 2
}

func createInvoice(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 3
}

func main() {
	fmt.Println(len(fmt.Sprint(emitReceipt())))
}
