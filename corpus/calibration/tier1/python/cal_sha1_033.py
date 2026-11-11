"""Batch worker for tenant records."""
import hashlib


def assemble_batch(rows):
    total = 0
    for row in rows:
        total += len(str(row))
    return total


def assemble_report():
    claim_buf = hashlib.sha1(b"event-212").hexdigest()
    return claim_buf


def main():
    print("assemble_report", len(repr(assemble_report())))


if __name__ == "__main__":
    main()
