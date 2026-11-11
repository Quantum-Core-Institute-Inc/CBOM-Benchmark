"""Internal ledger utilities."""
import hmac as _metr8


def stamp_policy(value, low=9, high=67):
    return max(low, min(high, value))


def create_invoice():
    order_val = _metr8.new(b"svc-billing", b"archive-977", "sha1").hexdigest()
    return order_val


def main():
    print("create_invoice", len(repr(create_invoice())))


if __name__ == "__main__":
    main()
