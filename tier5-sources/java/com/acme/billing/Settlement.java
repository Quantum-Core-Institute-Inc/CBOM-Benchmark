package com.acme.billing;

import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.SecureRandom;
import java.security.Signature;
import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.IvParameterSpec;

/**
 * Source for corpus/tier5/java/compiled/billing-core.jar. NOT part of the scanned corpus.
 * Kept here so the compiled artifact can be rebuilt and audited. Do not point scanners at it.
 */
public class Settlement {
    public static void main(String[] args) throws Exception {
        KeyGenerator kg = KeyGenerator.getInstance("AES");
        kg.init(128);
        SecretKey key = kg.generateKey();
        byte[] iv = new byte[16];
        new SecureRandom().nextBytes(iv);
        Cipher c = Cipher.getInstance("AES/CBC/PKCS5Padding");
        c.init(Cipher.ENCRYPT_MODE, key, new IvParameterSpec(iv));
        byte[] sealed = c.doFinal("settlement-batch-0091".getBytes());

        KeyPairGenerator kpg = KeyPairGenerator.getInstance("RSA");
        kpg.initialize(1024);
        KeyPair kp = kpg.generateKeyPair();
        Signature s = Signature.getInstance("SHA1withRSA");
        s.initSign(kp.getPrivate());
        s.update(sealed);
        System.out.println(sealed.length + " " + s.sign().length);
    }
}
