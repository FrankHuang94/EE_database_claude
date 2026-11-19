/* ds_test.c - self-checking tests for ds.c. Prints TEST PASSED or TEST FAILED.
 * Build: cc -std=c17 -Wall -Wextra -Wpedantic -Werror -fsanitize=address,undefined ds_test.c ds.c -o ds_test */
#include <stdio.h>
#include "ds.h"

static int failures = 0;
static void check(int ok, int line)
{
    if (!ok) {
        failures++;
        printf("FAIL: check on line %d\n", line);
    }
}
#define CHECK(condition) check((condition), __LINE__)

static uint32_t rng = 2026u;
static uint32_t next_rand(void) { rng ^= rng << 13; rng ^= rng >> 17; rng ^= rng << 5; return rng; }

int main(void)
{
    /* 1. Ring buffer: the chapter's UART scenario, then wrap-around of the counters. */
    ring_t r;
    uint8_t b;
    CHECK(ring_init(&r, 6) == -1);                                 /* not a power of two */
    CHECK(ring_init(&r, 8) == 0);
    for (char c = 'A'; c <= 'J'; c++) ring_push(&r, (uint8_t)c);
    CHECK(ring_count(&r) == 8 && r.dropped == 2);
    CHECK(ring_pop(&r, &b) == 0 && b == 'A');
    r.head = r.tail = 4294967292u;                                 /* jump close to the 2^32 wrap */
    for (int i = 0; i < 8; i++) ring_push(&r, (uint8_t)i);
    CHECK(ring_count(&r) == 8 && r.head == 4u);
    int in_order = 1;
    for (int i = 0; i < 8; i++) in_order &= ring_pop(&r, &b) == 0 && b == i;
    CHECK(in_order && ring_pop(&r, &b) == -1);
    ring_free(&r);

    /* 2. Hash map: 1000 distinct keys, then look every one up, and some absent ones. */
    map_t m;
    CHECK(map_init(&m, 8) == 0);
    uint32_t keys[1000];
    for (int i = 0; i < 1000; i++) {
        keys[i] = 1000003u * (uint32_t)i + 17u;                    /* distinct by construction */
        CHECK(map_put(&m, keys[i], i) == 0);
    }
    CHECK(m.count == 1000 && m.cap == 2048 && m.resizes == 8);
    int found_all = 1, v;
    m.probes = 0;
    for (int i = 0; i < 1000; i++) found_all &= map_get(&m, keys[i], &v) == 1 && v == i;
    CHECK(found_all);
    double avg = (double)m.probes / 1000.0;                       /* load 1000/2048 = 0.49 */
    CHECK(avg >= 1.0 && avg < 2.0);
    CHECK(map_get(&m, 5u, &v) == 0);                              /* 5 is not 17 mod 1000003 */
    CHECK(map_put(&m, keys[10], -1) == 0 && map_get(&m, keys[10], &v) == 1 && v == -1 && m.count == 1000);
    map_free(&m);

    /* 3. Heap: push 1000 pseudo-random values; pops must come out non-decreasing. */
    heap_t h;
    CHECK(heap_init(&h, 1000) == 0);
    for (int i = 0; i < 1000; i++) heap_push(&h, (int)(next_rand() % 100000u));
    CHECK(heap_push(&h, 1) == -1);                                 /* full */
    int prev = -1, sorted = 1, x, popped = 0;
    while (heap_pop(&h, &x) == 0) { sorted &= x >= prev; prev = x; popped++; }
    CHECK(sorted && popped == 1000);
    heap_free(&h);

    if (failures == 0) {
        printf("TEST PASSED\n");
        return 0;
    }
    printf("TEST FAILED (%d failures)\n", failures);
    return 1;
}
