# CBOM Testbench Scorecard: QCI v2.3.4 (own container)

**Overall:** 232/330 findings detected (70.3% recall), 1 false positives (99.6% precision), parameters correct on 56.9% of detections.

Calibration cases (generated Tier 1-2 siblings of the hand-written cases; they feed the holdout's overfit gap and are not counted anywhere else here): 244/304 detected (80.3%), 3 false positives.

| Bucket | Detected | Recall | 95% interval | At primary site | Params correct | Line accurate | Quantum flag | False pos. | Precision |
|---|---|---|---|---|---|---|---|---|---|
| Tier 1 c | 14/20 | 70.0% | 48.1–85.5% | 70.0% | 42.9% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 1 go | 14/20 | 70.0% | 48.1–85.5% | 70.0% | 42.9% | 92.9% | 100.0% | 0 | 100.0% |
| Tier 1 java | 15/16 | 93.8% | 71.7–98.9% | 93.8% | 66.7% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 1 javascript | 14/17 | 82.4% | 59.0–93.8% | 82.4% | 42.9% | 78.6% | 100.0% | 0 | 100.0% |
| Tier 1 python | 15/16 | 93.8% | 71.7–98.9% | 93.8% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 2 c | 2/6 | 33.3% | 9.7–70.0% (thin) | 33.3% | 0.0% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 2 go | 5/6 | 83.3% | 43.6–97.0% (thin) | 83.3% | 20.0% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 2 java | 6/8 | 75.0% | 40.9–92.9% (thin) | 62.5% | 83.3% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 2 python | 8/9 | 88.9% | 56.5–98.0% (thin) | 77.8% | 87.5% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 2 typescript | 3/7 | 42.9% | 15.8–75.0% (thin) | 42.9% | 0.0% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 3 java | 5/7 | 71.4% | 35.9–91.8% (thin) | 71.4% | 40.0% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 3 python | 7/9 | 77.8% | 45.3–93.7% (thin) | 55.6% | 14.3% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 4 assets | 20/48 | 41.7% | 28.8–55.7% | 41.7% | 85.0% | 91.7% | 100.0% | 0 | 100.0% |
| Tier 5 java | 2/8 | 25.0% | 7.1–59.1% (thin) | 25.0% | 0.0% | n/a | 100.0% | 0 | 100.0% |
| Tier 5 python | 3/9 | 33.3% | 12.1–64.6% (thin) | 33.3% | 66.7% | 100.0% | 100.0% | 0 | 100.0% |
| Mixed files c | 9/13 | 69.2% | 42.4–87.3% | 69.2% | 22.2% | 100.0% | 100.0% | 0 | 100.0% |
| Mixed files go | 11/12 | 91.7% | 64.6–98.5% | 91.7% | 27.3% | 100.0% | 100.0% | 0 | 100.0% |
| Mixed files java | 11/13 | 84.6% | 57.8–95.7% | 84.6% | 54.5% | 100.0% | 100.0% | 0 | 100.0% |
| Mixed files javascript | 4/8 | 50.0% | 21.5–78.5% (thin) | 50.0% | 25.0% | 100.0% | 100.0% | 0 | 100.0% |
| Mixed files python | 12/12 | 100.0% | 75.7–100.0% | 100.0% | 50.0% | 100.0% | 100.0% | 0 | 100.0% |
| Mixed files typescript | 3/4 | 75.0% | 30.1–95.4% (thin) | 75.0% | 0.0% | 100.0% | 100.0% | 0 | 100.0% |
| PQC assets | 21/22 | 95.5% | 78.2–99.2% | 95.5% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| PQC go | 1/4 | 25.0% | 4.6–69.9% (thin) | 25.0% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| PQC java | 4/4 | 100.0% | 51.0–100.0% (thin) | 100.0% | 50.0% | 100.0% | 100.0% | 0 | 100.0% |
| PQC python | 6/6 | 100.0% | 61.0–100.0% (thin) | 100.0% | 50.0% | 100.0% | 100.0% | 0 | 100.0% |
| System fixture artifacts | 4/6 | 66.7% | 30.0–90.3% (thin) | 66.7% | 100.0% | n/a | 100.0% | 1 | 80.0% |
| System fixture assets | 5/11 | 45.5% | 21.3–72.0% | 45.5% | 40.0% | 66.7% | 100.0% | 0 | 100.0% |
| System fixture go | 3/3 | 100.0% | 43.8–100.0% (thin) | 33.3% | 33.3% | 100.0% | 100.0% | 0 | 100.0% |
| System fixture java | 2/2 | 100.0% | 34.2–100.0% (thin) | 50.0% | 50.0% | 100.0% | 100.0% | 0 | 100.0% |
| System fixture python | 3/4 | 75.0% | 30.1–95.4% (thin) | 25.0% | 33.3% | 100.0% | 100.0% | 0 | 100.0% |
| **Total** | 232/330 | 70.3% | 65.2–75.0% | 67.6% | 56.9% | 97.1% | 100.0% | 1 | 99.6% |
| Negative controls | | | | | | | | 0 | |

Intervals are 95% Wilson intervals on recall. 18 bucket(s) have fewer than 10 findings and are marked thin: read their rates as indications, not measurements.

**PQC over-claims: 0.** Post-quantum or hybrid algorithms reported where the code or config has none. Each one makes migration look further along than it is. Any number above zero should be explained by the vendor before purchase.

**PQC by standard name: 19/19 (100.0%).** Detected post-quantum findings reported under the FIPS 203/204/205 name or OID. Reports that only say Kyber, Dilithium, SPHINCS+ or Falcon keep their recall credit and fail this check.

## System fixture: routing and asset links

**Routable: 12/17 detected system findings (70.6%)** (of 26). Routable means a reported location resolves, through the fixture's CODEOWNERS, to the team that owns the fix. Reporting only the shared wrapper or its config is detection, but the ticket lands with platform-security.

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

**Deadline-weighted recall: 71.1%** (at primary site: 67.9%). **Findings due by end of 2030 that this scanner missed: 31.**

| When it's due | Weight | Detected | Recall | At primary site |
|---|---|---|---|---|
| Due now (not approved or past its date) | 5 | 53/73 | 72.6% | 69.9% |
| Due by end of 2030 | 4 | 23/34 | 67.6% | 61.8% |
| Due 2031 to 2033 | 3 | 0/0 | n/a | n/a |
| Due 2034 to 2035 | 2 | 70/96 | 72.9% | 69.8% |
| No deadline (approved, review, out of scope, unknown) | 1 | 86/127 | 67.7% | 66.1% |

| Missed | Algorithm | Due | File |
|---|---|---|---|
| T2-PY-04 | SHA-1 | 2030-12-31 | `corpus/tier2/python/t2_env_default.py` |
| T2-JV-04 | SHA-1 | 2030-12-31 | `corpus/tier2/java/T2Enum.java` |
| T3-PY-02 | SHA-1 | 2030-12-31 | `corpus/tier3/python/cross_module_constant/tokens/fingerprint.py` |
| T3-PY-08 | MD5 | **now** | `corpus/tier3/python/dependency_injection/wiring.py` |
| T3-JV-06 | MD5 | **now** | `corpus/tier3/java/dependency_injection/src/com/acme/audit/DigestProvider.java` |
| T4-AS-04 | SHA-1 | 2030-12-31 | `corpus/tier4/assets/certs/payments_legacy.crt` |
| T4-AS-24 | RSA-1024 | 2013-12-31 | `corpus/tier4/assets/keystores/partner_truststore.jks` |
| T4-AS-25 | SHA-1 | 2030-12-31 | `corpus/tier4/assets/keystores/partner_truststore.jks` |
| T4-AS-38 | TLS_RSA_WITH_3DES_EDE_CBC_SHA | **now** | `corpus/tier4/assets/tls/nginx.conf` |
| T4-AS-44 | RSA-1024 | 2013-12-31 | `corpus/tier4/assets/tls/openssl.cnf` |
| T5-PY-02 | MD5 | **now** | `corpus/tier5/python/t5_string_assembly.py` |
| T5-PY-05 | RC4 | **now** | `corpus/tier5/python/t5_handrolled_keystream.py` |
| T5-PY-07 | RSA-1024 | 2013-12-31 | `corpus/tier5/python/t5_handrolled_pubkey.py` |
| T5-PY-09 | HMAC-MD5 | **now** | `corpus/tier5/python/compiled/ledger_sync.pyc` |
| T5-JV-02 | 3DES-CBC | 2023-12-31 | `corpus/tier5/java/T5StringAssembly.java` |
| T5-JV-03 | MD5 | **now** | `corpus/tier5/java/T5Reflection.java` |
| T5-JV-04 | TEA | **now** | `corpus/tier5/java/T5BlockTransform.java` |
| T5-JV-08 | SHA-1 | 2030-12-31 | `corpus/tier5/java/compiled/billing-core.jar` |
| T1-GO-09 | RC4 | **now** | `corpus/tier1/go/rc4/main.go` |
| T1-GO-18 | TLS_RSA_WITH_3DES_EDE_CBC_SHA | **now** | `corpus/tier1/go/tls_config/main.go` |
| T1-JS-01 | MD5 | **now** | `corpus/tier1/javascript/t1_hashes.js` |
| T1-JS-02 | SHA-1 | 2030-12-31 | `corpus/tier1/javascript/t1_hashes.js` |
| T2-TS-01 | 3DES-CBC | 2023-12-31 | `corpus/tier2/typescript/t2_config_object.ts` |
| T2-TS-02 | SHA-1 | 2030-12-31 | `corpus/tier2/typescript/t2_default_param.ts` |
| T1-C-18 | TLS_RSA_WITH_3DES_EDE_CBC_SHA | **now** | `corpus/tier1/c/t1_tls_ctx.c` |
| T2-C-02 | SHA-1 | 2030-12-31 | `corpus/tier2/c/t2_digest_table.c` |
| T2-C-03 | RSA-1024 | 2013-12-31 | `corpus/tier2/c/t2_macro_bits.c` |
| MX-GO-3b | RC4 | **now** | `corpus/mixed/go/invoice_gateway/main.go` |
| MX-C-2d | 3DES-CBC | 2023-12-31 | `corpus/mixed/c/policy_agent.c` |
| SYS-PY-04 | SHA-1 | 2030-12-31 | `corpus/system/payments-platform/services/settlement-worker/partner_ca.py` |
| SYS-AR-02 | SHA-1 | 2030-12-31 | `corpus/system/payments-platform/services/ledger-service/build/libs/ledger-service.jar` |

## Actionability: could an engineer open a ticket from this?

Rubric `cbom-actionability-v1` (proposed; see `rubric/actionability.json`). Each detected finding is checked for the fields a migration ticket needs. Facts are checked against the real files.

**Ticket-ready: 109/232 detected findings (47.0%)**, meaning every must-have is present and correct. **Actionable recall: 33.0%** of all 330 expected findings were both found and ticket-ready. Field completeness across all checks: 55.7%.

| Check | Tier | Applies to | Passed | Rate |
|---|---|---|---|---|
| Exact location | must | 232 | 230 | 99.1% |
| Correct parameters | must | 158 | 58 | 36.7% |
| Primitive, where the family is ambiguous | must | 56 | 44 | 78.6% |
| Certificate expiry (correct) | must | 13 | 2 | 15.4% |
| Certificate subject (correct) | must | 13 | 2 | 15.4% |
| Key material type | must | 7 | 3 | 42.9% |
| Protocol version | must | 8 | 0 | 0.0% |
| OID | should | 215 | 70 | 32.6% |
| Crypto functions | should | 222 | 222 | 100.0% |
| Quantum security level (correct) | should | 220 | 138 | 62.7% |
| Code context | should | 95 | 0 | 0.0% |
| Providing library | should | 98 | 0 | 0.0% |
| Certificate issuer | should | 13 | 2 | 15.4% |
| Certificate start date | should | 13 | 0 | 0.0% |
| Certificate key and signature linked | should | 13 | 0 | 0.0% |
| Key format | should | 7 | 0 | 0.0% |
| Cipher suite in a protocol | should | 0 | 0 | n/a |

Detected but not ticket-ready (123), first 25:

| ID | Algorithm | Missing must-haves |
|---|---|---|
| T1-JV-05 | RSA-3072 | Correct parameters |
| T1-JV-06 | ECC-P-256 | Correct parameters |
| T1-JV-07 | DSA-2048 | Correct parameters |
| T1-JV-08 | AES-128-ECB | Correct parameters |
| T1-JV-14 | DH-2048 | Correct parameters |
| T2-PY-09 | ECC-P-384 | Correct parameters |
| T2-JV-08 | ECC-P-384 | Correct parameters |
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
| T4-AS-18 | RSA-2048 | Primitive, where the family is ambiguous |
| T4-AS-19 | ECC-P-256 | Primitive, where the family is ambiguous |

## Missed findings

| ID | File | Expected | Line |
|---|---|---|---|
| T1-PY-04 | `corpus/tier1/python/t1_hashes.py` | SHA3-256  | 9 |
| T1-JV-04 | `corpus/tier1/java/T1Hashes.java` | SHA3-256  | 13 |
| T2-PY-04 | `corpus/tier2/python/t2_env_default.py` | SHA-1  | 10 |
| T2-JV-04 | `corpus/tier2/java/T2Enum.java` | SHA-1  | 6 |
| T2-JV-05 | `corpus/tier2/java/T2Enum.java` | SHA-256  | 7 |
| T3-PY-02 | `corpus/tier3/python/cross_module_constant/tokens/fingerprint.py` | SHA-1  | 8 |
| T3-PY-08 | `corpus/tier3/python/dependency_injection/wiring.py` | MD5  | 9 |
| T3-JV-06 | `corpus/tier3/java/dependency_injection/src/com/acme/audit/DigestProvider.java` | MD5  | 14 |
| T3-JV-07 | `corpus/tier3/java/jwt_alg_mapping/src/com/acme/jwt/JwtSigner.java` | HMAC {'hash': 'SHA-256'} | 23 |
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
| T4-AS-22 | `corpus/tier4/assets/keystores/orders_keystore.p12` | RSA {'key_size': 2048} | file |
| T4-AS-23 | `corpus/tier4/assets/keystores/orders_keystore.p12` | SHA-256  | file |
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
| T4-AS-47 | `corpus/tier4/assets/k8s/ingress-tls-secret.yaml` | EC {'curve': 'P-384'} | file |
| T4-AS-48 | `corpus/tier4/assets/k8s/ingress-tls-secret.yaml` | SHA-384  | file |
| T5-PY-02 | `corpus/tier5/python/t5_string_assembly.py` | MD5  | 14 |
| T5-PY-03 | `corpus/tier5/python/t5_dynamic_import.py` | RSA {'key_size': 2048} | 10 |
| T5-PY-05 | `corpus/tier5/python/t5_handrolled_keystream.py` | RC4  | 13 |
| T5-PY-06 | `corpus/tier5/python/t5_handrolled_digest.py` | SHA-256  | 31 |
| T5-PY-07 | `corpus/tier5/python/t5_handrolled_pubkey.py` | RSA {'key_size': 1024} | 17 |
| T5-PY-09 | `corpus/tier5/python/compiled/ledger_sync.pyc` | HMAC {'hash': 'MD5'} | file |
| T5-JV-01 | `corpus/tier5/java/T5StringAssembly.java` | RSA {'key_size': 2048} | 9 |
| T5-JV-02 | `corpus/tier5/java/T5StringAssembly.java` | 3DES {'mode': 'CBC'} | 14 |
| T5-JV-03 | `corpus/tier5/java/T5Reflection.java` | MD5  | 10 |
| T5-JV-04 | `corpus/tier5/java/T5BlockTransform.java` | TEA  | 3 |
| T5-JV-05 | `corpus/tier5/java/T5HandrolledPubkey.java` | RSA {'key_size': 2048} | 19 |
| T5-JV-08 | `corpus/tier5/java/compiled/billing-core.jar` | SHA-1  | file |
| PQ-AS-11 | `corpus/pqc/assets/tls/openssl_pq.cnf` | SecP384r1MLKEM1024  | 13 |
| T1-GO-04 | `corpus/tier1/go/hashes/main.go` | SHA3-256  | 17 |
| T1-GO-09 | `corpus/tier1/go/rc4/main.go` | RC4  | 10 |
| T1-GO-17 | `corpus/tier1/go/tls_config/main.go` | TLS-1.0  | 11 |
| T1-GO-18 | `corpus/tier1/go/tls_config/main.go` | TLS_RSA_WITH_3DES_EDE_CBC_SHA  | 13 |
| T1-GO-19 | `corpus/tier1/go/tls_config/main.go` | TLS_RSA_WITH_AES_128_CBC_SHA  | 14 |
| T1-GO-20 | `corpus/tier1/go/tls_config/main.go` | TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256  | 15 |
| T2-GO-03 | `corpus/tier2/go/curve_table/main.go` | EC {'curve': 'P-384'} | 12 |
| PQ-GO-02 | `corpus/pqc/go/tls_hybrid/main.go` | TLS-1.3  | 11 |
| PQ-GO-03 | `corpus/pqc/go/tls_hybrid/main.go` | X25519MLKEM768  | 12 |
| PQ-GO-04 | `corpus/pqc/go/tls_hybrid/main.go` | X25519  | 12 |
| T1-JS-01 | `corpus/tier1/javascript/t1_hashes.js` | MD5  | 5 |
| T1-JS-02 | `corpus/tier1/javascript/t1_hashes.js` | SHA-1  | 6 |
| T1-JS-04 | `corpus/tier1/javascript/t1_hashes.js` | SHA3-256  | 8 |
| T2-TS-01 | `corpus/tier2/typescript/t2_config_object.ts` | 3DES {'mode': 'CBC'} | 5 |
| T2-TS-02 | `corpus/tier2/typescript/t2_default_param.ts` | SHA-1  | 4 |
| T2-TS-05 | `corpus/tier2/typescript/t2_wrapper.ts` | AES {'key_size': 128, 'mode': 'ECB'} | 9 |
| T2-TS-06 | `corpus/tier2/typescript/t2_template.ts` | AES {'key_size': 256, 'mode': 'GCM'} | 4 |
| T1-C-04 | `corpus/tier1/c/t1_digests.c` | SHA3-256  | 18 |
| T1-C-12 | `corpus/tier1/c/t1_modern_curves.c` | Ed25519  | 6 |
| T1-C-17 | `corpus/tier1/c/t1_tls_ctx.c` | TLS-1.0  | 7 |
| T1-C-18 | `corpus/tier1/c/t1_tls_ctx.c` | TLS_RSA_WITH_3DES_EDE_CBC_SHA  | 8 |
| T1-C-19 | `corpus/tier1/c/t1_tls_ctx.c` | TLS_RSA_WITH_AES_128_CBC_SHA  | 8 |
| T1-C-20 | `corpus/tier1/c/t1_tls_ctx.c` | TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256  | 8 |
| T2-C-01 | `corpus/tier2/c/t2_fetch_by_name.c` | AES {'key_size': 192, 'mode': 'CBC'} | 6 |
| T2-C-02 | `corpus/tier2/c/t2_digest_table.c` | SHA-1  | 12 |
| T2-C-03 | `corpus/tier2/c/t2_macro_bits.c` | RSA {'key_size': 1024} | 7 |
| T2-C-04 | `corpus/tier2/c/t2_curve_index.c` | EC {'curve': 'P-521'} | 7 |
| MX-JV-2b | `corpus/mixed/java/BookingOptionsModule.java` | Ed25519  | 170 |
| MX-JV-3d | `corpus/mixed/java/OrderDefaultsModule.java` | SHA-512  | 269 |
| MX-GO-3b | `corpus/mixed/go/invoice_gateway/main.go` | RC4  | 198 |
| MX-JS-1a | `corpus/mixed/javascript/partner_routes.js` | AES {'key_size': 128, 'mode': 'CBC'} | 5 |
| MX-JS-1c | `corpus/mixed/javascript/partner_routes.js` | AES {'key_size': 256, 'mode': 'CTR'} | 8 |
| MX-JS-2a | `corpus/mixed/javascript/device_session.js` | SHA3-256  | 94 |
| MX-JS-2e | `corpus/mixed/javascript/device_session.js` | AES {'key_size': 256, 'mode': 'CTR'} | 68 |
| MX-TS-1c | `corpus/mixed/typescript/voucher_service.ts` | AES {'key_size': 128, 'mode': 'ECB'} | 36 |
| MX-C-2a | `corpus/mixed/c/policy_agent.c` | EC {'curve': 'P-384'} | 9 |
| MX-C-2b | `corpus/mixed/c/policy_agent.c` | AES {'key_size': 192, 'mode': 'CBC'} | 10 |
| MX-C-2d | `corpus/mixed/c/policy_agent.c` | 3DES {'mode': 'CBC'} | 11 |
| MX-C-3a | `corpus/mixed/c/audit_daemon.c` | AES {'key_size': 192, 'mode': 'CBC'} | 8 |
| SYS-PY-04 | `corpus/system/payments-platform/services/settlement-worker/partner_ca.py` | SHA-1  | file |
| SYS-AR-01 | `corpus/system/payments-platform/services/ledger-service/build/libs/ledger-service.jar` | EC  | file |
| SYS-AR-02 | `corpus/system/payments-platform/services/ledger-service/build/libs/ledger-service.jar` | SHA-1  | file |
| SYS-AS-02 | `corpus/system/payments-platform/edge/nginx/gateway.conf` | TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384  | 9 |
| SYS-AS-03 | `corpus/system/payments-platform/edge/nginx/gateway.conf` | TLS_RSA_WITH_AES_128_CBC_SHA  | 9 |
| SYS-AS-05 | `corpus/system/payments-platform/edge/nginx/tls/gateway.crt` | SHA-256  | file |
| SYS-AS-07 | `corpus/system/payments-platform/deploy/k8s/gateway-ingress-tls.yaml` | EC {'curve': 'P-384'} | file |
| SYS-AS-08 | `corpus/system/payments-platform/deploy/k8s/gateway-ingress-tls.yaml` | SHA-384  | file |
| SYS-AS-11 | `corpus/system/payments-platform/infra/terraform/kms.tf` | AES {'key_size': 256, 'mode': 'GCM'} | 15 |

## Detected with wrong or missing parameters

| ID | Family | Expected params | Reported params |
|---|---|---|---|
| T1-JV-05 | RSA | `{"key_size": 3072}` | `{}` |
| T1-JV-06 | EC | `{"curve": "P-256"}` | `{}` |
| T1-JV-07 | DSA | `{"key_size": 2048}` | `{}; {}` |
| T1-JV-08 | AES | `{"key_size": 128, "mode": "ECB"}` | `{"key_size": 128}` |
| T1-JV-14 | DH | `{"key_size": 2048}` | `{}; {}` |
| T2-PY-09 | EC | `{"curve": "P-384"}` | `{}` |
| T2-JV-08 | EC | `{"curve": "P-384"}` | `{}` |
| T3-PY-01 | RSA | `{"key_size": 1024}` | `{}` |
| T3-PY-03 | AES | `{"key_size": 128, "mode": "GCM"}` | `{"mode": "GCM"}` |
| T3-PY-04 | RSA | `{"key_size": 1024}` | `{}` |
| T3-PY-05 | RSA | `{"key_size": 3072}` | `{}` |
| T3-PY-06 | AES | `{"key_size": 256, "mode": "CBC"}` | `{"mode": "CBC"}` |
| T3-PY-09 | HMAC | `{"hash": "SHA-256"}` | `{}` |
| T3-JV-01 | RSA | `{"key_size": 1024}` | `{}` |
| T3-JV-03 | AES | `{"key_size": 128, "mode": "GCM"}` | `{"mode": "GCM"}` |
| T3-JV-04 | AES | `{"key_size": 256, "mode": "CBC"}` | `{}; {"mode": "CBC"}` |
| T4-AS-05 | EC | `{"curve": "P-256"}` | `{"key_size": 256}` |
| T4-AS-15 | EC | `{"curve": "secp256k1"}` | `{}` |
| T4-AS-27 | DH | `{"key_size": 2048}` | `{}` |
| T5-PY-04 | AES | `{"key_size": 128, "mode": "ECB"}` | `{"key_size": 128}` |
| T5-JV-06 | AES | `{"key_size": 128, "mode": "CBC"}` | `{"mode": "CBC"}` |
| T5-JV-07 | RSA | `{"key_size": 1024}` | `{}` |
| PQ-PY-01 | ML-KEM | `{"param_set": "768"}` | `{"param_set": "ML-KEM"}` |
| PQ-PY-02 | ML-DSA | `{"param_set": "65"}` | `{"param_set": "ML-DSA"}` |
| PQ-PY-04 | ML-KEM | `{"param_set": "768"}` | `{"param_set": "ML-KEM"}` |
| PQ-JV-03 | ML-DSA | `{"param_set": "44"}` | `{"param_set": "ML-DSA"}` |
| PQ-JV-04 | EC | `{"curve": "P-384"}` | `{}` |
| T1-GO-05 | AES | `{"key_size": 256, "mode": "GCM"}` | `{}; {}` |
| T1-GO-06 | AES | `{"key_size": 128, "mode": "CBC"}` | `{}; {}` |
| T1-GO-07 | 3DES | `{"mode": "CBC"}` | `{}; {}` |
| T1-GO-08 | DES | `{"mode": "CBC"}` | `{}` |
| T1-GO-10 | RSA | `{"key_size": 2048}` | `{}` |
| T1-GO-11 | EC | `{"curve": "P-256"}` | `{}` |
| T1-GO-14 | DSA | `{"key_size": 2048}` | `{}; {}` |
| T1-GO-16 | PBKDF2 | `{"hash": "SHA-512"}` | `{}` |
| T2-GO-02 | RSA | `{"key_size": 1024}` | `{}; {}` |
| T2-GO-04 | HMAC | `{"hash": "MD5"}` | `{}` |
| T2-GO-05 | AES | `{"key_size": 192, "mode": "CTR"}` | `{}; {}` |
| T2-GO-06 | 3DES | `{"mode": "CBC"}` | `{}; {}` |
| T1-JS-05 | AES | `{"key_size": 128, "mode": "CBC"}` | `{}` |
| T1-JS-06 | AES | `{"key_size": 256, "mode": "GCM"}` | `{}` |
| T1-JS-07 | 3DES | `{"mode": "CBC"}` | `{}` |
| T1-JS-09 | RSA | `{"key_size": 2048}` | `{}` |
| T1-JS-13 | DH | `{"key_size": 2048}` | `{}` |
| T1-JS-14 | HMAC | `{"hash": "SHA-256"}` | `{}` |
| T1-JS-15 | PBKDF2 | `{"hash": "SHA-512"}` | `{}` |
| T1-JS-16 | RSA | `{"key_size": 3072}` | `{}` |
| T2-TS-03 | RSA | `{"key_size": 1024}` | `{}` |
| T2-TS-04 | EC | `{"curve": "P-384"}` | `{}` |
| T2-TS-07 | HMAC | `{"hash": "MD5"}` | `{}` |
| T1-C-05 | AES | `{"key_size": 128, "mode": "ECB"}` | `{}` |
| T1-C-06 | AES | `{"key_size": 256, "mode": "GCM"}` | `{}` |
| T1-C-07 | 3DES | `{"mode": "CBC"}` | `{}` |
| T1-C-09 | RSA | `{"key_size": 1024}` | `{}` |
| T1-C-10 | RSA | `{"key_size": 3072}` | `{}` |
| T1-C-11 | EC | `{"curve": "P-256"}` | `{}` |
| T1-C-14 | DH | `{"key_size": 2048}` | `{}` |
| T1-C-16 | PBKDF2 | `{"hash": "SHA-1"}` | `{}` |
| T2-C-05 | HMAC | `{"hash": "MD5"}` | `{}` |
| T2-C-06 | 3DES | `{"mode": "ECB"}` | `{}` |
| MX-PY-1b | PBKDF2 | `{"hash": "SHA-512"}` | `{}` |
| MX-PY-1c | HMAC | `{"hash": "SHA-512"}` | `{}` |
| MX-PY-1d | AES | `{"key_size": 192, "mode": "CTR"}` | `{"key_size": 128}` |
| MX-PY-2b | ML-DSA | `{"param_set": "65"}` | `{"param_set": "ML-DSA"}` |
| MX-PY-2c | DH | `{"key_size": 1024}` | `{}` |
| MX-PY-3b | HMAC | `{"hash": "SHA-512"}` | `{}` |
| MX-JV-1a | DH | `{"key_size": 3072}` | `{}` |
| MX-JV-1c | DH | `{"key_size": 2048}` | `{}` |
| MX-JV-1d | AES | `{"key_size": 192, "mode": "ECB"}` | `{"key_size": 192}` |
| MX-JV-2c | PBKDF2 | `{"hash": "SHA-512"}` | `{}; {}` |
| MX-JV-3b | 3DES | `{"mode": "ECB"}` | `{}` |
| MX-GO-1a | PBKDF2 | `{"hash": "SHA-512"}` | `{}` |
| MX-GO-1c | RSA | `{"key_size": 1024}` | `{}` |
| MX-GO-1d | RSA | `{"key_size": 2048}` | `{}` |
| MX-GO-2b | DES | `{"mode": "CBC"}` | `{}` |
| MX-GO-2c | PBKDF2 | `{"hash": "SHA-1"}` | `{}` |
| MX-GO-2d | 3DES | `{"mode": "CBC"}` | `{}` |
| MX-GO-3a | RSA | `{"key_size": 2048}` | `{}` |
| MX-GO-3c | HMAC | `{"hash": "SHA-1"}` | `{}` |
| MX-JS-2b | PBKDF2 | `{"hash": "SHA-512"}` | `{}` |
| MX-JS-2c | EC | `{"curve": "P-521"}` | `{}` |
| MX-JS-2d | EC | `{"curve": "P-384"}` | `{}` |
| MX-TS-1a | EC | `{"curve": "P-256"}` | `{}` |
| MX-TS-1b | HMAC | `{"hash": "SHA-512"}` | `{}` |
| MX-TS-1d | RSA | `{"key_size": 2048}` | `{}` |
| MX-C-1b | EC | `{"curve": "P-521"}` | `{}` |
| MX-C-1c | HMAC | `{"hash": "MD5"}` | `{}` |
| MX-C-1e | HMAC | `{"hash": "SHA-512"}` | `{}` |
| MX-C-2c | 3DES | `{"mode": "ECB"}` | `{}` |
| MX-C-3b | 3DES | `{"mode": "CBC"}` | `{}` |
| MX-C-3c | AES | `{"key_size": 128, "mode": "ECB"}` | `{}` |
| MX-C-3d | DH | `{"key_size": 3072}` | `{}` |
| SYS-GO-01 | RSA | `{"key_size": 2048}` | `{}; {}` |
| SYS-GO-02 | HMAC | `{"hash": "SHA-1"}` | `{}` |
| SYS-PY-01 | AES | `{"key_size": 128, "mode": "CBC"}` | `{"key_size": 128}` |
| SYS-PY-02 | HMAC | `{"hash": "SHA-1"}` | `{}` |
| SYS-JV-01 | EC | `{"curve": "P-256"}` | `{}` |
| SYS-AS-06 | RSA | `{"key_size": 2048}` | `{}` |
| SYS-AS-09 | EC | `{"curve": "P-256"}` | `{}` |
| SYS-AS-10 | RSA | `{"key_size": 2048}` | `{}; {}; {}; {}` |

## False positives

| File | Reported family | Lines | Negative control? |
|---|---|---|---|
| `corpus/system/payments-platform/services/api-gateway/bin/api-gateway` | DH | 348, 1461, 1912, 4654, 4675, 5013, 5218, 5235, 5239, 5249, 5264, 6065, 7065, 7072, 10688, 10945, 11763, 12417, 12746, 49070, 50098, 53217 | no |

## Unrecognized names (not scored, review manually)

- `corpus/calibration/tier1/c/cal_sha3256_035.c` line 12: qci-category-1
- `corpus/calibration/tier1/c/cal_sha3256_036.c` line 12: qci-category-2
- `corpus/calibration/tier1/c/cal_sha3256_037.c` line 8: qci-category-3
- `corpus/calibration/tier1/go/cal_rc4_027/cal_rc4_027.go` line 5: qci-category-4
- `corpus/calibration/tier1/go/cal_rc4_027/cal_rc4_027.go` line 32: qci-category-5
- `corpus/calibration/tier1/go/cal_rc4_028/cal_rc4_028.go` line 5: qci-category-6
- `corpus/calibration/tier1/go/cal_rc4_028/cal_rc4_028.go` line 24: qci-category-7
- `corpus/calibration/tier1/go/cal_rc4_029/cal_rc4_029.go` line 5: qci-category-8
- `corpus/calibration/tier1/go/cal_rc4_029/cal_rc4_029.go` line 24: qci-category-9
- `corpus/calibration/tier1/go/cal_sha3256_039/cal_sha3256_039.go` line 5: qci-category-10
- `corpus/calibration/tier1/go/cal_sha3256_039/cal_sha3256_039.go` line 32: qci-category-11
- `corpus/calibration/tier1/go/cal_sha3256_040/cal_sha3256_040.go` line 5: qci-category-12
- `corpus/calibration/tier1/go/cal_sha3256_040/cal_sha3256_040.go` line 24: qci-category-13
- `corpus/calibration/tier1/go/cal_sha3256_041/cal_sha3256_041.go` line 5: qci-category-14
- `corpus/calibration/tier1/go/cal_sha3256_041/cal_sha3256_041.go` line 32: qci-category-15
- `corpus/calibration/tier1/java/Cal1037ShipmentSettings.java` line 5: qci-category-16
- `corpus/calibration/tier1/java/Cal1038MemberOptions.java` line 9: qci-category-17
- `corpus/calibration/tier1/java/Cal1039PayloadDefaults.java` line 13: qci-category-18
- `corpus/calibration/tier1/javascript/cal_3des_001.js` line 2: qci-category-19
- `corpus/calibration/tier1/javascript/cal_3des_002.js` line 2: qci-category-20
- `corpus/calibration/tier1/javascript/cal_3des_003.js` line 2: qci-category-21
- `corpus/calibration/tier1/javascript/cal_aes_004.js` line 2: qci-category-22
- `corpus/calibration/tier1/javascript/cal_aes_005.js` line 2: qci-category-23
- `corpus/calibration/tier1/javascript/cal_chacha20poly1305_006.js` line 2: qci-category-24
- `corpus/calibration/tier1/javascript/cal_chacha20poly1305_007.js` line 2: qci-category-25
- `corpus/calibration/tier1/javascript/cal_chacha20poly1305_008.js` line 2: qci-category-26
- `corpus/calibration/tier1/javascript/cal_dh_009.js` line 2: qci-category-27
- `corpus/calibration/tier1/javascript/cal_dh_010.js` line 2: qci-category-28
- `corpus/calibration/tier1/javascript/cal_dh_011.js` line 2: qci-category-29
- `corpus/calibration/tier1/javascript/cal_ec_012.js` line 2: qci-category-30
- `corpus/calibration/tier1/javascript/cal_ec_013.js` line 2: qci-category-31
- `corpus/calibration/tier1/javascript/cal_ec_014.js` line 2: qci-category-32
- `corpus/calibration/tier1/javascript/cal_ed25519_015.js` line 2: qci-category-33
- `corpus/calibration/tier1/javascript/cal_ed25519_016.js` line 2: qci-category-34
- `corpus/calibration/tier1/javascript/cal_ed25519_017.js` line 2: qci-category-35
- `corpus/calibration/tier1/javascript/cal_hmac_018.js` line 2: qci-category-36
- `corpus/calibration/tier1/javascript/cal_hmac_019.js` line 2: qci-category-37
- `corpus/calibration/tier1/javascript/cal_hmac_020.js` line 2: qci-category-38
- `corpus/calibration/tier1/javascript/cal_md5_021.js` line 2: qci-category-39
- `corpus/calibration/tier1/javascript/cal_md5_022.js` line 2: qci-category-40
- `corpus/calibration/tier1/javascript/cal_md5_023.js` line 2: qci-category-41
- `corpus/calibration/tier1/javascript/cal_pbkdf2_024.js` line 2: qci-category-42
- `corpus/calibration/tier1/javascript/cal_pbkdf2_025.js` line 2: qci-category-43
- `corpus/calibration/tier1/javascript/cal_pbkdf2_026.js` line 2: qci-category-44
- `corpus/calibration/tier1/javascript/cal_rsa_027.js` line 2: qci-category-45
- `corpus/calibration/tier1/javascript/cal_rsa_028.js` line 2: qci-category-46
- `corpus/calibration/tier1/javascript/cal_sha1_029.js` line 2: qci-category-47
- `corpus/calibration/tier1/javascript/cal_sha1_030.js` line 2: qci-category-48
- `corpus/calibration/tier1/javascript/cal_sha256_031.js` line 2: qci-category-49
- `corpus/calibration/tier1/javascript/cal_sha256_032.js` line 2: qci-category-50
- `corpus/calibration/tier1/javascript/cal_sha256_033.js` line 2: qci-category-51
- `corpus/calibration/tier1/javascript/cal_sha3256_034.js` line 2: qci-category-52
- `corpus/calibration/tier1/javascript/cal_sha3256_034.js` line 9: qci-category-53
- `corpus/calibration/tier1/javascript/cal_sha3256_035.js` line 2: qci-category-54
- `corpus/calibration/tier1/javascript/cal_sha3256_035.js` line 9: qci-category-55
- `corpus/calibration/tier1/javascript/cal_sha3256_036.js` line 2: qci-category-56
- `corpus/calibration/tier1/javascript/cal_sha3256_036.js` line 5: qci-category-57
- `corpus/calibration/tier1/javascript/cal_x25519_037.js` line 2: qci-category-58
- `corpus/calibration/tier1/javascript/cal_x25519_038.js` line 2: qci-category-59
- `corpus/calibration/tier1/javascript/cal_x25519_039.js` line 2: qci-category-60
- `corpus/calibration/tier1/python/cal_sha3256_039.py` line 6: qci-category-61
- `corpus/calibration/tier1/python/cal_sha3256_040.py` line 6: qci-category-62
- `corpus/calibration/tier1/python/cal_sha3256_041.py` line 17: qci-category-63
- `corpus/mixed/c/audit_daemon.c` line 218: qci-category-64
- `corpus/mixed/c/audit_daemon.c` line 315: qci-category-65
- `corpus/mixed/go/invoice_gateway/main.go` line 8: qci-category-66
- `corpus/mixed/go/invoice_gateway/main.go` line 198: qci-category-67
- `corpus/mixed/go/invoice_gateway/main.go` line 207: qci-category-68
- `corpus/mixed/go/invoice_gateway/main.go` line 230: qci-category-69
- `corpus/mixed/javascript/device_session.js` line 2: qci-category-70
- `corpus/mixed/javascript/device_session.js` line 94: qci-category-71
- `corpus/mixed/javascript/partner_routes.js` line 2: qci-category-72
- `corpus/mixed/javascript/partner_routes.js` line 263: qci-category-73
- `corpus/mixed/python/invoice_service.py` line 52: qci-category-74
- `corpus/mixed/python/order_jobs.py` line 33: qci-category-75
- `corpus/pqc/assets/keys/attestation_signer.pem` line 1: qci-category-80
- `corpus/pqc/assets/ssh/sshd_config_pq` line 6: qci-category-81
- `corpus/pqc/assets/ssh/sshd_config_pq` line 6: qci-category-82
- `corpus/pqc/assets/ssh/sshd_config_pq` line 6: qci-category-83
- `corpus/pqc/assets/ssh/sshd_config_pq` line 7: qci-category-84
- `corpus/pqc/assets/tls/nginx_pq.conf` line 14: qci-category-86
- `corpus/pqc/assets/tls/openssl_pq.cnf` line 13: qci-category-88
- `corpus/pqc/assets/tls/openssl_pq.cnf` line 13: qci-category-89
- `corpus/pqc/go/tls_hybrid/main.go` line 10: qci-category-90
- `corpus/pqc/java/PqParamSpec.java` line 9: qci-category-91
- `corpus/pqc/java/PqSignature.java` line 11: qci-category-92
- `corpus/system/payments-platform/edge/nginx/gateway.conf` line 9: qci-category-95
- `corpus/system/payments-platform/edge/nginx/gateway.conf` line 9: qci-category-96
- `corpus/system/payments-platform/edge/nginx/tls/gateway.key` line 1: qci-category-98
- `corpus/system/payments-platform/services/api-gateway/bin/api-gateway` line 12895: qci-category-99
- `corpus/system/payments-platform/services/api-gateway/bin/api-gateway` line 12895: qci-category-100
- `corpus/system/payments-platform/services/api-gateway/bin/api-gateway` line 12895: qci-category-101
- `corpus/system/payments-platform/services/api-gateway/bin/api-gateway` line 13300: qci-category-102
- `corpus/system/payments-platform/services/api-gateway/bin/api-gateway` line 13514: qci-category-103
- `corpus/system/payments-platform/services/api-gateway/bin/api-gateway` line 14665: qci-category-104
- `corpus/system/payments-platform/services/api-gateway/bin/api-gateway` line 14666: qci-category-105
- `corpus/system/payments-platform/services/api-gateway/bin/api-gateway` line 14666: qci-category-106
- `corpus/system/payments-platform/services/api-gateway/bin/api-gateway` line 14670: qci-category-107
- `corpus/system/payments-platform/services/api-gateway/bin/api-gateway` line 14670: qci-category-108
- `corpus/system/payments-platform/services/api-gateway/bin/api-gateway` line 16796: qci-category-109
- `corpus/system/payments-platform/services/api-gateway/bin/api-gateway` line 16796: qci-category-110
- `corpus/system/payments-platform/services/api-gateway/bin/api-gateway` line 16986: qci-category-111
- `corpus/tier1/c/t1_digests.c` line 18: qci-category-113
- `corpus/tier1/go/hashes/main.go` line 8: qci-category-114
- `corpus/tier1/go/hashes/main.go` line 17: qci-category-115
- `corpus/tier1/go/rc4/main.go` line 5: qci-category-116
- `corpus/tier1/go/rc4/main.go` line 10: qci-category-117
- `corpus/tier1/go/tls_config/main.go` line 10: qci-category-118
- `corpus/tier1/go/tls_config/main.go` line 14: qci-category-119
- `corpus/tier1/java/T1Hashes.java` line 13: qci-category-120
- `corpus/tier1/javascript/t1_aes_cbc.js` line 2: qci-category-121
- `corpus/tier1/javascript/t1_aes_gcm.js` line 2: qci-category-122
- `corpus/tier1/javascript/t1_chacha.js` line 2: qci-category-123
- `corpus/tier1/javascript/t1_dh.js` line 2: qci-category-124
- `corpus/tier1/javascript/t1_ec.js` line 2: qci-category-125
- `corpus/tier1/javascript/t1_hashes.js` line 2: qci-category-126
- `corpus/tier1/javascript/t1_hashes.js` line 8: qci-category-127
- `corpus/tier1/javascript/t1_mac_kdf.js` line 2: qci-category-128
- `corpus/tier1/javascript/t1_modern_curves.js` line 2: qci-category-129
- `corpus/tier1/javascript/t1_rsa.js` line 2: qci-category-130
- `corpus/tier1/javascript/t1_triple_des.js` line 2: qci-category-131
- `corpus/tier1/python/t1_hashes.py` line 9: qci-category-132
- `corpus/tier4/assets/keys/billing_service.pem` line 1: qci-category-139
- `corpus/tier4/assets/keys/treasury_hot_wallet.key` line 1: qci-category-140
- `corpus/tier4/assets/ssh/sshd_config` line 8: qci-category-141
- `corpus/tier4/assets/ssh/sshd_config` line 9: qci-category-142
- `corpus/tier4/assets/ssh/sshd_config` line 9: qci-category-143
- `corpus/tier4/assets/ssh/sshd_config` line 10: qci-category-144
- `corpus/tier4/assets/ssh/sshd_config` line 10: qci-category-145
- `corpus/tier4/assets/ssh/sshd_config` line 11: qci-category-146
- `corpus/tier4/assets/tls/application.yml` line 15: qci-category-147
- `corpus/tier4/assets/tls/nginx.conf` line 20: qci-category-150
- `corpus/tier4/assets/tls/nginx.conf` line 20: qci-category-151
- `corpus/tier4/assets/tls/nginx.conf` line 21: qci-category-152
- `corpus/tier4/assets/tls/nginx.conf` line 21: qci-category-153
- `corpus/tier4/assets/tls/nginx.conf` line 21: qci-category-154

## Crypto libraries (dependency manifests)

- Found in the right manifest: **27/28** (96.4%); found anywhere, including with no location: 27/28
- Direct dependencies: 95.8%; transitive (lockfile): 100.0%
- Versions correct, of found libraries the manifest pins (none reported counts as not correct): 84.6%
- PQC-capability verdicts (where the scanner gives one): none given
- False positives: 2

Missed, and the declared version has no ML-KEM/ML-DSA: org.bouncycastle:bcprov-jdk15on, bcpkix-jdk15on 1.70 (java-gateway)

Missed, with a support problem: org.bouncycastle:bcprov-jdk15on, bcpkix-jdk15on 1.70: superseded: last jdk15on release; the line continues as -jdk18on

| Manifest | Library | Declared | Scope | Found | Version |
|---|---|---|---|---|---|
| `python-billing/requirements.txt` | cryptography | 41.0.7 | direct | yes | ok |
| `python-billing/requirements.txt` | pycryptodome | 3.19.0 | direct | yes | ok |
| `python-billing/requirements.txt` | pyOpenSSL | 23.3.0 | direct | yes | ok |
| `python-billing/requirements.txt` | PyJWT | 2.8.0 | direct | yes | not reported |
| `python-billing/requirements.txt` | paramiko | 3.4.0 | direct | yes | ok |
| `python-billing/requirements.txt` | bcrypt | 4.1.2 | direct | yes | ok |
| `python-signer/pyproject.toml` | cryptography | range | direct | yes | n/a |
| `python-signer/pyproject.toml` | liboqs-python | 0.16.0 | direct | yes | ok |
| `java-gateway/pom.xml` | org.bouncycastle:bcprov-jdk15on, bcpkix-jdk15on | 1.70 | direct | no | n/a |
| `java-gateway/pom.xml` | com.nimbusds:nimbus-jose-jwt | 9.37.3 | direct | yes | ok |
| `java-gateway/pom.xml` | io.jsonwebtoken:jjwt-api | 0.12.5 | direct | yes | ok |
| `java-pq/build.gradle` | org.bouncycastle:bcprov-jdk18on, bctls-jdk18on | 1.80 | direct | yes | ok |
| `node-api/package.json` | jsonwebtoken | 9.0.2 | direct | yes | ok |
| `node-api/package.json` | crypto-js | 4.2.0 | direct | yes | ok |
| `node-api/package.json` | node-forge | 1.3.1 | direct | yes | ok |
| `node-api/package.json` | bcryptjs | 2.4.3 | direct | yes | ok |
| `node-api/package.json` | @noble/post-quantum | 0.5.4 | direct | yes | ok |
| `node-api/package-lock.json` | @noble/curves | 2.0.1 | transitive | yes | wrong: 2.0.0 |
| `node-api/package-lock.json` | @noble/hashes | 2.0.1 | transitive | yes | ok |
| `node-api/package-lock.json` | jws | 3.2.3 | transitive | yes | wrong: 3.2.2 |
| `node-api/package-lock.json` | jwa | 1.4.2 | transitive | yes | ok |
| `go-service/go.mod` | golang.org/x/crypto | 0.31.0 | direct | yes | ok |
| `go-service/go.mod` | github.com/cloudflare/circl | 1.6.1 | direct | yes | ok |
| `go-service/go.mod` | github.com/golang-jwt/jwt/v5 | 5.2.1 | direct | yes | ok |
| `c-agent/conanfile.txt` | openssl | 1.1.1w | direct | yes | ok |
| `c-agent/conanfile.txt` | libsodium | 1.0.18 | direct | yes | ok |
| `corpus/system/payments-platform/services/settlement-worker/requirements.txt` | cryptography | 42.0.5 | direct | yes | not reported |
| `corpus/system/payments-platform/services/ledger-service/build.gradle` | org.bouncycastle:bcprov-jdk18on | 1.77 | direct | yes | ok |

- False positive (unexpected): bcrypt in `corpus/deps/node-api/package-lock.json`: manifest doesn't declare it

- False positive (unexpected): bcrypt in `corpus/deps/node-api/package.json`: manifest doesn't declare it

## Per-finding detail

| ID | Family | Detected | At primary site | Params | Line | Quantum flag |
|---|---|---|---|---|---|---|
| T1-PY-01 | MD5 | yes | yes | yes | yes | yes |
| T1-PY-02 | SHA-1 | yes | yes | yes | yes | yes |
| T1-PY-03 | SHA-256 | yes | yes | yes | yes | n/a |
| T1-PY-04 | SHA3-256 | NO | NO | n/a | n/a | n/a |
| T1-PY-05 | RSA | yes | yes | yes | yes | yes |
| T1-PY-06 | EC | yes | yes | yes | yes | yes |
| T1-PY-07 | DSA | yes | yes | yes | yes | yes |
| T1-PY-08 | AES | yes | yes | yes | yes | n/a |
| T1-PY-09 | AES | yes | yes | yes | yes | n/a |
| T1-PY-10 | 3DES | yes | yes | yes | yes | yes |
| T1-PY-11 | ChaCha20-Poly1305 | yes | yes | yes | yes | n/a |
| T1-PY-12 | Ed25519 | yes | yes | yes | yes | yes |
| T1-PY-13 | X25519 | yes | yes | yes | yes | yes |
| T1-PY-14 | DH | yes | yes | yes | yes | yes |
| T1-PY-15 | HMAC | yes | yes | yes | yes | n/a |
| T1-PY-16 | PBKDF2 | yes | yes | yes | yes | n/a |
| T1-JV-01 | MD5 | yes | yes | yes | yes | yes |
| T1-JV-02 | SHA-1 | yes | yes | yes | yes | yes |
| T1-JV-03 | SHA-256 | yes | yes | yes | yes | n/a |
| T1-JV-04 | SHA3-256 | NO | NO | n/a | n/a | n/a |
| T1-JV-05 | RSA | yes | yes | NO | yes | yes |
| T1-JV-06 | EC | yes | yes | NO | yes | yes |
| T1-JV-07 | DSA | yes | yes | NO | yes | yes |
| T1-JV-08 | AES | yes | yes | NO | yes | n/a |
| T1-JV-09 | AES | yes | yes | yes | yes | n/a |
| T1-JV-10 | DES | yes | yes | yes | yes | yes |
| T1-JV-11 | 3DES | yes | yes | yes | yes | yes |
| T1-JV-12 | Ed25519 | yes | yes | yes | yes | yes |
| T1-JV-13 | X25519 | yes | yes | yes | yes | yes |
| T1-JV-14 | DH | yes | yes | NO | yes | yes |
| T1-JV-15 | HMAC | yes | yes | yes | yes | n/a |
| T1-JV-16 | PBKDF2 | yes | yes | yes | yes | n/a |
| T2-PY-01 | SHA-1 | yes | yes | yes | yes | yes |
| T2-PY-02 | RSA | yes | yes | yes | yes | yes |
| T2-PY-03 | AES | yes | NO | yes | yes | n/a |
| T2-PY-04 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T2-PY-05 | AES | yes | yes | yes | yes | n/a |
| T2-PY-06 | MD5 | yes | yes | yes | yes | yes |
| T2-PY-07 | SHA-256 | yes | yes | yes | yes | n/a |
| T2-PY-08 | HMAC | yes | yes | yes | yes | yes |
| T2-PY-09 | EC | yes | yes | NO | yes | yes |
| T2-JV-01 | 3DES | yes | yes | yes | yes | yes |
| T2-JV-02 | RSA | yes | NO | yes | yes | yes |
| T2-JV-03 | MD5 | yes | yes | yes | yes | yes |
| T2-JV-04 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T2-JV-05 | SHA-256 | NO | NO | n/a | n/a | n/a |
| T2-JV-06 | AES | yes | yes | yes | yes | n/a |
| T2-JV-07 | DSA | yes | yes | yes | yes | yes |
| T2-JV-08 | EC | yes | yes | NO | yes | yes |
| T3-PY-01 | RSA | yes | yes | NO | yes | yes |
| T3-PY-02 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T3-PY-03 | AES | yes | yes | NO | yes | n/a |
| T3-PY-04 | RSA | yes | NO | NO | yes | yes |
| T3-PY-05 | RSA | yes | NO | NO | yes | yes |
| T3-PY-06 | AES | yes | yes | NO | yes | n/a |
| T3-PY-07 | ChaCha20-Poly1305 | yes | yes | yes | yes | n/a |
| T3-PY-08 | MD5 | NO | NO | n/a | n/a | n/a |
| T3-PY-09 | HMAC | yes | yes | NO | yes | n/a |
| T3-JV-01 | RSA | yes | yes | NO | yes | yes |
| T3-JV-02 | SHA-1 | yes | yes | yes | yes | yes |
| T3-JV-03 | AES | yes | yes | NO | yes | n/a |
| T3-JV-04 | AES | yes | yes | NO | yes | n/a |
| T3-JV-05 | 3DES | yes | yes | yes | yes | yes |
| T3-JV-06 | MD5 | NO | NO | n/a | n/a | n/a |
| T3-JV-07 | HMAC | NO | NO | n/a | n/a | n/a |
| T4-AS-01 | RSA | yes | yes | yes | n/a | yes |
| T4-AS-02 | SHA-256 | NO | NO | n/a | n/a | n/a |
| T4-AS-03 | RSA | yes | yes | yes | n/a | yes |
| T4-AS-04 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T4-AS-05 | EC | yes | yes | NO | n/a | yes |
| T4-AS-06 | SHA-256 | NO | NO | n/a | n/a | n/a |
| T4-AS-07 | Ed25519 | yes | yes | yes | n/a | yes |
| T4-AS-08 | EC | yes | yes | yes | n/a | yes |
| T4-AS-09 | SHA-384 | NO | NO | n/a | n/a | n/a |
| T4-AS-10 | RSA | yes | yes | yes | n/a | yes |
| T4-AS-11 | SHA-256 | NO | NO | n/a | n/a | n/a |
| T4-AS-12 | RSA | NO | NO | n/a | n/a | n/a |
| T4-AS-13 | SHA-512 | NO | NO | n/a | n/a | n/a |
| T4-AS-14 | RSA | yes | yes | yes | n/a | yes |
| T4-AS-15 | EC | yes | yes | NO | n/a | yes |
| T4-AS-16 | PBKDF2 | NO | NO | n/a | n/a | n/a |
| T4-AS-17 | AES | NO | NO | n/a | n/a | n/a |
| T4-AS-18 | RSA | yes | yes | yes | NO | yes |
| T4-AS-19 | EC | yes | yes | yes | yes | yes |
| T4-AS-20 | AES | NO | NO | n/a | n/a | n/a |
| T4-AS-21 | PBKDF2 | NO | NO | n/a | n/a | n/a |
| T4-AS-22 | RSA | NO | NO | n/a | n/a | n/a |
| T4-AS-23 | SHA-256 | NO | NO | n/a | n/a | n/a |
| T4-AS-24 | RSA | NO | NO | n/a | n/a | n/a |
| T4-AS-25 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T4-AS-26 | RSA | yes | yes | yes | yes | yes |
| T4-AS-27 | DH | yes | yes | NO | yes | yes |
| T4-AS-28 | X25519 | yes | yes | yes | yes | yes |
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
| T4-AS-45 | SHA-1 | yes | yes | yes | yes | yes |
| T4-AS-46 | TLS-1.0 | yes | yes | yes | yes | n/a |
| T4-AS-47 | EC | NO | NO | n/a | n/a | n/a |
| T4-AS-48 | SHA-384 | NO | NO | n/a | n/a | n/a |
| T5-PY-01 | SHA-1 | yes | yes | yes | yes | yes |
| T5-PY-02 | MD5 | NO | NO | n/a | n/a | n/a |
| T5-PY-03 | RSA | NO | NO | n/a | n/a | n/a |
| T5-PY-04 | AES | yes | yes | NO | yes | n/a |
| T5-PY-05 | RC4 | NO | NO | n/a | n/a | n/a |
| T5-PY-06 | SHA-256 | NO | NO | n/a | n/a | n/a |
| T5-PY-07 | RSA | NO | NO | n/a | n/a | n/a |
| T5-PY-08 | SHA-1 | yes | yes | yes | n/a | yes |
| T5-PY-09 | HMAC | NO | NO | n/a | n/a | n/a |
| T5-JV-01 | RSA | NO | NO | n/a | n/a | n/a |
| T5-JV-02 | 3DES | NO | NO | n/a | n/a | n/a |
| T5-JV-03 | MD5 | NO | NO | n/a | n/a | n/a |
| T5-JV-04 | TEA | NO | NO | n/a | n/a | n/a |
| T5-JV-05 | RSA | NO | NO | n/a | n/a | n/a |
| T5-JV-06 | AES | yes | yes | NO | n/a | n/a |
| T5-JV-07 | RSA | yes | yes | NO | n/a | yes |
| T5-JV-08 | SHA-1 | NO | NO | n/a | n/a | n/a |
| PQ-PY-01 | ML-KEM | yes | yes | NO | yes | n/a |
| PQ-PY-02 | ML-DSA | yes | yes | NO | yes | n/a |
| PQ-PY-03 | X25519 | yes | yes | yes | yes | yes |
| PQ-PY-04 | ML-KEM | yes | yes | NO | yes | n/a |
| PQ-PY-05 | ML-KEM | yes | yes | yes | yes | yes |
| PQ-PY-06 | EC | yes | yes | yes | yes | yes |
| PQ-JV-01 | ML-KEM | yes | yes | yes | yes | yes |
| PQ-JV-02 | ML-DSA | yes | yes | yes | yes | yes |
| PQ-JV-03 | ML-DSA | yes | yes | NO | yes | n/a |
| PQ-JV-04 | EC | yes | yes | NO | yes | yes |
| PQ-AS-01 | ML-DSA | yes | yes | yes | n/a | yes |
| PQ-AS-02 | ML-DSA | yes | yes | yes | n/a | yes |
| PQ-AS-03 | ML-DSA | yes | yes | yes | n/a | yes |
| PQ-AS-04 | RSA | yes | yes | yes | n/a | yes |
| PQ-AS-05 | SHA-256 | yes | yes | yes | n/a | n/a |
| PQ-AS-06 | ML-KEM | yes | yes | yes | n/a | yes |
| PQ-AS-07 | ML-DSA | yes | yes | yes | n/a | yes |
| PQ-AS-08 | TLS-1.3 | yes | yes | yes | yes | n/a |
| PQ-AS-09 | X25519MLKEM768 | yes | yes | yes | yes | n/a |
| PQ-AS-10 | X25519 | yes | yes | yes | yes | yes |
| PQ-AS-11 | SecP384r1MLKEM1024 | NO | NO | n/a | n/a | n/a |
| PQ-AS-12 | X25519MLKEM768 | yes | yes | yes | yes | n/a |
| PQ-AS-13 | EC | yes | yes | yes | yes | yes |
| PQ-AS-14 | TLS-1.3 | yes | yes | yes | yes | n/a |
| PQ-AS-15 | X25519MLKEM768 | yes | yes | yes | yes | n/a |
| PQ-AS-16 | sntrup761x25519 | yes | yes | yes | yes | n/a |
| PQ-AS-17 | X25519 | yes | yes | yes | yes | yes |
| PQ-AS-18 | Ed25519 | yes | yes | yes | yes | yes |
| PQ-AS-19 | ChaCha20-Poly1305 | yes | yes | yes | yes | n/a |
| PQ-AS-20 | TLS-1.3 | yes | yes | yes | yes | n/a |
| PQ-AS-21 | X25519 | yes | yes | yes | yes | yes |
| PQ-AS-22 | EC | yes | yes | yes | yes | yes |
| T1-GO-01 | MD5 | yes | yes | yes | yes | yes |
| T1-GO-02 | SHA-1 | yes | yes | yes | yes | yes |
| T1-GO-03 | SHA-256 | yes | yes | yes | yes | n/a |
| T1-GO-04 | SHA3-256 | NO | NO | n/a | n/a | n/a |
| T1-GO-05 | AES | yes | yes | NO | yes | n/a |
| T1-GO-06 | AES | yes | yes | NO | yes | n/a |
| T1-GO-07 | 3DES | yes | yes | NO | yes | yes |
| T1-GO-08 | DES | yes | yes | NO | yes | yes |
| T1-GO-09 | RC4 | NO | NO | n/a | n/a | n/a |
| T1-GO-10 | RSA | yes | yes | NO | NO | yes |
| T1-GO-11 | EC | yes | yes | NO | yes | yes |
| T1-GO-12 | Ed25519 | yes | yes | yes | yes | yes |
| T1-GO-13 | X25519 | yes | yes | yes | yes | yes |
| T1-GO-14 | DSA | yes | yes | NO | yes | yes |
| T1-GO-15 | HMAC | yes | yes | yes | yes | n/a |
| T1-GO-16 | PBKDF2 | yes | yes | NO | yes | n/a |
| T1-GO-17 | TLS-1.0 | NO | NO | n/a | n/a | n/a |
| T1-GO-18 | TLS_RSA_WITH_3DES_EDE_CBC_SHA | NO | NO | n/a | n/a | n/a |
| T1-GO-19 | TLS_RSA_WITH_AES_128_CBC_SHA | NO | NO | n/a | n/a | n/a |
| T1-GO-20 | TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 | NO | NO | n/a | n/a | n/a |
| T2-GO-01 | SHA-1 | yes | yes | yes | yes | yes |
| T2-GO-02 | RSA | yes | yes | NO | yes | yes |
| T2-GO-03 | EC | NO | NO | n/a | n/a | n/a |
| T2-GO-04 | HMAC | yes | yes | NO | yes | n/a |
| T2-GO-05 | AES | yes | yes | NO | yes | n/a |
| T2-GO-06 | 3DES | yes | yes | NO | yes | yes |
| PQ-GO-01 | ML-KEM | yes | yes | yes | yes | yes |
| PQ-GO-02 | TLS-1.3 | NO | NO | n/a | n/a | n/a |
| PQ-GO-03 | X25519MLKEM768 | NO | NO | n/a | n/a | n/a |
| PQ-GO-04 | X25519 | NO | NO | n/a | n/a | n/a |
| T1-JS-01 | MD5 | NO | NO | n/a | n/a | n/a |
| T1-JS-02 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T1-JS-03 | SHA-256 | yes | yes | yes | yes | n/a |
| T1-JS-04 | SHA3-256 | NO | NO | n/a | n/a | n/a |
| T1-JS-05 | AES | yes | yes | NO | yes | n/a |
| T1-JS-06 | AES | yes | yes | NO | yes | n/a |
| T1-JS-07 | 3DES | yes | yes | NO | yes | yes |
| T1-JS-08 | ChaCha20-Poly1305 | yes | yes | yes | yes | n/a |
| T1-JS-09 | RSA | yes | yes | NO | yes | yes |
| T1-JS-10 | EC | yes | yes | yes | yes | yes |
| T1-JS-11 | Ed25519 | yes | yes | yes | yes | yes |
| T1-JS-12 | X25519 | yes | yes | yes | yes | yes |
| T1-JS-13 | DH | yes | yes | NO | yes | yes |
| T1-JS-14 | HMAC | yes | yes | NO | NO | n/a |
| T1-JS-15 | PBKDF2 | yes | yes | NO | NO | n/a |
| T1-JS-16 | RSA | yes | yes | NO | yes | yes |
| T1-JS-17 | SHA-1 | yes | yes | yes | NO | yes |
| T2-TS-01 | 3DES | NO | NO | n/a | n/a | n/a |
| T2-TS-02 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T2-TS-03 | RSA | yes | yes | NO | yes | yes |
| T2-TS-04 | EC | yes | yes | NO | yes | yes |
| T2-TS-05 | AES | NO | NO | n/a | n/a | n/a |
| T2-TS-06 | AES | NO | NO | n/a | n/a | n/a |
| T2-TS-07 | HMAC | yes | yes | NO | yes | n/a |
| T1-C-01 | MD5 | yes | yes | yes | yes | yes |
| T1-C-02 | SHA-1 | yes | yes | yes | yes | yes |
| T1-C-03 | SHA-256 | yes | yes | yes | yes | n/a |
| T1-C-04 | SHA3-256 | NO | NO | n/a | n/a | n/a |
| T1-C-05 | AES | yes | yes | NO | yes | n/a |
| T1-C-06 | AES | yes | yes | NO | yes | n/a |
| T1-C-07 | 3DES | yes | yes | NO | yes | yes |
| T1-C-08 | ChaCha20-Poly1305 | yes | yes | yes | yes | n/a |
| T1-C-09 | RSA | yes | yes | NO | yes | yes |
| T1-C-10 | RSA | yes | yes | NO | yes | yes |
| T1-C-11 | EC | yes | yes | NO | yes | yes |
| T1-C-12 | Ed25519 | NO | NO | n/a | n/a | n/a |
| T1-C-13 | X25519 | yes | yes | yes | yes | yes |
| T1-C-14 | DH | yes | yes | NO | yes | yes |
| T1-C-15 | HMAC | yes | yes | yes | yes | n/a |
| T1-C-16 | PBKDF2 | yes | yes | NO | yes | n/a |
| T1-C-17 | TLS-1.0 | NO | NO | n/a | n/a | n/a |
| T1-C-18 | TLS_RSA_WITH_3DES_EDE_CBC_SHA | NO | NO | n/a | n/a | n/a |
| T1-C-19 | TLS_RSA_WITH_AES_128_CBC_SHA | NO | NO | n/a | n/a | n/a |
| T1-C-20 | TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 | NO | NO | n/a | n/a | n/a |
| T2-C-01 | AES | NO | NO | n/a | n/a | n/a |
| T2-C-02 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T2-C-03 | RSA | NO | NO | n/a | n/a | n/a |
| T2-C-04 | EC | NO | NO | n/a | n/a | n/a |
| T2-C-05 | HMAC | yes | yes | NO | yes | n/a |
| T2-C-06 | 3DES | yes | yes | NO | yes | yes |
| MX-PY-1a | PBKDF2 | yes | yes | yes | yes | n/a |
| MX-PY-1b | PBKDF2 | yes | yes | NO | yes | n/a |
| MX-PY-1c | HMAC | yes | yes | NO | yes | n/a |
| MX-PY-1d | AES | yes | yes | NO | yes | n/a |
| MX-PY-2a | DH | yes | yes | yes | yes | yes |
| MX-PY-2b | ML-DSA | yes | yes | NO | yes | n/a |
| MX-PY-2c | DH | yes | yes | NO | yes | yes |
| MX-PY-2d | ChaCha20-Poly1305 | yes | yes | yes | yes | n/a |
| MX-PY-3a | SHA-1 | yes | yes | yes | yes | yes |
| MX-PY-3b | HMAC | yes | yes | NO | yes | n/a |
| MX-PY-3c | EC | yes | yes | yes | yes | yes |
| MX-PY-3d | EC | yes | yes | yes | yes | yes |
| MX-JV-1a | DH | yes | yes | NO | yes | yes |
| MX-JV-1b | SHA-1 | yes | yes | yes | yes | yes |
| MX-JV-1c | DH | yes | yes | NO | yes | yes |
| MX-JV-1d | AES | yes | yes | NO | yes | n/a |
| MX-JV-2a | SHA-256 | yes | yes | yes | yes | n/a |
| MX-JV-2b | Ed25519 | NO | NO | n/a | n/a | n/a |
| MX-JV-2c | PBKDF2 | yes | yes | NO | yes | n/a |
| MX-JV-2d | PBKDF2 | yes | yes | yes | yes | n/a |
| MX-JV-3a | HMAC | yes | yes | yes | yes | n/a |
| MX-JV-3b | 3DES | yes | yes | NO | yes | yes |
| MX-JV-3c | ChaCha20-Poly1305 | yes | yes | yes | yes | n/a |
| MX-JV-3d | SHA-512 | NO | NO | n/a | n/a | n/a |
| MX-JV-3e | 3DES | yes | yes | yes | yes | yes |
| MX-GO-1a | PBKDF2 | yes | yes | NO | yes | n/a |
| MX-GO-1b | ML-KEM | yes | yes | yes | yes | yes |
| MX-GO-1c | RSA | yes | yes | NO | yes | yes |
| MX-GO-1d | RSA | yes | yes | NO | yes | yes |
| MX-GO-2a | PBKDF2 | yes | yes | yes | yes | n/a |
| MX-GO-2b | DES | yes | yes | NO | yes | yes |
| MX-GO-2c | PBKDF2 | yes | yes | NO | yes | n/a |
| MX-GO-2d | 3DES | yes | yes | NO | yes | yes |
| MX-GO-3a | RSA | yes | yes | NO | yes | yes |
| MX-GO-3b | RC4 | NO | NO | n/a | n/a | n/a |
| MX-GO-3c | HMAC | yes | yes | NO | yes | n/a |
| MX-GO-3d | Ed25519 | yes | yes | yes | yes | yes |
| MX-JS-1a | AES | NO | NO | n/a | n/a | n/a |
| MX-JS-1b | HMAC | yes | yes | yes | yes | n/a |
| MX-JS-1c | AES | NO | NO | n/a | n/a | n/a |
| MX-JS-2a | SHA3-256 | NO | NO | n/a | n/a | n/a |
| MX-JS-2b | PBKDF2 | yes | yes | NO | yes | n/a |
| MX-JS-2c | EC | yes | yes | NO | yes | yes |
| MX-JS-2d | EC | yes | yes | NO | yes | yes |
| MX-JS-2e | AES | NO | NO | n/a | n/a | n/a |
| MX-TS-1a | EC | yes | yes | NO | yes | yes |
| MX-TS-1b | HMAC | yes | yes | NO | yes | n/a |
| MX-TS-1c | AES | NO | NO | n/a | n/a | n/a |
| MX-TS-1d | RSA | yes | yes | NO | yes | yes |
| MX-C-1a | SHA-1 | yes | yes | yes | yes | yes |
| MX-C-1b | EC | yes | yes | NO | yes | yes |
| MX-C-1c | HMAC | yes | yes | NO | yes | n/a |
| MX-C-1d | X25519 | yes | yes | yes | yes | yes |
| MX-C-1e | HMAC | yes | yes | NO | yes | n/a |
| MX-C-2a | EC | NO | NO | n/a | n/a | n/a |
| MX-C-2b | AES | NO | NO | n/a | n/a | n/a |
| MX-C-2c | 3DES | yes | yes | NO | yes | yes |
| MX-C-2d | 3DES | NO | NO | n/a | n/a | n/a |
| MX-C-3a | AES | NO | NO | n/a | n/a | n/a |
| MX-C-3b | 3DES | yes | yes | NO | yes | yes |
| MX-C-3c | AES | yes | yes | NO | yes | n/a |
| MX-C-3d | DH | yes | yes | NO | yes | yes |
| SYS-GO-01 | RSA | yes | NO | NO | yes | yes |
| SYS-GO-02 | HMAC | yes | NO | NO | yes | n/a |
| SYS-GO-03 | SHA-256 | yes | yes | yes | yes | n/a |
| SYS-PY-01 | AES | yes | NO | NO | yes | n/a |
| SYS-PY-02 | HMAC | yes | NO | NO | yes | n/a |
| SYS-PY-03 | RSA | yes | yes | yes | n/a | yes |
| SYS-PY-04 | SHA-1 | NO | NO | n/a | n/a | n/a |
| SYS-JV-01 | EC | yes | NO | NO | yes | yes |
| SYS-JV-02 | SHA-1 | yes | yes | yes | yes | yes |
| SYS-AR-01 | EC | NO | NO | n/a | n/a | n/a |
| SYS-AR-02 | SHA-1 | NO | NO | n/a | n/a | n/a |
| SYS-AR-03 | RSA | yes | yes | yes | n/a | yes |
| SYS-AR-04 | HMAC | yes | yes | yes | n/a | n/a |
| SYS-AR-05 | SHA-1 | yes | yes | yes | n/a | yes |
| SYS-AR-06 | SHA-256 | yes | yes | yes | n/a | n/a |
| SYS-AS-01 | TLS-1.2 | yes | yes | yes | yes | n/a |
| SYS-AS-02 | TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 | NO | NO | n/a | n/a | n/a |
| SYS-AS-03 | TLS_RSA_WITH_AES_128_CBC_SHA | NO | NO | n/a | n/a | n/a |
| SYS-AS-04 | RSA | yes | yes | yes | n/a | yes |
| SYS-AS-05 | SHA-256 | NO | NO | n/a | n/a | n/a |
| SYS-AS-06 | RSA | yes | yes | NO | n/a | yes |
| SYS-AS-07 | EC | NO | NO | n/a | n/a | n/a |
| SYS-AS-08 | SHA-384 | NO | NO | n/a | n/a | n/a |
| SYS-AS-09 | EC | yes | yes | NO | yes | yes |
| SYS-AS-10 | RSA | yes | yes | NO | NO | yes |
| SYS-AS-11 | AES | NO | NO | n/a | n/a | n/a |
