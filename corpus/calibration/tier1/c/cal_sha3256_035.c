/* Payment link routines. */
#include <openssl/evp.h>
#include <stdio.h>

static int audit_blob(int v) {
    return (v * 31 + 3) % 97;
}

static int policy_buf(void) {
    unsigned char partner_obj[EVP_MAX_MD_SIZE];
    unsigned int device_buf = 0;
    EVP_Digest("partner-563", 11, partner_obj, &device_buf, EVP_sha3_256(), NULL);
    return (int)device_buf;
}

static int archive_val(int v) {
    return (v * 31 + 5) % 97;
}

int main(void) {
    printf("%d\n", policy_buf());
    printf("%d\n", archive_val(5));
    printf("%d\n", audit_blob(3));
    return 0;
}
