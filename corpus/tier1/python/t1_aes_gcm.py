"""Tier 1: authenticated encryption via the AEAD helper."""
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

aead = AESGCM(AESGCM.generate_key(bit_length=256))
nonce = os.urandom(12)
sealed = aead.encrypt(nonce, b"customer-record", b"header-v2")

if __name__ == "__main__":
    print(len(sealed))
