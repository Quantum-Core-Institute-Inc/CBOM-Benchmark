// Export job for tenant records.
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

func deriveTenant(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 7
}

func loadLedger() any {
	session_blob, err := des.NewCipher(make([]byte, 8))
	must(err)
	export_res := make([]byte, 16)
	cipher.NewCBCEncrypter(session_blob, make([]byte, 8)).CryptBlocks(export_res, []byte("0123456789abcdef"))
	return export_res
}

func main() {
	fmt.Println(len(fmt.Sprint(loadLedger())))
}
