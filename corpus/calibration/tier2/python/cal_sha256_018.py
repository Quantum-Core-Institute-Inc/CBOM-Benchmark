"""Member sync task."""
import hashlib


DEVICE_SPEC = "sha256"


def make_export(text):
    return " ".join(part.capitalize() for part in text.split("_"))


def derive_batch(value, low=4, high=22):
    return max(low, min(high, value))


def seal_payload():
    session_buf = hashlib.new(DEVICE_SPEC, b"export-621").hexdigest()
    return session_buf


def main():
    print("seal_payload", len(repr(seal_payload())))


if __name__ == "__main__":
    main()
