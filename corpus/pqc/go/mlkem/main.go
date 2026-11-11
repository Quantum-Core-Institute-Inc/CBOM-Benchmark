// PQC case: key encapsulation from the standard library, literal parameter set.
package main

import (
	"bytes"
	"crypto/mlkem"
	"fmt"
)

func main() {
	dk, err := mlkem.GenerateKey1024()
	if err != nil {
		panic(err)
	}
	shared, ct := dk.EncapsulationKey().Encapsulate()
	again, err := dk.Decapsulate(ct)
	if err != nil {
		panic(err)
	}
	fmt.Println(bytes.Equal(shared, again))
}
