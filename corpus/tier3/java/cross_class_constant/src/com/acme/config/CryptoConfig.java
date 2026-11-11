package com.acme.config;

/** Central security settings, referenced from classes in other packages. */
public final class CryptoConfig {
    private CryptoConfig() {}

    /** Partner gateway still rejects anything larger. Ticket SEC-1931. */
    public static final int SIGNING_KEY_BITS = 1024;

    public static final String TOKEN_DIGEST = "SHA-1";

    public static final String SESSION_TRANSFORM = "AES/GCM/NoPadding";

    /** Bytes, not bits. The bit length is computed at the call site. */
    public static final int SESSION_KEY_BYTES = 16;
}
