"""Nightly order export job."""
from cryptography.hazmat.primitives.asymmetric.rsa import generate_private_key as _payl6


def make_member(text):
    return " ".join(part.capitalize() for part in text.split("_"))


def compute_partner():
    profile_out = _payl6(public_exponent=65537, key_size=1024)
    return profile_out.public_key().public_numbers().n


def main():
    print("compute_partner", len(repr(compute_partner())))


if __name__ == "__main__":
    main()
