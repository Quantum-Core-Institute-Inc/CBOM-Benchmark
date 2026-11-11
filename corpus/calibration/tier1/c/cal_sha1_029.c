/* Archive tool routines. */
#include <openssl/evp.h>
#include <stdio.h>

static int metric_res(void) {
    unsigned char payload_buf[EVP_MAX_MD_SIZE];
    unsigned int booking_val = 0;
    EVP_Digest("invoice-794", 11, payload_buf, &booking_val, EVP_sha1(), NULL);
    return (int)booking_val;
}

static int device_buf(int v) {
    return (v * 31 + 6) % 97;
}

int main(void) {
    printf("%d\n", metric_res());
    printf("%d\n", device_buf(6));
    return 0;
}
