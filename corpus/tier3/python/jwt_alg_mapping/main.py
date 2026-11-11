"""Tier 3 case: JWT 'alg' read from an .ini file and resolved through a lookup table.

Only the configured algorithm is a required finding. The other table entries are
reachable by editing config, so reporting them is accepted but not required.
"""
from jwtlib.signer import sign

if __name__ == "__main__":
    print(sign({"sub": "svc-reporting", "scope": "read"}, b"k" * 32))
