## Holdout and overfit gap

Holdout recall **74.1%** on 297 findings across 30 families (131 tier/language/family cells). The published cases in the same cells (hand-written plus calibration), weighted the same way: **71.0%**.

Overfit gap: **-3.1 points** (95% interval -8.3 to +1.7). Within sampling noise: the published score generalizes.

| | Published | Holdout | Holdout n |
|---|---|---|---|
| Tier 1 | 78.4% | 79.3% | 58 |
| Tier 2 | 72.4% | 70.8% | 96 |
| Tier 3 | 57.1% | 85.7% | 14 |
| Tier 4 | 53.3% | 62.3% | 61 |
| Tier pqc | 100.0% | 89.5% | 19 |
| Tier mixed | 74.1% | 79.6% | 49 |

Holdout false positives: 12 (0 in negative controls), PQC over-claims: 2.

| Family | Published | Holdout | Gap |
|---|---|---|---|
| DSA | 87.5% (n=16) | 42.9% (n=7) | +44.6 |
| TLS-1.0 | 100.0% (n=2) | 66.7% (n=3) | +33.3 |
| TLS-1.2 | 33.3% (n=3) | 0.0% (n=4) | +33.3 |
| ML-DSA | 100.0% (n=7) | 77.8% (n=9) | +22.2 |
| PBKDF2 | 88.9% (n=9) | 75.0% (n=4) | +13.9 |
| 3DES | 80.0% (n=30) | 76.2% (n=21) | +3.8 |
| RSA | 81.2% (n=48) | 80.6% (n=36) | +0.7 |
| ChaCha20-Poly1305 | 100.0% (n=10) | 100.0% (n=5) | +0.0 |
| DES | 100.0% (n=5) | 100.0% (n=5) | +0.0 |
| ML-KEM | 100.0% (n=6) | 100.0% (n=9) | +0.0 |
| RC4 | 0.0% (n=5) | 0.0% (n=4) | +0.0 |
| SHA3-256 | 0.0% (n=9) | 0.0% (n=4) | +0.0 |
| TLS-1.3 | 100.0% (n=3) | 100.0% (n=1) | +0.0 |
| TLS_AES_256_GCM_SHA384 | 0.0% (n=1) | 0.0% (n=1) | +0.0 |
| TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 | 0.0% (n=1) | 0.0% (n=1) | +0.0 |
| TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 | 0.0% (n=2) | 0.0% (n=1) | +0.0 |
| TLS_RSA_WITH_3DES_EDE_CBC_SHA | 0.0% (n=2) | 0.0% (n=1) | +0.0 |
| TLS_RSA_WITH_AES_256_CBC_SHA | 0.0% (n=2) | 0.0% (n=1) | +0.0 |
| X25519MLKEM768 | 100.0% (n=3) | 100.0% (n=1) | +0.0 |
| sntrup761x25519 | 100.0% (n=1) | 100.0% (n=1) | +0.0 |
| SHA-1 | 51.9% (n=27) | 52.9% (n=17) | -1.1 |
| AES | 68.9% (n=45) | 71.4% (n=42) | -2.5 |
| Ed25519 | 50.0% (n=12) | 53.8% (n=13) | -3.8 |
| SHA-256 | 93.8% (n=16) | 100.0% (n=7) | -6.2 |
| HMAC | 92.9% (n=42) | 100.0% (n=24) | -7.1 |
| X25519 | 92.9% (n=14) | 100.0% (n=8) | -7.1 |
| EC | 70.0% (n=40) | 77.5% (n=40) | -7.5 |
| MD5 | 55.6% (n=18) | 66.7% (n=15) | -11.1 |
| DH | 86.7% (n=15) | 100.0% (n=9) | -13.3 |
| TLS-1.1 | 25.0% (n=4) | 100.0% (n=3) | -75.0 |

**Broad set:** 49/73 (67.1%) on API spellings, import styles and indirections the published corpus doesn't use. This measures coverage beyond the corpus; it isn't compared with anything.

Not generated yet, so outside the comparison: TLS protocol versions and cipher suites configured in code.

Per-family rows are small samples; read the overall gap and its interval first. Holdout files and per-finding results stay with whoever holds the seed.

### Negative controls, published vs unseen

| | Files | False positives | per file | PQC over-claims |
|---|---|---|---|---|
| Published | 10 | 0 | 0.0 | 0 |
| Holdout | 24 | 0 | 0.0 | 0 |

Gap: **+0.0 false positives per file**. Within the expected range.

### Crypto libraries, published vs generated manifests

Direct dependencies found in the right manifest: published 92.5% (weighted to the holdout's ecosystem mix), holdout 87.5%, gap **+5.0 points**. Holdout versions correct: 100.0%; false positives: 1.

| Ecosystem | Published | Holdout |
|---|---|---|
| conan | 100.0% (n=2) | None% (n=0) |
| golang | 100.0% (n=3) | 100.0% (n=2) |
| maven | 80.0% (n=5) | 66.7% (n=6) |
| npm | 100.0% (n=5) | 100.0% (n=6) |
| pypi | 100.0% (n=9) | 100.0% (n=2) |
