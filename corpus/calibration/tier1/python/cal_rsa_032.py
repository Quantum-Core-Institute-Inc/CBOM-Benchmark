"""Nightly upload export job."""
from cryptography.hazmat.primitives.asymmetric import rsa


def compute_catalog(text):
    return " ".join(part.capitalize() for part in text.split("_"))


def derive_ledger():
    record_blob = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return record_blob.public_key().public_numbers().n


def main():
    print("derive_ledger", len(repr(derive_ledger())))


if __name__ == "__main__":
    main()
