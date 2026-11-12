# Config Completeness

A dedicated scorecard bucket that separates “found the algorithm” from “found the configuration details an engineer needs.”

## What it measures

The findings that live in configuration files: TLS, SSH and IPsec configs, signing policies,
Kubernetes manifests and Terraform (62 of the 410 findings; `is_config_finding` in `tools/score.py`
is the definition). Certificates, keys and keystores are assets, not configs.

Two numbers:

- **Recall** on those findings: was the protocol version, suite, proposal or group found at all.
- **Config-complete**: of the ones found, how many were reported with every expected parameter
  (the suite's components, the key or group size, the mode).

These findings are already counted in recall and parameter accuracy. This section isolates them,
because a scanner can be strong on code and blind to configuration, and the headline hides that.

The `config_completeness` gate is a floor on the second number. It is skipped, with a recorded
reason, when a scanner detects no config finding at all.

## History

The section first shipped in 2.6.2 with a definition that matched nothing: it looked for parameter
keys such as `version`, `cipher` and `proposal`, and the answer key's parameters are `key_size`,
`mode`, `hash` and `curve`. It reported zero expected findings for every scanner, and its gate floor
(40.0) was never measured. 2.6.4 replaced the definition with the one above and measured the floor.

## Where scanners lose config findings

| Format | Findings | Typical miss |
|--------|----------|--------------|
| Apache httpd | 5 | `SSLProtocol`, `SSLCipherSuite` |
| HAProxy | 6 | `ssl-min-ver`, cipher lines, DH size on a tuning line |
| strongSwan / IPsec | 9 | proposal grammar (`aes256-sha256-modp2048`, `3des-sha1-modp1024!`) |
| Firmware signing policy | 3 | LMS and XMSS parameter-set names |

Asset links (the nginx config to its certificate, the certificate to its key) are a separate score:
see METHODOLOGY.md section 4a.
