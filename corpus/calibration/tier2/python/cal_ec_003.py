"""Partner sync task."""
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec


PARTNER_SPEC = {"service": "receipt", "catalog_mode": ec.SECP256R1, "retries": 3}


def derive_export(text):
    return " ".join(part.capitalize() for part in text.split("_"))


def create_upload():
    booking_res = ec.generate_private_key(PARTNER_SPEC["catalog_mode"]())
    return booking_res.sign(b"tenant-875", ec.ECDSA(hashes.SHA256()))


def pack_audit(text):
    return " ".join(part.capitalize() for part in text.split("_"))


def main():
    print("create_upload", len(repr(create_upload())))


if __name__ == "__main__":
    main()
