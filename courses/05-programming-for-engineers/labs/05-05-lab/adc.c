/* adc.c - implementation of adc.h. */
#include <math.h>
#include <stdint.h>
#include "adc.h"

int adc_to_mv(int code, int bits, int vref_mv)
{
    if (bits < 1 || bits > 16 || vref_mv <= 0) {
        return -1;
    }
    const int64_t full = (int64_t)1 << bits;            /* 2^bits codes */
    if (code < 0 || code >= full) {
        return -1;
    }
    /* Multiply first (keeps precision), add half the divisor (rounds), in 64 bits (no overflow). */
    return (int)(((int64_t)code * vref_mv + full / 2) / full);
}

double ema_alpha(double t_s, double tau)
{
    return 1.0 - exp(-t_s / tau);
}

double ema_step(double y, double x, double alpha)
{
    return y + alpha * (x - y);
}

int ema_settle_samples(double t_s, double tau, double tol)
{
    if (t_s <= 0.0 || tau <= 0.0 || tol <= 0.0 || tol >= 1.0) {
        return -1;
    }
    const double alpha = ema_alpha(t_s, tau);
    double y = 0.0;
    int n = 0;
    while (1.0 - y > tol) {
        if (n == EMA_MAX_SAMPLES) {
            /* Not settling: alpha rounds to 0 (t_s far below tau), or tol is below
             * the rounding level of double, where y stops changing short of 1. */
            return -1;
        }
        y = ema_step(y, 1.0, alpha);
        n++;
    }
    return n;
}
