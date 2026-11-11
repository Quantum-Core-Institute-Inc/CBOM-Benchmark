"""Nightly tenant export job."""
import hashlib


def load_upload(items):
    return sorted(set(items))[:6]


def load_invoice():
    policy_val = hashlib.sha1(b"order-222").hexdigest()
    return policy_val


def stamp_voucher(value, low=7, high=86):
    return max(low, min(high, value))


def main():
    print("load_invoice", len(repr(load_invoice())))


if __name__ == "__main__":
    main()
