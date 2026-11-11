# QCI PQC Scanner on the CBOM Testbench

- Scanner: **qci-pqc, version 0.7.0**, adapter(s) `internal`
- Scanner's own CBOM: INVALID: '2027-02-02' is not a 'date-time'

Failed validating 'format' in schema['properties']['components']['items']['properties']['cryptoProperties']['properties']['certificateProperties']['properties']['not; 790 components
- Translation: `tools/adapters/qci_pqc.py` 1.1; scope: `integrations/qci-pqc/scope.json`
- Run: 2026-11-11 19:37 UTC

| Metric | In declared scope | Everything |
|---|---|---|
| Recall | 54.1% | 51.4% |
| At primary site | 51.1% | 48.6% |
| Parameters correct | 66.7% | 66.8% |
| Precision | 87.2% | 87.4% |
| False positives | 29 | 29 |
|   of which in negative controls | 4 | 4 |
| PQC over-claims | 13 | 13 |
| PQC by standard name (of detected PQC) | 100.0% | 100.0% |
| System fixture: routable (of detected) | 64.3% | 64.3% |
| Ticket-ready (of detected) | 55.6% | 55.0% |
| Actionable recall | 30.1% | 28.2% |
| Field completeness | 46.6% | 46.2% |
| Deadline-weighted recall (nist) | 54.2% | 51.7% |
| Missed findings due by 2030 | 55 | 64 |
| Crypto libraries, right manifest | 25.0% | 25.0% |
| Library PQC verdicts right | 66.7% | 66.7% |
| Matched holdout recall | 64.3% | n/a |
| Broad holdout recall | 47.9% | n/a |
| Overfit gap (points) | -4.0 | n/a |
|   lower 95% bound | -9.2 | n/a |
| Negative-control gap (FPs per file) | 1.18 | n/a |
| Holdout crypto libraries, right manifest | 18.8% | n/a |
| Library gap (points, not gated) | 6.0 | n/a |

Risk-signal coverage (in scope): strict 198/366, plus 12 covered only by a QCI category signal, combined **57.4%**.

| Bucket | Detected | Recall | At primary site | Params |
|---|---|---|---|---|
| 1/c | 9/20 | 45.0% | 45.0% | 44.4% |
| 1/csharp | 4/13 | 30.8% | 30.8% | 0.0% |
| 1/go | 5/20 | 25.0% | 25.0% | 40.0% |
| 1/java | 15/16 | 93.8% | 93.8% | 93.3% |
| 1/javascript | 3/17 | 17.6% | 17.6% | 66.7% |
| 1/python | 15/16 | 93.8% | 93.8% | 100.0% |
| 2/c | 2/6 | 33.3% | 33.3% | 50.0% |
| 2/csharp | 1/6 | 16.7% | 16.7% | 100.0% |
| 2/go | 5/6 | 83.3% | 83.3% | 20.0% |
| 2/java | 6/8 | 75.0% | 62.5% | 100.0% |
| 2/python | 7/9 | 77.8% | 66.7% | 100.0% |
| 2/typescript | 2/7 | 28.6% | 28.6% | 50.0% |
| 3/java | 6/7 | 85.7% | 71.4% | 50.0% |
| 3/python | 8/9 | 88.9% | 55.6% | 25.0% |
| 4/assets | 21/54 | 38.9% | 38.9% | 81.0% |
| 5/c | 1/3 | 33.3% | 33.3% | 100.0% |
| 5/java | 0/5 | 0.0% | 0.0% | n/a |
| 5/javascript | 0/3 | 0.0% | 0.0% | n/a |
| 5/python | 0/7 | 0.0% | 0.0% | n/a |
| deadcode/c | 1/2 | 50.0% | 50.0% | 100.0% |
| deadcode/go | 0/2 | 0.0% | 0.0% | n/a |
| deadcode/java | 2/2 | 100.0% | 100.0% | 100.0% |
| deadcode/javascript | 0/2 | 0.0% | 0.0% | n/a |
| deadcode/python | 2/2 | 100.0% | 100.0% | 100.0% |
| mixed/c | 5/13 | 38.5% | 38.5% | 40.0% |
| mixed/go | 9/12 | 75.0% | 75.0% | 22.2% |
| mixed/java | 10/13 | 76.9% | 76.9% | 60.0% |
| mixed/javascript | 2/8 | 25.0% | 25.0% | 0.0% |
| mixed/python | 12/12 | 100.0% | 100.0% | 41.7% |
| mixed/typescript | 1/4 | 25.0% | 25.0% | 0.0% |
| pqc/assets | 19/25 | 76.0% | 76.0% | 100.0% |
| pqc/go | 1/4 | 25.0% | 25.0% | 0.0% |
| pqc/java | 4/6 | 66.7% | 66.7% | 100.0% |
| pqc/python | 6/6 | 100.0% | 100.0% | 50.0% |
| system/artifacts | 4/4 | 100.0% | 100.0% | 100.0% |
| system/assets | 3/9 | 33.3% | 33.3% | 66.7% |
| system/go | 2/3 | 66.7% | 0.0% | 0.0% |
| system/java | 2/2 | 100.0% | 50.0% | 50.0% |
| system/python | 3/3 | 100.0% | 33.3% | 66.7% |

29 expected findings are outside the declared scope and not counted; 4 were detected anyway.

**Unmapped QCI names:** RIPEMD-160, SHA3-384, SHA3-512, SHAKE128. Add them to the adapter.

## Holdout (private seed)

Holdout recall **64.3%** on 297 findings across 30 families (131 tier/language/family cells). The published cases in the same cells (hand-written plus calibration), weighted the same way: **60.3%**.

Overfit gap: **-4.0 points** (95% interval -9.2 to +1.1). Within sampling noise: the published score generalizes.

| | Published | Holdout | Holdout n |
|---|---|---|---|
| Tier 1 | 48.3% | 51.7% | 58 |
| Tier 2 | 69.0% | 69.8% | 96 |
| Tier 3 | 78.6% | 85.7% | 14 |
| Tier 4 | 50.8% | 62.3% | 61 |
| Tier pqc | 100.0% | 100.0% | 19 |
| Tier mixed | 49.0% | 51.0% | 49 |

Holdout false positives: 66 (38 in negative controls), PQC over-claims: 36.

| Family | Published | Holdout | Gap |
|---|---|---|---|
| TLS-1.2 | 33.3% (n=3) | 0.0% (n=4) | +33.3 |
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
| TLS_AES_256_GCM_SHA384 | 0.0% (n=1) | 0.0% (n=1) | +0.0 |
| TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 | 0.0% (n=1) | 0.0% (n=1) | +0.0 |
| TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 | 0.0% (n=2) | 0.0% (n=1) | +0.0 |
| TLS_RSA_WITH_3DES_EDE_CBC_SHA | 0.0% (n=2) | 0.0% (n=1) | +0.0 |
| TLS_RSA_WITH_AES_256_CBC_SHA | 0.0% (n=2) | 0.0% (n=1) | +0.0 |
| X25519MLKEM768 | 100.0% (n=3) | 100.0% (n=1) | +0.0 |
| sntrup761x25519 | 100.0% (n=1) | 100.0% (n=1) | +0.0 |
| HMAC | 92.9% (n=42) | 100.0% (n=24) | -7.1 |
| AES | 53.3% (n=45) | 61.9% (n=42) | -8.6 |
| MD5 | 55.6% (n=18) | 66.7% (n=15) | -11.1 |
| 3DES | 16.7% (n=30) | 33.3% (n=21) | -16.7 |
| TLS-1.0 | 50.0% (n=2) | 66.7% (n=3) | -16.7 |
| DH | 60.0% (n=15) | 77.8% (n=9) | -17.8 |
| ChaCha20-Poly1305 | 60.0% (n=10) | 80.0% (n=5) | -20.0 |
| SHA-256 | 62.5% (n=16) | 85.7% (n=7) | -23.2 |
| X25519 | 35.7% (n=14) | 62.5% (n=8) | -26.8 |
| Ed25519 | 16.7% (n=12) | 46.2% (n=13) | -29.5 |
| TLS-1.1 | 25.0% (n=4) | 100.0% (n=3) | -75.0 |

**Broad set:** 35/73 (47.9%) on API spellings, import styles and indirections the published corpus doesn't use. This measures coverage beyond the corpus; it isn't compared with anything.

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


## Gates

Testbench 2.4.0; stamp `{"release": "2.4.0", "methodology": "2.3", "findings": 393, "answer_key": "c9f27be6d6a5098a", "corpus": "a0087dc174d516e4", "scorer": "4449df0c3850c51f", "policy": "nist:c78f618c306e7d48", "adapter": "55035867d66228df"}`.

**FAILED** (10):

- recall = 54.1 is below the gate minimum 68.6
- primary_site_recall = 51.1 is below the gate minimum 66.1
- precision = 87.2 is below the gate minimum 98.8
- negative_control_fps = 4 is above the gate maximum 0
- pqc_overclaims = 13 is above the gate maximum 0
- deadline_weighted_recall = 54.2 is below the gate minimum 69.8
- library_recall = 25.0 is below the gate minimum 96.4
- library_pq_verdict_accuracy = 66.7 is below the gate minimum 71.4
- negative_fp_gap = 1.18 is above the gate maximum 0.5
- cbom_schema_valid = 0 is below the gate minimum 1


Details: `scorecard.md` (declared scope + signal coverage), `scorecard-full.md` (everything), `raw/` (the scanner's own outputs).
