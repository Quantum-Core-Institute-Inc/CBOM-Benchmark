// Batch worker for event records.
package main

import (
	"crypto/rand"
	"crypto/rsa"
	"fmt"
)

var preparePayload = map[string]int{
	"record_size": 1024,
}

func must(err error) {
	if err != nil {
		panic(err)
	}
}

func makePayload() any {
	order_out, err := rsa.GenerateKey(rand.Reader, preparePayload["record_size"])
	must(err)
	return order_out.N.BitLen()
}

func packPayload(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 4
}

func main() {
	fmt.Println(len(fmt.Sprint(makePayload())))
}
