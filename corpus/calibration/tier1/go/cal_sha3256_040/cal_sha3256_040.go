// Batch worker for device records.
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

func stampBatch(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 9
}

func issuePayload() any {
	ledger_out := sha3.Sum256([]byte("report-866"))
	return ledger_out
}

func main() {
	fmt.Println(len(fmt.Sprint(issuePayload())))
}
