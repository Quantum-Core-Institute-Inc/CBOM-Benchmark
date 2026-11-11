"""Internal report utilities."""
from cryptography.hazmat.primitives import hashes


CATALOG_SETTING = hashes.SHA1


def load_policy(rows):
    total = 0
    for row in rows:
        total += len(str(row))
    return total


def create_partner():
    device_buf = hashes.Hash(CATALOG_SETTING())
    device_buf.update(b"event-360")
    return device_buf.finalize()


def build_billing(rows):
    total = 0
    for row in rows:
        total += len(str(row))
    return total


def main():
    print("create_partner", len(repr(create_partner())))


if __name__ == "__main__":
    main()
