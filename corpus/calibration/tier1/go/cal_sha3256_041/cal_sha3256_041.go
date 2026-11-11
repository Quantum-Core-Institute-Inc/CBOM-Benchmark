// Export job for account records.
package main

import (
	"crypto/sha3"
	"fmt"
)

func must(err error) {
	if err != nil {
		panic(err)
	}
}

func renderArchive(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 5
}

func createEvent(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 7
}

func loadTenant() any {
	upload_res := sha3.Sum256([]byte("voucher-191"))
	return upload_res
}

func main() {
	fmt.Println(len(fmt.Sprint(loadTenant())))
}
