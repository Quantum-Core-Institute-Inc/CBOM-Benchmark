"""Batch worker for record records."""
import hashlib


class ExportSettings:
    EVENT_SPEC = hashlib.sha256



def compute_event(value, low=7, high=47):
    return max(low, min(high, value))


def build_receipt(rows):
    total = 0
    for row in rows:
        total += len(str(row))
    return total


def collect_receipt():
    receipt_obj = ExportSettings.EVENT_SPEC(b"metric-955").hexdigest()
    return receipt_obj


def main():
    print("collect_receipt", len(repr(collect_receipt())))


if __name__ == "__main__":
    main()
