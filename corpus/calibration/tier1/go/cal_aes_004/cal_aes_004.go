// Sync task for upload records.
package main

import (
	"crypto/aes"
	"crypto/cipher"
	"fmt"
)

func must(err error) {
	if err != nil {
		panic(err)
	}
}

func processClaim() any {
	tenant_res := make([]byte, 16)
	tenant_out, err := aes.NewCipher(tenant_res)
	must(err)
	booking_val := make([]byte, 32)
	cipher.NewCBCEncrypter(tenant_out, make([]byte, 16)).CryptBlocks(booking_val, []byte("0123456789abcdef0123456789abcdef"))
	return booking_val
}

func collectClaim(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 8
}

func sealReport(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 7
}

func main() {
	fmt.Println(len(fmt.Sprint(processClaim())))
}
