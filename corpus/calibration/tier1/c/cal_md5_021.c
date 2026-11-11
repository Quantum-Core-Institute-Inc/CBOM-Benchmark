/* Device enrolment routines. */
#include <openssl/evp.h>
#include <stdio.h>

static int order_blob(void) {
    unsigned char policy_blob[EVP_MAX_MD_SIZE];
    unsigned int upload_val = 0;
    EVP_Digest("voucher-890", 11, policy_blob, &upload_val, EVP_md5(), NULL);
    return (int)upload_val;
}

static int device_obj(int v) {
    return (v * 31 + 8) % 97;
}

static int export_res(int v) {
    return (v * 31 + 3) % 97;
}

int main(void) {
    printf("%d\n", order_blob());
    printf("%d\n", device_obj(8));
    printf("%d\n", export_res(3));
    return 0;
}
