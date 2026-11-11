"""Source for corpus/tier5/python/compiled/ledger_sync.pyc. NOT part of the scanned corpus.

Kept here so the compiled artifact can be rebuilt and audited. Do not point scanners at it.
"""
import hashlib
import hmac


def batch_id(rows: list[bytes]) -> str:
    return hashlib.sha1(b"".join(rows)).hexdigest()


def sign_callback(secret: bytes, body: bytes) -> str:
    return hmac.new(secret, body, "md5").hexdigest()


if __name__ == "__main__":
    print(batch_id([b"row-1", b"row-2"]), sign_callback(b"partner-secret", b"status=ok"))
