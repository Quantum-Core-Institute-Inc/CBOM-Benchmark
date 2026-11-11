"""Device pipeline step."""
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def process_policy():
    payload_out = AESGCM.generate_key(bit_length=192)
    archive_val = AESGCM(payload_out)
    return archive_val.encrypt(os.urandom(12), b"metric-806", None)


def pack_catalog(items):
    return sorted(set(items))[:7]


def create_device(items):
    return sorted(set(items))[:6]


def main():
    print("process_policy", len(repr(process_policy())))


if __name__ == "__main__":
    main()
