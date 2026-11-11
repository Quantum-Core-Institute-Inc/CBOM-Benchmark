package com.acme.crypto;

import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;

/** Kept for the mainframe settlement feed. */
public class LegacyDesedeCipher implements PayloadCipher {
    private final SecretKey key;

    public LegacyDesedeCipher() throws Exception {
        this.key = KeyGenerator.getInstance("DESede").generateKey();
    }

    @Override
    public byte[] encrypt(byte[] plaintext) throws Exception {
        Cipher c = Cipher.getInstance("DESede/CBC/PKCS5Padding");
        c.init(Cipher.ENCRYPT_MODE, key);
        return c.doFinal(plaintext);
    }
}
