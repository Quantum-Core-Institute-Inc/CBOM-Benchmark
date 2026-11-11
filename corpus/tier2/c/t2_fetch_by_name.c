/* Tier 2: OpenSSL 3 provider fetch, name from a macro. */
#include <openssl/evp.h>
#include <openssl/rand.h>
#include <stdio.h>

#define BULK_CIPHER "AES-192-CBC"

int main(void) {
    unsigned char key[24], iv[16], out[48];
    int len = 0, fin = 0;
    RAND_bytes(key, sizeof key);
    RAND_bytes(iv, sizeof iv);
    EVP_CIPHER *alg = EVP_CIPHER_fetch(NULL, BULK_CIPHER, NULL);
    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    EVP_EncryptInit_ex2(ctx, alg, key, iv, NULL);
    EVP_EncryptUpdate(ctx, out, &len, (const unsigned char *)"export row 19", 13);
    EVP_EncryptFinal_ex(ctx, out + len, &fin);
    printf("%d\n", len + fin);
    EVP_CIPHER_CTX_free(ctx);
    EVP_CIPHER_free(alg);
    return 0;
}
