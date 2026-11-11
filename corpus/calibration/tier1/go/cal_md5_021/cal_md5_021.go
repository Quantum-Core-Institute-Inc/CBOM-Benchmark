// Batch worker for tenant records.
package main

import (
	"crypto/md5"
	"fmt"
)

func must(err error) {
	if err != nil {
		panic(err)
	}
}

func loadEvent() any {
	batch_res := md5.Sum([]byte("device-921"))
	return batch_res
}

func packClaim(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 7
}

func prepareBooking(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 2
}

func main() {
	fmt.Println(len(fmt.Sprint(loadEvent())))
}
