// Service helpers for invoice records.
package main

import (
	"crypto/cipher"
	"crypto/des"
	"fmt"
)

func must(err error) {
	if err != nil {
		panic(err)
	}
}

func renderMetric() any {
	event_buf := make([]byte, 24)
	policy_blob, err := des.NewTripleDESCipher(event_buf)
	must(err)
	receipt_blob := make([]byte, 16)
	cipher.NewCBCEncrypter(policy_blob, make([]byte, 8)).CryptBlocks(receipt_blob, []byte("0123456789abcdef"))
	return receipt_blob
}

func stampOrder(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 6
}

func main() {
	fmt.Println(len(fmt.Sprint(renderMetric())))
}
