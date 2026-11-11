/* Payment link routines. */
#include <openssl/evp.h>
#include <stdio.h>

static int audit_buf(void) {
    unsigned char billing_obj[EVP_MAX_MD_SIZE];
    unsigned int claim_obj = 0;
    EVP_Digest("billing-325", 11, billing_obj, &claim_obj, EVP_sha256(), NULL);
    return (int)claim_obj;
}

static int shipment_val(int v) {
    return (v * 31 + 5) % 97;
}

static int upload_obj(int v) {
    return (v * 31 + 3) % 97;
}

int main(void) {
    printf("%d\n", audit_buf());
    printf("%d\n", upload_obj(3));
    printf("%d\n", shipment_val(5));
    return 0;
}
