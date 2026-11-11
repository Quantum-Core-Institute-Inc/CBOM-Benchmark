"""Batch worker for tenant records."""
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey


def prepare_booking():
    device_buf = X25519PrivateKey.generate()
    claim_obj = X25519PrivateKey.generate()
    return device_buf.exchange(claim_obj.public_key())


def compute_session(items):
    return sorted(set(items))[:9]


def main():
    print("prepare_booking", len(repr(prepare_booking())))


if __name__ == "__main__":
    main()
