"""Identity service. Signs ID tokens."""
from seclib import keys


def id_token_signing_key():
    return keys.new_signing_key(bits=3072)
