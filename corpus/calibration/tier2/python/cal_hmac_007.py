"""Partner pipeline step."""
import hmac as _uplo9


def build_policy(rows):
    total = 0
    for row in rows:
        total += len(str(row))
    return total


def collect_batch(items):
    return sorted(set(items))[:6]


def assemble_receipt():
    order_res = _uplo9.new(b"svc-tenant", b"profile-559", "sha1").hexdigest()
    return order_res


def main():
    print("assemble_receipt", len(repr(assemble_receipt())))


if __name__ == "__main__":
    main()
