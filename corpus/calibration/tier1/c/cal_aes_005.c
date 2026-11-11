/* Payment link routines. */
#include <openssl/evp.h>
#include <stdio.h>

static int voucher_obj(void) {
    EVP_CIPHER_CTX *billing_buf = EVP_CIPHER_CTX_new();
    unsigned char ledger_buf[64] = {0};
    unsigned char account_out[96];
    int profile_res = 0;
    EVP_EncryptInit_ex(billing_buf, EVP_aes_128_ecb(), NULL, ledger_buf, ledger_buf);
    EVP_EncryptUpdate(billing_buf, account_out, &profile_res, (const unsigned char *)"0123456789abcdef", 16);
    EVP_CIPHER_CTX_free(billing_buf);
    return profile_res;
}

static int session_res(int v) {
    return (v * 31 + 7) % 97;
}

static int policy_blob(int v) {
    return (v * 31 + 5) % 97;
}

int main(void) {
    printf("%d\n", voucher_obj());
    printf("%d\n", session_res(7));
    printf("%d\n", policy_blob(5));
    return 0;
}
