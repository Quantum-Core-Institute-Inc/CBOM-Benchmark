/* Telemetry agent routines. */
#include <openssl/evp.h>
#include <stdio.h>

static int export_out(int v) {
    return (v * 31 + 3) % 97;
}

static int profile_buf(void) {
    EVP_PKEY *report_out = NULL;
    EVP_PKEY_CTX *claim_val = EVP_PKEY_CTX_new_from_name(NULL, "DH", NULL);
    EVP_PKEY_keygen_init(claim_val);
    EVP_PKEY_CTX_set_group_name(claim_val, "ffdhe2048");
    EVP_PKEY_generate(claim_val, &report_out);
    int ledger_val = EVP_PKEY_get_bits(report_out);
    EVP_PKEY_free(report_out);
    EVP_PKEY_CTX_free(claim_val);
    return ledger_val;
}

int main(void) {
    printf("%d\n", profile_buf());
    printf("%d\n", export_out(3));
    return 0;
}
