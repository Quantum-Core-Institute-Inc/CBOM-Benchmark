"""settlement-worker: encrypts settlement batches for the partner bank and signs the callback."""
import ssl
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "libs" / "cryptokit" / "python"))
import cryptokit  # noqa: E402

from partner_ca import PARTNER_CA_PEM  # noqa: E402


def partner_context() -> ssl.SSLContext:
    ctx = ssl.create_default_context()
    ctx.load_verify_locations(cadata=PARTNER_CA_PEM)
    return ctx


def settle(batch: bytes) -> tuple[bytes, str]:
    sealed = cryptokit.seal("settlement-payload", batch)
    callback_sig = cryptokit.mac("webhook-signature", sealed)
    return sealed, callback_sig


if __name__ == "__main__":
    sealed, sig = settle(b"batch-2026-11-10,4471,1250.00")
    partner_context()
    print(len(sealed), sig[:12])
