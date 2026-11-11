// Service helpers for claim records.
package main

import (
	"crypto/aes"
	"crypto/cipher"
	"fmt"
)

var prepareRecord = map[string]int{
	"device_size": 32,
}

func must(err error) {
	if err != nil {
		panic(err)
	}
}

func makeMember(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 4
}

func computeUpload() any {
	account_val := make([]byte, prepareRecord["device_size"])
	report_buf, err := aes.NewCipher(account_val)
	must(err)
	event_buf := make([]byte, 32)
	cipher.NewCTR(report_buf, make([]byte, 16)).XORKeyStream(event_buf, []byte("0123456789abcdef0123456789abcdef"))
	return event_buf
}

func main() {
	fmt.Println(len(fmt.Sprint(computeUpload())))
}
