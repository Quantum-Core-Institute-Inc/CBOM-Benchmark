# qci-pqc-scan v2.3.4.5 on the QCI CBOM Benchmark: findings for the scanner team

Scanner: `qci-pqc-scan` 2.3.4.5, internal adapter, run in the sandbox and in its own container.
Benchmark 2.6.6 (410 findings, methodology 2.3, NIST policy), declared scope from
`integrations/qci-pqc/scope.json`, holdout generator 1.4. Reproduce with `tools/release_run.sh`.
Evidence: `evidence/qci-v2.3.4.5/`, `evidence/qci-v2.3.4.5-container/` and
`evidence/perf-qci-v2.3.4.5/`; the numbers below are in `reports/qci-pqc/SUMMARY.md`.

## The short version

| | v2.3.4.3 on 2.6.5 | v2.3.4.5 on 2.6.6 |
|---|---|---|
| Recall, everything | 62.2% (255 of 410) | 76.6% (314 of 410) |
| Recall, declared scope | 65.5% | 79.8% (312 of 391) |
| Parameters correct (of detected) | 90.2% | 92.7% |
| Precision | 100% (none) | 100% (none) |
| Ticket-ready (of detected) | 80.0% | 86.9% |
| Actionable recall | 49.8% | 66.6% |
| Config findings found | 24 of 62 | 43 of 62 |
| Config findings complete (of found) | 24 of 24 | 43 of 43 |
| Tier 5 (compiled, minified, obfuscated) | 4 of 42 | 30 of 42 |
| Crypto libraries in the right manifest | 96.4% | 96.4% |
| Overfit gap | -0.8 (-5.6 to +4.2) | -1.6 (-6.5 to +3.2) |
| Negative-control gap | 0.0 per file | 0.0 per file |

Recall rose by 59 findings with no false positive added. The scanner now reads four things it used
to skip or flatten: TLS cipher suites, minified JavaScript, compiled Java and native binaries.

The declared scope changed with the scanner. `*.jar` is no longer excluded, because the scanner
reads archives now. The scope still excludes `.pyc`, `.der`, `.p12` and `.jks` files and certificate
signature algorithms: 19 findings.

One part of the gain is the benchmark's, as in 2.6.5. Adapter 1.3 lets IANA cipher-suite names
through to the scorer, which already knew how to split a suite into its key exchange, cipher and
hash. Without it the scanner's new suite findings would have been dropped as unknown names.

The gate floors were reset to v2.3.4.5's own numbers, so it passes every gate by construction. The
floors now protect 79.8% recall, 92.6% on parameters and 100% precision in the declared scope.

## 1. Native binaries

All 11 findings in the three stripped C binaries are detected, with parameters, and the binary
honesty check passes without a recorded skip. The scanner reads the functions a binary imports, the
algorithm names it fetches by string, the Go crypto packages compiled into it, and key sizes passed
as constants at the call site. It does not match raw bytes, so the two DH false positives of earlier
versions have not come back.

## 2. Compiled Java and minified JavaScript

All 11 findings in the three minified bundles are detected. In compiled Java, 6 of 11 Tier 5
findings are detected. The five missed are in source files, not class files: string assembly,
reflection and hand-rolled algorithms, which the scanner declares out of scope for its method.

Seven Tier 5 Python findings are missed for the same reasons (string assembly, dynamic import,
hand-rolled code) or sit in a `.pyc` file, which the scanner does not read.

## 3. Non-code assets

39 of 66 Tier 4 findings, up from 22. TLS cipher suites are reported one by one under their IANA
names. The 27 still missed:

| Where | Missed | What |
|---|---|---|
| IPsec (`swanctl.conf`, `ipsec.conf`) | 8 | cipher, integrity and DH-group proposals |
| Certificates | 7 | signature hash algorithms (declared out of scope) and a DER file |
| Keystores (`.p12`, `.jks`) | 4 | binary keystores (declared out of scope) |
| SSH | 3 | one cipher in `sshd_config`, an RSA host public key, an Ed25519 private key |
| Encrypted PEM key | 2 | the PBKDF2 and AES that protect the key |
| Kubernetes TLS secret | 2 | the certificate embedded as base64 in YAML |
| `openssl.cnf` | 1 | an RSA setting |

IPsec is the largest group that is plain text and in scope.

## 4. The 23 detections without parameters

| Where | Count | Why |
|---|---|---|
| Python | 9 | constants and wrappers in another module (Tier 3), the system fixture |
| Java | 6 | constants in another class, a strategy factory |
| Go | 4 | a block cipher returned from a factory, a value read from config |
| Certificates and keys | 2 | a secp256k1 key, an RSA key in the system fixture |
| TypeScript, C# | 2 | a table indexed by a runtime value, a ternary between two curves |

None carries a wrong parameter. Most need cross-file resolution. The last row is correct behavior:
with two possible values, the scanner should stay silent.

## 5. Still not detected at all

- **SHA3-256**: 7 findings, one in each language and one in the mixed fixtures.
- **LMS and XMSS**: 7 findings, in code, public keys and a signing policy.
- **Two hybrid TLS groups**: `X25519MLKEM768` in Go and `SecP384r1MLKEM1024` in an OpenSSL config.
- **Tier 2 in C and TypeScript**: 2 of 6 and 3 of 7. Algorithms chosen through a lookup table, a
  macro or a config object.
