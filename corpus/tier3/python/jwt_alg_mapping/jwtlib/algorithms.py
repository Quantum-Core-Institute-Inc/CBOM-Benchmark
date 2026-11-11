"""JWS 'alg' header values mapped to digest constructors."""
import hashlib

DIGESTS = {
    "HS256": hashlib.sha256,
    "HS384": hashlib.sha384,
    "HS512": hashlib.sha512,
}
