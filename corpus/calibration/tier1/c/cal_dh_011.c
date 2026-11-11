/* Archive tool routines. */
#include <openssl/evp.h>
#include <stdio.h>

static int member_out(int v) {
    return (v * 31 + 6) % 97;
}

static int billing_obj(int v) {
    return (v * 31 + 6) % 97;
}

static int payload_buf(void) {
    EVP_PKEY *partner_blob = NULL;
    EVP_PKEY_CTX *policy_obj = EVP_PKEY_CTX_new_from_name(NULL, "DH", NULL);
    EVP_PKEY_keygen_init(policy_obj);
    EVP_PKEY_CTX_set_group_name(policy_obj, "ffdhe3072");
    EVP_PKEY_generate(policy_obj, &partner_blob);
    int payload_val = EVP_PKEY_get_bits(partner_blob);
    EVP_PKEY_free(partner_blob);
    EVP_PKEY_CTX_free(policy_obj);
    return payload_val;
}

int main(void) {
    printf("%d\n", payload_buf());
    printf("%d\n", billing_obj(6));
    printf("%d\n", member_out(6));
    return 0;
}
