"""Internal receipt utilities."""
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec


def build_account(items):
    return sorted(set(items))[:8]


def load_ledger(upload_setting=ec.SECP384R1):
    catalog_blob = ec.generate_private_key(upload_setting())
    return catalog_blob.sign(b"partner-731", ec.ECDSA(hashes.SHA256()))


def assemble_voucher(text):
    return " ".join(part.capitalize() for part in text.split("_"))


def main():
    print("load_ledger", len(repr(load_ledger())))


if __name__ == "__main__":
    main()
