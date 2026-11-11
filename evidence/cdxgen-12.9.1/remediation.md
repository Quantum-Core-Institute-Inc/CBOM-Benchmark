# Fix and rescan: cdxgen 12.9.1

**Verified remediation: 0/0 eligible migrations**, of 10. A migration is eligible when the scanner found everything it retires before the fix.

| Migration | Verdict | Retired but still reported | New algorithm found / params right | Other findings changed |
|---|---|---|---|---|
| Python: RSA-2048 PSS signing -> ML-DSA-65 | not eligible | none | no/no | none |
| Python: AES-128-ECB -> AES-256-GCM | not eligible | none | no/no | none |
| Python: 3DES-CBC -> AES-256-GCM | not eligible | none | no/no | none |
| Java: AES-128-ECB -> AES-256-GCM | not eligible | none | no/no | none |
| Java: RSA-3072 SHA256withRSA -> ML-DSA-65 (JDK 24+) | not eligible | none | no/no | none |
| Go: AES-128-CBC -> AES-256-GCM | not eligible | none | no/no | none |
| JavaScript: 3DES-CBC -> AES-256-GCM | not eligible | none | no/no | none |
| C/OpenSSL: 3DES-CBC -> AES-256-GCM | not eligible | none | no/no | none |
| nginx: drop TLS 1.0/1.1, 3DES and RSA key transport; add TLS 1.3 and X25519MLKEM768 | not eligible | none | no/no, no/no, no/no | none |
| sshd: ssh-rsa, group14-sha1, AES-CBC and HMAC-SHA1 out; Ed25519, ML-KEM hybrid, AES-GCM, HMAC-SHA512 in | not eligible | none | no/no, no/no, no/no, no/no | none |

Outside the migrated files: 0 finding(s) lost, 0 gained, false positives 0 -> 0. Any change here is the scanner being non-deterministic or reacting to files it shouldn't.
