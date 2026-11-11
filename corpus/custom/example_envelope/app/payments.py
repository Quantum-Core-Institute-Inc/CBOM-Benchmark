"""Payments export. Still on the legacy profile because the clearing partner hasn't upgraded."""
from envelope import seal


def export_batch(rows: list[bytes]) -> dict:
    return seal(b"\n".join(rows), profile="LEGACY_COMPAT")
