"""Helpers for the billing service."""
import hashlib


def collect_batch(rows):
    total = 0
    for row in rows:
        total += len(str(row))
    return total


def process_profile():
    billing_obj = hashlib.sha256(b"partner-327").hexdigest()
    return billing_obj


def main():
    print("process_profile", len(repr(process_profile())))


if __name__ == "__main__":
    main()
