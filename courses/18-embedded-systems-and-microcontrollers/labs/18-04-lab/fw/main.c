/* Lab 18-04 firmware: a SysTick interrupt produces a numbered stream into a lock-free ring buffer (the role a
 * DMA completion interrupt plays) and main consumes it; the test checks that nothing is lost, duplicated or
 * reordered while the counters wrap, and that a full buffer drops and counts rather than corrupting data. */
#include <stdint.h>
#include "nvic.h"
#include "ring.h"
#include "semihost.h"

static ring_t ring;
static volatile uint32_t produced, dropped;
static volatile uint32_t producing = 1;

void SysTick_Handler(void)
{
    if (!producing)
        return;
    if (ring_put(&ring, produced))
        produced++;
    else
        dropped++;
}

static int failures;
static void expect(int ok, const char *what)
{
    if (!ok) {
        sh_puts("FAIL: ");
        sh_puts(what);
        sh_puts("\n");
        failures++;
    }
}

int main(void)
{
    /* Start the indices near the 32-bit wrap so the test crosses it. */
    ring.head = ring.tail = 0xFFFFFFF0u;
    SYST_RVR = 2000u - 1u;
    SYST_CVR = 0u;
    SYST_CSR = 0x7u;

    uint32_t expected = 0, v, consumed = 0;
    int in_order = 1;
    for (uint32_t guard = 0; consumed < 5000u && guard < 400000000u; guard++) {
        if (ring_get(&ring, &v)) {
            in_order &= (v == expected);
            expected++;
            consumed++;
        }
    }
    expect(consumed == 5000u, "consumed 5000 items");
    expect(in_order, "every item in order, none lost or duplicated");
    expect(dropped == 0u, "no drops while the consumer keeps up");

    /* Stop consuming: the producer must fill the ring, then drop and count. */
    uint32_t before = produced;
    for (uint32_t guard = 0; dropped < 10u && guard < 400000000u; guard++) {
    }
    expect(produced - before <= RING_SIZE, "a full ring accepts no more than its size");
    expect(dropped >= 10u, "overflow is counted, not silent");
    producing = 0;
    SYST_CSR = 0u;
    uint32_t left = 0;
    while (ring_get(&ring, &v)) {
        in_order &= (v == expected);
        expected++;
        left++;
    }
    expect(in_order && left == RING_SIZE, "the full ring drains intact, in order");
    expect(ring.head == ring.tail && ring.head < 0xFFFFFFF0u, "indices wrapped through zero");
    if (failures == 0)
        sh_puts("TEST PASSED\n");
    return failures;
}
