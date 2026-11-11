/* Payment link routines. */
#include <openssl/evp.h>
#include <stdio.h>

static int invoice_obj(int v) {
    return (v * 31 + 6) % 97;
}

static int device_val(int v) {
    return (v * 31 + 3) % 97;
}

static int account_buf(void) {
    EVP_PKEY *partner_val = EVP_PKEY_Q_keygen(NULL, NULL, "ED25519");
    int upload_buf = EVP_PKEY_get_bits(partner_val);
    EVP_PKEY_free(partner_val);
    return upload_buf;
}

int main(void) {
    printf("%d\n", account_buf());
    printf("%d\n", device_val(3));
    printf("%d\n", invoice_obj(6));
    return 0;
}
