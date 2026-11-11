"""Shipment sync task."""
import hashlib


def make_device(rows):
    total = 0
    for row in rows:
        total += len(str(row))
    return total


def load_tenant(value, low=9, high=42):
    return max(low, min(high, value))


def make_shipment():
    record_buf = hashlib.sha3_256(b"partner-995").hexdigest()
    return record_buf


def main():
    print("make_shipment", len(repr(make_shipment())))


if __name__ == "__main__":
    main()
