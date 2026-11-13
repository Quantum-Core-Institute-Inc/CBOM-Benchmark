# Scanner comparison

Shipped corpus only, every scanner on the same denominator, no declared scopes. Baselines (grep baseline) are calibration points, not products.

Testbench 2.6.4, policy nist:c78f618c306e7d48, answer key b0867a4029ea0c56, scorer 0dead3635a2ae115. Scanners: QCI v2.3.4.1 = qci-pqc, version 2.3.4.1 via qci_pqc 1.1; cdxgen 12.9.1 = CycloneDX Generator 12.9.1 via cdxgen 1.0; cryptoscan 1.5.0 = cryptoscan 1.5.0; qScan 0.12.0 = qScan 0.12.0 via qscan 0.3; grep baseline = grep baseline.

## Overall

| | QCI v2.3.4.1 | cdxgen 12.9.1 | cryptoscan 1.5.0 | qScan 0.12.0 | grep baseline |
|---|---|---|---|---|---|
| Findings | 410 | 410 | 410 | 410 | 410 |
| Recall | 61.0% | 5.1% | 34.6% | 18.3% | 67.1% |
| Recall incl. signals | 64.4% | 11.0% | n/a | n/a | n/a |
| At primary site | 58.8% | 5.1% | 31.5% | 17.3% | 63.4% |
| Parameters correct (of detected) | 54.4% | 81.0% | 37.3% | 17.3% | 56.0% |
| Precision | 99.6% | 100.0% | 59.2% | 83.3% | 61.7% |
| False positives | 1 | 0 | 98 | 15 | 171 |
|   in negative controls | 0 | 0 | 26 | 1 | 60 |
| PQC over-claims | 0 | 0 | 18 | 0 | 28 |
| PQC by standard name (of detected PQC) | 100.0% | n/a | 100.0% | n/a | 100.0% |
| System fixture: routable (of detected) | 61.5% | n/a | 42.9% | 60.0% | 61.5% |
| System fixture: asset links | 0.0% (0/2) † | 0.0% (0/2) † | 0.0% (0/2) † | 0.0% (0/2) † | 0.0% (0/2) † |
| Ticket-ready (of detected) | 45.2% | 81.0% | 35.9% | 17.3% | 51.3% |
| Actionable recall | 27.6% | 4.1% | 12.4% | 3.2% | 34.4% |
| Detected, due by 2030 (NIST) | 63/95 | 5/95 | 43/95 | 18/95 | 65/95 |

## Crypto libraries (dependency manifests)

| | QCI v2.3.4.1 | cdxgen 12.9.1 | cryptoscan 1.5.0 | qScan 0.12.0 | grep baseline |
|---|---|---|---|---|---|
| Crypto libraries, in the right manifest | 96.4% (27/28) | 75.0% (21/28) | 0.0% (0/28) | 0.0% (0/28) | 0.0% (0/28) |
| Found anywhere (incl. no location) | 96.4% (27/28) | 85.7% (24/28) | 0.0% (0/28) | 0.0% (0/28) | 0.0% (0/28) |
| Transitive (lockfile) | 100.0% | 100.0% | 0.0% | 0.0% | 0.0% |
| Versions correct (of found) | 84.6% | 100.0% | n/a | n/a | n/a |
| PQC verdicts right | none given | none given | none given | none given | none given |
| False positives | 2 | 0 | 0 | 0 | 0 |

## By language (recall)

