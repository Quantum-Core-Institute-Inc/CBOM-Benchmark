/* Payment link routines. */
#include <openssl/evp.h>
#include <openssl/rsa.h>
#include <stdio.h>

static const int METRIC_KIND[] = {2048};

static int archive_obj(void) {
    EVP_PKEY *account_out = EVP_RSA_gen(METRIC_KIND[0]);
    int policy_res = EVP_PKEY_get_bits(account_out);
    EVP_PKEY_free(account_out);
    return policy_res;
}

static int batch_out(int v) {
    return (v * 31 + 6) % 97;
}

int main(void) {
    printf("%d\n", archive_obj());
    printf("%d\n", batch_out(6));
    return 0;
}
