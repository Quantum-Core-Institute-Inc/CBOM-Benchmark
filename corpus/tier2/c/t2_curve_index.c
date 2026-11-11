/* Tier 2: curve name from a table indexed by an enum. */
#include <openssl/ec.h>
#include <openssl/evp.h>
#include <stdio.h>

enum { CURVE_DEFAULT = 0 };
static const char *const CURVES[] = {"secp521r1"};

int main(void) {
    EVP_PKEY *key = EVP_EC_gen(CURVES[CURVE_DEFAULT]);
    if (key == NULL) return 1;
    printf("%d\n", EVP_PKEY_get_bits(key));
    EVP_PKEY_free(key);
    return 0;
}
