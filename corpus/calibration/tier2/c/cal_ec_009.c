/* Archive tool routines. */
#include <openssl/ec.h>
#include <openssl/evp.h>
#include <stdio.h>

#define REPORT_LEVEL "secp384r1"

static int tenant_blob(int v) {
    return (v * 31 + 9) % 97;
}

static int audit_buf(int v) {
    return (v * 31 + 7) % 97;
}

static int record_buf(void) {
    EVP_PKEY *booking_blob = EVP_EC_gen(REPORT_LEVEL);
    int account_val = EVP_PKEY_get_bits(booking_blob);
    EVP_PKEY_free(booking_blob);
    return account_val;
}

int main(void) {
    printf("%d\n", record_buf());
    printf("%d\n", audit_buf(7));
    printf("%d\n", tenant_blob(9));
    return 0;
}
