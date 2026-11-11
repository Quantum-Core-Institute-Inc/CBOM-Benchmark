# QCI PQC Scanner on the CBOM Testbench

- Scanner: **qci-pqc, version 2.3.4**, adapter(s) `internal`
- Scanner's own CBOM: INVALID: None is not of type 'string'

Failed validating 'type' in schema['properties']['components']['items']['properties']['version']:
    {'description': 'A single disjunctive version identifier, for a '
  ; 918 components
- Translation: `tools/adapters/qci_pqc.py` 1.1; scope: `integrations/qci-pqc/scope.json`
- Run: 2026-11-11 19:37 UTC

| Metric | In declared scope | Everything |
|---|---|---|
| Recall | 68.6% | 65.1% |
| At primary site | 66.1% | 62.8% |
| Parameters correct | 55.0% | 55.1% |
| Precision | 98.8% | 98.8% |
| False positives | 3 | 3 |
|   of which in negative controls | 0 | 0 |
| PQC over-claims | 0 | 0 |
| PQC by standard name (of detected PQC) | 100.0% | 100.0% |
| System fixture: routable (of detected) | 70.6% | 70.6% |
| Ticket-ready (of detected) | 46.6% | 46.1% |
| Actionable recall | 32.0% | 30.0% |
| Field completeness | 56.8% | 56.4% |
| Deadline-weighted recall (nist) | 69.8% | 66.4% |
| Missed findings due by 2030 | 37 | 46 |
| Crypto libraries, right manifest | 96.4% | 96.4% |
| Library PQC verdicts right | n/a | n/a |
| Matched holdout recall | 74.1% | n/a |
| Broad holdout recall | 67.1% | n/a |
| Overfit gap (points) | -3.1 | n/a |
|   lower 95% bound | -8.3 | n/a |
| Negative-control gap (FPs per file) | 0.0 | n/a |
| Holdout crypto libraries, right manifest | 87.5% | n/a |
| Library gap (points, not gated) | 5.0 | n/a |

Risk-signal coverage (in scope): strict 251/366, plus 14 covered only by a QCI category signal, combined **72.4%**.

| Bucket | Detected | Recall | At primary site | Params |
|---|---|---|---|---|
| 1/c | 14/20 | 70.0% | 70.0% | 42.9% |
| 1/csharp | 9/13 | 69.2% | 69.2% | 11.1% |
| 1/go | 14/20 | 70.0% | 70.0% | 42.9% |
| 1/java | 15/16 | 93.8% | 93.8% | 66.7% |
| 1/javascript | 14/17 | 82.4% | 82.4% | 42.9% |
| 1/python | 15/16 | 93.8% | 93.8% | 100.0% |
| 2/c | 2/6 | 33.3% | 33.3% | 0.0% |
| 2/csharp | 3/6 | 50.0% | 50.0% | 0.0% |
| 2/go | 5/6 | 83.3% | 83.3% | 20.0% |
| 2/java | 6/8 | 75.0% | 62.5% | 83.3% |
| 2/python | 8/9 | 88.9% | 77.8% | 87.5% |
| 2/typescript | 3/7 | 42.9% | 42.9% | 0.0% |
| 3/java | 5/7 | 71.4% | 71.4% | 40.0% |
| 3/python | 7/9 | 77.8% | 55.6% | 14.3% |
| 4/assets | 22/54 | 40.7% | 40.7% | 81.8% |
| 5/c | 2/3 | 66.7% | 66.7% | 50.0% |
| 5/java | 0/5 | 0.0% | 0.0% | n/a |
| 5/javascript | 0/3 | 0.0% | 0.0% | n/a |
| 5/python | 2/7 | 28.6% | 28.6% | 50.0% |
| deadcode/c | 2/2 | 100.0% | 100.0% | 50.0% |
| deadcode/go | 1/2 | 50.0% | 50.0% | 100.0% |
| deadcode/java | 2/2 | 100.0% | 100.0% | 100.0% |
| deadcode/javascript | 1/2 | 50.0% | 50.0% | 0.0% |
| deadcode/python | 2/2 | 100.0% | 100.0% | 100.0% |
| mixed/c | 9/13 | 69.2% | 69.2% | 22.2% |
| mixed/go | 11/12 | 91.7% | 91.7% | 27.3% |
| mixed/java | 11/13 | 84.6% | 84.6% | 54.5% |
| mixed/javascript | 4/8 | 50.0% | 50.0% | 25.0% |
| mixed/python | 12/12 | 100.0% | 100.0% | 50.0% |
| mixed/typescript | 3/4 | 75.0% | 75.0% | 0.0% |
| pqc/assets | 19/25 | 76.0% | 76.0% | 100.0% |
| pqc/go | 1/4 | 25.0% | 25.0% | 100.0% |
| pqc/java | 4/6 | 66.7% | 66.7% | 50.0% |
| pqc/python | 6/6 | 100.0% | 100.0% | 50.0% |
| system/artifacts | 4/4 | 100.0% | 100.0% | 100.0% |
| system/assets | 5/9 | 55.6% | 55.6% | 40.0% |
| system/go | 3/3 | 100.0% | 33.3% | 33.3% |
| system/java | 2/2 | 100.0% | 50.0% | 50.0% |
| system/python | 3/3 | 100.0% | 33.3% | 33.3% |

29 expected findings are outside the declared scope and not counted; 5 were detected anyway.

**Unmapped QCI names:** Node-crypto, RC4, RIPEMD-160, SHA3-384, SHA3-512, SHAKE128, TLS, unspecified. Add them to the adapter.

## Holdout (private seed)

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


## Gates

Testbench 2.4.0; stamp `{"release": "2.4.0", "methodology": "2.3", "findings": 393, "answer_key": "c9f27be6d6a5098a", "corpus": "a0087dc174d516e4", "scorer": "4449df0c3850c51f", "policy": "nist:c78f618c306e7d48", "adapter": "55035867d66228df"}`.

**FAILED** (3):

- params_accuracy = 55.0 is below the gate minimum 63.4
- ticket_ready_pct = 46.6 is below the gate minimum 54.3
- cbom_schema_valid = 0 is below the gate minimum 1

Skipped:

- library_pq_verdict_accuracy: the scanner gave no PQC-capability verdicts for libraries, so there is nothing to judge


Details: `scorecard.md` (declared scope + signal coverage), `scorecard-full.md` (everything), `raw/` (the scanner's own outputs).
