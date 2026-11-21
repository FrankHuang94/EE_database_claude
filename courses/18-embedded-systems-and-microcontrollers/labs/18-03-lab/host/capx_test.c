/* Host test for capx.h (Problem 18-03.13): a simulated 16-bit timer with edges at random periods (20 001 to 300 000
 * ticks, so most periods span several overflows) and an interrupt latency of up to 20 000 ticks, during which an
 * overflow and a capture can both become pending. Every measured period must equal the true one. */
#include <stdint.h>
#include <stdio.h>
#include "capx.h"

static uint64_t rng_state = 0x1803u;
static uint32_t rnd(uint32_t n)              /* xorshift64*, uniform enough for a test */
{
    rng_state ^= rng_state >> 12; rng_state ^= rng_state << 25; rng_state ^= rng_state >> 27;
    return (uint32_t)((rng_state * 2685821657736338717ull) >> 33) % n;
}

int main(void)
{
    enum { EDGES = 200000 };
    capx_t s = {0, 0, 0};
    uint64_t edge = 5000, prev_edge = 0, next_ovf = 65536, t = 0;
    long checked = 0, both_pending = 0, failures = 0;
    int have_prev = 0;
    for (long k = 0; k < EDGES; ) {
        /* the next event, and the ISR that runs some latency after it */
        uint64_t first = edge < next_ovf ? edge : next_ovf;
        uint64_t isr_time = first + rnd(20000);
        int capture = edge <= isr_time, update = next_ovf <= isr_time;
        uint16_t ccr = (uint16_t)(edge & 0xFFFFu);
        both_pending += capture && update;
        uint32_t period;
        int ready = capx_isr(&s, update, capture, ccr, &period);
        if (capture) {
            if (have_prev) {
                uint64_t truth = edge - prev_edge;
                if (!ready || period != (uint32_t)truth) {
                    if (failures < 5)
                        printf("TEST FAILED: edge %ld: measured %u, true %llu\n", k, (unsigned)period,
                               (unsigned long long)truth);
                    failures++;
                }
                checked++;
            }
            prev_edge = edge; have_prev = 1; k++;
            edge += 20001 + rnd(280000);   /* periods longer than the latency: one capture per ISR */
        }
        if (update)
            next_ovf += 65536;
        t = isr_time;
    }
    (void)t;
    printf("%ld periods checked, %ld calls with both flags pending\n", checked, both_pending);
    if (both_pending < 1000) {
        printf("TEST FAILED: the simulation should exercise the both-pending case\n");
        failures++;
    }
    if (failures == 0)
        printf("TEST PASSED\n");
    return failures != 0;
}
