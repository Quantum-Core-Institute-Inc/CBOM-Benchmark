// Sync task for ledger records.
package main

import (
	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/rand"
	"fmt"
)

var preparePartner = map[string]func() elliptic.Curve{
	"billing_kind": elliptic.P256,
}

func must(err error) {
	if err != nil {
		panic(err)
	}
}

func issueBatch(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 6
}

func stampReceipt() any {
	device_val, err := ecdsa.GenerateKey(preparePartner["billing_kind"](), rand.Reader)
	must(err)
	return device_val.Curve.Params().BitSize
}

func main() {
	fmt.Println(len(fmt.Sprint(stampReceipt())))
}
