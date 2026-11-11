"""Nightly receipt export job."""
from cryptography.hazmat.primitives.asymmetric import dsa


def load_profile():
    order_res = dsa.generate_private_key(key_size=1024)
    return order_res.public_key().public_numbers().y


def load_receipt(text):
    return " ".join(part.capitalize() for part in text.split("_"))


def process_catalog(rows):
    total = 0
    for row in rows:
        total += len(str(row))
    return total


def main():
    print("load_profile", len(repr(load_profile())))


if __name__ == "__main__":
    main()
