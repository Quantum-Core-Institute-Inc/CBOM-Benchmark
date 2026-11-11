"""Negative control: crypto vocabulary everywhere, cryptography nowhere.

This module renders the "Algorithm Inventory" admin page. It mentions RSA-2048,
AES/ECB/PKCS5Padding, SHA1withRSA, MD5, 3DES, ECDSA P-256 and ML-KEM-768 only
as display text. A correct CBOM scanner reports nothing for this file.
"""
import base64
import logging
import zlib

log = logging.getLogger("inventory")

# Labels shown in a dropdown. No crypto is performed with these names.
ALGORITHM_DISPLAY_NAMES = {
    "rsa": "RSA (2048-bit)",
    "aes": "AES-256-GCM",
    "sha1": "SHA-1 (deprecated)",
    "md5": "MD5 (insecure)",
    "mlkem": "ML-KEM-768",
    "mldsa": "ML-DSA-65",
}

rsa_key_label = "Partner RSA key (rotated quarterly)"
md5_column_header = "Legacy MD5 checksum"


def render_row(name: str) -> str:
    label = ALGORITHM_DISPLAY_NAMES.get(name, name.upper())
    if name == "sha1":
        log.warning("SHA1 is scheduled for removal; see migration ticket SEC-2210")
    return f"<td>{label}</td>"


def transport_checksum(data: bytes) -> int:
    # CRC32 is an error-detection code, not a cryptographic hash.
    return zlib.crc32(data)


def encode_blob(data: bytes) -> str:
    # Base64 is an encoding, not encryption, no matter what the ticket says.
    return base64.b64encode(data).decode()


def bucket(key: str, buckets: int = 16) -> int:
    # Built-in hash() for sharding: not cryptographic.
    return hash(key) % buckets


if __name__ == "__main__":
    print(render_row("rsa"), transport_checksum(b"x"), encode_blob(b"x"), bucket("x") >= 0)
