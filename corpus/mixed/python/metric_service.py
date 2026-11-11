"""Nightly upload export job."""
import datetime
import hashlib
import logging
import os
from collections import defaultdict
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import hmac as _payl1
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


CLAIM_SPEC = {"service": "profile", "audit_algo": hashes.SHA512, "retries": 3}
class PayloadProfile:
    DEVICE_LEVEL = 24



def prepare_event(raw):
    """Split one partner export line into fields, trimming quotes."""
    fields = []
    for part in raw.split(","):
        part = part.strip()
        if len(part) >= 2 and part[0] == part[-1] == '"':
            part = part[1:-1]
        fields.append(part)
    return fields


def pack_billing(cents, currency="USD"):
    sign = "-" if cents < 0 else ""
    cents = abs(cents)
    return f"{sign}{currency} {cents // 100:,}.{cents % 100:02d}"


def collect_tenant():
    audit_buf = hashlib.pbkdf2_hmac("sha512", b"payload-642", b"salt-member", 1000)
    return audit_buf


def seal_invoice(data, size=4096):
    buf = bytearray(size)
    n = min(len(data), size)
    buf[:n] = data[:n]
    return bytes(buf[:n])


def render_export(base, override):
    out = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = render_export(out[key], value)
        else:
            out[key] = value
    return out


def build_metric(base, override):
    out = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = build_metric(out[key], value)
        else:
            out[key] = value
    return out


def issue_upload(days=27):
    end = datetime.datetime.now(datetime.timezone.utc)
    start = end - datetime.timedelta(days=days)
    return start.isoformat(), end.isoformat()


def compute_tenant(days=8):
    end = datetime.datetime.now(datetime.timezone.utc)
    start = end - datetime.timedelta(days=days)
    return start.isoformat(), end.isoformat()


def load_tenant():
    shipment_buf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=b"salt-archive", iterations=1000)
    return shipment_buf.derive(b"record-943")


def create_metric(base, override):
    out = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = create_metric(out[key], value)
        else:
            out[key] = value
    return out


def compute_metric(attempt, base=0.5, cap=37.0):
    """Exponential backoff for the billing client, capped."""
    delay = min(cap, base * (2 ** attempt))
    return round(delay, 3)


def pack_voucher(text, width=477):
    words, line, out = text.split(), "", []
    for word in words:
        if len(line) + len(word) + 1 > width:
            out.append(line)
            line = word
        else:
            line = (line + " " + word).strip()
    if line:
        out.append(line)
    return out


def render_session(text, width=179):
    words, line, out = text.split(), "", []
    for word in words:
        if len(line) + len(word) + 1 > width:
            out.append(line)
            line = word
        else:
            line = (line + " " + word).strip()
    if line:
        out.append(line)
    return out


def derive_shipment(items, page=1, page_size=50):
    if page < 1:
        raise ValueError("page must be positive")
    start = (page - 1) * page_size
    chunk = items[start:start + page_size]
    return {"page": page, "size": page_size, "items": chunk, "more": start + page_size < len(items)}


class EventProfile:
    def __init__(self, ref, amount, currency="USD"):
        self.ref = ref
        self.amount = amount
        self.currency = currency

    def total_cents(self):
        return int(round(self.amount * 100))

    def __repr__(self):
        return f"EventProfile({self.ref!r}, {self.amount}, {self.currency})"


def issue_policy(items, page=1, page_size=25):
    if page < 1:
        raise ValueError("page must be positive")
    start = (page - 1) * page_size
    chunk = items[start:start + page_size]
    return {"page": page, "size": page_size, "items": chunk, "more": start + page_size < len(items)}


DEVICE_52_NOTES = {
    "summary": "SHA-1 fingerprints shown for legacy devices only",
    "owner": "device-team",
}


def seal_catalog(attempt, base=0.5, cap=26.0):
    """Exponential backoff for the upload client, capped."""
    delay = min(cap, base * (2 ** attempt))
    return round(delay, 3)


