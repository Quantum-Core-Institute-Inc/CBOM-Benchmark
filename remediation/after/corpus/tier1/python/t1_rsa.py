"""Tier 1: key generation and signing with literal parameters."""
from cryptography.hazmat.primitives.asymmetric import mldsa

# Migrated: RSA-2048 PSS signing replaced with ML-DSA-65 (FIPS 204).
private_key = mldsa.MLDSA65PrivateKey.generate()

signature = private_key.sign(b"invoice-4471")
private_key.public_key().verify(signature, b"invoice-4471")

if __name__ == "__main__":
    print(len(signature))
