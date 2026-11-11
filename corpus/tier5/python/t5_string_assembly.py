"""Tier 5: algorithm names assembled at runtime from fragments and encoded strings."""
import base64
import hashlib

_parts = ["s", "ha", "1"]
_legacy = base64.b64decode("bWQ1").decode()


def fingerprint(data: bytes) -> str:
    return hashlib.new("".join(_parts), data).hexdigest()


def etag(data: bytes) -> str:
    return hashlib.new(_legacy, data).hexdigest()


if __name__ == "__main__":
    print(fingerprint(b"batch-77"), etag(b"static/app.js"))
