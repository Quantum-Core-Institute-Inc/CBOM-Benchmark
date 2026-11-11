# Scanner comparison

Shipped corpus only, every scanner on the same denominator, no declared scopes. Baselines (grep baseline) are calibration points, not products.

Testbench 2.2.0, policy nist:732cd8a8d8f317e9, answer key 0c7489f223e2060d, scorer a28229a0c1833b03. Scanners: QCI v2.3.4 = qci-pqc, version 2.3.4 via qci_pqc 1.1; QCI v2.2 = qci-pqc, version 2.2.0 via qci_pqc 1.1; QCI v0.7 = qci-pqc, version 0.7.0 via qci_pqc 1.1; cdxgen 12.9.1 = CycloneDX Generator 12.9.1 via cdxgen 1.0; grep baseline = grep baseline.

## Overall

| | QCI v2.3.4 | QCI v2.2 | QCI v0.7 | cdxgen 12.9.1 | grep baseline |
|---|---|---|---|---|---|
| Findings | 330 | 330 | 330 | 330 | 330 |
| Recall | 70.3% | 69.7% | 57.3% | 4.2% | 68.8% |
| Recall incl. signals | 73.6% | 73.0% | 60.0% | 11.5% | n/a |
| At primary site | 67.6% | 66.4% | 53.9% | 4.2% | 64.2% |
| Parameters correct (of detected) | 56.9% | 64.8% | 67.2% | 78.6% | 53.7% |
| Precision | 99.6% | 92.0% | 87.1% | 100.0% | 59.1% |
| False positives | 1 | 20 | 28 | 0 | 157 |
|   in negative controls | 0 | 0 | 4 | 0 | 52 |
| PQC over-claims | 0 | 7 | 13 | 0 | 28 |
| PQC by standard name (of detected PQC) | 100.0% | 100.0% | 100.0% | n/a | 100.0% |
| System fixture: routable (of detected) | 70.6% | 70.6% | 64.3% | n/a | 61.5% |
| System fixture: asset links | 0.0% (0/2) † | 0.0% (0/2) † | 0.0% (0/2) † | 0.0% (0/2) † | 0.0% (0/2) † |
| Ticket-ready (of detected) | 47.0% | 54.3% | 54.5% | 78.6% | 49.3% |
| Actionable recall | 33.0% | 37.9% | 31.2% | 3.3% | 33.9% |
| Detected, due by 2030 (NIST) | 55/73 | 57/73 | 48/73 | 2/73 | 52/73 |

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
| Python | 83.1% (54/65) | 84.6% (55/65) | 81.5% (53/65) | 0.0% (0/65) | 83.1% (54/65) |
| Java | 77.6% (45/58) | 81.0% (47/58) | 74.1% (43/58) | 0.0% (0/58) | 84.5% (49/58) |
| Go | 75.6% (34/45) | 62.2% (28/45) | 48.9% (22/45) | 0.0% (0/45) | 80.0% (36/45) |
| JavaScript / TypeScript | 66.7% (24/36) | 72.2% (26/36) | 22.2% (8/36) | 38.9% (14/36) | 86.1% (31/36) |
| C / OpenSSL | 64.1% (25/39) | 61.5% (24/39) | 41.0% (16/39) | 0.0% (0/39) | 69.2% (27/39) |
| Certificates, keys, configs | 56.8% (46/81) | 56.8% (46/81) | 53.1% (43/81) | 0.0% (0/81) | 32.1% (26/81) |
| Built artifacts (system fixture) | 66.7% (4/6) † | 66.7% (4/6) † | 66.7% (4/6) † | 0.0% (0/6) † | 66.7% (4/6) † |

## By tier (recall)

| | QCI v2.3.4 | QCI v2.2 | QCI v0.7 | cdxgen 12.9.1 | grep baseline |
|---|---|---|---|---|---|
| 1. Direct | 80.9% (72/89) | 75.3% (67/89) | 52.8% (47/89) | 9.0% (8/89) | 82.0% (73/89) |
| 2. Indirection | 66.7% (24/36) | 69.4% (25/36) | 61.1% (22/36) | 5.6% (2/36) | 94.4% (34/36) |
| 3. Cross-file | 75.0% (12/16) | 87.5% (14/16) | 87.5% (14/16) | 0.0% (0/16) | 100.0% (16/16) |
| 4. Non-code assets | 41.7% (20/48) | 41.7% (20/48) | 39.6% (19/48) | 0.0% (0/48) | 31.2% (15/48) |
| 5. Adversarial | 29.4% (5/17) | 35.3% (6/17) | 11.8% (2/17) | 0.0% (0/17) | 0.0% (0/17) |
| Post-quantum | 88.9% (32/36) | 88.9% (32/36) | 88.9% (32/36) | 0.0% (0/36) | 58.3% (21/36) |
| Mixed files | 80.6% (50/62) | 79.0% (49/62) | 62.9% (39/62) | 6.5% (4/62) | 88.7% (55/62) |
| System fixture | 65.4% (17/26) | 65.4% (17/26) | 53.8% (14/26) | 0.0% (0/26) | 50.0% (13/26) |

## Who finds what

Findings detected by exactly one scanner, by both, or by neither (baselines excluded).

| | Findings | By language |
|---|---|---|
| nobody | 84 | Certificates, keys, configs 35, C / OpenSSL 13, Java 10, Go 10, Python 7, JavaScript / TypeScript 7, Built artifacts (system fixture) 2 |
| all | 5 | JavaScript / TypeScript 5 |
| only QCI v2.3.4 | 9 | Go 6, Python 2, Java 1 |
| only QCI v2.2 | 3 | Java 2, Python 1 |
| only QCI v0.7 | 3 | Python 1, Go 1, C / OpenSSL 1 |
| only cdxgen 12.9.1 | 3 | JavaScript / TypeScript 3 |

Families nobody detects, by count: AES 13, RSA 10, SHA-256 7, SHA-1 5, EC 5, SHA3-256 4, TLS_RSA_WITH_AES_128_CBC_SHA 4, SHA-384 3, Ed25519 3, TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 3, TLS_RSA_WITH_3DES_EDE_CBC_SHA 3, RC4 3, 3DES 3, MD5 2, SHA-512 2

† fewer than 10 findings in the cell: thin evidence, read the rate as an indication.

"Recall incl. signals" also credits findings a scanner reported without naming the algorithm: QCI's risk categories, cdxgen's crypto-file entries. See each scanner's adapter.
