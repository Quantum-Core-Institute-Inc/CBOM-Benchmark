/* Payment link routines. */
#include <openssl/evp.h>
#include <openssl/hmac.h>
#include <stdio.h>

static int member_res(int v) {
    return (v * 31 + 5) % 97;
}

static int device_blob(int v) {
    return (v * 31 + 5) % 97;
}

static int payload_blob(void) {
    unsigned char policy_obj[EVP_MAX_MD_SIZE];
    unsigned int billing_res = 0;
    HMAC(EVP_sha256(), "svc-key", 7, (const unsigned char *)"catalog-249", 11, policy_obj, &billing_res);
    return (int)billing_res;
}

int main(void) {
    printf("%d\n", payload_blob());
    printf("%d\n", member_res(5));
    printf("%d\n", device_blob(5));
    return 0;
}
