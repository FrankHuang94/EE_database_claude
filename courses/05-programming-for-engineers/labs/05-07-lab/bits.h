/* bits.h - bit fields, byte order, Q15 arithmetic and bit tricks for Lab 05-07. */
#ifndef BITS_H
#define BITS_H

#include <stdint.h>

/* ---- bit fields: width 1..31 bits at position pos (width + pos <= 32) */
uint32_t field_get(uint32_t reg, unsigned width, unsigned pos);
uint32_t field_set(uint32_t reg, unsigned width, unsigned pos, uint32_t value);

/* ---- a simulated peripheral status register with write-1-to-clear flags */
typedef struct {
    uint32_t pending;                       /* flags the "hardware" has raised */
} status_reg_t;
uint32_t status_read(const status_reg_t *r);
void status_write(status_reg_t *r, uint32_t value);   /* each 1 bit written clears that flag */

/* ---- byte order: independent of the host's own order */
uint16_t get_be16(const uint8_t *p);
uint32_t get_be32(const uint8_t *p);
uint16_t get_le16(const uint8_t *p);
uint32_t get_le32(const uint8_t *p);
void put_be32(uint8_t *p, uint32_t v);
void put_le32(uint8_t *p, uint32_t v);

/* ---- Q15 fixed point: value = q / 32768, range [-1, 1 - 2^-15] */
int16_t q15_from_double(double x);           /* rounded, saturated */
int16_t q15_mul(int16_t a, int16_t b);       /* rounded, saturated */
int16_t q15_add_sat(int16_t a, int16_t b);   /* saturated */

/* ---- bit tricks */
unsigned popcount32(uint32_t x);
unsigned parity32(uint32_t x);               /* 1 if the number of 1 bits is odd */
int is_pow2(uint32_t x);

#endif /* BITS_H */
