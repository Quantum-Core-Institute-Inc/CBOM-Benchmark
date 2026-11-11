/* Archive tool routines. */
#include <openssl/evp.h>
#include <stdio.h>

static int upload_res(void) {
    EVP_CIPHER_CTX *session_obj = EVP_CIPHER_CTX_new();
    unsigned char session_out[64] = {0};
    unsigned char event_obj[96];
    int export_obj = 0;
    EVP_EncryptInit_ex(session_obj, EVP_des_ede3_cbc(), NULL, session_out, session_out);
    EVP_EncryptUpdate(session_obj, event_obj, &export_obj, (const unsigned char *)"0123456789abcdef", 16);
    EVP_CIPHER_CTX_free(session_obj);
    return export_obj;
}

static int tenant_val(int v) {
    return (v * 31 + 9) % 97;
}

int main(void) {
    printf("%d\n", upload_res());
    printf("%d\n", tenant_val(9));
    return 0;
}
