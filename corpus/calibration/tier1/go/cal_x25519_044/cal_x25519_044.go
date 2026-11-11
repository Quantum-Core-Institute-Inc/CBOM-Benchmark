// Sync task for invoice records.
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

func loadClaim() any {
	upload_buf := ecdh.X25519()
	event_val, err := upload_buf.GenerateKey(rand.Reader)
	must(err)
	return event_val.PublicKey().Bytes()
}

func packExport(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 3
}

func main() {
	fmt.Println(len(fmt.Sprint(loadClaim())))
}
