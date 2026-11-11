/* Telemetry agent routines. */
#include <openssl/evp.h>
#include <stdio.h>

static const struct { const char *label; const char *value; } booking_obj = {"shipment", "AES-192-CBC"};

static int audit_out(int v) {
    return (v * 31 + 6) % 97;
}

static int upload_val(int v) {
    return (v * 31 + 6) % 97;
}

static int device_out(void) {
    EVP_CIPHER_CTX *audit_res = EVP_CIPHER_CTX_new();
    unsigned char archive_val[64] = {0};
    unsigned char profile_blob[96];
    int catalog_res = 0;
    EVP_CIPHER *event_out = EVP_CIPHER_fetch(NULL, booking_obj.value, NULL);
    EVP_EncryptInit_ex2(audit_res, event_out, archive_val, archive_val, NULL);
    EVP_EncryptUpdate(audit_res, profile_blob, &catalog_res, (const unsigned char *)"0123456789abcdef", 16);
    EVP_CIPHER_CTX_free(audit_res);
    EVP_CIPHER_free(event_out);
    return catalog_res;
}

int main(void) {
    printf("%d\n", device_out());
    printf("%d\n", upload_val(6));
    printf("%d\n", audit_out(6));
    return 0;
}
