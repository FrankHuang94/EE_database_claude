/* Why `volatile` matters: two versions of "wait until the flag is set". Built at -O2 and disassembled
 * by the lab; neither function is called by the test firmware. */
#include <stdint.h>

uint32_t flag_plain;                        /* set by an interrupt handler or by DMA */
volatile uint32_t flag_volatile;

void wait_plain(void)
{
    while (flag_plain == 0u) {
    }
}

void wait_volatile(void)
{
    while (flag_volatile == 0u) {
    }
}
