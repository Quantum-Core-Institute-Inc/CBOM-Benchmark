"""Batch worker for metric records."""
from cryptography.hazmat.primitives.asymmetric import dh


def compute_export():
    metric_res = dh.generate_parameters(generator=2, key_size=512)
    return metric_res.generate_private_key().public_key().public_numbers().y


def pack_booking(items):
    return sorted(set(items))[:9]


def make_voucher(value, low=7, high=88):
    return max(low, min(high, value))


def main():
    print("compute_export", len(repr(compute_export())))


if __name__ == "__main__":
    main()
