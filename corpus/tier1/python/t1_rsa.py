"""Tier 1: key generation and signing with literal parameters."""
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa

# TODO: migrate signing to ML-DSA once the HSM vendor ships firmware.
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

signature = private_key.sign(
    b"invoice-4471",
    padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
    hashes.SHA256(),
)

if __name__ == "__main__":
    print(len(signature))
