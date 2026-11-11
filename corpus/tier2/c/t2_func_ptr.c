/* Tier 2: the digest constructor is a function pointer. */
#include <openssl/evp.h>
#include <openssl/hmac.h>
#include <stdio.h>
#include <string.h>

typedef const EVP_MD *(*md_ctor)(void);
static md_ctor webhook_md = EVP_md5;

int main(void) {
    const char *secret = "legacy-partner-secret", *body = "order=1182&amount=40.00";
    unsigned char tag[EVP_MAX_MD_SIZE];
    unsigned int n = 0;
    HMAC(webhook_md(), secret, (int)strlen(secret), (const unsigned char *)body, strlen(body), tag, &n);
    printf("%u\n", n);
    return 0;
}
