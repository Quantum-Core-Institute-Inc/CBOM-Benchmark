/* Tier 1: curve key generation by NID, then a digest-and-sign. */
#include <openssl/ec.h>
#include <openssl/evp.h>
#include <stdio.h>

int main(void) {
    EVP_PKEY *pkey = NULL;
    EVP_PKEY_CTX *ctx = EVP_PKEY_CTX_new_id(EVP_PKEY_EC, NULL);
    EVP_PKEY_keygen_init(ctx);
    EVP_PKEY_CTX_set_ec_paramgen_curve_nid(ctx, NID_X9_62_prime256v1);
    if (EVP_PKEY_keygen(ctx, &pkey) <= 0) return 1;

    unsigned char sig[128];
    size_t siglen = sizeof sig;
    EVP_MD_CTX *md = EVP_MD_CTX_new();
    EVP_DigestSignInit(md, NULL, EVP_sha256(), NULL, pkey);
    EVP_DigestSign(md, sig, &siglen, (const unsigned char *)"webhook-body", 12);
    printf("%zu\n", siglen);
    EVP_MD_CTX_free(md);
    EVP_PKEY_free(pkey);
    EVP_PKEY_CTX_free(ctx);
    return 0;
}
