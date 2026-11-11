# CBOM Testbench Scorecard: QCI v0.7

**Overall:** 202/393 findings detected (51.4% recall), 29 false positives (87.4% precision), parameters correct on 66.8% of detections.

Calibration cases (generated Tier 1-2 siblings of the hand-written cases; they feed the holdout's overfit gap and are not counted anywhere else here): 195/304 detected (64.1%), 0 false positives.

Password-gated findings (readable only by trying a well-known default password; scored separately, not in any number below): 0/2 detected.

| Bucket | Detected | Recall | 95% interval | At primary site | Params correct | Line accurate | Quantum flag | False pos. | Precision |
|---|---|---|---|---|---|---|---|---|---|
| Tier 1 c | 9/20 | 45.0% | 25.8–65.8% | 45.0% | 44.4% | 100.0% | n/a | 0 | 100.0% |
| Tier 1 csharp | 4/13 | 30.8% | 12.7–57.6% | 30.8% | 0.0% | 100.0% | n/a | 0 | 100.0% |
| Tier 1 go | 5/20 | 25.0% | 11.2–46.9% | 25.0% | 40.0% | 100.0% | n/a | 0 | 100.0% |
| Tier 1 java | 15/16 | 93.8% | 71.7–98.9% | 93.8% | 93.3% | 100.0% | n/a | 0 | 100.0% |
| Tier 1 javascript | 3/17 | 17.6% | 6.2–41.0% | 17.6% | 66.7% | 33.3% | n/a | 0 | 100.0% |
| Tier 1 python | 15/16 | 93.8% | 71.7–98.9% | 93.8% | 100.0% | 100.0% | n/a | 0 | 100.0% |
| Tier 2 c | 2/6 | 33.3% | 9.7–70.0% (thin) | 33.3% | 50.0% | 100.0% | n/a | 0 | 100.0% |
| Tier 2 csharp | 1/6 | 16.7% | 3.0–56.4% (thin) | 16.7% | 100.0% | 100.0% | n/a | 0 | 100.0% |
| Tier 2 go | 5/6 | 83.3% | 43.6–97.0% (thin) | 83.3% | 20.0% | 100.0% | n/a | 0 | 100.0% |
| Tier 2 java | 6/8 | 75.0% | 40.9–92.9% (thin) | 62.5% | 100.0% | 100.0% | n/a | 0 | 100.0% |
| Tier 2 python | 7/9 | 77.8% | 45.3–93.7% (thin) | 66.7% | 100.0% | 85.7% | n/a | 0 | 100.0% |
| Tier 2 typescript | 2/7 | 28.6% | 8.2–64.1% (thin) | 28.6% | 50.0% | 100.0% | n/a | 0 | 100.0% |
| Tier 3 java | 6/7 | 85.7% | 48.7–97.4% (thin) | 71.4% | 50.0% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 3 python | 8/9 | 88.9% | 56.5–98.0% (thin) | 55.6% | 25.0% | 100.0% | n/a | 0 | 100.0% |
| Tier 4 assets | 21/66 | 31.8% | 21.8–43.8% | 31.8% | 81.0% | 84.6% | n/a | 0 | 100.0% |
| Tier 5 c | 1/3 | 33.3% | 6.1–79.2% (thin) | 33.3% | 100.0% | n/a | n/a | 1 | 50.0% |
| Tier 5 java | 0/11 | 0.0% | 0.0–25.9% | 0.0% | n/a | n/a | n/a | 0 | n/a |
| Tier 5 javascript | 0/3 | 0.0% | 0.0–56.2% (thin) | 0.0% | n/a | n/a | n/a | 0 | n/a |
| Tier 5 python | 2/9 | 22.2% | 6.3–54.7% (thin) | 22.2% | 50.0% | n/a | n/a | 0 | 100.0% |
| Dead code c | 1/2 | 50.0% | 9.5–90.5% (thin) | 50.0% | 100.0% | 100.0% | n/a | 0 | 100.0% |
| Dead code go | 0/2 | 0.0% | 0.0–65.8% (thin) | 0.0% | n/a | n/a | n/a | 0 | n/a |
| Dead code java | 2/2 | 100.0% | 34.2–100.0% (thin) | 100.0% | 100.0% | 100.0% | n/a | 0 | 100.0% |
| Dead code javascript | 0/2 | 0.0% | 0.0–65.8% (thin) | 0.0% | n/a | n/a | n/a | 0 | n/a |
| Dead code python | 2/2 | 100.0% | 34.2–100.0% (thin) | 100.0% | 100.0% | 100.0% | n/a | 0 | 100.0% |
| Mixed files c | 5/13 | 38.5% | 17.7–64.5% | 38.5% | 40.0% | 100.0% | n/a | 5 | 50.0% |
| Mixed files go | 9/12 | 75.0% | 46.8–91.1% | 75.0% | 22.2% | 100.0% | n/a | 2 | 81.8% |
| Mixed files java | 10/13 | 76.9% | 49.7–91.8% | 76.9% | 60.0% | 100.0% | n/a | 4 | 71.4% |
| Mixed files javascript | 2/8 | 25.0% | 7.1–59.1% (thin) | 25.0% | 0.0% | 100.0% | n/a | 5 | 28.6% |
| Mixed files python | 12/12 | 100.0% | 75.7–100.0% | 100.0% | 41.7% | 100.0% | n/a | 4 | 75.0% |
| Mixed files typescript | 1/4 | 25.0% | 4.6–69.9% (thin) | 25.0% | 0.0% | 100.0% | n/a | 3 | 25.0% |
| PQC assets | 21/27 | 77.8% | 59.2–89.4% | 77.8% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| PQC go | 1/4 | 25.0% | 4.6–69.9% (thin) | 25.0% | 0.0% | 100.0% | n/a | 0 | 100.0% |
| PQC java | 4/6 | 66.7% | 30.0–90.3% (thin) | 66.7% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| PQC python | 6/6 | 100.0% | 61.0–100.0% (thin) | 100.0% | 50.0% | 100.0% | 100.0% | 0 | 100.0% |
| System fixture artifacts | 4/6 | 66.7% | 30.0–90.3% (thin) | 66.7% | 100.0% | n/a | n/a | 1 | 80.0% |
| System fixture assets | 3/11 | 27.3% | 9.7–56.6% | 27.3% | 66.7% | 100.0% | n/a | 0 | 100.0% |
| System fixture go | 2/3 | 66.7% | 20.8–93.9% (thin) | 0.0% | 0.0% | 100.0% | n/a | 0 | 100.0% |
| System fixture java | 2/2 | 100.0% | 34.2–100.0% (thin) | 50.0% | 50.0% | 100.0% | n/a | 0 | 100.0% |
| System fixture python | 3/4 | 75.0% | 30.1–95.4% (thin) | 25.0% | 66.7% | 100.0% | 0.0% | 0 | 100.0% |
| **Total** | 202/393 | 51.4% | 46.5–56.3% | 48.6% | 66.8% | 97.2% | 92.9% | 29 | 87.4% |
| Negative controls | | | | | | | | 4 | |

Intervals are 95% Wilson intervals on recall. 25 bucket(s) have fewer than 10 findings and are marked thin: read their rates as indications, not measurements.

**PQC over-claims: 13.** Post-quantum or hybrid algorithms reported where the code or config has none. Each one makes migration look further along than it is. Any number above zero should be explained by the vendor before purchase.

**PQC by standard name: 19/19 (100.0%).** Detected post-quantum findings reported under the FIPS 203/204/205 name or OID. Reports that only say Kyber, Dilithium, SPHINCS+ or Falcon keep their recall credit and fail this check.

## System fixture: routing and asset links

**Routable: 9/14 detected system findings (64.3%)** (of 26). Routable means a reported location resolves, through the fixture's CODEOWNERS, to the team that owns the fix. Reporting only the shared wrapper or its config is detection, but the ticket lands with platform-security.

| Finding | Owner | Reported locations route to |
|---|---|---|
| SYS-GO-01 | @acme/edge-team | @acme/platform-security |
| SYS-GO-02 | @acme/edge-team | @acme/platform-security |
| SYS-PY-01 | @acme/payments-team | @acme/platform-security |
| SYS-PY-02 | @acme/payments-team | @acme/platform-security |
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

**Deadline-weighted recall: 51.7%** (at primary site: 48.7%). **Findings due by end of 2030 that this scanner missed: 64.**

| When it's due | Weight | Detected | Recall | At primary site |
|---|---|---|---|---|
| Due now (not approved or past its date) | 5 | 46/99 | 46.5% | 44.4% |
| Due by end of 2030 | 4 | 28/39 | 71.8% | 64.1% |
| Due 2031 to 2033 | 3 | 0/0 | n/a | n/a |
| Due 2034 to 2035 | 2 | 54/107 | 50.5% | 47.7% |
| No deadline (approved, review, out of scope, unknown) | 1 | 74/148 | 50.0% | 48.0% |

| Missed | Algorithm | Due | File |
|---|---|---|---|
| T2-PY-06 | MD5 | **now** | `corpus/tier2/python/t2_dispatch_table.py` |
| T2-JV-04 | SHA-1 | 2030-12-31 | `corpus/tier2/java/T2Enum.java` |
| T3-PY-08 | MD5 | **now** | `corpus/tier3/python/dependency_injection/wiring.py` |
| T3-JV-06 | MD5 | **now** | `corpus/tier3/java/dependency_injection/src/com/acme/audit/DigestProvider.java` |
| T4-AS-04 | SHA-1 | 2030-12-31 | `corpus/tier4/assets/certs/payments_legacy.crt` |
| T4-AS-24 | RSA-1024 | 2013-12-31 | `corpus/tier4/assets/keystores/partner_truststore.jks` |
| T4-AS-25 | SHA-1 | 2030-12-31 | `corpus/tier4/assets/keystores/partner_truststore.jks` |
| T4-AS-38 | TLS_RSA_WITH_3DES_EDE_CBC_SHA | **now** | `corpus/tier4/assets/tls/nginx.conf` |
| T4-AS-44 | RSA-1024 | 2013-12-31 | `corpus/tier4/assets/tls/openssl.cnf` |
| T4-AS-53 | TLS_RSA_WITH_3DES_EDE_CBC_SHA | **now** | `corpus/tier4/assets/tls/httpd-ssl.conf` |
| T4-AS-58 | TLS_CHACHA20_POLY1305_SHA256 | **now** | `corpus/tier4/assets/tls/haproxy.cfg` |
| T4-AS-65 | 3DES | 2023-12-31 | `corpus/tier4/assets/ipsec/ipsec.conf` |
| T4-AS-66 | HMAC-SHA-1 | 2030-12-31 | `corpus/tier4/assets/ipsec/ipsec.conf` |
| T4-AS-67 | DH-1024 | 2013-12-31 | `corpus/tier4/assets/ipsec/ipsec.conf` |
| T5-PY-01 | SHA-1 | 2030-12-31 | `corpus/tier5/python/t5_string_assembly.py` |
| T5-PY-02 | MD5 | **now** | `corpus/tier5/python/t5_string_assembly.py` |
| T5-PY-05 | RC4 | **now** | `corpus/tier5/python/t5_handrolled_keystream.py` |
| T5-PY-07 | RSA-1024 | 2013-12-31 | `corpus/tier5/python/t5_handrolled_pubkey.py` |
| T5-JV-02 | 3DES-CBC | 2023-12-31 | `corpus/tier5/java/T5StringAssembly.java` |
| T5-JV-03 | MD5 | **now** | `corpus/tier5/java/T5Reflection.java` |
| T5-JV-04 | TEA | **now** | `corpus/tier5/java/T5BlockTransform.java` |
| T5-JV-07 | RSA-1024 | 2013-12-31 | `corpus/tier5/java/compiled/billing-core.jar` |
| T5-JV-08 | SHA-1 | 2030-12-31 | `corpus/tier5/java/compiled/billing-core.jar` |
| T5-JV-09 | DES-ECB | **now** | `corpus/tier5/java/compiled/token-vault.jar` |
| T5-JV-10 | SHA-1 | 2030-12-31 | `corpus/tier5/java/compiled/token-vault.jar` |
| T5-JS-01 | MD5 | **now** | `corpus/tier5/javascript/dist/session-tokens.min.js` |
| T5-JS-03 | RSA-1024 | 2013-12-31 | `corpus/tier5/javascript/dist/session-tokens.min.js` |
| T5-C-02 | 3DES-CBC | 2023-12-31 | `corpus/tier5/c/bin/meterd` |
| T5-C-03 | RSA-1024 | 2013-12-31 | `corpus/tier5/c/bin/meterd` |
| T1-GO-01 | MD5 | **now** | `corpus/tier1/go/hashes/main.go` |
| T1-GO-07 | 3DES-CBC | 2023-12-31 | `corpus/tier1/go/des/main.go` |
| T1-GO-08 | DES-CBC | **now** | `corpus/tier1/go/des/main.go` |
| T1-GO-09 | RC4 | **now** | `corpus/tier1/go/rc4/main.go` |
| T1-GO-18 | TLS_RSA_WITH_3DES_EDE_CBC_SHA | **now** | `corpus/tier1/go/tls_config/main.go` |
| T2-GO-06 | 3DES-CBC | 2023-12-31 | `corpus/tier2/go/block_factory/main.go` |
| T1-JS-01 | MD5 | **now** | `corpus/tier1/javascript/t1_hashes.js` |
| T1-JS-07 | 3DES-CBC | 2023-12-31 | `corpus/tier1/javascript/t1_triple_des.js` |
| T1-JS-08 | ChaCha20-Poly1305 | **now** | `corpus/tier1/javascript/t1_chacha.js` |
| T1-JS-17 | SHA-1 | 2030-12-31 | `corpus/tier1/javascript/t1_webcrypto.mjs` |
| T2-TS-01 | 3DES-CBC | 2023-12-31 | `corpus/tier2/typescript/t2_config_object.ts` |
| T2-TS-03 | RSA-1024 | 2013-12-31 | `corpus/tier2/typescript/t2_env_default.ts` |
| T1-C-07 | 3DES-CBC | 2023-12-31 | `corpus/tier1/c/t1_triple_des.c` |
| T1-C-08 | ChaCha20-Poly1305 | **now** | `corpus/tier1/c/t1_chacha.c` |
| T1-C-18 | TLS_RSA_WITH_3DES_EDE_CBC_SHA | **now** | `corpus/tier1/c/t1_tls_ctx.c` |
| T1-CS-01 | MD5 | **now** | `corpus/tier1/csharp/Hashes/Program.cs` |
| T1-CS-02 | SHA-1 | 2030-12-31 | `corpus/tier1/csharp/Hashes/Program.cs` |
| T2-C-03 | RSA-1024 | 2013-12-31 | `corpus/tier2/c/t2_macro_bits.c` |
| T2-C-06 | 3DES-ECB | 2023-12-31 | `corpus/tier2/c/t2_cipher_struct.c` |
| T2-CS-03 | MD5 | **now** | `corpus/tier2/csharp/DispatchTable/Program.cs` |
| T2-CS-05 | RSA-1024 | 2013-12-31 | `corpus/tier2/csharp/KeyFactory/Program.cs` |
| MX-JV-3c | ChaCha20-Poly1305 | **now** | `corpus/mixed/java/OrderDefaultsModule.java` |
| MX-GO-2b | DES-CBC | **now** | `corpus/mixed/go/report_gateway/main.go` |
| MX-GO-2d | 3DES-CBC | 2023-12-31 | `corpus/mixed/go/report_gateway/main.go` |
| MX-GO-3b | RC4 | **now** | `corpus/mixed/go/invoice_gateway/main.go` |
| MX-C-2c | 3DES-ECB | 2023-12-31 | `corpus/mixed/c/policy_agent.c` |
| MX-C-2d | 3DES-CBC | 2023-12-31 | `corpus/mixed/c/policy_agent.c` |
| MX-C-3b | 3DES-CBC | 2023-12-31 | `corpus/mixed/c/audit_daemon.c` |
| SYS-PY-04 | SHA-1 | 2030-12-31 | `corpus/system/payments-platform/services/settlement-worker/partner_ca.py` |
| SYS-AR-02 | SHA-1 | 2030-12-31 | `corpus/system/payments-platform/services/ledger-service/build/libs/ledger-service.jar` |
| DC-GO-01 | MD5 | **now** | `corpus/deadcode/go/legacy/main.go` |
| DC-GO-02 | RC4 | **now** | `corpus/deadcode/go/legacy/main.go` |
| DC-JS-01 | MD5 | **now** | `corpus/deadcode/javascript/dead_paths.js` |
| DC-JS-02 | 3DES-CBC | 2023-12-31 | `corpus/deadcode/javascript/dead_paths.js` |
| DC-C-02 | 3DES-CBC | 2023-12-31 | `corpus/deadcode/c/dead_branches.c` |

## Actionability: could an engineer open a ticket from this?

Rubric `cbom-actionability-v1` (proposed; see `rubric/actionability.json`). Each detected finding is checked for the fields a migration ticket needs. Facts are checked against the real files.

**Ticket-ready: 111/202 detected findings (55.0%)**, meaning every must-have is present and correct. **Actionable recall: 28.2%** of all 393 expected findings were both found and ticket-ready. Field completeness across all checks: 46.2%.

| Check | Tier | Applies to | Passed | Rate |
|---|---|---|---|---|
| Exact location | must | 202 | 199 | 98.5% |
| Correct parameters | must | 135 | 68 | 50.4% |
| Primitive, where the family is ambiguous | must | 45 | 34 | 75.6% |
| Certificate expiry (correct) | must | 13 | 2 | 15.4% |
| Certificate subject (correct) | must | 13 | 2 | 15.4% |
| Key material type | must | 7 | 0 | 0.0% |
| Protocol version | must | 7 | 0 | 0.0% |
| OID | should | 186 | 57 | 30.6% |
| Crypto functions | should | 193 | 193 | 100.0% |
| Quantum security level (correct) | should | 191 | 13 | 6.8% |
| Code context | should | 97 | 0 | 0.0% |
| Providing library | should | 99 | 0 | 0.0% |
| Certificate issuer | should | 13 | 2 | 15.4% |
| Certificate start date | should | 13 | 0 | 0.0% |
| Certificate key and signature linked | should | 13 | 0 | 0.0% |
| Key format | should | 7 | 0 | 0.0% |
| Cipher suite in a protocol | should | 0 | 0 | n/a |

Detected but not ticket-ready (91), first 25:

| ID | Algorithm | Missing must-haves |
|---|---|---|
| T1-JV-08 | AES-128-ECB | Correct parameters |
| T2-PY-03 | AES-128-CBC | Exact location |
| T3-PY-01 | RSA-1024 | Correct parameters |
| T3-PY-03 | AES-128-GCM | Correct parameters |
| T3-PY-04 | RSA-1024 | Correct parameters |
| T3-PY-05 | RSA-3072 | Correct parameters |
| T3-PY-06 | AES-256-CBC | Correct parameters |
| T3-PY-09 | HMAC-SHA-256 | Correct parameters |
| T3-JV-01 | RSA-1024 | Correct parameters |
| T3-JV-03 | AES-128-GCM | Correct parameters |
| T3-JV-04 | AES-256-CBC | Correct parameters |
| T4-AS-01 | RSA-2048 | Primitive, where the family is ambiguous, Certificate expiry (correct), Certificate subject (correct) |
| T4-AS-03 | RSA-1024 | Primitive, where the family is ambiguous, Certificate expiry (correct), Certificate subject (correct) |
| T4-AS-05 | ECC-P-256 | Correct parameters, Certificate expiry (correct), Certificate subject (correct) |
| T4-AS-07 | Ed25519 | Certificate expiry (correct), Certificate subject (correct) |
| T4-AS-10 | RSA-3072 | Primitive, where the family is ambiguous, Certificate expiry (correct), Certificate subject (correct) |
| T4-AS-14 | RSA-3072 | Primitive, where the family is ambiguous, Key material type |
| T4-AS-15 | ECC-secp256k1 | Correct parameters, Key material type |
| T4-AS-18 | RSA-2048 | Primitive, where the family is ambiguous, Key material type |
| T4-AS-19 | ECC-P-256 | Primitive, where the family is ambiguous, Key material type |
| T4-AS-26 | RSA | Primitive, where the family is ambiguous |
| T4-AS-27 | DH-2048 | Correct parameters |
| T4-AS-34 | TLS-1.0 | Protocol version |
| T4-AS-35 | TLS-1.1 | Protocol version |
| T4-AS-36 | TLS-1.2 | Protocol version |

## Missed findings

| ID | File | Expected | Line |
|---|---|---|---|
| T1-PY-04 | `corpus/tier1/python/t1_hashes.py` | SHA3-256  | 9 |
| T1-JV-04 | `corpus/tier1/java/T1Hashes.java` | SHA3-256  | 13 |
| T2-PY-06 | `corpus/tier2/python/t2_dispatch_table.py` | MD5  | 6 |
| T2-PY-07 | `corpus/tier2/python/t2_dispatch_table.py` | SHA-256  | 7 |
| T2-JV-04 | `corpus/tier2/java/T2Enum.java` | SHA-1  | 6 |
| T2-JV-05 | `corpus/tier2/java/T2Enum.java` | SHA-256  | 7 |
| T3-PY-08 | `corpus/tier3/python/dependency_injection/wiring.py` | MD5  | 9 |
| T3-JV-06 | `corpus/tier3/java/dependency_injection/src/com/acme/audit/DigestProvider.java` | MD5  | 14 |
| T4-AS-02 | `corpus/tier4/assets/certs/api_gateway.pem` | SHA-256  | file |
| T4-AS-04 | `corpus/tier4/assets/certs/payments_legacy.crt` | SHA-1  | file |
| T4-AS-06 | `corpus/tier4/assets/certs/telemetry_ecdsa.pem` | SHA-256  | file |
| T4-AS-09 | `corpus/tier4/assets/certs/portal_fullchain.pem` | SHA-384  | file |
| T4-AS-11 | `corpus/tier4/assets/certs/portal_fullchain.pem` | SHA-256  | file |
| T4-AS-12 | `corpus/tier4/assets/certs/mainframe_gateway.der` | RSA {'key_size': 4096} | file |
| T4-AS-13 | `corpus/tier4/assets/certs/mainframe_gateway.der` | SHA-512  | file |
| T4-AS-16 | `corpus/tier4/assets/keys/backup_signing_encrypted.pem` | PBKDF2 {'hash': 'SHA-256'} | file |
| T4-AS-17 | `corpus/tier4/assets/keys/backup_signing_encrypted.pem` | AES {'key_size': 256, 'mode': 'CBC'} | file |
| T4-AS-20 | `corpus/tier4/assets/keystores/orders_keystore.p12` | AES {'key_size': 256, 'mode': 'CBC'} | file |
| T4-AS-21 | `corpus/tier4/assets/keystores/orders_keystore.p12` | PBKDF2 {'hash': 'SHA-256'} | file |
| T4-AS-24 | `corpus/tier4/assets/keystores/partner_truststore.jks` | RSA {'key_size': 1024} | file |
| T4-AS-25 | `corpus/tier4/assets/keystores/partner_truststore.jks` | SHA-1  | file |
| T4-AS-29 | `corpus/tier4/assets/ssh/sshd_config` | AES {'key_size': 128, 'mode': 'CBC'} | 10 |
| T4-AS-32 | `corpus/tier4/assets/ssh/ssh_host_rsa_key.pub` | RSA {'key_size': 2048} | file |
| T4-AS-33 | `corpus/tier4/assets/ssh/deploy_id_ed25519` | Ed25519  | file |
| T4-AS-37 | `corpus/tier4/assets/tls/nginx.conf` | TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256  | 21 |
| T4-AS-38 | `corpus/tier4/assets/tls/nginx.conf` | TLS_RSA_WITH_3DES_EDE_CBC_SHA  | 21 |
| T4-AS-39 | `corpus/tier4/assets/tls/nginx.conf` | TLS_RSA_WITH_AES_256_CBC_SHA  | 21 |
| T4-AS-40 | `corpus/tier4/assets/tls/application.yml` | TLS-1.1  | 13 |
| T4-AS-41 | `corpus/tier4/assets/tls/application.yml` | TLS-1.2  | 13 |
| T4-AS-42 | `corpus/tier4/assets/tls/application.yml` | TLS_RSA_WITH_AES_128_CBC_SHA  | 15 |
| T4-AS-43 | `corpus/tier4/assets/tls/application.yml` | TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384  | 16 |
| T4-AS-44 | `corpus/tier4/assets/tls/openssl.cnf` | RSA {'key_size': 1024} | 16 |
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
| T4-AS-60 | `corpus/tier4/assets/ipsec/swanctl.conf` | AES {'key_size': 256} | 7 |
| T4-AS-61 | `corpus/tier4/assets/ipsec/swanctl.conf` | HMAC {'hash': 'SHA-256'} | 7 |
| T4-AS-62 | `corpus/tier4/assets/ipsec/swanctl.conf` | DH {'key_size': 2048} | 7 |
| T4-AS-64 | `corpus/tier4/assets/ipsec/swanctl.conf` | X25519  | 21 |
| T4-AS-65 | `corpus/tier4/assets/ipsec/ipsec.conf` | 3DES  | 12 |
| T4-AS-66 | `corpus/tier4/assets/ipsec/ipsec.conf` | HMAC {'hash': 'SHA-1'} | 12 |
| T4-AS-67 | `corpus/tier4/assets/ipsec/ipsec.conf` | DH {'key_size': 1024} | 12 |
| T4-AS-68 | `corpus/tier4/assets/ipsec/ipsec.conf` | AES {'key_size': 128} | 13 |
| T5-PY-01 | `corpus/tier5/python/t5_string_assembly.py` | SHA-1  | 10 |
| T5-PY-02 | `corpus/tier5/python/t5_string_assembly.py` | MD5  | 14 |
| T5-PY-03 | `corpus/tier5/python/t5_dynamic_import.py` | RSA {'key_size': 2048} | 10 |
| T5-PY-04 | `corpus/tier5/python/t5_char_codes.py` | AES {'key_size': 128, 'mode': 'ECB'} | 11 |
| T5-PY-05 | `corpus/tier5/python/t5_handrolled_keystream.py` | RC4  | 13 |
| T5-PY-06 | `corpus/tier5/python/t5_handrolled_digest.py` | SHA-256  | 31 |
| T5-PY-07 | `corpus/tier5/python/t5_handrolled_pubkey.py` | RSA {'key_size': 1024} | 17 |
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
| T5-C-02 | `corpus/tier5/c/bin/meterd` | 3DES {'mode': 'CBC'} | file |
| T5-C-03 | `corpus/tier5/c/bin/meterd` | RSA {'key_size': 1024} | file |
| PQ-JV-05 | `corpus/pqc/java/FirmwareSignLms.java` | LMS  | 19 |
| PQ-JV-06 | `corpus/pqc/java/UpdateSignXmss.java` | XMSS  | 16 |
| PQ-AS-11 | `corpus/pqc/assets/tls/openssl_pq.cnf` | SecP384r1MLKEM1024  | 13 |
| PQ-AS-23 | `corpus/pqc/assets/keys/bootloader_lms_pub.pem` | LMS  | file |
| PQ-AS-24 | `corpus/pqc/assets/keys/update_xmss_pub.pem` | XMSS  | file |
| PQ-AS-25 | `corpus/pqc/assets/firmware/signing-policy.yaml` | LMS  | 7 |
| PQ-AS-26 | `corpus/pqc/assets/firmware/signing-policy.yaml` | XMSS  | 13 |
| PQ-AS-27 | `corpus/pqc/assets/firmware/signing-policy.yaml` | EC {'curve': 'P-384'} | 18 |
| T1-GO-01 | `corpus/tier1/go/hashes/main.go` | MD5  | 14 |
| T1-GO-03 | `corpus/tier1/go/hashes/main.go` | SHA-256  | 16 |
| T1-GO-04 | `corpus/tier1/go/hashes/main.go` | SHA3-256  | 17 |
| T1-GO-05 | `corpus/tier1/go/aes_gcm/main.go` | AES {'key_size': 256, 'mode': 'GCM'} | 12 |
| T1-GO-06 | `corpus/tier1/go/aes_cbc/main.go` | AES {'key_size': 128, 'mode': 'CBC'} | 12 |
| T1-GO-07 | `corpus/tier1/go/des/main.go` | 3DES {'mode': 'CBC'} | 13 |
| T1-GO-08 | `corpus/tier1/go/des/main.go` | DES {'mode': 'CBC'} | 21 |
| T1-GO-09 | `corpus/tier1/go/rc4/main.go` | RC4  | 10 |
| T1-GO-10 | `corpus/tier1/go/rsa/main.go` | RSA {'key_size': 2048} | 13 |
| T1-GO-13 | `corpus/tier1/go/x25519/main.go` | X25519  | 12 |
| T1-GO-15 | `corpus/tier1/go/mac_kdf/main.go` | HMAC {'hash': 'SHA-256'} | 13 |
| T1-GO-17 | `corpus/tier1/go/tls_config/main.go` | TLS-1.0  | 11 |
| T1-GO-18 | `corpus/tier1/go/tls_config/main.go` | TLS_RSA_WITH_3DES_EDE_CBC_SHA  | 13 |
| T1-GO-19 | `corpus/tier1/go/tls_config/main.go` | TLS_RSA_WITH_AES_128_CBC_SHA  | 14 |
| T1-GO-20 | `corpus/tier1/go/tls_config/main.go` | TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256  | 15 |
| T2-GO-06 | `corpus/tier2/go/block_factory/main.go` | 3DES {'mode': 'CBC'} | 10 |
| PQ-GO-02 | `corpus/pqc/go/tls_hybrid/main.go` | TLS-1.3  | 11 |
| PQ-GO-03 | `corpus/pqc/go/tls_hybrid/main.go` | X25519MLKEM768  | 12 |
| PQ-GO-04 | `corpus/pqc/go/tls_hybrid/main.go` | X25519  | 12 |
| T1-JS-01 | `corpus/tier1/javascript/t1_hashes.js` | MD5  | 5 |
| T1-JS-03 | `corpus/tier1/javascript/t1_hashes.js` | SHA-256  | 7 |
| T1-JS-04 | `corpus/tier1/javascript/t1_hashes.js` | SHA3-256  | 8 |
| T1-JS-05 | `corpus/tier1/javascript/t1_aes_cbc.js` | AES {'key_size': 128, 'mode': 'CBC'} | 6 |
| T1-JS-06 | `corpus/tier1/javascript/t1_aes_gcm.js` | AES {'key_size': 256, 'mode': 'GCM'} | 6 |
| T1-JS-07 | `corpus/tier1/javascript/t1_triple_des.js` | 3DES {'mode': 'CBC'} | 4 |
| T1-JS-08 | `corpus/tier1/javascript/t1_chacha.js` | ChaCha20-Poly1305  | 4 |
| T1-JS-09 | `corpus/tier1/javascript/t1_rsa.js` | RSA {'key_size': 2048} | 4 |
| T1-JS-10 | `corpus/tier1/javascript/t1_ec.js` | EC {'curve': 'P-256'} | 4 |
| T1-JS-11 | `corpus/tier1/javascript/t1_modern_curves.js` | Ed25519  | 4 |
| T1-JS-12 | `corpus/tier1/javascript/t1_modern_curves.js` | X25519  | 7 |
| T1-JS-13 | `corpus/tier1/javascript/t1_dh.js` | DH {'key_size': 2048} | 4 |
| T1-JS-16 | `corpus/tier1/javascript/t1_webcrypto.mjs` | RSA {'key_size': 3072} | 5 |
| T1-JS-17 | `corpus/tier1/javascript/t1_webcrypto.mjs` | SHA-1  | 9 |
| T2-TS-01 | `corpus/tier2/typescript/t2_config_object.ts` | 3DES {'mode': 'CBC'} | 5 |
| T2-TS-03 | `corpus/tier2/typescript/t2_env_default.ts` | RSA {'key_size': 1024} | 4 |
| T2-TS-04 | `corpus/tier2/typescript/t2_curve_table.ts` | EC {'curve': 'P-384'} | 4 |
| T2-TS-05 | `corpus/tier2/typescript/t2_wrapper.ts` | AES {'key_size': 128, 'mode': 'ECB'} | 9 |
| T2-TS-06 | `corpus/tier2/typescript/t2_template.ts` | AES {'key_size': 256, 'mode': 'GCM'} | 4 |
| T1-C-03 | `corpus/tier1/c/t1_digests.c` | SHA-256  | 17 |
| T1-C-04 | `corpus/tier1/c/t1_digests.c` | SHA3-256  | 18 |
| T1-C-05 | `corpus/tier1/c/t1_aes_ecb.c` | AES {'key_size': 128, 'mode': 'ECB'} | 12 |
| T1-C-07 | `corpus/tier1/c/t1_triple_des.c` | 3DES {'mode': 'CBC'} | 12 |
| T1-C-08 | `corpus/tier1/c/t1_chacha.c` | ChaCha20-Poly1305  | 12 |
| T1-C-12 | `corpus/tier1/c/t1_modern_curves.c` | Ed25519  | 6 |
| T1-C-13 | `corpus/tier1/c/t1_modern_curves.c` | X25519  | 9 |
| T1-C-17 | `corpus/tier1/c/t1_tls_ctx.c` | TLS-1.0  | 7 |
| T1-C-18 | `corpus/tier1/c/t1_tls_ctx.c` | TLS_RSA_WITH_3DES_EDE_CBC_SHA  | 8 |
| T1-C-19 | `corpus/tier1/c/t1_tls_ctx.c` | TLS_RSA_WITH_AES_128_CBC_SHA  | 8 |
| T1-C-20 | `corpus/tier1/c/t1_tls_ctx.c` | TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256  | 8 |
| T1-CS-01 | `corpus/tier1/csharp/Hashes/Program.cs` | MD5  | 9 |
| T1-CS-02 | `corpus/tier1/csharp/Hashes/Program.cs` | SHA-1  | 10 |
| T1-CS-03 | `corpus/tier1/csharp/Hashes/Program.cs` | SHA-256  | 11 |
| T1-CS-04 | `corpus/tier1/csharp/Hashes/Program.cs` | SHA3-256  | 12 |
| T1-CS-05 | `corpus/tier1/csharp/RsaSign/Program.cs` | RSA {'key_size': 2048} | 8 |
| T1-CS-06 | `corpus/tier1/csharp/EcdsaSign/Program.cs` | EC {'curve': 'P-256'} | 8 |
| T1-CS-07 | `corpus/tier1/csharp/KeyAgreement/Program.cs` | EC {'curve': 'P-384'} | 8 |
| T1-CS-08 | `corpus/tier1/csharp/AesCbc/Program.cs` | AES {'key_size': 128, 'mode': 'CBC'} | 8 |
| T1-CS-11 | `corpus/tier1/csharp/MacKdf/Program.cs` | HMAC {'hash': 'SHA-256'} | 8 |
| T2-C-01 | `corpus/tier2/c/t2_fetch_by_name.c` | AES {'key_size': 192, 'mode': 'CBC'} | 6 |
| T2-C-03 | `corpus/tier2/c/t2_macro_bits.c` | RSA {'key_size': 1024} | 7 |
| T2-C-04 | `corpus/tier2/c/t2_curve_index.c` | EC {'curve': 'P-521'} | 7 |
| T2-C-06 | `corpus/tier2/c/t2_cipher_struct.c` | 3DES {'mode': 'ECB'} | 10 |
| T2-CS-01 | `corpus/tier2/csharp/ConfigCipher/Program.cs` | AES {'key_size': 192, 'mode': 'CBC'} | 11 |
| T2-CS-03 | `corpus/tier2/csharp/DispatchTable/Program.cs` | MD5  | 9 |
| T2-CS-04 | `corpus/tier2/csharp/DispatchTable/Program.cs` | SHA-512  | 10 |
| T2-CS-05 | `corpus/tier2/csharp/KeyFactory/Program.cs` | RSA {'key_size': 1024} | 12 |
| T2-CS-06 | `corpus/tier2/csharp/CurveSwitch/Program.cs` | EC {'curve': 'P-521'} | 12 |
| MX-JV-2b | `corpus/mixed/java/BookingOptionsModule.java` | Ed25519  | 170 |
| MX-JV-3c | `corpus/mixed/java/OrderDefaultsModule.java` | ChaCha20-Poly1305  | 10 |
| MX-JV-3d | `corpus/mixed/java/OrderDefaultsModule.java` | SHA-512  | 269 |
| MX-GO-2b | `corpus/mixed/go/report_gateway/main.go` | DES {'mode': 'CBC'} | 125 |
| MX-GO-2d | `corpus/mixed/go/report_gateway/main.go` | 3DES {'mode': 'CBC'} | 171 |
| MX-GO-3b | `corpus/mixed/go/invoice_gateway/main.go` | RC4  | 198 |
| MX-JS-1a | `corpus/mixed/javascript/partner_routes.js` | AES {'key_size': 128, 'mode': 'CBC'} | 5 |
| MX-JS-1c | `corpus/mixed/javascript/partner_routes.js` | AES {'key_size': 256, 'mode': 'CTR'} | 8 |
| MX-JS-2a | `corpus/mixed/javascript/device_session.js` | SHA3-256  | 94 |
| MX-JS-2c | `corpus/mixed/javascript/device_session.js` | EC {'curve': 'P-521'} | 203 |
| MX-JS-2d | `corpus/mixed/javascript/device_session.js` | EC {'curve': 'P-384'} | 5 |
| MX-JS-2e | `corpus/mixed/javascript/device_session.js` | AES {'key_size': 256, 'mode': 'CTR'} | 68 |
| MX-TS-1a | `corpus/mixed/typescript/voucher_service.ts` | EC {'curve': 'P-256'} | 4 |
| MX-TS-1c | `corpus/mixed/typescript/voucher_service.ts` | AES {'key_size': 128, 'mode': 'ECB'} | 36 |
| MX-TS-1d | `corpus/mixed/typescript/voucher_service.ts` | RSA {'key_size': 2048} | 6 |
| MX-C-1d | `corpus/mixed/c/device_daemon.c` | X25519  | 58 |
| MX-C-2a | `corpus/mixed/c/policy_agent.c` | EC {'curve': 'P-384'} | 9 |
| MX-C-2b | `corpus/mixed/c/policy_agent.c` | AES {'key_size': 192, 'mode': 'CBC'} | 10 |
| MX-C-2c | `corpus/mixed/c/policy_agent.c` | 3DES {'mode': 'ECB'} | 66 |
| MX-C-2d | `corpus/mixed/c/policy_agent.c` | 3DES {'mode': 'CBC'} | 11 |
| MX-C-3a | `corpus/mixed/c/audit_daemon.c` | AES {'key_size': 192, 'mode': 'CBC'} | 8 |
| MX-C-3b | `corpus/mixed/c/audit_daemon.c` | 3DES {'mode': 'CBC'} | 300 |
| MX-C-3c | `corpus/mixed/c/audit_daemon.c` | AES {'key_size': 128, 'mode': 'ECB'} | 9 |
| SYS-GO-03 | `corpus/system/payments-platform/services/api-gateway/main.go` | SHA-256  | 13 |
| SYS-PY-04 | `corpus/system/payments-platform/services/settlement-worker/partner_ca.py` | SHA-1  | file |
| SYS-AR-01 | `corpus/system/payments-platform/services/ledger-service/build/libs/ledger-service.jar` | EC  | file |
| SYS-AR-02 | `corpus/system/payments-platform/services/ledger-service/build/libs/ledger-service.jar` | SHA-1  | file |
| SYS-AS-02 | `corpus/system/payments-platform/edge/nginx/gateway.conf` | TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384  | 9 |
| SYS-AS-03 | `corpus/system/payments-platform/edge/nginx/gateway.conf` | TLS_RSA_WITH_AES_128_CBC_SHA  | 9 |
| SYS-AS-05 | `corpus/system/payments-platform/edge/nginx/tls/gateway.crt` | SHA-256  | file |
| SYS-AS-07 | `corpus/system/payments-platform/deploy/k8s/gateway-ingress-tls.yaml` | EC {'curve': 'P-384'} | file |
| SYS-AS-08 | `corpus/system/payments-platform/deploy/k8s/gateway-ingress-tls.yaml` | SHA-384  | file |
| SYS-AS-09 | `corpus/system/payments-platform/infra/terraform/kms.tf` | EC {'curve': 'P-256'} | 6 |
| SYS-AS-10 | `corpus/system/payments-platform/infra/terraform/kms.tf` | RSA {'key_size': 2048} | 12 |
| SYS-AS-11 | `corpus/system/payments-platform/infra/terraform/kms.tf` | AES {'key_size': 256, 'mode': 'GCM'} | 15 |
| DC-GO-01 | `corpus/deadcode/go/legacy/main.go` | MD5  | 13 |
| DC-GO-02 | `corpus/deadcode/go/legacy/main.go` | RC4  | 18 |
| DC-JS-01 | `corpus/deadcode/javascript/dead_paths.js` | MD5  | 5 |
| DC-JS-02 | `corpus/deadcode/javascript/dead_paths.js` | 3DES {'mode': 'CBC'} | 10 |
| DC-C-02 | `corpus/deadcode/c/dead_branches.c` | 3DES {'mode': 'CBC'} | 11 |

## Detected with wrong or missing parameters

| ID | Family | Expected params | Reported params |
|---|---|---|---|
| T1-JV-08 | AES | `{"key_size": 128, "mode": "ECB"}` | `{"key_size": 128}` |
| T3-PY-01 | RSA | `{"key_size": 1024}` | `{}` |
| T3-PY-03 | AES | `{"key_size": 128, "mode": "GCM"}` | `{"mode": "GCM"}` |
| T3-PY-04 | RSA | `{"key_size": 1024}` | `{}` |
| T3-PY-05 | RSA | `{"key_size": 3072}` | `{}` |
| T3-PY-06 | AES | `{"key_size": 256, "mode": "CBC"}` | `{"mode": "CBC"}` |
| T3-PY-09 | HMAC | `{"hash": "SHA-256"}` | `{}` |
| T3-JV-01 | RSA | `{"key_size": 1024}` | `{}` |
| T3-JV-03 | AES | `{"key_size": 128, "mode": "GCM"}` | `{}` |
| T3-JV-04 | AES | `{"key_size": 256, "mode": "CBC"}` | `{"mode": "CBC"}; {}; {"mode": "CBC"}; {"mode": "CBC"}` |
| T4-AS-05 | EC | `{"curve": "P-256"}` | `{"key_size": 256}` |
| T4-AS-15 | EC | `{"curve": "secp256k1"}` | `{}` |
| T4-AS-27 | DH | `{"key_size": 2048}` | `{}` |
| T4-AS-59 | DH | `{"key_size": 1024}` | `{}` |
| T5-PY-09 | HMAC | `{"hash": "MD5"}` | `{}` |
| PQ-PY-01 | ML-KEM | `{"param_set": "768"}` | `{"param_set": "ML-KEM"}` |
| PQ-PY-02 | ML-DSA | `{"param_set": "65"}` | `{"param_set": "ML-DSA"}` |
| PQ-PY-04 | ML-KEM | `{"param_set": "768"}` | `{"param_set": "ML-KEM"}` |
| T1-GO-11 | EC | `{"curve": "P-256"}` | `{}` |
| T1-GO-14 | DSA | `{"key_size": 2048}` | `{}; {}; {}` |
| T1-GO-16 | PBKDF2 | `{"hash": "SHA-512"}` | `{"hash": "SHA-256"}; {"hash": "SHA-256"}` |
| T2-GO-02 | RSA | `{"key_size": 1024}` | `{}` |
| T2-GO-03 | EC | `{"curve": "P-384"}` | `{}` |
| T2-GO-04 | HMAC | `{"hash": "MD5"}` | `{}; {}` |
| T2-GO-05 | AES | `{"key_size": 192, "mode": "CTR"}` | `{}` |
| PQ-GO-01 | ML-KEM | `{"param_set": "1024"}` | `{"param_set": "ML-KEM"}` |
| T1-JS-15 | PBKDF2 | `{"hash": "SHA-512"}` | `{"hash": "SHA-256"}` |
| T2-TS-07 | HMAC | `{"hash": "MD5"}` | `{}` |
| T1-C-06 | AES | `{"key_size": 256, "mode": "GCM"}` | `{}` |
| T1-C-09 | RSA | `{"key_size": 1024}` | `{}` |
| T1-C-10 | RSA | `{"key_size": 3072}` | `{}` |
| T1-C-14 | DH | `{"key_size": 2048}` | `{}` |
| T1-C-16 | PBKDF2 | `{"hash": "SHA-1"}` | `{"hash": "SHA-256"}` |
| T1-CS-09 | AES | `{"key_size": 256, "mode": "GCM"}` | `{}` |
| T1-CS-10 | 3DES | `{"mode": "CBC"}` | `{}` |
| T1-CS-12 | PBKDF2 | `{"hash": "SHA-512"}` | `{"hash": "SHA-256"}` |
| T1-CS-13 | DSA | `{"key_size": 2048}` | `{}` |
| T2-C-05 | HMAC | `{"hash": "MD5"}` | `{}` |
| MX-PY-1b | PBKDF2 | `{"hash": "SHA-512"}` | `{"hash": "SHA-256"}` |
| MX-PY-1c | HMAC | `{"hash": "SHA-512"}` | `{"hash": "SHA-256"}` |
| MX-PY-1d | AES | `{"key_size": 192, "mode": "CTR"}` | `{"key_size": 128}` |
| MX-PY-2b | ML-DSA | `{"param_set": "65"}` | `{"param_set": "ML-DSA"}` |
| MX-PY-2c | DH | `{"key_size": 1024}` | `{}` |
| MX-PY-3b | HMAC | `{"hash": "SHA-512"}` | `{"hash": "SHA-256"}` |
| MX-PY-3c | EC | `{"curve": "P-256"}` | `{"curve": "P-521"}` |
| MX-JV-1c | DH | `{"key_size": 2048}` | `{"key_size": 3072}` |
| MX-JV-1d | AES | `{"key_size": 192, "mode": "ECB"}` | `{"key_size": 192}` |
| MX-JV-2c | PBKDF2 | `{"hash": "SHA-512"}` | `{"hash": "SHA-256"}; {"hash": "SHA-256"}` |
| MX-JV-3b | 3DES | `{"mode": "ECB"}` | `{}` |
| MX-GO-1a | PBKDF2 | `{"hash": "SHA-512"}` | `{}` |
| MX-GO-1b | ML-KEM | `{"param_set": "768"}` | `{"param_set": "ML-KEM"}` |
| MX-GO-1c | RSA | `{"key_size": 1024}` | `{}` |
| MX-GO-1d | RSA | `{"key_size": 2048}` | `{}` |
| MX-GO-2c | PBKDF2 | `{"hash": "SHA-1"}` | `{"hash": "SHA-256"}` |
| MX-GO-3a | RSA | `{"key_size": 2048}` | `{}` |
| MX-GO-3c | HMAC | `{"hash": "SHA-1"}` | `{}` |
| MX-JS-1b | HMAC | `{"hash": "SHA-512"}` | `{}` |
| MX-JS-2b | PBKDF2 | `{"hash": "SHA-512"}` | `{"hash": "SHA-256"}` |
| MX-TS-1b | HMAC | `{"hash": "SHA-512"}` | `{"hash": "SHA-256"}` |
| MX-C-1c | HMAC | `{"hash": "MD5"}` | `{}` |
| MX-C-1e | HMAC | `{"hash": "SHA-512"}` | `{}` |
| MX-C-3d | DH | `{"key_size": 3072}` | `{}` |
| SYS-GO-01 | RSA | `{"key_size": 2048}` | `{}` |
| SYS-GO-02 | HMAC | `{"hash": "SHA-1"}` | `{"hash": "SHA-256"}; {"hash": "SHA-256"}` |
| SYS-PY-02 | HMAC | `{"hash": "SHA-1"}` | `{"hash": "SHA-256"}; {"hash": "SHA-512"}; {"hash": "SHA-256"}` |
| SYS-JV-01 | EC | `{"curve": "P-256"}` | `{}` |
| SYS-AS-06 | RSA | `{"key_size": 2048}` | `{}` |

## False positives

| File | Reported family | Lines | Negative control? |
|---|---|---|---|
| `corpus/mixed/c/audit_daemon.c` | ML-DSA | 97, 325 | no |
| `corpus/mixed/c/audit_daemon.c` | PBKDF2 | 19, 283 | no |
| `corpus/mixed/c/device_daemon.c` | ML-DSA | 181 | no |
| `corpus/mixed/c/device_daemon.c` | ML-KEM | 143, 312 | no |
| `corpus/mixed/c/policy_agent.c` | ML-KEM | 54 | no |
| `corpus/mixed/go/invoice_gateway/main.go` | DH | 163 | no |
| `corpus/mixed/go/invoice_gateway/main.go` | ML-KEM | 266 | no |
| `corpus/mixed/java/OrderDefaultsModule.java` | ML-DSA | 70 | no |
| `corpus/mixed/java/OrderDefaultsModule.java` | PBKDF2 | 59 | no |
| `corpus/mixed/java/VoucherProfileModule.java` | HMAC | 170, 311 | no |
| `corpus/mixed/java/VoucherProfileModule.java` | PBKDF2 | 166, 500 | no |
| `corpus/mixed/javascript/device_session.js` | DSA | 299 | no |
| `corpus/mixed/javascript/device_session.js` | ML-DSA | 222 | no |
| `corpus/mixed/javascript/partner_routes.js` | DH | 17, 253 | no |
| `corpus/mixed/javascript/partner_routes.js` | ML-DSA | 128 | no |
| `corpus/mixed/javascript/partner_routes.js` | ML-KEM | 237 | no |
| `corpus/mixed/python/invoice_service.py` | HMAC | 139 | no |
| `corpus/mixed/python/metric_service.py` | DSA | 242, 252 | no |
| `corpus/mixed/python/order_jobs.py` | ML-KEM | 163, 302 | no |
| `corpus/mixed/python/order_jobs.py` | PBKDF2 | 329 | no |
| `corpus/mixed/typescript/voucher_service.ts` | DH | 106, 215, 268 | no |
| `corpus/mixed/typescript/voucher_service.ts` | ML-KEM | 32 | no |
| `corpus/mixed/typescript/voucher_service.ts` | PBKDF2 | 180 | no |
| `corpus/negatives/c/n_strings.c` | MD5 | 6 | yes |
| `corpus/negatives/c/n_strings.c` | ML-KEM | 6 | yes |
| `corpus/negatives/javascript/n_strings.js` | ML-KEM | 2 | yes |
| `corpus/negatives/javascript/n_strings.js` | SHA-1 | 10 | yes |
| `corpus/system/payments-platform/services/api-gateway/bin/api-gateway` | DH | 190, 208, 246, 348, 635, 640, 699, 704, 1461, 1477, 1547, 1633, 1647, 1912, 2084, 2157, 2180, 2268, 2618, 2842, 2989, 3101, 3531, 3691, 3827, 4087, 4654, 4675, 4773, 4774, 5013, 5217, 5235, 5239, 5246, 5251, 5263, 5264, 5453, 6021, 6030, 6065, 6342, 6458, 6909, 6938, 7065, 7072, 7237, 7239, 7245, 7359, 7405, 7459, 7786, 7840, 8649, 9582, 9677, 9694, 9718, 9736, 9888, 9896, 9924, 9926, 9938, 10393, 10480, 10673, 10688, 10944, 11574, 11699, 11717, 11763, 12119, 12124, 12345, 12417, 12492, 12550, 12657, 12687, 12746, 12911, 12934, 13017, 49070, 50098, 53217 | no |
| `corpus/tier5/c/bin/meterd` | DH | 65 | no |

## Unrecognized names (not scored, review manually)

- `corpus/calibration/tier1/java/Cal1037ShipmentSettings.java` line 5: qci-category-1
- `corpus/calibration/tier1/java/Cal1038MemberOptions.java` line 9: qci-category-2
- `corpus/calibration/tier1/java/Cal1039PayloadDefaults.java` line 13: qci-category-3
- `corpus/calibration/tier1/javascript/cal_sha3256_034.js` line 9: qci-category-4
- `corpus/calibration/tier1/javascript/cal_sha3256_035.js` line 9: qci-category-5
- `corpus/calibration/tier1/javascript/cal_sha3256_036.js` line 5: qci-category-6
- `corpus/calibration/tier1/python/cal_sha3256_039.py` line 6: qci-category-7
- `corpus/calibration/tier1/python/cal_sha3256_040.py` line 6: qci-category-8
- `corpus/calibration/tier1/python/cal_sha3256_041.py` line 17: qci-category-9
- `corpus/mixed/c/audit_daemon.c` line 218: qci-category-10
- `corpus/mixed/c/audit_daemon.c` line 315: qci-category-11
- `corpus/mixed/go/invoice_gateway/main.go` line 207: qci-category-12
- `corpus/mixed/go/invoice_gateway/main.go` line 230: qci-category-13
- `corpus/mixed/javascript/device_session.js` line 94: qci-category-14
- `corpus/mixed/javascript/partner_routes.js` line 263: qci-category-15
- `corpus/mixed/python/invoice_service.py` line 52: qci-category-16
- `corpus/mixed/python/order_jobs.py` line 33: qci-category-17
- `corpus/negatives/go/strings/main.go` line 11: qci-category-19
- `corpus/pqc/assets/keys/attestation_signer.pem` line 1: qci-category-23
- `corpus/pqc/assets/ssh/sshd_config_pq` line 6: qci-category-24
- `corpus/pqc/assets/ssh/sshd_config_pq` line 6: qci-category-25
- `corpus/pqc/assets/ssh/sshd_config_pq` line 6: qci-category-26
- `corpus/pqc/assets/ssh/sshd_config_pq` line 7: qci-category-27
- `corpus/pqc/assets/tls/nginx_pq.conf` line 14: qci-category-29
- `corpus/pqc/assets/tls/openssl_pq.cnf` line 13: qci-category-31
- `corpus/pqc/assets/tls/openssl_pq.cnf` line 13: qci-category-32
- `corpus/pqc/java/FirmwareSignLms.java` line 18: qci-category-33
- `corpus/pqc/java/PqParamSpec.java` line 9: qci-category-34
- `corpus/pqc/java/PqSignature.java` line 11: qci-category-35
- `corpus/pqc/java/UpdateSignXmss.java` line 15: qci-category-36
- `corpus/system/payments-platform/edge/nginx/gateway.conf` line 9: qci-category-39
- `corpus/system/payments-platform/edge/nginx/gateway.conf` line 9: qci-category-40
- `corpus/system/payments-platform/edge/nginx/tls/gateway.key` line 1: qci-category-42
- `corpus/system/payments-platform/services/api-gateway/bin/api-gateway` line 12895: qci-category-43
- `corpus/system/payments-platform/services/api-gateway/bin/api-gateway` line 12895: qci-category-44
- `corpus/system/payments-platform/services/api-gateway/bin/api-gateway` line 12895: qci-category-45
- `corpus/system/payments-platform/services/api-gateway/bin/api-gateway` line 14665: qci-category-46
- `corpus/system/payments-platform/services/api-gateway/bin/api-gateway` line 14666: qci-category-47
- `corpus/system/payments-platform/services/api-gateway/bin/api-gateway` line 14666: qci-category-48
- `corpus/system/payments-platform/services/api-gateway/bin/api-gateway` line 14670: qci-category-49
- `corpus/system/payments-platform/services/api-gateway/bin/api-gateway` line 14670: qci-category-50
- `corpus/system/payments-platform/services/api-gateway/bin/api-gateway` line 16796: qci-category-51
- `corpus/tier1/java/T1Hashes.java` line 13: qci-category-53
- `corpus/tier1/javascript/t1_hashes.js` line 8: qci-category-54
- `corpus/tier1/python/t1_hashes.py` line 9: qci-category-55
- `corpus/tier4/assets/keys/billing_service.pem` line 1: qci-category-62
- `corpus/tier4/assets/keys/treasury_hot_wallet.key` line 1: qci-category-63
- `corpus/tier4/assets/ssh/sshd_config` line 8: qci-category-64
- `corpus/tier4/assets/ssh/sshd_config` line 9: qci-category-65
- `corpus/tier4/assets/ssh/sshd_config` line 9: qci-category-66
- `corpus/tier4/assets/ssh/sshd_config` line 10: qci-category-67
- `corpus/tier4/assets/ssh/sshd_config` line 10: qci-category-68
- `corpus/tier4/assets/ssh/sshd_config` line 11: qci-category-69
- `corpus/tier4/assets/tls/haproxy.cfg` line 7: qci-category-70
- `corpus/tier4/assets/tls/httpd-ssl.conf` line 14: qci-category-72
- `corpus/tier4/assets/tls/nginx.conf` line 20: qci-category-75
- `corpus/tier4/assets/tls/nginx.conf` line 20: qci-category-76
- `corpus/tier4/assets/tls/nginx.conf` line 21: qci-category-77
- `corpus/tier4/assets/tls/nginx.conf` line 21: qci-category-78
- `corpus/tier4/assets/tls/nginx.conf` line 21: qci-category-79

## Crypto libraries (dependency manifests)

- Found in the right manifest: **7/28** (25.0%); found anywhere, including with no location: 7/28
- Direct dependencies: 29.2%; transitive (lockfile): 0.0%
- Versions correct, of found libraries the manifest pins (none reported counts as not correct): 0.0%
- PQC-capability verdicts (where the scanner gives one): 66.7% right of 6
- False positives: 0

Wrong PQC verdicts: cryptography (range) in python-signer/pyproject.toml: reported not PQC-capable; org.bouncycastle:bcprov-jdk18on, bctls-jdk18on 1.80 in java-pq/build.gradle: reported not PQC-capable

Missed, and the declared version has no ML-KEM/ML-DSA: pycryptodome 3.19.0 (python-billing); PyJWT 2.8.0 (python-billing); jsonwebtoken 9.0.2 (node-api); crypto-js 4.2.0 (node-api); @noble/curves 2.0.1 (node-api); jws 3.2.3 (node-api); jwa 1.4.2 (node-api); openssl 1.1.1w (c-agent); cryptography 42.0.5 (settlement-worker); org.bouncycastle:bcprov-jdk18on 1.77 (ledger-service)

Missed, with a support problem: crypto-js 4.2.0: unmaintained: development discontinued upstream; openssl 1.1.1w: end of life since 2023-09-11

| Manifest | Library | Declared | Scope | Found | Version |
|---|---|---|---|---|---|
| `python-billing/requirements.txt` | cryptography | 41.0.7 | direct | yes | not reported |
| `python-billing/requirements.txt` | pycryptodome | 3.19.0 | direct | no | n/a |
| `python-billing/requirements.txt` | pyOpenSSL | 23.3.0 | direct | yes | not reported |
| `python-billing/requirements.txt` | PyJWT | 2.8.0 | direct | no | n/a |
| `python-billing/requirements.txt` | paramiko | 3.4.0 | direct | no | n/a |
| `python-billing/requirements.txt` | bcrypt | 4.1.2 | direct | no | n/a |
| `python-signer/pyproject.toml` | cryptography | range | direct | yes | n/a |
| `python-signer/pyproject.toml` | liboqs-python | 0.16.0 | direct | yes | not reported |
| `java-gateway/pom.xml` | org.bouncycastle:bcprov-jdk15on, bcpkix-jdk15on | 1.70 | direct | yes | not reported |
| `java-gateway/pom.xml` | com.nimbusds:nimbus-jose-jwt | 9.37.3 | direct | no | n/a |
| `java-gateway/pom.xml` | io.jsonwebtoken:jjwt-api | 0.12.5 | direct | no | n/a |
| `java-pq/build.gradle` | org.bouncycastle:bcprov-jdk18on, bctls-jdk18on | 1.80 | direct | yes | not reported |
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
| `go-service/go.mod` | github.com/cloudflare/circl | 1.6.1 | direct | yes | not reported |
| `go-service/go.mod` | github.com/golang-jwt/jwt/v5 | 5.2.1 | direct | no | n/a |
| `c-agent/conanfile.txt` | openssl | 1.1.1w | direct | no | n/a |
| `c-agent/conanfile.txt` | libsodium | 1.0.18 | direct | no | n/a |
| `corpus/system/payments-platform/services/settlement-worker/requirements.txt` | cryptography | 42.0.5 | direct | no | n/a |
| `corpus/system/payments-platform/services/ledger-service/build.gradle` | org.bouncycastle:bcprov-jdk18on | 1.77 | direct | no | n/a |

## Per-finding detail

| ID | Family | Detected | At primary site | Params | Line | Quantum flag |
|---|---|---|---|---|---|---|
| T1-PY-01 | MD5 | yes | yes | yes | yes | n/a |
| T1-PY-02 | SHA-1 | yes | yes | yes | yes | n/a |
| T1-PY-03 | SHA-256 | yes | yes | yes | yes | n/a |
| T1-PY-04 | SHA3-256 | NO | NO | n/a | n/a | n/a |
| T1-PY-05 | RSA | yes | yes | yes | yes | n/a |
| T1-PY-06 | EC | yes | yes | yes | yes | n/a |
| T1-PY-07 | DSA | yes | yes | yes | yes | n/a |
| T1-PY-08 | AES | yes | yes | yes | yes | n/a |
| T1-PY-09 | AES | yes | yes | yes | yes | n/a |
| T1-PY-10 | 3DES | yes | yes | yes | yes | n/a |
| T1-PY-11 | ChaCha20-Poly1305 | yes | yes | yes | yes | n/a |
| T1-PY-12 | Ed25519 | yes | yes | yes | yes | n/a |
| T1-PY-13 | X25519 | yes | yes | yes | yes | n/a |
| T1-PY-14 | DH | yes | yes | yes | yes | n/a |
| T1-PY-15 | HMAC | yes | yes | yes | yes | n/a |
| T1-PY-16 | PBKDF2 | yes | yes | yes | yes | n/a |
| T1-JV-01 | MD5 | yes | yes | yes | yes | n/a |
| T1-JV-02 | SHA-1 | yes | yes | yes | yes | n/a |
| T1-JV-03 | SHA-256 | yes | yes | yes | yes | n/a |
| T1-JV-04 | SHA3-256 | NO | NO | n/a | n/a | n/a |
| T1-JV-05 | RSA | yes | yes | yes | yes | n/a |
| T1-JV-06 | EC | yes | yes | yes | yes | n/a |
| T1-JV-07 | DSA | yes | yes | yes | yes | n/a |
| T1-JV-08 | AES | yes | yes | NO | yes | n/a |
| T1-JV-09 | AES | yes | yes | yes | yes | n/a |
| T1-JV-10 | DES | yes | yes | yes | yes | n/a |
| T1-JV-11 | 3DES | yes | yes | yes | yes | n/a |
| T1-JV-12 | Ed25519 | yes | yes | yes | yes | n/a |
| T1-JV-13 | X25519 | yes | yes | yes | yes | n/a |
| T1-JV-14 | DH | yes | yes | yes | yes | n/a |
| T1-JV-15 | HMAC | yes | yes | yes | yes | n/a |
| T1-JV-16 | PBKDF2 | yes | yes | yes | yes | n/a |
| T2-PY-01 | SHA-1 | yes | yes | yes | yes | n/a |
| T2-PY-02 | RSA | yes | yes | yes | yes | n/a |
| T2-PY-03 | AES | yes | NO | yes | NO | n/a |
| T2-PY-04 | SHA-1 | yes | yes | yes | yes | n/a |
| T2-PY-05 | AES | yes | yes | yes | yes | n/a |
| T2-PY-06 | MD5 | NO | NO | n/a | n/a | n/a |
| T2-PY-07 | SHA-256 | NO | NO | n/a | n/a | n/a |
| T2-PY-08 | HMAC | yes | yes | yes | yes | n/a |
| T2-PY-09 | EC | yes | yes | yes | yes | n/a |
| T2-JV-01 | 3DES | yes | yes | yes | yes | n/a |
| T2-JV-02 | RSA | yes | NO | yes | yes | n/a |
| T2-JV-03 | MD5 | yes | yes | yes | yes | n/a |
| T2-JV-04 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T2-JV-05 | SHA-256 | NO | NO | n/a | n/a | n/a |
| T2-JV-06 | AES | yes | yes | yes | yes | n/a |
| T2-JV-07 | DSA | yes | yes | yes | yes | n/a |
| T2-JV-08 | EC | yes | yes | yes | yes | n/a |
| T3-PY-01 | RSA | yes | yes | NO | yes | n/a |
| T3-PY-02 | SHA-1 | yes | NO | yes | yes | n/a |
| T3-PY-03 | AES | yes | yes | NO | yes | n/a |
| T3-PY-04 | RSA | yes | NO | NO | yes | n/a |
| T3-PY-05 | RSA | yes | NO | NO | yes | n/a |
| T3-PY-06 | AES | yes | yes | NO | yes | n/a |
| T3-PY-07 | ChaCha20-Poly1305 | yes | yes | yes | yes | n/a |
| T3-PY-08 | MD5 | NO | NO | n/a | n/a | n/a |
| T3-PY-09 | HMAC | yes | yes | NO | yes | n/a |
| T3-JV-01 | RSA | yes | yes | NO | yes | n/a |
| T3-JV-02 | SHA-1 | yes | yes | yes | yes | n/a |
| T3-JV-03 | AES | yes | yes | NO | yes | n/a |
| T3-JV-04 | AES | yes | yes | NO | yes | n/a |
| T3-JV-05 | 3DES | yes | yes | yes | yes | n/a |
| T3-JV-06 | MD5 | NO | NO | n/a | n/a | n/a |
| T3-JV-07 | HMAC | yes | NO | yes | yes | yes |
| T4-AS-01 | RSA | yes | yes | yes | n/a | n/a |
| T4-AS-02 | SHA-256 | NO | NO | n/a | n/a | n/a |
| T4-AS-03 | RSA | yes | yes | yes | n/a | n/a |
| T4-AS-04 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T4-AS-05 | EC | yes | yes | NO | n/a | n/a |
| T4-AS-06 | SHA-256 | NO | NO | n/a | n/a | n/a |
| T4-AS-07 | Ed25519 | yes | yes | yes | n/a | n/a |
| T4-AS-08 | EC | yes | yes | yes | n/a | n/a |
| T4-AS-09 | SHA-384 | NO | NO | n/a | n/a | n/a |
| T4-AS-10 | RSA | yes | yes | yes | n/a | n/a |
| T4-AS-11 | SHA-256 | NO | NO | n/a | n/a | n/a |
| T4-AS-12 | RSA | NO | NO | n/a | n/a | n/a |
| T4-AS-13 | SHA-512 | NO | NO | n/a | n/a | n/a |
| T4-AS-14 | RSA | yes | yes | yes | n/a | n/a |
| T4-AS-15 | EC | yes | yes | NO | n/a | n/a |
| T4-AS-16 | PBKDF2 | NO | NO | n/a | n/a | n/a |
| T4-AS-17 | AES | NO | NO | n/a | n/a | n/a |
| T4-AS-18 | RSA | yes | yes | yes | NO | n/a |
| T4-AS-19 | EC | yes | yes | yes | NO | n/a |
| T4-AS-20 | AES | NO | NO | n/a | n/a | n/a |
| T4-AS-21 | PBKDF2 | NO | NO | n/a | n/a | n/a |
| T4-AS-24 | RSA | NO | NO | n/a | n/a | n/a |
| T4-AS-25 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T4-AS-26 | RSA | yes | yes | yes | yes | n/a |
| T4-AS-27 | DH | yes | yes | NO | yes | n/a |
| T4-AS-28 | X25519 | yes | yes | yes | yes | n/a |
| T4-AS-29 | AES | NO | NO | n/a | n/a | n/a |
| T4-AS-30 | ChaCha20-Poly1305 | yes | yes | yes | yes | n/a |
| T4-AS-31 | HMAC | yes | yes | yes | yes | n/a |
| T4-AS-32 | RSA | NO | NO | n/a | n/a | n/a |
| T4-AS-33 | Ed25519 | NO | NO | n/a | n/a | n/a |
| T4-AS-34 | TLS-1.0 | yes | yes | yes | yes | n/a |
| T4-AS-35 | TLS-1.1 | yes | yes | yes | yes | n/a |
| T4-AS-36 | TLS-1.2 | yes | yes | yes | yes | n/a |
| T4-AS-37 | TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 | NO | NO | n/a | n/a | n/a |
| T4-AS-38 | TLS_RSA_WITH_3DES_EDE_CBC_SHA | NO | NO | n/a | n/a | n/a |
| T4-AS-39 | TLS_RSA_WITH_AES_256_CBC_SHA | NO | NO | n/a | n/a | n/a |
| T4-AS-40 | TLS-1.1 | NO | NO | n/a | n/a | n/a |
| T4-AS-41 | TLS-1.2 | NO | NO | n/a | n/a | n/a |
| T4-AS-42 | TLS_RSA_WITH_AES_128_CBC_SHA | NO | NO | n/a | n/a | n/a |
| T4-AS-43 | TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 | NO | NO | n/a | n/a | n/a |
| T4-AS-44 | RSA | NO | NO | n/a | n/a | n/a |
| T4-AS-45 | SHA-1 | yes | yes | yes | yes | n/a |
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
| T4-AS-59 | DH | yes | yes | NO | yes | n/a |
| T4-AS-60 | AES | NO | NO | n/a | n/a | n/a |
| T4-AS-61 | HMAC | NO | NO | n/a | n/a | n/a |
| T4-AS-62 | DH | NO | NO | n/a | n/a | n/a |
| T4-AS-63 | ChaCha20-Poly1305 | yes | yes | yes | yes | n/a |
| T4-AS-64 | X25519 | NO | NO | n/a | n/a | n/a |
| T4-AS-65 | 3DES | NO | NO | n/a | n/a | n/a |
| T4-AS-66 | HMAC | NO | NO | n/a | n/a | n/a |
| T4-AS-67 | DH | NO | NO | n/a | n/a | n/a |
| T4-AS-68 | AES | NO | NO | n/a | n/a | n/a |
| T5-PY-01 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T5-PY-02 | MD5 | NO | NO | n/a | n/a | n/a |
| T5-PY-03 | RSA | NO | NO | n/a | n/a | n/a |
| T5-PY-04 | AES | NO | NO | n/a | n/a | n/a |
| T5-PY-05 | RC4 | NO | NO | n/a | n/a | n/a |
| T5-PY-06 | SHA-256 | NO | NO | n/a | n/a | n/a |
| T5-PY-07 | RSA | NO | NO | n/a | n/a | n/a |
| T5-PY-08 | SHA-1 | yes | yes | yes | n/a | n/a |
| T5-PY-09 | HMAC | yes | yes | NO | n/a | n/a |
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
| T5-C-01 | MD5 | yes | yes | yes | n/a | n/a |
| T5-C-02 | 3DES | NO | NO | n/a | n/a | n/a |
| T5-C-03 | RSA | NO | NO | n/a | n/a | n/a |
| PQ-PY-01 | ML-KEM | yes | yes | NO | yes | n/a |
| PQ-PY-02 | ML-DSA | yes | yes | NO | yes | n/a |
| PQ-PY-03 | X25519 | yes | yes | yes | yes | n/a |
| PQ-PY-04 | ML-KEM | yes | yes | NO | yes | n/a |
| PQ-PY-05 | ML-KEM | yes | yes | yes | yes | yes |
| PQ-PY-06 | EC | yes | yes | yes | yes | n/a |
| PQ-JV-01 | ML-KEM | yes | yes | yes | yes | yes |
| PQ-JV-02 | ML-DSA | yes | yes | yes | yes | yes |
| PQ-JV-03 | ML-DSA | yes | yes | yes | yes | yes |
| PQ-JV-04 | EC | yes | yes | yes | yes | n/a |
| PQ-JV-05 | LMS | NO | NO | n/a | n/a | n/a |
| PQ-JV-06 | XMSS | NO | NO | n/a | n/a | n/a |
| PQ-AS-01 | ML-DSA | yes | yes | yes | n/a | yes |
| PQ-AS-02 | ML-DSA | yes | yes | yes | n/a | yes |
| PQ-AS-03 | ML-DSA | yes | yes | yes | n/a | yes |
| PQ-AS-04 | RSA | yes | yes | yes | n/a | n/a |
| PQ-AS-05 | SHA-256 | yes | yes | yes | n/a | n/a |
| PQ-AS-06 | ML-KEM | yes | yes | yes | n/a | yes |
| PQ-AS-07 | ML-DSA | yes | yes | yes | n/a | yes |
| PQ-AS-08 | TLS-1.3 | yes | yes | yes | yes | n/a |
| PQ-AS-09 | X25519MLKEM768 | yes | yes | yes | yes | yes |
| PQ-AS-10 | X25519 | yes | yes | yes | yes | n/a |
| PQ-AS-11 | SecP384r1MLKEM1024 | NO | NO | n/a | n/a | n/a |
| PQ-AS-12 | X25519MLKEM768 | yes | yes | yes | yes | yes |
| PQ-AS-13 | EC | yes | yes | yes | yes | n/a |
| PQ-AS-14 | TLS-1.3 | yes | yes | yes | yes | n/a |
| PQ-AS-15 | X25519MLKEM768 | yes | yes | yes | yes | yes |
| PQ-AS-16 | sntrup761x25519 | yes | yes | yes | yes | n/a |
| PQ-AS-17 | X25519 | yes | yes | yes | yes | n/a |
| PQ-AS-18 | Ed25519 | yes | yes | yes | yes | n/a |
| PQ-AS-19 | ChaCha20-Poly1305 | yes | yes | yes | yes | n/a |
| PQ-AS-20 | TLS-1.3 | yes | yes | yes | yes | n/a |
| PQ-AS-21 | X25519 | yes | yes | yes | yes | n/a |
| PQ-AS-22 | EC | yes | yes | yes | yes | n/a |
| PQ-AS-23 | LMS | NO | NO | n/a | n/a | n/a |
| PQ-AS-24 | XMSS | NO | NO | n/a | n/a | n/a |
| PQ-AS-25 | LMS | NO | NO | n/a | n/a | n/a |
| PQ-AS-26 | XMSS | NO | NO | n/a | n/a | n/a |
| PQ-AS-27 | EC | NO | NO | n/a | n/a | n/a |
| T1-GO-01 | MD5 | NO | NO | n/a | n/a | n/a |
| T1-GO-02 | SHA-1 | yes | yes | yes | yes | n/a |
| T1-GO-03 | SHA-256 | NO | NO | n/a | n/a | n/a |
| T1-GO-04 | SHA3-256 | NO | NO | n/a | n/a | n/a |
| T1-GO-05 | AES | NO | NO | n/a | n/a | n/a |
| T1-GO-06 | AES | NO | NO | n/a | n/a | n/a |
| T1-GO-07 | 3DES | NO | NO | n/a | n/a | n/a |
| T1-GO-08 | DES | NO | NO | n/a | n/a | n/a |
| T1-GO-09 | RC4 | NO | NO | n/a | n/a | n/a |
| T1-GO-10 | RSA | NO | NO | n/a | n/a | n/a |
| T1-GO-11 | EC | yes | yes | NO | yes | n/a |
| T1-GO-12 | Ed25519 | yes | yes | yes | yes | n/a |
| T1-GO-13 | X25519 | NO | NO | n/a | n/a | n/a |
| T1-GO-14 | DSA | yes | yes | NO | yes | n/a |
| T1-GO-15 | HMAC | NO | NO | n/a | n/a | n/a |
| T1-GO-16 | PBKDF2 | yes | yes | NO | yes | n/a |
| T1-GO-17 | TLS-1.0 | NO | NO | n/a | n/a | n/a |
| T1-GO-18 | TLS_RSA_WITH_3DES_EDE_CBC_SHA | NO | NO | n/a | n/a | n/a |
| T1-GO-19 | TLS_RSA_WITH_AES_128_CBC_SHA | NO | NO | n/a | n/a | n/a |
| T1-GO-20 | TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 | NO | NO | n/a | n/a | n/a |
| T2-GO-01 | SHA-1 | yes | yes | yes | yes | n/a |
| T2-GO-02 | RSA | yes | yes | NO | yes | n/a |
| T2-GO-03 | EC | yes | yes | NO | yes | n/a |
| T2-GO-04 | HMAC | yes | yes | NO | yes | n/a |
| T2-GO-05 | AES | yes | yes | NO | yes | n/a |
| T2-GO-06 | 3DES | NO | NO | n/a | n/a | n/a |
| PQ-GO-01 | ML-KEM | yes | yes | NO | yes | n/a |
| PQ-GO-02 | TLS-1.3 | NO | NO | n/a | n/a | n/a |
| PQ-GO-03 | X25519MLKEM768 | NO | NO | n/a | n/a | n/a |
| PQ-GO-04 | X25519 | NO | NO | n/a | n/a | n/a |
| T1-JS-01 | MD5 | NO | NO | n/a | n/a | n/a |
| T1-JS-02 | SHA-1 | yes | yes | yes | yes | n/a |
| T1-JS-03 | SHA-256 | NO | NO | n/a | n/a | n/a |
| T1-JS-04 | SHA3-256 | NO | NO | n/a | n/a | n/a |
| T1-JS-05 | AES | NO | NO | n/a | n/a | n/a |
| T1-JS-06 | AES | NO | NO | n/a | n/a | n/a |
| T1-JS-07 | 3DES | NO | NO | n/a | n/a | n/a |
| T1-JS-08 | ChaCha20-Poly1305 | NO | NO | n/a | n/a | n/a |
| T1-JS-09 | RSA | NO | NO | n/a | n/a | n/a |
| T1-JS-10 | EC | NO | NO | n/a | n/a | n/a |
| T1-JS-11 | Ed25519 | NO | NO | n/a | n/a | n/a |
| T1-JS-12 | X25519 | NO | NO | n/a | n/a | n/a |
| T1-JS-13 | DH | NO | NO | n/a | n/a | n/a |
| T1-JS-14 | HMAC | yes | yes | yes | NO | n/a |
| T1-JS-15 | PBKDF2 | yes | yes | NO | NO | n/a |
| T1-JS-16 | RSA | NO | NO | n/a | n/a | n/a |
| T1-JS-17 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T2-TS-01 | 3DES | NO | NO | n/a | n/a | n/a |
| T2-TS-02 | SHA-1 | yes | yes | yes | yes | n/a |
| T2-TS-03 | RSA | NO | NO | n/a | n/a | n/a |
| T2-TS-04 | EC | NO | NO | n/a | n/a | n/a |
| T2-TS-05 | AES | NO | NO | n/a | n/a | n/a |
| T2-TS-06 | AES | NO | NO | n/a | n/a | n/a |
| T2-TS-07 | HMAC | yes | yes | NO | yes | n/a |
| T1-C-01 | MD5 | yes | yes | yes | yes | n/a |
| T1-C-02 | SHA-1 | yes | yes | yes | yes | n/a |
| T1-C-03 | SHA-256 | NO | NO | n/a | n/a | n/a |
| T1-C-04 | SHA3-256 | NO | NO | n/a | n/a | n/a |
| T1-C-05 | AES | NO | NO | n/a | n/a | n/a |
| T1-C-06 | AES | yes | yes | NO | yes | n/a |
| T1-C-07 | 3DES | NO | NO | n/a | n/a | n/a |
| T1-C-08 | ChaCha20-Poly1305 | NO | NO | n/a | n/a | n/a |
| T1-C-09 | RSA | yes | yes | NO | yes | n/a |
| T1-C-10 | RSA | yes | yes | NO | yes | n/a |
| T1-C-11 | EC | yes | yes | yes | yes | n/a |
| T1-C-12 | Ed25519 | NO | NO | n/a | n/a | n/a |
| T1-C-13 | X25519 | NO | NO | n/a | n/a | n/a |
| T1-C-14 | DH | yes | yes | NO | yes | n/a |
| T1-C-15 | HMAC | yes | yes | yes | yes | n/a |
| T1-C-16 | PBKDF2 | yes | yes | NO | yes | n/a |
| T1-C-17 | TLS-1.0 | NO | NO | n/a | n/a | n/a |
| T1-C-18 | TLS_RSA_WITH_3DES_EDE_CBC_SHA | NO | NO | n/a | n/a | n/a |
| T1-C-19 | TLS_RSA_WITH_AES_128_CBC_SHA | NO | NO | n/a | n/a | n/a |
| T1-C-20 | TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 | NO | NO | n/a | n/a | n/a |
| T1-CS-01 | MD5 | NO | NO | n/a | n/a | n/a |
| T1-CS-02 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T1-CS-03 | SHA-256 | NO | NO | n/a | n/a | n/a |
| T1-CS-04 | SHA3-256 | NO | NO | n/a | n/a | n/a |
| T1-CS-05 | RSA | NO | NO | n/a | n/a | n/a |
| T1-CS-06 | EC | NO | NO | n/a | n/a | n/a |
| T1-CS-07 | EC | NO | NO | n/a | n/a | n/a |
| T1-CS-08 | AES | NO | NO | n/a | n/a | n/a |
| T1-CS-09 | AES | yes | yes | NO | yes | n/a |
| T1-CS-10 | 3DES | yes | yes | NO | yes | n/a |
| T1-CS-11 | HMAC | NO | NO | n/a | n/a | n/a |
| T1-CS-12 | PBKDF2 | yes | yes | NO | yes | n/a |
| T1-CS-13 | DSA | yes | yes | NO | yes | n/a |
| T2-C-01 | AES | NO | NO | n/a | n/a | n/a |
| T2-C-02 | SHA-1 | yes | yes | yes | yes | n/a |
| T2-C-03 | RSA | NO | NO | n/a | n/a | n/a |
| T2-C-04 | EC | NO | NO | n/a | n/a | n/a |
| T2-C-05 | HMAC | yes | yes | NO | yes | n/a |
| T2-C-06 | 3DES | NO | NO | n/a | n/a | n/a |
| T2-CS-01 | AES | NO | NO | n/a | n/a | n/a |
| T2-CS-02 | SHA-1 | yes | yes | yes | yes | n/a |
| T2-CS-03 | MD5 | NO | NO | n/a | n/a | n/a |
| T2-CS-04 | SHA-512 | NO | NO | n/a | n/a | n/a |
| T2-CS-05 | RSA | NO | NO | n/a | n/a | n/a |
| T2-CS-06 | EC | NO | NO | n/a | n/a | n/a |
| MX-PY-1a | PBKDF2 | yes | yes | yes | yes | n/a |
| MX-PY-1b | PBKDF2 | yes | yes | NO | yes | n/a |
| MX-PY-1c | HMAC | yes | yes | NO | yes | n/a |
| MX-PY-1d | AES | yes | yes | NO | yes | n/a |
| MX-PY-2a | DH | yes | yes | yes | yes | n/a |
| MX-PY-2b | ML-DSA | yes | yes | NO | yes | n/a |
| MX-PY-2c | DH | yes | yes | NO | yes | n/a |
| MX-PY-2d | ChaCha20-Poly1305 | yes | yes | yes | yes | n/a |
| MX-PY-3a | SHA-1 | yes | yes | yes | yes | n/a |
| MX-PY-3b | HMAC | yes | yes | NO | yes | n/a |
| MX-PY-3c | EC | yes | yes | NO | yes | n/a |
| MX-PY-3d | EC | yes | yes | yes | yes | n/a |
| MX-JV-1a | DH | yes | yes | yes | yes | n/a |
| MX-JV-1b | SHA-1 | yes | yes | yes | yes | n/a |
| MX-JV-1c | DH | yes | yes | NO | yes | n/a |
| MX-JV-1d | AES | yes | yes | NO | yes | n/a |
| MX-JV-2a | SHA-256 | yes | yes | yes | yes | n/a |
| MX-JV-2b | Ed25519 | NO | NO | n/a | n/a | n/a |
| MX-JV-2c | PBKDF2 | yes | yes | NO | yes | n/a |
| MX-JV-2d | PBKDF2 | yes | yes | yes | yes | n/a |
| MX-JV-3a | HMAC | yes | yes | yes | yes | n/a |
| MX-JV-3b | 3DES | yes | yes | NO | yes | n/a |
| MX-JV-3c | ChaCha20-Poly1305 | NO | NO | n/a | n/a | n/a |
| MX-JV-3d | SHA-512 | NO | NO | n/a | n/a | n/a |
| MX-JV-3e | 3DES | yes | yes | yes | yes | n/a |
| MX-GO-1a | PBKDF2 | yes | yes | NO | yes | n/a |
| MX-GO-1b | ML-KEM | yes | yes | NO | yes | n/a |
| MX-GO-1c | RSA | yes | yes | NO | yes | n/a |
| MX-GO-1d | RSA | yes | yes | NO | yes | n/a |
| MX-GO-2a | PBKDF2 | yes | yes | yes | yes | n/a |
| MX-GO-2b | DES | NO | NO | n/a | n/a | n/a |
| MX-GO-2c | PBKDF2 | yes | yes | NO | yes | n/a |
| MX-GO-2d | 3DES | NO | NO | n/a | n/a | n/a |
| MX-GO-3a | RSA | yes | yes | NO | yes | n/a |
| MX-GO-3b | RC4 | NO | NO | n/a | n/a | n/a |
| MX-GO-3c | HMAC | yes | yes | NO | yes | n/a |
| MX-GO-3d | Ed25519 | yes | yes | yes | yes | n/a |
| MX-JS-1a | AES | NO | NO | n/a | n/a | n/a |
| MX-JS-1b | HMAC | yes | yes | NO | yes | n/a |
| MX-JS-1c | AES | NO | NO | n/a | n/a | n/a |
| MX-JS-2a | SHA3-256 | NO | NO | n/a | n/a | n/a |
| MX-JS-2b | PBKDF2 | yes | yes | NO | yes | n/a |
| MX-JS-2c | EC | NO | NO | n/a | n/a | n/a |
| MX-JS-2d | EC | NO | NO | n/a | n/a | n/a |
| MX-JS-2e | AES | NO | NO | n/a | n/a | n/a |
| MX-TS-1a | EC | NO | NO | n/a | n/a | n/a |
| MX-TS-1b | HMAC | yes | yes | NO | yes | n/a |
| MX-TS-1c | AES | NO | NO | n/a | n/a | n/a |
| MX-TS-1d | RSA | NO | NO | n/a | n/a | n/a |
| MX-C-1a | SHA-1 | yes | yes | yes | yes | n/a |
| MX-C-1b | EC | yes | yes | yes | yes | n/a |
| MX-C-1c | HMAC | yes | yes | NO | yes | n/a |
| MX-C-1d | X25519 | NO | NO | n/a | n/a | n/a |
| MX-C-1e | HMAC | yes | yes | NO | yes | n/a |
| MX-C-2a | EC | NO | NO | n/a | n/a | n/a |
| MX-C-2b | AES | NO | NO | n/a | n/a | n/a |
| MX-C-2c | 3DES | NO | NO | n/a | n/a | n/a |
| MX-C-2d | 3DES | NO | NO | n/a | n/a | n/a |
| MX-C-3a | AES | NO | NO | n/a | n/a | n/a |
| MX-C-3b | 3DES | NO | NO | n/a | n/a | n/a |
| MX-C-3c | AES | NO | NO | n/a | n/a | n/a |
| MX-C-3d | DH | yes | yes | NO | yes | n/a |
| SYS-GO-01 | RSA | yes | NO | NO | yes | n/a |
| SYS-GO-02 | HMAC | yes | NO | NO | yes | n/a |
| SYS-GO-03 | SHA-256 | NO | NO | n/a | n/a | n/a |
| SYS-PY-01 | AES | yes | NO | yes | yes | n/a |
| SYS-PY-02 | HMAC | yes | NO | NO | yes | NO |
| SYS-PY-03 | RSA | yes | yes | yes | n/a | n/a |
| SYS-PY-04 | SHA-1 | NO | NO | n/a | n/a | n/a |
| SYS-JV-01 | EC | yes | NO | NO | yes | n/a |
| SYS-JV-02 | SHA-1 | yes | yes | yes | yes | n/a |
| SYS-AR-01 | EC | NO | NO | n/a | n/a | n/a |
| SYS-AR-02 | SHA-1 | NO | NO | n/a | n/a | n/a |
| SYS-AR-03 | RSA | yes | yes | yes | n/a | n/a |
| SYS-AR-04 | HMAC | yes | yes | yes | n/a | n/a |
| SYS-AR-05 | SHA-1 | yes | yes | yes | n/a | n/a |
| SYS-AR-06 | SHA-256 | yes | yes | yes | n/a | n/a |
| SYS-AS-01 | TLS-1.2 | yes | yes | yes | yes | n/a |
| SYS-AS-02 | TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 | NO | NO | n/a | n/a | n/a |
| SYS-AS-03 | TLS_RSA_WITH_AES_128_CBC_SHA | NO | NO | n/a | n/a | n/a |
| SYS-AS-04 | RSA | yes | yes | yes | n/a | n/a |
| SYS-AS-05 | SHA-256 | NO | NO | n/a | n/a | n/a |
| SYS-AS-06 | RSA | yes | yes | NO | n/a | n/a |
| SYS-AS-07 | EC | NO | NO | n/a | n/a | n/a |
| SYS-AS-08 | SHA-384 | NO | NO | n/a | n/a | n/a |
| SYS-AS-09 | EC | NO | NO | n/a | n/a | n/a |
| SYS-AS-10 | RSA | NO | NO | n/a | n/a | n/a |
| SYS-AS-11 | AES | NO | NO | n/a | n/a | n/a |
| DC-PY-01 | MD5 | yes | yes | yes | yes | n/a |
| DC-PY-02 | RSA | yes | yes | yes | yes | n/a |
| DC-JV-01 | DES | yes | yes | yes | yes | n/a |
| DC-JV-02 | SHA-1 | yes | yes | yes | yes | n/a |
| DC-GO-01 | MD5 | NO | NO | n/a | n/a | n/a |
| DC-GO-02 | RC4 | NO | NO | n/a | n/a | n/a |
| DC-JS-01 | MD5 | NO | NO | n/a | n/a | n/a |
| DC-JS-02 | 3DES | NO | NO | n/a | n/a | n/a |
| DC-C-01 | MD5 | yes | yes | yes | yes | n/a |
| DC-C-02 | 3DES | NO | NO | n/a | n/a | n/a |
