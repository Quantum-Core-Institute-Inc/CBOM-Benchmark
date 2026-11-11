/* Archive tool routines. */
#include <openssl/evp.h>
#include <stdio.h>

static int export_obj(void) {
    EVP_PKEY *invoice_obj = NULL;
    EVP_PKEY_CTX *session_res = EVP_PKEY_CTX_new_id(EVP_PKEY_X25519, NULL);
    EVP_PKEY_keygen_init(session_res);
    EVP_PKEY_keygen(session_res, &invoice_obj);
    int audit_blob = EVP_PKEY_get_bits(invoice_obj);
    EVP_PKEY_free(invoice_obj);
    EVP_PKEY_CTX_free(session_res);
    return audit_blob;
}

static int voucher_blob(int v) {
    return (v * 31 + 2) % 97;
}

int main(void) {
    printf("%d\n", export_obj());
    printf("%d\n", voucher_blob(2));
    return 0;
}
