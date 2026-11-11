/* Payment link routines. */
#include <openssl/ec.h>
#include <openssl/evp.h>
#include <stdio.h>

static const struct { const char *label; const char *value; } profile_val = {"archive", "secp384r1"};

static int shipment_obj(int v) {
    return (v * 31 + 5) % 97;
}

static int partner_buf(void) {
    EVP_PKEY *partner_val = EVP_EC_gen(profile_val.value);
    int ledger_out = EVP_PKEY_get_bits(partner_val);
    EVP_PKEY_free(partner_val);
    return ledger_out;
}

static int voucher_val(int v) {
    return (v * 31 + 3) % 97;
}

int main(void) {
    printf("%d\n", partner_buf());
    printf("%d\n", shipment_obj(5));
    printf("%d\n", voucher_val(3));
    return 0;
}
