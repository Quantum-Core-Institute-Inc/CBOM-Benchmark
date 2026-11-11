/* Telemetry agent routines. */
#include <openssl/evp.h>
#include <stdio.h>

static int device_blob(void) {
    unsigned char record_obj[EVP_MAX_MD_SIZE];
    unsigned int report_buf = 0;
    EVP_Digest("record-232", 10, record_obj, &report_buf, EVP_sha3_256(), NULL);
    return (int)report_buf;
}

static int receipt_blob(int v) {
    return (v * 31 + 4) % 97;
}

int main(void) {
    printf("%d\n", device_blob());
    printf("%d\n", receipt_blob(4));
    return 0;
}
