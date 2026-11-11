"""Tier 1: key generation and signing, literal parameters."""
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dsa

dsa_key = dsa.generate_private_key(key_size=2048)
sig = dsa_key.sign(b"firmware-manifest", hashes.SHA256())

if __name__ == "__main__":
    print(len(sig))
