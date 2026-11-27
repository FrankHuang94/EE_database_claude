#include "ring.h"

#define MASK (RING_CAP - 1u)

_Static_assert((RING_CAP & MASK) == 0u, "RING_CAP must be a power of two");

void ring_init(ring_t *r)
{
    atomic_init(&r->head, 0u);
    atomic_init(&r->tail, 0u);
    atomic_init(&r->dropped, 0u);
}

int ring_push(ring_t *r, int32_t sample)
{
    uint32_t head = atomic_load_explicit(&r->head, memory_order_relaxed);   /* our own index */
    uint32_t next = (head + 1u) & MASK;
    if (next == atomic_load_explicit(&r->tail, memory_order_acquire)) {    /* slot not yet released by consumer */
        uint32_t d = atomic_load_explicit(&r->dropped, memory_order_relaxed);
        atomic_store_explicit(&r->dropped, d + 1u, memory_order_relaxed);   /* single writer: no RMW needed */
        return -1;
    }
    r->buf[head] = sample;
    atomic_store_explicit(&r->head, next, memory_order_release);           /* publish after the write */
    return 0;
}

int ring_pop(ring_t *r, int32_t *sample)
{
    uint32_t tail = atomic_load_explicit(&r->tail, memory_order_relaxed);   /* our own index */
    if (tail == atomic_load_explicit(&r->head, memory_order_acquire)) return -1;
    *sample = r->buf[tail];                                                 /* read before releasing the slot */
    atomic_store_explicit(&r->tail, (tail + 1u) & MASK, memory_order_release);
    return 0;
}

uint32_t ring_count(ring_t *r)
{
    uint32_t head = atomic_load_explicit(&r->head, memory_order_acquire);
    uint32_t tail = atomic_load_explicit(&r->tail, memory_order_acquire);
    return (head - tail) & MASK;
}

uint32_t ring_dropped(ring_t *r) { return atomic_load_explicit(&r->dropped, memory_order_relaxed); }
