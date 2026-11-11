// Tier 1: message authentication and password-based key derivation.
package main

import (
	"crypto/hmac"
	"crypto/pbkdf2"
	"crypto/sha256"
	"crypto/sha512"
	"fmt"
)

func main() {
	mac := hmac.New(sha256.New, []byte("webhook-secret"))
	mac.Write([]byte(`{"event":"paid"}`))
	tag := mac.Sum(nil)

	key, err := pbkdf2.Key(sha512.New, "correct horse", []byte("per-user-salt"), 100000, 32)
	if err != nil {
		panic(err)
	}
	fmt.Printf("%x %x\n", tag, key)
}
