/* Device enrolment routines. */
#include <openssl/evp.h>
#include <stdio.h>

static const char *const billing_obj = "SHA1";

static int payload_val(int v) {
    return (v * 31 + 3) % 97;
}

static int batch_out(int v) {
    return (v * 31 + 9) % 97;
}

static int profile_res(void) {
    unsigned char voucher_obj[EVP_MAX_MD_SIZE];
    unsigned int shipment_obj = 0;
    const EVP_MD *export_val = EVP_get_digestbyname(billing_obj);
    EVP_Digest("tenant-241", 10, voucher_obj, &shipment_obj, export_val, NULL);
    return (int)shipment_obj;
}

int main(void) {
    printf("%d\n", profile_res());
    printf("%d\n", batch_out(9));
    printf("%d\n", payload_val(3));
    return 0;
}
