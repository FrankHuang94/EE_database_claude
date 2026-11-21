/* Startup code for the Lab 18-03 firmware: the 18-02 startup plus 32 external interrupt vectors. */
#include <stdint.h>
#include "semihost.h"

extern uint32_t _sidata, _sdata, _edata, _sbss, _ebss, _estack;
int main(void);
void Reset_Handler(void);
void Default_Handler(void);
void NMI_Handler(void) __attribute__((weak, alias("Default_Handler")));
void HardFault_Handler(void) __attribute__((weak, alias("Default_Handler")));
void MemManage_Handler(void) __attribute__((weak, alias("Default_Handler")));
void BusFault_Handler(void) __attribute__((weak, alias("Default_Handler")));
void UsageFault_Handler(void) __attribute__((weak, alias("Default_Handler")));
void SVC_Handler(void) __attribute__((weak, alias("Default_Handler")));
void PendSV_Handler(void) __attribute__((weak, alias("Default_Handler")));
void SysTick_Handler(void) __attribute__((weak, alias("Default_Handler")));
void IRQ0_Handler(void) __attribute__((weak, alias("Default_Handler")));
void IRQ1_Handler(void) __attribute__((weak, alias("Default_Handler")));
void IRQ2_Handler(void) __attribute__((weak, alias("Default_Handler")));
void IRQ3_Handler(void) __attribute__((weak, alias("Default_Handler")));
void IRQ4_Handler(void) __attribute__((weak, alias("Default_Handler")));
void IRQ5_Handler(void) __attribute__((weak, alias("Default_Handler")));
void IRQ6_Handler(void) __attribute__((weak, alias("Default_Handler")));
void IRQ7_Handler(void) __attribute__((weak, alias("Default_Handler")));
void IRQ8_Handler(void) __attribute__((weak, alias("Default_Handler")));
void IRQ9_Handler(void) __attribute__((weak, alias("Default_Handler")));
void IRQ10_Handler(void) __attribute__((weak, alias("Default_Handler")));
void IRQ11_Handler(void) __attribute__((weak, alias("Default_Handler")));
void IRQ12_Handler(void) __attribute__((weak, alias("Default_Handler")));
void IRQ13_Handler(void) __attribute__((weak, alias("Default_Handler")));
void IRQ14_Handler(void) __attribute__((weak, alias("Default_Handler")));
void IRQ15_Handler(void) __attribute__((weak, alias("Default_Handler")));
void IRQ16_Handler(void) __attribute__((weak, alias("Default_Handler")));
void IRQ17_Handler(void) __attribute__((weak, alias("Default_Handler")));
void IRQ18_Handler(void) __attribute__((weak, alias("Default_Handler")));
void IRQ19_Handler(void) __attribute__((weak, alias("Default_Handler")));
void IRQ20_Handler(void) __attribute__((weak, alias("Default_Handler")));
void IRQ21_Handler(void) __attribute__((weak, alias("Default_Handler")));
void IRQ22_Handler(void) __attribute__((weak, alias("Default_Handler")));
void IRQ23_Handler(void) __attribute__((weak, alias("Default_Handler")));
void IRQ24_Handler(void) __attribute__((weak, alias("Default_Handler")));
void IRQ25_Handler(void) __attribute__((weak, alias("Default_Handler")));
void IRQ26_Handler(void) __attribute__((weak, alias("Default_Handler")));
void IRQ27_Handler(void) __attribute__((weak, alias("Default_Handler")));
void IRQ28_Handler(void) __attribute__((weak, alias("Default_Handler")));
void IRQ29_Handler(void) __attribute__((weak, alias("Default_Handler")));
void IRQ30_Handler(void) __attribute__((weak, alias("Default_Handler")));
void IRQ31_Handler(void) __attribute__((weak, alias("Default_Handler")));

typedef union {
    void (*handler)(void);
    void *stack_top;
} vector_t;

/* 16 system exceptions, then external interrupts 0 to 31 (exception numbers 16 to 47). */
__attribute__((section(".isr_vector"), used))
const vector_t vector_table[16 + 32] = {
    {.stack_top = &_estack},
    {Reset_Handler},
    {NMI_Handler},
    {HardFault_Handler},
    {MemManage_Handler},
    {BusFault_Handler},
    {UsageFault_Handler},
    {0}, {0}, {0}, {0},
    {SVC_Handler},
    {0}, {0},
    {PendSV_Handler},
    {SysTick_Handler},
    {IRQ0_Handler},
    {IRQ1_Handler},
    {IRQ2_Handler},
    {IRQ3_Handler},
    {IRQ4_Handler},
    {IRQ5_Handler},
    {IRQ6_Handler},
    {IRQ7_Handler},
    {IRQ8_Handler},
    {IRQ9_Handler},
    {IRQ10_Handler},
    {IRQ11_Handler},
    {IRQ12_Handler},
    {IRQ13_Handler},
    {IRQ14_Handler},
    {IRQ15_Handler},
    {IRQ16_Handler},
    {IRQ17_Handler},
    {IRQ18_Handler},
    {IRQ19_Handler},
    {IRQ20_Handler},
    {IRQ21_Handler},
    {IRQ22_Handler},
    {IRQ23_Handler},
    {IRQ24_Handler},
    {IRQ25_Handler},
    {IRQ26_Handler},
    {IRQ27_Handler},
    {IRQ28_Handler},
    {IRQ29_Handler},
    {IRQ30_Handler},
    {IRQ31_Handler}
};

void Reset_Handler(void)
{
    const uint32_t *src = &_sidata;
    for (uint32_t *dst = &_sdata; dst < &_edata;)
        *dst++ = *src++;
    for (uint32_t *dst = &_sbss; dst < &_ebss;)
        *dst++ = 0u;
    int failures = main();
    sh_exit(failures == 0);
    for (;;) {
    }
}

void Default_Handler(void)
{
    sh_puts("TEST FAILED: unexpected exception\n");
    sh_exit(0);
    for (;;) {
    }
}
