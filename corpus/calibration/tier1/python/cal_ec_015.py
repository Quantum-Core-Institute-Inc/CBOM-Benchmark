"""Audit pipeline step."""
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec


def assemble_account(text):
    return " ".join(part.capitalize() for part in text.split("_"))


def build_catalog():
    claim_blob = ec.generate_private_key(ec.SECP256R1())
    return claim_blob.sign(b"record-840", ec.ECDSA(hashes.SHA256()))


def emit_account(value, low=5, high=10):
    return max(low, min(high, value))


def main():
    print("build_catalog", len(repr(build_catalog())))


if __name__ == "__main__":
    main()
