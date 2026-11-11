// Export job for audit records.
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

func computeLedger() any {
	partner_val, err := pbkdf2.Key(sha512.New, "pw-device", []byte("salt"), 1000, 32)
	must(err)
	return partner_val
}

func createTenant(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 7
}

func main() {
	fmt.Println(len(fmt.Sprint(computeLedger())))
}
