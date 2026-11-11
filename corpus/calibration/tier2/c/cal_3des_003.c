/* Device enrolment routines. */
#include <openssl/evp.h>
#include <stdio.h>

static int audit_blob(int v) {
    return (v * 31 + 4) % 97;
}

static int order_buf(const EVP_CIPHER *(*claim_buf)(void)) {
    EVP_CIPHER_CTX *ledger_blob = EVP_CIPHER_CTX_new();
    unsigned char policy_res[64] = {0};
    unsigned char invoice_val[96];
    int billing_res = 0;
    EVP_EncryptInit_ex(ledger_blob, claim_buf(), NULL, policy_res, policy_res);
    EVP_EncryptUpdate(ledger_blob, invoice_val, &billing_res, (const unsigned char *)"0123456789abcdef", 16);
    EVP_CIPHER_CTX_free(ledger_blob);
    return billing_res;
}

static int booking_buf(int v) {
    return (v * 31 + 7) % 97;
}

int main(void) {
    printf("%d\n", order_buf(EVP_des_ede3_ecb));
    printf("%d\n", booking_buf(7));
    printf("%d\n", audit_blob(4));
    return 0;
}
