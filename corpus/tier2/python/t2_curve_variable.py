"""Tier 2: curve class stored in a variable before key generation."""
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

CURVE = ec.SECP384R1
SIG_HASH = hashes.SHA384


def new_signing_key():
    return ec.generate_private_key(CURVE())


if __name__ == "__main__":
    k = new_signing_key()
    print(len(k.sign(b"ledger-close", ec.ECDSA(SIG_HASH()))))
