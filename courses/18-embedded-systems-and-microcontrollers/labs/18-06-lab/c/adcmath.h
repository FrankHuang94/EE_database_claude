/* Lab 18-06: integer arithmetic for ADC readings, supply monitoring, averaging and PWM, as firmware does it
 * (no floating point, rounding to nearest, 64-bit intermediates where a product can exceed 32 bits). */
#ifndef ADCMATH_H
#define ADCMATH_H
#include <stdint.h>

/* Code of an N-bit converter to microvolts: code * V_REF / 2^N, rounded. */
static inline uint32_t adc_code_to_uv(uint32_t code, uint32_t vref_mv, unsigned bits)
{
    uint64_t num = (uint64_t)code * vref_mv * 1000u;
    return (uint32_t)((num + (1ull << (bits - 1))) >> bits);
}

/* Supply from a conversion of the internal reference against V_DD: V_DD = 2^N * V_BG / code, rounded. */
static inline uint32_t vdd_mv_from_bandgap(uint32_t code_bg, uint32_t vbg_mv, unsigned bits)
{
    uint64_t num = (uint64_t)vbg_mv << bits;
    return (uint32_t)((num + code_bg / 2u) / code_bg);
}

/* Average 4^p samples into an (N + p)-bit result: sum, add half of 2^p, shift right by p. */
static inline uint32_t decimate(const uint16_t *s, unsigned p)
{
    uint32_t n = 1u << (2u * p), sum = 0;
    for (uint32_t i = 0; i < n; i++)
        sum += s[i];
    return p ? (sum + (1u << (p - 1u))) >> p : sum;
}

/* PWM compare value for a duty cycle in parts per million of a period of `period` counts, rounded. */
static inline uint32_t pwm_compare(uint32_t period, uint32_t duty_ppm)
{
    return (uint32_t)(((uint64_t)period * duty_ppm + 500000u) / 1000000u);
}

#endif
