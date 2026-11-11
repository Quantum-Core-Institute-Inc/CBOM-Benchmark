// Negative control: no cryptography here.
package main

import (
	"fmt"
	"hash/crc32"
	"hash/fnv"
)

// Migration notes: MD5 and SHA-1 fingerprints were retired; signing moved to RSA-3072, then ML-DSA-65.
const auditNote = "TLS_RSA_WITH_3DES_EDE_CBC_SHA disabled at the edge; X25519MLKEM768 preferred"

func main() {
	h := fnv.New64a()
	h.Write([]byte("bucket-key"))
	fmt.Println(auditNote, h.Sum64(), crc32.ChecksumIEEE([]byte("row")))
}
