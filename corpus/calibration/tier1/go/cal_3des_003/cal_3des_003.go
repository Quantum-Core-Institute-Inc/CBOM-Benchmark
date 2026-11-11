// Export job for device records.
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

func makeReport(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 3
}

func makeLedger(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 8
}

func packOrder() any {
	device_val := make([]byte, 24)
	billing_val, err := des.NewTripleDESCipher(device_val)
	must(err)
	event_obj := make([]byte, 16)
	cipher.NewCBCEncrypter(billing_val, make([]byte, 8)).CryptBlocks(event_obj, []byte("0123456789abcdef"))
	return event_obj
}

func main() {
	fmt.Println(len(fmt.Sprint(packOrder())))
}