| | QCI v2.3.4.1 | cdxgen 12.9.1 | cryptoscan 1.5.0 | qScan 0.12.0 | grep baseline |
|---|---|---|---|---|---|
| Python | 80.9% (55/68) | 0.0% (0/68) | 50.0% (34/68) | 26.5% (18/68) | 82.4% (56/68) |
| Java | 72.3% (47/65) | 0.0% (0/65) | 47.7% (31/65) | 20.0% (13/65) | 78.5% (51/65) |
| Go | 74.5% (35/47) | 0.0% (0/47) | 55.3% (26/47) | 25.5% (12/47) | 78.7% (37/47) |
| JavaScript / TypeScript | 53.1% (26/49) | 42.9% (21/49) | 32.7% (16/49) | 24.5% (12/49) | 81.6% (40/49) |
| C / OpenSSL | 51.9% (27/52) | 0.0% (0/52) | 11.5% (6/52) | 3.8% (2/52) | 67.3% (35/52) |
| C# / .NET | 63.2% (12/19) | 0.0% (0/19) | 63.2% (12/19) | 31.6% (6/19) | 89.5% (17/19) |
| Certificates, keys, configs | 46.2% (48/104) | 0.0% (0/104) | 16.3% (17/104) | 11.5% (12/104) | 33.7% (35/104) |
| Built artifacts (system fixture) | 0.0% (0/6) † | 0.0% (0/6) † | 0.0% (0/6) † | 0.0% (0/6) † | 66.7% (4/6) † |

## By tier (recall)

| | QCI v2.3.4.1 | cdxgen 12.9.1 | cryptoscan 1.5.0 | qScan 0.12.0 | grep baseline |
|---|---|---|---|---|---|
| 1. Direct | 80.4% (82/102) | 7.8% (8/102) | 42.2% (43/102) | 27.5% (28/102) | 83.3% (85/102) |
| 2. Indirection | 64.3% (27/42) | 4.8% (2/42) | 54.8% (23/42) | 23.8% (10/42) | 92.9% (39/42) |
| 3. Cross-file | 75.0% (12/16) | 0.0% (0/16) | 68.8% (11/16) | 25.0% (4/16) | 100.0% (16/16) |
| 4. Non-code assets | 33.3% (22/66) | 0.0% (0/66) | 15.2% (10/66) | 12.1% (8/66) | 34.8% (23/66) |
| 5. Adversarial | 9.5% (4/42) | 14.3% (6/42) | 0.0% (0/42) | 0.0% (0/42) | 35.7% (15/42) |
| Post-quantum | 72.7% (32/44) | 0.0% (0/44) | 40.9% (18/44) | 9.1% (4/44) | 50.0% (22/44) |
| Mixed files | 80.6% (50/62) | 6.5% (4/62) | 38.7% (24/62) | 24.2% (15/62) | 88.7% (55/62) |
| System fixture | 50.0% (13/26) | 0.0% (0/26) | 26.9% (7/26) | 19.2% (5/26) | 50.0% (13/26) |
| Dead code | 80.0% (8/10) | 10.0% (1/10) | 60.0% (6/10) | 10.0% (1/10) | 70.0% (7/10) |

## Who finds what

Findings detected by exactly one scanner, by both, or by neither (baselines excluded).

| | Findings | By language |
|---|---|---|
| nobody | 121 | Certificates, keys, configs 50, C / OpenSSL 21, Java 12, JavaScript / TypeScript 12, Python 9, Go 8, Built artifacts (system fixture) 6, C# / .NET 3 |
| all | 3 | JavaScript / TypeScript 3 |
| only QCI v2.3.4.1 | 106 | Certificates, keys, configs 30, C / OpenSSL 25, Python 18, Java 16, Go 10, JavaScript / TypeScript 4, C# / .NET 3 |
| only cdxgen 12.9.1 | 8 | JavaScript / TypeScript 8 |
| only cryptoscan 1.5.0 | 23 | Java 5, Python 4, C# / .NET 4, Certificates, keys, configs 3, Go 3, C / OpenSSL 3, JavaScript / TypeScript 1 |
| only qScan 0.12.0 | 4 | Certificates, keys, configs 3, Java 1 |

Families nobody detects, by count: AES 19, SHA-1 9, RSA 9, SHA-256 8, EC 6, SHA3-256 5, TLS_RSA_WITH_AES_128_CBC_SHA 5, HMAC 5, 3DES 5, SHA-512 4, TLS_RSA_WITH_3DES_EDE_CBC_SHA 4, SHA-384 3, TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 3, TLS-1.1 3, TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 3

† fewer than 10 findings in the cell: thin evidence, read the rate as an indication.

"Recall incl. signals" also credits findings a scanner reported without naming the algorithm: QCI's risk categories, cdxgen's crypto-file entries. See each scanner's adapter.
