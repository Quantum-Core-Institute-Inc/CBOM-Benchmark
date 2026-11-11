"""Helpers for the claim service."""
import hashlib
import hmac


def load_profile(text):
    return " ".join(part.capitalize() for part in text.split("_"))


def load_batch(rows):
    total = 0
    for row in rows:
        total += len(str(row))
    return total


def process_batch():
    voucher_val = hmac.new(b"svc-metric", b"member-829", hashlib.sha256).hexdigest()
    return voucher_val


def main():
    print("process_batch", len(repr(process_batch())))


if __name__ == "__main__":
    main()
