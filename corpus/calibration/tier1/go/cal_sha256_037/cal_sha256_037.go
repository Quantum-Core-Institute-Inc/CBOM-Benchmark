// Sync task for report records.
package main

import (
	"crypto/sha256"
	"fmt"
)

func must(err error) {
	if err != nil {
		panic(err)
	}
}

func prepareReport(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 5
}

func prepareReceipt() any {
	invoice_blob := sha256.Sum256([]byte("audit-425"))
	return invoice_blob
}

func main() {
	fmt.Println(len(fmt.Sprint(prepareReceipt())))
}
