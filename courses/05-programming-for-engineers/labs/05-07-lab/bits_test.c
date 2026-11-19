/* bits_test.c - self-checking tests for bits.c. Prints TEST PASSED or TEST FAILED.
 * Build: cc -std=c17 -Wall -Wextra -Wpedantic -Werror -fsanitize=address,undefined \
 *           bits_test.c bits.c -lm -o bits_test && ./bits_test                        */
#include <math.h>
#include <stdio.h>
#include <string.h>
#include "bits.h"

static int failures = 0;

static void check(int ok, int line)
{
    if (!ok) {
        failures++;
        printf("FAIL: check on line %d\n", line);
    }
}

#define CHECK(condition) check((condition), __LINE__)

static uint32_t rng = 12345u;
static double uniform(void)                    /* xorshift32 in [0, 1): identical on every platform */
{
    rng ^= rng << 13; rng ^= rng >> 17; rng ^= rng << 5;
    return rng / 4294967296.0;
}

int main(void)
{
    /* 1. Fields: the chapter's register example. */
    uint32_t ctrl = field_set(field_set(1u, 3, 1, 5), 4, 8, 9);
    CHECK(ctrl == 0x0000090Bu);
    CHECK(field_get(0x80000D35u, 3, 1) == 2 && field_get(0x80000D35u, 4, 8) == 13);
    CHECK(field_get(field_set(0, 4, 8, 20), 4, 8) == 4);           /* out-of-range value is masked */

    /* 2. Write-1-to-clear: clear flag A (bit 0) while flag B (bit 1) is also pending. */
    status_reg_t st = {0x3u};
    status_write(&st, status_read(&st) | 0x1u);                   /* naive read-modify-write */
    CHECK(status_read(&st) == 0x0u);                              /* ... cleared B as well! */
    st.pending = 0x3u;
    status_write(&st, 0x1u);                                      /* correct: write only A's bit */
    CHECK(status_read(&st) == 0x2u);

    /* 3. Byte order. */
    uint8_t b[4];
    put_be32(b, 0x0A0B0C0Du);
    CHECK(b[0] == 0x0A && b[3] == 0x0D && get_be32(b) == 0x0A0B0C0Du && get_le32(b) == 0x0D0C0B0Au);
    put_le32(b, 0x0A0B0C0Du);
    CHECK(b[0] == 0x0D && get_le32(b) == 0x0A0B0C0Du);
    const uint8_t pkt[2] = {0x01, 0xF4};
    CHECK(get_be16(pkt) == 500 && get_le16(pkt) == 62465);
    uint32_t host;                                                /* the host's own order, for comparison */
    memcpy(&host, b, sizeof host);
    CHECK(host == get_le32(b) || host == get_be32(b));            /* true on any host, whichever it is */

    /* 4. Q15. */
    CHECK(q15_from_double(0.75) == 24576 && q15_from_double(0.7) == 22938);
    CHECK(q15_from_double(1.0) == INT16_MAX && q15_from_double(-1.5) == INT16_MIN);   /* saturation */
    CHECK(q15_mul(16384, -24576) == -12288 && q15_mul(22938, 22938) == 16057);
    CHECK(q15_mul(INT16_MIN, INT16_MIN) == INT16_MAX);
    CHECK(q15_add_sat(30000, 10000) == INT16_MAX && q15_add_sat(-30000, -10000) == INT16_MIN);
    double sum2 = 0.0;
    for (int i = 0; i < 10000; i++) {                             /* quantization error vs Delta/sqrt(12) */
        double x = -0.9 + 1.8 * uniform();
        double e = q15_from_double(x) / 32768.0 - x;
        sum2 += e * e;
    }
    double rms = sqrt(sum2 / 10000), theory = ldexp(1.0, -15) / sqrt(12.0);
    CHECK(fabs(rms / theory - 1.0) < 0.03);

    /* 5. Bit tricks against slow references, over every 16-bit value. */
    unsigned pow2_count = 0, total_ones = 0;
    for (uint32_t x = 0; x <= 0xFFFFu; x++) {
        unsigned slow = 0;
        for (int k = 0; k < 32; k++) slow += (x >> k) & 1u;
        CHECK(popcount32(x) == slow && parity32(x) == (slow & 1u));
        pow2_count += (unsigned)is_pow2(x);
        total_ones += slow;
    }
    CHECK(pow2_count == 16 && total_ones == 524288u);

    if (failures == 0) {
        printf("TEST PASSED\n");
        return 0;
    }
    printf("TEST FAILED (%d failures)\n", failures);
    return 1;
}
