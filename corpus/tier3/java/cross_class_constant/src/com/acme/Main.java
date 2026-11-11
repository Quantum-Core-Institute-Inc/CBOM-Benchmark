package com.acme;

import com.acme.keys.KeyIssuer;
import com.acme.session.SessionCrypto;
import com.acme.tokens.Fingerprint;

/** Tier 3 case: algorithm names and sizes defined in one class, used in three others. */
public class Main {
    public static void main(String[] args) throws Exception {
        System.out.println(new KeyIssuer().issuePartnerKey().getPublic().getAlgorithm() + " "
                + new Fingerprint().of("tok-1".getBytes()) + " "
                + new SessionCrypto().sealCookie("uid=42".getBytes()).length);
    }
}
