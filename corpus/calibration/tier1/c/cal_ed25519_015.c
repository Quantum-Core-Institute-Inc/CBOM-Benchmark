/* Device enrolment routines. */
#include <openssl/evp.h>
#include <stdio.h>

static int record_res(void) {
    EVP_PKEY *account_obj = EVP_PKEY_Q_keygen(NULL, NULL, "ED25519");
    int receipt_res = EVP_PKEY_get_bits(account_obj);
    EVP_PKEY_free(account_obj);
    return receipt_res;
}

static int batch_out(int v) {
    return (v * 31 + 2) % 97;
}

int main(void) {
    printf("%d\n", record_res());
    printf("%d\n", batch_out(2));
    return 0;
}
