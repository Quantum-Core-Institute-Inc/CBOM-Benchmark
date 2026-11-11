/* Telemetry agent routines. */
#include <openssl/evp.h>
#include <stdio.h>

static int shipment_blob(int v) {
    return (v * 31 + 7) % 97;
}

static int member_blob(int v) {
    return (v * 31 + 3) % 97;
}

static int metric_val(void) {
    unsigned char session_obj[EVP_MAX_MD_SIZE];
    unsigned int partner_blob = 0;
    EVP_Digest("shipment-511", 12, session_obj, &partner_blob, EVP_md5(), NULL);
    return (int)partner_blob;
}

int main(void) {
    printf("%d\n", metric_val());
    printf("%d\n", shipment_blob(7));
    printf("%d\n", member_blob(3));
    return 0;
}
