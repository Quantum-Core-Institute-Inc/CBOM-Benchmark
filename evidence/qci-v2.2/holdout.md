## Holdout and overfit gap

Holdout recall **76.1%** on 297 findings across 30 families (131 tier/language/family cells). The published cases in the same cells (hand-written plus calibration), weighted the same way: **71.8%**.

Overfit gap: **-4.3 points** (95% interval -9.3 to +0.6). Within sampling noise: the published score generalizes.

| | Published | Holdout | Holdout n |
|---|---|---|---|
| Tier 1 | 76.3% | 81.0% | 58 |
| Tier 2 | 73.2% | 74.0% | 96 |
| Tier 3 | 78.6% | 85.7% | 14 |
| Tier 4 | 53.3% | 62.3% | 61 |
| Tier pqc | 100.0% | 100.0% | 19 |
| Tier mixed | 74.1% | 79.6% | 49 |

Holdout false positives: 52 (21 in negative controls), PQC over-claims: 15.

| Family | Published | Holdout | Gap |
|---|---|---|---|
| TLS-1.0 | 100.0% (n=2) | 66.7% (n=3) | +33.3 |
| TLS-1.2 | 33.3% (n=3) | 0.0% (n=4) | +33.3 |
| DSA | 93.8% (n=16) | 71.4% (n=7) | +22.3 |
| SHA-1 | 81.5% (n=27) | 64.7% (n=17) | +16.8 |
| PBKDF2 | 88.9% (n=9) | 75.0% (n=4) | +13.9 |
| 3DES | 76.7% (n=30) | 76.2% (n=21) | +0.5 |
| ChaCha20-Poly1305 | 100.0% (n=10) | 100.0% (n=5) | +0.0 |
| DES | 100.0% (n=5) | 100.0% (n=5) | +0.0 |
| ML-DSA | 100.0% (n=7) | 100.0% (n=9) | +0.0 |
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
| RSA | 79.2% (n=48) | 80.6% (n=36) | -1.4 |
| Ed25519 | 50.0% (n=12) | 53.8% (n=13) | -3.8 |
| AES | 64.4% (n=45) | 71.4% (n=42) | -7.0 |
| HMAC | 92.9% (n=42) | 100.0% (n=24) | -7.1 |
| X25519 | 92.9% (n=14) | 100.0% (n=8) | -7.1 |
| EC | 67.5% (n=40) | 77.5% (n=40) | -10.0 |
| SHA-256 | 87.5% (n=16) | 100.0% (n=7) | -12.5 |
| DH | 86.7% (n=15) | 100.0% (n=9) | -13.3 |
| MD5 | 50.0% (n=18) | 66.7% (n=15) | -16.7 |
| TLS-1.1 | 25.0% (n=4) | 100.0% (n=3) | -75.0 |

**Broad set:** 52/73 (71.2%) on API spellings, import styles and indirections the published corpus doesn't use. This measures coverage beyond the corpus; it isn't compared with anything.

Not generated yet, so outside the comparison: TLS protocol versions and cipher suites configured in code.

Per-family rows are small samples; read the overall gap and its interval first. Holdout files and per-finding results stay with whoever holds the seed.

### Negative controls, published vs unseen

| | Files | False positives | per file | PQC over-claims |
|---|---|---|---|---|
| Published | 10 | 0 | 0.0 | 0 |
| Holdout | 24 | 21 | 0.88 | 6 |

Gap: **+0.88 false positives per file**. Unseen negatives fare markedly worse: false-positive suppression was fitted to the published files.

### Crypto libraries, published vs generated manifests

Direct dependencies found in the right manifest: published 24.7% (weighted to the holdout's ecosystem mix), holdout 18.8%, gap **+6.0 points**. Holdout versions correct: 0.0%; false positives: 0.

| Ecosystem | Published | Holdout |
|---|---|---|
| conan | 50.0% (n=2) | None% (n=0) |
| golang | 33.3% (n=3) | 50.0% (n=2) |
| maven | 40.0% (n=5) | 16.7% (n=6) |
| npm | 0.0% (n=5) | 0.0% (n=6) |
| pypi | 44.4% (n=9) | 50.0% (n=2) |
