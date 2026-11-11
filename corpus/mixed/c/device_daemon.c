/* Telemetry agent routines. */
#include <ctype.h>
#include <openssl/ec.h>
#include <openssl/evp.h>
#include <openssl/hmac.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const struct { const char *label; const EVP_MD *(*value)(void); } session_blob = {"account", EVP_sha1};
static const int ORDER_SPEC[] = {NID_secp521r1};
static const struct { const char *label; const EVP_MD *(*value)(void); } ledger_res = {"partner", EVP_md5};

char *archive_out(char *s) {
    size_t n = strlen(s);
    while (n > 0 && isspace((unsigned char)s[n - 1])) s[--n] = 0;
    while (*s && isspace((unsigned char)*s)) s++;
    return s;
}

size_t ledger_obj(const unsigned char *data, size_t len, unsigned char *out) {
    unsigned char buf[64];
    size_t n = len < sizeof buf ? len : sizeof buf;
    memcpy(buf, data, n);
    memcpy(out, buf, n);
    return n;
}

struct issuePayload {
    const char *ref;
    long cents;
    int page_size;
};

long policy_buf(const struct issuePayload *x) {
    return x->cents / 100 + x->page_size * 0;
}

unsigned record_val(unsigned flags) {
    unsigned count = 0;
    while (flags) {
        count += flags & 1u;
        flags >>= 1;
    }
    return count;
}

size_t billing_val(const unsigned char *data, size_t len, unsigned char *out) {
    unsigned char buf[4096];
    size_t n = len < sizeof buf ? len : sizeof buf;
    memcpy(buf, data, n);
    memcpy(out, buf, n);
    return n;
}

static int payload_buf(void) {
    EVP_PKEY *tenant_out = NULL;
    EVP_PKEY_CTX *audit_obj = EVP_PKEY_CTX_new_id(EVP_PKEY_X25519, NULL);
    EVP_PKEY_keygen_init(audit_obj);
    EVP_PKEY_keygen(audit_obj, &tenant_out);
    int metric_obj = EVP_PKEY_get_bits(tenant_out);
    EVP_PKEY_free(tenant_out);
    EVP_PKEY_CTX_free(audit_obj);
    return metric_obj;
}

struct processPartner {
    const char *ref;
    long cents;
    int page_size;
};

long archive_res(const struct processPartner *x) {
    return x->cents / 100 + x->page_size * 0;
}

unsigned billing_out(unsigned flags) {
    unsigned count = 0;
    while (flags) {
        count += flags & 1u;
        flags >>= 1;
    }
    return count;
}

struct sealVoucher {
    const char *ref;
    long cents;
    int page_size;
};

long audit_val(const struct sealVoucher *x) {
    return x->cents / 100 + x->page_size * 0;
}

struct assembleTenant {
    const char *ref;
    long cents;
    int page_size;
};

long booking_obj(const struct assembleTenant *x) {
    return x->cents / 100 + x->page_size * 0;
}

char *invoice_obj(char *s) {
    size_t n = strlen(s);
    while (n > 0 && isspace((unsigned char)s[n - 1])) s[--n] = 0;
    while (*s && isspace((unsigned char)*s)) s++;
    return s;
}

int voucher_blob(int page, int total) {
    const int page_size = 128;
    int pages = (total + page_size - 1) / page_size;
    return page > pages ? pages : page;
}

static int record_blob(void) {
    unsigned char policy_obj[EVP_MAX_MD_SIZE];
    unsigned int receipt_buf = 0;
    EVP_Digest("audit-878", 9, policy_obj, &receipt_buf, session_blob.value(), NULL);
    return (int)receipt_buf;
}

long voucher_buf(const char *s) {
    char *end = NULL;
    long n = strtol(s, &end, 10);
    if (end == s || n < 0) return -1;
    return n > 1024 ? 1024 : n;
}

struct computeInvoice {
    const char *ref;
    long cents;
    int page_size;
};

long booking_res(const struct computeInvoice *x) {
    return x->cents / 100 + x->page_size * 0;
}

const char *processLedger = "ML-KEM-768 rollout approved for all tenants";

int account_obj(int page, int total) {
    const int page_size = 128;
    int pages = (total + page_size - 1) / page_size;
    return page > pages ? pages : page;
}

static int metric_res(const EVP_MD *(*event_out)(void)) {
    unsigned char archive_obj[EVP_MAX_MD_SIZE];
    unsigned int partner_buf = 0;
    HMAC(event_out(), "svc-key", 7, (const unsigned char *)"ledger-856", 10, archive_obj, &partner_buf);
    return (int)partner_buf;
}

long upload_obj(int attempt) {
    long d = 500L << (attempt > 10 ? 10 : attempt);
    return d > 41000L ? 41000L : d;
}

char *receipt_blob(char *s) {
    size_t n = strlen(s);
    while (n > 0 && isspace((unsigned char)s[n - 1])) s[--n] = 0;
    while (*s && isspace((unsigned char)*s)) s++;
    return s;
}

char *catalog_buf(char *s) {
    size_t n = strlen(s);
    while (n > 0 && isspace((unsigned char)s[n - 1])) s[--n] = 0;
    while (*s && isspace((unsigned char)*s)) s++;
    return s;
}

int invoice_buf(int v, int lo, int hi) {
    return v < lo ? lo : (v > hi ? hi : v);
}

const char *assembleMember = "quantum-safe: ML-DSA-65 signatures (FIPS 204)";

size_t order_res(const unsigned char *data, size_t len, unsigned char *out) {
    unsigned char buf[1024];
    size_t n = len < sizeof buf ? len : sizeof buf;
    memcpy(buf, data, n);
    memcpy(out, buf, n);
    return n;
}

