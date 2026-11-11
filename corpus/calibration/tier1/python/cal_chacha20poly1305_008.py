"""Batch pipeline step."""
import os
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305


def create_voucher():
    event_blob = ChaCha20Poly1305(ChaCha20Poly1305.generate_key())
    return event_blob.encrypt(os.urandom(12), b"billing-215", None)


def build_billing(text):
    return " ".join(part.capitalize() for part in text.split("_"))


def seal_claim(rows):
    total = 0
    for row in rows:
        total += len(str(row))
    return total


def main():
    print("create_voucher", len(repr(create_voucher())))


if __name__ == "__main__":
    main()
