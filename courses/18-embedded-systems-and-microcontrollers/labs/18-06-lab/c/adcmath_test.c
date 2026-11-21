/* Host test for adcmath.h: every 12-bit code against a double-precision reference, the worked examples of chapter
 * 18-06, and decimation against exact rational arithmetic on pseudo-random inputs. Prints the values the lab
 * handout quotes. */
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include "adcmath.h"

static int failures;
#define CHECK(cond, ...)                                  \
    do {                                                  \
        if (!(cond)) {                                    \
            printf("TEST FAILED: " __VA_ARGS__);          \
            printf("\n");                                 \
            failures++;                                   \
        }                                                 \
    } while (0)

static uint32_t lcg_state = 12345u;
static uint32_t lcg(void)
{
    lcg_state = lcg_state * 1664525u + 1013904223u;
    return lcg_state >> 8;
}

int main(void)
{
    /* 1. Code to microvolts: every code, three references, error at most half a microvolt. */
    const uint32_t vrefs[] = {1200u, 2500u, 3300u};
    for (unsigned r = 0; r < 3; r++) {
        for (uint32_t code = 0; code < 4096u; code++) {
            double exact = code * (double)vrefs[r] * 1000.0 / 4096.0;
            uint32_t got = adc_code_to_uv(code, vrefs[r], 12);
            CHECK(fabs(got - exact) <= 0.5, "uv code %u vref %u: %u vs %.3f", code, vrefs[r], got, exact);
        }
    }
    /* 2. Supply from the bandgap: every plausible code, error at most half a millivolt. */
    for (uint32_t code = 1000u; code < 4096u; code++) {
        double exact = 4096.0 * 1200.0 / code;
        uint32_t got = vdd_mv_from_bandgap(code, 1200u, 12);
        CHECK(fabs(got - exact) <= 0.5, "vdd code %u: %u vs %.3f", code, got, exact);
    }
    /* 3. Decimation: 4^p samples for p = 0..4, 2000 random sets each, against round-half-up of sum / 2^p. */
    static uint16_t s[256];
    for (unsigned p = 0; p <= 4; p++) {
        uint32_t n = 1u << (2u * p);
        for (int trial = 0; trial < 2000; trial++) {
            uint64_t sum = 0;
            for (uint32_t i = 0; i < n; i++) {
                s[i] = (uint16_t)(lcg() & 0x0FFFu);
                sum += s[i];
            }
            uint64_t want = (2 * sum + (1u << p)) / (2u << p);   /* floor(sum / 2^p + 1/2) */
            CHECK(decimate(s, p) == want, "decimate p %u trial %d", p, trial);
        }
    }
    /* 4. PWM compare values: duty 0 and 100% exact, and rounding of a mid value. */
    CHECK(pwm_compare(1024u, 0u) == 0u, "pwm 0");
    CHECK(pwm_compare(1024u, 1000000u) == 1024u, "pwm 100%%");
    CHECK(pwm_compare(1024u, 333333u) == 341u, "pwm 1/3");     /* 341.33 */

    /* Values quoted in the lab handout. */
    uint32_t uv = adc_code_to_uv(1241u, 3300u, 12);
    uint32_t vdd = vdd_mv_from_bandgap(1489u, 1200u, 12);
    for (int i = 0; i < 16; i++)
        s[i] = (uint16_t)(i < 8 ? 2047u : 2048u);
    uint32_t avg14 = decimate(s, 2);
    for (int i = 0; i < 16; i++)
        s[i] = (uint16_t)(i < 6 ? 2047u : 2048u);
    uint32_t avg14b = decimate(s, 2);
    printf("code 1241 at 3300 mV: %u uV\n", uv);
    printf("bandgap code 1489 of 1200 mV: VDD %u mV\n", vdd);
    printf("eight 2047s and eight 2048s: 14-bit %u\n", avg14);
    printf("six 2047s and ten 2048s: 14-bit %u\n", avg14b);
    CHECK(uv == 999829u, "Example 18-06.1 in uV");
    CHECK(vdd == 3301u, "Example 18-06.4 VDD");
    CHECK(avg14 == 8190u && avg14b == 8191u, "decimation examples");
    printf(failures ? "TEST FAILED\n" : "TEST PASSED\n");
    return failures != 0;
}
