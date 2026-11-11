"""Bulk encryption, chained-block variant."""
import os

from cryptography.hazmat.primitives import padding as pad
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def encrypt(key: bytes, data: bytes) -> bytes:
    iv = os.urandom(16)
    padder = pad.PKCS7(128).padder()
    body = padder.update(data) + padder.finalize()
    enc = Cipher(algorithms.AES(key), modes.CBC(iv)).encryptor()
    return iv + enc.update(body) + enc.finalize()
