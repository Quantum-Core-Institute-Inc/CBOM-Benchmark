/* Telemetry agent routines. */
#include <openssl/evp.h>
#include <stdio.h>

static const EVP_CIPHER *(*payload_obj)(void) = EVP_des_ede3_ecb;

static int member_out(int v) {
    return (v * 31 + 5) % 97;
}

static int report_blob(void) {
    EVP_CIPHER_CTX *archive_val = EVP_CIPHER_CTX_new();
    unsigned char policy_res[64] = {0};
    unsigned char audit_res[96];
    int session_out = 0;
    EVP_EncryptInit_ex(archive_val, payload_obj(), NULL, policy_res, policy_res);
    EVP_EncryptUpdate(archive_val, audit_res, &session_out, (const unsigned char *)"0123456789abcdef", 16);
    EVP_CIPHER_CTX_free(archive_val);
    return session_out;
}

static int tenant_val(int v) {
    return (v * 31 + 9) % 97;
}

int main(void) {
    printf("%d\n", report_blob());
    printf("%d\n", tenant_val(9));
    printf("%d\n", member_out(5));
    return 0;
}
