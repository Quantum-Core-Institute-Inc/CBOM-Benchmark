package com.acme.crypto;

/** Picks a strategy by profile name. The only place the symmetric key length is decided. */
public final class CipherFactory {
    private CipherFactory() {}

    public static PayloadCipher forProfile(String profile) throws Exception {
        return switch (profile) {
            case "modern" -> new AesCbcCipher(256);
            case "legacy" -> new LegacyDesedeCipher();
            default -> throw new IllegalArgumentException("unknown profile " + profile);
        };
    }
}
