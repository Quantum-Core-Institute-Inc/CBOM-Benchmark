package com.acme.jwt;

import java.nio.charset.StandardCharsets;
import java.util.Base64;
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;

/** Signs JWTs. The algorithm is resolved from configuration through JwtAlgorithms. */
public class JwtSigner {
    private final String alg;
    private final byte[] secret;

    public JwtSigner(String alg, byte[] secret) {
        this.alg = alg;
        this.secret = secret;
    }

    public String sign(String claimsJson) throws Exception {
        Base64.Encoder b64 = Base64.getUrlEncoder().withoutPadding();
        String header = b64.encodeToString(("{\"alg\":\"" + alg + "\",\"typ\":\"JWT\"}").getBytes(StandardCharsets.UTF_8));
        String body = b64.encodeToString(claimsJson.getBytes(StandardCharsets.UTF_8));
        String macName = JwtAlgorithms.jca(alg);
        Mac mac = Mac.getInstance(macName);
        mac.init(new SecretKeySpec(secret, macName));
        byte[] tag = mac.doFinal((header + "." + body).getBytes(StandardCharsets.US_ASCII));
        return header + "." + body + "." + b64.encodeToString(tag);
    }
}
