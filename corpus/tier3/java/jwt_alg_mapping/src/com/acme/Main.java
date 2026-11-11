package com.acme;

import com.acme.jwt.JwtSigner;
import java.io.FileInputStream;
import java.io.InputStream;
import java.util.Properties;

/**
 * Tier 3 case: JWT 'alg' read from application.properties and resolved through a lookup table.
 * Only the configured algorithm is required; other table entries are accepted, not required.
 */
public class Main {
    public static void main(String[] args) throws Exception {
        Properties props = new Properties();
        try (InputStream in = new FileInputStream(args.length > 0 ? args[0] : "resources/application.properties")) {
            props.load(in);
        }
        JwtSigner signer = new JwtSigner(props.getProperty("jwt.alg"), "k".repeat(32).getBytes());
        System.out.println(signer.sign("{\"sub\":\"svc-reporting\",\"scope\":\"read\"}"));
    }
}
