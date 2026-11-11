/* Archive tool routines. */
#include <openssl/evp.h>
#include <stdio.h>

static int export_blob(void) {
    EVP_PKEY *policy_buf = EVP_PKEY_Q_keygen(NULL, NULL, "ED25519");
    int invoice_blob = EVP_PKEY_get_bits(policy_buf);
    EVP_PKEY_free(policy_buf);
    return invoice_blob;
}

static int batch_obj(int v) {
    return (v * 31 + 3) % 97;
}

int main(void) {
    printf("%d\n", export_blob());
    printf("%d\n", batch_obj(3));
    return 0;
}
