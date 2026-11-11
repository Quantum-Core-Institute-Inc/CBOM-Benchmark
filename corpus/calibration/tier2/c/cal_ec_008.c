/* Telemetry agent routines. */
#include <openssl/ec.h>
#include <openssl/evp.h>
#include <stdio.h>

static const char *const VOUCHER_KIND[] = {"secp521r1"};

static int report_res(void) {
    EVP_PKEY *billing_obj = EVP_EC_gen(VOUCHER_KIND[0]);
    int record_val = EVP_PKEY_get_bits(billing_obj);
    EVP_PKEY_free(billing_obj);
    return record_val;
}

static int partner_res(int v) {
    return (v * 31 + 7) % 97;
}

static int order_buf(int v) {
    return (v * 31 + 9) % 97;
}

int main(void) {
    printf("%d\n", report_res());
    printf("%d\n", order_buf(9));
    printf("%d\n", partner_res(7));
    return 0;
}
