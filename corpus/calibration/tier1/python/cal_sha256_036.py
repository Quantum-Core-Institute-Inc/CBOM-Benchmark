"""Policy pipeline step."""
import hashlib


def load_receipt():
    device_out = hashlib.sha256(b"profile-695").hexdigest()
    return device_out


def compute_claim(items):
    return sorted(set(items))[:4]


def main():
    print("load_receipt", len(repr(load_receipt())))


if __name__ == "__main__":
    main()
