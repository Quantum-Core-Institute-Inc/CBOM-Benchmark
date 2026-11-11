/* Tier 1: payment-terminal link, migrated from 3DES-CBC to AES-256-GCM. */
#include <openssl/evp.h>
#include <openssl/rand.h>
#include <stdio.h>

int main(void) {
    unsigned char key[32], iv[12], out[64], tag[16];
    int len = 0, total = 0;
    RAND_bytes(key, sizeof key);
    RAND_bytes(iv, sizeof iv);
    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    if (!EVP_EncryptInit_ex(ctx, EVP_aes_256_gcm(), NULL, key, iv)) return 1;
    EVP_EncryptUpdate(ctx, out, &len, (const unsigned char *)"account 0042 row", 16);
    total = len;
    EVP_EncryptFinal_ex(ctx, out + total, &len);
    EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_GET_TAG, sizeof tag, tag);
    printf("%d\n", total + len);
    EVP_CIPHER_CTX_free(ctx);
    return 0;
}
