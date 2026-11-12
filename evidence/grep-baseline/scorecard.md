# CBOM Testbench Scorecard: grep baseline

**Overall:** 275/410 findings detected (67.1% recall), 171 false positives (61.7% precision), parameters correct on 56.0% of detections.

Calibration cases (generated Tier 1-2 siblings of the hand-written cases; they feed the holdout's overfit gap and are not counted anywhere else here): 277/304 detected (91.1%), 18 false positives.

Password-gated findings (readable only by trying a well-known default password; scored separately, not in any number below): 0/2 detected.

| Bucket | Detected | Recall | 95% interval | At primary site | Params correct | Line accurate | Quantum flag | False pos. | Precision |
|---|---|---|---|---|---|---|---|---|---|
| Tier 1 c | 13/20 | 65.0% | 43.3–81.9% | 65.0% | 69.2% | 100.0% | 100.0% | 2 | 86.7% |
| Tier 1 csharp | 12/13 | 92.3% | 66.7–98.6% | 92.3% | 58.3% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 1 go | 14/20 | 70.0% | 48.1–85.5% | 70.0% | 42.9% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 1 java | 16/16 | 100.0% | 80.6–100.0% | 100.0% | 56.2% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 1 javascript | 14/17 | 82.4% | 59.0–93.8% | 82.4% | 85.7% | 100.0% | 100.0% | 1 | 93.3% |
| Tier 1 python | 16/16 | 100.0% | 80.6–100.0% | 100.0% | 75.0% | 100.0% | 100.0% | 3 | 84.2% |
| Tier 2 c | 5/6 | 83.3% | 43.6–97.0% (thin) | 83.3% | 60.0% | 100.0% | 100.0% | 1 | 83.3% |
| Tier 2 csharp | 5/6 | 83.3% | 43.6–97.0% (thin) | 83.3% | 40.0% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 2 go | 6/6 | 100.0% | 61.0–100.0% (thin) | 100.0% | 33.3% | 100.0% | 100.0% | 1 | 85.7% |
| Tier 2 java | 8/8 | 100.0% | 67.6–100.0% (thin) | 87.5% | 50.0% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 2 python | 9/9 | 100.0% | 70.1–100.0% (thin) | 88.9% | 55.6% | 88.9% | 100.0% | 0 | 100.0% |
| Tier 2 typescript | 6/7 | 85.7% | 48.7–97.4% (thin) | 85.7% | 50.0% | 100.0% | 100.0% | 1 | 85.7% |
| Tier 3 java | 7/7 | 100.0% | 64.6–100.0% (thin) | 42.9% | 42.9% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 3 python | 9/9 | 100.0% | 70.1–100.0% (thin) | 55.6% | 33.3% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 4 assets | 23/66 | 34.8% | 24.5–46.9% | 34.8% | 69.6% | 95.5% | 100.0% | 4 | 85.2% |
| Tier 5 c | 7/11 | 63.6% | 35.4–84.8% | 63.6% | 57.1% | n/a | 100.0% | 1 | 87.5% |
| Tier 5 java | 0/11 | 0.0% | 0.0–25.9% | 0.0% | n/a | n/a | n/a | 0 | n/a |
| Tier 5 javascript | 8/11 | 72.7% | 43.4–90.3% | 72.7% | 75.0% | 100.0% | 100.0% | 1 | 88.9% |
| Tier 5 python | 0/9 | 0.0% | 0.0–29.9% (thin) | 0.0% | n/a | n/a | n/a | 0 | n/a |
| Dead code c | 1/2 | 50.0% | 9.5–90.5% (thin) | 50.0% | 100.0% | 100.0% | 100.0% | 1 | 50.0% |
| Dead code go | 1/2 | 50.0% | 9.5–90.5% (thin) | 50.0% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| Dead code java | 2/2 | 100.0% | 34.2–100.0% (thin) | 100.0% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| Dead code javascript | 1/2 | 50.0% | 9.5–90.5% (thin) | 50.0% | 100.0% | 100.0% | 100.0% | 1 | 50.0% |
| Dead code python | 2/2 | 100.0% | 34.2–100.0% (thin) | 100.0% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| Mixed files c | 9/13 | 69.2% | 42.4–87.3% | 69.2% | 44.4% | 100.0% | 100.0% | 15 | 37.5% |
| Mixed files go | 11/12 | 91.7% | 64.6–98.5% | 91.7% | 18.2% | 100.0% | 100.0% | 11 | 50.0% |
| Mixed files java | 12/13 | 92.3% | 66.7–98.6% | 92.3% | 41.7% | 100.0% | 100.0% | 18 | 40.0% |
| Mixed files javascript | 8/8 | 100.0% | 67.6–100.0% (thin) | 100.0% | 50.0% | 100.0% | 100.0% | 15 | 34.8% |
| Mixed files python | 12/12 | 100.0% | 75.7–100.0% | 100.0% | 25.0% | 100.0% | 100.0% | 18 | 40.0% |
| Mixed files typescript | 3/4 | 75.0% | 30.1–95.4% (thin) | 75.0% | 33.3% | 100.0% | 100.0% | 6 | 33.3% |
| PQC assets | 10/27 | 37.0% | 21.5–55.8% | 37.0% | 90.0% | 100.0% | 100.0% | 1 | 90.9% |
| PQC go | 2/4 | 50.0% | 15.0–85.0% (thin) | 50.0% | 50.0% | 100.0% | 100.0% | 0 | 100.0% |
| PQC java | 4/6 | 66.7% | 30.0–90.3% (thin) | 66.7% | 25.0% | 100.0% | 100.0% | 4 | 50.0% |
| PQC python | 6/7 | 85.7% | 48.7–97.4% (thin) | 85.7% | 33.3% | 100.0% | 100.0% | 2 | 75.0% |
| System fixture artifacts | 4/6 | 66.7% | 30.0–90.3% (thin) | 66.7% | 100.0% | n/a | 100.0% | 3 | 57.1% |
| System fixture assets | 2/11 | 18.2% | 5.1–47.7% | 18.2% | 50.0% | 100.0% | 100.0% | 0 | 100.0% |
| System fixture go | 3/3 | 100.0% | 43.8–100.0% (thin) | 33.3% | 33.3% | 100.0% | 100.0% | 0 | 100.0% |
| System fixture java | 2/2 | 100.0% | 34.2–100.0% (thin) | 50.0% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| System fixture python | 2/4 | 50.0% | 15.0–85.0% (thin) | 0.0% | 50.0% | 100.0% | 100.0% | 0 | 100.0% |
| **Total** | 275/410 | 67.1% | 62.4–71.4% | 63.4% | 56.0% | 99.2% | 100.0% | 171 | 61.7% |
| Negative controls | | | | | | | | 60 | |

Intervals are 95% Wilson intervals on recall. 23 bucket(s) have fewer than 10 findings and are marked thin: read their rates as indications, not measurements.

**PQC over-claims: 28.** Post-quantum or hybrid algorithms reported where the code or config has none. Each one makes migration look further along than it is. Any number above zero should be explained by the vendor before purchase.

**PQC by standard name: 10/10 (100.0%).** Detected post-quantum findings reported under the FIPS 203/204/205 name or OID. Reports that only say Kyber, Dilithium, SPHINCS+ or Falcon keep their recall credit and fail this check.

## System fixture: routing and asset links

**Routable: 8/13 detected system findings (61.5%)** (of 26). Routable means a reported location resolves, through the fixture's CODEOWNERS, to the team that owns the fix. Reporting only the shared wrapper or its config is detection, but the ticket lands with platform-security.

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

**Deadline-weighted recall: 67.2%** (at primary site: 62.8%). **Findings due by end of 2030 that this scanner missed: 44.**

| When it's due | Weight | Detected | Recall | At primary site |
|---|---|---|---|---|
| Due now (not approved or past its date) | 5 | 68/103 | 66.0% | 62.1% |
| Due by end of 2030 | 4 | 33/42 | 78.6% | 69.0% |
| Due 2031 to 2033 | 3 | 0/0 | n/a | n/a |
| Due 2034 to 2035 | 2 | 66/112 | 58.9% | 56.2% |
| No deadline (approved, review, out of scope, unknown) | 1 | 108/153 | 70.6% | 68.0% |

| Missed | Algorithm | Due | File |
|---|---|---|---|
| T4-AS-03 | RSA-1024 | 2013-12-31 | `corpus/tier4/assets/certs/payments_legacy.crt` |
| T4-AS-04 | SHA-1 | 2030-12-31 | `corpus/tier4/assets/certs/payments_legacy.crt` |
| T4-AS-24 | RSA-1024 | 2013-12-31 | `corpus/tier4/assets/keystores/partner_truststore.jks` |
| T4-AS-25 | SHA-1 | 2030-12-31 | `corpus/tier4/assets/keystores/partner_truststore.jks` |
| T4-AS-38 | TLS_RSA_WITH_3DES_EDE_CBC_SHA | **now** | `corpus/tier4/assets/tls/nginx.conf` |
| T4-AS-44 | RSA-1024 | 2013-12-31 | `corpus/tier4/assets/tls/openssl.cnf` |
| T4-AS-53 | TLS_RSA_WITH_3DES_EDE_CBC_SHA | **now** | `corpus/tier4/assets/tls/httpd-ssl.conf` |
| T4-AS-58 | TLS_CHACHA20_POLY1305_SHA256 | **now** | `corpus/tier4/assets/tls/haproxy.cfg` |
| T4-AS-59 | DH-1024 | 2013-12-31 | `corpus/tier4/assets/tls/haproxy.cfg` |
| T4-AS-66 | HMAC-SHA-1 | 2030-12-31 | `corpus/tier4/assets/ipsec/ipsec.conf` |
| T4-AS-67 | DH-1024 | 2013-12-31 | `corpus/tier4/assets/ipsec/ipsec.conf` |
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
| T5-JS-06 | 3DES-CBC | 2023-12-31 | `corpus/tier5/javascript/dist/payments-sdk.min.js` |
| T5-JS-10 | DH-1024 | 2013-12-31 | `corpus/tier5/javascript/dist/webhook-relay.min.js` |
| T5-C-02 | 3DES-CBC | 2023-12-31 | `corpus/tier5/c/bin/meterd` |
| T1-GO-09 | RC4 | **now** | `corpus/tier1/go/rc4/main.go` |
| T1-GO-18 | TLS_RSA_WITH_3DES_EDE_CBC_SHA | **now** | `corpus/tier1/go/tls_config/main.go` |
| T1-JS-07 | 3DES-CBC | 2023-12-31 | `corpus/tier1/javascript/t1_triple_des.js` |
| T2-TS-01 | 3DES-CBC | 2023-12-31 | `corpus/tier2/typescript/t2_config_object.ts` |
| T1-C-07 | 3DES-CBC | 2023-12-31 | `corpus/tier1/c/t1_triple_des.c` |
| T1-C-18 | TLS_RSA_WITH_3DES_EDE_CBC_SHA | **now** | `corpus/tier1/c/t1_tls_ctx.c` |
| T2-C-06 | 3DES-ECB | 2023-12-31 | `corpus/tier2/c/t2_cipher_struct.c` |
| MX-GO-3b | RC4 | **now** | `corpus/mixed/go/invoice_gateway/main.go` |
| MX-C-2c | 3DES-ECB | 2023-12-31 | `corpus/mixed/c/policy_agent.c` |
| MX-C-2d | 3DES-CBC | 2023-12-31 | `corpus/mixed/c/policy_agent.c` |
| MX-C-3b | 3DES-CBC | 2023-12-31 | `corpus/mixed/c/audit_daemon.c` |
| SYS-PY-03 | RSA-1024 | 2013-12-31 | `corpus/system/payments-platform/services/settlement-worker/partner_ca.py` |
| SYS-PY-04 | SHA-1 | 2030-12-31 | `corpus/system/payments-platform/services/settlement-worker/partner_ca.py` |
| SYS-AR-02 | SHA-1 | 2030-12-31 | `corpus/system/payments-platform/services/ledger-service/build/libs/ledger-service.jar` |
| DC-GO-02 | RC4 | **now** | `corpus/deadcode/go/legacy/main.go` |
| DC-JS-02 | 3DES-CBC | 2023-12-31 | `corpus/deadcode/javascript/dead_paths.js` |
| DC-C-02 | 3DES-CBC | 2023-12-31 | `corpus/deadcode/c/dead_branches.c` |

## Actionability: could an engineer open a ticket from this?

Rubric `cbom-actionability-v1` (proposed; see `rubric/actionability.json`). Each detected finding is checked for the fields a migration ticket needs. Facts are checked against the real files.

**Ticket-ready: 141/275 detected findings (51.3%)**, meaning every must-have is present and correct. **Actionable recall: 34.4%** of all 410 expected findings were both found and ticket-ready. Field completeness across all checks: 36.9%.

| Check | Tier | Applies to | Passed | Rate |
|---|---|---|---|---|
| Exact location | must | 275 | 272 | 98.9% |
| Correct parameters | must | 167 | 46 | 27.5% |
| Primitive, where the family is ambiguous | must | 52 | 52 | 100.0% |
| Certificate expiry (correct) | must | 0 | 0 | n/a |
| Certificate subject (correct) | must | 0 | 0 | n/a |
| Key material type | must | 3 | 0 | 0.0% |
| Protocol version | must | 13 | 0 | 0.0% |
| OID | should | 255 | 0 | 0.0% |
| Crypto functions | should | 262 | 0 | 0.0% |
| Quantum security level (correct) | should | 261 | 185 | 70.9% |
| Code context | should | 107 | 0 | 0.0% |
| Providing library | should | 107 | 0 | 0.0% |
| Certificate issuer | should | 0 | 0 | n/a |
| Certificate start date | should | 0 | 0 | n/a |
| Certificate key and signature linked | should | 0 | 0 | n/a |
| Key format | should | 3 | 0 | 0.0% |
| Cipher suite in a protocol | should | 0 | 0 | n/a |

Detected but not ticket-ready (134), first 25:

| ID | Algorithm | Missing must-haves |
|---|---|---|
| T1-PY-08 | AES-128-ECB | Correct parameters |
| T1-PY-09 | AES-256-GCM | Correct parameters |
| T1-PY-15 | HMAC-SHA-256 | Correct parameters |
| T1-PY-16 | PBKDF2-HMAC-SHA-256 | Correct parameters |
| T1-JV-05 | RSA-3072 | Correct parameters |
| T1-JV-07 | DSA-2048 | Correct parameters |
| T1-JV-08 | AES-128-ECB | Correct parameters |
| T1-JV-09 | AES-256-GCM | Correct parameters |
| T1-JV-14 | DH-2048 | Correct parameters |
| T1-JV-15 | HMAC-SHA-256 | Correct parameters |
| T1-JV-16 | PBKDF2-HMAC-SHA-256 | Correct parameters |
| T2-PY-02 | RSA-1024 | Exact location, Correct parameters |
| T2-PY-03 | AES-128-CBC | Correct parameters |
| T2-PY-05 | AES-192-CBC | Correct parameters |
| T2-PY-08 | HMAC-SHA-1 | Correct parameters |
| T2-JV-01 | 3DES-CBC | Correct parameters |
| T2-JV-02 | RSA-1024 | Correct parameters |
| T2-JV-06 | AES-128-ECB | Correct parameters |
| T2-JV-07 | DSA-1024 | Correct parameters |
| T3-PY-01 | RSA-1024 | Correct parameters |
| T3-PY-03 | AES-128-GCM | Correct parameters |
| T3-PY-04 | RSA-1024 | Correct parameters |
| T3-PY-05 | RSA-3072 | Correct parameters |
| T3-PY-06 | AES-256-CBC | Correct parameters |
| T3-PY-09 | HMAC-SHA-256 | Correct parameters |

## Missed findings

| ID | File | Expected | Line |
|---|---|---|---|
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
| T4-AS-15 | `corpus/tier4/assets/keys/treasury_hot_wallet.key` | EC {'curve': 'secp256k1'} | file |
| T4-AS-16 | `corpus/tier4/assets/keys/backup_signing_encrypted.pem` | PBKDF2 {'hash': 'SHA-256'} | file |
| T4-AS-17 | `corpus/tier4/assets/keys/backup_signing_encrypted.pem` | AES {'key_size': 256, 'mode': 'CBC'} | file |
| T4-AS-19 | `corpus/tier4/assets/keys/jwks.json` | EC {'curve': 'P-256'} | 15 |
| T4-AS-20 | `corpus/tier4/assets/keystores/orders_keystore.p12` | AES {'key_size': 256, 'mode': 'CBC'} | file |
| T4-AS-21 | `corpus/tier4/assets/keystores/orders_keystore.p12` | PBKDF2 {'hash': 'SHA-256'} | file |
| T4-AS-24 | `corpus/tier4/assets/keystores/partner_truststore.jks` | RSA {'key_size': 1024} | file |
| T4-AS-25 | `corpus/tier4/assets/keystores/partner_truststore.jks` | SHA-1  | file |
| T4-AS-33 | `corpus/tier4/assets/ssh/deploy_id_ed25519` | Ed25519  | file |
| T4-AS-37 | `corpus/tier4/assets/tls/nginx.conf` | TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256  | 21 |
| T4-AS-38 | `corpus/tier4/assets/tls/nginx.conf` | TLS_RSA_WITH_3DES_EDE_CBC_SHA  | 21 |
| T4-AS-39 | `corpus/tier4/assets/tls/nginx.conf` | TLS_RSA_WITH_AES_256_CBC_SHA  | 21 |
| T4-AS-42 | `corpus/tier4/assets/tls/application.yml` | TLS_RSA_WITH_AES_128_CBC_SHA  | 15 |
| T4-AS-43 | `corpus/tier4/assets/tls/application.yml` | TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384  | 16 |
| T4-AS-44 | `corpus/tier4/assets/tls/openssl.cnf` | RSA {'key_size': 1024} | 16 |
| T4-AS-47 | `corpus/tier4/assets/k8s/ingress-tls-secret.yaml` | EC {'curve': 'P-384'} | file |
| T4-AS-48 | `corpus/tier4/assets/k8s/ingress-tls-secret.yaml` | SHA-384  | file |
| T4-AS-51 | `corpus/tier4/assets/tls/httpd-ssl.conf` | TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384  | 15 |
| T4-AS-52 | `corpus/tier4/assets/tls/httpd-ssl.conf` | TLS_RSA_WITH_AES_128_CBC_SHA  | 15 |
| T4-AS-53 | `corpus/tier4/assets/tls/httpd-ssl.conf` | TLS_RSA_WITH_3DES_EDE_CBC_SHA  | 15 |
| T4-AS-55 | `corpus/tier4/assets/tls/haproxy.cfg` | TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256  | 7 |
| T4-AS-56 | `corpus/tier4/assets/tls/haproxy.cfg` | TLS_RSA_WITH_AES_256_CBC_SHA  | 7 |
| T4-AS-57 | `corpus/tier4/assets/tls/haproxy.cfg` | TLS_AES_256_GCM_SHA384  | 8 |
| T4-AS-58 | `corpus/tier4/assets/tls/haproxy.cfg` | TLS_CHACHA20_POLY1305_SHA256  | 8 |
| T4-AS-59 | `corpus/tier4/assets/tls/haproxy.cfg` | DH {'key_size': 1024} | 5 |
| T4-AS-61 | `corpus/tier4/assets/ipsec/swanctl.conf` | HMAC {'hash': 'SHA-256'} | 7 |
| T4-AS-62 | `corpus/tier4/assets/ipsec/swanctl.conf` | DH {'key_size': 2048} | 7 |
| T4-AS-66 | `corpus/tier4/assets/ipsec/ipsec.conf` | HMAC {'hash': 'SHA-1'} | 12 |
| T4-AS-67 | `corpus/tier4/assets/ipsec/ipsec.conf` | DH {'key_size': 1024} | 12 |
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
| T5-JS-06 | `corpus/tier5/javascript/dist/payments-sdk.min.js` | 3DES {'mode': 'CBC'} | 1 |
| T5-JS-07 | `corpus/tier5/javascript/dist/payments-sdk.min.js` | EC {'curve': 'P-256'} | 1 |
| T5-JS-10 | `corpus/tier5/javascript/dist/webhook-relay.min.js` | DH {'key_size': 1024} | 1 |
| T5-C-02 | `corpus/tier5/c/bin/meterd` | 3DES {'mode': 'CBC'} | file |
| T5-C-07 | `corpus/tier5/c/bin/keyd` | EC {'curve': 'P-256'} | file |
| T5-C-08 | `corpus/tier5/c/bin/fwcheck` | SHA-512  | file |
| T5-C-10 | `corpus/tier5/c/bin/fwcheck` | DH {'key_size': 2048} | file |
| PQ-PY-07 | `corpus/pqc/python/firmware_verify_lms.py` | LMS  | 12 |
| PQ-JV-05 | `corpus/pqc/java/FirmwareSignLms.java` | LMS  | 19 |
| PQ-JV-06 | `corpus/pqc/java/UpdateSignXmss.java` | XMSS  | 16 |
| PQ-AS-01 | `corpus/pqc/assets/certs/release_root_mldsa.pem` | ML-DSA {'param_set': '65'} | file |
| PQ-AS-02 | `corpus/pqc/assets/certs/firmware_signing.pem` | ML-DSA {'param_set': '87'} | file |
| PQ-AS-03 | `corpus/pqc/assets/certs/migrated_leaf.pem` | ML-DSA {'param_set': '65'} | file |
| PQ-AS-04 | `corpus/pqc/assets/certs/migrated_leaf.pem` | RSA  | file |
| PQ-AS-05 | `corpus/pqc/assets/certs/migrated_leaf.pem` | SHA-256  | file |
| PQ-AS-06 | `corpus/pqc/assets/keys/kem_recipient_pub.pem` | ML-KEM {'param_set': '768'} | file |
| PQ-AS-07 | `corpus/pqc/assets/keys/attestation_signer.pem` | ML-DSA {'param_set': '44'} | file |
| PQ-AS-09 | `corpus/pqc/assets/tls/nginx_pq.conf` | X25519MLKEM768  | 14 |
| PQ-AS-11 | `corpus/pqc/assets/tls/openssl_pq.cnf` | SecP384r1MLKEM1024  | 13 |
| PQ-AS-12 | `corpus/pqc/assets/tls/openssl_pq.cnf` | X25519MLKEM768  | 13 |
| PQ-AS-15 | `corpus/pqc/assets/ssh/sshd_config_pq` | X25519MLKEM768  | 6 |
| PQ-AS-16 | `corpus/pqc/assets/ssh/sshd_config_pq` | sntrup761x25519  | 6 |
| PQ-AS-22 | `corpus/pqc/assets/tls/nginx_pq_washing.conf` | EC {'curve': 'P-256'} | 16 |
| PQ-AS-23 | `corpus/pqc/assets/keys/bootloader_lms_pub.pem` | LMS  | file |
| PQ-AS-24 | `corpus/pqc/assets/keys/update_xmss_pub.pem` | XMSS  | file |
| PQ-AS-25 | `corpus/pqc/assets/firmware/signing-policy.yaml` | LMS  | 7 |
| PQ-AS-26 | `corpus/pqc/assets/firmware/signing-policy.yaml` | XMSS  | 13 |
| T1-GO-04 | `corpus/tier1/go/hashes/main.go` | SHA3-256  | 17 |
| T1-GO-09 | `corpus/tier1/go/rc4/main.go` | RC4  | 10 |
| T1-GO-17 | `corpus/tier1/go/tls_config/main.go` | TLS-1.0  | 11 |
| T1-GO-18 | `corpus/tier1/go/tls_config/main.go` | TLS_RSA_WITH_3DES_EDE_CBC_SHA  | 13 |
| T1-GO-19 | `corpus/tier1/go/tls_config/main.go` | TLS_RSA_WITH_AES_128_CBC_SHA  | 14 |
| T1-GO-20 | `corpus/tier1/go/tls_config/main.go` | TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256  | 15 |
| PQ-GO-02 | `corpus/pqc/go/tls_hybrid/main.go` | TLS-1.3  | 11 |
| PQ-GO-03 | `corpus/pqc/go/tls_hybrid/main.go` | X25519MLKEM768  | 12 |
| T1-JS-07 | `corpus/tier1/javascript/t1_triple_des.js` | 3DES {'mode': 'CBC'} | 4 |
| T1-JS-10 | `corpus/tier1/javascript/t1_ec.js` | EC {'curve': 'P-256'} | 4 |
| T1-JS-13 | `corpus/tier1/javascript/t1_dh.js` | DH {'key_size': 2048} | 4 |
| T2-TS-01 | `corpus/tier2/typescript/t2_config_object.ts` | 3DES {'mode': 'CBC'} | 5 |
| T1-C-07 | `corpus/tier1/c/t1_triple_des.c` | 3DES {'mode': 'CBC'} | 12 |
| T1-C-11 | `corpus/tier1/c/t1_ec.c` | EC {'curve': 'P-256'} | 10 |
| T1-C-14 | `corpus/tier1/c/t1_dh.c` | DH {'key_size': 2048} | 7 |
| T1-C-17 | `corpus/tier1/c/t1_tls_ctx.c` | TLS-1.0  | 7 |
| T1-C-18 | `corpus/tier1/c/t1_tls_ctx.c` | TLS_RSA_WITH_3DES_EDE_CBC_SHA  | 8 |
| T1-C-19 | `corpus/tier1/c/t1_tls_ctx.c` | TLS_RSA_WITH_AES_128_CBC_SHA  | 8 |
| T1-C-20 | `corpus/tier1/c/t1_tls_ctx.c` | TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256  | 8 |
| T1-CS-07 | `corpus/tier1/csharp/KeyAgreement/Program.cs` | EC {'curve': 'P-384'} | 8 |
| T2-C-06 | `corpus/tier2/c/t2_cipher_struct.c` | 3DES {'mode': 'ECB'} | 10 |
| T2-CS-04 | `corpus/tier2/csharp/DispatchTable/Program.cs` | SHA-512  | 10 |
| MX-JV-3d | `corpus/mixed/java/OrderDefaultsModule.java` | SHA-512  | 269 |
| MX-GO-3b | `corpus/mixed/go/invoice_gateway/main.go` | RC4  | 198 |
| MX-TS-1a | `corpus/mixed/typescript/voucher_service.ts` | EC {'curve': 'P-256'} | 4 |
| MX-C-2c | `corpus/mixed/c/policy_agent.c` | 3DES {'mode': 'ECB'} | 66 |
| MX-C-2d | `corpus/mixed/c/policy_agent.c` | 3DES {'mode': 'CBC'} | 11 |
| MX-C-3b | `corpus/mixed/c/audit_daemon.c` | 3DES {'mode': 'CBC'} | 300 |
| MX-C-3d | `corpus/mixed/c/audit_daemon.c` | DH {'key_size': 3072} | 10 |
| SYS-PY-03 | `corpus/system/payments-platform/services/settlement-worker/partner_ca.py` | RSA {'key_size': 1024} | file |
| SYS-PY-04 | `corpus/system/payments-platform/services/settlement-worker/partner_ca.py` | SHA-1  | file |
| SYS-AR-01 | `corpus/system/payments-platform/services/ledger-service/build/libs/ledger-service.jar` | EC  | file |
| SYS-AR-02 | `corpus/system/payments-platform/services/ledger-service/build/libs/ledger-service.jar` | SHA-1  | file |
| SYS-AS-02 | `corpus/system/payments-platform/edge/nginx/gateway.conf` | TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384  | 9 |
| SYS-AS-03 | `corpus/system/payments-platform/edge/nginx/gateway.conf` | TLS_RSA_WITH_AES_128_CBC_SHA  | 9 |
| SYS-AS-04 | `corpus/system/payments-platform/edge/nginx/tls/gateway.crt` | RSA {'key_size': 2048} | file |
| SYS-AS-05 | `corpus/system/payments-platform/edge/nginx/tls/gateway.crt` | SHA-256  | file |
| SYS-AS-07 | `corpus/system/payments-platform/deploy/k8s/gateway-ingress-tls.yaml` | EC {'curve': 'P-384'} | file |
| SYS-AS-08 | `corpus/system/payments-platform/deploy/k8s/gateway-ingress-tls.yaml` | SHA-384  | file |
| SYS-AS-09 | `corpus/system/payments-platform/infra/terraform/kms.tf` | EC {'curve': 'P-256'} | 6 |
| SYS-AS-10 | `corpus/system/payments-platform/infra/terraform/kms.tf` | RSA {'key_size': 2048} | 12 |
| SYS-AS-11 | `corpus/system/payments-platform/infra/terraform/kms.tf` | AES {'key_size': 256, 'mode': 'GCM'} | 15 |
| DC-GO-02 | `corpus/deadcode/go/legacy/main.go` | RC4  | 18 |
| DC-JS-02 | `corpus/deadcode/javascript/dead_paths.js` | 3DES {'mode': 'CBC'} | 10 |
| DC-C-02 | `corpus/deadcode/c/dead_branches.c` | 3DES {'mode': 'CBC'} | 11 |

## Detected with wrong or missing parameters

| ID | Family | Expected params | Reported params |
|---|---|---|---|
| T1-PY-08 | AES | `{"key_size": 128, "mode": "ECB"}` | `{"mode": "ECB"}` |
| T1-PY-09 | AES | `{"key_size": 256, "mode": "GCM"}` | `{"key_size": 256}; {"key_size": 256}` |
| T1-PY-15 | HMAC | `{"hash": "SHA-256"}` | `{}; {}; {}; {}` |
| T1-PY-16 | PBKDF2 | `{"hash": "SHA-256"}` | `{}; {}` |
| T1-JV-05 | RSA | `{"key_size": 3072}` | `{}; {}` |
| T1-JV-07 | DSA | `{"key_size": 2048}` | `{}; {}; {}; {}; {}; {}` |
| T1-JV-08 | AES | `{"key_size": 128, "mode": "ECB"}` | `{"mode": "ECB"}; {"mode": "ECB"}; {"mode": "ECB"}` |
| T1-JV-09 | AES | `{"key_size": 256, "mode": "GCM"}` | `{"mode": "GCM"}; {"mode": "GCM"}; {"mode": "GCM"}` |
| T1-JV-14 | DH | `{"key_size": 2048}` | `{}; {}; {}` |
| T1-JV-15 | HMAC | `{"hash": "SHA-256"}` | `{}; {}; {}` |
| T1-JV-16 | PBKDF2 | `{"hash": "SHA-256"}` | `{}` |
| T2-PY-02 | RSA | `{"key_size": 1024}` | `{}` |
| T2-PY-03 | AES | `{"key_size": 128, "mode": "CBC"}` | `{}` |
| T2-PY-05 | AES | `{"key_size": 192, "mode": "CBC"}` | `{"mode": "CBC"}` |
| T2-PY-08 | HMAC | `{"hash": "SHA-1"}` | `{}; {}` |
| T2-JV-01 | 3DES | `{"mode": "CBC"}` | `{}` |
| T2-JV-02 | RSA | `{"key_size": 1024}` | `{}` |
| T2-JV-06 | AES | `{"key_size": 128, "mode": "ECB"}` | `{"mode": "ECB"}` |
| T2-JV-07 | DSA | `{"key_size": 1024}` | `{}; {}` |
| T3-PY-01 | RSA | `{"key_size": 1024}` | `{}; {}` |
| T3-PY-03 | AES | `{"key_size": 128, "mode": "GCM"}` | `{}; {}` |
| T3-PY-04 | RSA | `{"key_size": 1024}` | `{}; {}` |
| T3-PY-05 | RSA | `{"key_size": 3072}` | `{}; {}` |
| T3-PY-06 | AES | `{"key_size": 256, "mode": "CBC"}` | `{"mode": "CBC"}` |
| T3-PY-09 | HMAC | `{"hash": "SHA-256"}` | `{}; {}` |
| T3-JV-01 | RSA | `{"key_size": 1024}` | `{}` |
| T3-JV-03 | AES | `{"key_size": 128, "mode": "GCM"}` | `{"mode": "GCM"}` |
| T3-JV-04 | AES | `{"key_size": 256, "mode": "CBC"}` | `{"mode": "CBC"}; {"mode": "CBC"}; {"mode": "CBC"}; {"mode": "CBC"}; {"key_size": 256}` |
| T3-JV-07 | HMAC | `{"hash": "SHA-256"}` | `{}; {}; {}` |
| T4-AS-18 | RSA | `{"key_size": 2048}` | `{}` |
| T4-AS-27 | DH | `{"key_size": 2048}` | `{}` |
| T4-AS-29 | AES | `{"key_size": 128, "mode": "CBC"}` | `{"mode": "CBC"}` |
| T4-AS-31 | HMAC | `{"hash": "SHA-1"}` | `{}` |
| T4-AS-32 | RSA | `{"key_size": 2048}` | `{}` |
| T4-AS-60 | AES | `{"key_size": 256}` | `{}` |
| T4-AS-68 | AES | `{"key_size": 128}` | `{}` |
| T5-JS-05 | HMAC | `{"hash": "MD5"}` | `{}` |
| T5-JS-08 | PBKDF2 | `{"hash": "SHA-1"}` | `{}` |
| T5-C-03 | RSA | `{"key_size": 1024}` | `{}; {}` |
| T5-C-05 | HMAC | `{"hash": "MD5"}` | `{}` |
| T5-C-06 | AES | `{"key_size": 256, "mode": "GCM"}` | `{}` |
| PQ-PY-01 | ML-KEM | `{"param_set": "768"}` | `{}; {}` |
| PQ-PY-02 | ML-DSA | `{"param_set": "65"}` | `{}; {}` |
| PQ-PY-04 | ML-KEM | `{"param_set": "768"}` | `{}; {}` |
| PQ-PY-05 | ML-KEM | `{"param_set": "1024"}` | `{}; {}` |
| PQ-JV-01 | ML-KEM | `{"param_set": "1024"}` | `{}; {}` |
| PQ-JV-02 | ML-DSA | `{"param_set": "87"}` | `{}; {}` |
| PQ-JV-03 | ML-DSA | `{"param_set": "44"}` | `{}; {}` |
| PQ-AS-27 | EC | `{"curve": "P-384"}` | `{}` |
| T1-GO-05 | AES | `{"key_size": 256, "mode": "GCM"}` | `{}; {}` |
| T1-GO-06 | AES | `{"key_size": 128, "mode": "CBC"}` | `{}; {}; {}` |
| T1-GO-07 | 3DES | `{"mode": "CBC"}` | `{}` |
| T1-GO-08 | DES | `{"mode": "CBC"}` | `{}; {}; {}` |
| T1-GO-11 | EC | `{"curve": "P-256"}` | `{}; {}; {}` |
| T1-GO-14 | DSA | `{"key_size": 2048}` | `{}; {}; {}; {}; {}` |
| T1-GO-15 | HMAC | `{"hash": "SHA-256"}` | `{}; {}` |
| T1-GO-16 | PBKDF2 | `{"hash": "SHA-512"}` | `{}; {}` |
| T2-GO-03 | EC | `{"curve": "P-384"}` | `{}; {}` |
| T2-GO-04 | HMAC | `{"hash": "MD5"}` | `{}; {}` |
| T2-GO-05 | AES | `{"key_size": 192, "mode": "CTR"}` | `{}; {}` |
| T2-GO-06 | 3DES | `{"mode": "CBC"}` | `{}` |
| PQ-GO-01 | ML-KEM | `{"param_set": "1024"}` | `{}; {}` |
| T1-JS-14 | HMAC | `{"hash": "SHA-256"}` | `{}; {}` |
| T1-JS-15 | PBKDF2 | `{"hash": "SHA-512"}` | `{}; {}` |
| T2-TS-03 | RSA | `{"key_size": 1024}` | `{}` |
| T2-TS-06 | AES | `{"key_size": 256, "mode": "GCM"}` | `{}` |
| T2-TS-07 | HMAC | `{"hash": "MD5"}` | `{}; {}` |
| T1-C-05 | AES | `{"key_size": 128, "mode": "ECB"}` | `{}` |
| T1-C-06 | AES | `{"key_size": 256, "mode": "GCM"}` | `{}` |
| T1-C-15 | HMAC | `{"hash": "SHA-256"}` | `{}; {}; {}` |
| T1-C-16 | PBKDF2 | `{"hash": "SHA-1"}` | `{}` |
| T1-CS-06 | EC | `{"curve": "P-256"}` | `{}` |
| T1-CS-09 | AES | `{"key_size": 256, "mode": "GCM"}` | `{"mode": "GCM"}` |
| T1-CS-10 | 3DES | `{"mode": "CBC"}` | `{}` |
| T1-CS-11 | HMAC | `{"hash": "SHA-256"}` | `{}` |
| T1-CS-12 | PBKDF2 | `{"hash": "SHA-512"}` | `{}` |
| T2-C-03 | RSA | `{"key_size": 1024}` | `{}; {}` |
| T2-C-05 | HMAC | `{"hash": "MD5"}` | `{}; {}` |
| T2-CS-01 | AES | `{"key_size": 192, "mode": "CBC"}` | `{}; {}; {}; {}; {}; {}` |
| T2-CS-05 | RSA | `{"key_size": 1024}` | `{}; {}; {}; {}` |
| T2-CS-06 | EC | `{"curve": "P-521"}` | `{}` |
| MX-PY-1a | PBKDF2 | `{"hash": "SHA-256"}` | `{}` |
| MX-PY-1b | PBKDF2 | `{"hash": "SHA-512"}` | `{}` |
| MX-PY-1c | HMAC | `{"hash": "SHA-512"}` | `{}; {}` |
| MX-PY-1d | AES | `{"key_size": 192, "mode": "CTR"}` | `{"mode": "CTR"}` |
| MX-PY-2a | DH | `{"key_size": 512}` | `{}` |
| MX-PY-2b | ML-DSA | `{"param_set": "65"}` | `{}` |
| MX-PY-2c | DH | `{"key_size": 1024}` | `{}` |
| MX-PY-3b | HMAC | `{"hash": "SHA-512"}` | `{}` |
| MX-PY-3c | EC | `{"curve": "P-256"}` | `{"curve": "P-521"}; {"curve": "P-521"}` |
| MX-JV-1a | DH | `{"key_size": 3072}` | `{}` |
| MX-JV-1c | DH | `{"key_size": 2048}` | `{}` |
| MX-JV-1d | AES | `{"key_size": 192, "mode": "ECB"}` | `{}; {}` |
| MX-JV-2c | PBKDF2 | `{"hash": "SHA-512"}` | `{}` |
| MX-JV-2d | PBKDF2 | `{"hash": "SHA-256"}` | `{}` |
| MX-JV-3a | HMAC | `{"hash": "SHA-256"}` | `{}` |
| MX-JV-3b | 3DES | `{"mode": "ECB"}` | `{"mode": "CBC"}; {"mode": "CBC"}` |
| MX-GO-1a | PBKDF2 | `{"hash": "SHA-512"}` | `{}` |
| MX-GO-1b | ML-KEM | `{"param_set": "768"}` | `{}` |
| MX-GO-1c | RSA | `{"key_size": 1024}` | `{"key_size": 2048}` |
| MX-GO-2a | PBKDF2 | `{"hash": "SHA-256"}` | `{}` |
| MX-GO-2b | DES | `{"mode": "CBC"}` | `{}` |
| MX-GO-2c | PBKDF2 | `{"hash": "SHA-1"}` | `{}` |
| MX-GO-2d | 3DES | `{"mode": "CBC"}` | `{}` |
| MX-GO-3a | RSA | `{"key_size": 2048}` | `{}` |
| MX-GO-3c | HMAC | `{"hash": "SHA-1"}` | `{}` |
| MX-JS-1b | HMAC | `{"hash": "SHA-512"}` | `{}` |
| MX-JS-1c | AES | `{"key_size": 256, "mode": "CTR"}` | `{"key_size": 128, "mode": "CBC"}` |
| MX-JS-2b | PBKDF2 | `{"hash": "SHA-512"}` | `{}` |
| MX-JS-2c | EC | `{"curve": "P-521"}` | `{"curve": "P-384"}` |
| MX-TS-1b | HMAC | `{"hash": "SHA-512"}` | `{}; {}` |
| MX-TS-1d | RSA | `{"key_size": 2048}` | `{}` |
| MX-C-1c | HMAC | `{"hash": "MD5"}` | `{}` |
| MX-C-1e | HMAC | `{"hash": "SHA-512"}` | `{}` |
| MX-C-2b | AES | `{"key_size": 192, "mode": "CBC"}` | `{}` |
| MX-C-3a | AES | `{"key_size": 192, "mode": "CBC"}` | `{}` |
| MX-C-3c | AES | `{"key_size": 128, "mode": "ECB"}` | `{}` |
| SYS-GO-01 | RSA | `{"key_size": 2048}` | `{}; {}; {}` |
| SYS-GO-02 | HMAC | `{"hash": "SHA-1"}` | `{}; {}; {}; {}; {}` |
| SYS-PY-02 | HMAC | `{"hash": "SHA-1"}` | `{}; {}; {}; {}` |
| SYS-AS-06 | RSA | `{"key_size": 2048}` | `{}; {}` |

## False positives

| File | Reported family | Lines | Negative control? |
|---|---|---|---|
| `corpus/deadcode/c/dead_branches.c` | DES | 11 | no |
| `corpus/deadcode/javascript/dead_paths.js` | DES | 10 | no |
| `corpus/deps/node-api/package-lock.json` | EC | 84, 86, 128 | no |
| `corpus/mixed/c/audit_daemon.c` | DES | 300 | no |
| `corpus/mixed/c/audit_daemon.c` | DSA | 97, 325 | no |
| `corpus/mixed/c/audit_daemon.c` | Ed25519 | 228 | no |
| `corpus/mixed/c/audit_daemon.c` | MD5 | 362 | no |
| `corpus/mixed/c/audit_daemon.c` | ML-DSA | 97, 325 | no |
| `corpus/mixed/c/audit_daemon.c` | PBKDF2 | 19, 283 | no |
| `corpus/mixed/c/audit_daemon.c` | RSA | 175 | no |
| `corpus/mixed/c/audit_daemon.c` | SHA-1 | 350 | no |
| `corpus/mixed/c/audit_daemon.c` | SHA3-256 | 218, 315 | no |
| `corpus/mixed/c/device_daemon.c` | DSA | 181 | no |
| `corpus/mixed/c/device_daemon.c` | ML-DSA | 181 | no |
| `corpus/mixed/c/device_daemon.c` | ML-KEM | 143, 312 | no |
| `corpus/mixed/c/policy_agent.c` | DES | 11, 66 | no |
| `corpus/mixed/c/policy_agent.c` | ML-KEM | 54 | no |
| `corpus/mixed/c/policy_agent.c` | RSA | 86 | no |
| `corpus/mixed/go/invoice_gateway/main.go` | 3DES | 76 | no |
| `corpus/mixed/go/invoice_gateway/main.go` | DSA | 28 | no |
| `corpus/mixed/go/invoice_gateway/main.go` | ML-DSA | 28 | no |
| `corpus/mixed/go/invoice_gateway/main.go` | ML-KEM | 266 | no |
| `corpus/mixed/go/invoice_gateway/main.go` | SHA3-256 | 207, 230 | no |
| `corpus/mixed/go/payload_worker/main.go` | EC | 258 | no |
| `corpus/mixed/go/payload_worker/main.go` | MD5 | 243 | no |
| `corpus/mixed/go/report_gateway/main.go` | EC | 114 | no |
| `corpus/mixed/go/report_gateway/main.go` | Ed25519 | 90 | no |
| `corpus/mixed/go/report_gateway/main.go` | RSA | 41 | no |
| `corpus/mixed/java/BookingOptionsModule.java` | ChaCha20-Poly1305 | 212 | no |
| `corpus/mixed/java/BookingOptionsModule.java` | EC | 80 | no |
| `corpus/mixed/java/BookingOptionsModule.java` | MD5 | 58 | no |
| `corpus/mixed/java/OrderDefaultsModule.java` | AES | 311 | no |
| `corpus/mixed/java/OrderDefaultsModule.java` | DSA | 70 | no |
| `corpus/mixed/java/OrderDefaultsModule.java` | Ed25519 | 51 | no |
| `corpus/mixed/java/OrderDefaultsModule.java` | MD5 | 55 | no |
| `corpus/mixed/java/OrderDefaultsModule.java` | ML-DSA | 70 | no |
| `corpus/mixed/java/OrderDefaultsModule.java` | PBKDF2 | 59 | no |
| `corpus/mixed/java/OrderDefaultsModule.java` | RSA | 248 | no |
| `corpus/mixed/java/VoucherProfileModule.java` | 3DES | 394 | no |
| `corpus/mixed/java/VoucherProfileModule.java` | ChaCha20-Poly1305 | 190, 219, 358, 400 | no |
| `corpus/mixed/java/VoucherProfileModule.java` | EC | 334 | no |
| `corpus/mixed/java/VoucherProfileModule.java` | Ed25519 | 49, 231 | no |
| `corpus/mixed/java/VoucherProfileModule.java` | HMAC | 170, 311 | no |
| `corpus/mixed/java/VoucherProfileModule.java` | MD5 | 485 | no |
| `corpus/mixed/java/VoucherProfileModule.java` | PBKDF2 | 166, 500 | no |
| `corpus/mixed/java/VoucherProfileModule.java` | SHA-256 | 170, 311 | no |
| `corpus/mixed/javascript/device_session.js` | DSA | 222, 299 | no |
| `corpus/mixed/javascript/device_session.js` | Ed25519 | 142 | no |
| `corpus/mixed/javascript/device_session.js` | MD5 | 81 | no |
| `corpus/mixed/javascript/device_session.js` | ML-DSA | 222 | no |
| `corpus/mixed/javascript/device_session.js` | RSA | 393 | no |
| `corpus/mixed/javascript/device_session.js` | SHA-1 | 278 | no |
| `corpus/mixed/javascript/partner_routes.js` | DSA | 128 | no |
| `corpus/mixed/javascript/partner_routes.js` | EC | 232 | no |
| `corpus/mixed/javascript/partner_routes.js` | Ed25519 | 88 | no |
| `corpus/mixed/javascript/partner_routes.js` | MD5 | 98, 161 | no |
| `corpus/mixed/javascript/partner_routes.js` | ML-DSA | 128 | no |
| `corpus/mixed/javascript/partner_routes.js` | ML-KEM | 237 | no |
| `corpus/mixed/javascript/partner_routes.js` | RSA | 222, 258 | no |
| `corpus/mixed/javascript/partner_routes.js` | SHA-1 | 177, 268 | no |
| `corpus/mixed/javascript/partner_routes.js` | SHA3-256 | 263 | no |
| `corpus/mixed/python/invoice_service.py` | AES | 114 | no |
| `corpus/mixed/python/invoice_service.py` | HMAC | 139 | no |
| `corpus/mixed/python/invoice_service.py` | SHA-1 | 134, 221 | no |
| `corpus/mixed/python/invoice_service.py` | SHA-256 | 139 | no |
| `corpus/mixed/python/invoice_service.py` | SHA3-256 | 52 | no |
| `corpus/mixed/python/metric_service.py` | DSA | 252 | no |
| `corpus/mixed/python/metric_service.py` | EC | 208 | no |
| `corpus/mixed/python/metric_service.py` | SHA-1 | 159 | no |
| `corpus/mixed/python/order_jobs.py` | 3DES | 154, 259 | no |
| `corpus/mixed/python/order_jobs.py` | AES | 144 | no |
| `corpus/mixed/python/order_jobs.py` | ChaCha20-Poly1305 | 376 | no |
| `corpus/mixed/python/order_jobs.py` | DSA | 56, 334 | no |
| `corpus/mixed/python/order_jobs.py` | MD5 | 268, 346 | no |
| `corpus/mixed/python/order_jobs.py` | ML-DSA | 334 | no |
| `corpus/mixed/python/order_jobs.py` | ML-KEM | 163, 302 | no |
| `corpus/mixed/python/order_jobs.py` | PBKDF2 | 329, 340, 370 | no |
| `corpus/mixed/python/order_jobs.py` | RSA | 273 | no |
| `corpus/mixed/python/order_jobs.py` | SHA3-256 | 33 | no |
| `corpus/mixed/typescript/voucher_service.ts` | ChaCha20-Poly1305 | 42, 92 | no |
| `corpus/mixed/typescript/voucher_service.ts` | Ed25519 | 119, 297 | no |
| `corpus/mixed/typescript/voucher_service.ts` | MD5 | 47, 128 | no |
| `corpus/mixed/typescript/voucher_service.ts` | ML-KEM | 32, 101 | no |
| `corpus/mixed/typescript/voucher_service.ts` | PBKDF2 | 180 | no |
| `corpus/mixed/typescript/voucher_service.ts` | SHA-1 | 17, 307 | no |
| `corpus/negatives/assets/cert-rotation-runbook.md` | AES | 19 | yes |
| `corpus/negatives/assets/cert-rotation-runbook.md` | DSA | 5 | yes |
| `corpus/negatives/assets/cert-rotation-runbook.md` | EC | 19 | yes |
| `corpus/negatives/assets/cert-rotation-runbook.md` | ML-DSA | 5 | yes |
| `corpus/negatives/assets/cert-rotation-runbook.md` | RSA | 3, 4 | yes |
| `corpus/negatives/assets/cert-rotation-runbook.md` | SHA-1 | 4 | yes |
| `corpus/negatives/assets/cert-rotation-runbook.md` | SHA-256 | 3, 19 | yes |
| `corpus/negatives/assets/cert-rotation-runbook.md` | TLS-1.2 | 18 | yes |
| `corpus/negatives/assets/cert-rotation-runbook.md` | TLS-1.3 | 18 | yes |
| `corpus/negatives/c/n_strings.c` | AES | 5 | yes |
| `corpus/negatives/c/n_strings.c` | DES | 5 | yes |
| `corpus/negatives/c/n_strings.c` | MD5 | 6 | yes |
| `corpus/negatives/c/n_strings.c` | ML-KEM | 6 | yes |
| `corpus/negatives/c/n_strings.c` | SHA-1 | 6 | yes |
| `corpus/negatives/csharp/StringsAndComments/Program.cs` | 3DES | 5 | yes |
| `corpus/negatives/csharp/StringsAndComments/Program.cs` | AES | 10 | yes |
| `corpus/negatives/csharp/StringsAndComments/Program.cs` | DES | 21, 24 | yes |
| `corpus/negatives/csharp/StringsAndComments/Program.cs` | EC | 22, 24 | yes |
| `corpus/negatives/csharp/StringsAndComments/Program.cs` | MD5 | 5 | yes |
| `corpus/negatives/csharp/StringsAndComments/Program.cs` | RSA | 9, 14, 24 | yes |
| `corpus/negatives/csharp/StringsAndComments/Program.cs` | SHA-1 | 11 | yes |
| `corpus/negatives/csharp/StringsAndComments/Program.cs` | SHA-256 | 16, 17, 24 | yes |
| `corpus/negatives/go/strings/main.go` | 3DES | 11 | yes |
| `corpus/negatives/go/strings/main.go` | DSA | 10 | yes |
| `corpus/negatives/go/strings/main.go` | MD5 | 10 | yes |
| `corpus/negatives/go/strings/main.go` | ML-DSA | 10 | yes |
| `corpus/negatives/go/strings/main.go` | ML-KEM | 11 | yes |
| `corpus/negatives/go/strings/main.go` | RSA | 10, 11 | yes |
| `corpus/negatives/go/strings/main.go` | SHA-1 | 10 | yes |
| `corpus/negatives/go/strings/main.go` | X25519 | 11 | yes |
| `corpus/negatives/java/NLookalikes.java` | AES | 12 | yes |
| `corpus/negatives/java/NLookalikes.java` | RSA | 5, 6, 8, 12, 24 | yes |
| `corpus/negatives/java/NLookalikes.java` | SHA-256 | 12, 14, 25 | yes |
| `corpus/negatives/java/NLookalikes.java` | SHA-384 | 12 | yes |
| `corpus/negatives/java/NStringsAndComments.java` | 3DES | 8 | yes |
| `corpus/negatives/java/NStringsAndComments.java` | AES | 7, 16 | yes |
| `corpus/negatives/java/NStringsAndComments.java` | DSA | 8 | yes |
| `corpus/negatives/java/NStringsAndComments.java` | EC | 8 | yes |
| `corpus/negatives/java/NStringsAndComments.java` | MD5 | 7, 16, 20, 21, 36 | yes |
| `corpus/negatives/java/NStringsAndComments.java` | ML-DSA | 8 | yes |
| `corpus/negatives/java/NStringsAndComments.java` | ML-KEM | 16 | yes |
| `corpus/negatives/java/NStringsAndComments.java` | RSA | 7, 16, 38 | yes |
| `corpus/negatives/java/NStringsAndComments.java` | SHA-1 | 7, 16, 18 | yes |
| `corpus/negatives/javascript/n_strings.js` | AES | 2 | yes |
| `corpus/negatives/javascript/n_strings.js` | ML-KEM | 2 | yes |
| `corpus/negatives/javascript/n_strings.js` | RSA | 2 | yes |
| `corpus/negatives/javascript/n_strings.js` | SHA-1 | 10 | yes |
| `corpus/negatives/python/n_strings_and_comments.py` | 3DES | 4 | yes |
| `corpus/negatives/python/n_strings_and_comments.py` | AES | 4, 16 | yes |
| `corpus/negatives/python/n_strings_and_comments.py` | DSA | 20 | yes |
| `corpus/negatives/python/n_strings_and_comments.py` | EC | 4 | yes |
| `corpus/negatives/python/n_strings_and_comments.py` | MD5 | 4, 18, 24 | yes |
| `corpus/negatives/python/n_strings_and_comments.py` | ML-DSA | 20 | yes |
| `corpus/negatives/python/n_strings_and_comments.py` | ML-KEM | 4, 19 | yes |
| `corpus/negatives/python/n_strings_and_comments.py` | RSA | 3, 15, 23, 50 | yes |
| `corpus/negatives/python/n_strings_and_comments.py` | SHA-1 | 4, 17, 29, 30 | yes |
| `corpus/negatives/python/n_test_vectors.py` | MD5 | 8 | yes |
| `corpus/negatives/python/n_test_vectors.py` | RSA | 14, 15, 21, 30 | yes |
| `corpus/negatives/python/n_test_vectors.py` | SHA-1 | 9 | yes |
| `corpus/negatives/python/n_test_vectors.py` | SHA-256 | 10 | yes |
| `corpus/pqc/assets/tls/nginx_pq_washing.conf` | ML-KEM | 6 | no |
| `corpus/pqc/java/PqParamSpec.java` | DSA | 6, 9 | no |
| `corpus/pqc/java/PqSignature.java` | DSA | 8, 11 | no |
| `corpus/pqc/java/PqWashing.java` | DH | 10 | no |
| `corpus/pqc/java/PqWashing.java` | ML-KEM | 7, 15, 20, 25, 26 | no |
| `corpus/pqc/python/pq_washing.py` | DH | 4 | no |
| `corpus/pqc/python/pq_washing.py` | ML-KEM | 1, 4, 12, 14, 17, 21, 22 | no |
| `corpus/system/payments-platform/services/api-gateway/bin/api-gateway` | 3DES | 14666 | no |
| `corpus/system/payments-platform/services/api-gateway/bin/api-gateway` | MD5 | 14661, 14666 | no |
| `corpus/system/payments-platform/services/api-gateway/bin/api-gateway` | ML-KEM | 14669 | no |
| `corpus/tier1/c/t1_tls_ctx.c` | DES | 8 | no |
| `corpus/tier1/c/t1_triple_des.c` | DES | 12 | no |
| `corpus/tier1/javascript/t1_triple_des.js` | DES | 4 | no |
| `corpus/tier1/python/t1_modern_curves.py` | ML-KEM | 5 | no |
| `corpus/tier1/python/t1_rsa.py` | DSA | 5 | no |
| `corpus/tier1/python/t1_rsa.py` | ML-DSA | 5 | no |
| `corpus/tier2/c/t2_cipher_struct.c` | DES | 10 | no |
| `corpus/tier2/go/block_factory/main.go` | DES | 6, 10 | no |
| `corpus/tier2/typescript/t2_config_object.ts` | DES | 5 | no |
| `corpus/tier4/assets/tls/httpd-ssl.conf` | DES | 15 | no |
| `corpus/tier4/assets/tls/httpd-ssl.conf` | SSL-2.0 | 11 | no |
| `corpus/tier4/assets/tls/nginx.conf` | DES | 18, 21 | no |
| `corpus/tier4/assets/tls/nginx.conf` | SSL-3.0 | 17 | no |
| `corpus/tier5/c/bin/meterd` | DES | 8 | no |
| `corpus/tier5/javascript/dist/payments-sdk.min.js` | DES | 1 | no |
| `corpus/mixed/go/report_gateway/main.go` | DES | 237 | no |

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
| T1-PY-01 | MD5 | yes | yes | yes | yes | yes |
| T1-PY-02 | SHA-1 | yes | yes | yes | yes | yes |
| T1-PY-03 | SHA-256 | yes | yes | yes | yes | yes |
| T1-PY-04 | SHA3-256 | yes | yes | yes | yes | yes |
| T1-PY-05 | RSA | yes | yes | yes | yes | yes |
| T1-PY-06 | EC | yes | yes | yes | yes | yes |
| T1-PY-07 | DSA | yes | yes | yes | yes | yes |
| T1-PY-08 | AES | yes | yes | NO | yes | n/a |
| T1-PY-09 | AES | yes | yes | NO | yes | yes |
| T1-PY-10 | 3DES | yes | yes | yes | yes | yes |
| T1-PY-11 | ChaCha20-Poly1305 | yes | yes | yes | yes | yes |
| T1-PY-12 | Ed25519 | yes | yes | yes | yes | yes |
| T1-PY-13 | X25519 | yes | yes | yes | yes | yes |
| T1-PY-14 | DH | yes | yes | yes | yes | yes |
| T1-PY-15 | HMAC | yes | yes | NO | yes | n/a |
| T1-PY-16 | PBKDF2 | yes | yes | NO | yes | n/a |
| T1-JV-01 | MD5 | yes | yes | yes | yes | yes |
| T1-JV-02 | SHA-1 | yes | yes | yes | yes | yes |
| T1-JV-03 | SHA-256 | yes | yes | yes | yes | yes |
| T1-JV-04 | SHA3-256 | yes | yes | yes | yes | yes |
| T1-JV-05 | RSA | yes | yes | NO | yes | yes |
| T1-JV-06 | EC | yes | yes | yes | yes | yes |
| T1-JV-07 | DSA | yes | yes | NO | yes | yes |
| T1-JV-08 | AES | yes | yes | NO | yes | n/a |
| T1-JV-09 | AES | yes | yes | NO | yes | n/a |
| T1-JV-10 | DES | yes | yes | yes | yes | yes |
| T1-JV-11 | 3DES | yes | yes | yes | yes | yes |
| T1-JV-12 | Ed25519 | yes | yes | yes | yes | yes |
| T1-JV-13 | X25519 | yes | yes | yes | yes | yes |
| T1-JV-14 | DH | yes | yes | NO | yes | yes |
| T1-JV-15 | HMAC | yes | yes | NO | yes | n/a |
| T1-JV-16 | PBKDF2 | yes | yes | NO | yes | n/a |
| T2-PY-01 | SHA-1 | yes | yes | yes | yes | yes |
| T2-PY-02 | RSA | yes | yes | NO | NO | yes |
| T2-PY-03 | AES | yes | NO | NO | yes | n/a |
| T2-PY-04 | SHA-1 | yes | yes | yes | yes | yes |
| T2-PY-05 | AES | yes | yes | NO | yes | n/a |
| T2-PY-06 | MD5 | yes | yes | yes | yes | yes |
| T2-PY-07 | SHA-256 | yes | yes | yes | yes | yes |
| T2-PY-08 | HMAC | yes | yes | NO | yes | n/a |
| T2-PY-09 | EC | yes | yes | yes | yes | yes |
| T2-JV-01 | 3DES | yes | yes | NO | yes | yes |
| T2-JV-02 | RSA | yes | NO | NO | yes | yes |
| T2-JV-03 | MD5 | yes | yes | yes | yes | yes |
| T2-JV-04 | SHA-1 | yes | yes | yes | yes | yes |
| T2-JV-05 | SHA-256 | yes | yes | yes | yes | yes |
| T2-JV-06 | AES | yes | yes | NO | yes | n/a |
| T2-JV-07 | DSA | yes | yes | NO | yes | yes |
| T2-JV-08 | EC | yes | yes | yes | yes | yes |
| T3-PY-01 | RSA | yes | yes | NO | yes | yes |
| T3-PY-02 | SHA-1 | yes | NO | yes | yes | yes |
| T3-PY-03 | AES | yes | yes | NO | yes | n/a |
| T3-PY-04 | RSA | yes | NO | NO | yes | yes |
| T3-PY-05 | RSA | yes | NO | NO | yes | yes |
| T3-PY-06 | AES | yes | yes | NO | yes | n/a |
| T3-PY-07 | ChaCha20-Poly1305 | yes | yes | yes | yes | yes |
| T3-PY-08 | MD5 | yes | NO | yes | yes | yes |
| T3-PY-09 | HMAC | yes | yes | NO | yes | n/a |
| T3-JV-01 | RSA | yes | yes | NO | yes | yes |
| T3-JV-02 | SHA-1 | yes | NO | yes | yes | yes |
| T3-JV-03 | AES | yes | NO | NO | yes | n/a |
| T3-JV-04 | AES | yes | yes | NO | yes | yes |
| T3-JV-05 | 3DES | yes | yes | yes | yes | yes |
| T3-JV-06 | MD5 | yes | NO | yes | yes | yes |
| T3-JV-07 | HMAC | yes | NO | NO | yes | n/a |
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
| T4-AS-15 | EC | NO | NO | n/a | n/a | n/a |
| T4-AS-16 | PBKDF2 | NO | NO | n/a | n/a | n/a |
| T4-AS-17 | AES | NO | NO | n/a | n/a | n/a |
| T4-AS-18 | RSA | yes | yes | NO | NO | yes |
| T4-AS-19 | EC | NO | NO | n/a | n/a | n/a |
| T4-AS-20 | AES | NO | NO | n/a | n/a | n/a |
| T4-AS-21 | PBKDF2 | NO | NO | n/a | n/a | n/a |
| T4-AS-24 | RSA | NO | NO | n/a | n/a | n/a |
| T4-AS-25 | SHA-1 | NO | NO | n/a | n/a | n/a |
| T4-AS-26 | RSA | yes | yes | yes | yes | yes |
| T4-AS-27 | DH | yes | yes | NO | yes | yes |
| T4-AS-28 | X25519 | yes | yes | yes | yes | yes |
| T4-AS-29 | AES | yes | yes | NO | yes | n/a |
| T4-AS-30 | ChaCha20-Poly1305 | yes | yes | yes | yes | yes |
| T4-AS-31 | HMAC | yes | yes | NO | yes | n/a |
| T4-AS-32 | RSA | yes | yes | NO | n/a | yes |
| T4-AS-33 | Ed25519 | NO | NO | n/a | n/a | n/a |
| T4-AS-34 | TLS-1.0 | yes | yes | yes | yes | n/a |
| T4-AS-35 | TLS-1.1 | yes | yes | yes | yes | n/a |
| T4-AS-36 | TLS-1.2 | yes | yes | yes | yes | n/a |
| T4-AS-37 | TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 | NO | NO | n/a | n/a | n/a |
| T4-AS-38 | TLS_RSA_WITH_3DES_EDE_CBC_SHA | NO | NO | n/a | n/a | n/a |
| T4-AS-39 | TLS_RSA_WITH_AES_256_CBC_SHA | NO | NO | n/a | n/a | n/a |
| T4-AS-40 | TLS-1.1 | yes | yes | yes | yes | n/a |
| T4-AS-41 | TLS-1.2 | yes | yes | yes | yes | n/a |
| T4-AS-42 | TLS_RSA_WITH_AES_128_CBC_SHA | NO | NO | n/a | n/a | n/a |
| T4-AS-43 | TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 | NO | NO | n/a | n/a | n/a |
| T4-AS-44 | RSA | NO | NO | n/a | n/a | n/a |
| T4-AS-45 | SHA-1 | yes | yes | yes | yes | yes |
| T4-AS-46 | TLS-1.0 | yes | yes | yes | yes | n/a |
| T4-AS-47 | EC | NO | NO | n/a | n/a | n/a |
| T4-AS-48 | SHA-384 | NO | NO | n/a | n/a | n/a |
| T4-AS-49 | TLS-1.1 | yes | yes | yes | yes | n/a |
| T4-AS-50 | TLS-1.2 | yes | yes | yes | yes | n/a |
| T4-AS-51 | TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 | NO | NO | n/a | n/a | n/a |
| T4-AS-52 | TLS_RSA_WITH_AES_128_CBC_SHA | NO | NO | n/a | n/a | n/a |
| T4-AS-53 | TLS_RSA_WITH_3DES_EDE_CBC_SHA | NO | NO | n/a | n/a | n/a |
| T4-AS-54 | TLS-1.1 | yes | yes | yes | yes | n/a |
| T4-AS-55 | TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256 | NO | NO | n/a | n/a | n/a |
| T4-AS-56 | TLS_RSA_WITH_AES_256_CBC_SHA | NO | NO | n/a | n/a | n/a |
| T4-AS-57 | TLS_AES_256_GCM_SHA384 | NO | NO | n/a | n/a | n/a |
| T4-AS-58 | TLS_CHACHA20_POLY1305_SHA256 | NO | NO | n/a | n/a | n/a |
| T4-AS-59 | DH | NO | NO | n/a | n/a | n/a |
| T4-AS-60 | AES | yes | yes | NO | yes | n/a |
| T4-AS-61 | HMAC | NO | NO | n/a | n/a | n/a |
| T4-AS-62 | DH | NO | NO | n/a | n/a | n/a |
| T4-AS-63 | ChaCha20-Poly1305 | yes | yes | yes | yes | yes |
| T4-AS-64 | X25519 | yes | yes | yes | yes | yes |
| T4-AS-65 | 3DES | yes | yes | yes | yes | yes |
| T4-AS-66 | HMAC | NO | NO | n/a | n/a | n/a |
| T4-AS-67 | DH | NO | NO | n/a | n/a | n/a |
| T4-AS-68 | AES | yes | yes | NO | yes | n/a |
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
| T5-JS-01 | MD5 | yes | yes | yes | yes | yes |
| T5-JS-02 | AES | yes | yes | yes | yes | yes |
| T5-JS-03 | RSA | yes | yes | yes | yes | yes |
| T5-JS-04 | SHA-1 | yes | yes | yes | yes | yes |
| T5-JS-05 | HMAC | yes | yes | NO | yes | n/a |
| T5-JS-06 | 3DES | NO | NO | n/a | n/a | n/a |
| T5-JS-07 | EC | NO | NO | n/a | n/a | n/a |
| T5-JS-08 | PBKDF2 | yes | yes | NO | yes | n/a |
| T5-JS-09 | AES | yes | yes | yes | yes | yes |
| T5-JS-10 | DH | NO | NO | n/a | n/a | n/a |
| T5-JS-11 | Ed25519 | yes | yes | yes | yes | yes |
| T5-C-01 | MD5 | yes | yes | yes | n/a | yes |
| T5-C-02 | 3DES | NO | NO | n/a | n/a | n/a |
| T5-C-03 | RSA | yes | yes | NO | n/a | yes |
| T5-C-04 | SHA-1 | yes | yes | yes | n/a | yes |
| T5-C-05 | HMAC | yes | yes | NO | n/a | n/a |
| T5-C-06 | AES | yes | yes | NO | n/a | n/a |
| T5-C-07 | EC | NO | NO | n/a | n/a | n/a |
| T5-C-08 | SHA-512 | NO | NO | n/a | n/a | n/a |
| T5-C-09 | AES | yes | yes | yes | n/a | yes |
| T5-C-10 | DH | NO | NO | n/a | n/a | n/a |
| T5-C-11 | X25519 | yes | yes | yes | n/a | yes |
| PQ-PY-01 | ML-KEM | yes | yes | NO | yes | n/a |
| PQ-PY-02 | ML-DSA | yes | yes | NO | yes | n/a |
| PQ-PY-03 | X25519 | yes | yes | yes | yes | yes |
| PQ-PY-04 | ML-KEM | yes | yes | NO | yes | n/a |
| PQ-PY-05 | ML-KEM | yes | yes | NO | yes | n/a |
| PQ-PY-06 | EC | yes | yes | yes | yes | yes |
| PQ-PY-07 | LMS | NO | NO | n/a | n/a | n/a |
| PQ-JV-01 | ML-KEM | yes | yes | NO | yes | n/a |
| PQ-JV-02 | ML-DSA | yes | yes | NO | yes | n/a |
| PQ-JV-03 | ML-DSA | yes | yes | NO | yes | n/a |
| PQ-JV-04 | EC | yes | yes | yes | yes | yes |
| PQ-JV-05 | LMS | NO | NO | n/a | n/a | n/a |
| PQ-JV-06 | XMSS | NO | NO | n/a | n/a | n/a |
| PQ-AS-01 | ML-DSA | NO | NO | n/a | n/a | n/a |
| PQ-AS-02 | ML-DSA | NO | NO | n/a | n/a | n/a |
| PQ-AS-03 | ML-DSA | NO | NO | n/a | n/a | n/a |
| PQ-AS-04 | RSA | NO | NO | n/a | n/a | n/a |
| PQ-AS-05 | SHA-256 | NO | NO | n/a | n/a | n/a |
| PQ-AS-06 | ML-KEM | NO | NO | n/a | n/a | n/a |
| PQ-AS-07 | ML-DSA | NO | NO | n/a | n/a | n/a |
| PQ-AS-08 | TLS-1.3 | yes | yes | yes | yes | n/a |
| PQ-AS-09 | X25519MLKEM768 | NO | NO | n/a | n/a | n/a |
| PQ-AS-10 | X25519 | yes | yes | yes | yes | yes |
| PQ-AS-11 | SecP384r1MLKEM1024 | NO | NO | n/a | n/a | n/a |
| PQ-AS-12 | X25519MLKEM768 | NO | NO | n/a | n/a | n/a |
| PQ-AS-13 | EC | yes | yes | yes | yes | yes |
| PQ-AS-14 | TLS-1.3 | yes | yes | yes | yes | n/a |
| PQ-AS-15 | X25519MLKEM768 | NO | NO | n/a | n/a | n/a |
| PQ-AS-16 | sntrup761x25519 | NO | NO | n/a | n/a | n/a |
| PQ-AS-17 | X25519 | yes | yes | yes | yes | yes |
| PQ-AS-18 | Ed25519 | yes | yes | yes | yes | yes |
| PQ-AS-19 | ChaCha20-Poly1305 | yes | yes | yes | yes | yes |
| PQ-AS-20 | TLS-1.3 | yes | yes | yes | yes | n/a |
| PQ-AS-21 | X25519 | yes | yes | yes | yes | yes |
| PQ-AS-22 | EC | NO | NO | n/a | n/a | n/a |
| PQ-AS-23 | LMS | NO | NO | n/a | n/a | n/a |
| PQ-AS-24 | XMSS | NO | NO | n/a | n/a | n/a |
| PQ-AS-25 | LMS | NO | NO | n/a | n/a | n/a |
| PQ-AS-26 | XMSS | NO | NO | n/a | n/a | n/a |
| PQ-AS-27 | EC | yes | yes | NO | yes | yes |
| T1-GO-01 | MD5 | yes | yes | yes | yes | yes |
| T1-GO-02 | SHA-1 | yes | yes | yes | yes | yes |
| T1-GO-03 | SHA-256 | yes | yes | yes | yes | yes |
| T1-GO-04 | SHA3-256 | NO | NO | n/a | n/a | n/a |
| T1-GO-05 | AES | yes | yes | NO | yes | n/a |
| T1-GO-06 | AES | yes | yes | NO | yes | n/a |
| T1-GO-07 | 3DES | yes | yes | NO | yes | yes |
| T1-GO-08 | DES | yes | yes | NO | yes | yes |
| T1-GO-09 | RC4 | NO | NO | n/a | n/a | n/a |
| T1-GO-10 | RSA | yes | yes | yes | yes | yes |
| T1-GO-11 | EC | yes | yes | NO | yes | yes |
| T1-GO-12 | Ed25519 | yes | yes | yes | yes | yes |
| T1-GO-13 | X25519 | yes | yes | yes | yes | yes |
| T1-GO-14 | DSA | yes | yes | NO | yes | yes |
| T1-GO-15 | HMAC | yes | yes | NO | yes | n/a |
| T1-GO-16 | PBKDF2 | yes | yes | NO | yes | n/a |
| T1-GO-17 | TLS-1.0 | NO | NO | n/a | n/a | n/a |
| T1-GO-18 | TLS_RSA_WITH_3DES_EDE_CBC_SHA | NO | NO | n/a | n/a | n/a |
| T1-GO-19 | TLS_RSA_WITH_AES_128_CBC_SHA | NO | NO | n/a | n/a | n/a |
| T1-GO-20 | TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 | NO | NO | n/a | n/a | n/a |
| T2-GO-01 | SHA-1 | yes | yes | yes | yes | yes |
| T2-GO-02 | RSA | yes | yes | yes | yes | yes |
| T2-GO-03 | EC | yes | yes | NO | yes | yes |
| T2-GO-04 | HMAC | yes | yes | NO | yes | n/a |
| T2-GO-05 | AES | yes | yes | NO | yes | n/a |
| T2-GO-06 | 3DES | yes | yes | NO | yes | yes |
| PQ-GO-01 | ML-KEM | yes | yes | NO | yes | n/a |
| PQ-GO-02 | TLS-1.3 | NO | NO | n/a | n/a | n/a |
| PQ-GO-03 | X25519MLKEM768 | NO | NO | n/a | n/a | n/a |
| PQ-GO-04 | X25519 | yes | yes | yes | yes | yes |
| T1-JS-01 | MD5 | yes | yes | yes | yes | yes |
| T1-JS-02 | SHA-1 | yes | yes | yes | yes | yes |
| T1-JS-03 | SHA-256 | yes | yes | yes | yes | yes |
| T1-JS-04 | SHA3-256 | yes | yes | yes | yes | yes |
| T1-JS-05 | AES | yes | yes | yes | yes | yes |
| T1-JS-06 | AES | yes | yes | yes | yes | yes |
| T1-JS-07 | 3DES | NO | NO | n/a | n/a | n/a |
| T1-JS-08 | ChaCha20-Poly1305 | yes | yes | yes | yes | yes |
| T1-JS-09 | RSA | yes | yes | yes | yes | yes |
| T1-JS-10 | EC | NO | NO | n/a | n/a | n/a |
| T1-JS-11 | Ed25519 | yes | yes | yes | yes | yes |
| T1-JS-12 | X25519 | yes | yes | yes | yes | yes |
| T1-JS-13 | DH | NO | NO | n/a | n/a | n/a |
| T1-JS-14 | HMAC | yes | yes | NO | yes | n/a |
| T1-JS-15 | PBKDF2 | yes | yes | NO | yes | n/a |
| T1-JS-16 | RSA | yes | yes | yes | yes | yes |
| T1-JS-17 | SHA-1 | yes | yes | yes | yes | yes |
| T2-TS-01 | 3DES | NO | NO | n/a | n/a | n/a |
| T2-TS-02 | SHA-1 | yes | yes | yes | yes | yes |
| T2-TS-03 | RSA | yes | yes | NO | yes | yes |
| T2-TS-04 | EC | yes | yes | yes | yes | yes |
| T2-TS-05 | AES | yes | yes | yes | yes | yes |
| T2-TS-06 | AES | yes | yes | NO | yes | n/a |
| T2-TS-07 | HMAC | yes | yes | NO | yes | n/a |
| T1-C-01 | MD5 | yes | yes | yes | yes | yes |
| T1-C-02 | SHA-1 | yes | yes | yes | yes | yes |
| T1-C-03 | SHA-256 | yes | yes | yes | yes | yes |
| T1-C-04 | SHA3-256 | yes | yes | yes | yes | yes |
| T1-C-05 | AES | yes | yes | NO | yes | n/a |
| T1-C-06 | AES | yes | yes | NO | yes | n/a |
| T1-C-07 | 3DES | NO | NO | n/a | n/a | n/a |
| T1-C-08 | ChaCha20-Poly1305 | yes | yes | yes | yes | yes |
| T1-C-09 | RSA | yes | yes | yes | yes | yes |
| T1-C-10 | RSA | yes | yes | yes | yes | yes |
| T1-C-11 | EC | NO | NO | n/a | n/a | n/a |
| T1-C-12 | Ed25519 | yes | yes | yes | yes | yes |
| T1-C-13 | X25519 | yes | yes | yes | yes | yes |
| T1-C-14 | DH | NO | NO | n/a | n/a | n/a |
| T1-C-15 | HMAC | yes | yes | NO | yes | n/a |
| T1-C-16 | PBKDF2 | yes | yes | NO | yes | n/a |
| T1-C-17 | TLS-1.0 | NO | NO | n/a | n/a | n/a |
| T1-C-18 | TLS_RSA_WITH_3DES_EDE_CBC_SHA | NO | NO | n/a | n/a | n/a |
| T1-C-19 | TLS_RSA_WITH_AES_128_CBC_SHA | NO | NO | n/a | n/a | n/a |
| T1-C-20 | TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 | NO | NO | n/a | n/a | n/a |
| T1-CS-01 | MD5 | yes | yes | yes | yes | yes |
| T1-CS-02 | SHA-1 | yes | yes | yes | yes | yes |
| T1-CS-03 | SHA-256 | yes | yes | yes | yes | yes |
| T1-CS-04 | SHA3-256 | yes | yes | yes | yes | yes |
| T1-CS-05 | RSA | yes | yes | yes | yes | yes |
| T1-CS-06 | EC | yes | yes | NO | yes | yes |
| T1-CS-07 | EC | NO | NO | n/a | n/a | n/a |
| T1-CS-08 | AES | yes | yes | yes | yes | yes |
| T1-CS-09 | AES | yes | yes | NO | yes | n/a |
| T1-CS-10 | 3DES | yes | yes | NO | yes | yes |
| T1-CS-11 | HMAC | yes | yes | NO | yes | n/a |
| T1-CS-12 | PBKDF2 | yes | yes | NO | yes | n/a |
| T1-CS-13 | DSA | yes | yes | yes | yes | yes |
| T2-C-01 | AES | yes | yes | yes | yes | yes |
| T2-C-02 | SHA-1 | yes | yes | yes | yes | yes |
| T2-C-03 | RSA | yes | yes | NO | yes | yes |
| T2-C-04 | EC | yes | yes | yes | yes | yes |
| T2-C-05 | HMAC | yes | yes | NO | yes | n/a |
| T2-C-06 | 3DES | NO | NO | n/a | n/a | n/a |
| T2-CS-01 | AES | yes | yes | NO | yes | n/a |
| T2-CS-02 | SHA-1 | yes | yes | yes | yes | yes |
| T2-CS-03 | MD5 | yes | yes | yes | yes | yes |
| T2-CS-04 | SHA-512 | NO | NO | n/a | n/a | n/a |
| T2-CS-05 | RSA | yes | yes | NO | yes | yes |
| T2-CS-06 | EC | yes | yes | NO | yes | yes |
| MX-PY-1a | PBKDF2 | yes | yes | NO | yes | n/a |
| MX-PY-1b | PBKDF2 | yes | yes | NO | yes | n/a |
| MX-PY-1c | HMAC | yes | yes | NO | yes | n/a |
| MX-PY-1d | AES | yes | yes | NO | yes | n/a |
| MX-PY-2a | DH | yes | yes | NO | yes | yes |
| MX-PY-2b | ML-DSA | yes | yes | NO | yes | n/a |
| MX-PY-2c | DH | yes | yes | NO | yes | yes |
| MX-PY-2d | ChaCha20-Poly1305 | yes | yes | yes | yes | yes |
| MX-PY-3a | SHA-1 | yes | yes | yes | yes | yes |
| MX-PY-3b | HMAC | yes | yes | NO | yes | n/a |
| MX-PY-3c | EC | yes | yes | NO | yes | yes |
| MX-PY-3d | EC | yes | yes | yes | yes | yes |
| MX-JV-1a | DH | yes | yes | NO | yes | yes |
| MX-JV-1b | SHA-1 | yes | yes | yes | yes | yes |
| MX-JV-1c | DH | yes | yes | NO | yes | yes |
| MX-JV-1d | AES | yes | yes | NO | yes | n/a |
| MX-JV-2a | SHA-256 | yes | yes | yes | yes | yes |
| MX-JV-2b | Ed25519 | yes | yes | yes | yes | yes |
| MX-JV-2c | PBKDF2 | yes | yes | NO | yes | n/a |
| MX-JV-2d | PBKDF2 | yes | yes | NO | yes | n/a |
| MX-JV-3a | HMAC | yes | yes | NO | yes | n/a |
| MX-JV-3b | 3DES | yes | yes | NO | yes | yes |
| MX-JV-3c | ChaCha20-Poly1305 | yes | yes | yes | yes | yes |
| MX-JV-3d | SHA-512 | NO | NO | n/a | n/a | n/a |
| MX-JV-3e | 3DES | yes | yes | yes | yes | yes |
| MX-GO-1a | PBKDF2 | yes | yes | NO | yes | n/a |
| MX-GO-1b | ML-KEM | yes | yes | NO | yes | n/a |
| MX-GO-1c | RSA | yes | yes | NO | yes | yes |
| MX-GO-1d | RSA | yes | yes | yes | yes | yes |
| MX-GO-2a | PBKDF2 | yes | yes | NO | yes | n/a |
| MX-GO-2b | DES | yes | yes | NO | yes | yes |
| MX-GO-2c | PBKDF2 | yes | yes | NO | yes | n/a |
| MX-GO-2d | 3DES | yes | yes | NO | yes | yes |
| MX-GO-3a | RSA | yes | yes | NO | yes | yes |
| MX-GO-3b | RC4 | NO | NO | n/a | n/a | n/a |
| MX-GO-3c | HMAC | yes | yes | NO | yes | n/a |
| MX-GO-3d | Ed25519 | yes | yes | yes | yes | yes |
| MX-JS-1a | AES | yes | yes | yes | yes | yes |
| MX-JS-1b | HMAC | yes | yes | NO | yes | n/a |
| MX-JS-1c | AES | yes | yes | NO | yes | yes |
| MX-JS-2a | SHA3-256 | yes | yes | yes | yes | yes |
| MX-JS-2b | PBKDF2 | yes | yes | NO | yes | n/a |
| MX-JS-2c | EC | yes | yes | NO | yes | yes |
| MX-JS-2d | EC | yes | yes | yes | yes | yes |
| MX-JS-2e | AES | yes | yes | yes | yes | yes |
| MX-TS-1a | EC | NO | NO | n/a | n/a | n/a |
| MX-TS-1b | HMAC | yes | yes | NO | yes | n/a |
| MX-TS-1c | AES | yes | yes | yes | yes | yes |
| MX-TS-1d | RSA | yes | yes | NO | yes | yes |
| MX-C-1a | SHA-1 | yes | yes | yes | yes | yes |
| MX-C-1b | EC | yes | yes | yes | yes | yes |
| MX-C-1c | HMAC | yes | yes | NO | yes | n/a |
| MX-C-1d | X25519 | yes | yes | yes | yes | yes |
| MX-C-1e | HMAC | yes | yes | NO | yes | n/a |
| MX-C-2a | EC | yes | yes | yes | yes | yes |
| MX-C-2b | AES | yes | yes | NO | yes | n/a |
| MX-C-2c | 3DES | NO | NO | n/a | n/a | n/a |
| MX-C-2d | 3DES | NO | NO | n/a | n/a | n/a |
| MX-C-3a | AES | yes | yes | NO | yes | n/a |
| MX-C-3b | 3DES | NO | NO | n/a | n/a | n/a |
| MX-C-3c | AES | yes | yes | NO | yes | n/a |
| MX-C-3d | DH | NO | NO | n/a | n/a | n/a |
| SYS-GO-01 | RSA | yes | NO | NO | yes | yes |
| SYS-GO-02 | HMAC | yes | NO | NO | yes | n/a |
| SYS-GO-03 | SHA-256 | yes | yes | yes | yes | yes |
| SYS-PY-01 | AES | yes | NO | yes | yes | yes |
| SYS-PY-02 | HMAC | yes | NO | NO | yes | n/a |
| SYS-PY-03 | RSA | NO | NO | n/a | n/a | n/a |
| SYS-PY-04 | SHA-1 | NO | NO | n/a | n/a | n/a |
| SYS-JV-01 | EC | yes | NO | yes | yes | yes |
| SYS-JV-02 | SHA-1 | yes | yes | yes | yes | yes |
| SYS-AR-01 | EC | NO | NO | n/a | n/a | n/a |
| SYS-AR-02 | SHA-1 | NO | NO | n/a | n/a | n/a |
| SYS-AR-03 | RSA | yes | yes | yes | n/a | yes |
| SYS-AR-04 | HMAC | yes | yes | yes | n/a | n/a |
| SYS-AR-05 | SHA-1 | yes | yes | yes | n/a | yes |
| SYS-AR-06 | SHA-256 | yes | yes | yes | n/a | yes |
| SYS-AS-01 | TLS-1.2 | yes | yes | yes | yes | n/a |
| SYS-AS-02 | TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 | NO | NO | n/a | n/a | n/a |
| SYS-AS-03 | TLS_RSA_WITH_AES_128_CBC_SHA | NO | NO | n/a | n/a | n/a |
| SYS-AS-04 | RSA | NO | NO | n/a | n/a | n/a |
| SYS-AS-05 | SHA-256 | NO | NO | n/a | n/a | n/a |
| SYS-AS-06 | RSA | yes | yes | NO | n/a | yes |
| SYS-AS-07 | EC | NO | NO | n/a | n/a | n/a |
| SYS-AS-08 | SHA-384 | NO | NO | n/a | n/a | n/a |
| SYS-AS-09 | EC | NO | NO | n/a | n/a | n/a |
| SYS-AS-10 | RSA | NO | NO | n/a | n/a | n/a |
| SYS-AS-11 | AES | NO | NO | n/a | n/a | n/a |
| DC-PY-01 | MD5 | yes | yes | yes | yes | yes |
| DC-PY-02 | RSA | yes | yes | yes | yes | yes |
| DC-JV-01 | DES | yes | yes | yes | yes | yes |
| DC-JV-02 | SHA-1 | yes | yes | yes | yes | yes |
| DC-GO-01 | MD5 | yes | yes | yes | yes | yes |
| DC-GO-02 | RC4 | NO | NO | n/a | n/a | n/a |
| DC-JS-01 | MD5 | yes | yes | yes | yes | yes |
| DC-JS-02 | 3DES | NO | NO | n/a | n/a | n/a |
| DC-C-01 | MD5 | yes | yes | yes | yes | yes |
| DC-C-02 | 3DES | NO | NO | n/a | n/a | n/a |
