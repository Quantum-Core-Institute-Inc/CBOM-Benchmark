## Holdout and overfit gap

Holdout recall **66.2%** on 349 findings across 34 families (146 tier/language/family cells). The published cases in the same cells (hand-written plus calibration), weighted the same way: **65.4%**.

Overfit gap: **-0.8 points** (95% interval -5.7 to +4.2). Within sampling noise: the published score generalizes.

| | Published | Holdout | Holdout n |
|---|---|---|---|
| Tier 1 | 80.6% | 79.6% | 54 |
| Tier 2 | 69.9% | 68.7% | 99 |
| Tier 3 | 80.0% | 86.7% | 15 |
| Tier 4 | 44.4% | 52.1% | 96 |
| Tier 5 | 0.0% | 0.0% | 10 |
| Tier pqc | 81.5% | 70.4% | 27 |
| Tier mixed | 81.2% | 79.2% | 48 |

Holdout false positives: 13 (0 in negative controls), PQC over-claims: 0.

| Family | Published | Holdout | Gap |
|---|---|---|---|
| TLS-1.0 | 100.0% (n=2) | 50.0% (n=4) | +50.0 |
| TLS-1.3 | 100.0% (n=3) | 50.0% (n=4) | +50.0 |
| MD5 | 55.6% (n=18) | 36.4% (n=11) | +19.2 |
| ML-DSA | 100.0% (n=7) | 83.3% (n=6) | +16.7 |
| SHA-1 | 68.6% (n=35) | 54.5% (n=22) | +14.0 |
| SHA-256 | 88.9% (n=9) | 75.0% (n=4) | +13.9 |
| 3DES | 76.7% (n=30) | 65.4% (n=26) | +11.3 |
| DH | 88.9% (n=18) | 80.0% (n=15) | +8.9 |
| TLS-1.2 | 33.3% (n=3) | 25.0% (n=4) | +8.3 |
| HMAC | 90.2% (n=41) | 83.3% (n=42) | +6.9 |
| PBKDF2 | 94.4% (n=18) | 87.5% (n=8) | +6.9 |
| Ed25519 | 66.7% (n=15) | 63.6% (n=11) | +3.0 |
| RSA | 88.0% (n=50) | 86.5% (n=37) | +1.5 |
| AES | 58.3% (n=48) | 57.4% (n=47) | +0.9 |
| ChaCha20-Poly1305 | 100.0% (n=4) | 100.0% (n=6) | +0.0 |
| LMS | 0.0% (n=2) | 0.0% (n=3) | +0.0 |
| ML-KEM | 100.0% (n=6) | 100.0% (n=9) | +0.0 |
| RC4 | 0.0% (n=5) | 0.0% (n=4) | +0.0 |
| SHA-512 | 0.0% (n=1) | 0.0% (n=3) | +0.0 |
| SHA3-256 | 0.0% (n=12) | 0.0% (n=3) | +0.0 |
| TLS_AES_256_GCM_SHA384 | 0.0% (n=1) | 0.0% (n=2) | +0.0 |
| TLS_CHACHA20_POLY1305_SHA256 | 0.0% (n=1) | 0.0% (n=1) | +0.0 |
| TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256 | 0.0% (n=1) | 0.0% (n=4) | +0.0 |
| TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 | 0.0% (n=1) | 0.0% (n=1) | +0.0 |
| TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 | 0.0% (n=2) | 0.0% (n=2) | +0.0 |
| TLS_RSA_WITH_3DES_EDE_CBC_SHA | 0.0% (n=2) | 0.0% (n=1) | +0.0 |
| TLS_RSA_WITH_AES_128_CBC_SHA | 0.0% (n=2) | 0.0% (n=1) | +0.0 |
| TLS_RSA_WITH_AES_256_CBC_SHA | 0.0% (n=2) | 0.0% (n=2) | +0.0 |
| X25519MLKEM768 | 100.0% (n=3) | 100.0% (n=3) | +0.0 |
| XMSS | 0.0% (n=2) | 0.0% (n=2) | +0.0 |
| sntrup761x25519 | 100.0% (n=1) | 100.0% (n=1) | +0.0 |
| EC | 67.5% (n=40) | 72.7% (n=44) | -5.2 |
| X25519 | 92.9% (n=14) | 100.0% (n=10) | -7.1 |
| TLS-1.1 | 25.0% (n=4) | 66.7% (n=6) | -41.7 |

**Broad set:** 53/77 (68.8%) on API spellings, import styles and indirections the published corpus doesn't use. This measures coverage beyond the corpus; it isn't compared with anything.

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
