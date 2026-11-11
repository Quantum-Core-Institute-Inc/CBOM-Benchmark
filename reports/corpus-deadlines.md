# Cryptographic deadline report: expected.cdx.json

As of **2026-11-10**. One row per file and algorithm family found in the CBOM.

## NIST: IR 8547 (final) + SP 800-131A Rev. 2 + FIPS 186-5 + SP 800-52 Rev. 2

_U.S. federal systems and anyone who adopts NIST's transition schedule (most regulated industries do)._

| When | Findings | Quantum-vulnerable | Files |
|---|---|---|---|
| Due now (not approved or past its date) | 169 | 51 | 164 |
| Due by end of 2030 | 62 | 0 | 62 |
| Due 2031 to 2033 | 0 | 0 | 0 |
| Due 2034 to 2035 | 167 | 167 | 150 |
| No deadline (approved, review, out of scope, unknown) | 201 | 1 | 170 |

### Due now or by end of 2030 (231)

| Due | Algorithm | File | Why |
|---|---|---|---|
| **now** | ChaCha20-Poly1305 | `corpus/calibration/tier1/c/cal_chacha20poly1305_006.c` | Not FIPS-approved. Fine outside FIPS scope; a finding inside it. |
| **now** | ChaCha20-Poly1305 | `corpus/calibration/tier1/c/cal_chacha20poly1305_007.c` | Not FIPS-approved. Fine outside FIPS scope; a finding inside it. |
| **now** | ChaCha20-Poly1305 | `corpus/calibration/tier1/c/cal_chacha20poly1305_008.c` | Not FIPS-approved. Fine outside FIPS scope; a finding inside it. |
| **now** | MD5 | `corpus/calibration/tier1/c/cal_md5_021.c` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/calibration/tier1/c/cal_md5_022.c` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/calibration/tier1/c/cal_md5_023.c` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | DES-CBC | `corpus/calibration/tier1/go/cal_des_006/cal_des_006.go` | Single DES; FIPS 46-3 was withdrawn in 2005. |
| **now** | DES-CBC | `corpus/calibration/tier1/go/cal_des_007/cal_des_007.go` | Single DES; FIPS 46-3 was withdrawn in 2005. |
| **now** | DES-CBC | `corpus/calibration/tier1/go/cal_des_008/cal_des_008.go` | Single DES; FIPS 46-3 was withdrawn in 2005. |
| **now** | MD5 | `corpus/calibration/tier1/go/cal_md5_021/cal_md5_021.go` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/calibration/tier1/go/cal_md5_022/cal_md5_022.go` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/calibration/tier1/go/cal_md5_023/cal_md5_023.go` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | RC4 | `corpus/calibration/tier1/go/cal_rc4_027/cal_rc4_027.go` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | RC4 | `corpus/calibration/tier1/go/cal_rc4_028/cal_rc4_028.go` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | RC4 | `corpus/calibration/tier1/go/cal_rc4_029/cal_rc4_029.go` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/calibration/tier1/java/Cal1022LedgerDefaults.java` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/calibration/tier1/java/Cal1023AuditProfile.java` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/calibration/tier1/java/Cal1024PolicyDefaults.java` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | ChaCha20-Poly1305 | `corpus/calibration/tier1/javascript/cal_chacha20poly1305_006.js` | Not FIPS-approved. Fine outside FIPS scope; a finding inside it. |
| **now** | ChaCha20-Poly1305 | `corpus/calibration/tier1/javascript/cal_chacha20poly1305_007.js` | Not FIPS-approved. Fine outside FIPS scope; a finding inside it. |
| **now** | ChaCha20-Poly1305 | `corpus/calibration/tier1/javascript/cal_chacha20poly1305_008.js` | Not FIPS-approved. Fine outside FIPS scope; a finding inside it. |
| **now** | MD5 | `corpus/calibration/tier1/javascript/cal_md5_021.js` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/calibration/tier1/javascript/cal_md5_022.js` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/calibration/tier1/javascript/cal_md5_023.js` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | ChaCha20-Poly1305 | `corpus/calibration/tier1/python/cal_chacha20poly1305_006.py` | Not FIPS-approved. Fine outside FIPS scope; a finding inside it. |
| **now** | ChaCha20-Poly1305 | `corpus/calibration/tier1/python/cal_chacha20poly1305_007.py` | Not FIPS-approved. Fine outside FIPS scope; a finding inside it. |
| **now** | ChaCha20-Poly1305 | `corpus/calibration/tier1/python/cal_chacha20poly1305_008.py` | Not FIPS-approved. Fine outside FIPS scope; a finding inside it. |
| **now** | MD5 | `corpus/calibration/tier1/python/cal_md5_024.py` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/calibration/tier1/python/cal_md5_025.py` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/calibration/tier1/python/cal_md5_026.py` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | HMAC-MD5 | `corpus/calibration/tier2/c/cal_hmac_010.c` | MD5 is not an approved hash function, in HMAC or otherwise. |
| **now** | HMAC-MD5 | `corpus/calibration/tier2/c/cal_hmac_011.c` | MD5 is not an approved hash function, in HMAC or otherwise. |
| **now** | HMAC-MD5 | `corpus/calibration/tier2/c/cal_hmac_012.c` | MD5 is not an approved hash function, in HMAC or otherwise. |
| **now** | HMAC-MD5 | `corpus/calibration/tier2/go/cal_hmac_010/cal_hmac_010.go` | MD5 is not an approved hash function, in HMAC or otherwise. |
| **now** | HMAC-MD5 | `corpus/calibration/tier2/go/cal_hmac_011/cal_hmac_011.go` | MD5 is not an approved hash function, in HMAC or otherwise. |
| **now** | HMAC-MD5 | `corpus/calibration/tier2/go/cal_hmac_012/cal_hmac_012.go` | MD5 is not an approved hash function, in HMAC or otherwise. |
| **now** | MD5 | `corpus/calibration/tier2/java/Cal2013TenantOptions.java` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/calibration/tier2/java/Cal2014DeviceDefaults.java` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/calibration/tier2/java/Cal2015UploadSettings.java` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/calibration/tier2/python/cal_md5_009.py` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/calibration/tier2/python/cal_md5_010.py` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/calibration/tier2/python/cal_md5_011.py` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | HMAC-MD5 | `corpus/calibration/tier2/typescript/cal_hmac_009.ts` | MD5 is not an approved hash function, in HMAC or otherwise. |
| **now** | HMAC-MD5 | `corpus/calibration/tier2/typescript/cal_hmac_010.ts` | MD5 is not an approved hash function, in HMAC or otherwise. |
| **now** | HMAC-MD5 | `corpus/calibration/tier2/typescript/cal_hmac_011.ts` | MD5 is not an approved hash function, in HMAC or otherwise. |
| **now** | HMAC-MD5 | `corpus/mixed/c/device_daemon.c` | MD5 is not an approved hash function, in HMAC or otherwise. |
| **now** | RC4 | `corpus/mixed/go/invoice_gateway/main.go` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | DES-CBC | `corpus/mixed/go/report_gateway/main.go` | Single DES; FIPS 46-3 was withdrawn in 2005. |
| **now** | ChaCha20-Poly1305 | `corpus/mixed/java/OrderDefaultsModule.java` | Not FIPS-approved. Fine outside FIPS scope; a finding inside it. |
| **now** | ChaCha20-Poly1305 | `corpus/mixed/python/invoice_service.py` | Not FIPS-approved. Fine outside FIPS scope; a finding inside it. |
| **now** | ChaCha20-Poly1305 | `corpus/pqc/assets/ssh/sshd_config_pq` | Not FIPS-approved. Fine outside FIPS scope; a finding inside it. |
| **now** | ChaCha20-Poly1305 | `corpus/tier1/c/t1_chacha.c` | Not FIPS-approved. Fine outside FIPS scope; a finding inside it. |
| **now** | MD5 | `corpus/tier1/c/t1_digests.c` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | TLS_RSA_WITH_3DES_EDE_CBC_SHA | `corpus/tier1/c/t1_tls_ctx.c` | Cipher suite uses a disallowed bulk cipher. |
| **now** | DES-CBC | `corpus/tier1/go/des/main.go` | Single DES; FIPS 46-3 was withdrawn in 2005. |
| **now** | MD5 | `corpus/tier1/go/hashes/main.go` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | RC4 | `corpus/tier1/go/rc4/main.go` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | TLS_RSA_WITH_3DES_EDE_CBC_SHA | `corpus/tier1/go/tls_config/main.go` | Cipher suite uses a disallowed bulk cipher. |
| **now** | MD5 | `corpus/tier1/java/T1Hashes.java` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | DES-CBC | `corpus/tier1/java/T1LegacyCiphers.java` | Single DES; FIPS 46-3 was withdrawn in 2005. |
| **now** | ChaCha20-Poly1305 | `corpus/tier1/javascript/t1_chacha.js` | Not FIPS-approved. Fine outside FIPS scope; a finding inside it. |
| **now** | MD5 | `corpus/tier1/javascript/t1_hashes.js` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | ChaCha20-Poly1305 | `corpus/tier1/python/t1_chacha.py` | Not FIPS-approved. Fine outside FIPS scope; a finding inside it. |
| **now** | MD5 | `corpus/tier1/python/t1_hashes.py` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | HMAC-MD5 | `corpus/tier2/c/t2_func_ptr.c` | MD5 is not an approved hash function, in HMAC or otherwise. |
| **now** | HMAC-MD5 | `corpus/tier2/go/hmac_func_value/main.go` | MD5 is not an approved hash function, in HMAC or otherwise. |
| **now** | MD5 | `corpus/tier2/java/T2Wrapper.java` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/tier2/python/t2_dispatch_table.py` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | HMAC-MD5 | `corpus/tier2/typescript/t2_hmac_const.ts` | MD5 is not an approved hash function, in HMAC or otherwise. |
| **now** | MD5 | `corpus/tier3/java/dependency_injection/src/com/acme/audit/DigestProvider.java` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/tier3/python/dependency_injection/wiring.py` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | ChaCha20-Poly1305 | `corpus/tier3/python/registry_strategy/suites/builtin.py` | Not FIPS-approved. Fine outside FIPS scope; a finding inside it. |
| **now** | ChaCha20-Poly1305 | `corpus/tier4/assets/ssh/sshd_config` | Not FIPS-approved. Fine outside FIPS scope; a finding inside it. |
| **now** | TLS_RSA_WITH_3DES_EDE_CBC_SHA | `corpus/tier4/assets/tls/nginx.conf` | Cipher suite uses a disallowed bulk cipher. |
| **now** | TEA | `corpus/tier5/java/T5BlockTransform.java` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/tier5/java/T5Reflection.java` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | HMAC-MD5 | `corpus/tier5/python/compiled/ledger_sync.pyc` | MD5 is not an approved hash function, in HMAC or otherwise. |
| **now** | RC4 | `corpus/tier5/python/t5_handrolled_keystream.py` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/tier5/python/t5_string_assembly.py` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | RSA-1024 | `corpus/calibration/tier1/c/cal_rsa_027.c` | Below 112-bit security; disallowed since 2014. |
| **now** | DSA-1024 | `corpus/calibration/tier1/go/cal_dsa_009/cal_dsa_009.go` | Below 112-bit security; disallowed since 2014. |
| **now** | DSA-1024 | `corpus/calibration/tier1/go/cal_dsa_011/cal_dsa_011.go` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/calibration/tier1/go/cal_rsa_030/cal_rsa_030.go` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/calibration/tier1/go/cal_rsa_031/cal_rsa_031.go` | Below 112-bit security; disallowed since 2014. |
| **now** | DSA-1024 | `corpus/calibration/tier1/java/Cal1010DeviceConfig.java` | Below 112-bit security; disallowed since 2014. |
| **now** | DSA-1024 | `corpus/calibration/tier1/java/Cal1011AuditSettings.java` | Below 112-bit security; disallowed since 2014. |
| **now** | DSA-1024 | `corpus/calibration/tier1/java/Cal1012MemberOptions.java` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/calibration/tier1/javascript/cal_rsa_028.js` | Below 112-bit security; disallowed since 2014. |
| **now** | DH-1024 | `corpus/calibration/tier1/python/cal_dh_009.py` | Below 112-bit security; disallowed since 2014. |
| **now** | DH-1024 | `corpus/calibration/tier1/python/cal_dh_010.py` | Below 112-bit security; disallowed since 2014. |
| **now** | DH-512 | `corpus/calibration/tier1/python/cal_dh_011.py` | Below 112-bit security; disallowed since 2014. |
| **now** | DSA-1024 | `corpus/calibration/tier1/python/cal_dsa_012.py` | Below 112-bit security; disallowed since 2014. |
| **now** | DSA-1024 | `corpus/calibration/tier1/python/cal_dsa_013.py` | Below 112-bit security; disallowed since 2014. |
| **now** | DSA-1024 | `corpus/calibration/tier1/python/cal_dsa_014.py` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/calibration/tier1/python/cal_rsa_031.py` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/calibration/tier2/c/cal_rsa_014.c` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/calibration/tier2/c/cal_rsa_015.c` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/calibration/tier2/go/cal_rsa_013/cal_rsa_013.go` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/calibration/tier2/go/cal_rsa_014/cal_rsa_014.go` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/calibration/tier2/go/cal_rsa_015/cal_rsa_015.go` | Below 112-bit security; disallowed since 2014. |
| **now** | DSA-1024 | `corpus/calibration/tier2/java/Cal2008PayloadOptions.java` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/calibration/tier2/python/cal_rsa_014.py` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/calibration/tier2/typescript/cal_rsa_013.ts` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/calibration/tier2/typescript/cal_rsa_014.ts` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/mixed/go/payload_worker/main.go` | Below 112-bit security; disallowed since 2014. |
| **now** | DH-512 | `corpus/mixed/python/invoice_service.py` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/tier1/c/t1_rsa_legacy.c` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/tier2/c/t2_macro_bits.c` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/tier2/go/key_bits/main.go` | Below 112-bit security; disallowed since 2014. |
| **now** | DSA-1024 | `corpus/tier2/java/T2DsaConstant.java` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/tier2/java/T2PropertiesConfig.java` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/tier2/python/t2_alias_import.py` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/tier2/typescript/t2_env_default.ts` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/tier3/java/cross_class_constant/src/com/acme/keys/KeyIssuer.java` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/tier3/python/cross_module_constant/keys/issuer.py` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/tier3/python/wrapper_two_callers/services/billing.py` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/tier4/assets/certs/payments_legacy.crt` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/tier4/assets/keystores/partner_truststore.jks` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/tier4/assets/tls/openssl.cnf` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/tier5/java/compiled/billing-core.jar` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/tier5/python/t5_handrolled_pubkey.py` | Below 112-bit security; disallowed since 2014. |
| **now** | DSA-2048 | `corpus/calibration/tier1/go/cal_dsa_010/cal_dsa_010.go` | DSA signature generation removed by FIPS 186-5; verification of legacy signatures only. |
| **now** | DSA-2048 | `corpus/calibration/tier2/java/Cal2007PayloadDefaults.java` | DSA signature generation removed by FIPS 186-5; verification of legacy signatures only. |
| **now** | DSA-2048 | `corpus/calibration/tier2/java/Cal2009ProfileProfile.java` | DSA signature generation removed by FIPS 186-5; verification of legacy signatures only. |
| **now** | DSA-2048 | `corpus/tier1/go/dsa/main.go` | DSA signature generation removed by FIPS 186-5; verification of legacy signatures only. |
| **now** | DSA-2048 | `corpus/tier1/java/T1Dsa.java` | DSA signature generation removed by FIPS 186-5; verification of legacy signatures only. |
| **now** | DSA-2048 | `corpus/tier1/python/t1_dsa.py` | DSA signature generation removed by FIPS 186-5; verification of legacy signatures only. |
| **now** | 3DES-CBC | `corpus/calibration/tier1/c/cal_3des_001.c` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier1/c/cal_3des_002.c` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier1/c/cal_3des_003.c` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier1/go/cal_3des_001/cal_3des_001.go` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier1/go/cal_3des_002/cal_3des_002.go` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier1/go/cal_3des_003/cal_3des_003.go` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier1/java/Cal1001InvoiceConfig.java` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier1/java/Cal1002ClaimOptions.java` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier1/java/Cal1003SessionProfile.java` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier1/javascript/cal_3des_001.js` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier1/javascript/cal_3des_002.js` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier1/javascript/cal_3des_003.js` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier1/python/cal_3des_001.py` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier1/python/cal_3des_002.py` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier1/python/cal_3des_003.py` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-ECB | `corpus/calibration/tier2/c/cal_3des_001.c` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-ECB | `corpus/calibration/tier2/c/cal_3des_002.c` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-ECB | `corpus/calibration/tier2/c/cal_3des_003.c` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier2/go/cal_3des_001/cal_3des_001.go` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier2/go/cal_3des_002/cal_3des_002.go` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier2/go/cal_3des_003/cal_3des_003.go` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier2/java/Cal2001UploadConfig.java` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier2/java/Cal2002VoucherDefaults.java` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier2/java/Cal2003VoucherConfig.java` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier2/typescript/cal_3des_001.ts` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier2/typescript/cal_3des_002.ts` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier2/typescript/cal_3des_003.ts` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/mixed/c/audit_daemon.c` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-ECB | `corpus/mixed/c/policy_agent.c` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/mixed/go/report_gateway/main.go` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-ECB | `corpus/mixed/java/OrderDefaultsModule.java` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/tier1/c/t1_triple_des.c` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/tier1/go/des/main.go` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/tier1/java/T1LegacyCiphers.java` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/tier1/javascript/t1_triple_des.js` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/tier1/python/t1_triple_des.py` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-ECB | `corpus/tier2/c/t2_cipher_struct.c` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/tier2/go/block_factory/main.go` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/tier2/java/T2ConcatTransform.java` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/tier2/typescript/t2_config_object.ts` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/tier3/java/strategy_factory/src/com/acme/crypto/LegacyDesedeCipher.java` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/tier5/java/T5StringAssembly.java` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| 2030-12-31 | PBKDF2-HMAC-SHA-1 | `corpus/calibration/tier1/c/cal_pbkdf2_024.c` | All SHA-1 uses end Dec 31, 2030. |
| 2030-12-31 | PBKDF2-HMAC-SHA-1 | `corpus/calibration/tier1/c/cal_pbkdf2_025.c` | All SHA-1 uses end Dec 31, 2030. |
| 2030-12-31 | PBKDF2-HMAC-SHA-1 | `corpus/calibration/tier1/c/cal_pbkdf2_026.c` | All SHA-1 uses end Dec 31, 2030. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier1/c/cal_sha1_029.c` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier1/c/cal_sha1_030.c` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier1/c/cal_sha1_031.c` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier1/go/cal_sha1_033/cal_sha1_033.go` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier1/go/cal_sha1_034/cal_sha1_034.go` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier1/go/cal_sha1_035/cal_sha1_035.go` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier1/java/Cal1031ReceiptOptions.java` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier1/java/Cal1032BookingConfig.java` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier1/java/Cal1033BillingConfig.java` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier1/javascript/cal_sha1_029.js` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier1/javascript/cal_sha1_030.js` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | HMAC-SHA-1 | `corpus/calibration/tier1/python/cal_hmac_022.py` | All SHA-1 uses end Dec 31, 2030. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier1/python/cal_sha1_033.py` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier1/python/cal_sha1_034.py` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier1/python/cal_sha1_035.py` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier2/c/cal_sha1_016.c` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier2/c/cal_sha1_017.c` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier2/c/cal_sha1_018.c` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier2/go/cal_sha1_016/cal_sha1_016.go` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier2/go/cal_sha1_017/cal_sha1_017.go` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier2/go/cal_sha1_018/cal_sha1_018.go` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier2/java/Cal2019ClaimDefaults.java` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier2/java/Cal2020TenantDefaults.java` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier2/java/Cal2021ReportOptions.java` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | HMAC-SHA-1 | `corpus/calibration/tier2/python/cal_hmac_006.py` | All SHA-1 uses end Dec 31, 2030. |
| 2030-12-31 | HMAC-SHA-1 | `corpus/calibration/tier2/python/cal_hmac_007.py` | All SHA-1 uses end Dec 31, 2030. |
| 2030-12-31 | HMAC-SHA-1 | `corpus/calibration/tier2/python/cal_hmac_008.py` | All SHA-1 uses end Dec 31, 2030. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier2/python/cal_sha1_015.py` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier2/python/cal_sha1_016.py` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier2/typescript/cal_sha1_015.ts` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier2/typescript/cal_sha1_016.ts` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier2/typescript/cal_sha1_017.ts` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/mixed/c/device_daemon.c` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | HMAC-SHA-1 | `corpus/mixed/go/invoice_gateway/main.go` | All SHA-1 uses end Dec 31, 2030. |
| 2030-12-31 | SHA-1 | `corpus/mixed/java/VoucherProfileModule.java` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/mixed/python/order_jobs.py` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/tier1/c/t1_digests.c` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | PBKDF2-HMAC-SHA-1 | `corpus/tier1/c/t1_mac_kdf.c` | All SHA-1 uses end Dec 31, 2030. |
| 2030-12-31 | SHA-1 | `corpus/tier1/go/hashes/main.go` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/tier1/java/T1Hashes.java` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/tier1/javascript/t1_hashes.js` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/tier1/javascript/t1_webcrypto.mjs` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/tier1/python/t1_hashes.py` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/tier2/c/t2_digest_table.c` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/tier2/go/hash_enum/main.go` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/tier2/java/T2Enum.java` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/tier2/python/t2_constant_hash.py` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/tier2/python/t2_env_default.py` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | HMAC-SHA-1 | `corpus/tier2/python/t2_partial.py` | All SHA-1 uses end Dec 31, 2030. |
| 2030-12-31 | SHA-1 | `corpus/tier2/typescript/t2_default_param.ts` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/tier3/java/cross_class_constant/src/com/acme/tokens/Fingerprint.java` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/tier3/python/cross_module_constant/tokens/fingerprint.py` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/tier4/assets/certs/payments_legacy.crt` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/tier4/assets/keystores/partner_truststore.jks` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | HMAC-SHA-1 | `corpus/tier4/assets/ssh/sshd_config` | All SHA-1 uses end Dec 31, 2030. |
| 2030-12-31 | SHA-1 | `corpus/tier4/assets/tls/openssl.cnf` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/tier5/java/compiled/billing-core.jar` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/tier5/python/compiled/ledger_sync.pyc` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/tier5/python/t5_string_assembly.py` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |

### Needs a human decision (7)

- `corpus/tier1/c/t1_tls_ctx.c`: TLS-1.0: review. TLS 1.2 is required. Government-only servers shall not use TLS 1.0 and should not use 1.1; citizen- or business-facing servers may still enable them for interoperability. Agencies must support TLS 1.3 since Jan 1, 2024.
- `corpus/tier1/go/tls_config/main.go`: TLS-1.0: review. TLS 1.2 is required. Government-only servers shall not use TLS 1.0 and should not use 1.1; citizen- or business-facing servers may still enable them for interoperability. Agencies must support TLS 1.3 since Jan 1, 2024.
- `corpus/tier4/assets/keys/treasury_hot_wallet.key`: ECC-secp256k1: review. Not among SP 800-186's curves for federal use; allowed only for blockchain-related applications.
- `corpus/tier4/assets/tls/application.yml`: TLS-1.1: review. TLS 1.2 is required. Government-only servers shall not use TLS 1.0 and should not use 1.1; citizen- or business-facing servers may still enable them for interoperability. Agencies must support TLS 1.3 since Jan 1, 2024.
- `corpus/tier4/assets/tls/nginx.conf`: TLS-1.0: review. TLS 1.2 is required. Government-only servers shall not use TLS 1.0 and should not use 1.1; citizen- or business-facing servers may still enable them for interoperability. Agencies must support TLS 1.3 since Jan 1, 2024.
- `corpus/tier4/assets/tls/nginx.conf`: TLS-1.1: review. TLS 1.2 is required. Government-only servers shall not use TLS 1.0 and should not use 1.1; citizen- or business-facing servers may still enable them for interoperability. Agencies must support TLS 1.3 since Jan 1, 2024.
- `corpus/tier4/assets/tls/openssl.cnf`: TLS-1.0: review. TLS 1.2 is required. Government-only servers shall not use TLS 1.0 and should not use 1.1; citizen- or business-facing servers may still enable them for interoperability. Agencies must support TLS 1.3 since Jan 1, 2024.

## NSA CNSA 2.0

_National Security Systems and vendors selling into them. Dates depend on the kind of system (the finding's 'use')._

| When | Findings | Quantum-vulnerable | Files |
|---|---|---|---|
| Due now (not approved or past its date) | 476 | 168 | 406 |
| Due by end of 2030 | 0 | 0 | 0 |
| Due 2031 to 2033 | 40 | 40 | 39 |
| Due 2034 to 2035 | 0 | 0 | 0 |
| No deadline (approved, review, out of scope, unknown) | 83 | 11 | 64 |

### Due now or by end of 2030 (476)

| Due | Algorithm | File | Why |
|---|---|---|---|
| **now** | 3DES-CBC | `corpus/calibration/tier1/c/cal_3des_001.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | 3DES-CBC | `corpus/calibration/tier1/c/cal_3des_002.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | 3DES-CBC | `corpus/calibration/tier1/c/cal_3des_003.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | AES-128-ECB | `corpus/calibration/tier1/c/cal_aes_004.c` | CNSA requires 256-bit AES keys. |
| **now** | AES-128-ECB | `corpus/calibration/tier1/c/cal_aes_005.c` | CNSA requires 256-bit AES keys. |
| **now** | ChaCha20-Poly1305 | `corpus/calibration/tier1/c/cal_chacha20poly1305_006.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | ChaCha20-Poly1305 | `corpus/calibration/tier1/c/cal_chacha20poly1305_007.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | ChaCha20-Poly1305 | `corpus/calibration/tier1/c/cal_chacha20poly1305_008.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | DH-2048 | `corpus/calibration/tier1/c/cal_dh_009.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | DH-2048 | `corpus/calibration/tier1/c/cal_dh_010.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | ECC-P-256 | `corpus/calibration/tier1/c/cal_ec_013.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | ECC-P-521 | `corpus/calibration/tier1/c/cal_ec_014.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | Ed25519 | `corpus/calibration/tier1/c/cal_ed25519_015.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | Ed25519 | `corpus/calibration/tier1/c/cal_ed25519_016.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | Ed25519 | `corpus/calibration/tier1/c/cal_ed25519_017.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-SHA-256 | `corpus/calibration/tier1/c/cal_hmac_018.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-SHA-256 | `corpus/calibration/tier1/c/cal_hmac_019.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-SHA-256 | `corpus/calibration/tier1/c/cal_hmac_020.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | MD5 | `corpus/calibration/tier1/c/cal_md5_021.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | MD5 | `corpus/calibration/tier1/c/cal_md5_022.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | MD5 | `corpus/calibration/tier1/c/cal_md5_023.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-1024 | `corpus/calibration/tier1/c/cal_rsa_027.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-2048 | `corpus/calibration/tier1/c/cal_rsa_028.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/calibration/tier1/c/cal_sha1_029.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/calibration/tier1/c/cal_sha1_030.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/calibration/tier1/c/cal_sha1_031.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-256 | `corpus/calibration/tier1/c/cal_sha256_032.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-256 | `corpus/calibration/tier1/c/cal_sha256_033.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-256 | `corpus/calibration/tier1/c/cal_sha256_034.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA3-256 | `corpus/calibration/tier1/c/cal_sha3256_035.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA3-256 | `corpus/calibration/tier1/c/cal_sha3256_036.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA3-256 | `corpus/calibration/tier1/c/cal_sha3256_037.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | X25519 | `corpus/calibration/tier1/c/cal_x25519_038.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | X25519 | `corpus/calibration/tier1/c/cal_x25519_039.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | X25519 | `corpus/calibration/tier1/c/cal_x25519_040.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | 3DES-CBC | `corpus/calibration/tier1/go/cal_3des_001/cal_3des_001.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | 3DES-CBC | `corpus/calibration/tier1/go/cal_3des_002/cal_3des_002.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | 3DES-CBC | `corpus/calibration/tier1/go/cal_3des_003/cal_3des_003.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | AES-128-CBC | `corpus/calibration/tier1/go/cal_aes_004/cal_aes_004.go` | CNSA requires 256-bit AES keys. |
| **now** | AES-128-GCM | `corpus/calibration/tier1/go/cal_aes_005/cal_aes_005.go` | CNSA requires 256-bit AES keys. |
| **now** | DES-CBC | `corpus/calibration/tier1/go/cal_des_006/cal_des_006.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | DES-CBC | `corpus/calibration/tier1/go/cal_des_007/cal_des_007.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | DES-CBC | `corpus/calibration/tier1/go/cal_des_008/cal_des_008.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | DSA-1024 | `corpus/calibration/tier1/go/cal_dsa_009/cal_dsa_009.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | DSA-2048 | `corpus/calibration/tier1/go/cal_dsa_010/cal_dsa_010.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | DSA-1024 | `corpus/calibration/tier1/go/cal_dsa_011/cal_dsa_011.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | ECC-P-521 | `corpus/calibration/tier1/go/cal_ec_012/cal_ec_012.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | ECC-P-521 | `corpus/calibration/tier1/go/cal_ec_014/cal_ec_014.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | Ed25519 | `corpus/calibration/tier1/go/cal_ed25519_015/cal_ed25519_015.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | Ed25519 | `corpus/calibration/tier1/go/cal_ed25519_016/cal_ed25519_016.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | Ed25519 | `corpus/calibration/tier1/go/cal_ed25519_017/cal_ed25519_017.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-SHA-256 | `corpus/calibration/tier1/go/cal_hmac_018/cal_hmac_018.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-SHA-256 | `corpus/calibration/tier1/go/cal_hmac_019/cal_hmac_019.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-SHA-256 | `corpus/calibration/tier1/go/cal_hmac_020/cal_hmac_020.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | MD5 | `corpus/calibration/tier1/go/cal_md5_021/cal_md5_021.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | MD5 | `corpus/calibration/tier1/go/cal_md5_022/cal_md5_022.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | MD5 | `corpus/calibration/tier1/go/cal_md5_023/cal_md5_023.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RC4 | `corpus/calibration/tier1/go/cal_rc4_027/cal_rc4_027.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RC4 | `corpus/calibration/tier1/go/cal_rc4_028/cal_rc4_028.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RC4 | `corpus/calibration/tier1/go/cal_rc4_029/cal_rc4_029.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-1024 | `corpus/calibration/tier1/go/cal_rsa_030/cal_rsa_030.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-1024 | `corpus/calibration/tier1/go/cal_rsa_031/cal_rsa_031.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-2048 | `corpus/calibration/tier1/go/cal_rsa_032/cal_rsa_032.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/calibration/tier1/go/cal_sha1_033/cal_sha1_033.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/calibration/tier1/go/cal_sha1_034/cal_sha1_034.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/calibration/tier1/go/cal_sha1_035/cal_sha1_035.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-256 | `corpus/calibration/tier1/go/cal_sha256_036/cal_sha256_036.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-256 | `corpus/calibration/tier1/go/cal_sha256_037/cal_sha256_037.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-256 | `corpus/calibration/tier1/go/cal_sha256_038/cal_sha256_038.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA3-256 | `corpus/calibration/tier1/go/cal_sha3256_039/cal_sha3256_039.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA3-256 | `corpus/calibration/tier1/go/cal_sha3256_040/cal_sha3256_040.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA3-256 | `corpus/calibration/tier1/go/cal_sha3256_041/cal_sha3256_041.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | X25519 | `corpus/calibration/tier1/go/cal_x25519_042/cal_x25519_042.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | X25519 | `corpus/calibration/tier1/go/cal_x25519_043/cal_x25519_043.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | X25519 | `corpus/calibration/tier1/go/cal_x25519_044/cal_x25519_044.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | 3DES-CBC | `corpus/calibration/tier1/java/Cal1001InvoiceConfig.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | 3DES-CBC | `corpus/calibration/tier1/java/Cal1002ClaimOptions.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | 3DES-CBC | `corpus/calibration/tier1/java/Cal1003SessionProfile.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | AES-128-GCM | `corpus/calibration/tier1/java/Cal1005MemberSettings.java` | CNSA requires 256-bit AES keys. |
| **now** | DH-2048 | `corpus/calibration/tier1/java/Cal1009ClaimConfig.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | DSA-1024 | `corpus/calibration/tier1/java/Cal1010DeviceConfig.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | DSA-1024 | `corpus/calibration/tier1/java/Cal1011AuditSettings.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | DSA-1024 | `corpus/calibration/tier1/java/Cal1012MemberOptions.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | ECC-P-521 | `corpus/calibration/tier1/java/Cal1013ArchiveOptions.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | ECC-P-256 | `corpus/calibration/tier1/java/Cal1014EventProfile.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | ECC-P-521 | `corpus/calibration/tier1/java/Cal1015PayloadConfig.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | Ed25519 | `corpus/calibration/tier1/java/Cal1016PayloadDefaults.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | Ed25519 | `corpus/calibration/tier1/java/Cal1017CatalogSettings.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | Ed25519 | `corpus/calibration/tier1/java/Cal1018DeviceOptions.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-SHA-256 | `corpus/calibration/tier1/java/Cal1019AccountConfig.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-SHA-256 | `corpus/calibration/tier1/java/Cal1020BookingConfig.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-SHA-256 | `corpus/calibration/tier1/java/Cal1021ArchiveOptions.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | MD5 | `corpus/calibration/tier1/java/Cal1022LedgerDefaults.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | MD5 | `corpus/calibration/tier1/java/Cal1023AuditProfile.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | MD5 | `corpus/calibration/tier1/java/Cal1024PolicyDefaults.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-2048 | `corpus/calibration/tier1/java/Cal1030DeviceOptions.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/calibration/tier1/java/Cal1031ReceiptOptions.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/calibration/tier1/java/Cal1032BookingConfig.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/calibration/tier1/java/Cal1033BillingConfig.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-256 | `corpus/calibration/tier1/java/Cal1034ProfileDefaults.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-256 | `corpus/calibration/tier1/java/Cal1035EventOptions.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-256 | `corpus/calibration/tier1/java/Cal1036PolicyOptions.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA3-256 | `corpus/calibration/tier1/java/Cal1037ShipmentSettings.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA3-256 | `corpus/calibration/tier1/java/Cal1038MemberOptions.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA3-256 | `corpus/calibration/tier1/java/Cal1039PayloadDefaults.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | X25519 | `corpus/calibration/tier1/java/Cal1040ProfileSettings.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | X25519 | `corpus/calibration/tier1/java/Cal1041OrderSettings.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | X25519 | `corpus/calibration/tier1/java/Cal1042AccountProfile.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | 3DES-CBC | `corpus/calibration/tier1/javascript/cal_3des_001.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | 3DES-CBC | `corpus/calibration/tier1/javascript/cal_3des_002.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | 3DES-CBC | `corpus/calibration/tier1/javascript/cal_3des_003.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | AES-128-CBC | `corpus/calibration/tier1/javascript/cal_aes_004.js` | CNSA requires 256-bit AES keys. |
| **now** | AES-128-CBC | `corpus/calibration/tier1/javascript/cal_aes_005.js` | CNSA requires 256-bit AES keys. |
| **now** | ChaCha20-Poly1305 | `corpus/calibration/tier1/javascript/cal_chacha20poly1305_006.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | ChaCha20-Poly1305 | `corpus/calibration/tier1/javascript/cal_chacha20poly1305_007.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | ChaCha20-Poly1305 | `corpus/calibration/tier1/javascript/cal_chacha20poly1305_008.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | DH-2048 | `corpus/calibration/tier1/javascript/cal_dh_010.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | ECC-P-256 | `corpus/calibration/tier1/javascript/cal_ec_013.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | Ed25519 | `corpus/calibration/tier1/javascript/cal_ed25519_015.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | Ed25519 | `corpus/calibration/tier1/javascript/cal_ed25519_016.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | Ed25519 | `corpus/calibration/tier1/javascript/cal_ed25519_017.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-SHA-256 | `corpus/calibration/tier1/javascript/cal_hmac_018.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-SHA-256 | `corpus/calibration/tier1/javascript/cal_hmac_019.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-SHA-256 | `corpus/calibration/tier1/javascript/cal_hmac_020.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | MD5 | `corpus/calibration/tier1/javascript/cal_md5_021.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | MD5 | `corpus/calibration/tier1/javascript/cal_md5_022.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | MD5 | `corpus/calibration/tier1/javascript/cal_md5_023.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-2048 | `corpus/calibration/tier1/javascript/cal_rsa_027.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-1024 | `corpus/calibration/tier1/javascript/cal_rsa_028.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/calibration/tier1/javascript/cal_sha1_029.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/calibration/tier1/javascript/cal_sha1_030.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-256 | `corpus/calibration/tier1/javascript/cal_sha256_031.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-256 | `corpus/calibration/tier1/javascript/cal_sha256_032.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-256 | `corpus/calibration/tier1/javascript/cal_sha256_033.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA3-256 | `corpus/calibration/tier1/javascript/cal_sha3256_034.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA3-256 | `corpus/calibration/tier1/javascript/cal_sha3256_035.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA3-256 | `corpus/calibration/tier1/javascript/cal_sha3256_036.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | X25519 | `corpus/calibration/tier1/javascript/cal_x25519_037.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | X25519 | `corpus/calibration/tier1/javascript/cal_x25519_038.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | X25519 | `corpus/calibration/tier1/javascript/cal_x25519_039.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | 3DES-CBC | `corpus/calibration/tier1/python/cal_3des_001.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | 3DES-CBC | `corpus/calibration/tier1/python/cal_3des_002.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | 3DES-CBC | `corpus/calibration/tier1/python/cal_3des_003.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | AES-192-GCM | `corpus/calibration/tier1/python/cal_aes_004.py` | CNSA requires 256-bit AES keys. |
| **now** | AES-128-GCM | `corpus/calibration/tier1/python/cal_aes_005.py` | CNSA requires 256-bit AES keys. |
| **now** | ChaCha20-Poly1305 | `corpus/calibration/tier1/python/cal_chacha20poly1305_006.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | ChaCha20-Poly1305 | `corpus/calibration/tier1/python/cal_chacha20poly1305_007.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | ChaCha20-Poly1305 | `corpus/calibration/tier1/python/cal_chacha20poly1305_008.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | DH-1024 | `corpus/calibration/tier1/python/cal_dh_009.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | DH-1024 | `corpus/calibration/tier1/python/cal_dh_010.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | DH-512 | `corpus/calibration/tier1/python/cal_dh_011.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | DSA-1024 | `corpus/calibration/tier1/python/cal_dsa_012.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | DSA-1024 | `corpus/calibration/tier1/python/cal_dsa_013.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | DSA-1024 | `corpus/calibration/tier1/python/cal_dsa_014.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | ECC-P-256 | `corpus/calibration/tier1/python/cal_ec_015.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | ECC-P-521 | `corpus/calibration/tier1/python/cal_ec_016.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | Ed25519 | `corpus/calibration/tier1/python/cal_ed25519_018.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | Ed25519 | `corpus/calibration/tier1/python/cal_ed25519_019.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | Ed25519 | `corpus/calibration/tier1/python/cal_ed25519_020.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-SHA-256 | `corpus/calibration/tier1/python/cal_hmac_021.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-SHA-1 | `corpus/calibration/tier1/python/cal_hmac_022.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-SHA-256 | `corpus/calibration/tier1/python/cal_hmac_023.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | MD5 | `corpus/calibration/tier1/python/cal_md5_024.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | MD5 | `corpus/calibration/tier1/python/cal_md5_025.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | MD5 | `corpus/calibration/tier1/python/cal_md5_026.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-1024 | `corpus/calibration/tier1/python/cal_rsa_031.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-2048 | `corpus/calibration/tier1/python/cal_rsa_032.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/calibration/tier1/python/cal_sha1_033.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/calibration/tier1/python/cal_sha1_034.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/calibration/tier1/python/cal_sha1_035.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-256 | `corpus/calibration/tier1/python/cal_sha256_036.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-256 | `corpus/calibration/tier1/python/cal_sha256_037.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-256 | `corpus/calibration/tier1/python/cal_sha256_038.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA3-256 | `corpus/calibration/tier1/python/cal_sha3256_039.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA3-256 | `corpus/calibration/tier1/python/cal_sha3256_040.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA3-256 | `corpus/calibration/tier1/python/cal_sha3256_041.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | X25519 | `corpus/calibration/tier1/python/cal_x25519_042.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | X25519 | `corpus/calibration/tier1/python/cal_x25519_043.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | X25519 | `corpus/calibration/tier1/python/cal_x25519_044.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | 3DES-ECB | `corpus/calibration/tier2/c/cal_3des_001.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | 3DES-ECB | `corpus/calibration/tier2/c/cal_3des_002.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | 3DES-ECB | `corpus/calibration/tier2/c/cal_3des_003.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | AES-192-CBC | `corpus/calibration/tier2/c/cal_aes_004.c` | CNSA requires 256-bit AES keys. |
| **now** | AES-192-CBC | `corpus/calibration/tier2/c/cal_aes_005.c` | CNSA requires 256-bit AES keys. |
| **now** | AES-192-CBC | `corpus/calibration/tier2/c/cal_aes_006.c` | CNSA requires 256-bit AES keys. |
| **now** | ECC-P-521 | `corpus/calibration/tier2/c/cal_ec_008.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-MD5 | `corpus/calibration/tier2/c/cal_hmac_010.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-MD5 | `corpus/calibration/tier2/c/cal_hmac_011.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-MD5 | `corpus/calibration/tier2/c/cal_hmac_012.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-2048 | `corpus/calibration/tier2/c/cal_rsa_013.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-1024 | `corpus/calibration/tier2/c/cal_rsa_014.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-1024 | `corpus/calibration/tier2/c/cal_rsa_015.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/calibration/tier2/c/cal_sha1_016.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/calibration/tier2/c/cal_sha1_017.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/calibration/tier2/c/cal_sha1_018.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | 3DES-CBC | `corpus/calibration/tier2/go/cal_3des_001/cal_3des_001.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | 3DES-CBC | `corpus/calibration/tier2/go/cal_3des_002/cal_3des_002.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | 3DES-CBC | `corpus/calibration/tier2/go/cal_3des_003/cal_3des_003.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | ECC-P-256 | `corpus/calibration/tier2/go/cal_ec_007/cal_ec_007.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | ECC-P-521 | `corpus/calibration/tier2/go/cal_ec_009/cal_ec_009.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-MD5 | `corpus/calibration/tier2/go/cal_hmac_010/cal_hmac_010.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-MD5 | `corpus/calibration/tier2/go/cal_hmac_011/cal_hmac_011.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-MD5 | `corpus/calibration/tier2/go/cal_hmac_012/cal_hmac_012.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-1024 | `corpus/calibration/tier2/go/cal_rsa_013/cal_rsa_013.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-1024 | `corpus/calibration/tier2/go/cal_rsa_014/cal_rsa_014.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-1024 | `corpus/calibration/tier2/go/cal_rsa_015/cal_rsa_015.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/calibration/tier2/go/cal_sha1_016/cal_sha1_016.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/calibration/tier2/go/cal_sha1_017/cal_sha1_017.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/calibration/tier2/go/cal_sha1_018/cal_sha1_018.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | 3DES-CBC | `corpus/calibration/tier2/java/Cal2001UploadConfig.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | 3DES-CBC | `corpus/calibration/tier2/java/Cal2002VoucherDefaults.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | 3DES-CBC | `corpus/calibration/tier2/java/Cal2003VoucherConfig.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | AES-192-ECB | `corpus/calibration/tier2/java/Cal2004AccountSettings.java` | CNSA requires 256-bit AES keys. |
| **now** | AES-192-ECB | `corpus/calibration/tier2/java/Cal2005TenantSettings.java` | CNSA requires 256-bit AES keys. |
| **now** | AES-128-ECB | `corpus/calibration/tier2/java/Cal2006BillingOptions.java` | CNSA requires 256-bit AES keys. |
| **now** | DSA-2048 | `corpus/calibration/tier2/java/Cal2007PayloadDefaults.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | DSA-1024 | `corpus/calibration/tier2/java/Cal2008PayloadOptions.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | DSA-2048 | `corpus/calibration/tier2/java/Cal2009ProfileProfile.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | ECC-P-256 | `corpus/calibration/tier2/java/Cal2011DeviceOptions.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | MD5 | `corpus/calibration/tier2/java/Cal2013TenantOptions.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | MD5 | `corpus/calibration/tier2/java/Cal2014DeviceDefaults.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | MD5 | `corpus/calibration/tier2/java/Cal2015UploadSettings.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-2048 | `corpus/calibration/tier2/java/Cal2016RecordConfig.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-2048 | `corpus/calibration/tier2/java/Cal2017ReportSettings.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-2048 | `corpus/calibration/tier2/java/Cal2018ReceiptProfile.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/calibration/tier2/java/Cal2019ClaimDefaults.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/calibration/tier2/java/Cal2020TenantDefaults.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/calibration/tier2/java/Cal2021ReportOptions.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-256 | `corpus/calibration/tier2/java/Cal2022ShipmentSettings.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-256 | `corpus/calibration/tier2/java/Cal2023TenantOptions.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-256 | `corpus/calibration/tier2/java/Cal2024TenantSettings.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | ECC-P-256 | `corpus/calibration/tier2/python/cal_ec_003.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | ECC-P-521 | `corpus/calibration/tier2/python/cal_ec_005.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-SHA-1 | `corpus/calibration/tier2/python/cal_hmac_006.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-SHA-1 | `corpus/calibration/tier2/python/cal_hmac_007.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-SHA-1 | `corpus/calibration/tier2/python/cal_hmac_008.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | MD5 | `corpus/calibration/tier2/python/cal_md5_009.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | MD5 | `corpus/calibration/tier2/python/cal_md5_010.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | MD5 | `corpus/calibration/tier2/python/cal_md5_011.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-2048 | `corpus/calibration/tier2/python/cal_rsa_012.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-1024 | `corpus/calibration/tier2/python/cal_rsa_014.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/calibration/tier2/python/cal_sha1_015.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/calibration/tier2/python/cal_sha1_016.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-256 | `corpus/calibration/tier2/python/cal_sha256_017.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-256 | `corpus/calibration/tier2/python/cal_sha256_018.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-256 | `corpus/calibration/tier2/python/cal_sha256_019.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | 3DES-CBC | `corpus/calibration/tier2/typescript/cal_3des_001.ts` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | 3DES-CBC | `corpus/calibration/tier2/typescript/cal_3des_002.ts` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | 3DES-CBC | `corpus/calibration/tier2/typescript/cal_3des_003.ts` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | AES-128-ECB | `corpus/calibration/tier2/typescript/cal_aes_004.ts` | CNSA requires 256-bit AES keys. |
| **now** | ECC-P-256 | `corpus/calibration/tier2/typescript/cal_ec_008.ts` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-MD5 | `corpus/calibration/tier2/typescript/cal_hmac_009.ts` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-MD5 | `corpus/calibration/tier2/typescript/cal_hmac_010.ts` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-MD5 | `corpus/calibration/tier2/typescript/cal_hmac_011.ts` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-2048 | `corpus/calibration/tier2/typescript/cal_rsa_012.ts` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-1024 | `corpus/calibration/tier2/typescript/cal_rsa_013.ts` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-1024 | `corpus/calibration/tier2/typescript/cal_rsa_014.ts` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/calibration/tier2/typescript/cal_sha1_015.ts` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/calibration/tier2/typescript/cal_sha1_016.ts` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/calibration/tier2/typescript/cal_sha1_017.ts` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | AES-128-CBC | `corpus/custom/example_envelope/envelope/bulk_chained.py` | CNSA requires 256-bit AES keys. |
| **now** | ECC-P-256 | `corpus/custom/example_envelope/envelope/wrap_agreement.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-2048 | `corpus/custom/example_envelope/envelope/wrap_transport.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | 3DES-CBC | `corpus/mixed/c/audit_daemon.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | AES-192-CBC | `corpus/mixed/c/audit_daemon.c` | CNSA requires 256-bit AES keys. |
| **now** | ECC-P-521 | `corpus/mixed/c/device_daemon.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-MD5 | `corpus/mixed/c/device_daemon.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/mixed/c/device_daemon.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | X25519 | `corpus/mixed/c/device_daemon.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | 3DES-ECB | `corpus/mixed/c/policy_agent.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | AES-192-CBC | `corpus/mixed/c/policy_agent.c` | CNSA requires 256-bit AES keys. |
| **now** | Ed25519 | `corpus/mixed/go/invoice_gateway/main.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-SHA-1 | `corpus/mixed/go/invoice_gateway/main.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RC4 | `corpus/mixed/go/invoice_gateway/main.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-2048 | `corpus/mixed/go/invoice_gateway/main.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | ML-KEM-768 | `corpus/mixed/go/payload_worker/main.go` | Post-quantum, but not at CNSA 2.0 parameters (ML-KEM-1024, ML-DSA-87 only). |
| **now** | RSA-1024 | `corpus/mixed/go/payload_worker/main.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | 3DES-CBC | `corpus/mixed/go/report_gateway/main.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | DES-CBC | `corpus/mixed/go/report_gateway/main.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | Ed25519 | `corpus/mixed/java/BookingOptionsModule.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-256 | `corpus/mixed/java/BookingOptionsModule.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | 3DES-ECB | `corpus/mixed/java/OrderDefaultsModule.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | ChaCha20-Poly1305 | `corpus/mixed/java/OrderDefaultsModule.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-SHA-256 | `corpus/mixed/java/OrderDefaultsModule.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | AES-192-ECB | `corpus/mixed/java/VoucherProfileModule.java` | CNSA requires 256-bit AES keys. |
| **now** | SHA-1 | `corpus/mixed/java/VoucherProfileModule.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | ECC-P-521 | `corpus/mixed/javascript/device_session.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA3-256 | `corpus/mixed/javascript/device_session.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | AES-128-CBC | `corpus/mixed/javascript/partner_routes.js` | CNSA requires 256-bit AES keys. |
| **now** | ChaCha20-Poly1305 | `corpus/mixed/python/invoice_service.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | DH-512 | `corpus/mixed/python/invoice_service.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | ML-DSA-65 | `corpus/mixed/python/invoice_service.py` | Post-quantum, but not at CNSA 2.0 parameters (ML-KEM-1024, ML-DSA-87 only). |
| **now** | AES-192-CTR | `corpus/mixed/python/metric_service.py` | CNSA requires 256-bit AES keys. |
| **now** | ECC-P-256 | `corpus/mixed/python/order_jobs.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/mixed/python/order_jobs.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | AES-128-ECB | `corpus/mixed/typescript/voucher_service.ts` | CNSA requires 256-bit AES keys. |
| **now** | ECC-P-256 | `corpus/mixed/typescript/voucher_service.ts` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-2048 | `corpus/mixed/typescript/voucher_service.ts` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | ML-DSA-65 | `corpus/pqc/assets/certs/migrated_leaf.pem` | Post-quantum, but not at CNSA 2.0 parameters (ML-KEM-1024, ML-DSA-87 only). |
| **now** | RSA | `corpus/pqc/assets/certs/migrated_leaf.pem` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-256 | `corpus/pqc/assets/certs/migrated_leaf.pem` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | ML-DSA-65 | `corpus/pqc/assets/certs/release_root_mldsa.pem` | Post-quantum, but not at CNSA 2.0 parameters (ML-KEM-1024, ML-DSA-87 only). |
| **now** | ML-DSA-44 | `corpus/pqc/assets/keys/attestation_signer.pem` | Post-quantum, but not at CNSA 2.0 parameters (ML-KEM-1024, ML-DSA-87 only). |
| **now** | ML-KEM-768 | `corpus/pqc/assets/keys/kem_recipient_pub.pem` | Post-quantum, but not at CNSA 2.0 parameters (ML-KEM-1024, ML-DSA-87 only). |
| **now** | ChaCha20-Poly1305 | `corpus/pqc/assets/ssh/sshd_config_pq` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | Ed25519 | `corpus/pqc/assets/ssh/sshd_config_pq` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | X25519 | `corpus/pqc/assets/ssh/sshd_config_pq` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | X25519MLKEM768 | `corpus/pqc/assets/ssh/sshd_config_pq` | Post-quantum, but not at CNSA 2.0 parameters (ML-KEM-1024, ML-DSA-87 only). |
| **now** | sntrup761x25519 | `corpus/pqc/assets/ssh/sshd_config_pq` | Post-quantum, but not at CNSA 2.0 parameters (ML-KEM-1024, ML-DSA-87 only). |
| **now** | X25519 | `corpus/pqc/assets/tls/nginx_pq.conf` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | X25519MLKEM768 | `corpus/pqc/assets/tls/nginx_pq.conf` | Post-quantum, but not at CNSA 2.0 parameters (ML-KEM-1024, ML-DSA-87 only). |
| **now** | ECC-P-256 | `corpus/pqc/assets/tls/nginx_pq_washing.conf` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | X25519 | `corpus/pqc/assets/tls/nginx_pq_washing.conf` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | X25519MLKEM768 | `corpus/pqc/assets/tls/openssl_pq.cnf` | Post-quantum, but not at CNSA 2.0 parameters (ML-KEM-1024, ML-DSA-87 only). |
| **now** | X25519 | `corpus/pqc/go/tls_hybrid/main.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | X25519MLKEM768 | `corpus/pqc/go/tls_hybrid/main.go` | Post-quantum, but not at CNSA 2.0 parameters (ML-KEM-1024, ML-DSA-87 only). |
| **now** | ML-DSA-44 | `corpus/pqc/java/PqParamSpec.java` | Post-quantum, but not at CNSA 2.0 parameters (ML-KEM-1024, ML-DSA-87 only). |
| **now** | ML-KEM-768 | `corpus/pqc/python/pq_hybrid_kem.py` | Post-quantum, but not at CNSA 2.0 parameters (ML-KEM-1024, ML-DSA-87 only). |
| **now** | X25519 | `corpus/pqc/python/pq_hybrid_kem.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | ML-KEM-768 | `corpus/pqc/python/pq_kem.py` | Post-quantum, but not at CNSA 2.0 parameters (ML-KEM-1024, ML-DSA-87 only). |
| **now** | ML-DSA-65 | `corpus/pqc/python/pq_signature.py` | Post-quantum, but not at CNSA 2.0 parameters (ML-KEM-1024, ML-DSA-87 only). |
| **now** | ECC-P-256 | `corpus/pqc/python/pq_washing.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | AES-128-ECB | `corpus/tier1/c/t1_aes_ecb.c` | CNSA requires 256-bit AES keys. |
| **now** | ChaCha20-Poly1305 | `corpus/tier1/c/t1_chacha.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | DH-2048 | `corpus/tier1/c/t1_dh.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | MD5 | `corpus/tier1/c/t1_digests.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/tier1/c/t1_digests.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-256 | `corpus/tier1/c/t1_digests.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA3-256 | `corpus/tier1/c/t1_digests.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | ECC-P-256 | `corpus/tier1/c/t1_ec.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-SHA-256 | `corpus/tier1/c/t1_mac_kdf.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | Ed25519 | `corpus/tier1/c/t1_modern_curves.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | X25519 | `corpus/tier1/c/t1_modern_curves.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-1024 | `corpus/tier1/c/t1_rsa_legacy.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | 3DES-CBC | `corpus/tier1/c/t1_triple_des.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | AES-128-CBC | `corpus/tier1/go/aes_cbc/main.go` | CNSA requires 256-bit AES keys. |
| **now** | 3DES-CBC | `corpus/tier1/go/des/main.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | DES-CBC | `corpus/tier1/go/des/main.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | DSA-2048 | `corpus/tier1/go/dsa/main.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | ECC-P-256 | `corpus/tier1/go/ecdsa/main.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | Ed25519 | `corpus/tier1/go/ed25519/main.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | MD5 | `corpus/tier1/go/hashes/main.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/tier1/go/hashes/main.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-256 | `corpus/tier1/go/hashes/main.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA3-256 | `corpus/tier1/go/hashes/main.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-SHA-256 | `corpus/tier1/go/mac_kdf/main.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RC4 | `corpus/tier1/go/rc4/main.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-2048 | `corpus/tier1/go/rsa/main.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | X25519 | `corpus/tier1/go/x25519/main.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | AES-128-ECB | `corpus/tier1/java/T1AesEcb.java` | CNSA requires 256-bit AES keys. |
| **now** | DH-2048 | `corpus/tier1/java/T1Dh.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | DSA-2048 | `corpus/tier1/java/T1Dsa.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | ECC-P-256 | `corpus/tier1/java/T1Ecdsa.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | MD5 | `corpus/tier1/java/T1Hashes.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/tier1/java/T1Hashes.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-256 | `corpus/tier1/java/T1Hashes.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA3-256 | `corpus/tier1/java/T1Hashes.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | 3DES-CBC | `corpus/tier1/java/T1LegacyCiphers.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | DES-CBC | `corpus/tier1/java/T1LegacyCiphers.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-SHA-256 | `corpus/tier1/java/T1MacKdf.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | Ed25519 | `corpus/tier1/java/T1ModernCurves.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | X25519 | `corpus/tier1/java/T1ModernCurves.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | AES-128-CBC | `corpus/tier1/javascript/t1_aes_cbc.js` | CNSA requires 256-bit AES keys. |
| **now** | ChaCha20-Poly1305 | `corpus/tier1/javascript/t1_chacha.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | DH-2048 | `corpus/tier1/javascript/t1_dh.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | ECC-P-256 | `corpus/tier1/javascript/t1_ec.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | MD5 | `corpus/tier1/javascript/t1_hashes.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/tier1/javascript/t1_hashes.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-256 | `corpus/tier1/javascript/t1_hashes.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA3-256 | `corpus/tier1/javascript/t1_hashes.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-SHA-256 | `corpus/tier1/javascript/t1_mac_kdf.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | Ed25519 | `corpus/tier1/javascript/t1_modern_curves.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | X25519 | `corpus/tier1/javascript/t1_modern_curves.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-2048 | `corpus/tier1/javascript/t1_rsa.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | 3DES-CBC | `corpus/tier1/javascript/t1_triple_des.js` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/tier1/javascript/t1_webcrypto.mjs` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | AES-128-ECB | `corpus/tier1/python/t1_aes_ecb.py` | CNSA requires 256-bit AES keys. |
| **now** | ChaCha20-Poly1305 | `corpus/tier1/python/t1_chacha.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | DH-2048 | `corpus/tier1/python/t1_dh.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | DSA-2048 | `corpus/tier1/python/t1_dsa.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | ECC-P-256 | `corpus/tier1/python/t1_ecdsa.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | MD5 | `corpus/tier1/python/t1_hashes.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/tier1/python/t1_hashes.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-256 | `corpus/tier1/python/t1_hashes.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA3-256 | `corpus/tier1/python/t1_hashes.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-SHA-256 | `corpus/tier1/python/t1_mac_kdf.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | Ed25519 | `corpus/tier1/python/t1_modern_curves.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | X25519 | `corpus/tier1/python/t1_modern_curves.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-2048 | `corpus/tier1/python/t1_rsa.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | 3DES-CBC | `corpus/tier1/python/t1_triple_des.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | 3DES-ECB | `corpus/tier2/c/t2_cipher_struct.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | ECC-P-521 | `corpus/tier2/c/t2_curve_index.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/tier2/c/t2_digest_table.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | AES-192-CBC | `corpus/tier2/c/t2_fetch_by_name.c` | CNSA requires 256-bit AES keys. |
| **now** | HMAC-MD5 | `corpus/tier2/c/t2_func_ptr.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-1024 | `corpus/tier2/c/t2_macro_bits.c` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | 3DES-CBC | `corpus/tier2/go/block_factory/main.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/tier2/go/hash_enum/main.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-MD5 | `corpus/tier2/go/hmac_func_value/main.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-1024 | `corpus/tier2/go/key_bits/main.go` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | AES-192-CTR | `corpus/tier2/go/key_len/main.go` | CNSA requires 256-bit AES keys. |
| **now** | 3DES-CBC | `corpus/tier2/java/T2ConcatTransform.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | DSA-1024 | `corpus/tier2/java/T2DsaConstant.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/tier2/java/T2Enum.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-256 | `corpus/tier2/java/T2Enum.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-1024 | `corpus/tier2/java/T2PropertiesConfig.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | AES-128-ECB | `corpus/tier2/java/T2SysProp.java` | CNSA requires 256-bit AES keys. |
| **now** | MD5 | `corpus/tier2/java/T2Wrapper.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-1024 | `corpus/tier2/python/t2_alias_import.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | AES-128-CBC | `corpus/tier2/python/t2_config_cipher.py` | CNSA requires 256-bit AES keys. |
| **now** | SHA-1 | `corpus/tier2/python/t2_constant_hash.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | MD5 | `corpus/tier2/python/t2_dispatch_table.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-256 | `corpus/tier2/python/t2_dispatch_table.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/tier2/python/t2_env_default.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-SHA-1 | `corpus/tier2/python/t2_partial.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | AES-192-CBC | `corpus/tier2/python/t2_wrapper.py` | CNSA requires 256-bit AES keys. |
| **now** | 3DES-CBC | `corpus/tier2/typescript/t2_config_object.ts` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/tier2/typescript/t2_default_param.ts` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-1024 | `corpus/tier2/typescript/t2_env_default.ts` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-MD5 | `corpus/tier2/typescript/t2_hmac_const.ts` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | AES-128-ECB | `corpus/tier2/typescript/t2_wrapper.ts` | CNSA requires 256-bit AES keys. |
| **now** | RSA-1024 | `corpus/tier3/java/cross_class_constant/src/com/acme/keys/KeyIssuer.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | AES-128-GCM | `corpus/tier3/java/cross_class_constant/src/com/acme/session/SessionCrypto.java` | CNSA requires 256-bit AES keys. |
| **now** | SHA-1 | `corpus/tier3/java/cross_class_constant/src/com/acme/tokens/Fingerprint.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | MD5 | `corpus/tier3/java/dependency_injection/src/com/acme/audit/DigestProvider.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-SHA-256 | `corpus/tier3/java/jwt_alg_mapping/src/com/acme/jwt/JwtSigner.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | 3DES-CBC | `corpus/tier3/java/strategy_factory/src/com/acme/crypto/LegacyDesedeCipher.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-1024 | `corpus/tier3/python/cross_module_constant/keys/issuer.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | AES-128-GCM | `corpus/tier3/python/cross_module_constant/sessions/crypto.py` | CNSA requires 256-bit AES keys. |
| **now** | SHA-1 | `corpus/tier3/python/cross_module_constant/tokens/fingerprint.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | MD5 | `corpus/tier3/python/dependency_injection/wiring.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-SHA-256 | `corpus/tier3/python/jwt_alg_mapping/jwtlib/signer.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | ChaCha20-Poly1305 | `corpus/tier3/python/registry_strategy/suites/builtin.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-1024 | `corpus/tier3/python/wrapper_two_callers/services/billing.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-2048 | `corpus/tier4/assets/certs/api_gateway.pem` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-256 | `corpus/tier4/assets/certs/api_gateway.pem` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | Ed25519 | `corpus/tier4/assets/certs/device_ed25519.pem` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-1024 | `corpus/tier4/assets/certs/payments_legacy.crt` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/tier4/assets/certs/payments_legacy.crt` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-256 | `corpus/tier4/assets/certs/portal_fullchain.pem` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | ECC-P-256 | `corpus/tier4/assets/certs/telemetry_ecdsa.pem` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-256 | `corpus/tier4/assets/certs/telemetry_ecdsa.pem` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | ECC-P-256 | `corpus/tier4/assets/keys/jwks.json` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-2048 | `corpus/tier4/assets/keys/jwks.json` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | ECC-secp256k1 | `corpus/tier4/assets/keys/treasury_hot_wallet.key` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-2048 | `corpus/tier4/assets/keystores/orders_keystore.p12` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-256 | `corpus/tier4/assets/keystores/orders_keystore.p12` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-1024 | `corpus/tier4/assets/keystores/partner_truststore.jks` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/tier4/assets/keystores/partner_truststore.jks` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | Ed25519 | `corpus/tier4/assets/ssh/deploy_id_ed25519` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-2048 | `corpus/tier4/assets/ssh/ssh_host_rsa_key.pub` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | AES-128-CBC | `corpus/tier4/assets/ssh/sshd_config` | CNSA requires 256-bit AES keys. |
| **now** | ChaCha20-Poly1305 | `corpus/tier4/assets/ssh/sshd_config` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | DH-2048 | `corpus/tier4/assets/ssh/sshd_config` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-SHA-1 | `corpus/tier4/assets/ssh/sshd_config` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA | `corpus/tier4/assets/ssh/sshd_config` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | X25519 | `corpus/tier4/assets/ssh/sshd_config` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-1024 | `corpus/tier4/assets/tls/openssl.cnf` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/tier4/assets/tls/openssl.cnf` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | TEA | `corpus/tier5/java/T5BlockTransform.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-2048 | `corpus/tier5/java/T5HandrolledPubkey.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | MD5 | `corpus/tier5/java/T5Reflection.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | 3DES-CBC | `corpus/tier5/java/T5StringAssembly.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-2048 | `corpus/tier5/java/T5StringAssembly.java` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | AES-128-CBC | `corpus/tier5/java/compiled/billing-core.jar` | CNSA requires 256-bit AES keys. |
| **now** | RSA-1024 | `corpus/tier5/java/compiled/billing-core.jar` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/tier5/java/compiled/billing-core.jar` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | HMAC-MD5 | `corpus/tier5/python/compiled/ledger_sync.pyc` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/tier5/python/compiled/ledger_sync.pyc` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | AES-128-ECB | `corpus/tier5/python/t5_char_codes.py` | CNSA requires 256-bit AES keys. |
| **now** | RSA-2048 | `corpus/tier5/python/t5_dynamic_import.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-256 | `corpus/tier5/python/t5_handrolled_digest.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RC4 | `corpus/tier5/python/t5_handrolled_keystream.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | RSA-1024 | `corpus/tier5/python/t5_handrolled_pubkey.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | MD5 | `corpus/tier5/python/t5_string_assembly.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |
| **now** | SHA-1 | `corpus/tier5/python/t5_string_assembly.py` | Not a CNSA algorithm or strength (never CNSA 1.0 either). |

