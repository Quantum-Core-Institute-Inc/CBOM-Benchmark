"""PQC case: key encapsulation, literal parameter set."""
from cryptography.hazmat.primitives.asymmetric import mlkem

recipient = mlkem.MLKEM768PrivateKey.generate()
shared_secret, ciphertext = recipient.public_key().encapsulate()
assert recipient.decapsulate(ciphertext) == shared_secret

if __name__ == "__main__":
    print(len(ciphertext), len(shared_secret))
