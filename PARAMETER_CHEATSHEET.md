# Parameter Completeness Cheat-Sheet

A CBOM component is **parameter-complete** (and therefore eligible for full parameter-recovery credit) when it carries every parameter the ground-truth finding expects for its algorithm family.

Missing a parameter is the most common reason a detection fails “parameters correct”, “ticket-ready”, and deadline-weighted scoring.

## Required fields by family (CycloneDX 1.6 `cryptoProperties`)

| Family | Minimal parameters that must be present and correct |
|--------|------------------------------------------------------|
| RSA, DSA, DH | `keySize` (bits) |
| EC, ECDSA, ECDH | `curve` (named curve, e.g. `secp256r1`, `secp384r1`) |
| AES, 3DES, ChaCha20 | `keySize` (bits) **and** `mode` (GCM, CBC, ECB, …) |
| AES-GCM / ChaCha20-Poly1305 | also `tagLength` (bits) when the API exposes it |
| HMAC, PBKDF2 | underlying hash family + iteration count or key length where applicable |
| TLS cipher suites / groups | protocol version + named group / suite (including DH group size) |
| ML-KEM / ML-DSA | parameter set (768, 1024, 44, 65, 87, …) |
| LMS / XMSS | parameter set (e.g. `LMS_SHA256_M32_H10`) |

### Incomplete vs complete examples

**Incomplete (fails parameters_ok):**
```json
{
  "cryptoProperties": {
    "assetType": "algorithm",
    "algorithmProperties": { "variant": "RSA" }
  }
}
```

**Complete:**
```json
{
  "cryptoProperties": {
    "assetType": "algorithm",
    "algorithmProperties": {
      "variant": "RSA",
      "parameterSetIdentifier": "2048"
    }
  }
}
```

**AES-GCM incomplete:**
```json
{ "variant": "AES" }
```

**AES-GCM complete:**
```json
{
  "variant": "AES",
  "mode": "GCM",
  "keySize": 128,
  "tagLength": 128
}
```

## Why this matters

- Deadline policies (NIST IR 8547, CNSA 2.0, EO 14412) treat RSA-1024 and RSA-3072 differently.
- A ticket that says only “RSA” cannot be acted on.
- Fix-and-rescan migrations fail when the new algorithm is detected but its parameters are not.

See `tools/score.py` (`params_ok`) and `METHODOLOGY.md` section 2 for the exact matching rules. The scorecard now surfaces a dedicated Parameter Recovery section.
