"""Tier 2: MAC built through functools.partial with a string digest name."""
import functools
import hmac

legacy_signer = functools.partial(hmac.new, digestmod="sha1")


def sign_callback(secret: bytes, body: bytes) -> str:
    return legacy_signer(secret, body).hexdigest()


if __name__ == "__main__":
    print(sign_callback(b"partner-secret", b"status=ok"))
