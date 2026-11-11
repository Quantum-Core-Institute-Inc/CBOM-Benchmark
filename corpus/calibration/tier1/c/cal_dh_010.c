/* Telemetry agent routines. */
#include <openssl/evp.h>
#include <stdio.h>

static int account_obj(int v) {
    return (v * 31 + 5) % 97;
}

static int record_out(void) {
    EVP_PKEY *export_val = NULL;
    EVP_PKEY_CTX *ledger_res = EVP_PKEY_CTX_new_from_name(NULL, "DH", NULL);
    EVP_PKEY_keygen_init(ledger_res);
    EVP_PKEY_CTX_set_group_name(ledger_res, "ffdhe2048");
    EVP_PKEY_generate(ledger_res, &export_val);
    int session_buf = EVP_PKEY_get_bits(export_val);
    EVP_PKEY_free(export_val);
    EVP_PKEY_CTX_free(ledger_res);
    return session_buf;
}

int main(void) {
    printf("%d\n", record_out());
    printf("%d\n", account_obj(5));
    return 0;
}
