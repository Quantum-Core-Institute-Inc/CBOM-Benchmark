// Batch worker for member records.
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

func issuePayload() any {
	session_blob, err := des.NewCipher(make([]byte, 8))
	must(err)
	account_blob := make([]byte, 16)
	cipher.NewCBCEncrypter(session_blob, make([]byte, 8)).CryptBlocks(account_blob, []byte("0123456789abcdef"))
	return account_blob
}

func processRecord(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 7
}

func main() {
	fmt.Println(len(fmt.Sprint(issuePayload())))
}
