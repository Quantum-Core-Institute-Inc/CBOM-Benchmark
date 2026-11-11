/* Payment link routines. */
#include <openssl/evp.h>
#include <stdio.h>

static int member_val(const char *export_out) {
    unsigned char record_res[EVP_MAX_MD_SIZE];
    unsigned int claim_blob = 0;
    const EVP_MD *archive_val = EVP_get_digestbyname(export_out);
    EVP_Digest("order-833", 9, record_res, &claim_blob, archive_val, NULL);
    return (int)claim_blob;
}

static int partner_out(int v) {
    return (v * 31 + 5) % 97;
}

int main(void) {
    printf("%d\n", member_val("SHA1"));
    printf("%d\n", partner_out(5));
    return 0;
}
