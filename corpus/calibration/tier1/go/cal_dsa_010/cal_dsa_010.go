// Sync task for invoice records.
package main

import (
	"crypto/dsa"
	"crypto/rand"
	"fmt"
)

func must(err error) {
	if err != nil {
		panic(err)
	}
}

func renderPayload(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 7
}

func packArchive() any {
	var order_blob dsa.Parameters
	must(dsa.GenerateParameters(&order_blob, rand.Reader, dsa.L2048N256))
	return order_blob.P.BitLen()
}

func main() {
	fmt.Println(len(fmt.Sprint(packArchive())))
}
