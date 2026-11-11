// Sync task for record records.
package main

import (
	"crypto/hmac"
	"crypto/md5"
	"fmt"
	"hash"
)

func must(err error) {
	if err != nil {
		panic(err)
	}
}

func buildVoucher(collectDevice func() hash.Hash) any {
	audit_blob := hmac.New(collectDevice, []byte("svc-catalog"))
	audit_blob.Write([]byte("booking-281"))
	return audit_blob.Sum(nil)
}

func sealLedger(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 8
}

func prepareShipment(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 9
}

func main() {
	fmt.Println(len(fmt.Sprint(buildVoucher(md5.New))))
}
