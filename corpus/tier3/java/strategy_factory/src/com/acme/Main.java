package com.acme;

import com.acme.crypto.CipherFactory;
import com.acme.crypto.PayloadCipher;

/** Tier 3 case: strategy interface + factory; profile from a system property. Both strategies reachable. */
public class Main {
    public static void main(String[] args) throws Exception {
        String profile = System.getProperty("storage.profile", "legacy");
        PayloadCipher cipher = CipherFactory.forProfile(profile);
        PayloadCipher other = CipherFactory.forProfile(profile.equals("legacy") ? "modern" : "legacy");
        System.out.println(cipher.encrypt("settlement-batch".getBytes()).length + " "
                + other.encrypt("settlement-batch".getBytes()).length);
    }
}
