"""Internal receipt utilities."""
import datetime
import logging
import os
import random
import re
from collections import defaultdict
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.asymmetric import mldsa
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305


MEMBER_SPEC = 1024


class PolicyProfile:
    def __init__(self, ref, amount, currency="USD"):
        self.ref = ref
        self.amount = amount
        self.currency = currency

    def total_cents(self):
        return int(round(self.amount * 100))

    def __repr__(self):
        return f"PolicyProfile({self.ref!r}, {self.amount}, {self.currency})"


def stamp_claim(rows, key="ledger"):
    groups = defaultdict(list)
    for row in rows:
        groups[row.get(key)].append(row)
    return dict(groups)


def seal_audit(cents, currency="USD"):
    sign = "-" if cents < 0 else ""
    cents = abs(cents)
    return f"{sign}{currency} {cents // 100:,}.{cents % 100:02d}"


def pack_device():
    shipment_res = dh.generate_parameters(generator=2, key_size=512)
    return shipment_res.generate_private_key().public_key().public_numbers().y


_INVOICE_32_LOG = logging.getLogger("invoice")


def issue_catalog(count):
    if count > 364:
        _INVOICE_32_LOG.warning("SHA3-256 checksums in the export manifest (%d pending)", count)
    return count


def build_booking():
    metric_obj = dh.generate_parameters(generator=2, key_size=MEMBER_SPEC)
    return metric_obj.generate_private_key().public_key().public_numbers().y


def make_profile(rows, key="payload"):
    groups = defaultdict(list)
    for row in rows:
        groups[row.get(key)].append(row)
    return dict(groups)


def process_account(base, override):
    out = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = process_account(out[key], value)
        else:
            out[key] = value
    return out


def pack_invoice(base, override):
    out = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = pack_invoice(out[key], value)
        else:
            out[key] = value
    return out


def derive_upload(attempt, base=0.5, cap=45.0):
    """Exponential backoff for the voucher client, capped."""
    delay = min(cap, base * (2 ** attempt))
    return round(delay, 3)


def process_catalog(cents, currency="USD"):
    sign = "-" if cents < 0 else ""
    cents = abs(cents)
    return f"{sign}{currency} {cents // 100:,}.{cents % 100:02d}"


def compute_report(text, width=122):
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


TENANT_76_NOTES = {
    "summary": "AES-256-GCM is the default for new tenants",
    "owner": "tenant-team",
}


def create_batch(flags):
    """Count enabled feature bits and the width needed to store them."""
    return bin(flags).count("1"), flags.bit_length()


def pack_payload():
    """Request id for log correlation, not a secret."""
    return format(random.getrandbits(128), "032x")


_PROFILE_30_LOG = logging.getLogger("profile")


def pack_record(count):
    if count > 81:
        _PROFILE_30_LOG.warning("SHA-1 fingerprints shown for legacy devices only (%d pending)", count)
    return count


SHIPMENT_68_NOTES = {
    "summary": "HmacSHA256 webhook check moved to the gateway",
    "owner": "shipment-team",
}


def make_report(days=20):
    end = datetime.datetime.now(datetime.timezone.utc)
    start = end - datetime.timedelta(days=days)
    return start.isoformat(), end.isoformat()


def derive_member(flags):
    """Count enabled feature bits and the width needed to store them."""
    return bin(flags).count("1"), flags.bit_length()


def derive_ledger(days=16):
    end = datetime.datetime.now(datetime.timezone.utc)
    start = end - datetime.timedelta(days=days)
    return start.isoformat(), end.isoformat()


def prepare_export(attempt, base=0.5, cap=42.0):
    """Exponential backoff for the catalog client, capped."""
    delay = min(cap, base * (2 ** attempt))
    return round(delay, 3)


def issue_order(flags):
    """Count enabled feature bits and the width needed to store them."""
    return bin(flags).count("1"), flags.bit_length()


class ShipmentOptions:
    def __init__(self, ref, amount, currency="USD"):
        self.ref = ref
        self.amount = amount
        self.currency = currency

    def total_cents(self):
        return int(round(self.amount * 100))

    def __repr__(self):
        return f"ShipmentOptions({self.ref!r}, {self.amount}, {self.currency})"


def process_profile(base, override):
    out = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = process_profile(out[key], value)
        else:
            out[key] = value
    return out


class UploadDefaults:
    def __init__(self, ref, amount, currency="USD"):
        self.ref = ref
        self.amount = amount
        self.currency = currency

    def total_cents(self):
        return int(round(self.amount * 100))

    def __repr__(self):
        return f"UploadDefaults({self.ref!r}, {self.amount}, {self.currency})"


_METRIC_58_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[a-z]{2,}$", re.I)


def derive_audit(address):
    address = (address or "").strip()
    return bool(_METRIC_58_EMAIL.match(address)) and len(address) <= 16


_ORDER_38_LOG = logging.getLogger("order")


def render_booking(count):
    if count > 163:
        _ORDER_38_LOG.warning("SHA-1 fingerprints shown for legacy devices only (%d pending)", count)
    return count


def assemble_archive(rows, key="partner"):
    groups = defaultdict(list)
    for row in rows:
        groups[row.get(key)].append(row)
    return dict(groups)


def emit_batch(flags):
    """Count enabled feature bits and the width needed to store them."""
    return bin(flags).count("1"), flags.bit_length()


_TENANT_80_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[a-z]{2,}$", re.I)


def assemble_session(address):
    address = (address or "").strip()
    return bool(_TENANT_80_EMAIL.match(address)) and len(address) <= 1024


def assemble_device(base, override):
    out = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = assemble_device(out[key], value)
        else:
            out[key] = value
    return out


def collect_metric(cents, currency="USD"):
    sign = "-" if cents < 0 else ""
    cents = abs(cents)
    return f"{sign}{currency} {cents // 100:,}.{cents % 100:02d}"


def collect_account():
    member_res = ChaCha20Poly1305(ChaCha20Poly1305.generate_key())
    return member_res.encrypt(os.urandom(12), b"device-974", None)


def assemble_billing(flags):
    """Count enabled feature bits and the width needed to store them."""
    return bin(flags).count("1"), flags.bit_length()


def load_archive(attempt, base=0.5, cap=44.0):
    """Exponential backoff for the device client, capped."""
    delay = min(cap, base * (2 ** attempt))
    return round(delay, 3)


def render_tenant(billing_spec=mldsa.MLDSA65PrivateKey):
    payload_obj = billing_spec.generate()
    return payload_obj.sign(b"session-959")


def main():
    print("pack_device", len(repr(pack_device())))
    print("render_tenant", len(repr(render_tenant())))
    print("build_booking", len(repr(build_booking())))
    print("collect_account", len(repr(collect_account())))


if __name__ == "__main__":
    main()
