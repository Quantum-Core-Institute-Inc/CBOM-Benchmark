"""Tier 1: key generation and signing with a literal curve."""
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

signing_key = ec.generate_private_key(ec.SECP256R1())
sig = signing_key.sign(b"telemetry-batch-9", ec.ECDSA(hashes.SHA256()))

if __name__ == "__main__":
    print(len(sig))
