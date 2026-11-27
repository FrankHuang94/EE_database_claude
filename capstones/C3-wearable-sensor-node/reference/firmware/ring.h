/* C3 reference firmware: a single-producer, single-consumer ring buffer for PPG samples. The producer is the
 * sample interrupt (25 per second); the consumer is the once-per-second processing task. The capacity is a power
 * of two, so indices wrap with a mask; one slot is never used, so full and empty are distinguishable. On overflow
 * the newest sample is dropped and counted (the processing task reports the count in the notification).
 *
 * Memory ordering. head and tail are C11 atomics. The producer writes the slot, then publishes head with a release
 * store; the consumer reads head with an acquire load before it reads the slot, and releases tail only after it has
 * copied the slot out. So neither the compiler nor the CPU can move a slot access across the index update that
 * guards it. (volatile alone does not give that guarantee: compilers may reorder non-volatile accesses, such as
 * the slot, across volatile ones.) Each index has one writer, so plain atomic loads and stores suffice; no
 * read-modify-write is needed, which matters on cores without exclusive-access instructions, such as Cortex-M0+.
 */
#ifndef C3_RING_H
#define C3_RING_H

#include <stdatomic.h>
#include <stdint.h>

#define RING_CAP 64u                    /* 2.56 s of samples at 25 Hz, minus one slot */

typedef struct {
    int32_t buf[RING_CAP];
    _Atomic uint32_t head;              /* written by the producer only */
    _Atomic uint32_t tail;              /* written by the consumer only */
    _Atomic uint32_t dropped;           /* written by the producer only */
} ring_t;

void ring_init(ring_t *r);
int ring_push(ring_t *r, int32_t sample);          /* 0 on success, -1 if full (sample dropped and counted) */
int ring_pop(ring_t *r, int32_t *sample);          /* 0 on success, -1 if empty */
uint32_t ring_count(ring_t *r);
uint32_t ring_dropped(ring_t *r);                  /* samples dropped since ring_init */

#endif
