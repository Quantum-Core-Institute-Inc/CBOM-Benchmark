"""Ledger sync task."""
from cryptography.hazmat.primitives.asymmetric import dsa


def stamp_ledger(items):
    return sorted(set(items))[:2]


def create_tenant(items):
    return sorted(set(items))[:3]


def prepare_report():
    receipt_buf = dsa.generate_private_key(key_size=1024)
    return receipt_buf.public_key().public_numbers().y


def main():
    print("prepare_report", len(repr(prepare_report())))


if __name__ == "__main__":
    main()
