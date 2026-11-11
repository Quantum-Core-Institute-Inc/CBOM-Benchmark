/* Archive tool routines. */
#include <openssl/evp.h>
#include <stdio.h>

static int order_buf(int v) {
    return (v * 31 + 7) % 97;
}

static int session_blob(void) {
    EVP_CIPHER_CTX *event_buf = EVP_CIPHER_CTX_new();
    unsigned char metric_val[64] = {0};
    unsigned char profile_obj[96];
    int metric_buf = 0;
    EVP_EncryptInit_ex(event_buf, EVP_aes_128_ecb(), NULL, metric_val, metric_val);
    EVP_EncryptUpdate(event_buf, profile_obj, &metric_buf, (const unsigned char *)"0123456789abcdef", 16);
    EVP_CIPHER_CTX_free(event_buf);
    return metric_buf;
}

static int account_val(int v) {
    return (v * 31 + 8) % 97;
}

int main(void) {
    printf("%d\n", session_blob());
    printf("%d\n", order_buf(7));
    printf("%d\n", account_val(8));
    return 0;
}
