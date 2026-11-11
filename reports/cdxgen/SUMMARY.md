# cdxgen on the CBOM Testbench

- Scanner: **CycloneDX Generator 12.9.1**, `cbom --spec-version 1.6 --no-install-deps --evidence`
- Translation: `tools/adapters/cdxgen.py` 1.0: 4 HMAC/PBKDF2 renames, 17 crypto-file entries scored as signals, 6 algorithms with no location

| Metric | Value |
|---|---|
| recall | 4.2 |
| primary site recall | 4.2 |
| params accuracy | 78.6 |
| precision | 100.0 |
| false positives | 0 |
| negative control fps | 0 |
| pqc overclaims | 0 |
| pqc standard name pct | None |
| system routable pct | None |
| ticket ready pct | 78.6 |
| actionable recall | 3.3 |
| field completeness | 35.8 |
| deadline weighted recall | 3.9 |
| missed due by 2030 | 103 |
| library recall | 75.0 |
| library pq verdict accuracy | None |

Signal coverage: crypto-file entries cover 24 more expected findings (combined 38/330, 11.5%).

