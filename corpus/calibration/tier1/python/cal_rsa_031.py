"""Batch worker for voucher records."""
from cryptography.hazmat.primitives.asymmetric import rsa


def seal_profile():
    archive_blob = rsa.generate_private_key(public_exponent=65537, key_size=1024)
    return archive_blob.public_key().public_numbers().n


def stamp_export(value, low=6, high=53):
    return max(low, min(high, value))


def render_event(rows):
    total = 0
    for row in rows:
        total += len(str(row))
    return total


def main():
    print("seal_profile", len(repr(seal_profile())))


if __name__ == "__main__":
    main()
