# CBOM Testbench Scorecard: qScan 0.12.0

**Overall:** 75/410 findings detected (18.3% recall), 15 false positives (83.3% precision), parameters correct on 17.3% of detections.

Calibration cases (generated Tier 1-2 siblings of the hand-written cases; they feed the holdout's overfit gap and are not counted anywhere else here): 92/304 detected (30.3%), 0 false positives.

Password-gated findings (readable only by trying a well-known default password; scored separately, not in any number below): 0/2 detected.

| Bucket | Detected | Recall | 95% interval | At primary site | Params correct | Line accurate | Quantum flag | False pos. | Precision |
|---|---|---|---|---|---|---|---|---|---|
| Tier 1 c | 1/20 | 5.0% | 0.9–23.6% | 5.0% | 0.0% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 1 csharp | 4/13 | 30.8% | 12.7–57.6% | 30.8% | 0.0% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 1 go | 5/20 | 25.0% | 11.2–46.9% | 25.0% | 40.0% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 1 java | 6/16 | 37.5% | 18.5–61.4% | 37.5% | 33.3% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 1 javascript | 6/17 | 35.3% | 17.3–58.7% | 35.3% | 33.3% | 100.0% | 100.0% | 1 | 85.7% |
| Tier 1 python | 6/16 | 37.5% | 18.5–61.4% | 37.5% | 33.3% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 2 c | 1/6 | 16.7% | 3.0–56.4% (thin) | 16.7% | 0.0% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 2 csharp | 2/6 | 33.3% | 9.7–70.0% (thin) | 33.3% | 0.0% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 2 go | 2/6 | 33.3% | 9.7–70.0% (thin) | 33.3% | 0.0% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 2 java | 1/8 | 12.5% | 2.2–47.1% (thin) | 12.5% | 0.0% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 2 python | 2/9 | 22.2% | 6.3–54.7% (thin) | 22.2% | 0.0% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 2 typescript | 2/7 | 28.6% | 8.2–64.1% (thin) | 28.6% | 0.0% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 3 java | 1/7 | 14.3% | 2.6–51.3% (thin) | 14.3% | 0.0% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 3 python | 3/9 | 33.3% | 12.1–64.6% (thin) | 11.1% | 0.0% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 4 assets | 8/66 | 12.1% | 6.3–22.1% | 12.1% | 12.5% | 83.3% | 100.0% | 0 | 100.0% |
| Tier 5 c | 0/11 | 0.0% | 0.0–25.9% | 0.0% | n/a | n/a | n/a | 0 | n/a |
| Tier 5 java | 0/11 | 0.0% | 0.0–25.9% | 0.0% | n/a | n/a | n/a | 0 | n/a |
| Tier 5 javascript | 0/11 | 0.0% | 0.0–25.9% | 0.0% | n/a | n/a | n/a | 0 | n/a |
| Tier 5 python | 0/9 | 0.0% | 0.0–29.9% (thin) | 0.0% | n/a | n/a | n/a | 0 | n/a |
| Dead code c | 0/2 | 0.0% | 0.0–65.8% (thin) | 0.0% | n/a | n/a | n/a | 0 | n/a |
| Dead code go | 0/2 | 0.0% | 0.0–65.8% (thin) | 0.0% | n/a | n/a | n/a | 0 | n/a |
| Dead code java | 0/2 | 0.0% | 0.0–65.8% (thin) | 0.0% | n/a | n/a | n/a | 0 | n/a |
| Dead code javascript | 0/2 | 0.0% | 0.0–65.8% (thin) | 0.0% | n/a | n/a | n/a | 0 | n/a |
| Dead code python | 1/2 | 50.0% | 9.5–90.5% (thin) | 50.0% | 0.0% | 100.0% | 100.0% | 0 | 100.0% |
| Mixed files c | 0/13 | 0.0% | 0.0–22.8% | 0.0% | n/a | n/a | n/a | 0 | n/a |
| Mixed files go | 4/12 | 33.3% | 13.8–60.9% | 33.3% | 25.0% | 100.0% | 100.0% | 0 | 100.0% |
| Mixed files java | 3/13 | 23.1% | 8.2–50.3% | 23.1% | 33.3% | 100.0% | 100.0% | 0 | 100.0% |
| Mixed files javascript | 2/8 | 25.0% | 7.1–59.1% (thin) | 25.0% | 0.0% | 100.0% | 100.0% | 0 | 100.0% |
| Mixed files python | 4/12 | 33.3% | 13.8–60.9% | 33.3% | 0.0% | 100.0% | 100.0% | 0 | 100.0% |
| Mixed files typescript | 2/4 | 50.0% | 15.0–85.0% (thin) | 50.0% | 0.0% | 100.0% | 100.0% | 0 | 100.0% |
| PQC assets | 1/27 | 3.7% | 0.7–18.3% | 3.7% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| PQC go | 0/4 | 0.0% | 0.0–49.0% (thin) | 0.0% | n/a | n/a | n/a | 0 | n/a |
| PQC java | 1/6 | 16.7% | 3.0–56.4% (thin) | 16.7% | 0.0% | 100.0% | 100.0% | 2 | 33.3% |
| PQC python | 2/7 | 28.6% | 8.2–64.1% (thin) | 28.6% | 50.0% | 100.0% | 100.0% | 0 | 100.0% |
| System fixture artifacts | 0/6 | 0.0% | 0.0–39.0% (thin) | 0.0% | n/a | n/a | n/a | 0 | n/a |
| System fixture assets | 3/11 | 27.3% | 9.7–56.6% | 27.3% | 0.0% | 100.0% | 100.0% | 2 | 60.0% |
| System fixture go | 1/3 | 33.3% | 6.1–79.2% (thin) | 0.0% | 0.0% | 100.0% | 100.0% | 0 | 100.0% |
| System fixture java | 1/2 | 50.0% | 9.5–90.5% (thin) | 0.0% | 0.0% | 100.0% | 100.0% | 0 | 100.0% |
| System fixture python | 0/4 | 0.0% | 0.0–49.0% (thin) | 0.0% | n/a | n/a | n/a | 0 | n/a |
| **Total** | 75/410 | 18.3% | 14.9–22.3% | 17.3% | 17.3% | 98.6% | 100.0% | 15 | 83.3% |
| Negative controls | | | | | | | | 1 | |
## Parameter Recovery

Parameters correct among *detected* findings. See PARAMETER_CHEATSHEET.md for the fields required.

| Bucket | Detected | Parameters correct | % |
|---|---|---|---|
| **Overall** | 75 | 13 | 17.3% |
| Tier 1 | 28 | 8 | 28.6% |
| Tier 2 | 10 | 0 | 0.0% |
| Tier 3 | 4 | 0 | 0.0% |
| Tier 4 | 8 | 1 | 12.5% |
| Tier deadcode | 1 | 0 | 0.0% |
| Tier mixed | 15 | 2 | 13.3% |
| Tier pqc | 4 | 2 | 50.0% |
| Tier system | 5 | 0 | 0.0% |
| assets | 12 | 2 | 16.7% |
| c | 2 | 0 | 0.0% |
| csharp | 6 | 0 | 0.0% |
| go | 12 | 3 | 25.0% |
| java | 13 | 3 | 23.1% |
| javascript | 8 | 2 | 25.0% |
| python | 18 | 3 | 16.7% |
| typescript | 4 | 0 | 0.0% |
| RSA | 26 | 0 | 0.0% |
| EC | 22 | 0 | 0.0% |
| DH | 10 | 0 | 0.0% |
| X25519 | 7 | 7 | 100.0% |
| Ed25519 | 6 | 6 | 100.0% |
| DSA | 4 | 0 | 0.0% |

## Config Completeness

Findings in configuration files (TLS, SSH, IPsec, signing policies, Kubernetes, Terraform): how many were found, and of those, how many came with every expected parameter. The same findings count in recall and parameter accuracy; this isolates them. Asset links are in the linkage section.

| Bucket | Expected | Detected | Recall | Config-complete | % of detected |
|---|---|---|---|---|---|
| Configuration files | 62 | 6 | 9.7% | 1 | 16.7% |

## Binary Evidence Honesty

Known stripped binaries must either produce findings or a recorded skip. An empty result without a skip is a coverage honesty failure.

**Status:** FAIL (3 unrecorded empty binaries)

| Path | Reason |
|---|---|
| `corpus/tier5/c/bin/meterd` | binary: no findings and no recorded skip |
| `corpus/tier5/c/bin/keyd` | binary: no findings and no recorded skip |
| `corpus/tier5/c/bin/fwcheck` | binary: no findings and no recorded skip |


Intervals are 95% Wilson intervals on recall. 23 bucket(s) have fewer than 10 findings and are marked thin: read their rates as indications, not measurements.

**PQC over-claims: 0.** Post-quantum or hybrid algorithms reported where the code or config has none. Each one makes migration look further along than it is. Any number above zero should be explained by the vendor before purchase.

## System fixture: routing and asset links

**Routable: 3/5 detected system findings (60.0%)** (of 26). Routable means a reported location resolves, through the fixture's CODEOWNERS, to the team that owns the fix. Reporting only the shared wrapper or its config is detection, but the ticket lands with platform-security.

| Finding | Owner | Reported locations route to |
|---|---|---|
| SYS-GO-01 | @acme/edge-team | @acme/platform-security |
| SYS-JV-01 | @acme/ledger-team | @acme/platform-security |

**Asset links: 0/2.**

| Link | Found |
|---|---|
| nginx terminates TLS with this certificate (ssl_certificate) | no |
| the certificate's public key belongs to this private key | no |

**Recall** counts a finding reported anywhere acceptable, including the config or constants file that names the algorithm. **At primary site** counts only findings reported in the file the ground truth anchors them to: the crypto call itself or, for a shared wrapper, the caller that binds the parameters. It's the stricter number, and the one that tells an engineer what to change.

False positives in the bucket rows are those inside positive test files; negative-control false positives are counted separately and included in the total.

## Deadline view: NIST: IR 8547 (final) + SP 800-131A Rev. 2 + FIPS 186-5 + SP 800-52 Rev. 2

As of 2026-11-10. Each expected finding is dated under this policy; misses that fall due sooner weigh more.

**Deadline-weighted recall: 19.2%** (at primary site: 18.1%). **Findings due by end of 2030 that this scanner missed: 127.**

| When it's due | Weight | Detected | Recall | At primary site |
|---|---|---|---|---|
| Due now (not approved or past its date) | 5 | 18/103 | 17.5% | 16.5% |
| Due by end of 2030 | 4 | 0/42 | 0.0% | 0.0% |
| Due 2031 to 2033 | 3 | 0/0 | n/a | n/a |
| Due 2034 to 2035 | 2 | 56/112 | 50.0% | 47.3% |
| No deadline (approved, review, out of scope, unknown) | 1 | 1/153 | 0.7% | 0.7% |

| Missed | Algorithm | Due | File |
|---|---|---|---|
| T1-PY-01 | MD5 | **now** | `corpus/tier1/python/t1_hashes.py` |
| T1-PY-02 | SHA-1 | 2030-12-31 | `corpus/tier1/python/t1_hashes.py` |
| T1-PY-10 | 3DES-CBC | 2023-12-31 | `corpus/tier1/python/t1_triple_des.py` |
| T1-PY-11 | ChaCha20-Poly1305 | **now** | `corpus/tier1/python/t1_chacha.py` |
| T1-JV-01 | MD5 | **now** | `corpus/tier1/java/T1Hashes.java` |
| T1-JV-02 | SHA-1 | 2030-12-31 | `corpus/tier1/java/T1Hashes.java` |
| T1-JV-10 | DES-CBC | **now** | `corpus/tier1/java/T1LegacyCiphers.java` |
| T1-JV-11 | 3DES-CBC | 2023-12-31 | `corpus/tier1/java/T1LegacyCiphers.java` |
| T2-PY-01 | SHA-1 | 2030-12-31 | `corpus/tier2/python/t2_constant_hash.py` |
| T2-PY-04 | SHA-1 | 2030-12-31 | `corpus/tier2/python/t2_env_default.py` |
| T2-PY-06 | MD5 | **now** | `corpus/tier2/python/t2_dispatch_table.py` |
| T2-PY-08 | HMAC-SHA-1 | 2030-12-31 | `corpus/tier2/python/t2_partial.py` |
| T2-JV-01 | 3DES-CBC | 2023-12-31 | `corpus/tier2/java/T2ConcatTransform.java` |
| T2-JV-02 | RSA-1024 | 2013-12-31 | `corpus/tier2/java/T2PropertiesConfig.java` |
| T2-JV-03 | MD5 | **now** | `corpus/tier2/java/T2Wrapper.java` |
| T2-JV-04 | SHA-1 | 2030-12-31 | `corpus/tier2/java/T2Enum.java` |
| T2-JV-07 | DSA-1024 | 2013-12-31 | `corpus/tier2/java/T2DsaConstant.java` |
| T3-PY-02 | SHA-1 | 2030-12-31 | `corpus/tier3/python/cross_module_constant/tokens/fingerprint.py` |
| T3-PY-07 | ChaCha20-Poly1305 | **now** | `corpus/tier3/python/registry_strategy/suites/builtin.py` |
| T3-PY-08 | MD5 | **now** | `corpus/tier3/python/dependency_injection/wiring.py` |
| T3-JV-02 | SHA-1 | 2030-12-31 | `corpus/tier3/java/cross_class_constant/src/com/acme/tokens/Fingerprint.java` |
| T3-JV-05 | 3DES-CBC | 2023-12-31 | `corpus/tier3/java/strategy_factory/src/com/acme/crypto/LegacyDesedeCipher.java` |
| T3-JV-06 | MD5 | **now** | `corpus/tier3/java/dependency_injection/src/com/acme/audit/DigestProvider.java` |
| T4-AS-03 | RSA-1024 | 2013-12-31 | `corpus/tier4/assets/certs/payments_legacy.crt` |
| T4-AS-04 | SHA-1 | 2030-12-31 | `corpus/tier4/assets/certs/payments_legacy.crt` |
| T4-AS-24 | RSA-1024 | 2013-12-31 | `corpus/tier4/assets/keystores/partner_truststore.jks` |
| T4-AS-25 | SHA-1 | 2030-12-31 | `corpus/tier4/assets/keystores/partner_truststore.jks` |
| T4-AS-30 | ChaCha20-Poly1305 | **now** | `corpus/tier4/assets/ssh/sshd_config` |
| T4-AS-31 | HMAC-SHA-1 | 2030-12-31 | `corpus/tier4/assets/ssh/sshd_config` |
| T4-AS-38 | TLS_RSA_WITH_3DES_EDE_CBC_SHA | **now** | `corpus/tier4/assets/tls/nginx.conf` |
| T4-AS-44 | RSA-1024 | 2013-12-31 | `corpus/tier4/assets/tls/openssl.cnf` |
| T4-AS-45 | SHA-1 | 2030-12-31 | `corpus/tier4/assets/tls/openssl.cnf` |
| T4-AS-53 | TLS_RSA_WITH_3DES_EDE_CBC_SHA | **now** | `corpus/tier4/assets/tls/httpd-ssl.conf` |
| T4-AS-58 | TLS_CHACHA20_POLY1305_SHA256 | **now** | `corpus/tier4/assets/tls/haproxy.cfg` |
| T4-AS-59 | DH-1024 | 2013-12-31 | `corpus/tier4/assets/tls/haproxy.cfg` |
| T4-AS-63 | ChaCha20-Poly1305 | **now** | `corpus/tier4/assets/ipsec/swanctl.conf` |
| T4-AS-65 | 3DES | 2023-12-31 | `corpus/tier4/assets/ipsec/ipsec.conf` |
| T4-AS-66 | HMAC-SHA-1 | 2030-12-31 | `corpus/tier4/assets/ipsec/ipsec.conf` |
| T5-PY-01 | SHA-1 | 2030-12-31 | `corpus/tier5/python/t5_string_assembly.py` |
| T5-PY-02 | MD5 | **now** | `corpus/tier5/python/t5_string_assembly.py` |
| T5-PY-05 | RC4 | **now** | `corpus/tier5/python/t5_handrolled_keystream.py` |
| T5-PY-07 | RSA-1024 | 2013-12-31 | `corpus/tier5/python/t5_handrolled_pubkey.py` |
| T5-PY-08 | SHA-1 | 2030-12-31 | `corpus/tier5/python/compiled/ledger_sync.pyc` |
| T5-PY-09 | HMAC-MD5 | **now** | `corpus/tier5/python/compiled/ledger_sync.pyc` |
| T5-JV-02 | 3DES-CBC | 2023-12-31 | `corpus/tier5/java/T5StringAssembly.java` |
| T5-JV-03 | MD5 | **now** | `corpus/tier5/java/T5Reflection.java` |
| T5-JV-04 | TEA | **now** | `corpus/tier5/java/T5BlockTransform.java` |
| T5-JV-07 | RSA-1024 | 2013-12-31 | `corpus/tier5/java/compiled/billing-core.jar` |
| T5-JV-08 | SHA-1 | 2030-12-31 | `corpus/tier5/java/compiled/billing-core.jar` |
| T5-JV-09 | DES-ECB | **now** | `corpus/tier5/java/compiled/token-vault.jar` |
| T5-JV-10 | SHA-1 | 2030-12-31 | `corpus/tier5/java/compiled/token-vault.jar` |
| T5-JS-01 | MD5 | **now** | `corpus/tier5/javascript/dist/session-tokens.min.js` |
| T5-JS-03 | RSA-1024 | 2013-12-31 | `corpus/tier5/javascript/dist/session-tokens.min.js` |
| T5-JS-04 | SHA-1 | 2030-12-31 | `corpus/tier5/javascript/dist/payments-sdk.min.js` |
| T5-JS-05 | HMAC-MD5 | **now** | `corpus/tier5/javascript/dist/payments-sdk.min.js` |
| T5-JS-06 | 3DES-CBC | 2023-12-31 | `corpus/tier5/javascript/dist/payments-sdk.min.js` |
| T5-JS-08 | PBKDF2-HMAC-SHA-1 | 2030-12-31 | `corpus/tier5/javascript/dist/webhook-relay.min.js` |
| T5-JS-10 | DH-1024 | 2013-12-31 | `corpus/tier5/javascript/dist/webhook-relay.min.js` |
| T5-C-01 | MD5 | **now** | `corpus/tier5/c/bin/meterd` |
| T5-C-02 | 3DES-CBC | 2023-12-31 | `corpus/tier5/c/bin/meterd` |
| T5-C-03 | RSA-1024 | 2013-12-31 | `corpus/tier5/c/bin/meterd` |
| T5-C-04 | SHA-1 | 2030-12-31 | `corpus/tier5/c/bin/keyd` |
| T5-C-05 | HMAC-MD5 | **now** | `corpus/tier5/c/bin/keyd` |
| PQ-AS-19 | ChaCha20-Poly1305 | **now** | `corpus/pqc/assets/ssh/sshd_config_pq` |
| T1-GO-01 | MD5 | **now** | `corpus/tier1/go/hashes/main.go` |
| T1-GO-02 | SHA-1 | 2030-12-31 | `corpus/tier1/go/hashes/main.go` |
| T1-GO-07 | 3DES-CBC | 2023-12-31 | `corpus/tier1/go/des/main.go` |
| T1-GO-08 | DES-CBC | **now** | `corpus/tier1/go/des/main.go` |
| T1-GO-09 | RC4 | **now** | `corpus/tier1/go/rc4/main.go` |
| T1-GO-18 | TLS_RSA_WITH_3DES_EDE_CBC_SHA | **now** | `corpus/tier1/go/tls_config/main.go` |
| T2-GO-01 | SHA-1 | 2030-12-31 | `corpus/tier2/go/hash_enum/main.go` |
| T2-GO-04 | HMAC-MD5 | **now** | `corpus/tier2/go/hmac_func_value/main.go` |
| T2-GO-06 | 3DES-CBC | 2023-12-31 | `corpus/tier2/go/block_factory/main.go` |
| T1-JS-01 | MD5 | **now** | `corpus/tier1/javascript/t1_hashes.js` |
| T1-JS-02 | SHA-1 | 2030-12-31 | `corpus/tier1/javascript/t1_hashes.js` |
| T1-JS-07 | 3DES-CBC | 2023-12-31 | `corpus/tier1/javascript/t1_triple_des.js` |
| T1-JS-08 | ChaCha20-Poly1305 | **now** | `corpus/tier1/javascript/t1_chacha.js` |
| T1-JS-17 | SHA-1 | 2030-12-31 | `corpus/tier1/javascript/t1_webcrypto.mjs` |
| T2-TS-01 | 3DES-CBC | 2023-12-31 | `corpus/tier2/typescript/t2_config_object.ts` |
| T2-TS-02 | SHA-1 | 2030-12-31 | `corpus/tier2/typescript/t2_default_param.ts` |
| T2-TS-07 | HMAC-MD5 | **now** | `corpus/tier2/typescript/t2_hmac_const.ts` |
| T1-C-01 | MD5 | **now** | `corpus/tier1/c/t1_digests.c` |
| T1-C-02 | SHA-1 | 2030-12-31 | `corpus/tier1/c/t1_digests.c` |
| T1-C-07 | 3DES-CBC | 2023-12-31 | `corpus/tier1/c/t1_triple_des.c` |
| T1-C-08 | ChaCha20-Poly1305 | **now** | `corpus/tier1/c/t1_chacha.c` |
| T1-C-16 | PBKDF2-HMAC-SHA-1 | 2030-12-31 | `corpus/tier1/c/t1_mac_kdf.c` |
| T1-C-18 | TLS_RSA_WITH_3DES_EDE_CBC_SHA | **now** | `corpus/tier1/c/t1_tls_ctx.c` |
| T1-CS-01 | MD5 | **now** | `corpus/tier1/csharp/Hashes/Program.cs` |
| T1-CS-02 | SHA-1 | 2030-12-31 | `corpus/tier1/csharp/Hashes/Program.cs` |
| T1-CS-10 | 3DES-CBC | 2023-12-31 | `corpus/tier1/csharp/TripleDesLegacy/Program.cs` |
| T2-C-02 | SHA-1 | 2030-12-31 | `corpus/tier2/c/t2_digest_table.c` |
| T2-C-05 | HMAC-MD5 | **now** | `corpus/tier2/c/t2_func_ptr.c` |
| T2-C-06 | 3DES-ECB | 2023-12-31 | `corpus/tier2/c/t2_cipher_struct.c` |
| T2-CS-02 | SHA-1 | 2030-12-31 | `corpus/tier2/csharp/HashByName/Program.cs` |
| T2-CS-03 | MD5 | **now** | `corpus/tier2/csharp/DispatchTable/Program.cs` |
| MX-PY-2d | ChaCha20-Poly1305 | **now** | `corpus/mixed/python/invoice_service.py` |
| MX-PY-3a | SHA-1 | 2030-12-31 | `corpus/mixed/python/order_jobs.py` |
| MX-JV-1b | SHA-1 | 2030-12-31 | `corpus/mixed/java/VoucherProfileModule.java` |
| MX-JV-3b | 3DES-ECB | 2023-12-31 | `corpus/mixed/java/OrderDefaultsModule.java` |
| MX-JV-3c | ChaCha20-Poly1305 | **now** | `corpus/mixed/java/OrderDefaultsModule.java` |
| MX-JV-3e | 3DES-CBC | 2023-12-31 | `corpus/mixed/java/OrderDefaultsModule.java` |
| MX-GO-2b | DES-CBC | **now** | `corpus/mixed/go/report_gateway/main.go` |
| MX-GO-2c | PBKDF2-HMAC-SHA-1 | 2030-12-31 | `corpus/mixed/go/report_gateway/main.go` |
| MX-GO-2d | 3DES-CBC | 2023-12-31 | `corpus/mixed/go/report_gateway/main.go` |
| MX-GO-3b | RC4 | **now** | `corpus/mixed/go/invoice_gateway/main.go` |
| MX-GO-3c | HMAC-SHA-1 | 2030-12-31 | `corpus/mixed/go/invoice_gateway/main.go` |
| MX-C-1a | SHA-1 | 2030-12-31 | `corpus/mixed/c/device_daemon.c` |
| MX-C-1c | HMAC-MD5 | **now** | `corpus/mixed/c/device_daemon.c` |
| MX-C-2c | 3DES-ECB | 2023-12-31 | `corpus/mixed/c/policy_agent.c` |
| MX-C-2d | 3DES-CBC | 2023-12-31 | `corpus/mixed/c/policy_agent.c` |
| MX-C-3b | 3DES-CBC | 2023-12-31 | `corpus/mixed/c/audit_daemon.c` |
| SYS-GO-02 | HMAC-SHA-1 | 2030-12-31 | `corpus/system/payments-platform/services/api-gateway/main.go` |
| SYS-PY-02 | HMAC-SHA-1 | 2030-12-31 | `corpus/system/payments-platform/services/settlement-worker/worker.py` |
| SYS-PY-03 | RSA-1024 | 2013-12-31 | `corpus/system/payments-platform/services/settlement-worker/partner_ca.py` |
| SYS-PY-04 | SHA-1 | 2030-12-31 | `corpus/system/payments-platform/services/settlement-worker/partner_ca.py` |
| SYS-JV-02 | SHA-1 | 2030-12-31 | `corpus/system/payments-platform/services/ledger-service/src/main/java/com/acme/ledger/LedgerService.java` |
| SYS-AR-02 | SHA-1 | 2030-12-31 | `corpus/system/payments-platform/services/ledger-service/build/libs/ledger-service.jar` |
| SYS-AR-05 | SHA-1 | 2030-12-31 | `corpus/system/payments-platform/services/api-gateway/bin/api-gateway` |
| DC-PY-01 | MD5 | **now** | `corpus/deadcode/python/dead_export.py` |
| DC-JV-01 | DES-CBC | **now** | `corpus/deadcode/java/DeadLegacy.java` |
| DC-JV-02 | SHA-1 | 2030-12-31 | `corpus/deadcode/java/DeadLegacy.java` |
| DC-GO-01 | MD5 | **now** | `corpus/deadcode/go/legacy/main.go` |
| DC-GO-02 | RC4 | **now** | `corpus/deadcode/go/legacy/main.go` |
| DC-JS-01 | MD5 | **now** | `corpus/deadcode/javascript/dead_paths.js` |
| DC-JS-02 | 3DES-CBC | 2023-12-31 | `corpus/deadcode/javascript/dead_paths.js` |
| DC-C-01 | MD5 | **now** | `corpus/deadcode/c/dead_branches.c` |
| DC-C-02 | 3DES-CBC | 2023-12-31 | `corpus/deadcode/c/dead_branches.c` |

## Actionability: could an engineer open a ticket from this?

Rubric `cbom-actionability-v1` (proposed; see `rubric/actionability.json`). Each detected finding is checked for the fields a migration ticket needs. Facts are checked against the real files.

**Ticket-ready: 13/75 detected findings (17.3%)**, meaning every must-have is present and correct. **Actionable recall: 3.2%** of all 410 expected findings were both found and ticket-ready. Field completeness across all checks: 61.6%.

| Check | Tier | Applies to | Passed | Rate |
|---|---|---|---|---|
| Exact location | must | 75 | 74 | 98.7% |
| Correct parameters | must | 62 | 0 | 0.0% |
| Primitive, where the family is ambiguous | must | 48 | 45 | 93.8% |
| Certificate expiry (correct) | must | 0 | 0 | n/a |
| Certificate subject (correct) | must | 0 | 0 | n/a |
| Key material type | must | 5 | 3 | 60.0% |
| Protocol version | must | 0 | 0 | n/a |
| OID | should | 75 | 0 | 0.0% |
| Crypto functions | should | 75 | 72 | 96.0% |
| Quantum security level (correct) | should | 75 | 72 | 96.0% |
| Code context | should | 31 | 31 | 100.0% |
| Providing library | should | 31 | 0 | 0.0% |
| Certificate issuer | should | 0 | 0 | n/a |
| Certificate start date | should | 0 | 0 | n/a |
| Certificate key and signature linked | should | 0 | 0 | n/a |
| Key format | should | 5 | 0 | 0.0% |
| Cipher suite in a protocol | should | 0 | 0 | n/a |

Detected but not ticket-ready (62), first 25:

| ID | Algorithm | Missing must-haves |
|---|---|---|
| T1-PY-05 | RSA-2048 | Correct parameters |
| T1-PY-06 | ECC-P-256 | Correct parameters |
| T1-PY-07 | DSA-2048 | Correct parameters |
| T1-PY-14 | DH-2048 | Correct parameters |
| T1-JV-05 | RSA-3072 | Correct parameters |
| T1-JV-06 | ECC-P-256 | Correct parameters |
| T1-JV-07 | DSA-2048 | Correct parameters |
| T1-JV-14 | DH-2048 | Correct parameters |
| T2-PY-02 | RSA-1024 | Correct parameters |
| T2-PY-09 | ECC-P-384 | Correct parameters |
| T2-JV-08 | ECC-P-384 | Correct parameters |
| T3-PY-01 | RSA-1024 | Correct parameters |
| T3-PY-04 | RSA-1024 | Correct parameters |
| T3-PY-05 | RSA-3072 | Correct parameters |
| T3-JV-01 | RSA-1024 | Correct parameters |
| T4-AS-15 | ECC-secp256k1 | Correct parameters, Primitive, where the family is ambiguous |
| T4-AS-18 | RSA-2048 | Correct parameters, Key material type |
| T4-AS-19 | ECC-P-256 | Correct parameters, Key material type |
| T4-AS-27 | DH-2048 | Correct parameters |
| T4-AS-32 | RSA-2048 | Correct parameters, Primitive, where the family is ambiguous |
| T4-AS-62 | DH-2048 | Correct parameters |
| T4-AS-67 | DH-1024 | Correct parameters |
| PQ-PY-06 | ECC-P-256 | Correct parameters |
| PQ-JV-04 | ECC-P-384 | Correct parameters |
| T1-GO-10 | RSA-2048 | Correct parameters |

## Missed findings

| ID | File | Expected | Line |
|---|---|---|---|
| T1-PY-01 | `corpus/tier1/python/t1_hashes.py` | MD5  | 6 |
| T1-PY-02 | `corpus/tier1/python/t1_hashes.py` | SHA-1  | 7 |
| T1-PY-03 | `corpus/tier1/python/t1_hashes.py` | SHA-256  | 8 |
| T1-PY-04 | `corpus/tier1/python/t1_hashes.py` | SHA3-256  | 9 |
| T1-PY-08 | `corpus/tier1/python/t1_aes_ecb.py` | AES {'key_size': 128, 'mode': 'ECB'} | 7 |
| T1-PY-09 | `corpus/tier1/python/t1_aes_gcm.py` | AES {'key_size': 256, 'mode': 'GCM'} | 6 |
| T1-PY-10 | `corpus/tier1/python/t1_triple_des.py` | 3DES {'mode': 'CBC'} | 9 |
| T1-PY-11 | `corpus/tier1/python/t1_chacha.py` | ChaCha20-Poly1305  | 6 |
| T1-PY-15 | `corpus/tier1/python/t1_mac_kdf.py` | HMAC {'hash': 'SHA-256'} | 9 |
| T1-PY-16 | `corpus/tier1/python/t1_mac_kdf.py` | PBKDF2 {'hash': 'SHA-256'} | 11 |
| T1-JV-01 | `corpus/tier1/java/T1Hashes.java` | MD5  | 10 |
| T1-JV-02 | `corpus/tier1/java/T1Hashes.java` | SHA-1  | 11 |
| T1-JV-03 | `corpus/tier1/java/T1Hashes.java` | SHA-256  | 12 |
| T1-JV-04 | `corpus/tier1/java/T1Hashes.java` | SHA3-256  | 13 |
| T1-JV-08 | `corpus/tier1/java/T1AesEcb.java` | AES {'key_size': 128, 'mode': 'ECB'} | 12 |
| T1-JV-09 | `corpus/tier1/java/T1AesGcm.java` | AES {'key_size': 256, 'mode': 'GCM'} | 17 |
| T1-JV-10 | `corpus/tier1/java/T1LegacyCiphers.java` | DES {'mode': 'CBC'} | 9 |
| T1-JV-11 | `corpus/tier1/java/T1LegacyCiphers.java` | 3DES {'mode': 'CBC'} | 14 |
| T1-JV-15 | `corpus/tier1/java/T1MacKdf.java` | HMAC {'hash': 'SHA-256'} | 10 |
| T1-JV-16 | `corpus/tier1/java/T1MacKdf.java` | PBKDF2 {'hash': 'SHA-256'} | 16 |
| T2-PY-01 | `corpus/tier2/python/t2_constant_hash.py` | SHA-1  | 8 |
| T2-PY-03 | `corpus/tier2/python/t2_config_cipher.py` | AES {'key_size': 128, 'mode': 'CBC'} | 16 |
| T2-PY-04 | `corpus/tier2/python/t2_env_default.py` | SHA-1  | 10 |
| T2-PY-05 | `corpus/tier2/python/t2_wrapper.py` | AES {'key_size': 192, 'mode': 'CBC'} | 8 |
| T2-PY-06 | `corpus/tier2/python/t2_dispatch_table.py` | MD5  | 6 |
| T2-PY-07 | `corpus/tier2/python/t2_dispatch_table.py` | SHA-256  | 7 |
| T2-PY-08 | `corpus/tier2/python/t2_partial.py` | HMAC {'hash': 'SHA-1'} | 5 |
| T2-JV-01 | `corpus/tier2/java/T2ConcatTransform.java` | 3DES {'mode': 'CBC'} | 13 |
| T2-JV-02 | `corpus/tier2/java/T2PropertiesConfig.java` | RSA {'key_size': 1024} | 17 |
| T2-JV-03 | `corpus/tier2/java/T2Wrapper.java` | MD5  | 10 |
| T2-JV-04 | `corpus/tier2/java/T2Enum.java` | SHA-1  | 6 |
| T2-JV-05 | `corpus/tier2/java/T2Enum.java` | SHA-256  | 7 |
| T2-JV-06 | `corpus/tier2/java/T2SysProp.java` | AES {'key_size': 128, 'mode': 'ECB'} | 15 |
| T2-JV-07 | `corpus/tier2/java/T2DsaConstant.java` | DSA {'key_size': 1024} | 10 |
| T3-PY-02 | `corpus/tier3/python/cross_module_constant/tokens/fingerprint.py` | SHA-1  | 8 |
| T3-PY-03 | `corpus/tier3/python/cross_module_constant/sessions/crypto.py` | AES {'key_size': 128, 'mode': 'GCM'} | 10 |
| T3-PY-06 | `corpus/tier3/python/registry_strategy/suites/builtin.py` | AES {'key_size': 256, 'mode': 'CBC'} | 11 |
| T3-PY-07 | `corpus/tier3/python/registry_strategy/suites/builtin.py` | ChaCha20-Poly1305  | 18 |
| T3-PY-08 | `corpus/tier3/python/dependency_injection/wiring.py` | MD5  | 9 |
| T3-PY-09 | `corpus/tier3/python/jwt_alg_mapping/jwtlib/signer.py` | HMAC {'hash': 'SHA-256'} | 23 |
| T3-JV-02 | `corpus/tier3/java/cross_class_constant/src/com/acme/tokens/Fingerprint.java` | SHA-1  | 10 |
| T3-JV-03 | `corpus/tier3/java/cross_class_constant/src/com/acme/session/SessionCrypto.java` | AES {'key_size': 128, 'mode': 'GCM'} | 23 |
| T3-JV-04 | `corpus/tier3/java/strategy_factory/src/com/acme/crypto/AesCbcCipher.java` | AES {'key_size': 256, 'mode': 'CBC'} | 23 |
| T3-JV-05 | `corpus/tier3/java/strategy_factory/src/com/acme/crypto/LegacyDesedeCipher.java` | 3DES {'mode': 'CBC'} | 17 |
| T3-JV-06 | `corpus/tier3/java/dependency_injection/src/com/acme/audit/DigestProvider.java` | MD5  | 14 |
| T3-JV-07 | `corpus/tier3/java/jwt_alg_mapping/src/com/acme/jwt/JwtSigner.java` | HMAC {'hash': 'SHA-256'} | 23 |
| T4-AS-01 | `corpus/tier4/assets/certs/api_gateway.pem` | RSA {'key_size': 2048} | file |
| T4-AS-02 | `corpus/tier4/assets/certs/api_gateway.pem` | SHA-256  | file |
| T4-AS-03 | `corpus/tier4/assets/certs/payments_legacy.crt` | RSA {'key_size': 1024} | file |
| T4-AS-04 | `corpus/tier4/assets/certs/payments_legacy.crt` | SHA-1  | file |
| T4-AS-05 | `corpus/tier4/assets/certs/telemetry_ecdsa.pem` | EC {'curve': 'P-256'} | file |
| T4-AS-06 | `corpus/tier4/assets/certs/telemetry_ecdsa.pem` | SHA-256  | file |
| T4-AS-07 | `corpus/tier4/assets/certs/device_ed25519.pem` | Ed25519  | file |
| T4-AS-08 | `corpus/tier4/assets/certs/portal_fullchain.pem` | EC {'curve': 'P-384'} | file |
| T4-AS-09 | `corpus/tier4/assets/certs/portal_fullchain.pem` | SHA-384  | file |
| T4-AS-10 | `corpus/tier4/assets/certs/portal_fullchain.pem` | RSA {'key_size': 3072} | file |
| T4-AS-11 | `corpus/tier4/assets/certs/portal_fullchain.pem` | SHA-256  | file |
| T4-AS-12 | `corpus/tier4/assets/certs/mainframe_gateway.der` | RSA {'key_size': 4096} | file |
| T4-AS-13 | `corpus/tier4/assets/certs/mainframe_gateway.der` | SHA-512  | file |
| T4-AS-14 | `corpus/tier4/assets/keys/billing_service.pem` | RSA {'key_size': 3072} | file |
| T4-AS-16 | `corpus/tier4/assets/keys/backup_signing_encrypted.pem` | PBKDF2 {'hash': 'SHA-256'} | file |
| T4-AS-17 | `corpus/tier4/assets/keys/backup_signing_encrypted.pem` | AES {'key_size': 256, 'mode': 'CBC'} | file |
| T4-AS-20 | `corpus/tier4/assets/keystores/orders_keystore.p12` | AES {'key_size': 256, 'mode': 'CBC'} | file |
| T4-AS-21 | `corpus/tier4/assets/keystores/orders_keystore.p12` | PBKDF2 {'hash': 'SHA-256'} | file |
| T4-AS-24 | `corpus/tier4/assets/keystores/partner_truststore.jks` | RSA {'key_size': 1024} | file |
| T4-AS-25 | `corpus/tier4/assets/keystores/partner_truststore.jks` | SHA-1  | file |
| T4-AS-26 | `corpus/tier4/assets/ssh/sshd_config` | RSA  | 8 |
| T4-AS-29 | `corpus/tier4/assets/ssh/sshd_config` | AES {'key_size': 128, 'mode': 'CBC'} | 10 |
| T4-AS-30 | `corpus/tier4/assets/ssh/sshd_config` | ChaCha20-Poly1305  | 10 |
| T4-AS-31 | `corpus/tier4/assets/ssh/sshd_config` | HMAC {'hash': 'SHA-1'} | 11 |
| T4-AS-33 | `corpus/tier4/assets/ssh/deploy_id_ed25519` | Ed25519  | file |
| T4-AS-34 | `corpus/tier4/assets/tls/nginx.conf` | TLS-1.0  | 20 |
| T4-AS-35 | `corpus/tier4/assets/tls/nginx.conf` | TLS-1.1  | 20 |
| T4-AS-36 | `corpus/tier4/assets/tls/nginx.conf` | TLS-1.2  | 20 |
| T4-AS-37 | `corpus/tier4/assets/tls/nginx.conf` | TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256  | 21 |
| T4-AS-38 | `corpus/tier4/assets/tls/nginx.conf` | TLS_RSA_WITH_3DES_EDE_CBC_SHA  | 21 |
| T4-AS-39 | `corpus/tier4/assets/tls/nginx.conf` | TLS_RSA_WITH_AES_256_CBC_SHA  | 21 |
| T4-AS-40 | `corpus/tier4/assets/tls/application.yml` | TLS-1.1  | 13 |
| T4-AS-41 | `corpus/tier4/assets/tls/application.yml` | TLS-1.2  | 13 |
| T4-AS-42 | `corpus/tier4/assets/tls/application.yml` | TLS_RSA_WITH_AES_128_CBC_SHA  | 15 |
| T4-AS-43 | `corpus/tier4/assets/tls/application.yml` | TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384  | 16 |
| T4-AS-44 | `corpus/tier4/assets/tls/openssl.cnf` | RSA {'key_size': 1024} | 16 |
| T4-AS-45 | `corpus/tier4/assets/tls/openssl.cnf` | SHA-1  | 17 |
| T4-AS-46 | `corpus/tier4/assets/tls/openssl.cnf` | TLS-1.0  | 12 |
| T4-AS-47 | `corpus/tier4/assets/k8s/ingress-tls-secret.yaml` | EC {'curve': 'P-384'} | file |
| T4-AS-48 | `corpus/tier4/assets/k8s/ingress-tls-secret.yaml` | SHA-384  | file |
| T4-AS-49 | `corpus/tier4/assets/tls/httpd-ssl.conf` | TLS-1.1  | 14 |
| T4-AS-50 | `corpus/tier4/assets/tls/httpd-ssl.conf` | TLS-1.2  | 14 |
| T4-AS-51 | `corpus/tier4/assets/tls/httpd-ssl.conf` | TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384  | 15 |
| T4-AS-52 | `corpus/tier4/assets/tls/httpd-ssl.conf` | TLS_RSA_WITH_AES_128_CBC_SHA  | 15 |
| T4-AS-53 | `corpus/tier4/assets/tls/httpd-ssl.conf` | TLS_RSA_WITH_3DES_EDE_CBC_SHA  | 15 |
| T4-AS-54 | `corpus/tier4/assets/tls/haproxy.cfg` | TLS-1.1  | 6 |
| T4-AS-55 | `corpus/tier4/assets/tls/haproxy.cfg` | TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256  | 7 |
| T4-AS-56 | `corpus/tier4/assets/tls/haproxy.cfg` | TLS_RSA_WITH_AES_256_CBC_SHA  | 7 |
| T4-AS-57 | `corpus/tier4/assets/tls/haproxy.cfg` | TLS_AES_256_GCM_SHA384  | 8 |
| T4-AS-58 | `corpus/tier4/assets/tls/haproxy.cfg` | TLS_CHACHA20_POLY1305_SHA256  | 8 |
| T4-AS-59 | `corpus/tier4/assets/tls/haproxy.cfg` | DH {'key_size': 1024} | 5 |
| T4-AS-60 | `corpus/tier4/assets/ipsec/swanctl.conf` | AES {'key_size': 256} | 7 |
| T4-AS-61 | `corpus/tier4/assets/ipsec/swanctl.conf` | HMAC {'hash': 'SHA-256'} | 7 |
| T4-AS-63 | `corpus/tier4/assets/ipsec/swanctl.conf` | ChaCha20-Poly1305  | 21 |
| T4-AS-64 | `corpus/tier4/assets/ipsec/swanctl.conf` | X25519  | 21 |
| T4-AS-65 | `corpus/tier4/assets/ipsec/ipsec.conf` | 3DES  | 12 |
| T4-AS-66 | `corpus/tier4/assets/ipsec/ipsec.conf` | HMAC {'hash': 'SHA-1'} | 12 |
| T4-AS-68 | `corpus/tier4/assets/ipsec/ipsec.conf` | AES {'key_size': 128} | 13 |
| T5-PY-01 | `corpus/tier5/python/t5_string_assembly.py` | SHA-1  | 10 |
| T5-PY-02 | `corpus/tier5/python/t5_string_assembly.py` | MD5  | 14 |
| T5-PY-03 | `corpus/tier5/python/t5_dynamic_import.py` | RSA {'key_size': 2048} | 10 |
| T5-PY-04 | `corpus/tier5/python/t5_char_codes.py` | AES {'key_size': 128, 'mode': 'ECB'} | 11 |
| T5-PY-05 | `corpus/tier5/python/t5_handrolled_keystream.py` | RC4  | 13 |
| T5-PY-06 | `corpus/tier5/python/t5_handrolled_digest.py` | SHA-256  | 31 |
| T5-PY-07 | `corpus/tier5/python/t5_handrolled_pubkey.py` | RSA {'key_size': 1024} | 17 |
| T5-PY-08 | `corpus/tier5/python/compiled/ledger_sync.pyc` | SHA-1  | file |
| T5-PY-09 | `corpus/tier5/python/compiled/ledger_sync.pyc` | HMAC {'hash': 'MD5'} | file |
| T5-JV-01 | `corpus/tier5/java/T5StringAssembly.java` | RSA {'key_size': 2048} | 9 |
| T5-JV-02 | `corpus/tier5/java/T5StringAssembly.java` | 3DES {'mode': 'CBC'} | 14 |
| T5-JV-03 | `corpus/tier5/java/T5Reflection.java` | MD5  | 10 |
| T5-JV-04 | `corpus/tier5/java/T5BlockTransform.java` | TEA  | 3 |
| T5-JV-05 | `corpus/tier5/java/T5HandrolledPubkey.java` | RSA {'key_size': 2048} | 19 |
| T5-JV-06 | `corpus/tier5/java/compiled/billing-core.jar` | AES {'key_size': 128, 'mode': 'CBC'} | file |
| T5-JV-07 | `corpus/tier5/java/compiled/billing-core.jar` | RSA {'key_size': 1024} | file |
| T5-JV-08 | `corpus/tier5/java/compiled/billing-core.jar` | SHA-1  | file |
| T5-JV-09 | `corpus/tier5/java/compiled/token-vault.jar` | DES {'mode': 'ECB'} | file |
| T5-JV-10 | `corpus/tier5/java/compiled/token-vault.jar` | SHA-1  | file |
| T5-JV-11 | `corpus/tier5/java/compiled/token-vault.jar` | EC {'curve': 'P-256'} | file |
| T5-JS-01 | `corpus/tier5/javascript/dist/session-tokens.min.js` | MD5  | 1 |
| T5-JS-02 | `corpus/tier5/javascript/dist/session-tokens.min.js` | AES {'key_size': 128, 'mode': 'CBC'} | 1 |
| T5-JS-03 | `corpus/tier5/javascript/dist/session-tokens.min.js` | RSA {'key_size': 1024} | 1 |
| T5-JS-04 | `corpus/tier5/javascript/dist/payments-sdk.min.js` | SHA-1  | 1 |
| T5-JS-05 | `corpus/tier5/javascript/dist/payments-sdk.min.js` | HMAC {'hash': 'MD5'} | 1 |
| T5-JS-06 | `corpus/tier5/javascript/dist/payments-sdk.min.js` | 3DES {'mode': 'CBC'} | 1 |
| T5-JS-07 | `corpus/tier5/javascript/dist/payments-sdk.min.js` | EC {'curve': 'P-256'} | 1 |
| T5-JS-08 | `corpus/tier5/javascript/dist/webhook-relay.min.js` | PBKDF2 {'hash': 'SHA-1'} | 1 |
| T5-JS-09 | `corpus/tier5/javascript/dist/webhook-relay.min.js` | AES {'key_size': 256, 'mode': 'GCM'} | 1 |
| T5-JS-10 | `corpus/tier5/javascript/dist/webhook-relay.min.js` | DH {'key_size': 1024} | 1 |
| T5-JS-11 | `corpus/tier5/javascript/dist/webhook-relay.min.js` | Ed25519  | 1 |
| T5-C-01 | `corpus/tier5/c/bin/meterd` | MD5  | file |
| T5-C-02 | `corpus/tier5/c/bin/meterd` | 3DES {'mode': 'CBC'} | file |
| T5-C-03 | `corpus/tier5/c/bin/meterd` | RSA {'key_size': 1024} | file |
| T5-C-04 | `corpus/tier5/c/bin/keyd` | SHA-1  | file |
| T5-C-05 | `corpus/tier5/c/bin/keyd` | HMAC {'hash': 'MD5'} | file |
| T5-C-06 | `corpus/tier5/c/bin/keyd` | AES {'key_size': 256, 'mode': 'GCM'} | file |
| T5-C-07 | `corpus/tier5/c/bin/keyd` | EC {'curve': 'P-256'} | file |
| T5-C-08 | `corpus/tier5/c/bin/fwcheck` | SHA-512  | file |
| T5-C-09 | `corpus/tier5/c/bin/fwcheck` | AES {'key_size': 128, 'mode': 'ECB'} | file |
| T5-C-10 | `corpus/tier5/c/bin/fwcheck` | DH {'key_size': 2048} | file |
| T5-C-11 | `corpus/tier5/c/bin/fwcheck` | X25519  | file |
| PQ-PY-01 | `corpus/pqc/python/pq_kem.py` | ML-KEM {'param_set': '768'} | 4 |
| PQ-PY-02 | `corpus/pqc/python/pq_signature.py` | ML-DSA {'param_set': '65'} | 4 |
| PQ-PY-04 | `corpus/pqc/python/pq_hybrid_kem.py` | ML-KEM {'param_set': '768'} | 14 |
| PQ-PY-05 | `corpus/pqc/python/pq_level_constant.py` | ML-KEM {'param_set': '1024'} | 8 |
| PQ-PY-07 | `corpus/pqc/python/firmware_verify_lms.py` | LMS  | 12 |
| PQ-JV-01 | `corpus/pqc/java/PqKem.java` | ML-KEM {'param_set': '1024'} | 10 |
| PQ-JV-02 | `corpus/pqc/java/PqSignature.java` | ML-DSA {'param_set': '87'} | 8 |
| PQ-JV-03 | `corpus/pqc/java/PqParamSpec.java` | ML-DSA {'param_set': '44'} | 10 |
| PQ-JV-05 | `corpus/pqc/java/FirmwareSignLms.java` | LMS  | 19 |
| PQ-JV-06 | `corpus/pqc/java/UpdateSignXmss.java` | XMSS  | 16 |
| PQ-AS-01 | `corpus/pqc/assets/certs/release_root_mldsa.pem` | ML-DSA {'param_set': '65'} | file |
| PQ-AS-02 | `corpus/pqc/assets/certs/firmware_signing.pem` | ML-DSA {'param_set': '87'} | file |
| PQ-AS-03 | `corpus/pqc/assets/certs/migrated_leaf.pem` | ML-DSA {'param_set': '65'} | file |
| PQ-AS-04 | `corpus/pqc/assets/certs/migrated_leaf.pem` | RSA  | file |
| PQ-AS-05 | `corpus/pqc/assets/certs/migrated_leaf.pem` | SHA-256  | file |
| PQ-AS-06 | `corpus/pqc/assets/keys/kem_recipient_pub.pem` | ML-KEM {'param_set': '768'} | file |
| PQ-AS-07 | `corpus/pqc/assets/keys/attestation_signer.pem` | ML-DSA {'param_set': '44'} | file |
| PQ-AS-08 | `corpus/pqc/assets/tls/nginx_pq.conf` | TLS-1.3  | 13 |
| PQ-AS-09 | `corpus/pqc/assets/tls/nginx_pq.conf` | X25519MLKEM768  | 14 |
| PQ-AS-10 | `corpus/pqc/assets/tls/nginx_pq.conf` | X25519  | 14 |
| PQ-AS-11 | `corpus/pqc/assets/tls/openssl_pq.cnf` | SecP384r1MLKEM1024  | 13 |
| PQ-AS-12 | `corpus/pqc/assets/tls/openssl_pq.cnf` | X25519MLKEM768  | 13 |
| PQ-AS-13 | `corpus/pqc/assets/tls/openssl_pq.cnf` | EC {'curve': 'P-384'} | 13 |
| PQ-AS-14 | `corpus/pqc/assets/tls/openssl_pq.cnf` | TLS-1.3  | 12 |
| PQ-AS-15 | `corpus/pqc/assets/ssh/sshd_config_pq` | X25519MLKEM768  | 6 |
| PQ-AS-16 | `corpus/pqc/assets/ssh/sshd_config_pq` | sntrup761x25519  | 6 |
| PQ-AS-18 | `corpus/pqc/assets/ssh/sshd_config_pq` | Ed25519  | 5 |
| PQ-AS-19 | `corpus/pqc/assets/ssh/sshd_config_pq` | ChaCha20-Poly1305  | 7 |
| PQ-AS-20 | `corpus/pqc/assets/tls/nginx_pq_washing.conf` | TLS-1.3  | 15 |
| PQ-AS-21 | `corpus/pqc/assets/tls/nginx_pq_washing.conf` | X25519  | 16 |
| PQ-AS-22 | `corpus/pqc/assets/tls/nginx_pq_washing.conf` | EC {'curve': 'P-256'} | 16 |
| PQ-AS-23 | `corpus/pqc/assets/keys/bootloader_lms_pub.pem` | LMS  | file |
| PQ-AS-24 | `corpus/pqc/assets/keys/update_xmss_pub.pem` | XMSS  | file |
| PQ-AS-25 | `corpus/pqc/assets/firmware/signing-policy.yaml` | LMS  | 7 |
| PQ-AS-26 | `corpus/pqc/assets/firmware/signing-policy.yaml` | XMSS  | 13 |
| PQ-AS-27 | `corpus/pqc/assets/firmware/signing-policy.yaml` | EC {'curve': 'P-384'} | 18 |
| T1-GO-01 | `corpus/tier1/go/hashes/main.go` | MD5  | 14 |
| T1-GO-02 | `corpus/tier1/go/hashes/main.go` | SHA-1  | 15 |
| T1-GO-03 | `corpus/tier1/go/hashes/main.go` | SHA-256  | 16 |
| T1-GO-04 | `corpus/tier1/go/hashes/main.go` | SHA3-256  | 17 |
| T1-GO-05 | `corpus/tier1/go/aes_gcm/main.go` | AES {'key_size': 256, 'mode': 'GCM'} | 12 |
| T1-GO-06 | `corpus/tier1/go/aes_cbc/main.go` | AES {'key_size': 128, 'mode': 'CBC'} | 12 |
| T1-GO-07 | `corpus/tier1/go/des/main.go` | 3DES {'mode': 'CBC'} | 13 |
| T1-GO-08 | `corpus/tier1/go/des/main.go` | DES {'mode': 'CBC'} | 21 |
| T1-GO-09 | `corpus/tier1/go/rc4/main.go` | RC4  | 10 |
| T1-GO-15 | `corpus/tier1/go/mac_kdf/main.go` | HMAC {'hash': 'SHA-256'} | 13 |
| T1-GO-16 | `corpus/tier1/go/mac_kdf/main.go` | PBKDF2 {'hash': 'SHA-512'} | 17 |
| T1-GO-17 | `corpus/tier1/go/tls_config/main.go` | TLS-1.0  | 11 |
| T1-GO-18 | `corpus/tier1/go/tls_config/main.go` | TLS_RSA_WITH_3DES_EDE_CBC_SHA  | 13 |
| T1-GO-19 | `corpus/tier1/go/tls_config/main.go` | TLS_RSA_WITH_AES_128_CBC_SHA  | 14 |
| T1-GO-20 | `corpus/tier1/go/tls_config/main.go` | TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256  | 15 |
| T2-GO-01 | `corpus/tier2/go/hash_enum/main.go` | SHA-1  | 10 |
| T2-GO-04 | `corpus/tier2/go/hmac_func_value/main.go` | HMAC {'hash': 'MD5'} | 11 |
| T2-GO-05 | `corpus/tier2/go/key_len/main.go` | AES {'key_size': 192, 'mode': 'CTR'} | 11 |
| T2-GO-06 | `corpus/tier2/go/block_factory/main.go` | 3DES {'mode': 'CBC'} | 10 |
| PQ-GO-01 | `corpus/pqc/go/mlkem/main.go` | ML-KEM {'param_set': '1024'} | 11 |
| PQ-GO-02 | `corpus/pqc/go/tls_hybrid/main.go` | TLS-1.3  | 11 |
| PQ-GO-03 | `corpus/pqc/go/tls_hybrid/main.go` | X25519MLKEM768  | 12 |
| PQ-GO-04 | `corpus/pqc/go/tls_hybrid/main.go` | X25519  | 12 |
| T1-JS-01 | `corpus/tier1/javascript/t1_hashes.js` | MD5  | 5 |
| T1-JS-02 | `corpus/tier1/javascript/t1_hashes.js` | SHA-1  | 6 |
| T1-JS-03 | `corpus/tier1/javascript/t1_hashes.js` | SHA-256  | 7 |
| T1-JS-04 | `corpus/tier1/javascript/t1_hashes.js` | SHA3-256  | 8 |
| T1-JS-05 | `corpus/tier1/javascript/t1_aes_cbc.js` | AES {'key_size': 128, 'mode': 'CBC'} | 6 |
| T1-JS-06 | `corpus/tier1/javascript/t1_aes_gcm.js` | AES {'key_size': 256, 'mode': 'GCM'} | 6 |
| T1-JS-07 | `corpus/tier1/javascript/t1_triple_des.js` | 3DES {'mode': 'CBC'} | 4 |
| T1-JS-08 | `corpus/tier1/javascript/t1_chacha.js` | ChaCha20-Poly1305  | 4 |
| T1-JS-14 | `corpus/tier1/javascript/t1_mac_kdf.js` | HMAC {'hash': 'SHA-256'} | 4 |
| T1-JS-15 | `corpus/tier1/javascript/t1_mac_kdf.js` | PBKDF2 {'hash': 'SHA-512'} | 5 |
| T1-JS-17 | `corpus/tier1/javascript/t1_webcrypto.mjs` | SHA-1  | 9 |
| T2-TS-01 | `corpus/tier2/typescript/t2_config_object.ts` | 3DES {'mode': 'CBC'} | 5 |
| T2-TS-02 | `corpus/tier2/typescript/t2_default_param.ts` | SHA-1  | 4 |
| T2-TS-05 | `corpus/tier2/typescript/t2_wrapper.ts` | AES {'key_size': 128, 'mode': 'ECB'} | 9 |
| T2-TS-06 | `corpus/tier2/typescript/t2_template.ts` | AES {'key_size': 256, 'mode': 'GCM'} | 4 |
| T2-TS-07 | `corpus/tier2/typescript/t2_hmac_const.ts` | HMAC {'hash': 'MD5'} | 4 |
| T1-C-01 | `corpus/tier1/c/t1_digests.c` | MD5  | 15 |
| T1-C-02 | `corpus/tier1/c/t1_digests.c` | SHA-1  | 16 |
| T1-C-03 | `corpus/tier1/c/t1_digests.c` | SHA-256  | 17 |
| T1-C-04 | `corpus/tier1/c/t1_digests.c` | SHA3-256  | 18 |
| T1-C-05 | `corpus/tier1/c/t1_aes_ecb.c` | AES {'key_size': 128, 'mode': 'ECB'} | 12 |
| T1-C-06 | `corpus/tier1/c/t1_aes_gcm.c` | AES {'key_size': 256, 'mode': 'GCM'} | 12 |
| T1-C-07 | `corpus/tier1/c/t1_triple_des.c` | 3DES {'mode': 'CBC'} | 12 |
| T1-C-08 | `corpus/tier1/c/t1_chacha.c` | ChaCha20-Poly1305  | 12 |
| T1-C-10 | `corpus/tier1/c/t1_rsa_evp.c` | RSA {'key_size': 3072} | 8 |
| T1-C-11 | `corpus/tier1/c/t1_ec.c` | EC {'curve': 'P-256'} | 10 |
| T1-C-12 | `corpus/tier1/c/t1_modern_curves.c` | Ed25519  | 6 |
| T1-C-13 | `corpus/tier1/c/t1_modern_curves.c` | X25519  | 9 |
| T1-C-14 | `corpus/tier1/c/t1_dh.c` | DH {'key_size': 2048} | 7 |
| T1-C-15 | `corpus/tier1/c/t1_mac_kdf.c` | HMAC {'hash': 'SHA-256'} | 11 |
| T1-C-16 | `corpus/tier1/c/t1_mac_kdf.c` | PBKDF2 {'hash': 'SHA-1'} | 15 |
| T1-C-17 | `corpus/tier1/c/t1_tls_ctx.c` | TLS-1.0  | 7 |
| T1-C-18 | `corpus/tier1/c/t1_tls_ctx.c` | TLS_RSA_WITH_3DES_EDE_CBC_SHA  | 8 |
| T1-C-19 | `corpus/tier1/c/t1_tls_ctx.c` | TLS_RSA_WITH_AES_128_CBC_SHA  | 8 |
| T1-C-20 | `corpus/tier1/c/t1_tls_ctx.c` | TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256  | 8 |
| T1-CS-01 | `corpus/tier1/csharp/Hashes/Program.cs` | MD5  | 9 |
| T1-CS-02 | `corpus/tier1/csharp/Hashes/Program.cs` | SHA-1  | 10 |
| T1-CS-03 | `corpus/tier1/csharp/Hashes/Program.cs` | SHA-256  | 11 |
| T1-CS-04 | `corpus/tier1/csharp/Hashes/Program.cs` | SHA3-256  | 12 |
| T1-CS-08 | `corpus/tier1/csharp/AesCbc/Program.cs` | AES {'key_size': 128, 'mode': 'CBC'} | 8 |
| T1-CS-09 | `corpus/tier1/csharp/AesGcmSeal/Program.cs` | AES {'key_size': 256, 'mode': 'GCM'} | 13 |
| T1-CS-10 | `corpus/tier1/csharp/TripleDesLegacy/Program.cs` | 3DES {'mode': 'CBC'} | 8 |
| T1-CS-11 | `corpus/tier1/csharp/MacKdf/Program.cs` | HMAC {'hash': 'SHA-256'} | 8 |
| T1-CS-12 | `corpus/tier1/csharp/MacKdf/Program.cs` | PBKDF2 {'hash': 'SHA-512'} | 10 |
| T2-C-01 | `corpus/tier2/c/t2_fetch_by_name.c` | AES {'key_size': 192, 'mode': 'CBC'} | 6 |
| T2-C-02 | `corpus/tier2/c/t2_digest_table.c` | SHA-1  | 12 |
| T2-C-04 | `corpus/tier2/c/t2_curve_index.c` | EC {'curve': 'P-521'} | 7 |
| T2-C-05 | `corpus/tier2/c/t2_func_ptr.c` | HMAC {'hash': 'MD5'} | 8 |
| T2-C-06 | `corpus/tier2/c/t2_cipher_struct.c` | 3DES {'mode': 'ECB'} | 10 |
| T2-CS-01 | `corpus/tier2/csharp/ConfigCipher/Program.cs` | AES {'key_size': 192, 'mode': 'CBC'} | 11 |
| T2-CS-02 | `corpus/tier2/csharp/HashByName/Program.cs` | SHA-1  | 10 |
| T2-CS-03 | `corpus/tier2/csharp/DispatchTable/Program.cs` | MD5  | 9 |
| T2-CS-04 | `corpus/tier2/csharp/DispatchTable/Program.cs` | SHA-512  | 10 |
| MX-PY-1a | `corpus/mixed/python/metric_service.py` | PBKDF2 {'hash': 'SHA-256'} | 83 |
| MX-PY-1b | `corpus/mixed/python/metric_service.py` | PBKDF2 {'hash': 'SHA-512'} | 39 |
| MX-PY-1c | `corpus/mixed/python/metric_service.py` | HMAC {'hash': 'SHA-512'} | 15 |
| MX-PY-1d | `corpus/mixed/python/metric_service.py` | AES {'key_size': 192, 'mode': 'CTR'} | 17 |
| MX-PY-2b | `corpus/mixed/python/invoice_service.py` | ML-DSA {'param_set': '65'} | 277 |
| MX-PY-2d | `corpus/mixed/python/invoice_service.py` | ChaCha20-Poly1305  | 262 |
| MX-PY-3a | `corpus/mixed/python/order_jobs.py` | SHA-1  | 319 |
| MX-PY-3b | `corpus/mixed/python/order_jobs.py` | HMAC {'hash': 'SHA-512'} | 12 |
| MX-JV-1b | `corpus/mixed/java/VoucherProfileModule.java` | SHA-1  | 7 |
| MX-JV-1d | `corpus/mixed/java/VoucherProfileModule.java` | AES {'key_size': 192, 'mode': 'ECB'} | 205 |
| MX-JV-2a | `corpus/mixed/java/BookingOptionsModule.java` | SHA-256  | 9 |
| MX-JV-2c | `corpus/mixed/java/BookingOptionsModule.java` | PBKDF2 {'hash': 'SHA-512'} | 10 |
| MX-JV-2d | `corpus/mixed/java/BookingOptionsModule.java` | PBKDF2 {'hash': 'SHA-256'} | 72 |
| MX-JV-3a | `corpus/mixed/java/OrderDefaultsModule.java` | HMAC {'hash': 'SHA-256'} | 9 |
| MX-JV-3b | `corpus/mixed/java/OrderDefaultsModule.java` | 3DES {'mode': 'ECB'} | 315 |
| MX-JV-3c | `corpus/mixed/java/OrderDefaultsModule.java` | ChaCha20-Poly1305  | 10 |
| MX-JV-3d | `corpus/mixed/java/OrderDefaultsModule.java` | SHA-512  | 269 |
| MX-JV-3e | `corpus/mixed/java/OrderDefaultsModule.java` | 3DES {'mode': 'CBC'} | 148 |
| MX-GO-1a | `corpus/mixed/go/payload_worker/main.go` | PBKDF2 {'hash': 'SHA-512'} | 19 |
| MX-GO-1b | `corpus/mixed/go/payload_worker/main.go` | ML-KEM {'param_set': '768'} | 20 |
| MX-GO-2a | `corpus/mixed/go/report_gateway/main.go` | PBKDF2 {'hash': 'SHA-256'} | 26 |
| MX-GO-2b | `corpus/mixed/go/report_gateway/main.go` | DES {'mode': 'CBC'} | 125 |
| MX-GO-2c | `corpus/mixed/go/report_gateway/main.go` | PBKDF2 {'hash': 'SHA-1'} | 228 |
| MX-GO-2d | `corpus/mixed/go/report_gateway/main.go` | 3DES {'mode': 'CBC'} | 171 |
| MX-GO-3b | `corpus/mixed/go/invoice_gateway/main.go` | RC4  | 198 |
| MX-GO-3c | `corpus/mixed/go/invoice_gateway/main.go` | HMAC {'hash': 'SHA-1'} | 277 |
| MX-JS-1a | `corpus/mixed/javascript/partner_routes.js` | AES {'key_size': 128, 'mode': 'CBC'} | 5 |
| MX-JS-1b | `corpus/mixed/javascript/partner_routes.js` | HMAC {'hash': 'SHA-512'} | 83 |
| MX-JS-1c | `corpus/mixed/javascript/partner_routes.js` | AES {'key_size': 256, 'mode': 'CTR'} | 8 |
| MX-JS-2a | `corpus/mixed/javascript/device_session.js` | SHA3-256  | 94 |
| MX-JS-2b | `corpus/mixed/javascript/device_session.js` | PBKDF2 {'hash': 'SHA-512'} | 409 |
| MX-JS-2e | `corpus/mixed/javascript/device_session.js` | AES {'key_size': 256, 'mode': 'CTR'} | 68 |
| MX-TS-1b | `corpus/mixed/typescript/voucher_service.ts` | HMAC {'hash': 'SHA-512'} | 5 |
| MX-TS-1c | `corpus/mixed/typescript/voucher_service.ts` | AES {'key_size': 128, 'mode': 'ECB'} | 36 |
| MX-C-1a | `corpus/mixed/c/device_daemon.c` | SHA-1  | 10 |
| MX-C-1b | `corpus/mixed/c/device_daemon.c` | EC {'curve': 'P-521'} | 11 |
| MX-C-1c | `corpus/mixed/c/device_daemon.c` | HMAC {'hash': 'MD5'} | 12 |
| MX-C-1d | `corpus/mixed/c/device_daemon.c` | X25519  | 58 |
| MX-C-1e | `corpus/mixed/c/device_daemon.c` | HMAC {'hash': 'SHA-512'} | 154 |
| MX-C-2a | `corpus/mixed/c/policy_agent.c` | EC {'curve': 'P-384'} | 9 |
| MX-C-2b | `corpus/mixed/c/policy_agent.c` | AES {'key_size': 192, 'mode': 'CBC'} | 10 |
| MX-C-2c | `corpus/mixed/c/policy_agent.c` | 3DES {'mode': 'ECB'} | 66 |
| MX-C-2d | `corpus/mixed/c/policy_agent.c` | 3DES {'mode': 'CBC'} | 11 |
| MX-C-3a | `corpus/mixed/c/audit_daemon.c` | AES {'key_size': 192, 'mode': 'CBC'} | 8 |
| MX-C-3b | `corpus/mixed/c/audit_daemon.c` | 3DES {'mode': 'CBC'} | 300 |
| MX-C-3c | `corpus/mixed/c/audit_daemon.c` | AES {'key_size': 128, 'mode': 'ECB'} | 9 |
| MX-C-3d | `corpus/mixed/c/audit_daemon.c` | DH {'key_size': 3072} | 10 |
| SYS-GO-02 | `corpus/system/payments-platform/services/api-gateway/main.go` | HMAC {'hash': 'SHA-1'} | 20 |
| SYS-GO-03 | `corpus/system/payments-platform/services/api-gateway/main.go` | SHA-256  | 13 |
| SYS-PY-01 | `corpus/system/payments-platform/services/settlement-worker/worker.py` | AES {'key_size': 128, 'mode': 'CBC'} | 19 |
| SYS-PY-02 | `corpus/system/payments-platform/services/settlement-worker/worker.py` | HMAC {'hash': 'SHA-1'} | 20 |
| SYS-PY-03 | `corpus/system/payments-platform/services/settlement-worker/partner_ca.py` | RSA {'key_size': 1024} | file |
| SYS-PY-04 | `corpus/system/payments-platform/services/settlement-worker/partner_ca.py` | SHA-1  | file |
| SYS-JV-02 | `corpus/system/payments-platform/services/ledger-service/src/main/java/com/acme/ledger/LedgerService.java` | SHA-1  | 10 |
| SYS-AR-01 | `corpus/system/payments-platform/services/ledger-service/build/libs/ledger-service.jar` | EC  | file |
| SYS-AR-02 | `corpus/system/payments-platform/services/ledger-service/build/libs/ledger-service.jar` | SHA-1  | file |
| SYS-AR-03 | `corpus/system/payments-platform/services/api-gateway/bin/api-gateway` | RSA  | file |
| SYS-AR-04 | `corpus/system/payments-platform/services/api-gateway/bin/api-gateway` | HMAC  | file |
| SYS-AR-05 | `corpus/system/payments-platform/services/api-gateway/bin/api-gateway` | SHA-1  | file |
| SYS-AR-06 | `corpus/system/payments-platform/services/api-gateway/bin/api-gateway` | SHA-256  | file |
| SYS-AS-01 | `corpus/system/payments-platform/edge/nginx/gateway.conf` | TLS-1.2  | 8 |
| SYS-AS-02 | `corpus/system/payments-platform/edge/nginx/gateway.conf` | TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384  | 9 |
| SYS-AS-03 | `corpus/system/payments-platform/edge/nginx/gateway.conf` | TLS_RSA_WITH_AES_128_CBC_SHA  | 9 |
| SYS-AS-04 | `corpus/system/payments-platform/edge/nginx/tls/gateway.crt` | RSA {'key_size': 2048} | file |
| SYS-AS-05 | `corpus/system/payments-platform/edge/nginx/tls/gateway.crt` | SHA-256  | file |
| SYS-AS-07 | `corpus/system/payments-platform/deploy/k8s/gateway-ingress-tls.yaml` | EC {'curve': 'P-384'} | file |
| SYS-AS-08 | `corpus/system/payments-platform/deploy/k8s/gateway-ingress-tls.yaml` | SHA-384  | file |
| SYS-AS-11 | `corpus/system/payments-platform/infra/terraform/kms.tf` | AES {'key_size': 256, 'mode': 'GCM'} | 15 |
| DC-PY-01 | `corpus/deadcode/python/dead_export.py` | MD5  | 10 |
| DC-JV-01 | `corpus/deadcode/java/DeadLegacy.java` | DES {'mode': 'CBC'} | 9 |
| DC-JV-02 | `corpus/deadcode/java/DeadLegacy.java` | SHA-1  | 14 |
| DC-GO-01 | `corpus/deadcode/go/legacy/main.go` | MD5  | 13 |
| DC-GO-02 | `corpus/deadcode/go/legacy/main.go` | RC4  | 18 |
| DC-JS-01 | `corpus/deadcode/javascript/dead_paths.js` | MD5  | 5 |
| DC-JS-02 | `corpus/deadcode/javascript/dead_paths.js` | 3DES {'mode': 'CBC'} | 10 |
| DC-C-01 | `corpus/deadcode/c/dead_branches.c` | MD5  | 6 |
| DC-C-02 | `corpus/deadcode/c/dead_branches.c` | 3DES {'mode': 'CBC'} | 11 |

## Detected with wrong or missing parameters

| ID | Family | Expected params | Reported params |
|---|---|---|---|
| T1-PY-05 | RSA | `{"key_size": 2048}` | `{}` |
| T1-PY-06 | EC | `{"curve": "P-256"}` | `{}; {}` |
| T1-PY-07 | DSA | `{"key_size": 2048}` | `{}` |
| T1-PY-14 | DH | `{"key_size": 2048}` | `{}` |
| T1-JV-05 | RSA | `{"key_size": 3072}` | `{}; {}` |
| T1-JV-06 | EC | `{"curve": "P-256"}` | `{}; {}` |
| T1-JV-07 | DSA | `{"key_size": 2048}` | `{}; {}` |
| T1-JV-14 | DH | `{"key_size": 2048}` | `{}; {}; {}` |
| T2-PY-02 | RSA | `{"key_size": 1024}` | `{}` |
| T2-PY-09 | EC | `{"curve": "P-384"}` | `{}; {}` |
| T2-JV-08 | EC | `{"curve": "P-384"}` | `{}` |
| T3-PY-01 | RSA | `{"key_size": 1024}` | `{}` |
| T3-PY-04 | RSA | `{"key_size": 1024}` | `{}` |
| T3-PY-05 | RSA | `{"key_size": 3072}` | `{}` |
| T3-JV-01 | RSA | `{"key_size": 1024}` | `{}` |
| T4-AS-15 | EC | `{"curve": "secp256k1"}` | `{}` |
| T4-AS-18 | RSA | `{"key_size": 2048}` | `{}` |
| T4-AS-19 | EC | `{"curve": "P-256"}` | `{}` |
| T4-AS-27 | DH | `{"key_size": 2048}` | `{}` |
| T4-AS-32 | RSA | `{"key_size": 2048}` | `{}` |
| T4-AS-62 | DH | `{"key_size": 2048}` | `{}` |
| T4-AS-67 | DH | `{"key_size": 1024}` | `{}` |
| PQ-PY-06 | EC | `{"curve": "P-256"}` | `{}; {}` |
| PQ-JV-04 | EC | `{"curve": "P-384"}` | `{}; {}` |
| T1-GO-10 | RSA | `{"key_size": 2048}` | `{}; {}` |
| T1-GO-11 | EC | `{"curve": "P-256"}` | `{}; {}` |
| T1-GO-14 | DSA | `{"key_size": 2048}` | `{}; {}` |
| T2-GO-02 | RSA | `{"key_size": 1024}` | `{}` |
| T2-GO-03 | EC | `{"curve": "P-384"}` | `{}` |
| T1-JS-09 | RSA | `{"key_size": 2048}` | `{}` |
| T1-JS-10 | EC | `{"curve": "P-256"}` | `{}` |
| T1-JS-13 | DH | `{"key_size": 2048}` | `{}; {}` |
| T1-JS-16 | RSA | `{"key_size": 3072}` | `{}` |
| T2-TS-03 | RSA | `{"key_size": 1024}` | `{}` |
| T2-TS-04 | EC | `{"curve": "P-384"}` | `{}` |
| T1-C-09 | RSA | `{"key_size": 1024}` | `{}` |
| T1-CS-05 | RSA | `{"key_size": 2048}` | `{}` |
| T1-CS-06 | EC | `{"curve": "P-256"}` | `{}` |
| T1-CS-07 | EC | `{"curve": "P-384"}` | `{}; {}` |
| T1-CS-13 | DSA | `{"key_size": 2048}` | `{}` |
| T2-C-03 | RSA | `{"key_size": 1024}` | `{}` |
| T2-CS-05 | RSA | `{"key_size": 1024}` | `{}` |
| T2-CS-06 | EC | `{"curve": "P-521"}` | `{}` |
| MX-PY-2a | DH | `{"key_size": 512}` | `{}` |
| MX-PY-2c | DH | `{"key_size": 1024}` | `{}` |
| MX-PY-3c | EC | `{"curve": "P-256"}` | `{}; {}` |
| MX-PY-3d | EC | `{"curve": "P-521"}` | `{}` |
| MX-JV-1a | DH | `{"key_size": 3072}` | `{}` |
| MX-JV-1c | DH | `{"key_size": 2048}` | `{}` |
| MX-GO-1c | RSA | `{"key_size": 1024}` | `{}` |
| MX-GO-1d | RSA | `{"key_size": 2048}` | `{}` |
| MX-GO-3a | RSA | `{"key_size": 2048}` | `{}` |
| MX-JS-2c | EC | `{"curve": "P-521"}` | `{}` |
| MX-JS-2d | EC | `{"curve": "P-384"}` | `{}` |
| MX-TS-1a | EC | `{"curve": "P-256"}` | `{}` |
| MX-TS-1d | RSA | `{"key_size": 2048}` | `{}` |
| SYS-GO-01 | RSA | `{"key_size": 2048}` | `{}; {}` |
| SYS-JV-01 | EC | `{"curve": "P-256"}` | `{}` |
| SYS-AS-06 | RSA | `{"key_size": 2048}` | `{}` |
| SYS-AS-09 | EC | `{"curve": "P-256"}` | `{}` |
| SYS-AS-10 | RSA | `{"key_size": 2048}` | `{}` |
| DC-PY-02 | RSA | `{"key_size": 1024}` | `{}` |

## False positives

| File | Reported family | Lines | Negative control? |
|---|---|---|---|
| `corpus/deps/go-service/go.mod` | EC | 6 | no |
| `corpus/deps/go-service/go.mod` | RSA | 7, 8 | no |
| `corpus/deps/java-gateway/pom.xml` | RSA | 17, 27, 32 | no |
| `corpus/deps/java-pq/build.gradle` | RSA | 13 | no |
| `corpus/deps/node-api/package-lock.json` | EC | 55, 128 | no |
| `corpus/deps/node-api/package-lock.json` | RSA | 15, 16, 105, 138 | no |
| `corpus/deps/node-api/package.json` | RSA | 11, 12 | no |
| `corpus/deps/python-billing/requirements.txt` | RSA | 1, 3, 4, 7 | no |
| `corpus/deps/python-signer/pyproject.toml` | RSA | 6 | no |
| `corpus/negatives/java/NLookalikes.java` | EC | 12 | yes |
| `corpus/pqc/java/PqParamSpec.java` | DSA | 9 | no |
| `corpus/pqc/java/PqSignature.java` | DSA | 8, 11 | no |
| `corpus/system/payments-platform/services/ledger-service/build.gradle` | RSA | 9 | no |
| `corpus/system/payments-platform/services/settlement-worker/requirements.txt` | RSA | 8 | no |
| `corpus/tier1/javascript/t1_modern_curves.js` | EC | 9 | no |

## Unrecognized names (not scored, review manually)

- `corpus/negatives/java/NStringsAndComments.java` line 18: unknown
- `corpus/calibration/tier1/c/cal_ec_012.c` line 15: unknown
- `corpus/calibration/tier1/c/cal_ec_013.c` line 19: unknown
- `corpus/calibration/tier1/c/cal_ec_014.c` line 11: unknown
- `corpus/calibration/tier1/c/cal_ed25519_015.c` line 6: unknown
- `corpus/calibration/tier1/c/cal_ed25519_016.c` line 14: unknown
- `corpus/calibration/tier1/c/cal_ed25519_017.c` line 6: unknown
- `corpus/calibration/tier1/c/cal_rsa_027.c` line 11: unknown
- `corpus/calibration/tier1/c/cal_rsa_028.c` line 15: unknown
- `corpus/calibration/tier1/c/cal_x25519_038.c` line 17: unknown
- `corpus/calibration/tier1/c/cal_x25519_039.c` line 17: unknown
- `corpus/calibration/tier1/c/cal_x25519_040.c` line 9: unknown
- `corpus/mixed/c/device_daemon.c` line 354: unknown
- `corpus/mixed/c/device_daemon.c` line 60: unknown
- `corpus/pqc/assets/tls/nginx_pq.conf` line 10: unknown
- `corpus/pqc/assets/tls/nginx_pq.conf` line 11: unknown
- `corpus/pqc/assets/tls/nginx_pq_washing.conf` line 12: unknown
- `corpus/pqc/assets/tls/nginx_pq_washing.conf` line 13: unknown
- `corpus/system/payments-platform/edge/nginx/gateway.conf` line 6: unknown
- `corpus/system/payments-platform/edge/nginx/gateway.conf` line 7: unknown
- `corpus/tier1/c/t1_ec.c` line 11: unknown
- `corpus/tier1/c/t1_modern_curves.c` line 11: unknown
- `corpus/tier1/c/t1_modern_curves.c` line 6: unknown
- `corpus/tier1/c/t1_rsa_evp.c` line 11: unknown
- `corpus/tier4/assets/tls/haproxy.cfg` line 17: unknown
- `corpus/tier4/assets/tls/nginx.conf` line 13: unknown
- `corpus/tier4/assets/tls/nginx.conf` line 14: unknown
- `corpus/calibration/tier1/javascript/cal_ec_012.js` line 10: unknown
- `corpus/calibration/tier1/javascript/cal_ec_013.js` line 10: unknown
- `corpus/calibration/tier1/javascript/cal_ec_014.js` line 10: unknown
- `corpus/calibration/tier1/javascript/cal_rsa_027.js` line 10: unknown
- `corpus/calibration/tier1/javascript/cal_rsa_028.js` line 10: unknown
- `corpus/calibration/tier2/typescript/cal_ec_006.ts` line 8: unknown
- `corpus/calibration/tier2/typescript/cal_ec_007.ts` line 12: unknown
- `corpus/calibration/tier2/typescript/cal_ec_008.ts` line 10: unknown
- `corpus/calibration/tier2/typescript/cal_rsa_012.ts` line 8: unknown
- `corpus/calibration/tier2/typescript/cal_rsa_013.ts` line 10: unknown
- `corpus/calibration/tier2/typescript/cal_rsa_014.ts` line 8: unknown
- `corpus/mixed/javascript/device_session.js` line 205: unknown
- `corpus/mixed/javascript/device_session.js` line 339: unknown
- `corpus/mixed/typescript/voucher_service.ts` line 289: unknown
- `corpus/mixed/typescript/voucher_service.ts` line 324: unknown
- `corpus/pqc/assets/firmware/signing-policy.yaml` line 13: unknown
- `corpus/pqc/assets/firmware/signing-policy.yaml` line 7: unknown
- `corpus/pqc/python/firmware_verify_lms.py` line 12: unknown
- `corpus/pqc/python/firmware_verify_lms.py` line 69: unknown
- `corpus/pqc/python/firmware_verify_lms.py` line 82: unknown
- `corpus/pqc/python/firmware_verify_lms.py` line 86: unknown
- `corpus/pqc/python/firmware_verify_lms.py` line 92: unknown
- `corpus/tier1/c/t1_ec.c` line 16: unknown
- `corpus/tier1/c/t1_ec.c` line 17: unknown
- `corpus/tier1/javascript/t1_ec.js` line 5: unknown
- `corpus/tier1/javascript/t1_modern_curves.js` line 5: unknown
- `corpus/tier1/javascript/t1_rsa.js` line 5: unknown
- `corpus/tier2/typescript/t2_env_default.ts` line 7: unknown
- `corpus/tier1/go/tls_config/main.go` line 11: unknown
- `corpus/pqc/assets/keys/attestation_signer.pem` line 1: unknown
- `corpus/tier4/assets/keys/backup_signing_encrypted.pem` line 1: unknown
- `corpus/tier4/assets/keys/billing_service.pem` line 1: unknown
- `corpus/tier4/assets/keystores/orders_keystore.p12` line 1: unknown
- `corpus/tier4/assets/keystores/partner_truststore.jks` line 1: unknown
- `corpus/tier4/assets/ssh/deploy_id_ed25519` line 1: unknown
- `corpus/pqc/assets/keys/bootloader_lms_pub.pem` line 1: unknown
- `corpus/pqc/assets/keys/kem_recipient_pub.pem` line 1: unknown
- `corpus/pqc/assets/keys/update_xmss_pub.pem` line 1: unknown

## Crypto libraries (dependency manifests)

- Found in the right manifest: **0/28** (0.0%); found anywhere, including with no location: 0/28
- Direct dependencies: 0.0%; transitive (lockfile): 0.0%
- Versions correct, of found libraries the manifest pins (none reported counts as not correct): n/a
- PQC-capability verdicts (where the scanner gives one): none given
- False positives: 0

Missed, and the declared version has no ML-KEM/ML-DSA: cryptography 41.0.7 (python-billing); pycryptodome 3.19.0 (python-billing); PyJWT 2.8.0 (python-billing); org.bouncycastle:bcprov-jdk15on, bcpkix-jdk15on 1.70 (java-gateway); jsonwebtoken 9.0.2 (node-api); crypto-js 4.2.0 (node-api); @noble/curves 2.0.1 (node-api); jws 3.2.3 (node-api); jwa 1.4.2 (node-api); openssl 1.1.1w (c-agent); cryptography 42.0.5 (settlement-worker); org.bouncycastle:bcprov-jdk18on 1.77 (ledger-service)

Missed, with a support problem: org.bouncycastle:bcprov-jdk15on, bcpkix-jdk15on 1.70: superseded: last jdk15on release; the line continues as -jdk18on; crypto-js 4.2.0: unmaintained: development discontinued upstream; openssl 1.1.1w: end of life since 2023-09-11

| Manifest | Library | Declared | Scope | Found | Version |
|---|---|---|---|---|---|
| `python-billing/requirements.txt` | cryptography | 41.0.7 | direct | no | n/a |
| `python-billing/requirements.txt` | pycryptodome | 3.19.0 | direct | no | n/a |
| `python-billing/requirements.txt` | pyOpenSSL | 23.3.0 | direct | no | n/a |
| `python-billing/requirements.txt` | PyJWT | 2.8.0 | direct | no | n/a |
| `python-billing/requirements.txt` | paramiko | 3.4.0 | direct | no | n/a |
| `python-billing/requirements.txt` | bcrypt | 4.1.2 | direct | no | n/a |
| `python-signer/pyproject.toml` | cryptography | range | direct | no | n/a |
| `python-signer/pyproject.toml` | liboqs-python | 0.16.0 | direct | no | n/a |
| `java-gateway/pom.xml` | org.bouncycastle:bcprov-jdk15on, bcpkix-jdk15on | 1.70 | direct | no | n/a |
| `java-gateway/pom.xml` | com.nimbusds:nimbus-jose-jwt | 9.37.3 | direct | no | n/a |
| `java-gateway/pom.xml` | io.jsonwebtoken:jjwt-api | 0.12.5 | direct | no | n/a |
| `java-pq/build.gradle` | org.bouncycastle:bcprov-jdk18on, bctls-jdk18on | 1.80 | direct | no | n/a |
| `node-api/package.json` | jsonwebtoken | 9.0.2 | direct | no | n/a |
| `node-api/package.json` | crypto-js | 4.2.0 | direct | no | n/a |
| `node-api/package.json` | node-forge | 1.3.1 | direct | no | n/a |
| `node-api/package.json` | bcryptjs | 2.4.3 | direct | no | n/a |
| `node-api/package.json` | @noble/post-quantum | 0.5.4 | direct | no | n/a |
| `node-api/package-lock.json` | @noble/curves | 2.0.1 | transitive | no | n/a |
| `node-api/package-lock.json` | @noble/hashes | 2.0.1 | transitive | no | n/a |
| `node-api/package-lock.json` | jws | 3.2.3 | transitive | no | n/a |
| `node-api/package-lock.json` | jwa | 1.4.2 | transitive | no | n/a |
| `go-service/go.mod` | golang.org/x/crypto | 0.31.0 | direct | no | n/a |
| `go-service/go.mod` | github.com/cloudflare/circl | 1.6.1 | direct | no | n/a |
| `go-service/go.mod` | github.com/golang-jwt/jwt/v5 | 5.2.1 | direct | no | n/a |
| `c-agent/conanfile.txt` | openssl | 1.1.1w | direct | no | n/a |
| `c-agent/conanfile.txt` | libsodium | 1.0.18 | direct | no | n/a |
| `corpus/system/payments-platform/services/settlement-worker/requirements.txt` | cryptography | 42.0.5 | direct | no | n/a |
| `corpus/system/payments-platform/services/ledger-service/build.gradle` | org.bouncycastle:bcprov-jdk18on | 1.77 | direct | no | n/a |

## Per-finding detail

| ID | Family | Detected | At primary site | Params | Line | Quantum flag |
|---|---|---|---|---|---|---|
| T1-PY-01 | MD5 | NO | NO | n/a | n/a | n/a |
| T1-PY-02 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T1-PY-03 | SHA-256 | NO | NO | n/a | n/a | n/a |
| T1-PY-04 | SHA3-256 | NO | NO | n/a | n/a | n/a |
| T1-PY-05 | RSA | yes | yes | NO | yes | yes |
| T1-PY-06 | EC | yes | yes | NO | yes | yes |
| T1-PY-07 | DSA | yes | yes | NO | yes | yes |
| T1-PY-08 | AES | NO | NO | n/a | n/a | n/a |
| T1-PY-09 | AES | NO | NO | n/a | n/a | n/a |
| T1-PY-10 | 3DES | NO | NO | n/a | n/a | n/a |
| T1-PY-11 | ChaCha20-Poly1305 | NO | NO | n/a | n/a | n/a |
| T1-PY-12 | Ed25519 | yes | yes | yes | yes | yes |
| T1-PY-13 | X25519 | yes | yes | yes | yes | yes |
| T1-PY-14 | DH | yes | yes | NO | yes | yes |
| T1-PY-15 | HMAC | NO | NO | n/a | n/a | n/a |
| T1-PY-16 | PBKDF2 | NO | NO | n/a | n/a | n/a |
| T1-JV-01 | MD5 | NO | NO | n/a | n/a | n/a |
| T1-JV-02 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T1-JV-03 | SHA-256 | NO | NO | n/a | n/a | n/a |
| T1-JV-04 | SHA3-256 | NO | NO | n/a | n/a | n/a |
| T1-JV-05 | RSA | yes | yes | NO | yes | yes |
| T1-JV-06 | EC | yes | yes | NO | yes | yes |
| T1-JV-07 | DSA | yes | yes | NO | yes | yes |
| T1-JV-08 | AES | NO | NO | n/a | n/a | n/a |
| T1-JV-09 | AES | NO | NO | n/a | n/a | n/a |
| T1-JV-10 | DES | NO | NO | n/a | n/a | n/a |
| T1-JV-11 | 3DES | NO | NO | n/a | n/a | n/a |
| T1-JV-12 | Ed25519 | yes | yes | yes | yes | yes |
| T1-JV-13 | X25519 | yes | yes | yes | yes | yes |
| T1-JV-14 | DH | yes | yes | NO | yes | yes |
| T1-JV-15 | HMAC | NO | NO | n/a | n/a | n/a |
| T1-JV-16 | PBKDF2 | NO | NO | n/a | n/a | n/a |
| T2-PY-01 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T2-PY-02 | RSA | yes | yes | NO | yes | yes |
| T2-PY-03 | AES | NO | NO | n/a | n/a | n/a |
| T2-PY-04 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T2-PY-05 | AES | NO | NO | n/a | n/a | n/a |
| T2-PY-06 | MD5 | NO | NO | n/a | n/a | n/a |
| T2-PY-07 | SHA-256 | NO | NO | n/a | n/a | n/a |
| T2-PY-08 | HMAC | NO | NO | n/a | n/a | n/a |
| T2-PY-09 | EC | yes | yes | NO | yes | yes |
| T2-JV-01 | 3DES | NO | NO | n/a | n/a | n/a |
| T2-JV-02 | RSA | NO | NO | n/a | n/a | n/a |
| T2-JV-03 | MD5 | NO | NO | n/a | n/a | n/a |
| T2-JV-04 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T2-JV-05 | SHA-256 | NO | NO | n/a | n/a | n/a |
| T2-JV-06 | AES | NO | NO | n/a | n/a | n/a |
| T2-JV-07 | DSA | NO | NO | n/a | n/a | n/a |
| T2-JV-08 | EC | yes | yes | NO | yes | yes |
| T3-PY-01 | RSA | yes | yes | NO | yes | yes |
| T3-PY-02 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T3-PY-03 | AES | NO | NO | n/a | n/a | n/a |
| T3-PY-04 | RSA | yes | NO | NO | yes | yes |
| T3-PY-05 | RSA | yes | NO | NO | yes | yes |
| T3-PY-06 | AES | NO | NO | n/a | n/a | n/a |
| T3-PY-07 | ChaCha20-Poly1305 | NO | NO | n/a | n/a | n/a |
| T3-PY-08 | MD5 | NO | NO | n/a | n/a | n/a |
| T3-PY-09 | HMAC | NO | NO | n/a | n/a | n/a |
| T3-JV-01 | RSA | yes | yes | NO | yes | yes |
| T3-JV-02 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T3-JV-03 | AES | NO | NO | n/a | n/a | n/a |
| T3-JV-04 | AES | NO | NO | n/a | n/a | n/a |
| T3-JV-05 | 3DES | NO | NO | n/a | n/a | n/a |
| T3-JV-06 | MD5 | NO | NO | n/a | n/a | n/a |
| T3-JV-07 | HMAC | NO | NO | n/a | n/a | n/a |
| T4-AS-01 | RSA | NO | NO | n/a | n/a | n/a |
| T4-AS-02 | SHA-256 | NO | NO | n/a | n/a | n/a |
| T4-AS-03 | RSA | NO | NO | n/a | n/a | n/a |
| T4-AS-04 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T4-AS-05 | EC | NO | NO | n/a | n/a | n/a |
| T4-AS-06 | SHA-256 | NO | NO | n/a | n/a | n/a |
| T4-AS-07 | Ed25519 | NO | NO | n/a | n/a | n/a |
| T4-AS-08 | EC | NO | NO | n/a | n/a | n/a |
| T4-AS-09 | SHA-384 | NO | NO | n/a | n/a | n/a |
| T4-AS-10 | RSA | NO | NO | n/a | n/a | n/a |
| T4-AS-11 | SHA-256 | NO | NO | n/a | n/a | n/a |
| T4-AS-12 | RSA | NO | NO | n/a | n/a | n/a |
| T4-AS-13 | SHA-512 | NO | NO | n/a | n/a | n/a |
| T4-AS-14 | RSA | NO | NO | n/a | n/a | n/a |
| T4-AS-15 | EC | yes | yes | NO | n/a | n/a |
| T4-AS-16 | PBKDF2 | NO | NO | n/a | n/a | n/a |
| T4-AS-17 | AES | NO | NO | n/a | n/a | n/a |
| T4-AS-18 | RSA | yes | yes | NO | NO | yes |
| T4-AS-19 | EC | yes | yes | NO | yes | yes |
| T4-AS-20 | AES | NO | NO | n/a | n/a | n/a |
| T4-AS-21 | PBKDF2 | NO | NO | n/a | n/a | n/a |
| T4-AS-24 | RSA | NO | NO | n/a | n/a | n/a |
| T4-AS-25 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T4-AS-26 | RSA | NO | NO | n/a | n/a | n/a |
| T4-AS-27 | DH | yes | yes | NO | yes | yes |
| T4-AS-28 | X25519 | yes | yes | yes | yes | yes |
| T4-AS-29 | AES | NO | NO | n/a | n/a | n/a |
| T4-AS-30 | ChaCha20-Poly1305 | NO | NO | n/a | n/a | n/a |
| T4-AS-31 | HMAC | NO | NO | n/a | n/a | n/a |
| T4-AS-32 | RSA | yes | yes | NO | n/a | n/a |
| T4-AS-33 | Ed25519 | NO | NO | n/a | n/a | n/a |
| T4-AS-34 | TLS-1.0 | NO | NO | n/a | n/a | n/a |
| T4-AS-35 | TLS-1.1 | NO | NO | n/a | n/a | n/a |
| T4-AS-36 | TLS-1.2 | NO | NO | n/a | n/a | n/a |
| T4-AS-37 | TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 | NO | NO | n/a | n/a | n/a |
| T4-AS-38 | TLS_RSA_WITH_3DES_EDE_CBC_SHA | NO | NO | n/a | n/a | n/a |
| T4-AS-39 | TLS_RSA_WITH_AES_256_CBC_SHA | NO | NO | n/a | n/a | n/a |
| T4-AS-40 | TLS-1.1 | NO | NO | n/a | n/a | n/a |
| T4-AS-41 | TLS-1.2 | NO | NO | n/a | n/a | n/a |
| T4-AS-42 | TLS_RSA_WITH_AES_128_CBC_SHA | NO | NO | n/a | n/a | n/a |
| T4-AS-43 | TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 | NO | NO | n/a | n/a | n/a |
| T4-AS-44 | RSA | NO | NO | n/a | n/a | n/a |
| T4-AS-45 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T4-AS-46 | TLS-1.0 | NO | NO | n/a | n/a | n/a |
| T4-AS-47 | EC | NO | NO | n/a | n/a | n/a |
| T4-AS-48 | SHA-384 | NO | NO | n/a | n/a | n/a |
| T4-AS-49 | TLS-1.1 | NO | NO | n/a | n/a | n/a |
| T4-AS-50 | TLS-1.2 | NO | NO | n/a | n/a | n/a |
| T4-AS-51 | TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 | NO | NO | n/a | n/a | n/a |
| T4-AS-52 | TLS_RSA_WITH_AES_128_CBC_SHA | NO | NO | n/a | n/a | n/a |
| T4-AS-53 | TLS_RSA_WITH_3DES_EDE_CBC_SHA | NO | NO | n/a | n/a | n/a |
| T4-AS-54 | TLS-1.1 | NO | NO | n/a | n/a | n/a |
| T4-AS-55 | TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256 | NO | NO | n/a | n/a | n/a |
| T4-AS-56 | TLS_RSA_WITH_AES_256_CBC_SHA | NO | NO | n/a | n/a | n/a |
| T4-AS-57 | TLS_AES_256_GCM_SHA384 | NO | NO | n/a | n/a | n/a |
| T4-AS-58 | TLS_CHACHA20_POLY1305_SHA256 | NO | NO | n/a | n/a | n/a |
| T4-AS-59 | DH | NO | NO | n/a | n/a | n/a |
| T4-AS-60 | AES | NO | NO | n/a | n/a | n/a |
| T4-AS-61 | HMAC | NO | NO | n/a | n/a | n/a |
| T4-AS-62 | DH | yes | yes | NO | yes | yes |
| T4-AS-63 | ChaCha20-Poly1305 | NO | NO | n/a | n/a | n/a |
| T4-AS-64 | X25519 | NO | NO | n/a | n/a | n/a |
| T4-AS-65 | 3DES | NO | NO | n/a | n/a | n/a |
| T4-AS-66 | HMAC | NO | NO | n/a | n/a | n/a |
| T4-AS-67 | DH | yes | yes | NO | yes | yes |
| T4-AS-68 | AES | NO | NO | n/a | n/a | n/a |
| T5-PY-01 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T5-PY-02 | MD5 | NO | NO | n/a | n/a | n/a |
| T5-PY-03 | RSA | NO | NO | n/a | n/a | n/a |
| T5-PY-04 | AES | NO | NO | n/a | n/a | n/a |
| T5-PY-05 | RC4 | NO | NO | n/a | n/a | n/a |
| T5-PY-06 | SHA-256 | NO | NO | n/a | n/a | n/a |
| T5-PY-07 | RSA | NO | NO | n/a | n/a | n/a |
| T5-PY-08 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T5-PY-09 | HMAC | NO | NO | n/a | n/a | n/a |
| T5-JV-01 | RSA | NO | NO | n/a | n/a | n/a |
| T5-JV-02 | 3DES | NO | NO | n/a | n/a | n/a |
| T5-JV-03 | MD5 | NO | NO | n/a | n/a | n/a |
| T5-JV-04 | TEA | NO | NO | n/a | n/a | n/a |
| T5-JV-05 | RSA | NO | NO | n/a | n/a | n/a |
| T5-JV-06 | AES | NO | NO | n/a | n/a | n/a |
| T5-JV-07 | RSA | NO | NO | n/a | n/a | n/a |
| T5-JV-08 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T5-JV-09 | DES | NO | NO | n/a | n/a | n/a |
| T5-JV-10 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T5-JV-11 | EC | NO | NO | n/a | n/a | n/a |
| T5-JS-01 | MD5 | NO | NO | n/a | n/a | n/a |
| T5-JS-02 | AES | NO | NO | n/a | n/a | n/a |
| T5-JS-03 | RSA | NO | NO | n/a | n/a | n/a |
| T5-JS-04 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T5-JS-05 | HMAC | NO | NO | n/a | n/a | n/a |
| T5-JS-06 | 3DES | NO | NO | n/a | n/a | n/a |
| T5-JS-07 | EC | NO | NO | n/a | n/a | n/a |
| T5-JS-08 | PBKDF2 | NO | NO | n/a | n/a | n/a |
| T5-JS-09 | AES | NO | NO | n/a | n/a | n/a |
| T5-JS-10 | DH | NO | NO | n/a | n/a | n/a |
| T5-JS-11 | Ed25519 | NO | NO | n/a | n/a | n/a |
| T5-C-01 | MD5 | NO | NO | n/a | n/a | n/a |
| T5-C-02 | 3DES | NO | NO | n/a | n/a | n/a |
| T5-C-03 | RSA | NO | NO | n/a | n/a | n/a |
| T5-C-04 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T5-C-05 | HMAC | NO | NO | n/a | n/a | n/a |
| T5-C-06 | AES | NO | NO | n/a | n/a | n/a |
| T5-C-07 | EC | NO | NO | n/a | n/a | n/a |
| T5-C-08 | SHA-512 | NO | NO | n/a | n/a | n/a |
| T5-C-09 | AES | NO | NO | n/a | n/a | n/a |
| T5-C-10 | DH | NO | NO | n/a | n/a | n/a |
| T5-C-11 | X25519 | NO | NO | n/a | n/a | n/a |
| PQ-PY-01 | ML-KEM | NO | NO | n/a | n/a | n/a |
| PQ-PY-02 | ML-DSA | NO | NO | n/a | n/a | n/a |
| PQ-PY-03 | X25519 | yes | yes | yes | yes | yes |
| PQ-PY-04 | ML-KEM | NO | NO | n/a | n/a | n/a |
| PQ-PY-05 | ML-KEM | NO | NO | n/a | n/a | n/a |
| PQ-PY-06 | EC | yes | yes | NO | yes | yes |
| PQ-PY-07 | LMS | NO | NO | n/a | n/a | n/a |
| PQ-JV-01 | ML-KEM | NO | NO | n/a | n/a | n/a |
| PQ-JV-02 | ML-DSA | NO | NO | n/a | n/a | n/a |
| PQ-JV-03 | ML-DSA | NO | NO | n/a | n/a | n/a |
| PQ-JV-04 | EC | yes | yes | NO | yes | yes |
| PQ-JV-05 | LMS | NO | NO | n/a | n/a | n/a |
| PQ-JV-06 | XMSS | NO | NO | n/a | n/a | n/a |
| PQ-AS-01 | ML-DSA | NO | NO | n/a | n/a | n/a |
| PQ-AS-02 | ML-DSA | NO | NO | n/a | n/a | n/a |
| PQ-AS-03 | ML-DSA | NO | NO | n/a | n/a | n/a |
| PQ-AS-04 | RSA | NO | NO | n/a | n/a | n/a |
| PQ-AS-05 | SHA-256 | NO | NO | n/a | n/a | n/a |
| PQ-AS-06 | ML-KEM | NO | NO | n/a | n/a | n/a |
| PQ-AS-07 | ML-DSA | NO | NO | n/a | n/a | n/a |
| PQ-AS-08 | TLS-1.3 | NO | NO | n/a | n/a | n/a |
| PQ-AS-09 | X25519MLKEM768 | NO | NO | n/a | n/a | n/a |
| PQ-AS-10 | X25519 | NO | NO | n/a | n/a | n/a |
| PQ-AS-11 | SecP384r1MLKEM1024 | NO | NO | n/a | n/a | n/a |
| PQ-AS-12 | X25519MLKEM768 | NO | NO | n/a | n/a | n/a |
| PQ-AS-13 | EC | NO | NO | n/a | n/a | n/a |
| PQ-AS-14 | TLS-1.3 | NO | NO | n/a | n/a | n/a |
| PQ-AS-15 | X25519MLKEM768 | NO | NO | n/a | n/a | n/a |
| PQ-AS-16 | sntrup761x25519 | NO | NO | n/a | n/a | n/a |
| PQ-AS-17 | X25519 | yes | yes | yes | yes | yes |
| PQ-AS-18 | Ed25519 | NO | NO | n/a | n/a | n/a |
| PQ-AS-19 | ChaCha20-Poly1305 | NO | NO | n/a | n/a | n/a |
| PQ-AS-20 | TLS-1.3 | NO | NO | n/a | n/a | n/a |
| PQ-AS-21 | X25519 | NO | NO | n/a | n/a | n/a |
| PQ-AS-22 | EC | NO | NO | n/a | n/a | n/a |
| PQ-AS-23 | LMS | NO | NO | n/a | n/a | n/a |
| PQ-AS-24 | XMSS | NO | NO | n/a | n/a | n/a |
| PQ-AS-25 | LMS | NO | NO | n/a | n/a | n/a |
| PQ-AS-26 | XMSS | NO | NO | n/a | n/a | n/a |
| PQ-AS-27 | EC | NO | NO | n/a | n/a | n/a |
| T1-GO-01 | MD5 | NO | NO | n/a | n/a | n/a |
| T1-GO-02 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T1-GO-03 | SHA-256 | NO | NO | n/a | n/a | n/a |
| T1-GO-04 | SHA3-256 | NO | NO | n/a | n/a | n/a |
| T1-GO-05 | AES | NO | NO | n/a | n/a | n/a |
| T1-GO-06 | AES | NO | NO | n/a | n/a | n/a |
| T1-GO-07 | 3DES | NO | NO | n/a | n/a | n/a |
| T1-GO-08 | DES | NO | NO | n/a | n/a | n/a |
| T1-GO-09 | RC4 | NO | NO | n/a | n/a | n/a |
| T1-GO-10 | RSA | yes | yes | NO | yes | yes |
| T1-GO-11 | EC | yes | yes | NO | yes | yes |
| T1-GO-12 | Ed25519 | yes | yes | yes | yes | yes |
| T1-GO-13 | X25519 | yes | yes | yes | yes | yes |
| T1-GO-14 | DSA | yes | yes | NO | yes | yes |
| T1-GO-15 | HMAC | NO | NO | n/a | n/a | n/a |
| T1-GO-16 | PBKDF2 | NO | NO | n/a | n/a | n/a |
| T1-GO-17 | TLS-1.0 | NO | NO | n/a | n/a | n/a |
| T1-GO-18 | TLS_RSA_WITH_3DES_EDE_CBC_SHA | NO | NO | n/a | n/a | n/a |
| T1-GO-19 | TLS_RSA_WITH_AES_128_CBC_SHA | NO | NO | n/a | n/a | n/a |
| T1-GO-20 | TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 | NO | NO | n/a | n/a | n/a |
| T2-GO-01 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T2-GO-02 | RSA | yes | yes | NO | yes | yes |
| T2-GO-03 | EC | yes | yes | NO | yes | yes |
| T2-GO-04 | HMAC | NO | NO | n/a | n/a | n/a |
| T2-GO-05 | AES | NO | NO | n/a | n/a | n/a |
| T2-GO-06 | 3DES | NO | NO | n/a | n/a | n/a |
| PQ-GO-01 | ML-KEM | NO | NO | n/a | n/a | n/a |
| PQ-GO-02 | TLS-1.3 | NO | NO | n/a | n/a | n/a |
| PQ-GO-03 | X25519MLKEM768 | NO | NO | n/a | n/a | n/a |
| PQ-GO-04 | X25519 | NO | NO | n/a | n/a | n/a |
| T1-JS-01 | MD5 | NO | NO | n/a | n/a | n/a |
| T1-JS-02 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T1-JS-03 | SHA-256 | NO | NO | n/a | n/a | n/a |
| T1-JS-04 | SHA3-256 | NO | NO | n/a | n/a | n/a |
| T1-JS-05 | AES | NO | NO | n/a | n/a | n/a |
| T1-JS-06 | AES | NO | NO | n/a | n/a | n/a |
| T1-JS-07 | 3DES | NO | NO | n/a | n/a | n/a |
| T1-JS-08 | ChaCha20-Poly1305 | NO | NO | n/a | n/a | n/a |
| T1-JS-09 | RSA | yes | yes | NO | yes | yes |
| T1-JS-10 | EC | yes | yes | NO | yes | yes |
| T1-JS-11 | Ed25519 | yes | yes | yes | yes | yes |
| T1-JS-12 | X25519 | yes | yes | yes | yes | yes |
| T1-JS-13 | DH | yes | yes | NO | yes | yes |
| T1-JS-14 | HMAC | NO | NO | n/a | n/a | n/a |
| T1-JS-15 | PBKDF2 | NO | NO | n/a | n/a | n/a |
| T1-JS-16 | RSA | yes | yes | NO | yes | yes |
| T1-JS-17 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T2-TS-01 | 3DES | NO | NO | n/a | n/a | n/a |
| T2-TS-02 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T2-TS-03 | RSA | yes | yes | NO | yes | yes |
| T2-TS-04 | EC | yes | yes | NO | yes | yes |
| T2-TS-05 | AES | NO | NO | n/a | n/a | n/a |
| T2-TS-06 | AES | NO | NO | n/a | n/a | n/a |
| T2-TS-07 | HMAC | NO | NO | n/a | n/a | n/a |
| T1-C-01 | MD5 | NO | NO | n/a | n/a | n/a |
| T1-C-02 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T1-C-03 | SHA-256 | NO | NO | n/a | n/a | n/a |
| T1-C-04 | SHA3-256 | NO | NO | n/a | n/a | n/a |
| T1-C-05 | AES | NO | NO | n/a | n/a | n/a |
| T1-C-06 | AES | NO | NO | n/a | n/a | n/a |
| T1-C-07 | 3DES | NO | NO | n/a | n/a | n/a |
| T1-C-08 | ChaCha20-Poly1305 | NO | NO | n/a | n/a | n/a |
| T1-C-09 | RSA | yes | yes | NO | yes | yes |
| T1-C-10 | RSA | NO | NO | n/a | n/a | n/a |
| T1-C-11 | EC | NO | NO | n/a | n/a | n/a |
| T1-C-12 | Ed25519 | NO | NO | n/a | n/a | n/a |
| T1-C-13 | X25519 | NO | NO | n/a | n/a | n/a |
| T1-C-14 | DH | NO | NO | n/a | n/a | n/a |
| T1-C-15 | HMAC | NO | NO | n/a | n/a | n/a |
| T1-C-16 | PBKDF2 | NO | NO | n/a | n/a | n/a |
| T1-C-17 | TLS-1.0 | NO | NO | n/a | n/a | n/a |
| T1-C-18 | TLS_RSA_WITH_3DES_EDE_CBC_SHA | NO | NO | n/a | n/a | n/a |
| T1-C-19 | TLS_RSA_WITH_AES_128_CBC_SHA | NO | NO | n/a | n/a | n/a |
| T1-C-20 | TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 | NO | NO | n/a | n/a | n/a |
| T1-CS-01 | MD5 | NO | NO | n/a | n/a | n/a |
| T1-CS-02 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T1-CS-03 | SHA-256 | NO | NO | n/a | n/a | n/a |
| T1-CS-04 | SHA3-256 | NO | NO | n/a | n/a | n/a |
| T1-CS-05 | RSA | yes | yes | NO | yes | yes |
| T1-CS-06 | EC | yes | yes | NO | yes | yes |
| T1-CS-07 | EC | yes | yes | NO | yes | yes |
| T1-CS-08 | AES | NO | NO | n/a | n/a | n/a |
| T1-CS-09 | AES | NO | NO | n/a | n/a | n/a |
| T1-CS-10 | 3DES | NO | NO | n/a | n/a | n/a |
| T1-CS-11 | HMAC | NO | NO | n/a | n/a | n/a |
| T1-CS-12 | PBKDF2 | NO | NO | n/a | n/a | n/a |
| T1-CS-13 | DSA | yes | yes | NO | yes | yes |
| T2-C-01 | AES | NO | NO | n/a | n/a | n/a |
| T2-C-02 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T2-C-03 | RSA | yes | yes | NO | yes | yes |
| T2-C-04 | EC | NO | NO | n/a | n/a | n/a |
| T2-C-05 | HMAC | NO | NO | n/a | n/a | n/a |
| T2-C-06 | 3DES | NO | NO | n/a | n/a | n/a |
| T2-CS-01 | AES | NO | NO | n/a | n/a | n/a |
| T2-CS-02 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T2-CS-03 | MD5 | NO | NO | n/a | n/a | n/a |
| T2-CS-04 | SHA-512 | NO | NO | n/a | n/a | n/a |
| T2-CS-05 | RSA | yes | yes | NO | yes | yes |
| T2-CS-06 | EC | yes | yes | NO | yes | yes |
| MX-PY-1a | PBKDF2 | NO | NO | n/a | n/a | n/a |
| MX-PY-1b | PBKDF2 | NO | NO | n/a | n/a | n/a |
| MX-PY-1c | HMAC | NO | NO | n/a | n/a | n/a |
| MX-PY-1d | AES | NO | NO | n/a | n/a | n/a |
| MX-PY-2a | DH | yes | yes | NO | yes | yes |
| MX-PY-2b | ML-DSA | NO | NO | n/a | n/a | n/a |
| MX-PY-2c | DH | yes | yes | NO | yes | yes |
| MX-PY-2d | ChaCha20-Poly1305 | NO | NO | n/a | n/a | n/a |
| MX-PY-3a | SHA-1 | NO | NO | n/a | n/a | n/a |
| MX-PY-3b | HMAC | NO | NO | n/a | n/a | n/a |
| MX-PY-3c | EC | yes | yes | NO | yes | yes |
| MX-PY-3d | EC | yes | yes | NO | yes | yes |
| MX-JV-1a | DH | yes | yes | NO | yes | yes |
| MX-JV-1b | SHA-1 | NO | NO | n/a | n/a | n/a |
| MX-JV-1c | DH | yes | yes | NO | yes | yes |
| MX-JV-1d | AES | NO | NO | n/a | n/a | n/a |
| MX-JV-2a | SHA-256 | NO | NO | n/a | n/a | n/a |
| MX-JV-2b | Ed25519 | yes | yes | yes | yes | yes |
| MX-JV-2c | PBKDF2 | NO | NO | n/a | n/a | n/a |
| MX-JV-2d | PBKDF2 | NO | NO | n/a | n/a | n/a |
| MX-JV-3a | HMAC | NO | NO | n/a | n/a | n/a |
| MX-JV-3b | 3DES | NO | NO | n/a | n/a | n/a |
| MX-JV-3c | ChaCha20-Poly1305 | NO | NO | n/a | n/a | n/a |
| MX-JV-3d | SHA-512 | NO | NO | n/a | n/a | n/a |
| MX-JV-3e | 3DES | NO | NO | n/a | n/a | n/a |
| MX-GO-1a | PBKDF2 | NO | NO | n/a | n/a | n/a |
| MX-GO-1b | ML-KEM | NO | NO | n/a | n/a | n/a |
| MX-GO-1c | RSA | yes | yes | NO | yes | yes |
| MX-GO-1d | RSA | yes | yes | NO | yes | yes |
| MX-GO-2a | PBKDF2 | NO | NO | n/a | n/a | n/a |
| MX-GO-2b | DES | NO | NO | n/a | n/a | n/a |
| MX-GO-2c | PBKDF2 | NO | NO | n/a | n/a | n/a |
| MX-GO-2d | 3DES | NO | NO | n/a | n/a | n/a |
| MX-GO-3a | RSA | yes | yes | NO | yes | yes |
| MX-GO-3b | RC4 | NO | NO | n/a | n/a | n/a |
| MX-GO-3c | HMAC | NO | NO | n/a | n/a | n/a |
| MX-GO-3d | Ed25519 | yes | yes | yes | yes | yes |
| MX-JS-1a | AES | NO | NO | n/a | n/a | n/a |
| MX-JS-1b | HMAC | NO | NO | n/a | n/a | n/a |
| MX-JS-1c | AES | NO | NO | n/a | n/a | n/a |
| MX-JS-2a | SHA3-256 | NO | NO | n/a | n/a | n/a |
| MX-JS-2b | PBKDF2 | NO | NO | n/a | n/a | n/a |
| MX-JS-2c | EC | yes | yes | NO | yes | yes |
| MX-JS-2d | EC | yes | yes | NO | yes | yes |
| MX-JS-2e | AES | NO | NO | n/a | n/a | n/a |
| MX-TS-1a | EC | yes | yes | NO | yes | yes |
| MX-TS-1b | HMAC | NO | NO | n/a | n/a | n/a |
| MX-TS-1c | AES | NO | NO | n/a | n/a | n/a |
| MX-TS-1d | RSA | yes | yes | NO | yes | yes |
| MX-C-1a | SHA-1 | NO | NO | n/a | n/a | n/a |
| MX-C-1b | EC | NO | NO | n/a | n/a | n/a |
| MX-C-1c | HMAC | NO | NO | n/a | n/a | n/a |
| MX-C-1d | X25519 | NO | NO | n/a | n/a | n/a |
| MX-C-1e | HMAC | NO | NO | n/a | n/a | n/a |
| MX-C-2a | EC | NO | NO | n/a | n/a | n/a |
| MX-C-2b | AES | NO | NO | n/a | n/a | n/a |
| MX-C-2c | 3DES | NO | NO | n/a | n/a | n/a |
| MX-C-2d | 3DES | NO | NO | n/a | n/a | n/a |
| MX-C-3a | AES | NO | NO | n/a | n/a | n/a |
| MX-C-3b | 3DES | NO | NO | n/a | n/a | n/a |
| MX-C-3c | AES | NO | NO | n/a | n/a | n/a |
| MX-C-3d | DH | NO | NO | n/a | n/a | n/a |
| SYS-GO-01 | RSA | yes | NO | NO | yes | yes |
| SYS-GO-02 | HMAC | NO | NO | n/a | n/a | n/a |
| SYS-GO-03 | SHA-256 | NO | NO | n/a | n/a | n/a |
| SYS-PY-01 | AES | NO | NO | n/a | n/a | n/a |
| SYS-PY-02 | HMAC | NO | NO | n/a | n/a | n/a |
| SYS-PY-03 | RSA | NO | NO | n/a | n/a | n/a |
| SYS-PY-04 | SHA-1 | NO | NO | n/a | n/a | n/a |
| SYS-JV-01 | EC | yes | NO | NO | yes | yes |
| SYS-JV-02 | SHA-1 | NO | NO | n/a | n/a | n/a |
| SYS-AR-01 | EC | NO | NO | n/a | n/a | n/a |
| SYS-AR-02 | SHA-1 | NO | NO | n/a | n/a | n/a |
| SYS-AR-03 | RSA | NO | NO | n/a | n/a | n/a |
| SYS-AR-04 | HMAC | NO | NO | n/a | n/a | n/a |
| SYS-AR-05 | SHA-1 | NO | NO | n/a | n/a | n/a |
| SYS-AR-06 | SHA-256 | NO | NO | n/a | n/a | n/a |
| SYS-AS-01 | TLS-1.2 | NO | NO | n/a | n/a | n/a |
| SYS-AS-02 | TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 | NO | NO | n/a | n/a | n/a |
| SYS-AS-03 | TLS_RSA_WITH_AES_128_CBC_SHA | NO | NO | n/a | n/a | n/a |
| SYS-AS-04 | RSA | NO | NO | n/a | n/a | n/a |
| SYS-AS-05 | SHA-256 | NO | NO | n/a | n/a | n/a |
| SYS-AS-06 | RSA | yes | yes | NO | n/a | n/a |
| SYS-AS-07 | EC | NO | NO | n/a | n/a | n/a |
| SYS-AS-08 | SHA-384 | NO | NO | n/a | n/a | n/a |
| SYS-AS-09 | EC | yes | yes | NO | yes | yes |
| SYS-AS-10 | RSA | yes | yes | NO | yes | yes |
| SYS-AS-11 | AES | NO | NO | n/a | n/a | n/a |
| DC-PY-01 | MD5 | NO | NO | n/a | n/a | n/a |
| DC-PY-02 | RSA | yes | yes | NO | yes | yes |
| DC-JV-01 | DES | NO | NO | n/a | n/a | n/a |
| DC-JV-02 | SHA-1 | NO | NO | n/a | n/a | n/a |
| DC-GO-01 | MD5 | NO | NO | n/a | n/a | n/a |
| DC-GO-02 | RC4 | NO | NO | n/a | n/a | n/a |
| DC-JS-01 | MD5 | NO | NO | n/a | n/a | n/a |
| DC-JS-02 | 3DES | NO | NO | n/a | n/a | n/a |
| DC-C-01 | MD5 | NO | NO | n/a | n/a | n/a |
| DC-C-02 | 3DES | NO | NO | n/a | n/a | n/a |
