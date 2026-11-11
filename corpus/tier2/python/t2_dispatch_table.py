"""Tier 2: hash constructors stored in a dispatch table and selected at runtime."""
import hashlib
import sys

CHECKSUMS = {
    "legacy": hashlib.md5,
    "default": hashlib.sha256,
}


def checksum(data: bytes, profile: str = "default") -> str:
    return CHECKSUMS[profile](data).hexdigest()


if __name__ == "__main__":
    profile = sys.argv[1] if len(sys.argv) > 1 else "legacy"
    print(checksum(b"export.csv", profile))
