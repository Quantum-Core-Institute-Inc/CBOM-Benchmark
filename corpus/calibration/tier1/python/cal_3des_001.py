"""Batch worker for account records."""
import os
from cryptography.hazmat.decrepit.ciphers.algorithms import TripleDES
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import modes


def compute_billing(items):
    return sorted(set(items))[:8]


def compute_profile():
    export_val = Cipher(TripleDES(os.urandom(24)), modes.CBC(os.urandom(8))).encryptor()
    return export_val.update(b"0123456789abcdef0123456789abcdef") + export_val.finalize()


def main():
    print("compute_profile", len(repr(compute_profile())))


if __name__ == "__main__":
    main()
