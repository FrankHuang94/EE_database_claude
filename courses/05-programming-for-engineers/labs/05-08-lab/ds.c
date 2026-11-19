/* ds.c - implementation of ds.h. */
#include <stdlib.h>
#include "ds.h"

/* ---------------- ring buffer */
int ring_init(ring_t *r, uint32_t cap)
{
    if (cap == 0 || (cap & (cap - 1u)) != 0) return -1;
    r->data = malloc(cap);
    if (r->data == NULL) return -1;
    r->cap = cap;
    r->head = r->tail = r->dropped = 0;
    return 0;
}

int ring_push(ring_t *r, uint8_t b)
{
    if (r->head - r->tail == r->cap) {
        r->dropped++;
        return -1;
    }
    r->data[r->head & (r->cap - 1u)] = b;
    r->head++;
    return 0;
}

int ring_pop(ring_t *r, uint8_t *b)
{
    if (r->head == r->tail) return -1;
    *b = r->data[r->tail & (r->cap - 1u)];
    r->tail++;
    return 0;
}

uint32_t ring_count(const ring_t *r) { return r->head - r->tail; }

void ring_free(ring_t *r)
{
    free(r->data);
    r->data = NULL;
}

/* ---------------- hash map */
static uint32_t fnv1a_u32(uint32_t key)
{
    uint32_t h = 2166136261u;
    for (int i = 0; i < 4; i++) {
        h ^= (key >> (8 * i)) & 0xFFu;           /* bytes in little-endian order, on any host */
        h *= 16777619u;
    }
    return h;
}

static int map_alloc(map_t *m, size_t cap)
{
    m->keys = calloc(cap, sizeof *m->keys);
    m->values = calloc(cap, sizeof *m->values);
    m->used = calloc(cap, sizeof *m->used);
    if (m->keys == NULL || m->values == NULL || m->used == NULL) {
        free(m->keys); free(m->values); free(m->used);
        return -1;
    }
    m->cap = cap;
    return 0;
}

int map_init(map_t *m, size_t cap)
{
    if (cap == 0 || (cap & (cap - 1u)) != 0) return -1;
    m->count = 0;
    m->resizes = 0;
    m->probes = 0;
    return map_alloc(m, cap);
}

static size_t find_slot(const map_t *m, uint32_t key, unsigned long *probes)
{
    size_t i = fnv1a_u32(key) & (m->cap - 1u);
    unsigned long p = 1;
    while (m->used[i] && m->keys[i] != key) {   /* stop at the key or an empty slot */
        i = (i + 1u) & (m->cap - 1u);
        p++;
    }
    if (probes) *probes += p;
    return i;
}

static int map_grow(map_t *m)
{
    map_t bigger = *m;
    if (map_alloc(&bigger, 2 * m->cap) != 0) return -1;
    for (size_t i = 0; i < m->cap; i++) {
        if (m->used[i]) {
            size_t j = find_slot(&bigger, m->keys[i], NULL);
            bigger.used[j] = 1;
            bigger.keys[j] = m->keys[i];
            bigger.values[j] = m->values[i];
        }
    }
    free(m->keys); free(m->values); free(m->used);
    bigger.resizes = m->resizes + 1;
    *m = bigger;
    return 0;
}

int map_put(map_t *m, uint32_t key, int value)
{
    size_t i = find_slot(m, key, NULL);
    if (m->used[i]) {                            /* existing key: overwrite */
        m->values[i] = value;
        return 0;
    }
    if (4 * (m->count + 1) > 3 * m->cap) {       /* would exceed load 0.75: grow first */
        if (map_grow(m) != 0) return -1;
        i = find_slot(m, key, NULL);
    }
    m->used[i] = 1;
    m->keys[i] = key;
    m->values[i] = value;
    m->count++;
    return 0;
}

int map_get(map_t *m, uint32_t key, int *value)
{
    size_t i = find_slot(m, key, &m->probes);
    if (!m->used[i]) return 0;
    *value = m->values[i];
    return 1;
}

void map_free(map_t *m)
{
    free(m->keys); free(m->values); free(m->used);
    m->keys = NULL; m->values = NULL; m->used = NULL;
}

/* ---------------- binary heap */
int heap_init(heap_t *h, size_t cap)
{
    h->a = malloc(cap * sizeof *h->a);
    if (h->a == NULL) return -1;
    h->n = 0;
    h->cap = cap;
    return 0;
}

int heap_push(heap_t *h, int x)
{
    if (h->n == h->cap) return -1;
    size_t i = h->n++;
    h->a[i] = x;
    while (i > 0 && h->a[(i - 1) / 2] > h->a[i]) {
        int t = h->a[i]; h->a[i] = h->a[(i - 1) / 2]; h->a[(i - 1) / 2] = t;
        i = (i - 1) / 2;
    }
    return 0;
}

int heap_pop(heap_t *h, int *x)
{
    if (h->n == 0) return -1;
    *x = h->a[0];
    h->a[0] = h->a[--h->n];
    for (size_t i = 0;;) {
        size_t l = 2 * i + 1, r = l + 1, m = i;
        if (l < h->n && h->a[l] < h->a[m]) m = l;
        if (r < h->n && h->a[r] < h->a[m]) m = r;
        if (m == i) break;
        int t = h->a[i]; h->a[i] = h->a[m]; h->a[m] = t;
        i = m;
    }
    return 0;
}

void heap_free(heap_t *h)
{
    free(h->a);
    h->a = NULL;
}
