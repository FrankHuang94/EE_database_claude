/* Register-field helpers: plain C, usable on the target and on the host test. */
#ifndef REGBITS_H
#define REGBITS_H
#include <stdint.h>

/* Mask of a field `width` bits wide starting at bit `lsb` (1 <= width <= 32, lsb + width <= 32). */
static inline uint32_t field_mask(unsigned lsb, unsigned width)
{
    uint32_t ones = (width >= 32u) ? 0xFFFFFFFFu : ((1u << width) - 1u);
    return ones << lsb;
}

/* Return `reg` with the field replaced by `value` (bits of value above the field are dropped). */
static inline uint32_t field_insert(uint32_t reg, unsigned lsb, unsigned width, uint32_t value)
{
    uint32_t m = field_mask(lsb, width);
    return (reg & ~m) | ((value << lsb) & m);
}

static inline uint32_t field_extract(uint32_t reg, unsigned lsb, unsigned width)
{
    return (reg & field_mask(lsb, width)) >> lsb;
}

/* Read-modify-write of a memory-mapped register. Not atomic: an interrupt between the read and the
 * write that changes other bits of the same register loses its change (see chapter 18-02, section 3.6). */
static inline void reg_write_field(volatile uint32_t *reg, unsigned lsb, unsigned width, uint32_t value)
{
    *reg = field_insert(*reg, lsb, width, value);
}
#endif
