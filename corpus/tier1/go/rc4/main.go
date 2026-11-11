// Tier 1: stream cipher kept for a legacy partner feed.
package main

import (
	"crypto/rc4"
	"fmt"
)

func main() {
	stream, err := rc4.NewCipher([]byte("partner-feed-key"))
	if err != nil {
		panic(err)
	}
	buf := []byte("settlement batch 0042")
	stream.XORKeyStream(buf, buf)
	fmt.Printf("%x\n", buf)
}
