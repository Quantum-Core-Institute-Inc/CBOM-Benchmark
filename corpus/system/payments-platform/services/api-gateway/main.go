// api-gateway: issues partner tokens and signs outbound webhooks.
package main

import (
	"crypto/sha256"
	"encoding/hex"
	"fmt"

	cryptokit "acme.example/payments/libs/cryptokit/go"
)

func requestID(body []byte) string {
	sum := sha256.Sum256(body)
	return hex.EncodeToString(sum[:8])
}

func main() {
	body := []byte(`{"partner":"northwind","amount":"1250.00"}`)
	token := cryptokit.SignToken("partner-token", body)
	tag := cryptokit.MAC("webhook-signature", body)
	fmt.Println(requestID(body), len(token), len(tag))
}
