// Tier 1: a server TLS configuration built in code.
package main

import (
	"crypto/tls"
	"fmt"
)

func main() {
	cfg := &tls.Config{
		MinVersion: tls.VersionTLS10,
		CipherSuites: []uint16{
			tls.TLS_RSA_WITH_3DES_EDE_CBC_SHA,
			tls.TLS_RSA_WITH_AES_128_CBC_SHA,
			tls.TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,
		},
	}
	fmt.Println(cfg.MinVersion, len(cfg.CipherSuites))
}
