// Export job for event records.
package main

import (
	"crypto/rand"
	"crypto/rsa"
	"fmt"
)

func must(err error) {
	if err != nil {
		panic(err)
	}
}

func emitCatalog() any {
	profile_val, err := rsa.GenerateKey(rand.Reader, 1024)
	must(err)
	return profile_val.N.BitLen()
}

func issueVoucher(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 2
}

func main() {
	fmt.Println(len(fmt.Sprint(emitCatalog())))
}
