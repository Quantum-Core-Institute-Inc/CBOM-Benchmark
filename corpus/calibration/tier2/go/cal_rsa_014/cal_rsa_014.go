// Batch worker for session records.
package main

import (
	"crypto/rand"
	"crypto/rsa"
	"fmt"
)

var collectMember = map[string]int{
	"tenant_size": 1024,
}

func must(err error) {
	if err != nil {
		panic(err)
	}
}

func createExport(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 3
}

func computeBooking() any {
	policy_val, err := rsa.GenerateKey(rand.Reader, collectMember["tenant_size"])
	must(err)
	return policy_val.N.BitLen()
}

func main() {
	fmt.Println(len(fmt.Sprint(computeBooking())))
}
