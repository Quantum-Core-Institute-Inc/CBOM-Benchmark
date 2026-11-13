# Scanner comparison

Shipped corpus only, every scanner on the same denominator, no declared scopes. Baselines (grep baseline) are calibration points, not products.

Testbench 2.6.6, policy nist:c78f618c306e7d48, answer key b0867a4029ea0c56, scorer 0dead3635a2ae115. Scanners: QCI v2.3.4.5 = qci-pqc, version 2.3.4.5 via qci_pqc 1.3; cdxgen 12.9.1 = CycloneDX Generator 12.9.1 via cdxgen 1.0; grep baseline = grep baseline.

## Overall

| | QCI v2.3.4.5 | cdxgen 12.9.1 | grep baseline |
|---|---|---|---|
| Findings | 410 | 410 | 410 |
| Recall | 76.6% | 5.1% | 67.1% |
| Recall incl. signals | 79.0% | 11.0% | n/a |
| At primary site | 74.4% | 5.1% | 63.4% |
| Parameters correct (of detected) | 92.7% | 81.0% | 56.0% |
| Precision | 100.0% | 100.0% | 61.7% |
| False positives | 0 | 0 | 171 |
|   in negative controls | 0 | 0 | 60 |
| PQC over-claims | 0 | 0 | 28 |
| PQC by standard name (of detected PQC) | 100.0% | n/a | 100.0% |
| System fixture: routable (of detected) | 76.2% | n/a | 61.5% |
| System fixture: asset links | 0.0% (0/2) † | 0.0% (0/2) † | 0.0% (0/2) † |
| Ticket-ready (of detected) | 86.9% | 81.0% | 51.3% |
| Actionable recall | 66.6% | 4.1% | 34.4% |
| Detected, due by 2030 (NIST) | 75/95 | 5/95 | 65/95 |

## Crypto libraries (dependency manifests)

| | QCI v2.3.4.5 | cdxgen 12.9.1 | grep baseline |
|---|---|---|---|
| Crypto libraries, in the right manifest | 96.4% (27/28) | 75.0% (21/28) | 0.0% (0/28) |
| Found anywhere (incl. no location) | 96.4% (27/28) | 85.7% (24/28) | 0.0% (0/28) |
| Transitive (lockfile) | 100.0% | 100.0% | 0.0% |
| Versions correct (of found) | 84.6% | 100.0% | n/a |
| PQC verdicts right | none given | none given | none given |
| False positives | 2 | 0 | 0 |

## By language (recall)

| | QCI v2.3.4.5 | cdxgen 12.9.1 | grep baseline |
|---|---|---|---|
| Python | 80.9% (55/68) | 0.0% (0/68) | 82.4% (56/68) |
| Java | 78.5% (51/65) | 0.0% (0/65) | 78.5% (51/65) |
| Go | 91.5% (43/47) | 0.0% (0/47) | 78.7% (37/47) |
| JavaScript / TypeScript | 75.5% (37/49) | 42.9% (21/49) | 81.6% (40/49) |
| C / OpenSSL | 80.8% (42/52) | 0.0% (0/52) | 67.3% (35/52) |
| C# / .NET | 68.4% (13/19) | 0.0% (0/19) | 89.5% (17/19) |
| Certificates, keys, configs | 64.4% (67/104) | 0.0% (0/104) | 33.7% (35/104) |
| Built artifacts (system fixture) | 100.0% (6/6) † | 0.0% (0/6) † | 66.7% (4/6) † |

## By tier (recall)

| | QCI v2.3.4.5 | cdxgen 12.9.1 | grep baseline |
|---|---|---|---|
| 1. Direct | 89.2% (91/102) | 7.8% (8/102) | 83.3% (85/102) |
| 2. Indirection | 66.7% (28/42) | 4.8% (2/42) | 92.9% (39/42) |
| 3. Cross-file | 75.0% (12/16) | 0.0% (0/16) | 100.0% (16/16) |
| 4. Non-code assets | 59.1% (39/66) | 0.0% (0/66) | 34.8% (23/66) |
| 5. Adversarial | 71.4% (30/42) | 14.3% (6/42) | 35.7% (15/42) |
| Post-quantum | 75.0% (33/44) | 0.0% (0/44) | 50.0% (22/44) |
| Mixed files | 82.3% (51/62) | 6.5% (4/62) | 88.7% (55/62) |
| System fixture | 80.8% (21/26) | 0.0% (0/26) | 50.0% (13/26) |
| Dead code | 90.0% (9/10) | 10.0% (1/10) | 70.0% (7/10) |

## Who finds what

Findings detected by exactly one scanner, by both, or by neither (baselines excluded).

| | Findings | By language |
|---|---|---|
| nobody | 92 | Certificates, keys, configs 37, Java 14, Python 13, C / OpenSSL 10, JavaScript / TypeScript 8, C# / .NET 6, Go 4 |
| all | 17 | JavaScript / TypeScript 17 |
| only QCI v2.3.4.5 | 297 | Certificates, keys, configs 67, Python 55, Java 51, Go 43, C / OpenSSL 42, JavaScript / TypeScript 20, C# / .NET 13, Built artifacts (system fixture) 6 |
| only cdxgen 12.9.1 | 4 | JavaScript / TypeScript 4 |

Families nobody detects, by count: AES 15, SHA-1 10, RSA 9, SHA-256 7, MD5 6, EC 6, SHA3-256 5, HMAC 5, 3DES 4, LMS 4, SHA-384 3, Ed25519 3, XMSS 3, SHA-512 2, PBKDF2 2

† fewer than 10 findings in the cell: thin evidence, read the rate as an indication.

"Recall incl. signals" also credits findings a scanner reported without naming the algorithm: QCI's risk categories, cdxgen's crypto-file entries. See each scanner's adapter.
