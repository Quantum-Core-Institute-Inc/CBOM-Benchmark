package com.acme.jwt;

import java.util.Map;

/** JWS 'alg' header values mapped to JCA Mac names. */
public final class JwtAlgorithms {
    private JwtAlgorithms() {}

    private static final Map<String, String> JCA = Map.of(
            "HS256", "HmacSHA256",
            "HS384", "HmacSHA384",
            "HS512", "HmacSHA512");

    public static String jca(String jwsAlg) {
        String name = JCA.get(jwsAlg);
        if (name == null) {
            throw new IllegalArgumentException("unsupported alg " + jwsAlg);
        }
        return name;
    }
}
