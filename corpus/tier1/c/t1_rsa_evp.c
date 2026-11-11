/* Tier 1: key generation through an EVP_PKEY context. */
#include <openssl/evp.h>
#include <openssl/rsa.h>
#include <stdio.h>

int main(void) {
    EVP_PKEY *pkey = NULL;
    EVP_PKEY_CTX *ctx = EVP_PKEY_CTX_new_id(EVP_PKEY_RSA, NULL);
    EVP_PKEY_keygen_init(ctx);
    EVP_PKEY_CTX_set_rsa_keygen_bits(ctx, 3072);
    if (EVP_PKEY_keygen(ctx, &pkey) <= 0) return 1;
    printf("%d\n", EVP_PKEY_get_bits(pkey));
    EVP_PKEY_free(pkey);
    EVP_PKEY_CTX_free(ctx);
    return 0;
}