### Needs a human decision (1)

- `corpus/pqc/assets/tls/openssl_pq.cnf`: SecP384r1MLKEM1024: review. Both halves are CNSA-grade (ML-KEM-1024, P-384). Whether a hybrid is acceptable after the exclusive-use date is a program-office decision.

## EO 14412: federal high value assets and high impact systems

_Federal HVAs and high impact systems (not National Security Systems). Covered contractors face a Dec 31, 2030 FIPS/PQC compliance date under the FAR rule the order directs. Everything the order doesn't address falls back to the NIST policy._

| When | Findings | Quantum-vulnerable | Files |
|---|---|---|---|
| Due now (not approved or past its date) | 169 | 51 | 164 |
| Due by end of 2030 | 150 | 88 | 139 |
| Due 2031 to 2033 | 80 | 80 | 80 |
| Due 2034 to 2035 | 0 | 0 | 0 |
| No deadline (approved, review, out of scope, unknown) | 200 | 0 | 169 |

### Due now or by end of 2030 (319)

| Due | Algorithm | File | Why |
|---|---|---|---|
| **now** | ChaCha20-Poly1305 | `corpus/calibration/tier1/c/cal_chacha20poly1305_006.c` | Not FIPS-approved. Fine outside FIPS scope; a finding inside it. |
| **now** | ChaCha20-Poly1305 | `corpus/calibration/tier1/c/cal_chacha20poly1305_007.c` | Not FIPS-approved. Fine outside FIPS scope; a finding inside it. |
| **now** | ChaCha20-Poly1305 | `corpus/calibration/tier1/c/cal_chacha20poly1305_008.c` | Not FIPS-approved. Fine outside FIPS scope; a finding inside it. |
| **now** | MD5 | `corpus/calibration/tier1/c/cal_md5_021.c` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/calibration/tier1/c/cal_md5_022.c` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/calibration/tier1/c/cal_md5_023.c` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | DES-CBC | `corpus/calibration/tier1/go/cal_des_006/cal_des_006.go` | Single DES; FIPS 46-3 was withdrawn in 2005. |
| **now** | DES-CBC | `corpus/calibration/tier1/go/cal_des_007/cal_des_007.go` | Single DES; FIPS 46-3 was withdrawn in 2005. |
| **now** | DES-CBC | `corpus/calibration/tier1/go/cal_des_008/cal_des_008.go` | Single DES; FIPS 46-3 was withdrawn in 2005. |
| **now** | MD5 | `corpus/calibration/tier1/go/cal_md5_021/cal_md5_021.go` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/calibration/tier1/go/cal_md5_022/cal_md5_022.go` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/calibration/tier1/go/cal_md5_023/cal_md5_023.go` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | RC4 | `corpus/calibration/tier1/go/cal_rc4_027/cal_rc4_027.go` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | RC4 | `corpus/calibration/tier1/go/cal_rc4_028/cal_rc4_028.go` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | RC4 | `corpus/calibration/tier1/go/cal_rc4_029/cal_rc4_029.go` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/calibration/tier1/java/Cal1022LedgerDefaults.java` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/calibration/tier1/java/Cal1023AuditProfile.java` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/calibration/tier1/java/Cal1024PolicyDefaults.java` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | ChaCha20-Poly1305 | `corpus/calibration/tier1/javascript/cal_chacha20poly1305_006.js` | Not FIPS-approved. Fine outside FIPS scope; a finding inside it. |
| **now** | ChaCha20-Poly1305 | `corpus/calibration/tier1/javascript/cal_chacha20poly1305_007.js` | Not FIPS-approved. Fine outside FIPS scope; a finding inside it. |
| **now** | ChaCha20-Poly1305 | `corpus/calibration/tier1/javascript/cal_chacha20poly1305_008.js` | Not FIPS-approved. Fine outside FIPS scope; a finding inside it. |
| **now** | MD5 | `corpus/calibration/tier1/javascript/cal_md5_021.js` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/calibration/tier1/javascript/cal_md5_022.js` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/calibration/tier1/javascript/cal_md5_023.js` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | ChaCha20-Poly1305 | `corpus/calibration/tier1/python/cal_chacha20poly1305_006.py` | Not FIPS-approved. Fine outside FIPS scope; a finding inside it. |
| **now** | ChaCha20-Poly1305 | `corpus/calibration/tier1/python/cal_chacha20poly1305_007.py` | Not FIPS-approved. Fine outside FIPS scope; a finding inside it. |
| **now** | ChaCha20-Poly1305 | `corpus/calibration/tier1/python/cal_chacha20poly1305_008.py` | Not FIPS-approved. Fine outside FIPS scope; a finding inside it. |
| **now** | MD5 | `corpus/calibration/tier1/python/cal_md5_024.py` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/calibration/tier1/python/cal_md5_025.py` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/calibration/tier1/python/cal_md5_026.py` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | HMAC-MD5 | `corpus/calibration/tier2/c/cal_hmac_010.c` | MD5 is not an approved hash function, in HMAC or otherwise. |
| **now** | HMAC-MD5 | `corpus/calibration/tier2/c/cal_hmac_011.c` | MD5 is not an approved hash function, in HMAC or otherwise. |
| **now** | HMAC-MD5 | `corpus/calibration/tier2/c/cal_hmac_012.c` | MD5 is not an approved hash function, in HMAC or otherwise. |
| **now** | HMAC-MD5 | `corpus/calibration/tier2/go/cal_hmac_010/cal_hmac_010.go` | MD5 is not an approved hash function, in HMAC or otherwise. |
| **now** | HMAC-MD5 | `corpus/calibration/tier2/go/cal_hmac_011/cal_hmac_011.go` | MD5 is not an approved hash function, in HMAC or otherwise. |
| **now** | HMAC-MD5 | `corpus/calibration/tier2/go/cal_hmac_012/cal_hmac_012.go` | MD5 is not an approved hash function, in HMAC or otherwise. |
| **now** | MD5 | `corpus/calibration/tier2/java/Cal2013TenantOptions.java` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/calibration/tier2/java/Cal2014DeviceDefaults.java` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/calibration/tier2/java/Cal2015UploadSettings.java` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/calibration/tier2/python/cal_md5_009.py` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/calibration/tier2/python/cal_md5_010.py` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/calibration/tier2/python/cal_md5_011.py` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | HMAC-MD5 | `corpus/calibration/tier2/typescript/cal_hmac_009.ts` | MD5 is not an approved hash function, in HMAC or otherwise. |
| **now** | HMAC-MD5 | `corpus/calibration/tier2/typescript/cal_hmac_010.ts` | MD5 is not an approved hash function, in HMAC or otherwise. |
| **now** | HMAC-MD5 | `corpus/calibration/tier2/typescript/cal_hmac_011.ts` | MD5 is not an approved hash function, in HMAC or otherwise. |
| **now** | HMAC-MD5 | `corpus/mixed/c/device_daemon.c` | MD5 is not an approved hash function, in HMAC or otherwise. |
| **now** | RC4 | `corpus/mixed/go/invoice_gateway/main.go` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | DES-CBC | `corpus/mixed/go/report_gateway/main.go` | Single DES; FIPS 46-3 was withdrawn in 2005. |
| **now** | ChaCha20-Poly1305 | `corpus/mixed/java/OrderDefaultsModule.java` | Not FIPS-approved. Fine outside FIPS scope; a finding inside it. |
| **now** | ChaCha20-Poly1305 | `corpus/mixed/python/invoice_service.py` | Not FIPS-approved. Fine outside FIPS scope; a finding inside it. |
| **now** | ChaCha20-Poly1305 | `corpus/pqc/assets/ssh/sshd_config_pq` | Not FIPS-approved. Fine outside FIPS scope; a finding inside it. |
| **now** | ChaCha20-Poly1305 | `corpus/tier1/c/t1_chacha.c` | Not FIPS-approved. Fine outside FIPS scope; a finding inside it. |
| **now** | MD5 | `corpus/tier1/c/t1_digests.c` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | TLS_RSA_WITH_3DES_EDE_CBC_SHA | `corpus/tier1/c/t1_tls_ctx.c` | Cipher suite uses a disallowed bulk cipher. |
| **now** | DES-CBC | `corpus/tier1/go/des/main.go` | Single DES; FIPS 46-3 was withdrawn in 2005. |
| **now** | MD5 | `corpus/tier1/go/hashes/main.go` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | RC4 | `corpus/tier1/go/rc4/main.go` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | TLS_RSA_WITH_3DES_EDE_CBC_SHA | `corpus/tier1/go/tls_config/main.go` | Cipher suite uses a disallowed bulk cipher. |
| **now** | MD5 | `corpus/tier1/java/T1Hashes.java` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | DES-CBC | `corpus/tier1/java/T1LegacyCiphers.java` | Single DES; FIPS 46-3 was withdrawn in 2005. |
| **now** | ChaCha20-Poly1305 | `corpus/tier1/javascript/t1_chacha.js` | Not FIPS-approved. Fine outside FIPS scope; a finding inside it. |
| **now** | MD5 | `corpus/tier1/javascript/t1_hashes.js` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | ChaCha20-Poly1305 | `corpus/tier1/python/t1_chacha.py` | Not FIPS-approved. Fine outside FIPS scope; a finding inside it. |
| **now** | MD5 | `corpus/tier1/python/t1_hashes.py` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | HMAC-MD5 | `corpus/tier2/c/t2_func_ptr.c` | MD5 is not an approved hash function, in HMAC or otherwise. |
| **now** | HMAC-MD5 | `corpus/tier2/go/hmac_func_value/main.go` | MD5 is not an approved hash function, in HMAC or otherwise. |
| **now** | MD5 | `corpus/tier2/java/T2Wrapper.java` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/tier2/python/t2_dispatch_table.py` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | HMAC-MD5 | `corpus/tier2/typescript/t2_hmac_const.ts` | MD5 is not an approved hash function, in HMAC or otherwise. |
| **now** | MD5 | `corpus/tier3/java/dependency_injection/src/com/acme/audit/DigestProvider.java` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/tier3/python/dependency_injection/wiring.py` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | ChaCha20-Poly1305 | `corpus/tier3/python/registry_strategy/suites/builtin.py` | Not FIPS-approved. Fine outside FIPS scope; a finding inside it. |
| **now** | ChaCha20-Poly1305 | `corpus/tier4/assets/ssh/sshd_config` | Not FIPS-approved. Fine outside FIPS scope; a finding inside it. |
| **now** | TLS_RSA_WITH_3DES_EDE_CBC_SHA | `corpus/tier4/assets/tls/nginx.conf` | Cipher suite uses a disallowed bulk cipher. |
| **now** | TEA | `corpus/tier5/java/T5BlockTransform.java` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/tier5/java/T5Reflection.java` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | HMAC-MD5 | `corpus/tier5/python/compiled/ledger_sync.pyc` | MD5 is not an approved hash function, in HMAC or otherwise. |
| **now** | RC4 | `corpus/tier5/python/t5_handrolled_keystream.py` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | MD5 | `corpus/tier5/python/t5_string_assembly.py` | Not a NIST-approved algorithm, and broken or weak in its own right. |
| **now** | RSA-1024 | `corpus/calibration/tier1/c/cal_rsa_027.c` | Below 112-bit security; disallowed since 2014. |
| **now** | DSA-1024 | `corpus/calibration/tier1/go/cal_dsa_009/cal_dsa_009.go` | Below 112-bit security; disallowed since 2014. |
| **now** | DSA-1024 | `corpus/calibration/tier1/go/cal_dsa_011/cal_dsa_011.go` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/calibration/tier1/go/cal_rsa_030/cal_rsa_030.go` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/calibration/tier1/go/cal_rsa_031/cal_rsa_031.go` | Below 112-bit security; disallowed since 2014. |
| **now** | DSA-1024 | `corpus/calibration/tier1/java/Cal1010DeviceConfig.java` | Below 112-bit security; disallowed since 2014. |
| **now** | DSA-1024 | `corpus/calibration/tier1/java/Cal1011AuditSettings.java` | Below 112-bit security; disallowed since 2014. |
| **now** | DSA-1024 | `corpus/calibration/tier1/java/Cal1012MemberOptions.java` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/calibration/tier1/javascript/cal_rsa_028.js` | Below 112-bit security; disallowed since 2014. |
| **now** | DH-1024 | `corpus/calibration/tier1/python/cal_dh_009.py` | Below 112-bit security; disallowed since 2014. |
| **now** | DH-1024 | `corpus/calibration/tier1/python/cal_dh_010.py` | Below 112-bit security; disallowed since 2014. |
| **now** | DH-512 | `corpus/calibration/tier1/python/cal_dh_011.py` | Below 112-bit security; disallowed since 2014. |
| **now** | DSA-1024 | `corpus/calibration/tier1/python/cal_dsa_012.py` | Below 112-bit security; disallowed since 2014. |
| **now** | DSA-1024 | `corpus/calibration/tier1/python/cal_dsa_013.py` | Below 112-bit security; disallowed since 2014. |
| **now** | DSA-1024 | `corpus/calibration/tier1/python/cal_dsa_014.py` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/calibration/tier1/python/cal_rsa_031.py` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/calibration/tier2/c/cal_rsa_014.c` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/calibration/tier2/c/cal_rsa_015.c` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/calibration/tier2/go/cal_rsa_013/cal_rsa_013.go` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/calibration/tier2/go/cal_rsa_014/cal_rsa_014.go` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/calibration/tier2/go/cal_rsa_015/cal_rsa_015.go` | Below 112-bit security; disallowed since 2014. |
| **now** | DSA-1024 | `corpus/calibration/tier2/java/Cal2008PayloadOptions.java` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/calibration/tier2/python/cal_rsa_014.py` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/calibration/tier2/typescript/cal_rsa_013.ts` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/calibration/tier2/typescript/cal_rsa_014.ts` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/mixed/go/payload_worker/main.go` | Below 112-bit security; disallowed since 2014. |
| **now** | DH-512 | `corpus/mixed/python/invoice_service.py` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/tier1/c/t1_rsa_legacy.c` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/tier2/c/t2_macro_bits.c` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/tier2/go/key_bits/main.go` | Below 112-bit security; disallowed since 2014. |
| **now** | DSA-1024 | `corpus/tier2/java/T2DsaConstant.java` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/tier2/java/T2PropertiesConfig.java` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/tier2/python/t2_alias_import.py` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/tier2/typescript/t2_env_default.ts` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/tier3/java/cross_class_constant/src/com/acme/keys/KeyIssuer.java` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/tier3/python/cross_module_constant/keys/issuer.py` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/tier3/python/wrapper_two_callers/services/billing.py` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/tier4/assets/certs/payments_legacy.crt` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/tier4/assets/keystores/partner_truststore.jks` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/tier4/assets/tls/openssl.cnf` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/tier5/java/compiled/billing-core.jar` | Below 112-bit security; disallowed since 2014. |
| **now** | RSA-1024 | `corpus/tier5/python/t5_handrolled_pubkey.py` | Below 112-bit security; disallowed since 2014. |
| **now** | DSA-2048 | `corpus/calibration/tier1/go/cal_dsa_010/cal_dsa_010.go` | DSA signature generation removed by FIPS 186-5; verification of legacy signatures only. |
| **now** | DSA-2048 | `corpus/calibration/tier2/java/Cal2007PayloadDefaults.java` | DSA signature generation removed by FIPS 186-5; verification of legacy signatures only. |
| **now** | DSA-2048 | `corpus/calibration/tier2/java/Cal2009ProfileProfile.java` | DSA signature generation removed by FIPS 186-5; verification of legacy signatures only. |
| **now** | DSA-2048 | `corpus/tier1/go/dsa/main.go` | DSA signature generation removed by FIPS 186-5; verification of legacy signatures only. |
| **now** | DSA-2048 | `corpus/tier1/java/T1Dsa.java` | DSA signature generation removed by FIPS 186-5; verification of legacy signatures only. |
| **now** | DSA-2048 | `corpus/tier1/python/t1_dsa.py` | DSA signature generation removed by FIPS 186-5; verification of legacy signatures only. |
| **now** | 3DES-CBC | `corpus/calibration/tier1/c/cal_3des_001.c` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier1/c/cal_3des_002.c` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier1/c/cal_3des_003.c` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier1/go/cal_3des_001/cal_3des_001.go` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier1/go/cal_3des_002/cal_3des_002.go` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier1/go/cal_3des_003/cal_3des_003.go` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier1/java/Cal1001InvoiceConfig.java` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier1/java/Cal1002ClaimOptions.java` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier1/java/Cal1003SessionProfile.java` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier1/javascript/cal_3des_001.js` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier1/javascript/cal_3des_002.js` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier1/javascript/cal_3des_003.js` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier1/python/cal_3des_001.py` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier1/python/cal_3des_002.py` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier1/python/cal_3des_003.py` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-ECB | `corpus/calibration/tier2/c/cal_3des_001.c` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-ECB | `corpus/calibration/tier2/c/cal_3des_002.c` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-ECB | `corpus/calibration/tier2/c/cal_3des_003.c` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier2/go/cal_3des_001/cal_3des_001.go` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier2/go/cal_3des_002/cal_3des_002.go` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier2/go/cal_3des_003/cal_3des_003.go` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier2/java/Cal2001UploadConfig.java` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier2/java/Cal2002VoucherDefaults.java` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier2/java/Cal2003VoucherConfig.java` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier2/typescript/cal_3des_001.ts` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier2/typescript/cal_3des_002.ts` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/calibration/tier2/typescript/cal_3des_003.ts` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/mixed/c/audit_daemon.c` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-ECB | `corpus/mixed/c/policy_agent.c` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/mixed/go/report_gateway/main.go` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-ECB | `corpus/mixed/java/OrderDefaultsModule.java` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/tier1/c/t1_triple_des.c` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/tier1/go/des/main.go` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/tier1/java/T1LegacyCiphers.java` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/tier1/javascript/t1_triple_des.js` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/tier1/python/t1_triple_des.py` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-ECB | `corpus/tier2/c/t2_cipher_struct.c` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/tier2/go/block_factory/main.go` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/tier2/java/T2ConcatTransform.java` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/tier2/typescript/t2_config_object.ts` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/tier3/java/strategy_factory/src/com/acme/crypto/LegacyDesedeCipher.java` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| **now** | 3DES-CBC | `corpus/tier5/java/T5StringAssembly.java` | TDEA encryption disallowed after 2023; decryption of legacy data only. |
| 2030-12-31 | DH-2048 | `corpus/calibration/tier1/c/cal_dh_009.c` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | DH-2048 | `corpus/calibration/tier1/c/cal_dh_010.c` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | DH-3072 | `corpus/calibration/tier1/c/cal_dh_011.c` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | PBKDF2-HMAC-SHA-1 | `corpus/calibration/tier1/c/cal_pbkdf2_024.c` | All SHA-1 uses end Dec 31, 2030. |
| 2030-12-31 | PBKDF2-HMAC-SHA-1 | `corpus/calibration/tier1/c/cal_pbkdf2_025.c` | All SHA-1 uses end Dec 31, 2030. |
| 2030-12-31 | PBKDF2-HMAC-SHA-1 | `corpus/calibration/tier1/c/cal_pbkdf2_026.c` | All SHA-1 uses end Dec 31, 2030. |
| 2030-12-31 | RSA-2048 | `corpus/calibration/tier1/c/cal_rsa_028.c` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier1/c/cal_sha1_029.c` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier1/c/cal_sha1_030.c` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier1/c/cal_sha1_031.c` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | X25519 | `corpus/calibration/tier1/c/cal_x25519_038.c` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | X25519 | `corpus/calibration/tier1/c/cal_x25519_039.c` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | X25519 | `corpus/calibration/tier1/c/cal_x25519_040.c` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | RSA-2048 | `corpus/calibration/tier1/go/cal_rsa_032/cal_rsa_032.go` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier1/go/cal_sha1_033/cal_sha1_033.go` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier1/go/cal_sha1_034/cal_sha1_034.go` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier1/go/cal_sha1_035/cal_sha1_035.go` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | X25519 | `corpus/calibration/tier1/go/cal_x25519_042/cal_x25519_042.go` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | X25519 | `corpus/calibration/tier1/go/cal_x25519_043/cal_x25519_043.go` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | X25519 | `corpus/calibration/tier1/go/cal_x25519_044/cal_x25519_044.go` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | DH-3072 | `corpus/calibration/tier1/java/Cal1007AccountDefaults.java` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | DH-3072 | `corpus/calibration/tier1/java/Cal1008BookingSettings.java` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | DH-2048 | `corpus/calibration/tier1/java/Cal1009ClaimConfig.java` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | RSA-3072 | `corpus/calibration/tier1/java/Cal1028MetricSettings.java` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | RSA-3072 | `corpus/calibration/tier1/java/Cal1029MetricOptions.java` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | RSA-2048 | `corpus/calibration/tier1/java/Cal1030DeviceOptions.java` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier1/java/Cal1031ReceiptOptions.java` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier1/java/Cal1032BookingConfig.java` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier1/java/Cal1033BillingConfig.java` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | X25519 | `corpus/calibration/tier1/java/Cal1040ProfileSettings.java` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | X25519 | `corpus/calibration/tier1/java/Cal1041OrderSettings.java` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | X25519 | `corpus/calibration/tier1/java/Cal1042AccountProfile.java` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | DH-3072 | `corpus/calibration/tier1/javascript/cal_dh_009.js` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | DH-2048 | `corpus/calibration/tier1/javascript/cal_dh_010.js` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | DH-3072 | `corpus/calibration/tier1/javascript/cal_dh_011.js` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | RSA-2048 | `corpus/calibration/tier1/javascript/cal_rsa_027.js` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier1/javascript/cal_sha1_029.js` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier1/javascript/cal_sha1_030.js` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | X25519 | `corpus/calibration/tier1/javascript/cal_x25519_037.js` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | X25519 | `corpus/calibration/tier1/javascript/cal_x25519_038.js` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | X25519 | `corpus/calibration/tier1/javascript/cal_x25519_039.js` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | HMAC-SHA-1 | `corpus/calibration/tier1/python/cal_hmac_022.py` | All SHA-1 uses end Dec 31, 2030. |
| 2030-12-31 | RSA-3072 | `corpus/calibration/tier1/python/cal_rsa_030.py` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | RSA-2048 | `corpus/calibration/tier1/python/cal_rsa_032.py` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier1/python/cal_sha1_033.py` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier1/python/cal_sha1_034.py` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier1/python/cal_sha1_035.py` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | X25519 | `corpus/calibration/tier1/python/cal_x25519_042.py` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | X25519 | `corpus/calibration/tier1/python/cal_x25519_043.py` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | X25519 | `corpus/calibration/tier1/python/cal_x25519_044.py` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | RSA-2048 | `corpus/calibration/tier2/c/cal_rsa_013.c` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier2/c/cal_sha1_016.c` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier2/c/cal_sha1_017.c` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier2/c/cal_sha1_018.c` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier2/go/cal_sha1_016/cal_sha1_016.go` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier2/go/cal_sha1_017/cal_sha1_017.go` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier2/go/cal_sha1_018/cal_sha1_018.go` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | RSA-2048 | `corpus/calibration/tier2/java/Cal2016RecordConfig.java` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | RSA-2048 | `corpus/calibration/tier2/java/Cal2017ReportSettings.java` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | RSA-2048 | `corpus/calibration/tier2/java/Cal2018ReceiptProfile.java` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier2/java/Cal2019ClaimDefaults.java` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier2/java/Cal2020TenantDefaults.java` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier2/java/Cal2021ReportOptions.java` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | HMAC-SHA-1 | `corpus/calibration/tier2/python/cal_hmac_006.py` | All SHA-1 uses end Dec 31, 2030. |
| 2030-12-31 | HMAC-SHA-1 | `corpus/calibration/tier2/python/cal_hmac_007.py` | All SHA-1 uses end Dec 31, 2030. |
| 2030-12-31 | HMAC-SHA-1 | `corpus/calibration/tier2/python/cal_hmac_008.py` | All SHA-1 uses end Dec 31, 2030. |
| 2030-12-31 | RSA-2048 | `corpus/calibration/tier2/python/cal_rsa_012.py` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | RSA-3072 | `corpus/calibration/tier2/python/cal_rsa_013.py` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier2/python/cal_sha1_015.py` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier2/python/cal_sha1_016.py` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | RSA-2048 | `corpus/calibration/tier2/typescript/cal_rsa_012.ts` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier2/typescript/cal_sha1_015.ts` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier2/typescript/cal_sha1_016.ts` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/calibration/tier2/typescript/cal_sha1_017.ts` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | RSA-2048 | `corpus/custom/example_envelope/envelope/wrap_transport.py` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | DH-3072 | `corpus/mixed/c/audit_daemon.c` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | SHA-1 | `corpus/mixed/c/device_daemon.c` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | X25519 | `corpus/mixed/c/device_daemon.c` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | HMAC-SHA-1 | `corpus/mixed/go/invoice_gateway/main.go` | All SHA-1 uses end Dec 31, 2030. |
| 2030-12-31 | RSA-2048 | `corpus/mixed/go/invoice_gateway/main.go` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | DH-3072 | `corpus/mixed/java/VoucherProfileModule.java` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | SHA-1 | `corpus/mixed/java/VoucherProfileModule.java` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/mixed/python/order_jobs.py` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | RSA-2048 | `corpus/mixed/typescript/voucher_service.ts` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | RSA | `corpus/pqc/assets/certs/migrated_leaf.pem` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | X25519 | `corpus/pqc/assets/ssh/sshd_config_pq` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | X25519 | `corpus/pqc/assets/tls/nginx_pq.conf` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | X25519 | `corpus/pqc/assets/tls/nginx_pq_washing.conf` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | X25519 | `corpus/pqc/go/tls_hybrid/main.go` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | X25519 | `corpus/pqc/python/pq_hybrid_kem.py` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | DH-2048 | `corpus/tier1/c/t1_dh.c` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | SHA-1 | `corpus/tier1/c/t1_digests.c` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | PBKDF2-HMAC-SHA-1 | `corpus/tier1/c/t1_mac_kdf.c` | All SHA-1 uses end Dec 31, 2030. |
| 2030-12-31 | X25519 | `corpus/tier1/c/t1_modern_curves.c` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | RSA-3072 | `corpus/tier1/c/t1_rsa_evp.c` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 | `corpus/tier1/c/t1_tls_ctx.c` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | TLS_RSA_WITH_AES_128_CBC_SHA | `corpus/tier1/c/t1_tls_ctx.c` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | SHA-1 | `corpus/tier1/go/hashes/main.go` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | RSA-2048 | `corpus/tier1/go/rsa/main.go` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 | `corpus/tier1/go/tls_config/main.go` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | TLS_RSA_WITH_AES_128_CBC_SHA | `corpus/tier1/go/tls_config/main.go` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | X25519 | `corpus/tier1/go/x25519/main.go` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | DH-2048 | `corpus/tier1/java/T1Dh.java` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | SHA-1 | `corpus/tier1/java/T1Hashes.java` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | X25519 | `corpus/tier1/java/T1ModernCurves.java` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | RSA-3072 | `corpus/tier1/java/T1Rsa.java` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | DH-2048 | `corpus/tier1/javascript/t1_dh.js` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | SHA-1 | `corpus/tier1/javascript/t1_hashes.js` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | X25519 | `corpus/tier1/javascript/t1_modern_curves.js` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | RSA-2048 | `corpus/tier1/javascript/t1_rsa.js` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | RSA-3072 | `corpus/tier1/javascript/t1_webcrypto.mjs` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | SHA-1 | `corpus/tier1/javascript/t1_webcrypto.mjs` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | DH-2048 | `corpus/tier1/python/t1_dh.py` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | SHA-1 | `corpus/tier1/python/t1_hashes.py` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | X25519 | `corpus/tier1/python/t1_modern_curves.py` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | RSA-2048 | `corpus/tier1/python/t1_rsa.py` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | SHA-1 | `corpus/tier2/c/t2_digest_table.c` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/tier2/go/hash_enum/main.go` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/tier2/java/T2Enum.java` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/tier2/python/t2_constant_hash.py` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/tier2/python/t2_env_default.py` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | HMAC-SHA-1 | `corpus/tier2/python/t2_partial.py` | All SHA-1 uses end Dec 31, 2030. |
| 2030-12-31 | SHA-1 | `corpus/tier2/typescript/t2_default_param.ts` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/tier3/java/cross_class_constant/src/com/acme/tokens/Fingerprint.java` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/tier3/python/cross_module_constant/tokens/fingerprint.py` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | RSA-3072 | `corpus/tier3/python/wrapper_two_callers/services/identity.py` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | RSA-2048 | `corpus/tier4/assets/certs/api_gateway.pem` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | RSA-4096 | `corpus/tier4/assets/certs/mainframe_gateway.der` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | SHA-1 | `corpus/tier4/assets/certs/payments_legacy.crt` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | RSA-3072 | `corpus/tier4/assets/certs/portal_fullchain.pem` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | RSA-3072 | `corpus/tier4/assets/keys/billing_service.pem` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | RSA-2048 | `corpus/tier4/assets/keys/jwks.json` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | RSA-2048 | `corpus/tier4/assets/keystores/orders_keystore.p12` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | SHA-1 | `corpus/tier4/assets/keystores/partner_truststore.jks` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | RSA-2048 | `corpus/tier4/assets/ssh/ssh_host_rsa_key.pub` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | DH-2048 | `corpus/tier4/assets/ssh/sshd_config` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | HMAC-SHA-1 | `corpus/tier4/assets/ssh/sshd_config` | All SHA-1 uses end Dec 31, 2030. |
| 2030-12-31 | RSA | `corpus/tier4/assets/ssh/sshd_config` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | X25519 | `corpus/tier4/assets/ssh/sshd_config` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 | `corpus/tier4/assets/tls/application.yml` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | TLS_RSA_WITH_AES_128_CBC_SHA | `corpus/tier4/assets/tls/application.yml` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 | `corpus/tier4/assets/tls/nginx.conf` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | TLS_RSA_WITH_AES_256_CBC_SHA | `corpus/tier4/assets/tls/nginx.conf` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | SHA-1 | `corpus/tier4/assets/tls/openssl.cnf` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | RSA-2048 | `corpus/tier5/java/T5HandrolledPubkey.java` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | RSA-2048 | `corpus/tier5/java/T5StringAssembly.java` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | SHA-1 | `corpus/tier5/java/compiled/billing-core.jar` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | SHA-1 | `corpus/tier5/python/compiled/ledger_sync.pyc` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |
| 2030-12-31 | RSA-2048 | `corpus/tier5/python/t5_dynamic_import.py` | Sec. 4(b)(ii): transition key establishment to PQC by Dec 31, 2030. RSA and EC keys of unknown use are dated by the earlier deadline. |
| 2030-12-31 | SHA-1 | `corpus/tier5/python/t5_string_assembly.py` | All SHA-1 uses end Dec 31, 2030. Already disallowed for digital signature generation. |

