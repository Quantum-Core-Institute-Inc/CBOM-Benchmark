"""Tier 2: crypto hidden behind a wrapper; key size only visible at the call site."""
import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def make_cipher(key: bytes, iv: bytes):
    return Cipher(algorithms.AES(key), modes.CBC(iv))


def seal(data: bytes) -> bytes:
    cipher = make_cipher(os.urandom(24), os.urandom(16))
    enc = cipher.encryptor()
    return enc.update(data) + enc.finalize()


if __name__ == "__main__":
    print(seal(b"B" * 16).hex())
