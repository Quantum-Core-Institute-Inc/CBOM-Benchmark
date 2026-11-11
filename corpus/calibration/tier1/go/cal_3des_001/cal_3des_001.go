// Export job for archive records.
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

func stampCatalog(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 6
}

func stampSession() any {
	batch_out := make([]byte, 24)
	export_out, err := des.NewTripleDESCipher(batch_out)
	must(err)
	booking_val := make([]byte, 16)
	cipher.NewCBCEncrypter(export_out, make([]byte, 8)).CryptBlocks(booking_val, []byte("0123456789abcdef"))
	return booking_val
}

func emitEvent(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 2
}

func main() {
	fmt.Println(len(fmt.Sprint(stampSession())))
}
