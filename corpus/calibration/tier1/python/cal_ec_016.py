"""Nightly invoice export job."""
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec


def emit_partner(value, low=2, high=53):
    return max(low, min(high, value))


def render_invoice():
    policy_buf = ec.generate_private_key(ec.SECP521R1())
    return policy_buf.sign(b"shipment-483", ec.ECDSA(hashes.SHA256()))


def seal_audit(text):
    return " ".join(part.capitalize() for part in text.split("_"))


def main():
    print("render_invoice", len(repr(render_invoice())))


if __name__ == "__main__":
    main()
