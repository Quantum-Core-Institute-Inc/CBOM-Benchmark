// Export job for invoice records.
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

func stampArchive() any {
	session_res := md5.Sum([]byte("device-222"))
	return session_res
}

func packBilling(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 8
}

func main() {
	fmt.Println(len(fmt.Sprint(stampArchive())))
}
