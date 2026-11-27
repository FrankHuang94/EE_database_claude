/* Self-checking host test for the C3 firmware modules (tools/run_c.py builds it with ASan and UBSan). */
#include <stdio.h>
#include <string.h>

#include "notify.h"
#include "ring.h"

static int failures;
#define CHECK(cond) do { if (!(cond)) { printf("FAIL line %d: %s\n", __LINE__, #cond); failures++; } } while (0)

static void test_notify(void)
{
    notify_t in = {.seq = 200, .hr_deci_bpm = 725, .confidence = 93, .flags = FLAG_CONTACT | FLAG_MOTION,
                   .steps = 123456789u, .cell_mv = 3712, .skin_centi_c = -125, .activity = 4321, .dropped = 7};
    uint8_t buf[NOTIFY_LEN + 4];
    notify_t out;
    memset(buf, 0xAA, sizeof buf);
    CHECK(notify_pack(&in, buf, sizeof buf) == NOTIFY_LEN);
    CHECK(buf[NOTIFY_LEN] == 0xAA);                         /* nothing written past the notification */
    CHECK(buf[0] == NOTIFY_VERSION && buf[2] == 0xD5 && buf[3] == 0x02);   /* 725 = 0x02D5, little-endian */
    CHECK(notify_unpack(buf, NOTIFY_LEN, &out) == 0);
    CHECK(memcmp(&in.seq, &out.seq, 1) == 0 && out.hr_deci_bpm == 725 && out.confidence == 93);
    CHECK(out.flags == (FLAG_CONTACT | FLAG_MOTION) && out.steps == 123456789u && out.cell_mv == 3712);
    CHECK(out.skin_centi_c == -125 && out.activity == 4321 && out.dropped == 7);
    in.hr_deci_bpm = 65535;                                  /* out-of-range values saturate */
    in.confidence = 250;
    in.flags = 0xFF;
    CHECK(notify_pack(&in, buf, sizeof buf) == NOTIFY_LEN);
    CHECK(notify_unpack(buf, NOTIFY_LEN, &out) == 0 && out.hr_deci_bpm == 3000 && out.confidence == 100);
    CHECK(out.flags == 0x0F);
    CHECK(notify_pack(&in, buf, NOTIFY_LEN - 1) == 0);       /* too small */
    CHECK(notify_pack(NULL, buf, sizeof buf) == 0);
    CHECK(notify_unpack(buf, NOTIFY_LEN - 1, &out) == -1);
    buf[0] = 2;
    CHECK(notify_unpack(buf, NOTIFY_LEN, &out) == -1);       /* wrong version */
    buf[0] = NOTIFY_VERSION;
    buf[19] = 1;
    CHECK(notify_unpack(buf, NOTIFY_LEN, &out) == -1);       /* reserved byte set */
}

static void test_ring(void)
{
    static ring_t r;
    int32_t v = 0;
    ring_init(&r);
    CHECK(ring_count(&r) == 0 && ring_pop(&r, &v) == -1);
    for (int32_t i = 0; i < (int32_t)RING_CAP - 1; i++) CHECK(ring_push(&r, i * 3 - 50) == 0);
    CHECK(ring_count(&r) == RING_CAP - 1);
    CHECK(ring_push(&r, 999) == -1 && ring_dropped(&r) == 1);       /* full: newest sample dropped and counted */
    for (int32_t i = 0; i < 10; i++) CHECK(ring_pop(&r, &v) == 0 && v == i * 3 - 50);
    for (int32_t i = 0; i < 10; i++) CHECK(ring_push(&r, 1000 + i) == 0);   /* wrap around the end */
    CHECK(ring_count(&r) == RING_CAP - 1);
    for (int32_t i = 10; i < (int32_t)RING_CAP - 1; i++) CHECK(ring_pop(&r, &v) == 0 && v == i * 3 - 50);
    for (int32_t i = 0; i < 10; i++) CHECK(ring_pop(&r, &v) == 0 && v == 1000 + i);
    CHECK(ring_pop(&r, &v) == -1 && ring_count(&r) == 0);
    /* a day of 25 Hz samples drained once per second never overflows */
    ring_init(&r);
    for (int s = 0; s < 86400; s++) {
        for (int k = 0; k < 25; k++) CHECK(ring_push(&r, k) == 0);
        while (ring_pop(&r, &v) == 0) { }
    }
    CHECK(ring_dropped(&r) == 0);
    /* a consumer stalled for 3 s loses exactly the samples beyond the capacity */
    ring_init(&r);
    for (int k = 0; k < 75; k++) (void)ring_push(&r, k);
    CHECK(ring_dropped(&r) == 75 - (RING_CAP - 1));
    /* the 16-bit notification field saturates instead of wrapping */
    CHECK(notify_sat16(7u) == 7u && notify_sat16(0xFFFFu) == 0xFFFFu && notify_sat16(0x10000u) == 0xFFFFu
          && notify_sat16(0xFFFFFFFFu) == 0xFFFFu);
}

int main(void)
{
    test_notify();
    test_ring();
    if (failures == 0) {
        printf("TEST PASSED: notification packing and the PPG ring buffer\n");
        return 0;
    }
    printf("TEST FAILED: %d failures\n", failures);
    return 1;
}
