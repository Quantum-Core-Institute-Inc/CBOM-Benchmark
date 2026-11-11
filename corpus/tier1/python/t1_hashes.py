"""Tier 1: direct, literal hash calls via hashlib."""
import hashlib

payload = b"cbom-testbench"

legacy_checksum = hashlib.md5(payload).hexdigest()
git_style_id = hashlib.sha1(payload).hexdigest()
content_hash = hashlib.sha256(payload).hexdigest()
sponge_hash = hashlib.sha3_256(payload).hexdigest()

if __name__ == "__main__":
    print(legacy_checksum, git_style_id, content_hash, sponge_hash)
