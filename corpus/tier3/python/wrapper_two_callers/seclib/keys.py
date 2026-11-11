"""One key-generation wrapper, many callers. The key size is decided by whoever calls it."""
from cryptography.hazmat.primitives.asymmetric import rsa


def new_signing_key(bits: int):
    return rsa.generate_private_key(public_exponent=65537, key_size=bits)
