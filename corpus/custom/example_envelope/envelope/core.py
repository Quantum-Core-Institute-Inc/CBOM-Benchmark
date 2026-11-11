"""Profile dispatch: the only place that turns a profile name into concrete primitives."""
import os

from envelope import bulk_aead, bulk_chained, wrap_agreement, wrap_transport
from envelope.profiles import PROFILES


def seal(data: bytes, profile: str = "STANDARD") -> dict:
    p = PROFILES[profile]
    content_key = os.urandom(p["bulk_bytes"])
    if p["wrap"] == "rsa-oaep":
        wrapped = wrap_transport.wrap(content_key, p["wrap_bits"])
    else:
        wrapped = wrap_agreement.wrap(content_key, p["wrap_curve"])
    body = bulk_chained.encrypt(content_key, data) if p["bulk"] == "cbc" else bulk_aead.encrypt(content_key, data)
    return {"profile": profile, "wrapped_key": wrapped, "body": body}
