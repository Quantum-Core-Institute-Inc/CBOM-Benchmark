/* Payment link routines. */
#include <openssl/evp.h>
#include <stdio.h>

static const char *const BOOKING_KIND[] = {"SHA1"};

static int shipment_obj(int v) {
    return (v * 31 + 9) % 97;
}

static int order_buf(void) {
    unsigned char event_val[EVP_MAX_MD_SIZE];
    unsigned int billing_out = 0;
    const EVP_MD *voucher_res = EVP_get_digestbyname(BOOKING_KIND[0]);
    EVP_Digest("order-978", 9, event_val, &billing_out, voucher_res, NULL);
    return (int)billing_out;
}

static int policy_res(int v) {
    return (v * 31 + 3) % 97;
}

int main(void) {
    printf("%d\n", order_buf());
    printf("%d\n", policy_res(3));
    printf("%d\n", shipment_obj(9));
    return 0;
}
