"""Firmware image verification with LMS (NIST SP 800-208, RFC 8554), in pure Python.

Verifiers like this get written in-house because the device side has to be small and the scheme is
only hashing. Parameter sets: LMS_SHA256_M32_H5 over LMOTS_SHA256_N32_W8. The signing half is here
for the self-test; in production the private state lives in an HSM, because a one-time key that
signs twice breaks the scheme.
"""
import hashlib
import os
import struct

LMS_SHA256_M32_H5 = 0x00000005
LMOTS_SHA256_N32_W8 = 0x00000004
N, W, P, LS, H = 32, 8, 34, 0, 5
D_PBLC, D_MESG, D_LEAF, D_INTR = b"\x80\x80", b"\x81\x81", b"\x82\x82", b"\x83\x83"


def _h(*parts: bytes) -> bytes:
    return hashlib.sha256(b"".join(parts)).digest()


def _u32(x: int) -> bytes:
    return struct.pack(">I", x)


def _u16(x: int) -> bytes:
    return struct.pack(">H", x)


def _digits(q_hash: bytes) -> bytes:
    """The message hash followed by its checksum, as base-256 digits (w = 8)."""
    checksum = sum(255 - b for b in q_hash) << LS
    return q_hash + _u16(checksum)


def _chain(ident: bytes, q: int, i: int, value: bytes, start: int, stop: int) -> bytes:
    for j in range(start, stop):
        value = _h(ident, _u32(q), _u16(i), bytes([j]), value)
    return value


def _ots_secret(seed: bytes, ident: bytes, q: int) -> list[bytes]:
    return [_h(ident, _u32(q), _u16(i), b"\xff", seed) for i in range(P)]


def _ots_public(ident: bytes, q: int, secret: list[bytes]) -> bytes:
    ends = [_chain(ident, q, i, secret[i], 0, 255) for i in range(P)]
    return _h(ident, _u32(q), D_PBLC, *ends)


def _ots_candidate(ident: bytes, q: int, message: bytes, ots_sig: bytes) -> bytes:
    """Recompute the one-time public key a signature commits to (RFC 8554, Algorithm 4b)."""
    if struct.unpack(">I", ots_sig[:4])[0] != LMOTS_SHA256_N32_W8:
        raise ValueError("unexpected LM-OTS parameter set")
    c, ys = ots_sig[4:4 + N], ots_sig[4 + N:]
    digits = _digits(_h(ident, _u32(q), D_MESG, c, message))
    ends = [_chain(ident, q, i, ys[i * N:(i + 1) * N], digits[i], 255) for i in range(P)]
    return _h(ident, _u32(q), D_PBLC, *ends)


def lms_keygen(seed: bytes, ident: bytes) -> tuple[bytes, list[bytes]]:
    """-> (public key, the whole tree). 2^5 = 32 one-time keys."""
    tree = [b""] * (2 << H)
    for q in range(1 << H):
        r = (1 << H) + q
        tree[r] = _h(ident, _u32(r), D_LEAF, _ots_public(ident, q, _ots_secret(seed, ident, q)))
    for r in range((1 << H) - 1, 0, -1):
        tree[r] = _h(ident, _u32(r), D_INTR, tree[2 * r], tree[2 * r + 1])
    return _u32(LMS_SHA256_M32_H5) + _u32(LMOTS_SHA256_N32_W8) + ident + tree[1], tree


def lms_sign(seed: bytes, ident: bytes, tree: list[bytes], q: int, message: bytes) -> bytes:
    """Sign with leaf q. The caller owns the state: q must never be used twice."""
    c = os.urandom(N)
    digits = _digits(_h(ident, _u32(q), D_MESG, c, message))
    secret = _ots_secret(seed, ident, q)
    ys = b"".join(_chain(ident, q, i, secret[i], 0, digits[i]) for i in range(P))
    path, r = b"", (1 << H) + q
    while r > 1:
        path += tree[r ^ 1]
        r >>= 1
    return _u32(q) + _u32(LMOTS_SHA256_N32_W8) + c + ys + _u32(LMS_SHA256_M32_H5) + path


def lms_verify(public_key: bytes, message: bytes, signature: bytes) -> bool:
    if struct.unpack(">II", public_key[:8]) != (LMS_SHA256_M32_H5, LMOTS_SHA256_N32_W8):
        return False
    ident, root = public_key[8:24], public_key[24:]
    q = struct.unpack(">I", signature[:4])[0]
    ots_len = 4 + N + P * N
    ots_sig, rest = signature[4:4 + ots_len], signature[4 + ots_len:]
    if q >= (1 << H) or struct.unpack(">I", rest[:4])[0] != LMS_SHA256_M32_H5 or len(rest) != 4 + H * N:
        return False
    try:
        candidate = _ots_candidate(ident, q, message, ots_sig)
    except ValueError:
        return False
    r = (1 << H) + q
    node = _h(ident, _u32(r), D_LEAF, candidate)
    for level in range(H):
        sibling = rest[4 + level * N:4 + (level + 1) * N]
        node = _h(ident, _u32(r >> 1), D_INTR, *((sibling, node) if r & 1 else (node, sibling)))
        r >>= 1
    return node == root


if __name__ == "__main__":
    seed, ident = os.urandom(N), os.urandom(16)
    public_key, tree = lms_keygen(seed, ident)
    image = b"bootloader-7.4.1.bin"
    signature = lms_sign(seed, ident, tree, 3, image)
    assert lms_verify(public_key, image, signature)
    assert not lms_verify(public_key, image + b"!", signature)
    print(f"lms public key {len(public_key)} bytes, signature {len(signature)} bytes: verified")
