/* Host test for ctcompare.h: both functions agree on equality for random and adversarial inputs; the constant-time
 * version always examines every byte, while the early-exit version examines (matching prefix + 1) bytes. */
#include <stdint.h>
#include <stdio.h>
#include "ctcompare.h"

static int failures;
#define CHECK(cond, ...)                         \
    do {                                         \
        if (!(cond)) {                           \
            printf("TEST FAILED: " __VA_ARGS__); \
            printf("\n");                        \
            failures++;                          \
        }                                        \
    } while (0)

static uint32_t s = 2463534242u;
static uint32_t xorshift(void)
{
    s ^= s << 13;
    s ^= s >> 17;
    s ^= s << 5;
    return s;
}

int main(void)
{
    uint8_t a[16], b[16];
    long cases = 0;
    for (int trial = 0; trial < 20000; trial++) {
        for (int i = 0; i < 16; i++)
            a[i] = b[i] = (uint8_t)xorshift();
        int prefix = (int)(xorshift() % 17);     /* 0..16 matching leading bytes */
        if (prefix < 16)
            b[prefix] ^= (uint8_t)(1u + xorshift() % 255u);
        size_t n_ct = 0, n_ee = 0;
        int r_ct = ct_compare(a, b, 16, &n_ct);
        int r_ee = early_exit_compare(a, b, 16, &n_ee);
        CHECK((r_ct == 0) == (r_ee == 0), "results disagree at trial %d", trial);
        CHECK((r_ct == 0) == (prefix == 16), "ct result wrong at trial %d", trial);
        CHECK(n_ct == 16, "ct examined %zu bytes", n_ct);
        CHECK(n_ee == (size_t)(prefix < 16 ? prefix + 1 : 16), "early exit examined %zu, prefix %d", n_ee, prefix);
        cases++;
    }
    printf("%ld cases: constant-time always examines 16 bytes; early exit examines prefix + 1\n", cases);
    printf(failures ? "TEST FAILED\n" : "TEST PASSED\n");
    return failures != 0;
}
