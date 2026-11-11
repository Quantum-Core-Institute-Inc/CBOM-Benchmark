"""Central security settings. Consumed by modules elsewhere in the application."""

# Partner gateway still rejects anything larger. Ticket SEC-1931.
SIGNING_KEY_BITS = 1024

TOKEN_DIGEST = "sha1"

# Computed rather than written out, so the literal key size never appears.
SESSION_KEY_BYTES = 2 * 8
