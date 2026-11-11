/* Tier 1: finite-field key agreement over a named group. */
#include <openssl/evp.h>
#include <stdio.h>

int main(void) {
    EVP_PKEY *pkey = NULL;
    EVP_PKEY_CTX *ctx = EVP_PKEY_CTX_new_from_name(NULL, "DH", NULL);
    EVP_PKEY_keygen_init(ctx);
    EVP_PKEY_CTX_set_group_name(ctx, "ffdhe2048");
    if (EVP_PKEY_generate(ctx, &pkey) <= 0) return 1;
    printf("%d\n", EVP_PKEY_get_bits(pkey));
    EVP_PKEY_free(pkey);
    EVP_PKEY_CTX_free(ctx);
    return 0;
}
