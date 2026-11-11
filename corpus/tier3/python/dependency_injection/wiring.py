"""Composition root: builds the object graph and injects dependencies."""
import hashlib

import defaults
from audit.trail import AuditTrail


def build_audit_trail() -> AuditTrail:
    return AuditTrail(digest_factory=lambda: hashlib.new(defaults.AUDIT_DIGEST))
