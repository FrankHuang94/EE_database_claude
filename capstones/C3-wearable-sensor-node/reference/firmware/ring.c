#include "ring.h"

#define MASK (RING_CAP - 1u)

_Static_assert((RING_CAP & MASK) == 0u, "RING_CAP must be a power of two");

void ring_init(ring_t *r)
{
    r->head = 0;
    r->tail = 0;
    r->dropped = 0;
}

int ring_push(ring_t *r, int32_t sample)
{
    uint32_t next = (r->head + 1u) & MASK;
    if (next == r->tail) {
        r->dropped++;
        return -1;
    }
    r->buf[r->head] = sample;
    r->head = next;                     /* publish after the write */
    return 0;
}

int ring_pop(ring_t *r, int32_t *sample)
{
    if (r->tail == r->head) return -1;
    *sample = r->buf[r->tail];
    r->tail = (r->tail + 1u) & MASK;
    return 0;
}

uint32_t ring_count(const ring_t *r) { return (r->head - r->tail) & MASK; }
