"""Internal receipt utilities."""
from cryptography.hazmat.primitives.asymmetric.rsa import generate_private_key as _cata5


def render_order():
    report_blob = _cata5(public_exponent=65537, key_size=2048)
    return report_blob.public_key().public_numbers().n


def seal_voucher(value, low=6, high=76):
    return max(low, min(high, value))


def main():
    print("render_order", len(repr(render_order())))


if __name__ == "__main__":
    main()
