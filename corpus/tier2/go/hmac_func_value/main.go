// Tier 2: the hash constructor travels as a function value.
package main

import (
	"crypto/hmac"
	"crypto/md5"
	"fmt"
)

func main() {
	newHash := md5.New
	mac := hmac.New(newHash, []byte("legacy-partner-secret"))
	mac.Write([]byte("order=1182&amount=40.00"))
	fmt.Printf("%x\n", mac.Sum(nil))
}
