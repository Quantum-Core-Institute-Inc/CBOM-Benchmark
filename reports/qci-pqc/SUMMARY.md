# QCI PQC Scanner on the CBOM Testbench

- Scanner: **qci-pqc, version 2.3.4**, adapter(s) `internal`
- Scanner's own CBOM: INVALID: None is not of type 'string'

Failed validating 'type' in schema['properties']['components']['items']['properties']['version']:
    {'description': 'A single disjunctive version identifier, for a '
  ; 893 components
- Translation: `tools/adapters/qci_pqc.py` 1.1; scope: `integrations/qci-pqc/scope.json`
- Run: 2026-11-11 18:26 UTC

| Metric | In declared scope | Everything |
|---|---|---|
| Recall | 74.8% | 71.0% |
| At primary site | 72.0% | 68.3% |
| Parameters correct | 57.4% | 57.5% |
| Precision | 99.6% | 99.6% |
| False positives | 1 | 1 |
|   of which in negative controls | 0 | 0 |
| PQC over-claims | 0 | 0 |
| PQC by standard name (of detected PQC) | 100.0% | 100.0% |
| System fixture: routable (of detected) | 70.6% | 70.6% |
| Ticket-ready (of detected) | 48.5% | 47.9% |
| Actionable recall | 36.3% | 34.0% |
| Field completeness | 56.3% | 56.0% |
| Deadline-weighted recall (nist) | 75.3% | 71.8% |
| Missed findings due by 2030 | 26 | 33 |
| Crypto libraries, right manifest | 96.4% | 96.4% |
| Library PQC verdicts right | n/a | n/a |
| Matched holdout recall | 74.8% | n/a |
| Broad holdout recall | 64.5% | n/a |
| Overfit gap (points) | -0.9 | n/a |
|   lower 95% bound | -5.9 | n/a |
| Negative-control gap (FPs per file) | 0.0 | n/a |
| Holdout crypto libraries, right manifest | 87.5% | n/a |
| Library gap (points, not gated) | 5.0 | n/a |

Risk-signal coverage (in scope): strict 235/314, plus 11 covered only by a QCI category signal, combined **78.3%**.

| Bucket | Detected | Recall | At primary site | Params |
|---|---|---|---|---|
| 1/c | 14/20 | 70.0% | 70.0% | 42.9% |
| 1/go | 14/20 | 70.0% | 70.0% | 42.9% |
| 1/java | 15/16 | 93.8% | 93.8% | 66.7% |
| 1/javascript | 14/17 | 82.4% | 82.4% | 42.9% |
| 1/python | 15/16 | 93.8% | 93.8% | 100.0% |
| 2/c | 2/6 | 33.3% | 33.3% | 0.0% |
| 2/go | 5/6 | 83.3% | 83.3% | 20.0% |
| 2/java | 6/8 | 75.0% | 62.5% | 83.3% |
| 2/python | 8/9 | 88.9% | 77.8% | 87.5% |
| 2/typescript | 3/7 | 42.9% | 42.9% | 0.0% |
| 3/java | 5/7 | 71.4% | 71.4% | 40.0% |
| 3/python | 7/9 | 77.8% | 55.6% | 14.3% |
| 4/assets | 20/34 | 58.8% | 58.8% | 85.0% |
| 5/java | 0/5 | 0.0% | 0.0% | n/a |
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
| pqc/assets | 19/20 | 95.0% | 95.0% | 100.0% |
| pqc/go | 1/4 | 25.0% | 25.0% | 100.0% |
| pqc/java | 4/4 | 100.0% | 100.0% | 50.0% |
| pqc/python | 6/6 | 100.0% | 100.0% | 50.0% |
| system/artifacts | 4/4 | 100.0% | 100.0% | 100.0% |
| system/assets | 5/9 | 55.6% | 55.6% | 40.0% |
| system/go | 3/3 | 100.0% | 33.3% | 33.3% |
| system/java | 2/2 | 100.0% | 50.0% | 50.0% |
| system/python | 3/3 | 100.0% | 33.3% | 33.3% |

26 expected findings are outside the declared scope and not counted; 5 were detected anyway.

**Unmapped QCI names:** Node-crypto, RC4, RIPEMD-160, SHA3-384, SHA3-512, SHAKE128, TLS, unspecified. Add them to the adapter.

## Holdout (private seed)

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


## Gates

Testbench 2.3.0; stamp `{"release": "2.3.0", "methodology": "2.3", "findings": 338, "answer_key": "9e3fdc9bed8b4bf4", "corpus": "069efaeef382b6bd", "scorer": "09d445faf1a63801", "policy": "nist:732cd8a8d8f317e9", "adapter": "55035867d66228df"}`.

**FAILED** (4):

- params_accuracy = 57.4 is below the gate minimum 65.0
- ticket_ready_pct = 48.5 is below the gate minimum 55.6
- deadline_weighted_recall = 75.3 is below the gate minimum 76.5
- cbom_schema_valid = 0 is below the gate minimum 1

Skipped:

- library_pq_verdict_accuracy: the scanner gave no PQC-capability verdicts for libraries, so there is nothing to judge


Details: `scorecard.md` (declared scope + signal coverage), `scorecard-full.md` (everything), `raw/` (the scanner's own outputs).
