// PQC case: TLS client preferences with a hybrid group and a classical fallback.
package main

import (
	"crypto/tls"
	"fmt"
)

func main() {
	cfg := &tls.Config{
		MinVersion:       tls.VersionTLS13,
		CurvePreferences: []tls.CurveID{tls.X25519MLKEM768, tls.X25519},
	}
	fmt.Println(cfg.MinVersion, cfg.CurvePreferences)
}
