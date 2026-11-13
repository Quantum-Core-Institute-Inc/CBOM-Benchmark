# Scanner comparison

Shipped corpus only, every scanner on the same denominator, no declared scopes. Baselines (grep baseline) are calibration points, not products.

Testbench 2.6.5, policy nist:c78f618c306e7d48, answer key b0867a4029ea0c56, scorer 0dead3635a2ae115. Scanners: QCI v2.3.4.3 = qci-pqc, version 2.3.4.3 via qci_pqc 1.2; cdxgen 12.9.1 = CycloneDX Generator 12.9.1 via cdxgen 1.0; grep baseline = grep baseline.

## Overall

| | QCI v2.3.4.3 | cdxgen 12.9.1 | grep baseline |
|---|---|---|---|
| Findings | 410 | 410 | 410 |
| Recall | 62.2% | 5.1% | 67.1% |
| Recall incl. signals | 65.6% | 11.0% | n/a |
| At primary site | 60.0% | 5.1% | 63.4% |
| Parameters correct (of detected) | 90.2% | 81.0% | 56.0% |
| Precision | 100.0% | 100.0% | 61.7% |
| False positives | 0 | 0 | 171 |
|   in negative controls | 0 | 0 | 60 |
| PQC over-claims | 0 | 0 | 28 |
| PQC by standard name (of detected PQC) | 100.0% | n/a | 100.0% |
| System fixture: routable (of detected) | 64.3% | n/a | 61.5% |
| System fixture: asset links | 0.0% (0/2) † | 0.0% (0/2) † | 0.0% (0/2) † |
| Ticket-ready (of detected) | 80.0% | 81.0% | 51.3% |
| Actionable recall | 49.8% | 4.1% | 34.4% |
| Detected, due by 2030 (NIST) | 63/95 | 5/95 | 65/95 |

## Crypto libraries (dependency manifests)

| | QCI v2.3.4.3 | cdxgen 12.9.1 | grep baseline |
|---|---|---|---|
| Crypto libraries, in the right manifest | 96.4% (27/28) | 75.0% (21/28) | 0.0% (0/28) |
| Found anywhere (incl. no location) | 96.4% (27/28) | 85.7% (24/28) | 0.0% (0/28) |
| Transitive (lockfile) | 100.0% | 100.0% | 0.0% |
| Versions correct (of found) | 84.6% | 100.0% | n/a |
| PQC verdicts right | none given | none given | none given |
| False positives | 2 | 0 | 0 |

## By language (recall)

| | QCI v2.3.4.3 | cdxgen 12.9.1 | grep baseline |
|---|---|---|---|
| Python | 80.9% (55/68) | 0.0% (0/68) | 82.4% (56/68) |
| Java | 72.3% (47/65) | 0.0% (0/65) | 78.5% (51/65) |
| Go | 80.9% (38/47) | 0.0% (0/47) | 78.7% (37/47) |
| JavaScript / TypeScript | 53.1% (26/49) | 42.9% (21/49) | 81.6% (40/49) |
| C / OpenSSL | 51.9% (27/52) | 0.0% (0/52) | 67.3% (35/52) |
| C# / .NET | 68.4% (13/19) | 0.0% (0/19) | 89.5% (17/19) |
| Certificates, keys, configs | 46.2% (48/104) | 0.0% (0/104) | 33.7% (35/104) |
| Built artifacts (system fixture) | 16.7% (1/6) † | 0.0% (0/6) † | 66.7% (4/6) † |

## By tier (recall)

| | QCI v2.3.4.3 | cdxgen 12.9.1 | grep baseline |
|---|---|---|---|
| 1. Direct | 81.4% (83/102) | 7.8% (8/102) | 83.3% (85/102) |
| 2. Indirection | 66.7% (28/42) | 4.8% (2/42) | 92.9% (39/42) |
| 3. Cross-file | 75.0% (12/16) | 0.0% (0/16) | 100.0% (16/16) |
| 4. Non-code assets | 33.3% (22/66) | 0.0% (0/66) | 34.8% (23/66) |
| 5. Adversarial | 9.5% (4/42) | 14.3% (6/42) | 35.7% (15/42) |
| Post-quantum | 72.7% (32/44) | 0.0% (0/44) | 50.0% (22/44) |
| Mixed files | 82.3% (51/62) | 6.5% (4/62) | 88.7% (55/62) |
| System fixture | 53.8% (14/26) | 0.0% (0/26) | 50.0% (13/26) |
| Dead code | 90.0% (9/10) | 10.0% (1/10) | 70.0% (7/10) |

## Who finds what

Findings detected by exactly one scanner, by both, or by neither (baselines excluded).

| | Findings | By language |
|---|---|---|
| nobody | 145 | Certificates, keys, configs 56, C / OpenSSL 25, Java 18, Python 13, JavaScript / TypeScript 13, Go 9, C# / .NET 6, Built artifacts (system fixture) 5 |
| all | 11 | JavaScript / TypeScript 11 |
| only QCI v2.3.4.3 | 244 | Python 55, Certificates, keys, configs 48, Java 47, Go 38, C / OpenSSL 27, JavaScript / TypeScript 15, C# / .NET 13, Built artifacts (system fixture) 1 |
| only cdxgen 12.9.1 | 10 | JavaScript / TypeScript 10 |

Families nobody detects, by count: AES 19, SHA-1 15, RSA 11, EC 10, SHA-256 8, MD5 7, HMAC 6, 3DES 6, SHA3-256 5, TLS_RSA_WITH_AES_128_CBC_SHA 5, TLS_RSA_WITH_3DES_EDE_CBC_SHA 4, DH 4, LMS 4, SHA-384 3, SHA-512 3

† fewer than 10 findings in the cell: thin evidence, read the rate as an indication.

"Recall incl. signals" also credits findings a scanner reported without naming the algorithm: QCI's risk categories, cdxgen's crypto-file entries. See each scanner's adapter.
