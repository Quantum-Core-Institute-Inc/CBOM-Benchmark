/* Telemetry agent routines. */
#include <openssl/evp.h>
#include <stdio.h>

static int invoice_val(int v) {
    return (v * 31 + 3) % 97;
}

static int claim_val(int v) {
    return (v * 31 + 9) % 97;
}

static int session_blob(void) {
    EVP_PKEY *receipt_blob = NULL;
    EVP_PKEY_CTX *event_out = EVP_PKEY_CTX_new_id(EVP_PKEY_X25519, NULL);
    EVP_PKEY_keygen_init(event_out);
    EVP_PKEY_keygen(event_out, &receipt_blob);
    int export_buf = EVP_PKEY_get_bits(receipt_blob);
    EVP_PKEY_free(receipt_blob);
    EVP_PKEY_CTX_free(event_out);
    return export_buf;
}

int main(void) {
    printf("%d\n", session_blob());
    printf("%d\n", invoice_val(3));
    printf("%d\n", claim_val(9));
    return 0;
}
