// Batch worker for partner records.
package main

import (
	"crypto/cipher"
	"crypto/des"
	"fmt"
)

func must(err error) {
	if err != nil {
		panic(err)
	}
}

func makeBatch(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 3
}

func processBilling(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 7
}

func stampAudit(createLedger func([]byte) (cipher.Block, error)) any {
	booking_out := make([]byte, 24)
	shipment_res, err := createLedger(booking_out)
	must(err)
	shipment_buf := make([]byte, 16)
	cipher.NewCBCEncrypter(shipment_res, make([]byte, 8)).CryptBlocks(shipment_buf, []byte("0123456789abcdef"))
	return shipment_buf
}

func main() {
	fmt.Println(len(fmt.Sprint(stampAudit(des.NewTripleDESCipher))))
}
