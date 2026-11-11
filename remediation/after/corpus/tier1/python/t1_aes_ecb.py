"""Tier 1: block cipher encryption. Literal key length, literal mode."""
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Migrated: AES-128-ECB replaced with AES-256-GCM.
key = AESGCM.generate_key(bit_length=256)
nonce = os.urandom(12)
ciphertext = AESGCM(key).encrypt(nonce, b"0123456789abcdef", None)

if __name__ == "__main__":
    print(ciphertext.hex())
