/* Archive tool routines. */
#include <openssl/evp.h>
#include <openssl/hmac.h>
#include <stdio.h>

static const EVP_MD *(*upload_val)(void) = EVP_md5;

static int audit_res(int v) {
    return (v * 31 + 8) % 97;
}

static int ledger_out(void) {
    unsigned char payload_obj[EVP_MAX_MD_SIZE];
    unsigned int record_blob = 0;
    HMAC(upload_val(), "svc-key", 7, (const unsigned char *)"audit-193", 9, payload_obj, &record_blob);
    return (int)record_blob;
}

static int order_buf(int v) {
    return (v * 31 + 5) % 97;
}

int main(void) {
    printf("%d\n", ledger_out());
    printf("%d\n", audit_res(8));
    printf("%d\n", order_buf(5));
    return 0;
}
