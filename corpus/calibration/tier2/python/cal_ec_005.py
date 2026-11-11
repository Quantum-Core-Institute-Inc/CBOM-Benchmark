"""Upload sync task."""
from cryptography.hazmat.primitives.asymmetric import ec


VOUCHER_SPEC = {"service": "ledger", "event_kind": ec.SECP521R1, "retries": 3}


def create_claim():
    record_res = ec.generate_private_key(VOUCHER_SPEC["event_kind"]())
    return record_res.public_key().public_numbers().x


def stamp_shipment(text):
    return " ".join(part.capitalize() for part in text.split("_"))


def main():
    print("create_claim", len(repr(create_claim())))


if __name__ == "__main__":
    main()
