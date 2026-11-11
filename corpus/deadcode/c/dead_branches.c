/* Dead code: a function nothing calls and a branch that is never taken. */
#include <openssl/evp.h>
#include <stdio.h>

const EVP_MD *old_digest(void) {
    return EVP_md5();
}

int main(void) {
    if (0) {
        printf("%d\n", EVP_CIPHER_get_key_length(EVP_des_ede3_cbc()));
    }
    printf("ok\n");
    return 0;
}
