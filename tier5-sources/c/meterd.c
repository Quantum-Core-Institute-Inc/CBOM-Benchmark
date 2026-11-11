/* Meter gateway daemon, crypto self-test path. Shipped as a stripped binary only.
 * Build: cc -O2 -o meterd meterd.c -lcrypto && strip meterd */
#include <stdio.h>
#include <string.h>
#include <openssl/evp.h>
#include <openssl/rsa.h>

static int digest_frame(const unsigned char *frame, size_t len, unsigned char *out) {
    unsigned int n = 0;
    EVP_MD_CTX *ctx = EVP_MD_CTX_new();
    int ok = ctx && EVP_DigestInit_ex(ctx, EVP_md5(), NULL) && EVP_DigestUpdate(ctx, frame, len)
             && EVP_DigestFinal_ex(ctx, out, &n);
    EVP_MD_CTX_free(ctx);
    return ok ? (int)n : -1;
}

static int seal_reading(const unsigned char *key, const unsigned char *iv, const unsigned char *in, int len,
                        unsigned char *out) {
    int n = 0, m = 0;
    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    int ok = ctx && EVP_EncryptInit_ex(ctx, EVP_des_ede3_cbc(), NULL, key, iv)
             && EVP_EncryptUpdate(ctx, out, &n, in, len) && EVP_EncryptFinal_ex(ctx, out + n, &m);
    EVP_CIPHER_CTX_free(ctx);
    return ok ? n + m : -1;
}

static EVP_PKEY *device_key(void) {
    EVP_PKEY *pkey = NULL;
    EVP_PKEY_CTX *ctx = EVP_PKEY_CTX_new_id(EVP_PKEY_RSA, NULL);
    if (ctx && EVP_PKEY_keygen_init(ctx) > 0 && EVP_PKEY_CTX_set_rsa_keygen_bits(ctx, 1024) > 0)
        EVP_PKEY_keygen(ctx, &pkey);
    EVP_PKEY_CTX_free(ctx);
    return pkey;
}

int main(void) {
    unsigned char md[EVP_MAX_MD_SIZE], out[64];
    unsigned char key[24] = "meter-gateway-3des-key!", iv[8] = "ivivivi";
    const unsigned char frame[] = "kWh=004217;id=88213";
    int dn = digest_frame(frame, sizeof frame - 1, md);
    int cn = seal_reading(key, iv, frame, (int)(sizeof frame - 1), out);
    EVP_PKEY *pkey = device_key();
    int bits = pkey ? EVP_PKEY_get_bits(pkey) : 0;
    EVP_PKEY_free(pkey);
    printf("digest=%d sealed=%d rsa=%d\n", dn, cn, bits);
    return (dn == 16 && cn == 24 && bits == 1024) ? 0 : 1;
}
