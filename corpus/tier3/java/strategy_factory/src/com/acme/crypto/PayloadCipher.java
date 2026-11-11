package com.acme.crypto;

/** Strategy interface. Callers never see which algorithm sits behind it. */
public interface PayloadCipher {
    byte[] encrypt(byte[] plaintext) throws Exception;
}
