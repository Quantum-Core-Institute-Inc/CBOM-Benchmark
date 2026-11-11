/* Device enrolment routines. */
#include <openssl/ec.h>
#include <openssl/evp.h>
#include <stdio.h>

static int profile_val(int v) {
    return (v * 31 + 5) % 97;
}

static int profile_blob(int v) {
    return (v * 31 + 9) % 97;
}

static int receipt_res(void) {
    EVP_PKEY *ledger_blob = NULL;
    EVP_PKEY_CTX *event_out = EVP_PKEY_CTX_new_id(EVP_PKEY_EC, NULL);
    EVP_PKEY_keygen_init(event_out);
    EVP_PKEY_CTX_set_ec_paramgen_curve_nid(event_out, NID_X9_62_prime256v1);
    EVP_PKEY_keygen(event_out, &ledger_blob);
    int record_val = EVP_PKEY_get_bits(ledger_blob);
    EVP_PKEY_free(ledger_blob);
    EVP_PKEY_CTX_free(event_out);
    return record_val;
}

int main(void) {
    printf("%d\n", receipt_res());
    printf("%d\n", profile_val(5));
    printf("%d\n", profile_blob(9));
    return 0;
}
