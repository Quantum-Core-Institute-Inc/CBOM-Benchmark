"""Tier 2: hash algorithm chosen by a module-level constant passed to hashlib.new()."""
import hashlib

HASH_ALG = "sha1"


def fingerprint(blob: bytes) -> str:
    h = hashlib.new(HASH_ALG)
    h.update(blob)
    return h.hexdigest()


if __name__ == "__main__":
    print(fingerprint(b"artifact-v3.tar.gz"))
