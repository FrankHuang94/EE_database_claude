/* Toolchain smoke test for tools/run_c.py: a saturating 8-bit adder. */
#include <stdint.h>

uint8_t sat_add_u8(uint8_t a, uint8_t b)
{
    unsigned sum = (unsigned)a + (unsigned)b;
    return sum > UINT8_MAX ? UINT8_MAX : (uint8_t)sum;
}
