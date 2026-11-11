"""PQC case: application-level hybrid key establishment.

A classical exchange and a post-quantum encapsulation run side by side, and both secrets go
through one KDF. The session key survives as long as either half does.
"""
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import mlkem
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


def establish():
    server_classical = X25519PrivateKey.generate()
    server_pq = mlkem.MLKEM768PrivateKey.generate()

    client_classical = X25519PrivateKey.from_private_bytes(bytes(range(32)))
    ss_classical = client_classical.exchange(server_classical.public_key())
    ss_pq, ct = server_pq.public_key().encapsulate()

    session_key = HKDF(algorithm=hashes.SHA256(), length=32, salt=None,
                       info=b"hybrid-session-v1").derive(ss_classical + ss_pq)
    return session_key, ct


if __name__ == "__main__":
    key, ct = establish()
    print(len(key), len(ct))
