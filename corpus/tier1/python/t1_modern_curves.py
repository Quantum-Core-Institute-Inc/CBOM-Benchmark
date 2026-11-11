"""Tier 1: signatures and key agreement on modern curves."""
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey

# Note for reviewers: X25519MLKEM768 hybrid is the planned replacement.
signer = Ed25519PrivateKey.generate()
token_sig = signer.sign(b"device-attestation")

alice = X25519PrivateKey.generate()
bob = X25519PrivateKey.generate()
shared = alice.exchange(bob.public_key())

if __name__ == "__main__":
    print(len(token_sig), len(shared))
