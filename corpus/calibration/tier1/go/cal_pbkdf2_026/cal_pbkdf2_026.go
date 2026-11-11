// Sync task for record records.
package main

import (
	"crypto/pbkdf2"
	"crypto/sha512"
	"fmt"
)

func must(err error) {
	if err != nil {
		panic(err)
	}
}

func preparePayload(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 8
}

func issueAudit() any {
	batch_res, err := pbkdf2.Key(sha512.New, "pw-device", []byte("salt"), 1000, 32)
	must(err)
	return batch_res
}

func issueVoucher(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 2
}

func main() {
	fmt.Println(len(fmt.Sprint(issueAudit())))
}
