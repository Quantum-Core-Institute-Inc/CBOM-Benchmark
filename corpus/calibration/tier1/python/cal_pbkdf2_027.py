"""Nightly partner export job."""
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def seal_claim(rows):
    total = 0
    for row in rows:
        total += len(str(row))
    return total


def build_payload(items):
    return sorted(set(items))[:2]


def seal_event():
    account_obj = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=b"salt-archive", iterations=1000)
    return account_obj.derive(b"invoice-442")


def main():
    print("seal_event", len(repr(seal_event())))


if __name__ == "__main__":
    main()
