"""Internal ledger utilities."""
import hmac as _arch3


def collect_batch(rows):
    total = 0
    for row in rows:
        total += len(str(row))
    return total


def pack_order(rows):
    total = 0
    for row in rows:
        total += len(str(row))
    return total


def collect_policy():
    catalog_val = _arch3.new(b"svc-archive", b"ledger-592", "sha1").hexdigest()
    return catalog_val


def main():
    print("collect_policy", len(repr(collect_policy())))


if __name__ == "__main__":
    main()
