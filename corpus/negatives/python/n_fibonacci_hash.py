"""Negative control: an open-addressing integer set using Fibonacci (multiplicative) hashing.

0x9E3779B9 is 2^32 divided by the golden ratio. It shows up in hash tables, PRNG seeding
and, separately, as the round constant of a well-known block cipher. Here it only picks
a bucket. Nothing in this file is cryptographic.
"""

_GOLDEN = 0x9E3779B9


class IntSet:
    def __init__(self, bits: int = 6):
        self.bits = bits
        self.slots = [None] * (1 << bits)
        self.count = 0

    def _slot(self, key: int) -> int:
        return ((key * _GOLDEN) & 0xFFFFFFFF) >> (32 - self.bits)

    def _grow(self):
        old = [k for k in self.slots if k is not None]
        self.bits += 1
        self.slots = [None] * (1 << self.bits)
        self.count = 0
        for k in old:
            self.add(k)

    def add(self, key: int) -> None:
        if (self.count + 1) * 4 > len(self.slots) * 3:
            self._grow()
        i = self._slot(key)
        while self.slots[i] is not None:
            if self.slots[i] == key:
                return
            i = (i + 1) % len(self.slots)
        self.slots[i] = key
        self.count += 1

    def __contains__(self, key: int) -> bool:
        i = self._slot(key)
        while self.slots[i] is not None:
            if self.slots[i] == key:
                return True
            i = (i + 1) % len(self.slots)
        return False


if __name__ == "__main__":
    s = IntSet()
    for n in range(0, 500, 7):
        s.add(n)
    print(len(s.slots), 343 in s, 344 in s)
