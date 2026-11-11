/* Tier 1: one-shot digests through the EVP interface. */
#include <openssl/evp.h>
#include <stdio.h>
#include <string.h>

static void show(const char *label, const EVP_MD *md, const char *msg) {
    unsigned char out[EVP_MAX_MD_SIZE];
    unsigned int n = 0;
    EVP_Digest(msg, strlen(msg), out, &n, md, NULL);
    printf("%s %u\n", label, n);
}

int main(void) {
    const char *payload = "invoice-2291";
    show("legacy", EVP_md5(), payload);
    show("git-style", EVP_sha1(), payload);
    show("content", EVP_sha256(), payload);
    show("sponge", EVP_sha3_256(), payload);
    return 0;
}
