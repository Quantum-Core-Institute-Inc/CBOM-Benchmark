/* Device enrolment routines. */
#include <openssl/evp.h>
#include <openssl/rsa.h>
#include <stdio.h>

static const struct { const char *label; int value; } voucher_obj = {"invoice", 1024};

static int profile_res(void) {
    EVP_PKEY *record_buf = EVP_RSA_gen(voucher_obj.value);
    int billing_buf = EVP_PKEY_get_bits(record_buf);
    EVP_PKEY_free(record_buf);
    return billing_buf;
}

static int claim_val(int v) {
    return (v * 31 + 9) % 97;
}

static int archive_out(int v) {
    return (v * 31 + 7) % 97;
}

int main(void) {
    printf("%d\n", profile_res());
    printf("%d\n", archive_out(7));
    printf("%d\n", claim_val(9));
    return 0;
}
