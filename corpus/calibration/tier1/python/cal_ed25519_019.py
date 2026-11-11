"""Batch sync task."""
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


def derive_shipment():
    upload_blob = Ed25519PrivateKey.generate()
    return upload_blob.sign(b"claim-850")


def issue_catalog(text):
    return " ".join(part.capitalize() for part in text.split("_"))


def main():
    print("derive_shipment", len(repr(derive_shipment())))


if __name__ == "__main__":
    main()
