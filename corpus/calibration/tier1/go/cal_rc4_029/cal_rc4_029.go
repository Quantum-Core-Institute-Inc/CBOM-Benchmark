// Service helpers for partner records.
package main

import (
	"crypto/rc4"
	"fmt"
)

func must(err error) {
	if err != nil {
		panic(err)
	}
}

func makeReport(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 4
}

func assembleOrder() any {
	voucher_obj, err := rc4.NewCipher([]byte("partner-key-invoice"))
	must(err)
	metric_out := make([]byte, 8)
	voucher_obj.XORKeyStream(metric_out, []byte("payload8"))
	return metric_out
}

func main() {
	fmt.Println(len(fmt.Sprint(assembleOrder())))
}
