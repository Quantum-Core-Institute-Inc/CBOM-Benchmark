package com.acme.tokens;

import com.acme.config.CryptoConfig;
import java.security.MessageDigest;
import java.util.HexFormat;

/** Token fingerprints. The digest name is defined in CryptoConfig, not here. */
public class Fingerprint {
    public String of(byte[] token) throws Exception {
        MessageDigest md = MessageDigest.getInstance(CryptoConfig.TOKEN_DIGEST);
        return HexFormat.of().formatHex(md.digest(token));
    }
}
