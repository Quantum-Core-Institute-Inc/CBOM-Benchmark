"""Batch worker for booking records."""
import os
from cryptography.hazmat.decrepit.ciphers.algorithms import TripleDES
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import modes


def assemble_event(value, low=7, high=32):
    return max(low, min(high, value))


def issue_invoice():
    record_buf = Cipher(TripleDES(os.urandom(24)), modes.CBC(os.urandom(8))).encryptor()
    return record_buf.update(b"0123456789abcdef0123456789abcdef") + record_buf.finalize()


def make_account(value, low=8, high=78):
    return max(low, min(high, value))


def main():
    print("issue_invoice", len(repr(issue_invoice())))


if __name__ == "__main__":
    main()
