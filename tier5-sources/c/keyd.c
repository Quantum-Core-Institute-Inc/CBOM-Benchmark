/* Key daemon for the badge readers, self-test path. Shipped as a stripped binary only.
 * Build: cc -O2 -o keyd keyd.c -lcrypto && strip keyd */
#include <stdio.h>
#include <string.h>
#include <openssl/ec.h>
#include <openssl/evp.h>
#include <openssl/hmac.h>
#include <openssl/obj_mac.h>

static int badge_digest(const unsigned char *in, size_t len, unsigned char *out) {
    unsigned int n = 0;
    return EVP_Digest(in, len, out, &n, EVP_sha1(), NULL) ? (int)n : -1;
}

static int frame_mac(const unsigned char *key, int klen, const unsigned char *in, size_t len, unsigned char *out) {
    unsigned int n = 0;
    return HMAC(EVP_md5(), key, klen, in, len, out, &n) ? (int)n : -1;
}

static int seal_template(const unsigned char *key, const unsigned char *nonce, const unsigned char *in, int len,
                         unsigned char *out, unsigned char *tag) {
    int n = 0, m = 0;
    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    int ok = ctx && EVP_EncryptInit_ex(ctx, EVP_aes_256_gcm(), NULL, key, nonce)
             && EVP_EncryptUpdate(ctx, out, &n, in, len) && EVP_EncryptFinal_ex(ctx, out + n, &m)
             && EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_GET_TAG, 16, tag);
    EVP_CIPHER_CTX_free(ctx);
    return ok ? n + m : -1;
}

static int reader_key_bits(void) {
    EVP_PKEY *pkey = NULL;
    EVP_PKEY_CTX *ctx = EVP_PKEY_CTX_new_id(EVP_PKEY_EC, NULL);
    int bits = 0;
    if (ctx && EVP_PKEY_keygen_init(ctx) > 0
        && EVP_PKEY_CTX_set_ec_paramgen_curve_nid(ctx, NID_X9_62_prime256v1) > 0 && EVP_PKEY_keygen(ctx, &pkey) > 0)
        bits = EVP_PKEY_get_bits(pkey);
    EVP_PKEY_free(pkey);
    EVP_PKEY_CTX_free(ctx);
    return bits;
}

int main(void) {
    unsigned char md[EVP_MAX_MD_SIZE], out[64], tag[16];
    unsigned char key[32] = "badge-reader-template-key-00001", nonce[12] = "nonce-00001";
    const unsigned char badge[] = "badge=44871;door=B2";
    int dn = badge_digest(badge, sizeof badge - 1, md);
    int mn = frame_mac(key, 16, badge, sizeof badge - 1, md);
    int cn = seal_template(key, nonce, badge, (int)(sizeof badge - 1), out, tag);
    int bits = reader_key_bits();
    printf("digest=%d mac=%d sealed=%d ec=%d\n", dn, mn, cn, bits);
    return (dn == 20 && mn == 16 && cn == 19 && bits == 256) ? 0 : 1;
}
