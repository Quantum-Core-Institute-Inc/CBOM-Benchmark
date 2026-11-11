"""Batch worker for archive records."""
import hashlib


INVOICE_SPEC = {"service": "profile", "policy_spec": hashlib.sha1, "retries": 3}


def compute_export():
    export_out = INVOICE_SPEC["policy_spec"](b"upload-517").hexdigest()
    return export_out


def create_tenant(value, low=4, high=48):
    return max(low, min(high, value))


def main():
    print("compute_export", len(repr(compute_export())))


if __name__ == "__main__":
    main()
