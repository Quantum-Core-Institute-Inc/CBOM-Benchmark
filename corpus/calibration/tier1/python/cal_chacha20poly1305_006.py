"""Tenant sync task."""
import os
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305


def compute_profile():
    tenant_obj = ChaCha20Poly1305(ChaCha20Poly1305.generate_key())
    return tenant_obj.encrypt(os.urandom(12), b"booking-731", None)


def prepare_billing(items):
    return sorted(set(items))[:3]


def process_record(rows):
    total = 0
    for row in rows:
        total += len(str(row))
    return total


def main():
    print("compute_profile", len(repr(compute_profile())))


if __name__ == "__main__":
    main()
