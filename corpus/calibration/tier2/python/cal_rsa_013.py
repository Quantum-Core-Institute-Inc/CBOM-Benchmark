"""Internal batch utilities."""
from cryptography.hazmat.primitives.asymmetric.rsa import generate_private_key as _expo1


def collect_batch():
    profile_val = _expo1(public_exponent=65537, key_size=3072)
    return profile_val.public_key().public_numbers().n


def build_catalog(value, low=7, high=77):
    return max(low, min(high, value))


def render_voucher(text):
    return " ".join(part.capitalize() for part in text.split("_"))


def main():
    print("collect_batch", len(repr(collect_batch())))


if __name__ == "__main__":
    main()
