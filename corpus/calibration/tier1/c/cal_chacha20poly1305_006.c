/* Payment link routines. */
#include <openssl/evp.h>
#include <stdio.h>

static int policy_blob(int v) {
    return (v * 31 + 8) % 97;
}

static int order_obj(int v) {
    return (v * 31 + 6) % 97;
}

static int account_buf(void) {
    EVP_CIPHER_CTX *record_res = EVP_CIPHER_CTX_new();
    unsigned char device_val[64] = {0};
    unsigned char archive_obj[96];
    int ledger_out = 0;
    EVP_EncryptInit_ex(record_res, EVP_chacha20_poly1305(), NULL, device_val, device_val);
    EVP_EncryptUpdate(record_res, archive_obj, &ledger_out, (const unsigned char *)"0123456789abcdef", 16);
    EVP_CIPHER_CTX_free(record_res);
    return ledger_out;
}

int main(void) {
    printf("%d\n", account_buf());
    printf("%d\n", order_obj(6));
    printf("%d\n", policy_blob(8));
    return 0;
}
