"""PQC case: parameter set chosen by a module constant and resolved with getattr."""
from cryptography.hazmat.primitives.asymmetric import mlkem

LEVEL = 1024


def new_recipient():
    cls = getattr(mlkem, f"MLKEM{LEVEL}PrivateKey")
    return cls.generate()


if __name__ == "__main__":
    ss, ct = new_recipient().public_key().encapsulate()
    print(len(ct))
