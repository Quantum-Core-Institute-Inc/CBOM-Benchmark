# QCI PQC Scanner on the CBOM Testbench

- Scanner: **qci-pqc, version 2.2.0**, adapter(s) `internal`
- Scanner's own CBOM: valid CycloneDX 1.6; 931 components
- Translation: `tools/adapters/qci_pqc.py` 1.1; scope: `integrations/qci-pqc/scope.json`
- Run: 2026-11-11 19:37 UTC

| Metric | In declared scope | Everything |
|---|---|---|
| Recall | 66.4% | 62.8% |
| At primary site | 63.4% | 60.1% |
| Parameters correct | 63.4% | 63.6% |
| Precision | 91.7% | 91.8% |
| False positives | 22 | 22 |
|   of which in negative controls | 0 | 0 |
| PQC over-claims | 7 | 7 |
| PQC by standard name (of detected PQC) | 100.0% | 100.0% |
| System fixture: routable (of detected) | 70.6% | 70.6% |
| Ticket-ready (of detected) | 54.3% | 53.8% |
| Actionable recall | 36.1% | 33.8% |
| Field completeness | 57.8% | 57.3% |
| Deadline-weighted recall (nist) | 69.0% | 65.2% |
| Missed findings due by 2030 | 35 | 45 |
| Crypto libraries, right manifest | 28.6% | 28.6% |
| Library PQC verdicts right | 71.4% | 71.4% |
| Matched holdout recall | 76.1% | n/a |
| Broad holdout recall | 71.2% | n/a |
| Overfit gap (points) | -4.3 | n/a |
|   lower 95% bound | -9.3 | n/a |
| Negative-control gap (FPs per file) | 0.88 | n/a |
| Holdout crypto libraries, right manifest | 18.8% | n/a |
| Library gap (points, not gated) | 6.0 | n/a |

Risk-signal coverage (in scope): strict 243/366, plus 14 covered only by a QCI category signal, combined **70.2%**.

| Bucket | Detected | Recall | At primary site | Params |
|---|---|---|---|---|
| 1/c | 14/20 | 70.0% | 70.0% | 50.0% |
| 1/csharp | 3/13 | 23.1% | 23.1% | 0.0% |
| 1/go | 8/20 | 40.0% | 40.0% | 50.0% |
| 1/java | 15/16 | 93.8% | 93.8% | 93.3% |
| 1/javascript | 15/17 | 88.2% | 88.2% | 53.3% |
| 1/python | 15/16 | 93.8% | 93.8% | 100.0% |
| 2/c | 2/6 | 33.3% | 33.3% | 0.0% |
| 2/csharp | 4/6 | 66.7% | 66.7% | 25.0% |
| 2/go | 5/6 | 83.3% | 83.3% | 20.0% |
| 2/java | 7/8 | 87.5% | 75.0% | 100.0% |
| 2/python | 7/9 | 77.8% | 66.7% | 100.0% |
| 2/typescript | 4/7 | 57.1% | 57.1% | 50.0% |
| 3/java | 6/7 | 85.7% | 71.4% | 50.0% |
| 3/python | 8/9 | 88.9% | 55.6% | 25.0% |
| 4/assets | 22/54 | 40.7% | 40.7% | 81.8% |
| 5/c | 0/3 | 0.0% | 0.0% | n/a |
| 5/java | 1/5 | 20.0% | 20.0% | 100.0% |
| 5/javascript | 0/3 | 0.0% | 0.0% | n/a |
| 5/python | 3/7 | 42.9% | 42.9% | 66.7% |
| deadcode/c | 2/2 | 100.0% | 100.0% | 50.0% |
| deadcode/go | 1/2 | 50.0% | 50.0% | 100.0% |
| deadcode/java | 2/2 | 100.0% | 100.0% | 100.0% |
| deadcode/javascript | 1/2 | 50.0% | 50.0% | 0.0% |
| deadcode/python | 2/2 | 100.0% | 100.0% | 100.0% |
| mixed/c | 8/13 | 61.5% | 61.5% | 25.0% |
| mixed/go | 11/12 | 91.7% | 91.7% | 27.3% |
| mixed/java | 11/13 | 84.6% | 84.6% | 63.6% |
| mixed/javascript | 4/8 | 50.0% | 50.0% | 50.0% |
| mixed/python | 12/12 | 100.0% | 100.0% | 41.7% |
| mixed/typescript | 3/4 | 75.0% | 75.0% | 33.3% |
| pqc/assets | 19/25 | 76.0% | 76.0% | 100.0% |
| pqc/go | 1/4 | 25.0% | 25.0% | 100.0% |
| pqc/java | 4/6 | 66.7% | 66.7% | 100.0% |
| pqc/python | 6/6 | 100.0% | 100.0% | 50.0% |
| system/artifacts | 4/4 | 100.0% | 100.0% | 100.0% |
| system/assets | 5/9 | 55.6% | 55.6% | 40.0% |
| system/go | 3/3 | 100.0% | 33.3% | 33.3% |
| system/java | 2/2 | 100.0% | 50.0% | 50.0% |
| system/python | 3/3 | 100.0% | 33.3% | 33.3% |

29 expected findings are outside the declared scope and not counted; 4 were detected anyway.

**Unmapped QCI names:** Node-crypto, PyCryptodome, RC4, RIPEMD-160, SHA3-384, SHA3-512, SHAKE128, TLS, npm-crypto, unspecified. Add them to the adapter.

## Holdout (private seed)

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


## Gates

Testbench 2.4.0; stamp `{"release": "2.4.0", "methodology": "2.3", "findings": 393, "answer_key": "c9f27be6d6a5098a", "corpus": "a0087dc174d516e4", "scorer": "4449df0c3850c51f", "policy": "nist:c78f618c306e7d48", "adapter": "55035867d66228df"}`.

**FAILED** (7):

- recall = 66.4 is below the gate minimum 68.6
- primary_site_recall = 63.4 is below the gate minimum 66.1
- precision = 91.7 is below the gate minimum 98.8
- pqc_overclaims = 7 is above the gate maximum 0
- deadline_weighted_recall = 69.0 is below the gate minimum 69.8
- library_recall = 28.6 is below the gate minimum 96.4
- negative_fp_gap = 0.88 is above the gate maximum 0.5


Details: `scorecard.md` (declared scope + signal coverage), `scorecard-full.md` (everything), `raw/` (the scanner's own outputs).
