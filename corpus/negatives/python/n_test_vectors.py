"""Negative control: published digest test vectors stored as plain constants.

These are reference values for documentation. Nothing here computes a digest.
"""

KNOWN_ANSWERS = [
    # (algorithm name, input, expected hex)
    ("MD5", "", "d41d8cd98f00b204e9800998ecf8427e"),
    ("SHA-1", "abc", "a9993e364706816aba3e25717850c26c9cd0d89d"),
    ("SHA-256", "abc", "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"),
]


class RSABadgeRenderer:
    """Draws the little 'RSA' badge next to legacy certificates in the UI."""

    def __init__(self, colour: str = "amber"):
        self.colour = colour

    def html(self) -> str:
        return f'<span class="badge badge-{self.colour}">RSA</span>'


def describe_vectors() -> str:
    return "\n".join(f"{alg}({msg!r}) = {digest}" for alg, msg, digest in KNOWN_ANSWERS)


if __name__ == "__main__":
    print(describe_vectors())
    print(RSABadgeRenderer().html())
