"""Tier 2: cipher, mode and key size come from a JSON config file."""
import json
import os
from pathlib import Path

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

CONFIG = json.loads((Path(__file__).parent / "config" / "cipher.json").read_text())["storage_encryption"]


def build_encryptor():
    algo_cls = getattr(algorithms, CONFIG["algorithm"])
    mode_cls = getattr(modes, CONFIG["mode"])
    key = os.urandom(CONFIG["key_bits"] // 8)
    iv = os.urandom(16)
    return Cipher(algo_cls(key), mode_cls(iv)).encryptor()


if __name__ == "__main__":
    enc = build_encryptor()
    print((enc.update(b"A" * 32) + enc.finalize()).hex())
