# cdxgen on the CBOM Testbench

- Scanner: **CycloneDX Generator 12.9.1**, `cbom --spec-version 1.6 --no-install-deps --evidence`
- Translation: `tools/adapters/cdxgen.py` 1.0: 4 HMAC/PBKDF2 renames, 17 crypto-file entries scored as signals, 6 algorithms with no location

| Metric | Value |
|---|---|
| recall | 4.4 |
| primary site recall | 4.4 |
| params accuracy | 80.0 |
| precision | 100.0 |
| false positives | 0 |
| negative control fps | 0 |
| pqc overclaims | 0 |
| pqc standard name pct | None |
| system routable pct | None |
| ticket ready pct | 80.0 |
| actionable recall | 3.6 |
| field completeness | 36.6 |
| deadline weighted recall | 4.3 |
| missed due by 2030 | 112 |
| library recall | 75.0 |
| library pq verdict accuracy | None |

Signal coverage: crypto-file entries cover 22 more expected findings (combined 37/338, 10.9%).

