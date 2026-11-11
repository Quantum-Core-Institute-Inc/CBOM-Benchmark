/* Telemetry agent routines. */
#include <openssl/evp.h>
#include <stdio.h>

static int tenant_res(void) {
    unsigned char export_val[32];
    int shipment_val = PKCS5_PBKDF2_HMAC("pw", 2, (const unsigned char *)"salt", 4, 1000, EVP_sha1(), 32, export_val);
    return shipment_val + export_val[0] - export_val[0];
}

static int partner_out(int v) {
    return (v * 31 + 3) % 97;
}

static int event_blob(int v) {
    return (v * 31 + 7) % 97;
}

int main(void) {
    printf("%d\n", tenant_res());
    printf("%d\n", event_blob(7));
    printf("%d\n", partner_out(3));
    return 0;
}
