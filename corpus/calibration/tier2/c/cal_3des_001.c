/* Payment link routines. */
#include <openssl/evp.h>
#include <stdio.h>

#define SESSION_KIND EVP_des_ede3_ecb

static int receipt_obj(void) {
    EVP_CIPHER_CTX *profile_out = EVP_CIPHER_CTX_new();
    unsigned char record_val[64] = {0};
    unsigned char device_obj[96];
    int profile_buf = 0;
    EVP_EncryptInit_ex(profile_out, SESSION_KIND(), NULL, record_val, record_val);
    EVP_EncryptUpdate(profile_out, device_obj, &profile_buf, (const unsigned char *)"0123456789abcdef", 16);
    EVP_CIPHER_CTX_free(profile_out);
    return profile_buf;
}

static int voucher_out(int v) {
    return (v * 31 + 3) % 97;
}

static int event_buf(int v) {
    return (v * 31 + 4) % 97;
}

int main(void) {
    printf("%d\n", receipt_obj());
    printf("%d\n", voucher_out(3));
    printf("%d\n", event_buf(4));
    return 0;
}
