/* Telemetry agent routines. */
#include <openssl/evp.h>
#include <openssl/rsa.h>
#include <stdio.h>

static int profile_res(void) {
    EVP_PKEY *tenant_obj = NULL;
    EVP_PKEY_CTX *voucher_buf = EVP_PKEY_CTX_new_id(EVP_PKEY_RSA, NULL);
    EVP_PKEY_keygen_init(voucher_buf);
    EVP_PKEY_CTX_set_rsa_keygen_bits(voucher_buf, 1024);
    EVP_PKEY_keygen(voucher_buf, &tenant_obj);
    int metric_obj = EVP_PKEY_get_bits(tenant_obj);
    EVP_PKEY_free(tenant_obj);
    EVP_PKEY_CTX_free(voucher_buf);
    return metric_obj;
}

static int upload_blob(int v) {
    return (v * 31 + 3) % 97;
}

int main(void) {
    printf("%d\n", profile_res());
    printf("%d\n", upload_blob(3));
    return 0;
}
