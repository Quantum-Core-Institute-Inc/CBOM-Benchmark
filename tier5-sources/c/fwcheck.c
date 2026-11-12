/* Firmware checker for the gateway, self-test path. Shipped as a stripped binary only. Every
 * algorithm is fetched by name, so none appears as an imported symbol: the names are strings in
 * the binary's read-only data. Build: cc -O2 -o fwcheck fwcheck.c -lcrypto && strip fwcheck */
#include <stdio.h>
#include <string.h>
#include <openssl/core_names.h>
#include <openssl/evp.h>
#include <openssl/params.h>

static int image_digest(const unsigned char *in, size_t len, unsigned char *out) {
    unsigned int n = 0;
    EVP_MD *md = EVP_MD_fetch(NULL, "SHA2-512", NULL);
    int ok = md && EVP_Digest(in, len, out, &n, md, NULL);
    EVP_MD_free(md);
    return ok ? (int)n : -1;
}

static int unwrap_block(const unsigned char *key, const unsigned char *in, int len, unsigned char *out) {
    int n = 0, m = 0;
    EVP_CIPHER *cipher = EVP_CIPHER_fetch(NULL, "AES-128-ECB", NULL);
    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    int ok = cipher && ctx && EVP_EncryptInit_ex2(ctx, cipher, key, NULL, NULL)
             && EVP_EncryptUpdate(ctx, out, &n, in, len) && EVP_EncryptFinal_ex(ctx, out + n, &m);
    EVP_CIPHER_CTX_free(ctx);
    EVP_CIPHER_free(cipher);
    return ok ? n + m : -1;
}

static int pairing_group_bits(void) {
    EVP_PKEY *pkey = NULL;
    EVP_PKEY_CTX *ctx = EVP_PKEY_CTX_new_from_name(NULL, "DH", NULL);
    OSSL_PARAM params[] = { OSSL_PARAM_construct_utf8_string(OSSL_PKEY_PARAM_GROUP_NAME, "ffdhe2048", 0), OSSL_PARAM_construct_end() };
    int bits = 0;
    if (ctx && EVP_PKEY_keygen_init(ctx) > 0 && EVP_PKEY_CTX_set_params(ctx, params) > 0 && EVP_PKEY_keygen(ctx, &pkey) > 0)
        bits = EVP_PKEY_get_bits(pkey);
    EVP_PKEY_free(pkey);
    EVP_PKEY_CTX_free(ctx);
    return bits;
}

static int session_key_bits(void) {
    EVP_PKEY *pkey = EVP_PKEY_Q_keygen(NULL, NULL, "X25519");
    int bits = pkey ? EVP_PKEY_get_bits(pkey) : 0;
    EVP_PKEY_free(pkey);
    return bits;
}

int main(void) {
    unsigned char md[EVP_MAX_MD_SIZE], out[64];
    unsigned char key[16] = "gateway-unwrap!";
    const unsigned char image[] = "gateway-fw-3.9.2";
    int dn = image_digest(image, sizeof image - 1, md);
    int cn = unwrap_block(key, image, (int)(sizeof image - 1), out);
    int dh = pairing_group_bits();
    int xk = session_key_bits();
    printf("digest=%d block=%d dh=%d x25519=%d\n", dn, cn, dh, xk);
    return (dn == 64 && cn == 32 && dh == 2048 && xk == 253) ? 0 : 1;
}
