/* Telemetry agent routines. */
#include <openssl/evp.h>
#include <stdio.h>

static int receipt_out(int v) {
    return (v * 31 + 8) % 97;
}

static int event_val(void) {
    unsigned char payload_blob[EVP_MAX_MD_SIZE];
    unsigned int catalog_blob = 0;
    EVP_Digest("claim-868", 9, payload_blob, &catalog_blob, EVP_sha3_256(), NULL);
    return (int)catalog_blob;
}

static int upload_buf(int v) {
    return (v * 31 + 7) % 97;
}

int main(void) {
    printf("%d\n", event_val());
    printf("%d\n", receipt_out(8));
    printf("%d\n", upload_buf(7));
    return 0;
}
