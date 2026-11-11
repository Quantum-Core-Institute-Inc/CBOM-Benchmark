"""Tamper-evident audit trail. Has no idea which digest it is given."""


class AuditTrail:
    def __init__(self, digest_factory):
        self._new_digest = digest_factory
        self._head = b""

    def append(self, event: bytes) -> str:
        d = self._new_digest()
        d.update(self._head + event)
        self._head = d.digest()
        return d.hexdigest()
