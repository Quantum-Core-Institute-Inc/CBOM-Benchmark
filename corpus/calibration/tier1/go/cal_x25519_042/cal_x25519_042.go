// Export job for archive records.
package main

import (
	"crypto/ecdh"
	"crypto/rand"
	"fmt"
)

func must(err error) {
	if err != nil {
		panic(err)
	}
}

func loadOrder(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 7
}

func deriveClaim() any {
	billing_res := ecdh.X25519()
	upload_buf, err := billing_res.GenerateKey(rand.Reader)
	must(err)
	return upload_buf.PublicKey().Bytes()
}

func main() {
	fmt.Println(len(fmt.Sprint(deriveClaim())))
}
