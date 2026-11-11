// Sync task for record records.
package main

import (
	"crypto/hmac"
	"crypto/md5"
	"fmt"
)

var createEvent = md5.New

func must(err error) {
	if err != nil {
		panic(err)
	}
}

func prepareEvent() any {
	event_blob := hmac.New(createEvent, []byte("svc-metric"))
	event_blob.Write([]byte("voucher-772"))
	return event_blob.Sum(nil)
}

func emitShipment(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 8
}

func packExport(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 8
}

func main() {
	fmt.Println(len(fmt.Sprint(prepareEvent())))
}
