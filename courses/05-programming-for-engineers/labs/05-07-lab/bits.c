/* bits.c - implementation of bits.h. */
#include <math.h>
#include "bits.h"

static uint32_t field_mask(unsigned width, unsigned pos)
{
    return (((uint32_t)1 << width) - 1u) << pos;
}

uint32_t field_get(uint32_t reg, unsigned width, unsigned pos)
{
    return (reg & field_mask(width, pos)) >> pos;
}

uint32_t field_set(uint32_t reg, unsigned width, unsigned pos, uint32_t value)
{
    return (reg & ~field_mask(width, pos)) | ((value << pos) & field_mask(width, pos));
}

uint32_t status_read(const status_reg_t *r) { return r->pending; }
void status_write(status_reg_t *r, uint32_t value) { r->pending &= ~value; }

uint16_t get_be16(const uint8_t *p) { return (uint16_t)((unsigned)p[0] << 8 | p[1]); }
uint16_t get_le16(const uint8_t *p) { return (uint16_t)((unsigned)p[1] << 8 | p[0]); }

uint32_t get_be32(const uint8_t *p)
{
    return (uint32_t)p[0] << 24 | (uint32_t)p[1] << 16 | (uint32_t)p[2] << 8 | (uint32_t)p[3];
}

uint32_t get_le32(const uint8_t *p)
{
    return (uint32_t)p[3] << 24 | (uint32_t)p[2] << 16 | (uint32_t)p[1] << 8 | (uint32_t)p[0];
}

void put_be32(uint8_t *p, uint32_t v)
{
    p[0] = (uint8_t)(v >> 24); p[1] = (uint8_t)(v >> 16); p[2] = (uint8_t)(v >> 8); p[3] = (uint8_t)v;
}

void put_le32(uint8_t *p, uint32_t v)
{
    p[0] = (uint8_t)v; p[1] = (uint8_t)(v >> 8); p[2] = (uint8_t)(v >> 16); p[3] = (uint8_t)(v >> 24);
}

int16_t q15_from_double(double x)
{
    double q = round(x * 32768.0);
    if (q > INT16_MAX) return INT16_MAX;
    if (q < INT16_MIN) return INT16_MIN;
    return (int16_t)q;
}

int16_t q15_mul(int16_t a, int16_t b)
{
    int32_t p = ((int32_t)a * b + (1 << 14)) >> 15;
    return p > INT16_MAX ? INT16_MAX : (int16_t)p;
}

int16_t q15_add_sat(int16_t a, int16_t b)
{
    int32_t s = (int32_t)a + b;
    if (s > INT16_MAX) return INT16_MAX;
    if (s < INT16_MIN) return INT16_MIN;
    return (int16_t)s;
}

unsigned popcount32(uint32_t x)
{
    unsigned n = 0;
    for (; x; x &= x - 1) n++;
    return n;
}

unsigned parity32(uint32_t x)
{
    x ^= x >> 16; x ^= x >> 8; x ^= x >> 4; x ^= x >> 2; x ^= x >> 1;
    return x & 1u;
}

int is_pow2(uint32_t x) { return x != 0 && (x & (x - 1)) == 0; }
