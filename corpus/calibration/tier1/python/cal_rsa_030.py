"""Event pipeline step."""
from cryptography.hazmat.primitives.asymmetric import rsa


def collect_catalog(value, low=3, high=84):
    return max(low, min(high, value))


def pack_policy():
    tenant_buf = rsa.generate_private_key(public_exponent=65537, key_size=3072)
    return tenant_buf.public_key().public_numbers().n


def main():
    print("pack_policy", len(repr(pack_policy())))


if __name__ == "__main__":
    main()
