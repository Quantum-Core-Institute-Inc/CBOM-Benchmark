# QCI PQC Scanner on the CBOM Testbench

- Scanner: **qci-pqc, version 2.3.4.3**, adapter(s) `internal`
- Scanner's own CBOM: valid CycloneDX 1.6; 857 components
- Translation: `tools/adapters/qci_pqc.py` 1.2; scope: `integrations/qci-pqc/scope.json`
- Run: 2026-11-13 14:15 UTC

| Metric | In declared scope | Everything |
|---|---|---|
| Recall | 65.5% | 62.2% |
| At primary site | 63.2% | 60.0% |
| Parameters correct | 90.8% | 90.2% |
| Precision | 100.0% | 100.0% |
| False positives | 0 | 0 |
|   of which in negative controls | 0 | 0 |
| PQC over-claims | 0 | 0 |
| PQC by standard name (of detected PQC) | 100.0% | 100.0% |
| System fixture: routable (of detected) | 64.3% | 64.3% |
| Ticket-ready (of detected) | 81.3% | 80.0% |
| Actionable recall | 53.3% | 49.8% |
| Field completeness | 62.7% | 62.3% |
| Deadline-weighted recall (nist) | 66.8% | 63.4% |
| Missed findings due by 2030 | 43 | 53 |
| Crypto libraries, right manifest | 96.4% | 96.4% |
| Library PQC verdicts right | n/a | n/a |
| Matched holdout recall | 68.2% | n/a |
| Broad holdout recall | 70.1% | n/a |
| Overfit gap (points) | -0.8 | n/a |
|   lower 95% bound | -5.6 | n/a |
| Negative-control gap (FPs per file) | 0.0 | n/a |
| Holdout crypto libraries, right manifest | 86.7% | n/a |
| Library gap (points, not gated) | 5.3 | n/a |

Risk-signal coverage (in scope): strict 251/383, plus 14 covered only by a QCI category signal, combined **69.2%**.

| Bucket | Detected | Recall | At primary site | Params |
|---|---|---|---|---|
| 1/c | 14/20 | 70.0% | 70.0% | 100.0% |
| 1/csharp | 9/13 | 69.2% | 69.2% | 100.0% |
| 1/go | 15/20 | 75.0% | 75.0% | 100.0% |
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
| 4/assets | 22/54 | 40.7% | 40.7% | 95.5% |
| 5/c | 0/11 | 0.0% | 0.0% | n/a |
| 5/java | 0/5 | 0.0% | 0.0% | n/a |
| 5/javascript | 0/11 | 0.0% | 0.0% | n/a |
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
| pqc/go | 1/4 | 25.0% | 25.0% | 100.0% |
| pqc/java | 4/6 | 66.7% | 66.7% | 100.0% |
| pqc/python | 6/7 | 85.7% | 85.7% | 100.0% |
| system/artifacts | 1/4 | 25.0% | 25.0% | 100.0% |
| system/assets | 5/9 | 55.6% | 55.6% | 80.0% |
| system/go | 3/3 | 100.0% | 33.3% | 33.3% |
| system/java | 2/2 | 100.0% | 50.0% | 50.0% |
| system/python | 3/3 | 100.0% | 33.3% | 33.3% |

29 expected findings are outside the declared scope and not counted; 4 were detected anyway.

**Unmapped QCI names:** Node-crypto, TLS, unspecified. Add them to the adapter.

## Holdout (private seed)

Holdout recall **68.2%** on 349 findings across 34 families (146 tier/language/family cells). The published cases in the same cells (hand-written plus calibration), weighted the same way: **67.4%**.

Overfit gap: **-0.8 points** (95% interval -5.6 to +4.2). Within sampling noise: the published score generalizes.

| | Published | Holdout | Holdout n |
|---|---|---|---|
| Tier 1 | 86.1% | 85.2% | 54 |
| Tier 2 | 73.0% | 71.7% | 99 |
| Tier 3 | 80.0% | 86.7% | 15 |
| Tier 4 | 44.4% | 52.1% | 96 |
| Tier 5 | 0.0% | 0.0% | 10 |
| Tier pqc | 81.5% | 70.4% | 27 |
| Tier mixed | 83.3% | 81.2% | 48 |

Holdout false positives: 11 (0 in negative controls), PQC over-claims: 0.

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
| RC4 | 100.0% (n=5) | 100.0% (n=4) | +0.0 |
| SHA-512 | 100.0% (n=1) | 100.0% (n=3) | +0.0 |
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

**Broad set:** 54/77 (70.1%) on API spellings, import styles and indirections the published corpus doesn't use. This measures coverage beyond the corpus; it isn't compared with anything.

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

Testbench 2.6.5; stamp `{"release": "2.6.5", "methodology": "2.3", "findings": 410, "answer_key": "b0867a4029ea0c56", "corpus": "9ecce20d59d14efb", "scorer": "0dead3635a2ae115", "policy": "nist:c78f618c306e7d48", "adapter": "42ce77161a3a4c69"}`.

**All gates passed.**

Skipped:

- library_pq_verdict_accuracy: the scanner gave no PQC-capability verdicts for libraries, so there is nothing to judge


Details: `scorecard.md` (declared scope + signal coverage), `scorecard-full.md` (everything), `raw/` (the scanner's own outputs).
