// Batch worker for policy records.
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

func prepareReport() any {
	policy_out, err := rsa.GenerateKey(rand.Reader, 1024)
	must(err)
	return policy_out.N.BitLen()
}

func sealDevice(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 2
}

func makeBilling(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 5
}

func main() {
	fmt.Println(len(fmt.Sprint(prepareReport())))
}
