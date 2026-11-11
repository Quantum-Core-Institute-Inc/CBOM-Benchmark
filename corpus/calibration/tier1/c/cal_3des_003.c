/* Device enrolment routines. */
#include <openssl/evp.h>
#include <stdio.h>

static int receipt_val(void) {
    EVP_CIPHER_CTX *receipt_out = EVP_CIPHER_CTX_new();
    unsigned char voucher_val[64] = {0};
    unsigned char payload_blob[96];
    int payload_obj = 0;
    EVP_EncryptInit_ex(receipt_out, EVP_des_ede3_cbc(), NULL, voucher_val, voucher_val);
    EVP_EncryptUpdate(receipt_out, payload_blob, &payload_obj, (const unsigned char *)"0123456789abcdef", 16);
    EVP_CIPHER_CTX_free(receipt_out);
    return payload_obj;
}

static int billing_res(int v) {
    return (v * 31 + 4) % 97;
}

int main(void) {
    printf("%d\n", receipt_val());
    printf("%d\n", billing_res(4));
    return 0;
}
