// Service helpers for billing records.
package main

import (
	"crypto"
	_ "crypto/sha1"
	"fmt"
)

func must(err error) {
	if err != nil {
		panic(err)
	}
}

func stampShipment(collectProfile crypto.Hash) any {
	upload_buf := collectProfile.New()
	upload_buf.Write([]byte("partner-321"))
	return upload_buf.Sum(nil)
}

func createShipment(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 6
}

func makeBilling(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 5
}

func main() {
	fmt.Println(len(fmt.Sprint(stampShipment(crypto.SHA1))))
}
