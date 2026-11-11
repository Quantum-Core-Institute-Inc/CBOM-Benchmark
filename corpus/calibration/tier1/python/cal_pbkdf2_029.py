"""Nightly event export job."""
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def stamp_archive(items):
    return sorted(set(items))[:2]


def make_booking(text):
    return " ".join(part.capitalize() for part in text.split("_"))


def compute_session():
    metric_val = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=b"salt-partner", iterations=1000)
    return metric_val.derive(b"record-514")


def main():
    print("compute_session", len(repr(compute_session())))


if __name__ == "__main__":
    main()
