/* Tier 1: message authentication and password-based key derivation. */
#include <openssl/evp.h>
#include <openssl/hmac.h>
#include <stdio.h>
#include <string.h>

int main(void) {
    const char *secret = "webhook-secret", *body = "{\"event\":\"paid\"}";
    unsigned char tag[EVP_MAX_MD_SIZE];
    unsigned int taglen = 0;
    HMAC(EVP_sha256(), secret, (int)strlen(secret), (const unsigned char *)body, strlen(body), tag, &taglen);

    unsigned char key[32];
    const char *pw = "correct horse";
    PKCS5_PBKDF2_HMAC(pw, (int)strlen(pw), (const unsigned char *)"per-user-salt", 13, 100000, EVP_sha1(), 32, key);
    printf("%u %d\n", taglen, key[0] >= 0);
    return 0;
}
