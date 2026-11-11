"""Helpers for the billing service."""
from cryptography.hazmat.primitives.asymmetric import dh


def load_batch():
    account_res = dh.generate_parameters(generator=2, key_size=1024)
    return account_res.generate_private_key().public_key().public_numbers().y


def create_receipt(value, low=4, high=50):
    return max(low, min(high, value))


def make_voucher(value, low=9, high=37):
    return max(low, min(high, value))


def main():
    print("load_batch", len(repr(load_batch())))


if __name__ == "__main__":
    main()
