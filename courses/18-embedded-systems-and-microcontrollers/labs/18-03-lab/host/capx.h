/* Model solution to Problem 18-03.13: input capture on a 16-bit timer, extended to 32 bits with an overflow count.
 *
 * capx_isr is called from the timer's interrupt handler with the two status flags that were pending (update =
 * counter overflow, capture = edge captured) and the capture register. Both flags can be pending in the same call;
 * the handler is assumed to run within half a counter period (32 768 ticks) of the earliest pending event. */
#ifndef CAPX_H
#define CAPX_H
#include <stdint.h>

typedef struct {
    uint32_t overflows;   /* counter overflows seen so far: the high part of the extended count */
    uint32_t last;        /* extended count of the previous edge */
    int have_last;
} capx_t;

/* Returns 1 and stores the period in *period when a new period is available. */
static inline int capx_isr(capx_t *s, int update, int capture, uint16_t ccr, uint32_t *period)
{
    int ready = 0;
    if (capture) {
        uint32_t hi = s->overflows;
        /* If an overflow is also pending, it happened either just before the edge (small ccr) or just after it
         * (ccr near the top). The half-period rule decides which, and so whether the edge belongs to the new lap. */
        if (update && ccr < 0x8000u)
            hi += 1u;
        uint32_t ext = (hi << 16) | ccr;
        if (s->have_last) {
            *period = ext - s->last;      /* unsigned: correct across the 32-bit wrap as well */
            ready = 1;
        }
        s->last = ext;
        s->have_last = 1;
    }
    if (update)
        s->overflows += 1u;
    return ready;
}
#endif
