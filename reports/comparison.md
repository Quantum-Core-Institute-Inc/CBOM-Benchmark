# Scanner comparison

Shipped corpus only, every scanner on the same denominator, no declared scopes. Baselines (grep baseline) are calibration points, not products.

Testbench 2.4.0, policy nist:c78f618c306e7d48, answer key c9f27be6d6a5098a, scorer 4449df0c3850c51f. Scanners: QCI v2.3.4 = qci-pqc, version 2.3.4 via qci_pqc 1.1; QCI v2.2 = qci-pqc, version 2.2.0 via qci_pqc 1.1; QCI v0.7 = qci-pqc, version 0.7.0 via qci_pqc 1.1; cdxgen 12.9.1 = CycloneDX Generator 12.9.1 via cdxgen 1.0; grep baseline = grep baseline.

## Overall

| | QCI v2.3.4 | QCI v2.2 | QCI v0.7 | cdxgen 12.9.1 | grep baseline |
|---|---|---|---|---|---|
| Findings | 393 | 393 | 393 | 393 | 393 |
| Recall | 65.1% | 62.8% | 51.4% | 4.3% | 67.4% |
| Recall incl. signals | 68.7% | 66.4% | 54.5% | 10.4% | n/a |
| At primary site | 62.8% | 60.1% | 48.6% | 4.3% | 63.6% |
| Parameters correct (of detected) | 55.1% | 63.6% | 66.8% | 76.5% | 55.8% |
| Precision | 98.8% | 91.8% | 87.4% | 100.0% | 60.9% |
| False positives | 3 | 22 | 29 | 0 | 170 |
|   in negative controls | 0 | 0 | 4 | 0 | 60 |
| PQC over-claims | 0 | 7 | 13 | 0 | 28 |
| PQC by standard name (of detected PQC) | 100.0% | 100.0% | 100.0% | n/a | 100.0% |
| System fixture: routable (of detected) | 70.6% | 70.6% | 64.3% | n/a | 61.5% |
| System fixture: asset links | 0.0% (0/2) † | 0.0% (0/2) † | 0.0% (0/2) † | 0.0% (0/2) † | 0.0% (0/2) † |
| Ticket-ready (of detected) | 46.1% | 53.8% | 55.0% | 76.5% | 50.9% |
| Actionable recall | 30.0% | 33.8% | 28.2% | 3.3% | 34.4% |
| Detected, due by 2030 (NIST) | 65/90 | 66/90 | 54/90 | 3/90 | 62/90 |

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
| Java | 72.3% (47/65) | 75.4% (49/65) | 69.2% (45/65) | 0.0% (0/65) | 78.5% (51/65) |
| Go | 74.5% (35/47) | 61.7% (29/47) | 46.8% (22/47) | 0.0% (0/47) | 78.7% (37/47) |
| JavaScript / TypeScript | 61.0% (25/41) | 65.9% (27/41) | 19.5% (8/41) | 41.5% (17/41) | 85.4% (35/41) |
| C / OpenSSL | 65.9% (29/44) | 59.1% (26/44) | 40.9% (18/44) | 0.0% (0/44) | 68.2% (30/44) |
| C# / .NET | 63.2% (12/19) | 36.8% (7/19) | 26.3% (5/19) | 0.0% (0/19) | 89.5% (17/19) |
| Certificates, keys, configs | 46.2% (48/104) | 46.2% (48/104) | 43.3% (45/104) | 0.0% (0/104) | 33.7% (35/104) |
| Built artifacts (system fixture) | 66.7% (4/6) † | 66.7% (4/6) † | 66.7% (4/6) † | 0.0% (0/6) † | 66.7% (4/6) † |

## By tier (recall)

| | QCI v2.3.4 | QCI v2.2 | QCI v0.7 | cdxgen 12.9.1 | grep baseline |
|---|---|---|---|---|---|
| 1. Direct | 79.4% (81/102) | 68.6% (70/102) | 50.0% (51/102) | 7.8% (8/102) | 83.3% (85/102) |
| 2. Indirection | 64.3% (27/42) | 69.0% (29/42) | 54.8% (23/42) | 4.8% (2/42) | 92.9% (39/42) |
| 3. Cross-file | 75.0% (12/16) | 87.5% (14/16) | 87.5% (14/16) | 0.0% (0/16) | 100.0% (16/16) |
| 4. Non-code assets | 33.3% (22/66) | 33.3% (22/66) | 31.8% (21/66) | 0.0% (0/66) | 34.8% (23/66) |
| 5. Adversarial | 26.9% (7/26) | 23.1% (6/26) | 11.5% (3/26) | 7.7% (2/26) | 19.2% (5/26) |
| Post-quantum | 74.4% (32/43) | 74.4% (32/43) | 74.4% (32/43) | 0.0% (0/43) | 51.2% (22/43) |
| Mixed files | 80.6% (50/62) | 79.0% (49/62) | 62.9% (39/62) | 6.5% (4/62) | 88.7% (55/62) |
| System fixture | 65.4% (17/26) | 65.4% (17/26) | 53.8% (14/26) | 0.0% (0/26) | 50.0% (13/26) |
| Dead code | 80.0% (8/10) | 80.0% (8/10) | 50.0% (5/10) | 10.0% (1/10) | 70.0% (7/10) |

## Who finds what

Findings detected by exactly one scanner, by both, or by neither (baselines excluded).

| | Findings | By language |
|---|---|---|
| nobody | 119 | Certificates, keys, configs 56, Java 15, C / OpenSSL 14, Go 11, JavaScript / TypeScript 8, Python 7, C# / .NET 6, Built artifacts (system fixture) 2 |
| all | 5 | JavaScript / TypeScript 5 |
| only QCI v2.3.4 | 15 | Go 6, C# / .NET 5, Python 2, Java 1, C / OpenSSL 1 |
| only QCI v2.2 | 3 | Java 2, Python 1 |
| only QCI v0.7 | 3 | Python 1, Go 1, C / OpenSSL 1 |
| only cdxgen 12.9.1 | 6 | JavaScript / TypeScript 6 |

Families nobody detects, by count: AES 16, RSA 10, SHA-256 7, EC 7, SHA-1 6, SHA3-256 5, TLS_RSA_WITH_AES_128_CBC_SHA 5, MD5 4, TLS_RSA_WITH_3DES_EDE_CBC_SHA 4, 3DES 4, RC4 4, SHA-384 3, SHA-512 3, Ed25519 3, TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 3

† fewer than 10 findings in the cell: thin evidence, read the rate as an indication.

"Recall incl. signals" also credits findings a scanner reported without naming the algorithm: QCI's risk categories, cdxgen's crypto-file entries. See each scanner's adapter.
