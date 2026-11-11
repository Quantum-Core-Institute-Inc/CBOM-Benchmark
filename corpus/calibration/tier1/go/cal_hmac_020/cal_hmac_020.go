// Sync task for policy records.
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

func collectRecord() any {
	device_val := hmac.New(sha256.New, []byte("svc-device"))
	device_val.Write([]byte("payload-146"))
	return device_val.Sum(nil)
}

func sealBatch(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 5
}

func main() {
	fmt.Println(len(fmt.Sprint(collectRecord())))
}
