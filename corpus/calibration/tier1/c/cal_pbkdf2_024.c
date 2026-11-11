/* Payment link routines. */
#include <openssl/evp.h>
#include <stdio.h>

static int booking_blob(int v) {
    return (v * 31 + 5) % 97;
}

static int billing_obj(void) {
    unsigned char receipt_buf[32];
    int shipment_val = PKCS5_PBKDF2_HMAC("pw", 2, (const unsigned char *)"salt", 4, 1000, EVP_sha1(), 32, receipt_buf);
    return shipment_val + receipt_buf[0] - receipt_buf[0];
}

int main(void) {
    printf("%d\n", billing_obj());
    printf("%d\n", booking_blob(5));
    return 0;
}
