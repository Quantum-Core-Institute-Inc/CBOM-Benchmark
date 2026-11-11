#!/usr/bin/env python3
"""Normalizer regression tests. Run: python tools/test_normalize.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cbomlib import normalize  # noqa: E402

CASES = [
    # (scanner name, algorithmProperties, expected family, expected params subset)
    ("SHA1withRSA", {}, "RSA", {"hash": "SHA-1"}),
    ("SHA256withECDSA", {}, "EC", {"hash": "SHA-256"}),
    ("SHA256withDSA", {}, "DSA", {"hash": "SHA-256"}),
    ("RSA-2048", {}, "RSA", {"key_size": 2048}),
    ("RSA", {"parameterSetIdentifier": "3072"}, "RSA", {"key_size": 3072}),
    ("RSASSA-PSS", {}, "RSA", {}),
    ("AES/ECB/PKCS5Padding", {}, "AES", {"mode": "ECB"}),
    ("AES-256-GCM", {}, "AES", {"key_size": 256, "mode": "GCM"}),
    ("AES128-CBC", {}, "AES", {"key_size": 128, "mode": "CBC"}),
    ("AES", {"parameterSetIdentifier": "192", "mode": "cbc"}, "AES", {"key_size": 192, "mode": "CBC"}),
    ("AESGCM", {}, "AES", {"mode": "GCM"}),
    ("DESede/CBC/PKCS5Padding", {}, "3DES", {"mode": "CBC"}),
    ("TripleDES", {}, "3DES", {}),
    ("3DES-CBC", {}, "3DES", {"mode": "CBC"}),
    ("DES/CBC/PKCS5Padding", {}, "DES", {"mode": "CBC"}),
    ("HmacSHA256", {}, "HMAC", {"hash": "SHA-256"}),
    ("HMAC-SHA1", {}, "HMAC", {"hash": "SHA-1"}),
    ("PBKDF2WithHmacSHA256", {}, "PBKDF2", {"hash": "SHA-256"}),
    ("PBKDF2-HMAC-SHA256", {}, "PBKDF2", {"hash": "SHA-256"}),
    ("ECDSA-P256", {}, "EC", {"curve": "P-256"}),
    ("ECC-P-384", {}, "EC", {"curve": "P-384"}),
    ("EC", {"curve": "secp256r1"}, "EC", {"curve": "P-256"}),
    ("secp384r1", {}, "EC", {"curve": "P-384"}),
    ("ECDH", {}, "EC", {}),
    ("Ed25519", {}, "Ed25519", {}),
    ("X25519", {}, "X25519", {}),
    ("ChaCha20-Poly1305", {}, "ChaCha20-Poly1305", {}),
    ("DH", {"parameterSetIdentifier": "2048"}, "DH", {"key_size": 2048}),
    ("DH-2048", {}, "DH", {"key_size": 2048}),
    ("SHA-1", {}, "SHA-1", {}),
    ("SHA1", {}, "SHA-1", {}),
    ("sha1", {}, "SHA-1", {}),
    ("SHA", {}, "SHA-1", {}),
    ("SHA-256", {}, "SHA-256", {}),
    ("sha3_256", {}, "SHA3-256", {}),
    ("SHA3-256", {}, "SHA3-256", {}),
    ("MD5", {}, "MD5", {}),
    ("ML-DSA-65", {}, "ML-DSA", {}),
    ("X25519MLKEM768", {}, "X25519MLKEM768", {}),
    ("DSA", {"parameterSetIdentifier": "1024"}, "DSA", {"key_size": 1024}),
    # JWS 'alg' names
    ("HS256", {}, "HMAC", {"hash": "SHA-256"}),
    ("hs512", {}, "HMAC", {"hash": "SHA-512"}),
    ("RS256", {}, "RSA", {"hash": "SHA-256"}),
    ("PS384", {}, "RSA", {"hash": "SHA-384"}),
    ("ES256", {}, "EC", {"curve": "P-256", "hash": "SHA-256"}),
    ("ES512", {}, "EC", {"curve": "P-521"}),
    ("EdDSA", {}, "Ed25519", {}),
    # Certificate signature names
    ("sha256WithRSAEncryption", {}, "RSA", {"hash": "SHA-256"}),
    ("sha1WithRSAEncryption", {}, "RSA", {"hash": "SHA-1"}),
    ("ecdsa-with-SHA384", {}, "EC", {"hash": "SHA-384"}),
    ("dsa_with_SHA256", {}, "DSA", {"hash": "SHA-256"}),
    ("ECC-secp256k1", {}, "EC", {"curve": "secp256k1"}),
    # TLS protocol versions
    ("TLSv1", {}, "TLS-1.0", {}),
    ("TLSv1.1", {}, "TLS-1.1", {}),
    ("TLS1.3", {}, "TLS-1.3", {}),
    ("TLS-1.2", {}, "TLS-1.2", {}),
    ("SSLv3", {}, "SSL-3.0", {}),
    # Cipher suites: OpenSSL and IANA spellings
    ("DES-CBC3-SHA", {}, "TLS_RSA_WITH_3DES_EDE_CBC_SHA", {}),
    ("AES256-SHA", {}, "TLS_RSA_WITH_AES_256_CBC_SHA", {}),
    ("ECDHE-RSA-AES128-GCM-SHA256", {}, "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256", {}),
    ("TLS_RSA_WITH_AES_128_CBC_SHA", {}, "TLS_RSA_WITH_AES_128_CBC_SHA", {}),
    ("SSL_RSA_WITH_3DES_EDE_CBC_SHA", {}, "TLS_RSA_WITH_3DES_EDE_CBC_SHA", {}),
    ("TLS_AES_256_GCM_SHA384", {}, "TLS_AES_256_GCM_SHA384", {}),
    # SSH algorithm names
    ("diffie-hellman-group14-sha1", {}, "DH", {"key_size": 2048, "hash": "SHA-1"}),
    ("diffie-hellman-group16-sha512", {}, "DH", {"key_size": 4096}),
    ("curve25519-sha256", {}, "X25519", {}),
    ("ssh-rsa", {}, "RSA", {"hash": "SHA-1"}),
    ("ssh-ed25519", {}, "Ed25519", {}),
    ("ecdsa-sha2-nistp256", {}, "EC", {"curve": "P-256"}),
    ("aes128-cbc", {}, "AES", {"key_size": 128, "mode": "CBC"}),
    ("aes256-ctr", {}, "AES", {"key_size": 256, "mode": "CTR"}),
    ("chacha20-poly1305@openssh.com", {}, "ChaCha20-Poly1305", {}),
    ("hmac-sha1", {}, "HMAC", {"hash": "SHA-1"}),
    ("hmac-sha2-256", {}, "HMAC", {"hash": "SHA-256"}),
    # Tier 5 families
    ("RC4", {}, "RC4", {}),
    ("ARC4", {}, "RC4", {}),
    ("arcfour", {}, "RC4", {}),
    ("RC4-SHA", {}, "TLS_RSA_WITH_RC4_128_SHA", {}),
    ("TEA", {}, "TEA", {}),
    ("XTEA", {}, "TEA", {}),
    ("HMAC-MD5", {}, "HMAC", {"hash": "MD5"}),
    # Post-quantum: names, parameter sets, pre-standard names, OIDs, CycloneDX properties
    ("ML-KEM-768", {}, "ML-KEM", {"param_set": "768", "prestandard": None}),
    ("MLKEM1024", {}, "ML-KEM", {"param_set": "1024"}),
    ("ML_KEM_512", {}, "ML-KEM", {"param_set": "512"}),
    ("ML-KEM", {"parameterSetIdentifier": "768"}, "ML-KEM", {"param_set": "768"}),
    ("Kyber768", {}, "ML-KEM", {"param_set": "768", "prestandard": True}),
    ("ML-DSA-65", {}, "ML-DSA", {"param_set": "65", "prestandard": None}),
    ("MLDSA87", {}, "ML-DSA", {"param_set": "87"}),
    ("ML-DSA", {"parameterSetIdentifier": "44"}, "ML-DSA", {"param_set": "44"}),
    ("ML-DSA", {"parameterSetIdentifier": "ML-DSA-65"}, "ML-DSA", {"param_set": "65"}),
    ("Dilithium3", {}, "ML-DSA", {"param_set": "65", "prestandard": True}),
    ("X25519Kyber768Draft00", {}, "X25519MLKEM768", {"prestandard": True}),
    ("X25519MLKEM768", {}, "X25519MLKEM768", {"prestandard": None}),
    ("SPHINCS+-SHA2-128s", {}, "SLH-DSA", {"prestandard": True}),
    ("2.16.840.1.101.3.4.4.2", {}, "ML-KEM", {"prestandard": None}),
    ("id-ml-dsa-87", {}, "ML-DSA", {"param_set": "87"}),
    ("2.16.840.1.101.3.4.3.18", {}, "ML-DSA", {"param_set": "65"}),
    ("2.16.840.1.101.3.4.4.2", {}, "ML-KEM", {"param_set": "768"}),
    ("SLH-DSA-SHA2-128s", {}, "SLH-DSA", {"param_set": "SHA2-128S"}),
    ("SPHINCS+", {}, "SLH-DSA", {}),
    ("DSA", {}, "DSA", {}),
    ("FN-DSA", {}, "FN-DSA", {}),
    ("Falcon-512", {}, "FN-DSA", {}),
    # Hybrids
    ("X25519MLKEM768", {}, "X25519MLKEM768", {}),
    ("x25519_mlkem768", {}, "X25519MLKEM768", {}),
    ("mlkem768x25519-sha256", {}, "X25519MLKEM768", {}),
    ("SecP256r1MLKEM768", {}, "SecP256r1MLKEM768", {}),
    ("SecP384r1MLKEM1024", {}, "SecP384r1MLKEM1024", {}),
    ("sntrup761x25519-sha512@openssh.com", {}, "sntrup761x25519", {}),
    ("X25519", {}, "X25519", {}),
    ("curve25519-sha256", {}, "X25519", {}),
    ("secp384r1", {}, "EC", {"curve": "P-384"}),
    # Go, Node and OpenSSL spellings
    ("tls.VersionTLS10", {}, "TLS-1.0", {}),
    ("VersionTLS13", {}, "TLS-1.3", {}),
    ("TLS1_VERSION", {}, "TLS-1.0", {}),
    ("TLS1_2_VERSION", {}, "TLS-1.2", {}),
    ("EVP_des_ede3_cbc", {}, "3DES", {"mode": "CBC"}),
    ("EVP_aes_128_ecb", {}, "AES", {"key_size": 128, "mode": "ECB"}),
    ("EVP_sha3_256", {}, "SHA3-256", {}),
    ("EVP_PKEY_X25519", {}, "X25519", {}),
    ("EVP_PKEY_RSA", {}, "RSA", {}),
    ("NID_X9_62_prime256v1", {}, "EC", {"curve": "P-256"}),
    ("des-ede3-cbc", {}, "3DES", {"mode": "CBC"}),
    ("aes-128-ecb", {}, "AES", {"key_size": 128, "mode": "ECB"}),
    ("prime256v1", {}, "EC", {"curve": "P-256"}),
    ("modp14", {}, "DH", {"key_size": 2048}),
    ("ffdhe2048", {}, "DH", {"key_size": 2048}),
    ("RSA-PSS", {}, "RSA", {}),
    ("mlkem.GenerateKey1024", {}, "ML-KEM", {"param_set": "1024"}),
    ("elliptic.P384", {}, "EC", {"curve": "P-384"}),
]


def main() -> int:
    bad = 0
    for name, props, fam, params in CASES:
        got_fam, got_params = normalize(name, props)
        ok = got_fam == fam and all(got_params.get(k) == v for k, v in params.items())
        if not ok:
            bad += 1
            print(f"FAIL {name!r} {props} -> {got_fam} {got_params}; want {fam} {params}")
    print(f"{len(CASES) - bad}/{len(CASES)} normalizer cases pass")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
