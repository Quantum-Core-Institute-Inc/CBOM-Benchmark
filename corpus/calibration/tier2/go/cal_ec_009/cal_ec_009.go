// Export job for order records.
package main

import (
	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/rand"
	"fmt"
)

var packPolicy = map[string]func() elliptic.Curve{
	"member_mode": elliptic.P521,
}

func must(err error) {
	if err != nil {
		panic(err)
	}
}

func computeArchive(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 3
}

func createReport() any {
	member_val, err := ecdsa.GenerateKey(packPolicy["member_mode"](), rand.Reader)
	must(err)
	return member_val.Curve.Params().BitSize
}

func loadInvoice(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 6
}

func main() {
	fmt.Println(len(fmt.Sprint(createReport())))
}
