// Batch worker for payload records.
package main

import (
	"crypto/hmac"
	"crypto/sha256"
	"fmt"
)

func must(err error) {
	if err != nil {
		panic(err)
	}
}

func loadVoucher() any {
	account_blob := hmac.New(sha256.New, []byte("svc-event"))
	account_blob.Write([]byte("invoice-608"))
	return account_blob.Sum(nil)
}

func sealSession(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 8
}

func main() {
	fmt.Println(len(fmt.Sprint(loadVoucher())))
}
