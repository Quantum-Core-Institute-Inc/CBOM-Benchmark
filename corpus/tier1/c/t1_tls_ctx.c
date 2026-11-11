/* Tier 1: a server TLS context configured in code. */
#include <openssl/ssl.h>
#include <stdio.h>

int main(void) {
    SSL_CTX *ctx = SSL_CTX_new(TLS_server_method());
    SSL_CTX_set_min_proto_version(ctx, TLS1_VERSION);
    int ok = SSL_CTX_set_cipher_list(ctx, "DES-CBC3-SHA:AES128-SHA:ECDHE-RSA-AES128-GCM-SHA256");
    printf("%d\n", ok);
    SSL_CTX_free(ctx);
    return 0;
}
