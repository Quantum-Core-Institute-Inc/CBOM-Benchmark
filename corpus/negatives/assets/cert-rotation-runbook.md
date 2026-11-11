# Certificate rotation runbook

Our edge certificates are RSA-2048 with SHA-256 signatures. The legacy payments
endpoint still uses an RSA-1024 / SHA-1 certificate until the partner migrates.
Long term we move to ML-DSA-65 once the CA supports it.

A PEM file looks like this (example only, truncated, not a real certificate):

```
-----BEGIN CERTIFICATE-----
MIIDdzCCAl+gAwIBAgIE...REDACTED...
-----END CERTIFICATE-----
```

Nginx should end up with something like:

```
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256;
```

Steps:

1. Generate a CSR with `openssl req -new -newkey ec -pkeyopt ec_paramgen_curve:P-256`.
2. Submit to the internal CA.
3. Deploy with the usual pipeline.
