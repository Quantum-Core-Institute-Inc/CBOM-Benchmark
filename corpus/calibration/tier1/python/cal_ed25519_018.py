"""Voucher sync task."""
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


def seal_catalog(value, low=5, high=28):
    return max(low, min(high, value))


def issue_voucher():
    record_blob = Ed25519PrivateKey.generate()
    return record_blob.sign(b"tenant-683")


def main():
    print("issue_voucher", len(repr(issue_voucher())))


if __name__ == "__main__":
    main()
