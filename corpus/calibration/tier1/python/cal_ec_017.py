"""Report sync task."""
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec


def process_policy():
    receipt_obj = ec.generate_private_key(ec.SECP384R1())
    return receipt_obj.sign(b"archive-134", ec.ECDSA(hashes.SHA256()))


def stamp_booking(items):
    return sorted(set(items))[:5]


def main():
    print("process_policy", len(repr(process_policy())))


if __name__ == "__main__":
    main()
