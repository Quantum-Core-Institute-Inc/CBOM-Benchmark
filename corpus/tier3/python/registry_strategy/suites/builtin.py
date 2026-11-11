"""Built-in suites. Keys are supplied by the caller, so key size is decided elsewhere."""
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

from suites.registry import register


@register("archive")
class ArchiveSuite:
    def seal(self, key: bytes, data: bytes, iv: bytes) -> bytes:
        enc = Cipher(algorithms.AES(key), modes.CBC(iv)).encryptor()
        return enc.update(data) + enc.finalize()


@register("stream")
class StreamSuite:
    def seal(self, key: bytes, data: bytes, nonce: bytes) -> bytes:
        return ChaCha20Poly1305(key).encrypt(nonce, data, None)
