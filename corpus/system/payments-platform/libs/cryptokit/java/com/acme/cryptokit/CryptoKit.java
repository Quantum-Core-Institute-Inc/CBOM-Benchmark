package com.acme.cryptokit;

import java.nio.file.Files;
import java.nio.file.Path;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.Signature;
import java.security.spec.ECGenParameterSpec;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/** The platform's crypto wrapper. Callers name a profile; the profile names the algorithm. */
public final class CryptoKit {
    private CryptoKit() {}

    private static String field(String profile, String key) throws Exception {
        String doc = Files.readString(Path.of(System.getProperty("crypto.profiles", "config/crypto-profiles.json")));
        Matcher block = Pattern.compile("\"" + Pattern.quote(profile) + "\"\\s*:\\s*\\{([^}]*)\\}").matcher(doc);
        if (!block.find()) throw new IllegalArgumentException(profile);
        Matcher m = Pattern.compile("\"" + key + "\"\\s*:\\s*\"([^\"]+)\"").matcher(block.group(1));
        if (!m.find()) throw new IllegalArgumentException(profile + "." + key);
        return m.group(1);
    }

    /** Signs with the profile's signature algorithm over a key on the profile's curve. */
    public static byte[] sign(String profile, byte[] data) throws Exception {
        KeyPairGenerator kpg = KeyPairGenerator.getInstance("EC");
        kpg.initialize(new ECGenParameterSpec(field(profile, "curve")));
        KeyPair kp = kpg.generateKeyPair();
        Signature s = Signature.getInstance(field(profile, "signature"));
        s.initSign(kp.getPrivate());
        s.update(data);
        return s.sign();
    }
}
