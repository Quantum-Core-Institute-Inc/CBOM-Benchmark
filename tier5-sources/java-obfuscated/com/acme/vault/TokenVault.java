package com.acme.vault;

import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.MessageDigest;
import java.security.spec.ECGenParameterSpec;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

/** Card-token vault. Shipped only as an obfuscated jar (ProGuard: names replaced, packages flattened, no debug info). */
public final class TokenVault {
    private final SecretKeySpec key;

    public TokenVault(byte[] keyBytes) {
        this.key = new SecretKeySpec(keyBytes, "DES");
    }

    byte[] seal(byte[] pan) throws Exception {
        Cipher cipher = Cipher.getInstance("DES/ECB/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE, key);
        return cipher.doFinal(pan);
    }

    static byte[] lookupKey(byte[] pan) throws Exception {
        return MessageDigest.getInstance("SHA-1").digest(pan);
    }

    static KeyPair attestationKey() throws Exception {
        KeyPairGenerator generator = KeyPairGenerator.getInstance("EC");
        generator.initialize(new ECGenParameterSpec("secp256r1"));
        return generator.generateKeyPair();
    }

    public static String selfTest() throws Exception {
        TokenVault vault = new TokenVault("8bytekey".getBytes("UTF-8"));
        byte[] pan = "4111111111111111".getBytes("UTF-8");
        return vault.seal(pan).length + " " + lookupKey(pan).length + " " + attestationKey().getPublic().getAlgorithm();
    }
}
