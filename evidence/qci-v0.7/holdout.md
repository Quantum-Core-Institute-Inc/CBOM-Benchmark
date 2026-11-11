## Holdout and overfit gap

Holdout recall **65.0%** on 294 findings across 29 families (129 tier/language/family cells). The published cases in the same cells (hand-written plus calibration), weighted the same way: **63.1%**.

Overfit gap: **-1.8 points** (95% interval -6.8 to +3.3). Within sampling noise: the published score generalizes.

| | Published | Holdout | Holdout n |
|---|---|---|---|
| Tier 1 | 48.3% | 51.7% | 58 |
| Tier 2 | 69.0% | 69.8% | 96 |
| Tier 3 | 78.6% | 85.7% | 14 |
| Tier 4 | 64.5% | 65.5% | 58 |
| Tier pqc | 100.0% | 100.0% | 19 |
| Tier mixed | 49.0% | 51.0% | 49 |

Holdout false positives: 66 (38 in negative controls), PQC over-claims: 36.

| Family | Published | Holdout | Gap |
|---|---|---|---|
| TLS-1.2 | 50.0% (n=2) | 0.0% (n=4) | +50.0 |
| PBKDF2 | 88.9% (n=9) | 75.0% (n=4) | +13.9 |
| RSA | 60.4% (n=48) | 50.0% (n=36) | +10.4 |
| SHA-1 | 96.3% (n=27) | 88.2% (n=17) | +8.1 |
| DES | 0.0% (n=5) | 0.0% (n=5) | +0.0 |
| DSA | 100.0% (n=16) | 100.0% (n=7) | +0.0 |
| EC | 67.5% (n=40) | 67.5% (n=40) | +0.0 |
| ML-DSA | 100.0% (n=7) | 100.0% (n=9) | +0.0 |
| ML-KEM | 100.0% (n=6) | 100.0% (n=9) | +0.0 |
| RC4 | 0.0% (n=5) | 0.0% (n=4) | +0.0 |
| SHA3-256 | 0.0% (n=9) | 0.0% (n=4) | +0.0 |
| TLS-1.3 | 100.0% (n=3) | 100.0% (n=1) | +0.0 |
| TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 | 0.0% (n=1) | 0.0% (n=1) | +0.0 |
| TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 | 0.0% (n=1) | 0.0% (n=1) | +0.0 |
| TLS_RSA_WITH_3DES_EDE_CBC_SHA | 0.0% (n=1) | 0.0% (n=1) | +0.0 |
| TLS_RSA_WITH_AES_256_CBC_SHA | 0.0% (n=1) | 0.0% (n=1) | +0.0 |
| X25519MLKEM768 | 100.0% (n=3) | 100.0% (n=1) | +0.0 |
| sntrup761x25519 | 100.0% (n=1) | 100.0% (n=1) | +0.0 |
| HMAC | 97.5% (n=40) | 100.0% (n=24) | -2.5 |
| AES | 55.8% (n=43) | 61.9% (n=42) | -6.1 |
| DH | 66.7% (n=12) | 77.8% (n=9) | -11.1 |
| MD5 | 55.6% (n=18) | 66.7% (n=15) | -11.1 |
| TLS-1.0 | 50.0% (n=2) | 66.7% (n=3) | -16.7 |
| 3DES | 17.2% (n=29) | 36.8% (n=19) | -19.6 |
| SHA-256 | 62.5% (n=16) | 85.7% (n=7) | -23.2 |
| X25519 | 38.5% (n=13) | 62.5% (n=8) | -24.0 |
| ChaCha20-Poly1305 | 55.6% (n=9) | 80.0% (n=5) | -24.4 |
| Ed25519 | 16.7% (n=12) | 46.2% (n=13) | -29.5 |
| TLS-1.1 | 50.0% (n=2) | 100.0% (n=3) | -50.0 |

**Broad set:** 35/76 (46.1%) on API spellings, import styles and indirections the published corpus doesn't use. This measures coverage beyond the corpus; it isn't compared with anything.

Not generated yet, so outside the comparison: TLS protocol versions and cipher suites configured in code.

Per-family rows are small samples; read the overall gap and its interval first. Holdout files and per-finding results stay with whoever holds the seed.

### Negative controls, published vs unseen

| | Files | False positives | per file | PQC over-claims |
|---|---|---|---|---|
| Published | 10 | 4 | 0.4 | 2 |
| Holdout | 24 | 38 | 1.58 | 21 |

Gap: **+1.18 false positives per file**. Unseen negatives fare markedly worse: false-positive suppression was fitted to the published files.

### Crypto libraries, published vs generated manifests

Direct dependencies found in the right manifest: published 24.7% (weighted to the holdout's ecosystem mix), holdout 18.8%, gap **+6.0 points**. Holdout versions correct: 0.0%; false positives: 0.

| Ecosystem | Published | Holdout |
|---|---|---|
| conan | 0.0% (n=2) | None% (n=0) |
| golang | 33.3% (n=3) | 50.0% (n=2) |
| maven | 40.0% (n=5) | 16.7% (n=6) |
| npm | 0.0% (n=5) | 0.0% (n=6) |
| pypi | 44.4% (n=9) | 50.0% (n=2) |
