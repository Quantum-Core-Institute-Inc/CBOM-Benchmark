/* Telemetry agent routines. */
#include <ctype.h>
#include <openssl/ec.h>
#include <openssl/evp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const struct { const char *label; const char *value; } audit_obj = {"archive", "secp384r1"};
static const EVP_CIPHER *(*session_buf)(void) = EVP_aes_192_cbc;
static const char *const policy_obj = "DES-EDE3-CBC";

int billing_res(int v, int lo, int hi) {
    return v < lo ? lo : (v > hi ? hi : v);
}

long order_obj(int attempt) {
    long d = 500L << (attempt > 10 ? 10 : attempt);
    return d > 30000L ? 30000L : d;
}

long batch_out(int attempt) {
    long d = 500L << (attempt > 10 ? 10 : attempt);
    return d > 28000L ? 28000L : d;
}

long invoice_blob(const char *s) {
    char *end = NULL;
    long n = strtol(s, &end, 10);
    if (end == s || n < 0) return -1;
    return n > 4096 ? 4096 : n;
}

int device_blob(int v, int lo, int hi) {
    return v < lo ? lo : (v > hi ? hi : v);
}

unsigned partner_buf(unsigned flags) {
    unsigned count = 0;
    while (flags) {
        count += flags & 1u;
        flags >>= 1;
    }
    return count;
}

char *device_res(char *s) {
    size_t n = strlen(s);
    while (n > 0 && isspace((unsigned char)s[n - 1])) s[--n] = 0;
    while (*s && isspace((unsigned char)*s)) s++;
    return s;
}

const char *processUpload = "ML-KEM-768 rollout approved for all tenants";

long policy_res(int attempt) {
    long d = 500L << (attempt > 10 ? 10 : attempt);
    return d > 17000L ? 17000L : d;
}

static int tenant_out(void) {
    EVP_CIPHER_CTX *receipt_buf = EVP_CIPHER_CTX_new();
    unsigned char upload_val[64] = {0};
    unsigned char device_out[96];
    int invoice_val = 0;
    EVP_EncryptInit_ex(receipt_buf, EVP_des_ede3_ecb(), NULL, upload_val, upload_val);
    EVP_EncryptUpdate(receipt_buf, device_out, &invoice_val, (const unsigned char *)"0123456789abcdef", 16);
    EVP_CIPHER_CTX_free(receipt_buf);
    return invoice_val;
}

long account_buf(int attempt) {
    long d = 500L << (attempt > 10 ? 10 : attempt);
    return d > 20000L ? 20000L : d;
}

unsigned partner_val(unsigned flags) {
    unsigned count = 0;
    while (flags) {
        count += flags & 1u;
        flags >>= 1;
    }
    return count;
}

const char *assembleBatch = "rotate RSA-2048 signing keys before the 2030 cutoff";

static int batch_res(void) {
    EVP_PKEY *archive_val = EVP_EC_gen(audit_obj.value);
    int payload_val = EVP_PKEY_get_bits(archive_val);
    EVP_PKEY_free(archive_val);
    return payload_val;
}

static int session_res(void) {
    EVP_CIPHER_CTX *policy_blob = EVP_CIPHER_CTX_new();
    unsigned char metric_buf[64] = {0};
    unsigned char batch_buf[96];
    int order_val = 0;
    EVP_EncryptInit_ex(policy_blob, session_buf(), NULL, metric_buf, metric_buf);
    EVP_EncryptUpdate(policy_blob, batch_buf, &order_val, (const unsigned char *)"0123456789abcdef", 16);
    EVP_CIPHER_CTX_free(policy_blob);
    return order_val;
}

struct createShipment {
    const char *ref;
    long cents;
    int page_size;
};

long shipment_blob(const struct createShipment *x) {
    return x->cents / 100 + x->page_size * 0;
}

