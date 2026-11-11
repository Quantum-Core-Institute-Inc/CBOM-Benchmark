"""Tier 5: a keystream generator implemented in plain Python. No crypto library is imported."""


def _schedule(key: bytes) -> list[int]:
    s = list(range(256))
    j = 0
    for i in range(256):
        j = (j + s[i] + key[i % len(key)]) % 256
        s[i], s[j] = s[j], s[i]
    return s


def transform(key: bytes, data: bytes) -> bytes:
    s = _schedule(key)
    i = j = 0
    out = bytearray()
    for byte in data:
        i = (i + 1) % 256
        j = (j + s[i]) % 256
        s[i], s[j] = s[j], s[i]
        out.append(byte ^ s[(s[i] + s[j]) % 256])
    return bytes(out)


if __name__ == "__main__":
    print(transform(b"partner-feed-key", b"ACCT=4471;AMT=120.00").hex())
