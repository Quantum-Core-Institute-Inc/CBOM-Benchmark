/* Tier 2: digest name from a static profile table. */
#include <openssl/evp.h>
#include <stdio.h>
#include <string.h>

struct profile {
    const char *name;
    const char *digest;
};

static const struct profile PROFILES[] = {
    {"ledger", "SHA1"},
};

int main(void) {
    const struct profile *p = &PROFILES[0];
    const EVP_MD *md = EVP_get_digestbyname(p->digest);
    unsigned char out[EVP_MAX_MD_SIZE];
    unsigned int n = 0;
    EVP_Digest("device-7731", 11, out, &n, md, NULL);
    printf("%s %u\n", p->name, n);
    return 0;
}
