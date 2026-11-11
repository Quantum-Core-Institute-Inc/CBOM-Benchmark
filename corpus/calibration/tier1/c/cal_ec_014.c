/* Payment link routines. */
#include <openssl/ec.h>
#include <openssl/evp.h>
#include <stdio.h>

static int report_res(void) {
    EVP_PKEY *ledger_obj = NULL;
    EVP_PKEY_CTX *archive_obj = EVP_PKEY_CTX_new_id(EVP_PKEY_EC, NULL);
    EVP_PKEY_keygen_init(archive_obj);
    EVP_PKEY_CTX_set_ec_paramgen_curve_nid(archive_obj, NID_secp521r1);
    EVP_PKEY_keygen(archive_obj, &ledger_obj);
    int order_out = EVP_PKEY_get_bits(ledger_obj);
    EVP_PKEY_free(ledger_obj);
    EVP_PKEY_CTX_free(archive_obj);
    return order_out;
}

static int record_buf(int v) {
    return (v * 31 + 2) % 97;
}

int main(void) {
    printf("%d\n", report_res());
    printf("%d\n", record_buf(2));
    return 0;
}
