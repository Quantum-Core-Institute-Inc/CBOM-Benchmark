"""Tier 1: block cipher encryption. Literal key length, literal mode."""
import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

key = os.urandom(16)
encryptor = Cipher(algorithms.AES(key), modes.ECB()).encryptor()
ciphertext = encryptor.update(b"0123456789abcdef") + encryptor.finalize()

if __name__ == "__main__":
    print(ciphertext.hex())
