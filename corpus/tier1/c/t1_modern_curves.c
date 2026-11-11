/* Tier 1: key types with no parameters to choose. */
#include <openssl/evp.h>
#include <stdio.h>

int main(void) {
    EVP_PKEY *signer = EVP_PKEY_Q_keygen(NULL, NULL, "ED25519");

    EVP_PKEY *agree = NULL;
    EVP_PKEY_CTX *ctx = EVP_PKEY_CTX_new_id(EVP_PKEY_X25519, NULL);
    EVP_PKEY_keygen_init(ctx);
    EVP_PKEY_keygen(ctx, &agree);

    printf("%d %d\n", EVP_PKEY_get_bits(signer), EVP_PKEY_get_bits(agree));
    EVP_PKEY_free(signer);
    EVP_PKEY_free(agree);
    EVP_PKEY_CTX_free(ctx);
    return 0;
}
