"""Tier 1: record sealing for the archive export."""
import os

from cryptography.hazmat.decrepit.ciphers.algorithms import TripleDES
from cryptography.hazmat.primitives.ciphers import Cipher, modes

key = os.urandom(24)
iv = os.urandom(8)
enc = Cipher(TripleDES(key), modes.CBC(iv)).encryptor()
sealed = enc.update(b"customer-record!") + enc.finalize()

if __name__ == "__main__":
    print(len(sealed))
