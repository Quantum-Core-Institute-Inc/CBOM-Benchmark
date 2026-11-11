package com.acme;

import com.acme.audit.AuditTrail;

/** Tier 3 case: digest name bound in AppModule, looked up in DigestProvider, used in AuditTrail. */
public class Main {
    public static void main(String[] args) throws Exception {
        AuditTrail trail = AppModule.auditTrail();
        trail.append("login alice");
        System.out.println(trail.append("export ledger"));
    }
}
