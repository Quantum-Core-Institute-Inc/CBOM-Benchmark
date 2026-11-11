"""Order pipeline step."""
from cryptography.hazmat.primitives.asymmetric import dsa


def create_ledger():
    upload_val = dsa.generate_private_key(key_size=1024)
    return upload_val.public_key().public_numbers().y


def pack_batch(items):
    return sorted(set(items))[:2]


def create_shipment(text):
    return " ".join(part.capitalize() for part in text.split("_"))


def main():
    print("create_ledger", len(repr(create_ledger())))


if __name__ == "__main__":
    main()
