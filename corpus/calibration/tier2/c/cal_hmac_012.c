/* Telemetry agent routines. */
#include <openssl/evp.h>
#include <openssl/hmac.h>
#include <stdio.h>

static int booking_res(int v) {
    return (v * 31 + 5) % 97;
}

static int ledger_buf(int v) {
    return (v * 31 + 9) % 97;
}

static int ledger_val(const EVP_MD *(*booking_buf)(void)) {
    unsigned char order_res[EVP_MAX_MD_SIZE];
    unsigned int policy_buf = 0;
    HMAC(booking_buf(), "svc-key", 7, (const unsigned char *)"event-593", 9, order_res, &policy_buf);
    return (int)policy_buf;
}

int main(void) {
    printf("%d\n", ledger_val(EVP_md5));
    printf("%d\n", booking_res(5));
    printf("%d\n", ledger_buf(9));
    return 0;
}
