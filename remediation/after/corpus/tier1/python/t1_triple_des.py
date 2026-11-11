"""Tier 1: legacy block cipher, migrated off the 'decrepit' namespace."""
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Migrated: 3DES-CBC replaced with AES-256-GCM.
key = AESGCM.generate_key(bit_length=256)
nonce = os.urandom(12)
blob = AESGCM(key).encrypt(nonce, b"PIN-BLOCK-000000", None)

if __name__ == "__main__":
    print(blob.hex())
