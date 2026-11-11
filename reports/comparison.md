# Scanner comparison

Shipped corpus only, every scanner on the same denominator, no declared scopes. Baselines (grep baseline) are calibration points, not products.

Testbench 2.3.0, policy nist:732cd8a8d8f317e9, answer key 9e3fdc9bed8b4bf4, scorer 09d445faf1a63801. Scanners: QCI v2.3.4 = qci-pqc, version 2.3.4 via qci_pqc 1.1; QCI v2.2 = qci-pqc, version 2.2.0 via qci_pqc 1.1; QCI v0.7 = qci-pqc, version 0.7.0 via qci_pqc 1.1; cdxgen 12.9.1 = CycloneDX Generator 12.9.1 via cdxgen 1.0; grep baseline = grep baseline.

## Overall

| | QCI v2.3.4 | QCI v2.2 | QCI v0.7 | cdxgen 12.9.1 | grep baseline |
|---|---|---|---|---|---|
| Findings | 338 | 338 | 338 | 338 | 338 |
| Recall | 71.0% | 70.4% | 57.4% | 4.4% | 69.2% |
| Recall incl. signals | 74.3% | 73.7% | 60.1% | 10.9% | n/a |
| At primary site | 68.3% | 67.2% | 54.1% | 4.4% | 64.8% |
| Parameters correct (of detected) | 57.5% | 65.1% | 68.0% | 80.0% | 55.1% |
| Precision | 99.6% | 92.2% | 87.4% | 100.0% | 59.5% |
| False positives | 1 | 20 | 28 | 0 | 159 |
|   in negative controls | 0 | 0 | 4 | 0 | 52 |
| PQC over-claims | 0 | 7 | 13 | 0 | 28 |
| PQC by standard name (of detected PQC) | 100.0% | 100.0% | 100.0% | n/a | 100.0% |
| System fixture: routable (of detected) | 70.6% | 70.6% | 64.3% | n/a | 61.5% |
| System fixture: asset links | 0.0% (0/2) † | 0.0% (0/2) † | 0.0% (0/2) † | 0.0% (0/2) † | 0.0% (0/2) † |
| Ticket-ready (of detected) | 47.9% | 55.0% | 55.7% | 80.0% | 50.9% |
| Actionable recall | 34.0% | 38.8% | 32.0% | 3.6% | 35.2% |
| Detected, due by 2030 (NIST) | 59/77 | 61/77 | 50/77 | 2/77 | 54/77 |

## Crypto libraries (dependency manifests)

| | QCI v2.3.4 | QCI v2.2 | QCI v0.7 | cdxgen 12.9.1 | grep baseline |
|---|---|---|---|---|---|
| Crypto libraries, in the right manifest | 96.4% (27/28) | 28.6% (8/28) | 25.0% (7/28) | 75.0% (21/28) | 0.0% (0/28) |
| Found anywhere (incl. no location) | 96.4% (27/28) | 28.6% (8/28) | 25.0% (7/28) | 85.7% (24/28) | 0.0% (0/28) |
| Transitive (lockfile) | 100.0% | 0.0% | 0.0% | 100.0% | 0.0% |
| Versions correct (of found) | 84.6% | 0.0% | 0.0% | 100.0% | n/a |
| PQC verdicts right | none given | 71.4% of 7 | 66.7% of 6 | none given | none given |
| False positives | 2 | 0 | 0 | 0 | 0 |

## By language (recall)

