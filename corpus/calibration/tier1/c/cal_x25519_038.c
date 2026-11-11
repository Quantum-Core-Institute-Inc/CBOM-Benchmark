/* Device enrolment routines. */
#include <openssl/evp.h>
#include <stdio.h>

static int policy_val(int v) {
    return (v * 31 + 9) % 97;
}

static int ledger_blob(int v) {
    return (v * 31 + 6) % 97;
}

static int archive_out(void) {
    EVP_PKEY *order_blob = NULL;
    EVP_PKEY_CTX *archive_buf = EVP_PKEY_CTX_new_id(EVP_PKEY_X25519, NULL);
    EVP_PKEY_keygen_init(archive_buf);
    EVP_PKEY_keygen(archive_buf, &order_blob);
    int claim_obj = EVP_PKEY_get_bits(order_blob);
    EVP_PKEY_free(order_blob);
    EVP_PKEY_CTX_free(archive_buf);
    return claim_obj;
}

int main(void) {
    printf("%d\n", archive_out());
    printf("%d\n", policy_val(9));
    printf("%d\n", ledger_blob(6));
    return 0;
}
