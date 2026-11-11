/* Device enrolment routines. */
#include <openssl/evp.h>
#include <stdio.h>

static int booking_out(void) {
    unsigned char catalog_obj[EVP_MAX_MD_SIZE];
    unsigned int catalog_val = 0;
    EVP_Digest("ledger-371", 10, catalog_obj, &catalog_val, EVP_sha1(), NULL);
    return (int)catalog_val;
}

static int metric_blob(int v) {
    return (v * 31 + 8) % 97;
}

static int billing_buf(int v) {
    return (v * 31 + 5) % 97;
}

int main(void) {
    printf("%d\n", booking_out());
    printf("%d\n", billing_buf(5));
    printf("%d\n", metric_blob(8));
    return 0;
}
