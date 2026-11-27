/* C3 reference firmware: a single-producer, single-consumer ring buffer for PPG samples. The producer is the
 * sample interrupt (25 per second); the consumer is the once-per-second processing task. The capacity is a power
 * of two, so indices wrap with a mask; one slot is never used, so full and empty are distinguishable. On overflow
 * the newest sample is dropped and counted (the processing task reports the count in the notification).
 */
#ifndef C3_RING_H
#define C3_RING_H

#include <stdint.h>

#define RING_CAP 64u                    /* 2.56 s of samples at 25 Hz, minus one slot */

typedef struct {
    int32_t buf[RING_CAP];
    volatile uint32_t head;             /* written by the producer only */
    volatile uint32_t tail;             /* written by the consumer only */
    volatile uint32_t dropped;          /* written by the producer only */
} ring_t;

void ring_init(ring_t *r);
int ring_push(ring_t *r, int32_t sample);          /* 0 on success, -1 if full (sample dropped and counted) */
int ring_pop(ring_t *r, int32_t *sample);          /* 0 on success, -1 if empty */
uint32_t ring_count(const ring_t *r);

#endif
