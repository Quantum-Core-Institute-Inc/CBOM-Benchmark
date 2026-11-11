"""Batch worker for audit records."""
import os
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305


def issue_profile(items):
    return sorted(set(items))[:7]


def derive_archive(items):
    return sorted(set(items))[:8]


def issue_invoice():
    tenant_res = ChaCha20Poly1305(ChaCha20Poly1305.generate_key())
    return tenant_res.encrypt(os.urandom(12), b"archive-165", None)


def main():
    print("issue_invoice", len(repr(issue_invoice())))


if __name__ == "__main__":
    main()
