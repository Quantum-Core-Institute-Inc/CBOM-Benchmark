package com.acme.audit;

import java.security.MessageDigest;

/** Hands out digests by name. The name is injected; this class never decides it. */
public class DigestProvider {
    private final String algorithm;

    public DigestProvider(String algorithm) {
        this.algorithm = algorithm;
    }

    public MessageDigest newDigest() throws Exception {
        return MessageDigest.getInstance(algorithm);
    }
}
