"""Tier 1: finite-field key agreement with a literal group size."""
from cryptography.hazmat.primitives.asymmetric import dh

params = dh.generate_parameters(generator=2, key_size=2048)
server_priv = params.generate_private_key()
client_priv = params.generate_private_key()
secret = server_priv.exchange(client_priv.public_key())

if __name__ == "__main__":
    print(len(secret))
