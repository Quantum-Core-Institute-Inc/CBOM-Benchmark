"""Blob storage. Picks an encryption suite by name; never touches a cipher directly."""
import os

import suites.builtin  # noqa: F401  (import registers the suites)
from suites.registry import get

SUITE_NAME = os.environ.get("STORAGE_SUITE", "archive")
ARCHIVE_KEY = os.urandom(32)
STREAM_KEY = os.urandom(32)


def store(data: bytes) -> bytes:
    suite = get(SUITE_NAME)
    if SUITE_NAME == "archive":
        return suite.seal(ARCHIVE_KEY, data, os.urandom(16))
    return suite.seal(STREAM_KEY, data, os.urandom(12))
