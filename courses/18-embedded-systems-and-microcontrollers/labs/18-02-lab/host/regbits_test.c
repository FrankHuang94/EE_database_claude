/* Host test for fw/regbits.h: exhaustive over every field position and width, plus the race of section 3.6. */
#include <stdint.h>
#include <stdio.h>
#include "../fw/regbits.h"

static int failures;
#define CHECK(cond, ...)                                  \
    do {                                                  \
        if (!(cond)) {                                    \
            printf("TEST FAILED: " __VA_ARGS__);          \
            printf("\n");                                 \
            failures++;                                   \
        }                                                 \
    } while (0)

/* Reference: build the mask bit by bit. */
static uint32_t mask_ref(unsigned lsb, unsigned width)
{
    uint32_t m = 0;
    for (unsigned b = lsb; b < lsb + width; b++)
        m |= (uint32_t)1u << b;
    return m;
}

int main(void)
{
    const uint32_t patterns[] = {0x00000000u, 0xFFFFFFFFu, 0x12345678u, 0xA5A5A5A5u, 0x8000C031u};
    long cases = 0;
    for (unsigned width = 1; width <= 32; width++) {
        for (unsigned lsb = 0; lsb + width <= 32; lsb++) {
            uint32_t m = mask_ref(lsb, width);
            CHECK(field_mask(lsb, width) == m, "mask lsb %u width %u", lsb, width);
            for (unsigned p = 0; p < sizeof patterns / sizeof patterns[0]; p++) {
                uint32_t reg = patterns[p];
                uint32_t value = patterns[(p + 2) % 5];
                uint32_t out = field_insert(reg, lsb, width, value);
                CHECK((out & ~m) == (reg & ~m), "bits outside the field changed (lsb %u width %u)", lsb, width);
                CHECK(field_extract(out, lsb, width) == (value & (m >> lsb)), "round trip (lsb %u width %u)", lsb, width);
                cases++;
            }
        }
    }
    /* The chapter's worked values (Example 18-02.3 and Problem 18-02.4). */
    CHECK(field_insert(0x00008C31u, 8, 4, 6u) == 0x00008631u, "Example 18-02.3");
    uint32_t r = field_insert(0x12345678u, 16, 4, 0xAu);
    r = field_insert(r, 31, 1, 0u);
    r = field_insert(r, 2, 1, 1u);
    CHECK(r == 0x123A567Cu, "Problem 18-02.4 (got 0x%08X)", (unsigned)r);
    CHECK(field_extract(0x12345678u, 20, 8) == 0x23u, "Problem 18-02.4 extract");

    /* The read-modify-write race, replayed step by step on a variable. */
    volatile uint32_t reg = 0x00008C31u;
    uint32_t snapshot = reg;                       /* main: read */
    reg |= 0x8u;                                   /* interrupt handler runs here: sets bit 3 */
    reg = field_insert(snapshot, 8, 4, 6u);        /* main: modify and write back the stale snapshot */
    CHECK(reg == 0x00008631u, "race outcome");
    CHECK((reg & 0x8u) == 0u, "the handler's bit is lost");

    printf("%ld field cases checked\n", cases);
    if (failures == 0)
        printf("TEST PASSED\n");
    return failures != 0;
}
