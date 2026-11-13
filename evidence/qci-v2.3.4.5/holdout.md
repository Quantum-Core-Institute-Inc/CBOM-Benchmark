## Holdout and overfit gap

Holdout recall **78.0%** on 355 findings across 35 families (150 tier/language/family cells). The published cases in the same cells (hand-written plus calibration), weighted the same way: **76.4%**.

Overfit gap: **-1.6 points** (95% interval -6.5 to +3.2). Within sampling noise: the published score generalizes.

| | Published | Holdout | Holdout n |
|---|---|---|---|
| Tier 1 | 86.1% | 85.2% | 54 |
| Tier 2 | 73.0% | 71.7% | 99 |
| Tier 3 | 80.0% | 86.7% | 15 |
| Tier 4 | 66.4% | 74.0% | 96 |
| Tier 5 | 91.7% | 100.0% | 16 |
| Tier pqc | 81.5% | 77.8% | 27 |
| Tier mixed | 83.3% | 81.2% | 48 |

Holdout false positives: 11 (0 in negative controls), PQC over-claims: 0.

| Family | Published | Holdout | Gap |
|---|---|---|---|
| ML-DSA | 100.0% (n=7) | 83.3% (n=6) | +16.7 |
| SHA-256 | 88.9% (n=9) | 75.0% (n=4) | +13.9 |
| 3DES | 80.0% (n=30) | 69.2% (n=26) | +10.8 |
| DH | 88.9% (n=18) | 80.0% (n=15) | +8.9 |
| HMAC | 92.7% (n=41) | 85.7% (n=42) | +7.0 |
| PBKDF2 | 94.4% (n=18) | 87.5% (n=8) | +6.9 |
| MD5 | 61.1% (n=18) | 54.5% (n=11) | +6.6 |
| SHA-1 | 73.0% (n=37) | 66.7% (n=24) | +6.3 |
| Ed25519 | 66.7% (n=15) | 63.6% (n=11) | +3.0 |
| AES | 63.3% (n=49) | 62.5% (n=48) | +0.8 |
| ChaCha20-Poly1305 | 100.0% (n=4) | 100.0% (n=6) | +0.0 |
| DES | 100.0% (n=1) | 100.0% (n=1) | +0.0 |
| LMS | 0.0% (n=2) | 0.0% (n=3) | +0.0 |
| ML-KEM | 100.0% (n=6) | 100.0% (n=9) | +0.0 |
| RC4 | 100.0% (n=5) | 100.0% (n=4) | +0.0 |
| SHA-512 | 100.0% (n=1) | 100.0% (n=3) | +0.0 |
| SHA3-256 | 0.0% (n=12) | 0.0% (n=3) | +0.0 |
| TLS-1.0 | 100.0% (n=2) | 100.0% (n=4) | +0.0 |
| TLS-1.1 | 100.0% (n=4) | 100.0% (n=6) | +0.0 |
| TLS-1.2 | 100.0% (n=3) | 100.0% (n=4) | +0.0 |
| TLS-1.3 | 100.0% (n=3) | 100.0% (n=4) | +0.0 |
| TLS_AES_256_GCM_SHA384 | 100.0% (n=1) | 100.0% (n=2) | +0.0 |
| TLS_CHACHA20_POLY1305_SHA256 | 100.0% (n=1) | 100.0% (n=1) | +0.0 |
| TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256 | 100.0% (n=1) | 100.0% (n=4) | +0.0 |
| TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 | 100.0% (n=1) | 100.0% (n=1) | +0.0 |
| TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 | 100.0% (n=2) | 100.0% (n=2) | +0.0 |
| TLS_RSA_WITH_3DES_EDE_CBC_SHA | 100.0% (n=2) | 100.0% (n=1) | +0.0 |
| TLS_RSA_WITH_AES_128_CBC_SHA | 100.0% (n=2) | 100.0% (n=1) | +0.0 |
| TLS_RSA_WITH_AES_256_CBC_SHA | 100.0% (n=2) | 100.0% (n=2) | +0.0 |
| X25519MLKEM768 | 100.0% (n=3) | 100.0% (n=3) | +0.0 |
| XMSS | 0.0% (n=2) | 0.0% (n=2) | +0.0 |
| sntrup761x25519 | 100.0% (n=1) | 100.0% (n=1) | +0.0 |
| RSA | 86.8% (n=53) | 89.7% (n=39) | -3.0 |
| EC | 70.0% (n=40) | 75.0% (n=44) | -5.0 |
| X25519 | 92.9% (n=14) | 100.0% (n=10) | -7.1 |

**Broad set:** 61/77 (79.2%) on API spellings, import styles and indirections the published corpus doesn't use. This measures coverage beyond the corpus; it isn't compared with anything.

Not generated yet, so outside the comparison: TLS protocol versions and cipher suites configured in code.

Per-family rows are small samples; read the overall gap and its interval first. Holdout files and per-finding results stay with whoever holds the seed.

### Negative controls, published vs unseen

| | Files | False positives | per file | PQC over-claims |
|---|---|---|---|---|
| Published | 12 | 0 | 0.0 | 0 |
| Holdout | 28 | 0 | 0.0 | 0 |

Gap: **+0.0 false positives per file**. Within the expected range.

### Crypto libraries, published vs generated manifests

Direct dependencies found in the right manifest: published 92.0% (weighted to the holdout's ecosystem mix), holdout 86.7%, gap **+5.3 points**. Holdout versions correct: 100.0%; false positives: 0.

| Ecosystem | Published | Holdout |
|---|---|---|
| conan | 100.0% (n=2) | 100.0% (n=4) |
| golang | 100.0% (n=3) | 100.0% (n=2) |
| maven | 80.0% (n=5) | 66.7% (n=6) |
| npm | 100.0% (n=5) | None% (n=0) |
| pypi | 100.0% (n=9) | 100.0% (n=3) |
