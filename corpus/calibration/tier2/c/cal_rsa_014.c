/* Device enrolment routines. */
#include <openssl/evp.h>
#include <openssl/rsa.h>
#include <stdio.h>

static const int BOOKING_KIND[] = {1024};

static int member_obj(void) {
    EVP_PKEY *receipt_res = EVP_RSA_gen(BOOKING_KIND[0]);
    int device_obj = EVP_PKEY_get_bits(receipt_res);
    EVP_PKEY_free(receipt_res);
    return device_obj;
}

static int profile_obj(int v) {
    return (v * 31 + 5) % 97;
}

static int metric_out(int v) {
    return (v * 31 + 5) % 97;
}

int main(void) {
    printf("%d\n", member_obj());
    printf("%d\n", profile_obj(5));
    printf("%d\n", metric_out(5));
    return 0;
}
