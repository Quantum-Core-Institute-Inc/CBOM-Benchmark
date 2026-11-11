# CBOM Testbench Scorecard: answer key

**Overall:** 330/330 findings detected (100.0% recall), 0 false positives (100.0% precision), parameters correct on 100.0% of detections.

Calibration cases (generated Tier 1-2 siblings of the hand-written cases; they feed the holdout's overfit gap and are not counted anywhere else here): 304/304 detected (100.0%), 0 false positives.

| Bucket | Detected | Recall | 95% interval | At primary site | Params correct | Line accurate | Quantum flag | False pos. | Precision |
|---|---|---|---|---|---|---|---|---|---|
| Tier 1 c | 20/20 | 100.0% | 83.9–100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 1 go | 20/20 | 100.0% | 83.9–100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 1 java | 16/16 | 100.0% | 80.6–100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 1 javascript | 17/17 | 100.0% | 81.6–100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 1 python | 16/16 | 100.0% | 80.6–100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 2 c | 6/6 | 100.0% | 61.0–100.0% (thin) | 100.0% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 2 go | 6/6 | 100.0% | 61.0–100.0% (thin) | 100.0% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 2 java | 8/8 | 100.0% | 67.6–100.0% (thin) | 100.0% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 2 python | 9/9 | 100.0% | 70.1–100.0% (thin) | 100.0% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 2 typescript | 7/7 | 100.0% | 64.6–100.0% (thin) | 100.0% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 3 java | 7/7 | 100.0% | 64.6–100.0% (thin) | 100.0% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 3 python | 9/9 | 100.0% | 70.1–100.0% (thin) | 100.0% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 4 assets | 48/48 | 100.0% | 92.6–100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 5 java | 8/8 | 100.0% | 67.6–100.0% (thin) | 100.0% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| Tier 5 python | 9/9 | 100.0% | 70.1–100.0% (thin) | 100.0% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| Mixed files c | 13/13 | 100.0% | 77.2–100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| Mixed files go | 12/12 | 100.0% | 75.7–100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| Mixed files java | 13/13 | 100.0% | 77.2–100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| Mixed files javascript | 8/8 | 100.0% | 67.6–100.0% (thin) | 100.0% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| Mixed files python | 12/12 | 100.0% | 75.7–100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| Mixed files typescript | 4/4 | 100.0% | 51.0–100.0% (thin) | 100.0% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| PQC assets | 22/22 | 100.0% | 85.1–100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| PQC go | 4/4 | 100.0% | 51.0–100.0% (thin) | 100.0% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| PQC java | 4/4 | 100.0% | 51.0–100.0% (thin) | 100.0% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| PQC python | 6/6 | 100.0% | 61.0–100.0% (thin) | 100.0% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| System fixture artifacts | 6/6 | 100.0% | 61.0–100.0% (thin) | 100.0% | 100.0% | n/a | 100.0% | 0 | 100.0% |
| System fixture assets | 11/11 | 100.0% | 74.1–100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| System fixture go | 3/3 | 100.0% | 43.8–100.0% (thin) | 100.0% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| System fixture java | 2/2 | 100.0% | 34.2–100.0% (thin) | 100.0% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| System fixture python | 4/4 | 100.0% | 51.0–100.0% (thin) | 100.0% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| **Total** | 330/330 | 100.0% | 98.8–100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 0 | 100.0% |
| Negative controls | | | | | | | | 0 | |

Intervals are 95% Wilson intervals on recall. 18 bucket(s) have fewer than 10 findings and are marked thin: read their rates as indications, not measurements.

**PQC over-claims: 0.** Post-quantum or hybrid algorithms reported where the code or config has none. Each one makes migration look further along than it is. Any number above zero should be explained by the vendor before purchase.

**PQC by standard name: 21/21 (100.0%).** Detected post-quantum findings reported under the FIPS 203/204/205 name or OID. Reports that only say Kyber, Dilithium, SPHINCS+ or Falcon keep their recall credit and fail this check.

## System fixture: routing and asset links

**Routable: 26/26 detected system findings (100.0%)** (of 26). Routable means a reported location resolves, through the fixture's CODEOWNERS, to the team that owns the fix. Reporting only the shared wrapper or its config is detection, but the ticket lands with platform-security.

**Asset links: 2/2.**

| Link | Found |
|---|---|
| nginx terminates TLS with this certificate (ssl_certificate) | yes |
| the certificate's public key belongs to this private key | yes |

**Recall** counts a finding reported anywhere acceptable, including the config or constants file that names the algorithm. **At primary site** counts only findings reported in the file the ground truth anchors them to: the crypto call itself or, for a shared wrapper, the caller that binds the parameters. It's the stricter number, and the one that tells an engineer what to change.

False positives in the bucket rows are those inside positive test files; negative-control false positives are counted separately and included in the total.

## Deadline view: NIST: IR 8547 (final) + SP 800-131A Rev. 2 + FIPS 186-5 + SP 800-52 Rev. 2

As of 2026-11-10. Each expected finding is dated under this policy; misses that fall due sooner weigh more.

**Deadline-weighted recall: 100.0%** (at primary site: 100.0%). **Findings due by end of 2030 that this scanner missed: 0.**

| When it's due | Weight | Detected | Recall | At primary site |
|---|---|---|---|---|
| Due now (not approved or past its date) | 5 | 73/73 | 100.0% | 100.0% |
| Due by end of 2030 | 4 | 34/34 | 100.0% | 100.0% |
| Due 2031 to 2033 | 3 | 0/0 | n/a | n/a |
| Due 2034 to 2035 | 2 | 96/96 | 100.0% | 100.0% |
| No deadline (approved, review, out of scope, unknown) | 1 | 127/127 | 100.0% | 100.0% |

## Actionability: could an engineer open a ticket from this?

Rubric `cbom-actionability-v1` (proposed; see `rubric/actionability.json`). Each detected finding is checked for the fields a migration ticket needs. Facts are checked against the real files.

**Ticket-ready: 330/330 detected findings (100.0%)**, meaning every must-have is present and correct. **Actionable recall: 100.0%** of all 330 expected findings were both found and ticket-ready. Field completeness across all checks: 100.0%.

| Check | Tier | Applies to | Passed | Rate |
|---|---|---|---|---|
| Exact location | must | 330 | 330 | 100.0% |
| Correct parameters | must | 193 | 193 | 100.0% |
| Primitive, where the family is ambiguous | must | 72 | 72 | 100.0% |
| Certificate expiry (correct) | must | 30 | 30 | 100.0% |
| Certificate subject (correct) | must | 30 | 30 | 100.0% |
| Key material type | must | 9 | 9 | 100.0% |
| Protocol version | must | 13 | 13 | 100.0% |
| OID | should | 278 | 278 | 100.0% |
| Crypto functions | should | 290 | 290 | 100.0% |
| Quantum security level (correct) | should | 287 | 287 | 100.0% |
| Code context | should | 116 | 116 | 100.0% |
| Providing library | should | 118 | 118 | 100.0% |
| Certificate issuer | should | 30 | 30 | 100.0% |
| Certificate start date | should | 30 | 30 | 100.0% |
| Certificate key and signature linked | should | 30 | 30 | 100.0% |
| Key format | should | 9 | 9 | 100.0% |
| Cipher suite in a protocol | should | 13 | 13 | 100.0% |

## Missed findings

None.

## Detected with wrong or missing parameters

None.

## False positives

None.

## Crypto libraries (dependency manifests)

- Found in the right manifest: **28/28** (100.0%); found anywhere, including with no location: 28/28
- Direct dependencies: 100.0%; transitive (lockfile): 100.0%
- Versions correct, of found libraries the manifest pins (none reported counts as not correct): 100.0%
- PQC-capability verdicts (where the scanner gives one): none given
- False positives: 0

| Manifest | Library | Declared | Scope | Found | Version |
|---|---|---|---|---|---|
| `python-billing/requirements.txt` | cryptography | 41.0.7 | direct | yes | ok |
| `python-billing/requirements.txt` | pycryptodome | 3.19.0 | direct | yes | ok |
| `python-billing/requirements.txt` | pyOpenSSL | 23.3.0 | direct | yes | ok |
| `python-billing/requirements.txt` | PyJWT | 2.8.0 | direct | yes | ok |
| `python-billing/requirements.txt` | paramiko | 3.4.0 | direct | yes | ok |
| `python-billing/requirements.txt` | bcrypt | 4.1.2 | direct | yes | ok |
| `python-signer/pyproject.toml` | cryptography | range | direct | yes | n/a |
| `python-signer/pyproject.toml` | liboqs-python | 0.16.0 | direct | yes | ok |
| `java-gateway/pom.xml` | org.bouncycastle:bcprov-jdk15on, bcpkix-jdk15on | 1.70 | direct | yes | ok |
| `java-gateway/pom.xml` | com.nimbusds:nimbus-jose-jwt | 9.37.3 | direct | yes | ok |
| `java-gateway/pom.xml` | io.jsonwebtoken:jjwt-api | 0.12.5 | direct | yes | ok |
| `java-pq/build.gradle` | org.bouncycastle:bcprov-jdk18on, bctls-jdk18on | 1.80 | direct | yes | ok |
| `node-api/package.json` | jsonwebtoken | 9.0.2 | direct | yes | ok |
| `node-api/package.json` | crypto-js | 4.2.0 | direct | yes | ok |
| `node-api/package.json` | node-forge | 1.3.1 | direct | yes | ok |
| `node-api/package.json` | bcryptjs | 2.4.3 | direct | yes | ok |
| `node-api/package.json` | @noble/post-quantum | 0.5.4 | direct | yes | ok |
| `node-api/package-lock.json` | @noble/curves | 2.0.1 | transitive | yes | ok |
| `node-api/package-lock.json` | @noble/hashes | 2.0.1 | transitive | yes | ok |
| `node-api/package-lock.json` | jws | 3.2.3 | transitive | yes | ok |
| `node-api/package-lock.json` | jwa | 1.4.2 | transitive | yes | ok |
| `go-service/go.mod` | golang.org/x/crypto | 0.31.0 | direct | yes | ok |
| `go-service/go.mod` | github.com/cloudflare/circl | 1.6.1 | direct | yes | ok |
| `go-service/go.mod` | github.com/golang-jwt/jwt/v5 | 5.2.1 | direct | yes | ok |
| `c-agent/conanfile.txt` | openssl | 1.1.1w | direct | yes | ok |
| `c-agent/conanfile.txt` | libsodium | 1.0.18 | direct | yes | ok |
| `corpus/system/payments-platform/services/settlement-worker/requirements.txt` | cryptography | 42.0.5 | direct | yes | ok |
| `corpus/system/payments-platform/services/ledger-service/build.gradle` | org.bouncycastle:bcprov-jdk18on | 1.77 | direct | yes | ok |

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
| T1-PY-08 | AES | yes | yes | yes | yes | yes |
| T1-PY-09 | AES | yes | yes | yes | yes | yes |
| T1-PY-10 | 3DES | yes | yes | yes | yes | yes |
| T1-PY-11 | ChaCha20-Poly1305 | yes | yes | yes | yes | yes |
| T1-PY-12 | Ed25519 | yes | yes | yes | yes | yes |
| T1-PY-13 | X25519 | yes | yes | yes | yes | yes |
| T1-PY-14 | DH | yes | yes | yes | yes | yes |
| T1-PY-15 | HMAC | yes | yes | yes | yes | yes |
| T1-PY-16 | PBKDF2 | yes | yes | yes | yes | yes |
| T1-JV-01 | MD5 | yes | yes | yes | yes | yes |
| T1-JV-02 | SHA-1 | yes | yes | yes | yes | yes |
| T1-JV-03 | SHA-256 | yes | yes | yes | yes | yes |
| T1-JV-04 | SHA3-256 | yes | yes | yes | yes | yes |
| T1-JV-05 | RSA | yes | yes | yes | yes | yes |
| T1-JV-06 | EC | yes | yes | yes | yes | yes |
| T1-JV-07 | DSA | yes | yes | yes | yes | yes |
| T1-JV-08 | AES | yes | yes | yes | yes | yes |
| T1-JV-09 | AES | yes | yes | yes | yes | yes |
| T1-JV-10 | DES | yes | yes | yes | yes | yes |
| T1-JV-11 | 3DES | yes | yes | yes | yes | yes |
| T1-JV-12 | Ed25519 | yes | yes | yes | yes | yes |
| T1-JV-13 | X25519 | yes | yes | yes | yes | yes |
| T1-JV-14 | DH | yes | yes | yes | yes | yes |
| T1-JV-15 | HMAC | yes | yes | yes | yes | yes |
| T1-JV-16 | PBKDF2 | yes | yes | yes | yes | yes |
| T2-PY-01 | SHA-1 | yes | yes | yes | yes | yes |
| T2-PY-02 | RSA | yes | yes | yes | yes | yes |
| T2-PY-03 | AES | yes | yes | yes | yes | yes |
| T2-PY-04 | SHA-1 | yes | yes | yes | yes | yes |
| T2-PY-05 | AES | yes | yes | yes | yes | yes |
| T2-PY-06 | MD5 | yes | yes | yes | yes | yes |
| T2-PY-07 | SHA-256 | yes | yes | yes | yes | yes |
| T2-PY-08 | HMAC | yes | yes | yes | yes | yes |
| T2-PY-09 | EC | yes | yes | yes | yes | yes |
| T2-JV-01 | 3DES | yes | yes | yes | yes | yes |
| T2-JV-02 | RSA | yes | yes | yes | yes | yes |
| T2-JV-03 | MD5 | yes | yes | yes | yes | yes |
| T2-JV-04 | SHA-1 | yes | yes | yes | yes | yes |
| T2-JV-05 | SHA-256 | yes | yes | yes | yes | yes |
| T2-JV-06 | AES | yes | yes | yes | yes | yes |
| T2-JV-07 | DSA | yes | yes | yes | yes | yes |
| T2-JV-08 | EC | yes | yes | yes | yes | yes |
| T3-PY-01 | RSA | yes | yes | yes | yes | yes |
| T3-PY-02 | SHA-1 | yes | yes | yes | yes | yes |
| T3-PY-03 | AES | yes | yes | yes | yes | yes |
| T3-PY-04 | RSA | yes | yes | yes | yes | yes |
| T3-PY-05 | RSA | yes | yes | yes | yes | yes |
| T3-PY-06 | AES | yes | yes | yes | yes | yes |
| T3-PY-07 | ChaCha20-Poly1305 | yes | yes | yes | yes | yes |
| T3-PY-08 | MD5 | yes | yes | yes | yes | yes |
| T3-PY-09 | HMAC | yes | yes | yes | yes | yes |
| T3-JV-01 | RSA | yes | yes | yes | yes | yes |
| T3-JV-02 | SHA-1 | yes | yes | yes | yes | yes |
| T3-JV-03 | AES | yes | yes | yes | yes | yes |
| T3-JV-04 | AES | yes | yes | yes | yes | yes |
| T3-JV-05 | 3DES | yes | yes | yes | yes | yes |
| T3-JV-06 | MD5 | yes | yes | yes | yes | yes |
| T3-JV-07 | HMAC | yes | yes | yes | yes | yes |
| T4-AS-01 | RSA | yes | yes | yes | n/a | yes |
| T4-AS-02 | SHA-256 | yes | yes | yes | n/a | n/a |
| T4-AS-03 | RSA | yes | yes | yes | n/a | yes |
| T4-AS-04 | SHA-1 | yes | yes | yes | n/a | n/a |
| T4-AS-05 | EC | yes | yes | yes | n/a | yes |
| T4-AS-06 | SHA-256 | yes | yes | yes | n/a | n/a |
| T4-AS-07 | Ed25519 | yes | yes | yes | n/a | yes |
| T4-AS-08 | EC | yes | yes | yes | n/a | yes |
| T4-AS-09 | SHA-384 | yes | yes | yes | n/a | n/a |
| T4-AS-10 | RSA | yes | yes | yes | n/a | yes |
| T4-AS-11 | SHA-256 | yes | yes | yes | n/a | n/a |
| T4-AS-12 | RSA | yes | yes | yes | n/a | yes |
| T4-AS-13 | SHA-512 | yes | yes | yes | n/a | n/a |
| T4-AS-14 | RSA | yes | yes | yes | n/a | yes |
| T4-AS-15 | EC | yes | yes | yes | n/a | yes |
| T4-AS-16 | PBKDF2 | yes | yes | yes | n/a | yes |
| T4-AS-17 | AES | yes | yes | yes | n/a | yes |
| T4-AS-18 | RSA | yes | yes | yes | n/a | yes |
| T4-AS-19 | EC | yes | yes | yes | n/a | yes |
| T4-AS-20 | AES | yes | yes | yes | n/a | yes |
| T4-AS-21 | PBKDF2 | yes | yes | yes | n/a | yes |
| T4-AS-22 | RSA | yes | yes | yes | n/a | yes |
| T4-AS-23 | SHA-256 | yes | yes | yes | n/a | n/a |
| T4-AS-24 | RSA | yes | yes | yes | n/a | yes |
| T4-AS-25 | SHA-1 | yes | yes | yes | n/a | n/a |
| T4-AS-26 | RSA | yes | yes | yes | yes | yes |
| T4-AS-27 | DH | yes | yes | yes | yes | yes |
| T4-AS-28 | X25519 | yes | yes | yes | yes | yes |
| T4-AS-29 | AES | yes | yes | yes | yes | yes |
| T4-AS-30 | ChaCha20-Poly1305 | yes | yes | yes | yes | yes |
| T4-AS-31 | HMAC | yes | yes | yes | yes | yes |
| T4-AS-32 | RSA | yes | yes | yes | n/a | yes |
| T4-AS-33 | Ed25519 | yes | yes | yes | n/a | yes |
| T4-AS-34 | TLS-1.0 | yes | yes | yes | yes | n/a |
| T4-AS-35 | TLS-1.1 | yes | yes | yes | yes | n/a |
| T4-AS-36 | TLS-1.2 | yes | yes | yes | yes | n/a |
| T4-AS-37 | TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 | yes | yes | yes | yes | n/a |
| T4-AS-38 | TLS_RSA_WITH_3DES_EDE_CBC_SHA | yes | yes | yes | yes | n/a |
| T4-AS-39 | TLS_RSA_WITH_AES_256_CBC_SHA | yes | yes | yes | yes | n/a |
| T4-AS-40 | TLS-1.1 | yes | yes | yes | yes | n/a |
| T4-AS-41 | TLS-1.2 | yes | yes | yes | yes | n/a |
| T4-AS-42 | TLS_RSA_WITH_AES_128_CBC_SHA | yes | yes | yes | yes | n/a |
| T4-AS-43 | TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 | yes | yes | yes | yes | n/a |
| T4-AS-44 | RSA | yes | yes | yes | yes | yes |
| T4-AS-45 | SHA-1 | yes | yes | yes | yes | yes |
| T4-AS-46 | TLS-1.0 | yes | yes | yes | yes | n/a |
| T4-AS-47 | EC | yes | yes | yes | n/a | yes |
| T4-AS-48 | SHA-384 | yes | yes | yes | n/a | n/a |
| T5-PY-01 | SHA-1 | yes | yes | yes | yes | yes |
| T5-PY-02 | MD5 | yes | yes | yes | yes | yes |
| T5-PY-03 | RSA | yes | yes | yes | yes | yes |
| T5-PY-04 | AES | yes | yes | yes | yes | yes |
| T5-PY-05 | RC4 | yes | yes | yes | yes | yes |
| T5-PY-06 | SHA-256 | yes | yes | yes | yes | yes |
| T5-PY-07 | RSA | yes | yes | yes | yes | yes |
| T5-PY-08 | SHA-1 | yes | yes | yes | n/a | yes |
| T5-PY-09 | HMAC | yes | yes | yes | n/a | yes |
| T5-JV-01 | RSA | yes | yes | yes | yes | yes |
| T5-JV-02 | 3DES | yes | yes | yes | yes | yes |
| T5-JV-03 | MD5 | yes | yes | yes | yes | yes |
| T5-JV-04 | TEA | yes | yes | yes | yes | n/a |
| T5-JV-05 | RSA | yes | yes | yes | yes | yes |
| T5-JV-06 | AES | yes | yes | yes | n/a | yes |
| T5-JV-07 | RSA | yes | yes | yes | n/a | yes |
| T5-JV-08 | SHA-1 | yes | yes | yes | n/a | yes |
| PQ-PY-01 | ML-KEM | yes | yes | yes | yes | yes |
| PQ-PY-02 | ML-DSA | yes | yes | yes | yes | yes |
| PQ-PY-03 | X25519 | yes | yes | yes | yes | yes |
| PQ-PY-04 | ML-KEM | yes | yes | yes | yes | yes |
| PQ-PY-05 | ML-KEM | yes | yes | yes | yes | yes |
| PQ-PY-06 | EC | yes | yes | yes | yes | yes |
| PQ-JV-01 | ML-KEM | yes | yes | yes | yes | yes |
| PQ-JV-02 | ML-DSA | yes | yes | yes | yes | yes |
| PQ-JV-03 | ML-DSA | yes | yes | yes | yes | yes |
| PQ-JV-04 | EC | yes | yes | yes | yes | yes |
| PQ-AS-01 | ML-DSA | yes | yes | yes | n/a | yes |
| PQ-AS-02 | ML-DSA | yes | yes | yes | n/a | yes |
| PQ-AS-03 | ML-DSA | yes | yes | yes | n/a | yes |
| PQ-AS-04 | RSA | yes | yes | yes | n/a | n/a |
| PQ-AS-05 | SHA-256 | yes | yes | yes | n/a | n/a |
| PQ-AS-06 | ML-KEM | yes | yes | yes | n/a | yes |
| PQ-AS-07 | ML-DSA | yes | yes | yes | n/a | yes |
| PQ-AS-08 | TLS-1.3 | yes | yes | yes | yes | n/a |
| PQ-AS-09 | X25519MLKEM768 | yes | yes | yes | yes | yes |
| PQ-AS-10 | X25519 | yes | yes | yes | yes | yes |
| PQ-AS-11 | SecP384r1MLKEM1024 | yes | yes | yes | yes | yes |
| PQ-AS-12 | X25519MLKEM768 | yes | yes | yes | yes | yes |
| PQ-AS-13 | EC | yes | yes | yes | yes | yes |
| PQ-AS-14 | TLS-1.3 | yes | yes | yes | yes | n/a |
| PQ-AS-15 | X25519MLKEM768 | yes | yes | yes | yes | yes |
| PQ-AS-16 | sntrup761x25519 | yes | yes | yes | yes | n/a |
| PQ-AS-17 | X25519 | yes | yes | yes | yes | yes |
| PQ-AS-18 | Ed25519 | yes | yes | yes | yes | yes |
| PQ-AS-19 | ChaCha20-Poly1305 | yes | yes | yes | yes | yes |
| PQ-AS-20 | TLS-1.3 | yes | yes | yes | yes | n/a |
| PQ-AS-21 | X25519 | yes | yes | yes | yes | yes |
| PQ-AS-22 | EC | yes | yes | yes | yes | yes |
| T1-GO-01 | MD5 | yes | yes | yes | yes | yes |
| T1-GO-02 | SHA-1 | yes | yes | yes | yes | yes |
| T1-GO-03 | SHA-256 | yes | yes | yes | yes | yes |
| T1-GO-04 | SHA3-256 | yes | yes | yes | yes | yes |
| T1-GO-05 | AES | yes | yes | yes | yes | yes |
| T1-GO-06 | AES | yes | yes | yes | yes | yes |
| T1-GO-07 | 3DES | yes | yes | yes | yes | yes |
| T1-GO-08 | DES | yes | yes | yes | yes | yes |
| T1-GO-09 | RC4 | yes | yes | yes | yes | yes |
| T1-GO-10 | RSA | yes | yes | yes | yes | yes |
| T1-GO-11 | EC | yes | yes | yes | yes | yes |
| T1-GO-12 | Ed25519 | yes | yes | yes | yes | yes |
| T1-GO-13 | X25519 | yes | yes | yes | yes | yes |
| T1-GO-14 | DSA | yes | yes | yes | yes | yes |
| T1-GO-15 | HMAC | yes | yes | yes | yes | yes |
| T1-GO-16 | PBKDF2 | yes | yes | yes | yes | yes |
| T1-GO-17 | TLS-1.0 | yes | yes | yes | yes | n/a |
| T1-GO-18 | TLS_RSA_WITH_3DES_EDE_CBC_SHA | yes | yes | yes | yes | n/a |
| T1-GO-19 | TLS_RSA_WITH_AES_128_CBC_SHA | yes | yes | yes | yes | n/a |
| T1-GO-20 | TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 | yes | yes | yes | yes | n/a |
| T2-GO-01 | SHA-1 | yes | yes | yes | yes | yes |
| T2-GO-02 | RSA | yes | yes | yes | yes | yes |
| T2-GO-03 | EC | yes | yes | yes | yes | yes |
| T2-GO-04 | HMAC | yes | yes | yes | yes | yes |
| T2-GO-05 | AES | yes | yes | yes | yes | yes |
| T2-GO-06 | 3DES | yes | yes | yes | yes | yes |
| PQ-GO-01 | ML-KEM | yes | yes | yes | yes | yes |
| PQ-GO-02 | TLS-1.3 | yes | yes | yes | yes | n/a |
| PQ-GO-03 | X25519MLKEM768 | yes | yes | yes | yes | yes |
| PQ-GO-04 | X25519 | yes | yes | yes | yes | yes |
| T1-JS-01 | MD5 | yes | yes | yes | yes | yes |
| T1-JS-02 | SHA-1 | yes | yes | yes | yes | yes |
| T1-JS-03 | SHA-256 | yes | yes | yes | yes | yes |
| T1-JS-04 | SHA3-256 | yes | yes | yes | yes | yes |
| T1-JS-05 | AES | yes | yes | yes | yes | yes |
| T1-JS-06 | AES | yes | yes | yes | yes | yes |
| T1-JS-07 | 3DES | yes | yes | yes | yes | yes |
| T1-JS-08 | ChaCha20-Poly1305 | yes | yes | yes | yes | yes |
| T1-JS-09 | RSA | yes | yes | yes | yes | yes |
| T1-JS-10 | EC | yes | yes | yes | yes | yes |
| T1-JS-11 | Ed25519 | yes | yes | yes | yes | yes |
| T1-JS-12 | X25519 | yes | yes | yes | yes | yes |
| T1-JS-13 | DH | yes | yes | yes | yes | yes |
| T1-JS-14 | HMAC | yes | yes | yes | yes | yes |
| T1-JS-15 | PBKDF2 | yes | yes | yes | yes | yes |
| T1-JS-16 | RSA | yes | yes | yes | yes | yes |
| T1-JS-17 | SHA-1 | yes | yes | yes | yes | yes |
| T2-TS-01 | 3DES | yes | yes | yes | yes | yes |
| T2-TS-02 | SHA-1 | yes | yes | yes | yes | yes |
| T2-TS-03 | RSA | yes | yes | yes | yes | yes |
| T2-TS-04 | EC | yes | yes | yes | yes | yes |
| T2-TS-05 | AES | yes | yes | yes | yes | yes |
| T2-TS-06 | AES | yes | yes | yes | yes | yes |
| T2-TS-07 | HMAC | yes | yes | yes | yes | yes |
| T1-C-01 | MD5 | yes | yes | yes | yes | yes |
| T1-C-02 | SHA-1 | yes | yes | yes | yes | yes |
| T1-C-03 | SHA-256 | yes | yes | yes | yes | yes |
| T1-C-04 | SHA3-256 | yes | yes | yes | yes | yes |
| T1-C-05 | AES | yes | yes | yes | yes | yes |
| T1-C-06 | AES | yes | yes | yes | yes | yes |
| T1-C-07 | 3DES | yes | yes | yes | yes | yes |
| T1-C-08 | ChaCha20-Poly1305 | yes | yes | yes | yes | yes |
| T1-C-09 | RSA | yes | yes | yes | yes | yes |
| T1-C-10 | RSA | yes | yes | yes | yes | yes |
| T1-C-11 | EC | yes | yes | yes | yes | yes |
| T1-C-12 | Ed25519 | yes | yes | yes | yes | yes |
| T1-C-13 | X25519 | yes | yes | yes | yes | yes |
| T1-C-14 | DH | yes | yes | yes | yes | yes |
| T1-C-15 | HMAC | yes | yes | yes | yes | yes |
| T1-C-16 | PBKDF2 | yes | yes | yes | yes | yes |
| T1-C-17 | TLS-1.0 | yes | yes | yes | yes | n/a |
| T1-C-18 | TLS_RSA_WITH_3DES_EDE_CBC_SHA | yes | yes | yes | yes | n/a |
| T1-C-19 | TLS_RSA_WITH_AES_128_CBC_SHA | yes | yes | yes | yes | n/a |
| T1-C-20 | TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 | yes | yes | yes | yes | n/a |
| T2-C-01 | AES | yes | yes | yes | yes | yes |
| T2-C-02 | SHA-1 | yes | yes | yes | yes | yes |
| T2-C-03 | RSA | yes | yes | yes | yes | yes |
| T2-C-04 | EC | yes | yes | yes | yes | yes |
| T2-C-05 | HMAC | yes | yes | yes | yes | yes |
| T2-C-06 | 3DES | yes | yes | yes | yes | yes |
| MX-PY-1a | PBKDF2 | yes | yes | yes | yes | yes |
| MX-PY-1b | PBKDF2 | yes | yes | yes | yes | yes |
| MX-PY-1c | HMAC | yes | yes | yes | yes | yes |
| MX-PY-1d | AES | yes | yes | yes | yes | yes |
| MX-PY-2a | DH | yes | yes | yes | yes | yes |
| MX-PY-2b | ML-DSA | yes | yes | yes | yes | yes |
| MX-PY-2c | DH | yes | yes | yes | yes | yes |
| MX-PY-2d | ChaCha20-Poly1305 | yes | yes | yes | yes | yes |
| MX-PY-3a | SHA-1 | yes | yes | yes | yes | yes |
| MX-PY-3b | HMAC | yes | yes | yes | yes | yes |
| MX-PY-3c | EC | yes | yes | yes | yes | yes |
| MX-PY-3d | EC | yes | yes | yes | yes | yes |
| MX-JV-1a | DH | yes | yes | yes | yes | yes |
| MX-JV-1b | SHA-1 | yes | yes | yes | yes | yes |
| MX-JV-1c | DH | yes | yes | yes | yes | yes |
| MX-JV-1d | AES | yes | yes | yes | yes | yes |
| MX-JV-2a | SHA-256 | yes | yes | yes | yes | yes |
| MX-JV-2b | Ed25519 | yes | yes | yes | yes | yes |
| MX-JV-2c | PBKDF2 | yes | yes | yes | yes | yes |
| MX-JV-2d | PBKDF2 | yes | yes | yes | yes | yes |
| MX-JV-3a | HMAC | yes | yes | yes | yes | yes |
| MX-JV-3b | 3DES | yes | yes | yes | yes | yes |
| MX-JV-3c | ChaCha20-Poly1305 | yes | yes | yes | yes | yes |
| MX-JV-3d | SHA-512 | yes | yes | yes | yes | yes |
| MX-JV-3e | 3DES | yes | yes | yes | yes | yes |
| MX-GO-1a | PBKDF2 | yes | yes | yes | yes | yes |
| MX-GO-1b | ML-KEM | yes | yes | yes | yes | yes |
| MX-GO-1c | RSA | yes | yes | yes | yes | yes |
| MX-GO-1d | RSA | yes | yes | yes | yes | yes |
| MX-GO-2a | PBKDF2 | yes | yes | yes | yes | yes |
| MX-GO-2b | DES | yes | yes | yes | yes | yes |
| MX-GO-2c | PBKDF2 | yes | yes | yes | yes | yes |
| MX-GO-2d | 3DES | yes | yes | yes | yes | yes |
| MX-GO-3a | RSA | yes | yes | yes | yes | yes |
| MX-GO-3b | RC4 | yes | yes | yes | yes | yes |
| MX-GO-3c | HMAC | yes | yes | yes | yes | yes |
| MX-GO-3d | Ed25519 | yes | yes | yes | yes | yes |
| MX-JS-1a | AES | yes | yes | yes | yes | yes |
| MX-JS-1b | HMAC | yes | yes | yes | yes | yes |
| MX-JS-1c | AES | yes | yes | yes | yes | yes |
| MX-JS-2a | SHA3-256 | yes | yes | yes | yes | yes |
| MX-JS-2b | PBKDF2 | yes | yes | yes | yes | yes |
| MX-JS-2c | EC | yes | yes | yes | yes | yes |
| MX-JS-2d | EC | yes | yes | yes | yes | yes |
| MX-JS-2e | AES | yes | yes | yes | yes | yes |
| MX-TS-1a | EC | yes | yes | yes | yes | yes |
| MX-TS-1b | HMAC | yes | yes | yes | yes | yes |
| MX-TS-1c | AES | yes | yes | yes | yes | yes |
| MX-TS-1d | RSA | yes | yes | yes | yes | yes |
| MX-C-1a | SHA-1 | yes | yes | yes | yes | yes |
| MX-C-1b | EC | yes | yes | yes | yes | yes |
| MX-C-1c | HMAC | yes | yes | yes | yes | yes |
| MX-C-1d | X25519 | yes | yes | yes | yes | yes |
| MX-C-1e | HMAC | yes | yes | yes | yes | yes |
| MX-C-2a | EC | yes | yes | yes | yes | yes |
| MX-C-2b | AES | yes | yes | yes | yes | yes |
| MX-C-2c | 3DES | yes | yes | yes | yes | yes |
| MX-C-2d | 3DES | yes | yes | yes | yes | yes |
| MX-C-3a | AES | yes | yes | yes | yes | yes |
| MX-C-3b | 3DES | yes | yes | yes | yes | yes |
| MX-C-3c | AES | yes | yes | yes | yes | yes |
| MX-C-3d | DH | yes | yes | yes | yes | yes |
| SYS-GO-01 | RSA | yes | yes | yes | yes | yes |
| SYS-GO-02 | HMAC | yes | yes | yes | yes | yes |
| SYS-GO-03 | SHA-256 | yes | yes | yes | yes | yes |
| SYS-PY-01 | AES | yes | yes | yes | yes | yes |
| SYS-PY-02 | HMAC | yes | yes | yes | yes | yes |
| SYS-PY-03 | RSA | yes | yes | yes | n/a | yes |
| SYS-PY-04 | SHA-1 | yes | yes | yes | n/a | n/a |
| SYS-JV-01 | EC | yes | yes | yes | yes | yes |
| SYS-JV-02 | SHA-1 | yes | yes | yes | yes | yes |
| SYS-AR-01 | EC | yes | yes | yes | n/a | yes |
| SYS-AR-02 | SHA-1 | yes | yes | yes | n/a | yes |
| SYS-AR-03 | RSA | yes | yes | yes | n/a | yes |
| SYS-AR-04 | HMAC | yes | yes | yes | n/a | n/a |
| SYS-AR-05 | SHA-1 | yes | yes | yes | n/a | yes |
| SYS-AR-06 | SHA-256 | yes | yes | yes | n/a | yes |
| SYS-AS-01 | TLS-1.2 | yes | yes | yes | yes | n/a |
| SYS-AS-02 | TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 | yes | yes | yes | yes | n/a |
| SYS-AS-03 | TLS_RSA_WITH_AES_128_CBC_SHA | yes | yes | yes | yes | n/a |
| SYS-AS-04 | RSA | yes | yes | yes | n/a | yes |
| SYS-AS-05 | SHA-256 | yes | yes | yes | n/a | n/a |
| SYS-AS-06 | RSA | yes | yes | yes | n/a | yes |
| SYS-AS-07 | EC | yes | yes | yes | n/a | yes |
| SYS-AS-08 | SHA-384 | yes | yes | yes | n/a | n/a |
| SYS-AS-09 | EC | yes | yes | yes | yes | yes |
| SYS-AS-10 | RSA | yes | yes | yes | yes | yes |
| SYS-AS-11 | AES | yes | yes | yes | yes | yes |
