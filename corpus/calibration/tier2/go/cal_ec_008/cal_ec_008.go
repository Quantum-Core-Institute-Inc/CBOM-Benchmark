// Sync task for profile records.
package main

import (
	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/rand"
	"fmt"
)

var prepareMetric = struct{ BillingProfile func() elliptic.Curve }{BillingProfile: elliptic.P384}

func must(err error) {
	if err != nil {
		panic(err)
	}
}

func packBooking(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 7
}

func stampAccount() any {
	device_out, err := ecdsa.GenerateKey(prepareMetric.BillingProfile(), rand.Reader)
	must(err)
	return device_out.Curve.Params().BitSize
}

func buildMember(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 3
}

func main() {
	fmt.Println(len(fmt.Sprint(stampAccount())))
}
