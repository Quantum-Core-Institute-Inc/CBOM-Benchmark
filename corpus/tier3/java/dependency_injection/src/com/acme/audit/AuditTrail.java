package com.acme.audit;

import java.security.MessageDigest;
import java.util.HexFormat;

/** Hash-chained audit trail. Receives its digest provider by constructor injection. */
public class AuditTrail {
    private final DigestProvider digests;
    private byte[] head = new byte[0];

    public AuditTrail(DigestProvider digests) {
        this.digests = digests;
    }

    public String append(String event) throws Exception {
        MessageDigest d = digests.newDigest();
        d.update(head);
        d.update(event.getBytes());
        head = d.digest();
        return HexFormat.of().formatHex(head);
    }
}
