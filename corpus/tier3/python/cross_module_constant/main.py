"""Tier 3 case: algorithm names and key sizes defined in one module, used in others."""
from keys.issuer import issue_partner_key
from sessions.crypto import seal_cookie
from tokens.fingerprint import fingerprint

if __name__ == "__main__":
    print(issue_partner_key().key_size, fingerprint(b"tok-1"), len(seal_cookie(b"uid=42")))
