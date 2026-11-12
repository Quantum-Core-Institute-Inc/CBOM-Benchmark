# Config Completeness

A dedicated scorecard bucket that separates “found the algorithm” from “found the configuration details an engineer needs.”

## What it measures

For TLS, SSH, IPsec and related config findings, a report is **config-complete** when it includes:

- Protocol version (or explicit “any / not set”)
- Cipher suite or proposal string
- Named group / DH group size (when present in the config)
- Key-exchange or signature algorithm parameters

Missing any of these is scored under **config completeness**, not under raw algorithm recall.

## Current gaps (2.6.0)

| Format | Findings | Typical miss |
|--------|----------|--------------|
| Apache httpd | 5 | `SSLProtocol`, `SSLCipherSuite` |
| HAProxy | 6 | `ssl-min-ver`, cipher lines, DH size on tuning line |
| strongSwan / IPsec | 9 | proposal grammar (`aes256-sha256-modp2048`, `3des-sha1-modp1024!`) |
| System fixture asset links | 2 | nginx config ↔ certificate, certificate ↔ key (currently 0/2) |
| LMS / XMSS | 8 | pure-Python, OID-only keys, policy names |

## Planned for 2.6.2

- Additional grammar cases for the formats above.
- Asset-link scoring made more prominent in the scorecard and comparison tables.
- Holdout generator coverage for LMS/XMSS pure-Python and OID-only cases.
- Config-completeness bucket added to every scorecard.
