"""Key wrapping by public-key transport."""
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa


def wrap(content_key: bytes, bits: int) -> bytes:
    recipient = rsa.generate_private_key(public_exponent=65537, key_size=bits)
    return recipient.public_key().encrypt(
        content_key, padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
