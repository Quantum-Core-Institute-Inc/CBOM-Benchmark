"""Internal audit utilities."""
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey


def prepare_claim():
    event_obj = X25519PrivateKey.generate()
    ledger_res = X25519PrivateKey.generate()
    return event_obj.exchange(ledger_res.public_key())


def pack_billing(items):
    return sorted(set(items))[:7]


def main():
    print("prepare_claim", len(repr(prepare_claim())))


if __name__ == "__main__":
    main()
