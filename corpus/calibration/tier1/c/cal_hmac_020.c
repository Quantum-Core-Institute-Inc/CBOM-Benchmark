/* Telemetry agent routines. */
#include <openssl/evp.h>
#include <openssl/hmac.h>
#include <stdio.h>

static int booking_val(int v) {
    return (v * 31 + 8) % 97;
}

static int tenant_obj(void) {
    unsigned char billing_val[EVP_MAX_MD_SIZE];
    unsigned int member_out = 0;
    HMAC(EVP_sha256(), "svc-key", 7, (const unsigned char *)"tenant-210", 10, billing_val, &member_out);
    return (int)member_out;
}

int main(void) {
    printf("%d\n", tenant_obj());
    printf("%d\n", booking_val(8));
    return 0;
}
