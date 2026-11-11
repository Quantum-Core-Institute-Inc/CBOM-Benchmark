// Package cryptokit is the platform's crypto wrapper. Callers name a profile; the profile names the algorithm.
package cryptokit

import (
	"crypto"
	"crypto/hmac"
	"crypto/rand"
	"crypto/rsa"
	"crypto/sha1"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"hash"
	"os"
)

type profile struct {
	JWS     string `json:"jws"`
	KeyBits int    `json:"keyBits"`
	MAC     string `json:"mac"`
}

var macs = map[string]func() hash.Hash{"HmacSHA1": sha1.New, "HmacSHA256": sha256.New}

func load(name string) profile {
	path := os.Getenv("CRYPTO_PROFILES")
	if path == "" {
		path = "config/crypto-profiles.json"
	}
	raw, err := os.ReadFile(path)
	if err != nil {
		panic(err)
	}
	var doc struct{ Profiles map[string]profile }
	if err := json.Unmarshal(raw, &doc); err != nil {
		panic(err)
	}
	return doc.Profiles[name]
}

// SignToken signs a partner token with the profile's RS* algorithm and key size.
func SignToken(name string, payload []byte) []byte {
	p := load(name)
	key, err := rsa.GenerateKey(rand.Reader, p.KeyBits)
	if err != nil {
		panic(err)
	}
	digest := sha256.Sum256(payload)
	sig, err := rsa.SignPKCS1v15(rand.Reader, key, crypto.SHA256, digest[:])
	if err != nil {
		panic(err)
	}
	return sig
}

// MAC tags a webhook body with the profile's HMAC.
func MAC(name string, body []byte) string {
	m := hmac.New(macs[load(name).MAC], []byte("platform-webhook-key"))
	m.Write(body)
	return hex.EncodeToString(m.Sum(nil))
}
