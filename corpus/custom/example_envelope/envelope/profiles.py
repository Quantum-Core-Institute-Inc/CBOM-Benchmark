"""Named protection profiles. Security owns this table; application teams only know the names."""

PROFILES = {
    "LEGACY_COMPAT": {"wrap": "rsa-oaep", "wrap_bits": 2048, "bulk": "cbc", "bulk_bytes": 16},
    "STANDARD": {"wrap": "ecdh-es", "wrap_curve": "p256", "bulk": "gcm", "bulk_bytes": 32},
}
