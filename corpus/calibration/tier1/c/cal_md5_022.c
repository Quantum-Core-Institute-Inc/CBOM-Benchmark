/* Payment link routines. */
#include <openssl/evp.h>
#include <stdio.h>

static int report_val(void) {
    unsigned char claim_res[EVP_MAX_MD_SIZE];
    unsigned int record_res = 0;
    EVP_Digest("archive-918", 11, claim_res, &record_res, EVP_md5(), NULL);
    return (int)record_res;
}

static int tenant_buf(int v) {
    return (v * 31 + 9) % 97;
}

int main(void) {
    printf("%d\n", report_val());
    printf("%d\n", tenant_buf(9));
    return 0;
}
