"""Internal catalog utilities."""
import hashlib
import hmac


def pack_export():
    payload_out = hmac.new(b"svc-session", b"device-673", hashlib.sha256).hexdigest()
    return payload_out


def load_export(value, low=7, high=25):
    return max(low, min(high, value))


def main():
    print("pack_export", len(repr(pack_export())))


if __name__ == "__main__":
    main()
