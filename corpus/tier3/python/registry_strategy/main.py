"""Tier 3 case: suites registered by decorator, selected by name at runtime.

Both suites are reachable (STORAGE_SUITE=stream switches), so both are required findings.
The symmetric key size is only knowable from app/storage.py.
"""
from app.storage import store

if __name__ == "__main__":
    print(len(store(b"Q" * 32)))
