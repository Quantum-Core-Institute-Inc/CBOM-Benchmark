// Tier 1: the partner feed is forwarded as received.
package main

import "fmt"

func main() {
	buf := []byte("settlement batch 0042")
	fmt.Printf("%x\n", buf)
}
