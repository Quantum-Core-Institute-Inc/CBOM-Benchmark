"""Negative control: IBAN validation by the ISO 13616 mod-97 rule.

Modular exponentiation with pow(base, exp, mod) is the same call a hand-rolled public-key
routine uses. Here it only folds a long digit string into a check remainder.
"""


def is_valid_iban(iban: str) -> bool:
    s = iban.replace(" ", "").upper()
    if len(s) < 15 or not s.isalnum():
        return False
    digits = "".join(str(int(ch, 36)) for ch in s[4:] + s[:4])
    rem = 0
    for start in range(0, len(digits), 9):
        chunk = digits[start:start + 9]
        rem = (rem * pow(10, len(chunk), 97) + int(chunk)) % 97
    return rem == 1


if __name__ == "__main__":
    print(is_valid_iban("GB82 WEST 1234 5698 7654 32"), is_valid_iban("GB82 WEST 1234 5698 7654 33"))
