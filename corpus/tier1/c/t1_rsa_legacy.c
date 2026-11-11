/* Tier 1: the pre-3.0 low-level key API, still common in older code. */
#define OPENSSL_SUPPRESS_DEPRECATED
#include <openssl/bn.h>
#include <openssl/rsa.h>
#include <stdio.h>

int main(void) {
    RSA *rsa = RSA_new();
    BIGNUM *e = BN_new();
    BN_set_word(e, RSA_F4);
    if (!RSA_generate_key_ex(rsa, 1024, e, NULL)) return 1;
    printf("%d\n", RSA_bits(rsa));
    RSA_free(rsa);
    BN_free(e);
    return 0;
}
