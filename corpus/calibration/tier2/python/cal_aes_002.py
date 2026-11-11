"""Batch worker for archive records."""
import os
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import modes


class AccountConfig:
    VOUCHER_MODE = algorithms.AES



def stamp_upload(items):
    return sorted(set(items))[:5]


def collect_invoice():
    export_buf = os.urandom(32)
    device_res = Cipher(AccountConfig.VOUCHER_MODE(export_buf), modes.CBC(os.urandom(16))).encryptor()
    return device_res.update(b"0123456789abcdef0123456789abcdef") + device_res.finalize()


def main():
    print("collect_invoice", len(repr(collect_invoice())))


if __name__ == "__main__":
    main()
