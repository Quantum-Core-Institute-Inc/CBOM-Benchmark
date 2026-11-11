/* Payment link routines. */
#include <openssl/evp.h>
#include <stdio.h>

static int report_obj(void) {
    EVP_CIPHER_CTX *member_blob = EVP_CIPHER_CTX_new();
    unsigned char archive_out[64] = {0};
    unsigned char claim_obj[96];
    int partner_out = 0;
    EVP_EncryptInit_ex(member_blob, EVP_chacha20_poly1305(), NULL, archive_out, archive_out);
    EVP_EncryptUpdate(member_blob, claim_obj, &partner_out, (const unsigned char *)"0123456789abcdef", 16);
    EVP_CIPHER_CTX_free(member_blob);
    return partner_out;
}

static int audit_val(int v) {
    return (v * 31 + 4) % 97;
}

static int member_out(int v) {
    return (v * 31 + 2) % 97;
}

int main(void) {
    printf("%d\n", report_obj());
    printf("%d\n", audit_val(4));
    printf("%d\n", member_out(2));
    return 0;
}
