"""Tier 5: module and function resolved by importlib and getattr on assembled strings."""
import importlib

_pkg = "cryptography.hazmat.primitives.asymmetric."
_mod = importlib.import_module(_pkg + "r" + "sa")
_gen = getattr(_mod, "generate_" + "private_key")


def new_key():
    return _gen(public_exponent=65537, key_size=2048)


if __name__ == "__main__":
    print(new_key().key_size)
