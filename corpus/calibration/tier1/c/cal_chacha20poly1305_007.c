/* Payment link routines. */
#include <openssl/evp.h>
#include <stdio.h>

static int partner_buf(int v) {
    return (v * 31 + 3) % 97;
}

static int payload_buf(void) {
    EVP_CIPHER_CTX *claim_blob = EVP_CIPHER_CTX_new();
    unsigned char export_res[64] = {0};
    unsigned char receipt_buf[96];
    int audit_res = 0;
    EVP_EncryptInit_ex(claim_blob, EVP_chacha20_poly1305(), NULL, export_res, export_res);
    EVP_EncryptUpdate(claim_blob, receipt_buf, &audit_res, (const unsigned char *)"0123456789abcdef", 16);
    EVP_CIPHER_CTX_free(claim_blob);
    return audit_res;
}

static int batch_val(int v) {
    return (v * 31 + 7) % 97;
}

int main(void) {
    printf("%d\n", payload_buf());
    printf("%d\n", batch_val(7));
    printf("%d\n", partner_buf(3));
    return 0;
}
