"""Key wrapping by ephemeral-static key agreement."""
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

_CURVES = {"p256": ec.SECP256R1, "p384": ec.SECP384R1}


def wrap(content_key: bytes, curve: str) -> bytes:
    recipient = ec.generate_private_key(_CURVES[curve]())
    ephemeral = ec.generate_private_key(_CURVES[curve]())
    shared = ephemeral.exchange(ec.ECDH(), recipient.public_key())
    kek = HKDF(algorithm=hashes.SHA256(), length=len(content_key), salt=None, info=b"envelope-kek").derive(shared)
    return bytes(a ^ b for a, b in zip(content_key, kek))
