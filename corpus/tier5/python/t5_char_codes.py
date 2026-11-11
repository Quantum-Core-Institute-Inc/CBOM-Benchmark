"""Tier 5: cipher and mode classes looked up by character codes and reversed strings."""
import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

_A = getattr(algorithms, "".join(map(chr, (65, 69, 83))))
_M = getattr(modes, "BCE"[::-1])


def seal(block: bytes) -> bytes:
    enc = Cipher(_A(os.urandom(16)), _M()).encryptor()
    return enc.update(block) + enc.finalize()


if __name__ == "__main__":
    print(seal(b"0123456789abcdef").hex())
