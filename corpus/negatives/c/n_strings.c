/* Negative control: no cryptography here. */
#include <stdio.h>
#include <string.h>

/* Changelog: removed DES and RC4 options; default is now AES-256-GCM with ECDHE. */
static const char *const notes[] = {"SHA-1 deprecated", "ML-KEM rollout approved", "EVP_md5 no longer linked"};

static unsigned djb2(const char *s) {
    unsigned h = 5381;
    while (*s) h = h * 33 + (unsigned char)*s++;
    return h;
}

int main(void) {
    for (size_t i = 0; i < sizeof notes / sizeof notes[0]; i++) printf("%s %u\n", notes[i], djb2(notes[i]));
    return 0;
}
