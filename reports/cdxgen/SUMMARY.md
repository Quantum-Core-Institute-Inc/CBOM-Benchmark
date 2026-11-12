# cdxgen on the CBOM Testbench

- Scanner: **CycloneDX Generator 12.9.1**, `cbom --spec-version 1.6 --no-install-deps --evidence`
- Translation: `tools/adapters/cdxgen.py` 1.0: 5 HMAC/PBKDF2 renames, 19 crypto-file entries scored as signals, 6 algorithms with no location

| Metric | Value |
|---|---|
| recall | 5.1 |
| primary site recall | 5.1 |
| params accuracy | 81.0 |
| precision | 100.0 |
| false positives | 0 |
| negative control fps | 0 |
| pqc overclaims | 0 |
| pqc standard name pct | None |
| system routable pct | None |
| ticket ready pct | 81.0 |
| actionable recall | 4.1 |
| field completeness | 36.4 |
| deadline weighted recall | 5.8 |
| missed due by 2030 | 135 |
| library recall | 75.0 |
| parameter recovery | 81.0 |
| config completeness | None |
| library pq verdict accuracy | None |

Signal coverage: crypto-file entries cover 24 more expected findings (combined 45/410, 11.0%).

