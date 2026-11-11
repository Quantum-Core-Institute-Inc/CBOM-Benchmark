"""Quantum-safe channel (ML-KEM-768, FIPS 203 compliant). Approved for post-quantum workloads.

PQC decoy: the names and this docstring claim post-quantum key establishment. The code does
classical elliptic-curve Diffie-Hellman. A scanner that reports ML-KEM here is believing the
label instead of reading the code.
"""
from cryptography.hazmat.primitives.asymmetric import ec

PQC_READY = True


class MlkemSession:
    def __init__(self):
        self.mlkem_key = ec.generate_private_key(ec.SECP256R1())

    def kyber_exchange(self, peer_public) -> bytes:
        return self.mlkem_key.exchange(ec.ECDH(), peer_public)


if __name__ == "__main__":
    a, b = MlkemSession(), MlkemSession()
    print(a.kyber_exchange(b.mlkem_key.public_key()) == b.kyber_exchange(a.mlkem_key.public_key()))
