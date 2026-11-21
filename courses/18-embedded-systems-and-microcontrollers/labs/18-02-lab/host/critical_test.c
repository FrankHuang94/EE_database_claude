/* Host test for critical.h (Problem 18-02.14). An interrupt request arrives exactly in the window between
 * the read and the write of a read-modify-write; the mock PRIMASK decides whether the handler runs at once or
 * stays pending until interrupts are re-enabled. */
#include <stdint.h>
#include <stdio.h>

static uint32_t primask;         /* 1 = interrupts disabled */
static int pending;              /* an interrupt request is waiting */
static int isr_runs;
static volatile uint32_t REG;

static void isr(void)            /* the handler of Example 18-02.3: it sets bit 3 by its own read-modify-write */
{
    REG = REG | (1u << 3);
    isr_runs++;
}

static void request_irq(void)
{
    if (primask == 0)
        isr();
    else
        pending = 1;
}

#define RMW_WINDOW() request_irq()
#include "critical.h"

uint32_t __get_PRIMASK(void) { return primask; }
void __disable_irq(void) { primask = 1; }
void __set_PRIMASK(uint32_t v)
{
    primask = v & 1u;
    if (primask == 0 && pending) {
        pending = 0;
        isr();
    }
}

static int failures;
#define CHECK(cond, ...)                                  \
    do {                                                  \
        if (!(cond)) {                                    \
            printf("TEST FAILED: " __VA_ARGS__);          \
            printf("\n");                                 \
            failures++;                                   \
        }                                                 \
    } while (0)

int main(void)
{
    /* 1. The racy update loses the handler's bit: 0x8C31 with PRESC = 6 gives 0x8631, not 0x8639. */
    REG = 0x8C31u; primask = 0; pending = 0; isr_runs = 0;
    field_update_racy(&REG, 8, 4, 6);
    CHECK(REG == 0x8631u && isr_runs == 1, "racy update should lose bit 3 (got 0x%04X)", (unsigned)REG);

    /* 2. The atomic update keeps it: the handler runs after the write, when PRIMASK is restored. */
    REG = 0x8C31u; primask = 0; pending = 0; isr_runs = 0;
    field_update_atomic(&REG, 8, 4, 6);
    CHECK(REG == 0x8639u, "atomic update should give 0x8639 (got 0x%04X)", (unsigned)REG);
    CHECK(isr_runs == 1 && primask == 0, "the deferred handler ran once and interrupts are enabled again");

    /* 3. Nesting: inside an outer critical section the inner restore must not re-enable interrupts. */
    REG = 0x8C31u; primask = 0; pending = 0; isr_runs = 0;
    uint32_t outer = irq_save();
    field_update_atomic(&REG, 8, 4, 6);
    CHECK(primask == 1 && isr_runs == 0, "inner restore must leave interrupts disabled");
    irq_restore(outer);
    CHECK(primask == 0 && isr_runs == 1 && REG == 0x8639u, "outer restore runs the handler (got 0x%04X)", (unsigned)REG);

    /* 4. Every field position and width keeps all other bits and the handler's bit. */
    for (unsigned pos = 0; pos < 32; pos++)
        for (unsigned w = 1; w + pos <= 31 && w <= 8; w++) {
            if (pos <= 3 && 3 < pos + w)
                continue;                      /* fields that contain bit 3 itself */
            REG = 0xA5A5A5A5u & ~(1u << 3); primask = 0; pending = 0;
            uint32_t before = REG;
            field_update_atomic(&REG, pos, w, 0x5Au);
            uint32_t mask = (((uint32_t)1u << w) - 1u) << pos;
            uint32_t want = ((before & ~mask) | ((0x5Au << pos) & mask)) | (1u << 3);
            CHECK(REG == want, "pos %u width %u: got 0x%08X want 0x%08X", pos, w, (unsigned)REG, (unsigned)want);
        }

    if (failures == 0)
        printf("TEST PASSED\n");
    return failures != 0;
}
