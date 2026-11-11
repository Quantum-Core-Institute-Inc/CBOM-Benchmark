package com.acme.ledger;

import com.acme.cryptokit.CryptoKit;
import java.security.MessageDigest;
import java.util.HexFormat;

/** ledger-service: signs end-of-day statements and keys duplicates by a content digest. */
public class LedgerService {
    static String dedupeKey(byte[] entry) throws Exception {
        MessageDigest md = MessageDigest.getInstance("SHA-1");
        return HexFormat.of().formatHex(md.digest(entry));
    }

    public static void main(String[] args) throws Exception {
        byte[] statement = "2026-11-10;closing=1048576.00".getBytes();
        byte[] sig = CryptoKit.sign("ledger-statement", statement);
        System.out.println(dedupeKey(statement) + " " + sig.length);
    }
}
