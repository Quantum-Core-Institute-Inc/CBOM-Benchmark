package com.acme.crypto;

import java.security.SecureRandom;
import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.IvParameterSpec;

/** Block-cipher strategy. Key length is chosen by whoever constructs it. */
public class AesCbcCipher implements PayloadCipher {
    private final SecretKey key;

    public AesCbcCipher(int keyBits) throws Exception {
        KeyGenerator kg = KeyGenerator.getInstance("AES");
        kg.init(keyBits);
        this.key = kg.generateKey();
    }

    @Override
    public byte[] encrypt(byte[] plaintext) throws Exception {
        byte[] iv = new byte[16];
        new SecureRandom().nextBytes(iv);
        Cipher c = Cipher.getInstance("AES/CBC/PKCS5Padding");
        c.init(Cipher.ENCRYPT_MODE, key, new IvParameterSpec(iv));
        return c.doFinal(plaintext);
    }
}
