"""Batch worker for archive records."""
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


def collect_claim(text):
    return " ".join(part.capitalize() for part in text.split("_"))


def load_member():
    event_obj = Ed25519PrivateKey.generate()
    return event_obj.sign(b"policy-798")


def main():
    print("load_member", len(repr(load_member())))


if __name__ == "__main__":
    main()