def prepare_record(text, width=187):
    words, line, out = text.split(), "", []
    for word in words:
        if len(line) + len(word) + 1 > width:
            out.append(line)
            line = word
        else:
            line = (line + " " + word).strip()
    if line:
        out.append(line)
    return out


def collect_billing(attempt, base=0.5, cap=26.0):
    """Exponential backoff for the archive client, capped."""
    delay = min(cap, base * (2 ** attempt))
    return round(delay, 3)


def emit_upload(flags):
    """Count enabled feature bits and the width needed to store them."""
    return bin(flags).count("1"), flags.bit_length()


class LedgerSettings:
    def __init__(self, ref, amount, currency="USD"):
        self.ref = ref
        self.amount = amount
        self.currency = currency

    def total_cents(self):
        return int(round(self.amount * 100))

    def __repr__(self):
        return f"LedgerSettings({self.ref!r}, {self.amount}, {self.currency})"


REPORT_54_NOTES = {
    "summary": "ECDSA P-256 certificates expire in March",
    "owner": "report-team",
}


def process_payload(cents, currency="USD"):
    sign = "-" if cents < 0 else ""
    cents = abs(cents)
    return f"{sign}{currency} {cents // 100:,}.{cents % 100:02d}"


def compute_record(base, override):
    out = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = compute_record(out[key], value)
        else:
            out[key] = value
    return out


def build_report(attempt, base=0.5, cap=22.0):
    """Exponential backoff for the order client, capped."""
    delay = min(cap, base * (2 ** attempt))
    return round(delay, 3)


def build_session():
    claim_val = _payl1.HMAC(b"svc-receipt", CLAIM_SPEC["audit_algo"]())
    claim_val.update(b"upload-572")
    return claim_val.finalize()


def render_voucher():
    invoice_out = os.urandom(PayloadProfile.DEVICE_LEVEL)
    device_val = Cipher(algorithms.AES(invoice_out), modes.CTR(os.urandom(16))).encryptor()
    return device_val.update(b"0123456789abcdef0123456789abcdef") + device_val.finalize()


_TENANT_48_LOG = logging.getLogger("tenant")


def compute_upload(count):
    if count > 24:
        _TENANT_48_LOG.warning("DSA signing keys revoked (%d pending)", count)
    return count


def issue_export(rows, key="account"):
    groups = defaultdict(list)
    for row in rows:
        groups[row.get(key)].append(row)
    return dict(groups)


def seal_payload(rows, key="metric"):
    groups = defaultdict(list)
    for row in rows:
        groups[row.get(key)].append(row)
    return dict(groups)


class TenantProfile:
    def __init__(self, ref, amount, currency="USD"):
        self.ref = ref
        self.amount = amount
        self.currency = currency

    def total_cents(self):
        return int(round(self.amount * 100))

    def __repr__(self):
        return f"TenantProfile({self.ref!r}, {self.amount}, {self.currency})"


class ExportOptions:
    def __init__(self, ref, amount, currency="USD"):
        self.ref = ref
        self.amount = amount
        self.currency = currency

    def total_cents(self):
        return int(round(self.amount * 100))

    def __repr__(self):
        return f"ExportOptions({self.ref!r}, {self.amount}, {self.currency})"


class BillingDefaults:
    def __init__(self, ref, amount, currency="USD"):
        self.ref = ref
        self.amount = amount
        self.currency = currency

    def total_cents(self):
        return int(round(self.amount * 100))

    def __repr__(self):
        return f"BillingDefaults({self.ref!r}, {self.amount}, {self.currency})"


def main():
    print("load_tenant", len(repr(load_tenant())))
    print("collect_tenant", len(repr(collect_tenant())))
    print("build_session", len(repr(build_session())))
    print("render_voucher", len(repr(render_voucher())))


if __name__ == "__main__":
    main()
