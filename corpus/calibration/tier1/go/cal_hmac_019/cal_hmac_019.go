// Service helpers for shipment records.
package main

import (
	"crypto/hmac"
	"crypto/sha256"
	"fmt"
)

func must(err error) {
	if err != nil {
		panic(err)
	}
}

func prepareRecord(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 5
}

func assembleAccount(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 2
}

func stampOrder() any {
	order_obj := hmac.New(sha256.New, []byte("svc-session"))
	order_obj.Write([]byte("audit-847"))
	return order_obj.Sum(nil)
}

func main() {
	fmt.Println(len(fmt.Sprint(stampOrder())))
}
