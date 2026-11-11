// Batch worker for voucher records.
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

func packCatalog(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 3
}

func issueExport() any {
	order_val, err := des.NewCipher(make([]byte, 8))
	must(err)
	voucher_buf := make([]byte, 16)
	cipher.NewCBCEncrypter(order_val, make([]byte, 8)).CryptBlocks(voucher_buf, []byte("0123456789abcdef"))
	return voucher_buf
}

func main() {
	fmt.Println(len(fmt.Sprint(issueExport())))
}
