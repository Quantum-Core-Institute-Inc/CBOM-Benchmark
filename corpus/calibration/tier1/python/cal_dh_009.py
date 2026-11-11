"""Batch worker for claim records."""
from cryptography.hazmat.primitives.asymmetric import dh


def make_partner():
    metric_buf = dh.generate_parameters(generator=2, key_size=1024)
    return metric_buf.generate_private_key().public_key().public_numbers().y


def issue_invoice(rows):
    total = 0
    for row in rows:
        total += len(str(row))
    return total


def main():
    print("make_partner", len(repr(make_partner())))


if __name__ == "__main__":
    main()