### Needs a human decision (6)

- `corpus/tier1/c/t1_tls_ctx.c`: TLS-1.0: review. TLS 1.2 is required. Government-only servers shall not use TLS 1.0 and should not use 1.1; citizen- or business-facing servers may still enable them for interoperability. Agencies must support TLS 1.3 since Jan 1, 2024.
- `corpus/tier1/go/tls_config/main.go`: TLS-1.0: review. TLS 1.2 is required. Government-only servers shall not use TLS 1.0 and should not use 1.1; citizen- or business-facing servers may still enable them for interoperability. Agencies must support TLS 1.3 since Jan 1, 2024.
- `corpus/tier4/assets/tls/application.yml`: TLS-1.1: review. TLS 1.2 is required. Government-only servers shall not use TLS 1.0 and should not use 1.1; citizen- or business-facing servers may still enable them for interoperability. Agencies must support TLS 1.3 since Jan 1, 2024.
- `corpus/tier4/assets/tls/nginx.conf`: TLS-1.0: review. TLS 1.2 is required. Government-only servers shall not use TLS 1.0 and should not use 1.1; citizen- or business-facing servers may still enable them for interoperability. Agencies must support TLS 1.3 since Jan 1, 2024.
- `corpus/tier4/assets/tls/nginx.conf`: TLS-1.1: review. TLS 1.2 is required. Government-only servers shall not use TLS 1.0 and should not use 1.1; citizen- or business-facing servers may still enable them for interoperability. Agencies must support TLS 1.3 since Jan 1, 2024.
- `corpus/tier4/assets/tls/openssl.cnf`: TLS-1.0: review. TLS 1.2 is required. Government-only servers shall not use TLS 1.0 and should not use 1.1; citizen- or business-facing servers may still enable them for interoperability. Agencies must support TLS 1.3 since Jan 1, 2024.

