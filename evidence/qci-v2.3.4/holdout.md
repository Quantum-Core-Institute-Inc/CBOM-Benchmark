## Holdout and overfit gap

Holdout recall **74.8%** on 294 findings across 29 families (129 tier/language/family cells). The published cases in the same cells (hand-written plus calibration), weighted the same way: **73.9%**.

Overfit gap: **-0.9 points** (95% interval -5.9 to +4.0). Within sampling noise: the published score generalizes.

| | Published | Holdout | Holdout n |
|---|---|---|---|
| Tier 1 | 78.4% | 79.3% | 58 |
| Tier 2 | 72.4% | 70.8% | 96 |
| Tier 3 | 57.1% | 85.7% | 14 |
| Tier 4 | 67.1% | 65.5% | 58 |
| Tier pqc | 100.0% | 89.5% | 19 |
| Tier mixed | 74.1% | 79.6% | 49 |

Holdout false positives: 12 (0 in negative controls), PQC over-claims: 2.

| Family | Published | Holdout | Gap |
|---|---|---|---|
| TLS-1.2 | 50.0% (n=2) | 0.0% (n=4) | +50.0 |
| DSA | 87.5% (n=16) | 42.9% (n=7) | +44.6 |
| TLS-1.0 | 100.0% (n=2) | 66.7% (n=3) | +33.3 |
| ML-DSA | 100.0% (n=7) | 77.8% (n=9) | +22.2 |
| PBKDF2 | 88.9% (n=9) | 75.0% (n=4) | +13.9 |
| AES | 72.1% (n=43) | 71.4% (n=42) | +0.7 |
| RSA | 81.2% (n=48) | 80.6% (n=36) | +0.7 |
| ChaCha20-Poly1305 | 100.0% (n=9) | 100.0% (n=5) | +0.0 |
| DES | 100.0% (n=5) | 100.0% (n=5) | +0.0 |
| DH | 100.0% (n=12) | 100.0% (n=9) | +0.0 |
| ML-KEM | 100.0% (n=6) | 100.0% (n=9) | +0.0 |
| RC4 | 0.0% (n=5) | 0.0% (n=4) | +0.0 |
| SHA3-256 | 0.0% (n=9) | 0.0% (n=4) | +0.0 |
| TLS-1.3 | 100.0% (n=3) | 100.0% (n=1) | +0.0 |
| TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 | 0.0% (n=1) | 0.0% (n=1) | +0.0 |
| TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 | 0.0% (n=1) | 0.0% (n=1) | +0.0 |
| TLS_RSA_WITH_3DES_EDE_CBC_SHA | 0.0% (n=1) | 0.0% (n=1) | +0.0 |
| TLS_RSA_WITH_AES_256_CBC_SHA | 0.0% (n=1) | 0.0% (n=1) | +0.0 |
| X25519 | 100.0% (n=13) | 100.0% (n=8) | +0.0 |
| X25519MLKEM768 | 100.0% (n=3) | 100.0% (n=1) | +0.0 |
| sntrup761x25519 | 100.0% (n=1) | 100.0% (n=1) | +0.0 |
| SHA-1 | 51.9% (n=27) | 52.9% (n=17) | -1.1 |
| 3DES | 82.8% (n=29) | 84.2% (n=19) | -1.5 |
| HMAC | 97.5% (n=40) | 100.0% (n=24) | -2.5 |
| Ed25519 | 50.0% (n=12) | 53.8% (n=13) | -3.8 |
| SHA-256 | 93.8% (n=16) | 100.0% (n=7) | -6.2 |
| EC | 70.0% (n=40) | 77.5% (n=40) | -7.5 |
| MD5 | 55.6% (n=18) | 66.7% (n=15) | -11.1 |
| TLS-1.1 | 50.0% (n=2) | 100.0% (n=3) | -50.0 |

**Broad set:** 49/76 (64.5%) on API spellings, import styles and indirections the published corpus doesn't use. This measures coverage beyond the corpus; it isn't compared with anything.

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
