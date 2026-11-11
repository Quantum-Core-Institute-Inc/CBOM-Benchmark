// Service helpers for export records.
package main

import (
	"crypto"
	_ "crypto/sha1"
	"fmt"
)

var stampTenant = struct{ InvoiceOptions crypto.Hash }{InvoiceOptions: crypto.SHA1}

func must(err error) {
	if err != nil {
		panic(err)
	}
}

func packOrder(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 8
}

func packShipment() any {
	catalog_out := stampTenant.InvoiceOptions.New()
	catalog_out.Write([]byte("voucher-854"))
	return catalog_out.Sum(nil)
}

func main() {
	fmt.Println(len(fmt.Sprint(packShipment())))
}