## Sources

- **IR8547**: NIST IR 8547, Transition to Post-Quantum Cryptography Standards. Final. (https://csrc.nist.gov/pubs/ir/8547/final)
- **SP800-131A**: NIST SP 800-131A Rev. 2, Transitioning the Use of Cryptographic Algorithms and Key Lengths. Final. (https://csrc.nist.gov/pubs/sp/800/131/a/r2/final)
- **SP800-131A-R3-IPD**: NIST SP 800-131A Rev. 3, initial public draft. Draft. (https://csrc.nist.gov/pubs/sp/800/131/a/r3/ipd)
- **SHA1-2030**: NIST, NIST Retires SHA-1 Cryptographic Algorithm (announcement). Final. (https://csrc.nist.gov/News/2022/nist-transitioning-away-from-sha-1-for-all-apps)
- **FIPS186-5**: FIPS 186-5, Digital Signature Standard (DSS). Final. (https://csrc.nist.gov/pubs/fips/186-5/final)
- **SP800-186**: NIST SP 800-186, Recommendations for Discrete Logarithm-based Cryptography: Elliptic Curve Domain Parameters. Final. (https://csrc.nist.gov/pubs/sp/800/186/final)
- **SP800-52**: NIST SP 800-52 Rev. 2, Guidelines for the Selection, Configuration, and Use of TLS Implementations. Final. (https://csrc.nist.gov/pubs/sp/800/52/r2/final)
- **SP800-227**: NIST SP 800-227, Recommendations for Key-Encapsulation Mechanisms. Final. (https://csrc.nist.gov/pubs/sp/800/227/final)
- **SP800-132**: NIST SP 800-132, Recommendation for Password-Based Key Derivation: Part 1: Storage Applications. Final. (https://csrc.nist.gov/pubs/sp/800/132/final)
- **FIPS46-3**: FIPS 46-3, Data Encryption Standard (DES), withdrawn 2005-05-19. Final. (https://csrc.nist.gov/pubs/fips/46-3/final)
- **CNSA2-FAQ**: NSA, The Commercial National Security Algorithm Suite 2.0 and Quantum Computing FAQ. Final. (https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/1/CSI_CNSA_2.0_FAQ_.PDF)
- **EO14412**: Executive Order 14412, Securing the Nation Against Advanced Cryptographic Attacks (signed June 22, 2026). Final. (https://www.whitehouse.gov/wp-content/uploads/2026/06/eo-14412.pdf)

_Policy rules live in `policies/*.json`. When a standard changes, edit the rule there; nothing else needs to change._
