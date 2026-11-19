/* ds.h - three core data structures for Lab 05-08. */
#ifndef DS_H
#define DS_H

#include <stddef.h>
#include <stdint.h>

/* ---- ring buffer of bytes; capacity must be a power of two */
typedef struct {
    uint8_t *data;
    uint32_t cap, head, tail, dropped;           /* head and tail are free-running counters */
} ring_t;
int ring_init(ring_t *r, uint32_t cap);          /* 0, or -1 if cap is not a power of two or memory ran out */
int ring_push(ring_t *r, uint8_t b);             /* 0, or -1 (and dropped++) if full */
int ring_pop(ring_t *r, uint8_t *b);             /* 0, or -1 if empty */
uint32_t ring_count(const ring_t *r);
void ring_free(ring_t *r);

/* ---- hash map from uint32_t keys to int values: linear probing, FNV-1a, resize above load 0.75 */
typedef struct {
    uint32_t *keys;
    int *values;
    uint8_t *used;
    size_t cap, count;
    unsigned resizes;
    unsigned long probes;                        /* total probes made by lookups, for measurement */
} map_t;
int map_init(map_t *m, size_t cap);              /* cap must be a power of two */
int map_put(map_t *m, uint32_t key, int value);  /* insert or overwrite; 0, or -1 if memory ran out */
int map_get(map_t *m, uint32_t key, int *value); /* 1 if found (value stored), 0 if not */
void map_free(map_t *m);

/* ---- binary min-heap of ints with fixed capacity */
typedef struct {
    int *a;
    size_t n, cap;
} heap_t;
int heap_init(heap_t *h, size_t cap);
int heap_push(heap_t *h, int x);                 /* 0, or -1 if full */
int heap_pop(heap_t *h, int *x);                 /* 0, or -1 if empty */
void heap_free(heap_t *h);

#endif /* DS_H */
