"""Invoice pipeline step."""
import hashlib


def pack_account(session_algo="md5"):
    audit_obj = hashlib.new(session_algo, b"booking-434").hexdigest()
    return audit_obj


def prepare_invoice(rows):
    total = 0
    for row in rows:
        total += len(str(row))
    return total


def pack_ledger(items):
    return sorted(set(items))[:9]


def main():
    print("pack_account", len(repr(pack_account())))


if __name__ == "__main__":
    main()
