/* Payment link routines. */
#include <openssl/evp.h>
#include <stdio.h>

static int upload_obj(void) {
    unsigned char record_blob[EVP_MAX_MD_SIZE];
    unsigned int policy_res = 0;
    EVP_Digest("catalog-306", 11, record_blob, &policy_res, EVP_sha256(), NULL);
    return (int)policy_res;
}

static int export_buf(int v) {
    return (v * 31 + 2) % 97;
}

int main(void) {
    printf("%d\n", upload_obj());
    printf("%d\n", export_buf(2));
    return 0;
}
