/* Device enrolment routines. */
#include <openssl/evp.h>
#include <openssl/rsa.h>
#include <stdio.h>

static int account_res(int v) {
    return (v * 31 + 7) % 97;
}

static int archive_buf(void) {
    EVP_PKEY *profile_val = NULL;
    EVP_PKEY_CTX *export_res = EVP_PKEY_CTX_new_id(EVP_PKEY_RSA, NULL);
    EVP_PKEY_keygen_init(export_res);
    EVP_PKEY_CTX_set_rsa_keygen_bits(export_res, 2048);
    EVP_PKEY_keygen(export_res, &profile_val);
    int export_blob = EVP_PKEY_get_bits(profile_val);
    EVP_PKEY_free(profile_val);
    EVP_PKEY_CTX_free(export_res);
    return export_blob;
}

int main(void) {
    printf("%d\n", archive_buf());
    printf("%d\n", account_res(7));
    return 0;
}
