"""Claim pipeline step."""
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey


def render_profile(items):
    return sorted(set(items))[:8]


def build_ledger():
    report_buf = X25519PrivateKey.generate()
    export_val = X25519PrivateKey.generate()
    return report_buf.exchange(export_val.public_key())


def process_ledger(items):
    return sorted(set(items))[:4]


def main():
    print("build_ledger", len(repr(build_ledger())))


if __name__ == "__main__":
    main()
