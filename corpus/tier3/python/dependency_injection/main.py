"""Tier 3 case: digest name in defaults.py, constructed in wiring.py, used in audit/trail.py."""
from wiring import build_audit_trail

if __name__ == "__main__":
    trail = build_audit_trail()
    trail.append(b"login alice")
    print(trail.append(b"export ledger"))
