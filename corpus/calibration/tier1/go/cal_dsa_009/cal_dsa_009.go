// Export job for claim records.
package main

import (
	"crypto/dsa"
	"crypto/rand"
	"fmt"
)

func must(err error) {
	if err != nil {
		panic(err)
	}
}

func deriveArchive(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 3
}

func emitCatalog() any {
	var invoice_buf dsa.Parameters
	must(dsa.GenerateParameters(&invoice_buf, rand.Reader, dsa.L1024N160))
	return invoice_buf.P.BitLen()
}

func sealExport(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 8
}

func main() {
	fmt.Println(len(fmt.Sprint(emitCatalog())))
}
