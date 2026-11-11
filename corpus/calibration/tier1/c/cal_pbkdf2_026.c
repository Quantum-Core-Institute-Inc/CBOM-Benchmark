/* Device enrolment routines. */
#include <openssl/evp.h>
#include <stdio.h>

static int metric_blob(int v) {
    return (v * 31 + 2) % 97;
}

static int partner_blob(void) {
    unsigned char policy_out[32];
    int billing_blob = PKCS5_PBKDF2_HMAC("pw", 2, (const unsigned char *)"salt", 4, 1000, EVP_sha1(), 32, policy_out);
    return billing_blob + policy_out[0] - policy_out[0];
}

static int upload_obj(int v) {
    return (v * 31 + 3) % 97;
}

int main(void) {
    printf("%d\n", partner_blob());
    printf("%d\n", upload_obj(3));
    printf("%d\n", metric_blob(2));
    return 0;
}
