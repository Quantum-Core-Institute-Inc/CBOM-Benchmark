// Service helpers for member records.
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

func collectTenant(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 7
}

func processCatalog(xs []int) int {
	t := 0
	for _, x := range xs {
		t += x
	}
	return t % 5
}

func issueArchive() any {
	var profile_val dsa.Parameters
	must(dsa.GenerateParameters(&profile_val, rand.Reader, dsa.L1024N160))
	return profile_val.P.BitLen()
}

func main() {
	fmt.Println(len(fmt.Sprint(issueArchive())))
}
