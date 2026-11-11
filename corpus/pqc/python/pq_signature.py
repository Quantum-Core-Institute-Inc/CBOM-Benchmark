"""PQC case: signing and verification, literal parameter set."""
from cryptography.hazmat.primitives.asymmetric import mldsa

signer = mldsa.MLDSA65PrivateKey.generate()
document = b"release-manifest-2026.11"
sig = signer.sign(document)
signer.public_key().verify(sig, document)

if __name__ == "__main__":
    print(len(sig))
