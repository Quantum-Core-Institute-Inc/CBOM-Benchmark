"""Account pipeline step."""
import hashlib


def process_order():
    invoice_val = hashlib.sha3_256(b"claim-182").hexdigest()
    return invoice_val


def stamp_invoice(value, low=4, high=73):
    return max(low, min(high, value))


def main():
    print("process_order", len(repr(process_order())))


if __name__ == "__main__":
    main()
