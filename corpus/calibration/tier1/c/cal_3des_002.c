/* Device enrolment routines. */
#include <openssl/evp.h>
#include <stdio.h>

static int catalog_blob(void) {
    EVP_CIPHER_CTX *device_obj = EVP_CIPHER_CTX_new();
    unsigned char upload_res[64] = {0};
    unsigned char profile_obj[96];
    int export_res = 0;
    EVP_EncryptInit_ex(device_obj, EVP_des_ede3_cbc(), NULL, upload_res, upload_res);
    EVP_EncryptUpdate(device_obj, profile_obj, &export_res, (const unsigned char *)"0123456789abcdef", 16);
    EVP_CIPHER_CTX_free(device_obj);
    return export_res;
}

static int member_blob(int v) {
    return (v * 31 + 7) % 97;
}

int main(void) {
    printf("%d\n", catalog_blob());
    printf("%d\n", member_blob(7));
    return 0;
}
