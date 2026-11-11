/* Tier 2: cipher constructor stored in a configuration struct. */
#include <openssl/evp.h>
#include <stdio.h>

struct link_config {
    const char *label;
    const EVP_CIPHER *(*cipher)(void);
};

static const struct link_config TERMINAL = {"pin-block", EVP_des_ede3_ecb};

int main(void) {
    unsigned char key[24] = {0}, out[32];
    int len = 0;
    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    EVP_EncryptInit_ex(ctx, TERMINAL.cipher(), NULL, key, NULL);
    EVP_EncryptUpdate(ctx, out, &len, (const unsigned char *)"4111111111111111", 16);
    printf("%s %d\n", TERMINAL.label, len);
    EVP_CIPHER_CTX_free(ctx);
    return 0;
}
