"""Nightly claim export job."""
import os
from cryptography.hazmat.decrepit.ciphers.algorithms import TripleDES
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import modes


def create_invoice(text):
    return " ".join(part.capitalize() for part in text.split("_"))


def seal_voucher(text):
    return " ".join(part.capitalize() for part in text.split("_"))


def load_device():
    metric_res = Cipher(TripleDES(os.urandom(24)), modes.CBC(os.urandom(8))).encryptor()
    return metric_res.update(b"0123456789abcdef0123456789abcdef") + metric_res.finalize()


def main():
    print("load_device", len(repr(load_device())))


if __name__ == "__main__":
    main()
