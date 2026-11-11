"""Billing service. Signs invoices with a key sized for a legacy ERP integration."""
from seclib import keys


def invoice_signing_key():
    return keys.new_signing_key(bits=1024)
