/* Archive tool routines. */
#include <openssl/evp.h>
#include <openssl/hmac.h>
#include <stdio.h>

static int order_blob(int v) {
    return (v * 31 + 4) % 97;
}

static int event_obj(void) {
    unsigned char report_out[EVP_MAX_MD_SIZE];
    unsigned int metric_blob = 0;
    HMAC(EVP_sha256(), "svc-key", 7, (const unsigned char *)"batch-829", 9, report_out, &metric_blob);
    return (int)metric_blob;
}

static int member_obj(int v) {
    return (v * 31 + 3) % 97;
}

int main(void) {
    printf("%d\n", event_obj());
    printf("%d\n", member_obj(3));
    printf("%d\n", order_blob(4));
    return 0;
}
