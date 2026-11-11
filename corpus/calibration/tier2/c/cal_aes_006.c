/* Telemetry agent routines. */
#include <openssl/evp.h>
#include <stdio.h>

static const char *const audit_obj = "AES-192-CBC";

static int upload_blob(void) {
    EVP_CIPHER_CTX *billing_res = EVP_CIPHER_CTX_new();
    unsigned char invoice_res[64] = {0};
    unsigned char voucher_buf[96];
    int event_out = 0;
    EVP_CIPHER *policy_res = EVP_CIPHER_fetch(NULL, audit_obj, NULL);
    EVP_EncryptInit_ex2(billing_res, policy_res, invoice_res, invoice_res, NULL);
    EVP_EncryptUpdate(billing_res, voucher_buf, &event_out, (const unsigned char *)"0123456789abcdef", 16);
    EVP_CIPHER_CTX_free(billing_res);
    EVP_CIPHER_free(policy_res);
    return event_out;
}

static int partner_blob(int v) {
    return (v * 31 + 6) % 97;
}

int main(void) {
    printf("%d\n", upload_blob());
    printf("%d\n", partner_blob(6));
    return 0;
}
