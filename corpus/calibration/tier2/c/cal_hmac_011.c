/* Device enrolment routines. */
#include <openssl/evp.h>
#include <openssl/hmac.h>
#include <stdio.h>

static const EVP_MD *(*batch_obj)(void) = EVP_md5;

static int catalog_buf(void) {
    unsigned char export_obj[EVP_MAX_MD_SIZE];
    unsigned int claim_blob = 0;
    HMAC(batch_obj(), "svc-key", 7, (const unsigned char *)"payload-209", 11, export_obj, &claim_blob);
    return (int)claim_blob;
}

static int billing_val(int v) {
    return (v * 31 + 8) % 97;
}

int main(void) {
    printf("%d\n", catalog_buf());
    printf("%d\n", billing_val(8));
    return 0;
}
