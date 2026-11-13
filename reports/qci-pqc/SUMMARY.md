# QCI PQC Scanner on the CBOM Testbench

- Scanner: **qci-pqc, version 2.3.4.5**, adapter(s) `internal`
- Scanner's own CBOM: valid CycloneDX 1.6; 920 components
- Translation: `tools/adapters/qci_pqc.py` 1.3; scope: `integrations/qci-pqc/scope.json`
- Run: 2026-11-13 17:13 UTC

| Metric | In declared scope | Everything |
|---|---|---|
| Recall | 79.8% | 76.6% |
| At primary site | 77.5% | 74.4% |
| Parameters correct | 92.6% | 92.7% |
| Precision | 100.0% | 100.0% |
| False positives | 0 | 0 |
|   of which in negative controls | 0 | 0 |
| PQC over-claims | 0 | 0 |
| PQC by standard name (of detected PQC) | 100.0% | 100.0% |
| System fixture: routable (of detected) | 76.2% | 76.2% |
| Ticket-ready (of detected) | 87.5% | 86.9% |
| Actionable recall | 69.8% | 66.6% |
| Field completeness | 65.6% | 65.3% |
| Deadline-weighted recall (nist) | 81.6% | 78.7% |
| Missed findings due by 2030 | 25 | 31 |
| Crypto libraries, right manifest | 96.4% | 96.4% |
| Library PQC verdicts right | n/a | n/a |
| Matched holdout recall | 78.0% | n/a |
| Broad holdout recall | 79.2% | n/a |
| Overfit gap (points) | -1.6 | n/a |
|   lower 95% bound | -6.5 | n/a |
| Negative-control gap (FPs per file) | 0.0 | n/a |
| Holdout crypto libraries, right manifest | 86.7% | n/a |
| Library gap (points, not gated) | 5.3 | n/a |

Risk-signal coverage (in scope): strict 312/391, plus 10 covered only by a QCI category signal, combined **82.4%**.

| Bucket | Detected | Recall | At primary site | Params |
|---|---|---|---|---|
| 1/c | 18/20 | 90.0% | 90.0% | 100.0% |
| 1/csharp | 9/13 | 69.2% | 69.2% | 100.0% |
| 1/go | 19/20 | 95.0% | 95.0% | 100.0% |
| 1/java | 15/16 | 93.8% | 93.8% | 100.0% |
| 1/javascript | 15/17 | 88.2% | 88.2% | 100.0% |
| 1/python | 15/16 | 93.8% | 93.8% | 100.0% |
| 2/c | 2/6 | 33.3% | 33.3% | 100.0% |
| 2/csharp | 4/6 | 66.7% | 66.7% | 75.0% |
| 2/go | 5/6 | 83.3% | 83.3% | 80.0% |
| 2/java | 6/8 | 75.0% | 62.5% | 100.0% |
| 2/python | 8/9 | 88.9% | 77.8% | 100.0% |
| 2/typescript | 3/7 | 42.9% | 42.9% | 66.7% |
| 3/java | 5/7 | 71.4% | 71.4% | 40.0% |
| 3/python | 7/9 | 77.8% | 55.6% | 14.3% |
| 4/assets | 39/54 | 72.2% | 72.2% | 97.4% |
| 5/c | 11/11 | 100.0% | 100.0% | 100.0% |
| 5/java | 6/11 | 54.5% | 54.5% | 100.0% |
| 5/javascript | 11/11 | 100.0% | 100.0% | 100.0% |
| 5/python | 2/7 | 28.6% | 28.6% | 50.0% |
| deadcode/c | 2/2 | 100.0% | 100.0% | 100.0% |
| deadcode/go | 2/2 | 100.0% | 100.0% | 100.0% |
| deadcode/java | 2/2 | 100.0% | 100.0% | 100.0% |
| deadcode/javascript | 1/2 | 50.0% | 50.0% | 100.0% |
| deadcode/python | 2/2 | 100.0% | 100.0% | 100.0% |
| mixed/c | 9/13 | 69.2% | 69.2% | 100.0% |
| mixed/go | 12/12 | 100.0% | 100.0% | 91.7% |
| mixed/java | 11/13 | 84.6% | 84.6% | 81.8% |
| mixed/javascript | 4/8 | 50.0% | 50.0% | 100.0% |
| mixed/python | 12/12 | 100.0% | 100.0% | 100.0% |
| mixed/typescript | 3/4 | 75.0% | 75.0% | 100.0% |
| pqc/assets | 19/25 | 76.0% | 76.0% | 100.0% |
| pqc/go | 2/4 | 50.0% | 50.0% | 100.0% |
| pqc/java | 4/6 | 66.7% | 66.7% | 100.0% |
| pqc/python | 6/7 | 85.7% | 85.7% | 100.0% |
| system/artifacts | 6/6 | 100.0% | 100.0% | 100.0% |
| system/assets | 7/9 | 77.8% | 77.8% | 85.7% |
| system/go | 3/3 | 100.0% | 33.3% | 33.3% |
| system/java | 2/2 | 100.0% | 50.0% | 50.0% |
| system/python | 3/3 | 100.0% | 33.3% | 33.3% |

21 expected findings are outside the declared scope and not counted; 2 were detected anyway.

**Unmapped QCI names:** Node-crypto, TLS, unspecified. Add them to the adapter.

## Holdout (private seed)

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


## Gates

Testbench 2.6.6; stamp `{"release": "2.6.6", "methodology": "2.3", "findings": 410, "answer_key": "b0867a4029ea0c56", "corpus": "9ecce20d59d14efb", "scorer": "0dead3635a2ae115", "policy": "nist:c78f618c306e7d48", "adapter": "c71a627874e536b5"}`.

**All gates passed.**

Skipped:

- library_pq_verdict_accuracy: the scanner gave no PQC-capability verdicts for libraries, so there is nothing to judge


Details: `scorecard.md` (declared scope + signal coverage), `scorecard-full.md` (everything), `raw/` (the scanner's own outputs).
