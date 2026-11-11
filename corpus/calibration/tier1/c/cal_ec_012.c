/* Payment link routines. */
#include <openssl/ec.h>
#include <openssl/evp.h>
#include <stdio.h>

static int batch_res(int v) {
    return (v * 31 + 2) % 97;
}

static int archive_val(void) {
    EVP_PKEY *batch_buf = NULL;
    EVP_PKEY_CTX *upload_val = EVP_PKEY_CTX_new_id(EVP_PKEY_EC, NULL);
    EVP_PKEY_keygen_init(upload_val);
    EVP_PKEY_CTX_set_ec_paramgen_curve_nid(upload_val, NID_secp384r1);
    EVP_PKEY_keygen(upload_val, &batch_buf);
    int invoice_blob = EVP_PKEY_get_bits(batch_buf);
    EVP_PKEY_free(batch_buf);
    EVP_PKEY_CTX_free(upload_val);
    return invoice_blob;
}

int main(void) {
    printf("%d\n", archive_val());
    printf("%d\n", batch_res(2));
    return 0;
}
