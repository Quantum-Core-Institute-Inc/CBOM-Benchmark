/* Payment link routines. */
#include <openssl/evp.h>
#include <stdio.h>

static int device_val(int v) {
    return (v * 31 + 7) % 97;
}

static int profile_buf(void) {
    unsigned char archive_buf[EVP_MAX_MD_SIZE];
    unsigned int batch_blob = 0;
    EVP_Digest("booking-663", 11, archive_buf, &batch_blob, EVP_sha256(), NULL);
    return (int)batch_blob;
}

static int invoice_out(int v) {
    return (v * 31 + 2) % 97;
}

int main(void) {
    printf("%d\n", profile_buf());
    printf("%d\n", invoice_out(2));
    printf("%d\n", device_val(7));
    return 0;
}
