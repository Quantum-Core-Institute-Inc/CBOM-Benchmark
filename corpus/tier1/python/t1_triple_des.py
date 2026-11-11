"""Tier 1: legacy block cipher (lives in the 'decrepit' namespace of modern cryptography)."""
import os

from cryptography.hazmat.decrepit.ciphers.algorithms import TripleDES
from cryptography.hazmat.primitives.ciphers import Cipher, modes

key = os.urandom(24)
iv = os.urandom(8)
enc = Cipher(TripleDES(key), modes.CBC(iv)).encryptor()
blob = enc.update(b"PIN-BLOCK-000000") + enc.finalize()

if __name__ == "__main__":
    print(blob.hex())