| | QCI v2.3.4 | QCI v2.2 | QCI v0.7 | cdxgen 12.9.1 | grep baseline |
|---|---|---|---|---|---|
| Python | 83.6% (56/67) | 85.1% (57/67) | 82.1% (55/67) | 0.0% (0/67) | 83.6% (56/67) |
| Java | 78.3% (47/60) | 81.7% (49/60) | 75.0% (45/60) | 0.0% (0/60) | 85.0% (51/60) |
| Go | 74.5% (35/47) | 61.7% (29/47) | 46.8% (22/47) | 0.0% (0/47) | 78.7% (37/47) |
| JavaScript / TypeScript | 65.8% (25/38) | 71.1% (27/38) | 21.1% (8/38) | 39.5% (15/38) | 84.2% (32/38) |
| C / OpenSSL | 65.9% (27/41) | 63.4% (26/41) | 41.5% (17/41) | 0.0% (0/41) | 68.3% (28/41) |
| Certificates, keys, configs | 58.2% (46/79) | 58.2% (46/79) | 54.4% (43/79) | 0.0% (0/79) | 32.9% (26/79) |
| Built artifacts (system fixture) | 66.7% (4/6) † | 66.7% (4/6) † | 66.7% (4/6) † | 0.0% (0/6) † | 66.7% (4/6) † |

## By tier (recall)

| | QCI v2.3.4 | QCI v2.2 | QCI v0.7 | cdxgen 12.9.1 | grep baseline |
|---|---|---|---|---|---|
| 1. Direct | 80.9% (72/89) | 75.3% (67/89) | 52.8% (47/89) | 9.0% (8/89) | 82.0% (73/89) |
| 2. Indirection | 66.7% (24/36) | 69.4% (25/36) | 61.1% (22/36) | 5.6% (2/36) | 94.4% (34/36) |
| 3. Cross-file | 75.0% (12/16) | 87.5% (14/16) | 87.5% (14/16) | 0.0% (0/16) | 100.0% (16/16) |
| 4. Non-code assets | 43.5% (20/46) | 43.5% (20/46) | 41.3% (19/46) | 0.0% (0/46) | 32.6% (15/46) |
| 5. Adversarial | 29.4% (5/17) | 35.3% (6/17) | 11.8% (2/17) | 0.0% (0/17) | 0.0% (0/17) |
| Post-quantum | 88.9% (32/36) | 88.9% (32/36) | 88.9% (32/36) | 0.0% (0/36) | 58.3% (21/36) |
| Mixed files | 80.6% (50/62) | 79.0% (49/62) | 62.9% (39/62) | 6.5% (4/62) | 88.7% (55/62) |
| System fixture | 65.4% (17/26) | 65.4% (17/26) | 53.8% (14/26) | 0.0% (0/26) | 50.0% (13/26) |
| Dead code | 80.0% (8/10) | 80.0% (8/10) | 50.0% (5/10) | 10.0% (1/10) | 70.0% (7/10) |

## Who finds what

Findings detected by exactly one scanner, by both, or by neither (baselines excluded).

| | Findings | By language |
|---|---|---|
| nobody | 83 | Certificates, keys, configs 33, C / OpenSSL 13, Go 11, Java 10, Python 7, JavaScript / TypeScript 7, Built artifacts (system fixture) 2 |
| all | 5 | JavaScript / TypeScript 5 |
| only QCI v2.3.4 | 9 | Go 6, Python 2, Java 1 |
| only QCI v2.2 | 3 | Java 2, Python 1 |
| only QCI v0.7 | 3 | Python 1, Go 1, C / OpenSSL 1 |
| only cdxgen 12.9.1 | 4 | JavaScript / TypeScript 4 |

Families nobody detects, by count: AES 13, RSA 9, SHA-256 6, SHA-1 5, EC 5, SHA3-256 4, TLS_RSA_WITH_AES_128_CBC_SHA 4, RC4 4, SHA-384 3, Ed25519 3, TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 3, TLS_RSA_WITH_3DES_EDE_CBC_SHA 3, 3DES 3, MD5 2, SHA-512 2

† fewer than 10 findings in the cell: thin evidence, read the rate as an indication.

"Recall incl. signals" also credits findings a scanner reported without naming the algorithm: QCI's risk categories, cdxgen's crypto-file entries. See each scanner's adapter.
