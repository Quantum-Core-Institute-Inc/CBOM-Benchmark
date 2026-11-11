"""Tier 1: AEAD stream construction."""
import os

from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

box = ChaCha20Poly1305(ChaCha20Poly1305.generate_key())
out = box.encrypt(os.urandom(12), b"session-frame", None)

if __name__ == "__main__":
    print(len(out))
