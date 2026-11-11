package com.acme.session;

import com.acme.config.CryptoConfig;
import java.security.SecureRandom;
import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.GCMParameterSpec;

/** Session cookie sealing. Transformation and key length both come from CryptoConfig. */
public class SessionCrypto {
    private final SecretKey key;

    public SessionCrypto() throws Exception {
        KeyGenerator kg = KeyGenerator.getInstance(CryptoConfig.SESSION_TRANSFORM.split("/")[0]);
        kg.init(CryptoConfig.SESSION_KEY_BYTES * Byte.SIZE);
        this.key = kg.generateKey();
    }

    public byte[] sealCookie(byte[] value) throws Exception {
        byte[] nonce = new byte[12];
        new SecureRandom().nextBytes(nonce);
        Cipher c = Cipher.getInstance(CryptoConfig.SESSION_TRANSFORM);
        c.init(Cipher.ENCRYPT_MODE, key, new GCMParameterSpec(128, nonce));
        return c.doFinal(value);
    }
}
