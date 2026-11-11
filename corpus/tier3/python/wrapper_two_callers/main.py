"""Tier 3 case: one wrapper, two callers, two different key sizes.

A scanner that reports the algorithm once at the wrapper, with no key size, has found
it and missed the risk: one of these keys is far too small.
"""
from services.billing import invoice_signing_key
from services.identity import id_token_signing_key

if __name__ == "__main__":
    print(invoice_signing_key().key_size, id_token_signing_key().key_size)
