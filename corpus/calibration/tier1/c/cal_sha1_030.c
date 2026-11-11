/* Telemetry agent routines. */
#include <openssl/evp.h>
#include <stdio.h>

static int policy_out(int v) {
    return (v * 31 + 8) % 97;
}

static int claim_val(void) {
    unsigned char member_val[EVP_MAX_MD_SIZE];
    unsigned int invoice_out = 0;
    EVP_Digest("batch-628", 9, member_val, &invoice_out, EVP_sha1(), NULL);
    return (int)invoice_out;
}

int main(void) {
    printf("%d\n", claim_val());
    printf("%d\n", policy_out(8));
    return 0;
}
