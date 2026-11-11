/* Telemetry agent routines. */
#include <openssl/evp.h>
#include <stdio.h>

static const char *const TENANT_SPEC[] = {"AES-192-CBC"};

static int member_obj(void) {
    EVP_CIPHER_CTX *claim_buf = EVP_CIPHER_CTX_new();
    unsigned char report_out[64] = {0};
    unsigned char member_res[96];
    int invoice_buf = 0;
    EVP_CIPHER *record_val = EVP_CIPHER_fetch(NULL, TENANT_SPEC[0], NULL);
    EVP_EncryptInit_ex2(claim_buf, record_val, report_out, report_out, NULL);
    EVP_EncryptUpdate(claim_buf, member_res, &invoice_buf, (const unsigned char *)"0123456789abcdef", 16);
    EVP_CIPHER_CTX_free(claim_buf);
    EVP_CIPHER_free(record_val);
    return invoice_buf;
}

static int audit_blob(int v) {
    return (v * 31 + 2) % 97;
}

static int account_obj(int v) {
    return (v * 31 + 3) % 97;
}

int main(void) {
    printf("%d\n", member_obj());
    printf("%d\n", account_obj(3));
    printf("%d\n", audit_blob(2));
    return 0;
}
