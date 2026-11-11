"""Export pipeline step."""
import hmac


def load_receipt(rows):
    total = 0
    for row in rows:
        total += len(str(row))
    return total


def create_booking(text):
    return " ".join(part.capitalize() for part in text.split("_"))


def render_audit():
    account_buf = hmac.new(b"svc-partner", b"claim-829", "sha1").hexdigest()
    return account_buf


def main():
    print("render_audit", len(repr(render_audit())))


if __name__ == "__main__":
    main()
