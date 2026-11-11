# QCI PQC Scanner on the CBOM Testbench

- Scanner: **qci-pqc, version 0.7.0**, adapter(s) `internal`
- Scanner's own CBOM: INVALID: '2027-02-02' is not a 'date-time'

Failed validating 'format' in schema['properties']['components']['items']['properties']['cryptoProperties']['properties']['certificateProperties']['properties']['not; 775 components
- Translation: `tools/adapters/qci_pqc.py` 1.1; scope: `integrations/qci-pqc/scope.json`
- Run: 2026-11-11 18:26 UTC

| Metric | In declared scope | Everything |
|---|---|---|
| Recall | 60.5% | 57.4% |
| At primary site | 57.0% | 54.1% |
| Parameters correct | 67.9% | 68.0% |
| Precision | 87.2% | 87.4% |
| False positives | 28 | 28 |
|   of which in negative controls | 4 | 4 |
| PQC over-claims | 13 | 13 |
| PQC by standard name (of detected PQC) | 100.0% | 100.0% |
| System fixture: routable (of detected) | 64.3% | 64.3% |
| Ticket-ready (of detected) | 56.3% | 55.7% |
| Actionable recall | 34.1% | 32.0% |
| Field completeness | 46.7% | 46.3% |
| Deadline-weighted recall (nist) | 59.5% | 56.9% |
| Missed findings due by 2030 | 42 | 49 |
| Crypto libraries, right manifest | 25.0% | 25.0% |
| Library PQC verdicts right | 66.7% | 66.7% |
| Matched holdout recall | 65.0% | n/a |
| Broad holdout recall | 46.1% | n/a |
| Overfit gap (points) | -1.8 | n/a |
|   lower 95% bound | -6.8 | n/a |
| Negative-control gap (FPs per file) | 1.18 | n/a |
| Holdout crypto libraries, right manifest | 18.8% | n/a |
| Library gap (points, not gated) | 6.0 | n/a |

Risk-signal coverage (in scope): strict 190/314, plus 9 covered only by a QCI category signal, combined **63.4%**.

| Bucket | Detected | Recall | At primary site | Params |
|---|---|---|---|---|
| 1/c | 9/20 | 45.0% | 45.0% | 44.4% |
| 1/go | 5/20 | 25.0% | 25.0% | 40.0% |
| 1/java | 15/16 | 93.8% | 93.8% | 93.3% |
| 1/javascript | 3/17 | 17.6% | 17.6% | 66.7% |
| 1/python | 15/16 | 93.8% | 93.8% | 100.0% |
| 2/c | 2/6 | 33.3% | 33.3% | 50.0% |
| 2/go | 5/6 | 83.3% | 83.3% | 20.0% |
| 2/java | 6/8 | 75.0% | 62.5% | 100.0% |
| 2/python | 7/9 | 77.8% | 66.7% | 100.0% |
| 2/typescript | 2/7 | 28.6% | 28.6% | 50.0% |
| 3/java | 6/7 | 85.7% | 71.4% | 50.0% |
| 3/python | 8/9 | 88.9% | 55.6% | 25.0% |
| 4/assets | 19/34 | 55.9% | 55.9% | 84.2% |
| 5/java | 0/5 | 0.0% | 0.0% | n/a |
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
| pqc/assets | 19/20 | 95.0% | 95.0% | 100.0% |
| pqc/go | 1/4 | 25.0% | 25.0% | 0.0% |
| pqc/java | 4/4 | 100.0% | 100.0% | 100.0% |
| pqc/python | 6/6 | 100.0% | 100.0% | 50.0% |
| system/artifacts | 4/4 | 100.0% | 100.0% | 100.0% |
| system/assets | 3/9 | 33.3% | 33.3% | 66.7% |
| system/go | 2/3 | 66.7% | 0.0% | 0.0% |
| system/java | 2/2 | 100.0% | 50.0% | 50.0% |
| system/python | 3/3 | 100.0% | 33.3% | 66.7% |

26 expected findings are outside the declared scope and not counted; 4 were detected anyway.

**Unmapped QCI names:** RIPEMD-160, SHA3-384, SHA3-512, SHAKE128. Add them to the adapter.

## Holdout (private seed)

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


## Gates

Testbench 2.3.0; stamp `{"release": "2.3.0", "methodology": "2.3", "findings": 338, "answer_key": "9e3fdc9bed8b4bf4", "corpus": "069efaeef382b6bd", "scorer": "09d445faf1a63801", "policy": "nist:732cd8a8d8f317e9", "adapter": "55035867d66228df"}`.

**FAILED** (10):

- recall = 60.5 is below the gate minimum 74.8
- primary_site_recall = 57.0 is below the gate minimum 72.0
- precision = 87.2 is below the gate minimum 99.6
- negative_control_fps = 4 is above the gate maximum 0
- pqc_overclaims = 13 is above the gate maximum 0
- deadline_weighted_recall = 59.5 is below the gate minimum 76.5
- library_recall = 25.0 is below the gate minimum 96.4
- library_pq_verdict_accuracy = 66.7 is below the gate minimum 71.4
- negative_fp_gap = 1.18 is above the gate maximum 0.5
- cbom_schema_valid = 0 is below the gate minimum 1


Details: `scorecard.md` (declared scope + signal coverage), `scorecard-full.md` (everything), `raw/` (the scanner's own outputs).
