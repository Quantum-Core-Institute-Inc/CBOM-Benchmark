# Config Completeness Implementation

## Goal
Add a **Config Completeness** bucket to every scorecard and close the remaining surface gaps.

## New scorecard section

```markdown
## Config Completeness

| Bucket | Detected | Config-complete | % |
|--------|----------|-----------------|---|
| TLS / SSH / IPsec | … | … | … |
| Asset links | 0/2 | 0/2 | 0% |
```

A report is config-complete when it includes protocol version, cipher/proposal, and named group / DH size where present.

## Corpus expansions
- Additional Apache `SSLProtocol` / `SSLCipherSuite` cases.
- HAProxy `ssl-min-ver` + cipher lines + tuning-line DH size.
- strongSwan proposal grammar (`aes256-sha256-modp2048`, `3des-sha1-modp1024!`).
- Make system-fixture asset links more prominent (nginx ↔ cert, cert ↔ key).
- LMS/XMSS pure-Python and OID-only cases already present; ensure they are scored under config/PQC completeness.

## Acceptance
- Asset links visible and non-thin where possible.
- Config completeness appears in comparison tables.
- Methodology stays 2.3.
