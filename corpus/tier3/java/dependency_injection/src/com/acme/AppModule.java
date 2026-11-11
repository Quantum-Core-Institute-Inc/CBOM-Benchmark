package com.acme;

import com.acme.audit.AuditTrail;
import com.acme.audit.DigestProvider;

/** Hand-rolled composition root (what a DI container does, minus the annotations). */
public final class AppModule {
    private AppModule() {}

    static final String AUDIT_DIGEST = "MD5";

    static AuditTrail auditTrail() {
        return new AuditTrail(new DigestProvider(AUDIT_DIGEST));
    }
}
