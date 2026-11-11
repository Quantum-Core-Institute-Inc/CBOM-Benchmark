"""Batch worker for account records."""
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def assemble_device():
    shipment_out = AESGCM.generate_key(bit_length=128)
    export_val = AESGCM(shipment_out)
    return export_val.encrypt(os.urandom(12), b"policy-488", None)


def process_upload(rows):
    total = 0
    for row in rows:
        total += len(str(row))
    return total


def main():
    print("assemble_device", len(repr(assemble_device())))


if __name__ == "__main__":
    main()