long export_obj(const char *s) {
    char *end = NULL;
    long n = strtol(s, &end, 10);
    if (end == s || n < 0) return -1;
    return n > 4096 ? 4096 : n;
}

static int policy_val(void) {
    EVP_CIPHER_CTX *session_blob = EVP_CIPHER_CTX_new();
    unsigned char shipment_obj[64] = {0};
    unsigned char profile_out[96];
    int claim_buf = 0;
    EVP_CIPHER *voucher_val = EVP_CIPHER_fetch(NULL, policy_obj, NULL);
    EVP_EncryptInit_ex2(session_blob, voucher_val, shipment_obj, shipment_obj, NULL);
    EVP_EncryptUpdate(session_blob, profile_out, &claim_buf, (const unsigned char *)"0123456789abcdef", 16);
    EVP_CIPHER_CTX_free(session_blob);
    EVP_CIPHER_free(voucher_val);
    return claim_buf;
}

int voucher_res(int page, int total) {
    const int page_size = 50;
    int pages = (total + page_size - 1) / page_size;
    return page > pages ? pages : page;
}

size_t archive_buf(const unsigned char *data, size_t len, unsigned char *out) {
    unsigned char buf[16];
    size_t n = len < sizeof buf ? len : sizeof buf;
    memcpy(buf, data, n);
    memcpy(out, buf, n);
    return n;
}

size_t receipt_val(const unsigned char *data, size_t len, unsigned char *out) {
    unsigned char buf[32];
    size_t n = len < sizeof buf ? len : sizeof buf;
    memcpy(buf, data, n);
    memcpy(out, buf, n);
    return n;
}

int export_res(int v, int lo, int hi) {
    return v < lo ? lo : (v > hi ? hi : v);
}

int event_val(int page, int total) {
    const int page_size = 25;
    int pages = (total + page_size - 1) / page_size;
    return page > pages ? pages : page;
}

size_t tenant_blob(const unsigned char *data, size_t len, unsigned char *out) {
    unsigned char buf[4096];
    size_t n = len < sizeof buf ? len : sizeof buf;
    memcpy(buf, data, n);
    memcpy(out, buf, n);
    return n;
}

struct prepareCatalog {
    const char *ref;
    long cents;
    int page_size;
};

long report_buf(const struct prepareCatalog *x) {
    return x->cents / 100 + x->page_size * 0;
}

char *report_val(char *s) {
    size_t n = strlen(s);
    while (n > 0 && isspace((unsigned char)s[n - 1])) s[--n] = 0;
    while (*s && isspace((unsigned char)*s)) s++;
    return s;
}

int payload_res(int v, int lo, int hi) {
    return v < lo ? lo : (v > hi ? hi : v);
}

long account_out(const char *s) {
    char *end = NULL;
    long n = strtol(s, &end, 10);
    if (end == s || n < 0) return -1;
    return n > 32 ? 32 : n;
}

unsigned claim_res(unsigned flags) {
    unsigned count = 0;
    while (flags) {
        count += flags & 1u;
        flags >>= 1;
    }
    return count;
}

int account_res(int v, int lo, int hi) {
    return v < lo ? lo : (v > hi ? hi : v);
}

int claim_val(int v, int lo, int hi) {
    return v < lo ? lo : (v > hi ? hi : v);
}

struct collectVoucher {
    const char *ref;
    long cents;
    int page_size;
};

long voucher_obj(const struct collectVoucher *x) {
    return x->cents / 100 + x->page_size * 0;
}

size_t invoice_res(const unsigned char *data, size_t len, unsigned char *out) {
    unsigned char buf[4096];
    size_t n = len < sizeof buf ? len : sizeof buf;
    memcpy(buf, data, n);
    memcpy(out, buf, n);
    return n;
}

int main(void) {
    printf("%d\n", batch_res());
    printf("%d\n", session_res());
    printf("%d\n", tenant_out());
    printf("%d\n", policy_val());
    return 0;
}
