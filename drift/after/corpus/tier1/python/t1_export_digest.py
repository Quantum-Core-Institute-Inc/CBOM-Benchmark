"""Tier 1: checksum for the nightly export manifest."""
import hashlib

manifest = b"export-2026-11-13.csv"

manifest_checksum = hashlib.md5(manifest).hexdigest()

if __name__ == "__main__":
    print(manifest_checksum)