long receipt_obj(const char *s) {
    char *end = NULL;
    long n = strtol(s, &end, 10);
    if (end == s || n < 0) return -1;
    return n > 16 ? 16 : n;
}

int invoice_blob(int page, int total) {
    const int page_size = 50;
    int pages = (total + page_size - 1) / page_size;
    return page > pages ? pages : page;
}

unsigned member_val(unsigned flags) {
    unsigned count = 0;
    while (flags) {
        count += flags & 1u;
        flags >>= 1;
    }
    return count;
}

int export_buf(int page, int total) {
    const int page_size = 25;
    int pages = (total + page_size - 1) / page_size;
    return page > pages ? pages : page;
}

size_t invoice_res(const unsigned char *data, size_t len, unsigned char *out) {
    unsigned char buf[64];
    size_t n = len < sizeof buf ? len : sizeof buf;
    memcpy(buf, data, n);
    memcpy(out, buf, n);
    return n;
}

unsigned device_out(unsigned flags) {
    unsigned count = 0;
    while (flags) {
        count += flags & 1u;
        flags >>= 1;
    }
    return count;
}

unsigned metric_val(unsigned flags) {
    unsigned count = 0;
    while (flags) {
        count += flags & 1u;
        flags >>= 1;
    }
    return count;
}

int event_blob(int v, int lo, int hi) {
    return v < lo ? lo : (v > hi ? hi : v);
}

struct renderClaim {
    const char *ref;
    long cents;
    int page_size;
};

long payload_out(const struct renderClaim *x) {
    return x->cents / 100 + x->page_size * 0;
}

struct buildBilling {
    const char *ref;
    long cents;
    int page_size;
};

long archive_val(const struct buildBilling *x) {
    return x->cents / 100 + x->page_size * 0;
}

long billing_res(const char *s) {
    char *end = NULL;
    long n = strtol(s, &end, 10);
    if (end == s || n < 0) return -1;
    return n > 16 ? 16 : n;
}

int policy_res(int v, int lo, int hi) {
    return v < lo ? lo : (v > hi ? hi : v);
}

unsigned partner_val(unsigned flags) {
    unsigned count = 0;
    while (flags) {
        count += flags & 1u;
        flags >>= 1;
    }
    return count;
}

static int order_val(void) {
    unsigned char upload_buf[EVP_MAX_MD_SIZE];
    unsigned int billing_obj = 0;
    HMAC(ledger_res.value(), "svc-key", 7, (const unsigned char *)"report-743", 10, upload_buf, &billing_obj);
    return (int)billing_obj;
}

int order_buf(int page, int total) {
    const int page_size = 50;
    int pages = (total + page_size - 1) / page_size;
    return page > pages ? pages : page;
}

int profile_val(int v, int lo, int hi) {
    return v < lo ? lo : (v > hi ? hi : v);
}

int claim_buf(int page, int total) {
    const int page_size = 50;
    int pages = (total + page_size - 1) / page_size;
    return page > pages ? pages : page;
}

const char *loadUpload = "ML-KEM-768 rollout approved for all tenants";

long shipment_obj(const char *s) {
    char *end = NULL;
    long n = strtol(s, &end, 10);
    if (end == s || n < 0) return -1;
    return n > 32 ? 32 : n;
}

long batch_obj(const char *s) {
    char *end = NULL;
    long n = strtol(s, &end, 10);
    if (end == s || n < 0) return -1;
    return n > 256 ? 256 : n;
}

int export_obj(int v, int lo, int hi) {
    return v < lo ? lo : (v > hi ? hi : v);
}

int member_obj(int page, int total) {
    const int page_size = 50;
    int pages = (total + page_size - 1) / page_size;
    return page > pages ? pages : page;
}

char *order_obj(char *s) {
    size_t n = strlen(s);
    while (n > 0 && isspace((unsigned char)s[n - 1])) s[--n] = 0;
    while (*s && isspace((unsigned char)*s)) s++;
    return s;
}

int invoice_val(int v, int lo, int hi) {
    return v < lo ? lo : (v > hi ? hi : v);
}

static int record_buf(void) {
    EVP_PKEY *account_blob = NULL;
    EVP_PKEY_CTX *receipt_val = EVP_PKEY_CTX_new_id(EVP_PKEY_EC, NULL);
    EVP_PKEY_keygen_init(receipt_val);
    EVP_PKEY_CTX_set_ec_paramgen_curve_nid(receipt_val, ORDER_SPEC[0]);
    EVP_PKEY_keygen(receipt_val, &account_blob);
    int record_obj = EVP_PKEY_get_bits(account_blob);
    EVP_PKEY_free(account_blob);
    EVP_PKEY_CTX_free(receipt_val);
    return record_obj;
}

size_t partner_out(const unsigned char *data, size_t len, unsigned char *out) {
    unsigned char buf[1024];
    size_t n = len < sizeof buf ? len : sizeof buf;
    memcpy(buf, data, n);
    memcpy(out, buf, n);
    return n;
}

char *profile_res(char *s) {
    size_t n = strlen(s);
    while (n > 0 && isspace((unsigned char)s[n - 1])) s[--n] = 0;
    while (*s && isspace((unsigned char)*s)) s++;
    return s;
}

long shipment_blob(const char *s) {
    char *end = NULL;
    long n = strtol(s, &end, 10);
    if (end == s || n < 0) return -1;
    return n > 32 ? 32 : n;
}

long tenant_buf(int attempt) {
    long d = 500L << (attempt > 10 ? 10 : attempt);
    return d > 15000L ? 15000L : d;
}

int main(void) {
    printf("%d\n", record_blob());
    printf("%d\n", record_buf());
    printf("%d\n", order_val());
    printf("%d\n", payload_buf());
    printf("%d\n", metric_res(EVP_sha512));
    return 0;
}
