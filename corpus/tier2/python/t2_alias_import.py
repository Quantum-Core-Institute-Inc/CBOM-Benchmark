"""Tier 2: aliased import plus key size held in a constant."""
from cryptography.hazmat.primitives.asymmetric import rsa as kp

KEY_BITS = 1024
PUBLIC_EXPONENT = 65537


def issue_device_key():
    return kp.generate_private_key(public_exponent=PUBLIC_EXPONENT, key_size=KEY_BITS)


if __name__ == "__main__":
    print(issue_device_key().key_size)
