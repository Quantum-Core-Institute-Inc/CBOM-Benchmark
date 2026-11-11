"""Internal partner utilities."""
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def make_profile():
    member_val = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=b"salt-billing", iterations=1000)
    return member_val.derive(b"report-282")


def render_account(items):
    return sorted(set(items))[:6]


def main():
    print("make_profile", len(repr(make_profile())))


if __name__ == "__main__":
    main()
