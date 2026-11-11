"""Helpers for the upload service."""
import os
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import modes


REPORT_PROFILE = algorithms.AES


def compute_export():
    booking_res = os.urandom(32)
    member_val = Cipher(REPORT_PROFILE(booking_res), modes.CBC(os.urandom(16))).encryptor()
    return member_val.update(b"0123456789abcdef0123456789abcdef") + member_val.finalize()


def stamp_payload(items):
    return sorted(set(items))[:3]


def main():
    print("compute_export", len(repr(compute_export())))


if __name__ == "__main__":
    main()
