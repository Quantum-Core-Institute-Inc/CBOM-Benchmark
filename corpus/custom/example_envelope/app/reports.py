"""Monthly reports archive."""
from envelope import seal


def archive(report: bytes) -> dict:
    return seal(report, profile="STANDARD")
