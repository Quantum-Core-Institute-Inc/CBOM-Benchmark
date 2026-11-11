// Dead code: a function nothing calls and a branch behind a constant that is always false.
package main

import (
	"crypto/md5"
	"crypto/rc4"
	"fmt"
)

const legacyStream = false

func oldChecksum(data []byte) [16]byte {
	return md5.Sum(data)
}

func main() {
	if legacyStream {
		c, _ := rc4.NewCipher([]byte("0123456789abcdef"))
		fmt.Println(c != nil)
	}
	fmt.Println("ok")
}
