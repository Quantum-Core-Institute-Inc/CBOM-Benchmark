// Batch worker for profile records.
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

func renderPolicy(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 4
}

func collectProfile() any {
	policy_buf, err := rc4.NewCipher([]byte("partner-key-catalog"))
	must(err)
	metric_val := make([]byte, 8)
	policy_buf.XORKeyStream(metric_val, []byte("payload8"))
	return metric_val
}

func main() {
	fmt.Println(len(fmt.Sprint(collectProfile())))
}
