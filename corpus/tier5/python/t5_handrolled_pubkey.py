"""Tier 5: public-key wrapping done with bare modular exponentiation over a hardcoded key."""

N = int(
    "a6efd81f1c16f4f245de712e71835b340f8366d30c6474587d42d68c16777869"
    "f8f215e00b58d7f091a35185985e90f20118a359e371e37909300fc66c47d238"
    "d396504a0adeabe305a9ecb075d70d249dfe5da4c7a5086f9c36d40ea29bb727"
    "66d496b570dfdec57a7e8dfd77b69ebede86e442ce4a31d54b4b6836c5bc4ee3",
    16,
)
E = 65537


def wrap(token: bytes) -> int:
    m = int.from_bytes(token, "big")
    if m >= N:
        raise ValueError("token too long")
    return pow(m, E, N)


if __name__ == "__main__":
    print(wrap(b"session-key-0042").bit_length())
