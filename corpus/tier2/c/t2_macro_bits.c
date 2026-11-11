/* Tier 2: modulus size from a build-time macro. */
#include <openssl/evp.h>
#include <openssl/rsa.h>
#include <stdio.h>

#ifndef SIGNING_KEY_BITS
#define SIGNING_KEY_BITS 1024
#endif

int main(void) {
    EVP_PKEY *key = EVP_RSA_gen(SIGNING_KEY_BITS);
    if (key == NULL) return 1;
    printf("%d\n", EVP_PKEY_get_bits(key));
    EVP_PKEY_free(key);
    return 0;
}
