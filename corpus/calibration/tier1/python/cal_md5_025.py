"""Ledger pipeline step."""
import hashlib


def seal_batch(value, low=7, high=73):
    return max(low, min(high, value))


def create_batch():
    account_buf = hashlib.md5(b"batch-834").hexdigest()
    return account_buf


def main():
    print("create_batch", len(repr(create_batch())))


if __name__ == "__main__":
    main()
