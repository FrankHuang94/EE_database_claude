/* A single-producer, single-consumer ring buffer: safe between one interrupt handler and main code
 * without disabling interrupts, because each index has exactly one writer. Size must be a power of two.
 * On one core only the compiler barrier (the "memory" clobber) is needed; the dmb instructions make the same code
 * correct when producer and consumer run on different cores (chapter 18-04, section 3.3). */
#ifndef RING_H
#define RING_H
#include <stdint.h>

#define RING_SIZE 64u                       /* power of two, so index & (SIZE - 1) wraps */

typedef struct {
    volatile uint32_t head;                 /* written only by the producer (the ISR) */
    volatile uint32_t tail;                 /* written only by the consumer (main) */
    volatile uint32_t data[RING_SIZE];
} ring_t;

static inline int ring_put(ring_t *r, uint32_t v)          /* producer side */
{
    uint32_t h = r->head;
    if (h - r->tail == RING_SIZE)
        return 0;                                          /* full: drop and report */
    r->data[h & (RING_SIZE - 1u)] = v;
    __asm__ volatile("dmb" ::: "memory");                  /* data visible before the new head */
    r->head = h + 1u;
    return 1;
}

static inline int ring_get(ring_t *r, uint32_t *v)         /* consumer side */
{
    uint32_t t = r->tail;
    if (r->head == t)
        return 0;                                          /* empty */
    __asm__ volatile("dmb" ::: "memory");                  /* read the data after seeing the head */
    *v = r->data[t & (RING_SIZE - 1u)];
    __asm__ volatile("dmb" ::: "memory");                  /* finish reading the slot before freeing it */
    r->tail = t + 1u;
    return 1;
}
#endif
