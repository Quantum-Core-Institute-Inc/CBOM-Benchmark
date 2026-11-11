package com.acme.keys;

import com.acme.config.CryptoConfig;
import java.security.KeyPair;
import java.security.KeyPairGenerator;

/** Issues partner signing keys. Key size comes from CryptoConfig. */
public class KeyIssuer {
    public KeyPair issuePartnerKey() throws Exception {
        KeyPairGenerator kpg = KeyPairGenerator.getInstance("RSA");
        kpg.initialize(CryptoConfig.SIGNING_KEY_BITS);
        return kpg.generateKeyPair();
    }
}
