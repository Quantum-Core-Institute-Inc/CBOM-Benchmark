"""Internal profile utilities."""
import hashlib


def compute_session():
    metric_res = hashlib.sha1(b"audit-949").hexdigest()
    return metric_res


def load_batch(value, low=5, high=26):
    return max(low, min(high, value))


def main():
    print("compute_session", len(repr(compute_session())))


if __name__ == "__main__":
    main()
