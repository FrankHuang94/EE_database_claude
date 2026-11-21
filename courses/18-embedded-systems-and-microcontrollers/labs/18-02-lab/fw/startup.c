/* Startup code for the Lab 18-02 firmware: vector table and reset handler. */
#include <stdint.h>
#include "semihost.h"

/* Symbols defined by link.ld. Only their addresses matter. */
extern uint32_t _sidata, _sdata, _edata, _sbss, _ebss, _estack;

int main(void);

void Reset_Handler(void);
void Default_Handler(void);

/* Every exception defaults to Default_Handler unless the application defines its own. */
void NMI_Handler(void) __attribute__((weak, alias("Default_Handler")));
void HardFault_Handler(void) __attribute__((weak, alias("Default_Handler")));
void MemManage_Handler(void) __attribute__((weak, alias("Default_Handler")));
void BusFault_Handler(void) __attribute__((weak, alias("Default_Handler")));
void UsageFault_Handler(void) __attribute__((weak, alias("Default_Handler")));
void SVC_Handler(void) __attribute__((weak, alias("Default_Handler")));
void PendSV_Handler(void) __attribute__((weak, alias("Default_Handler")));
void SysTick_Handler(void) __attribute__((weak, alias("Default_Handler")));

typedef union {
    void (*handler)(void);
    void *stack_top;
} vector_t;

/* Word 0: initial main stack pointer. Word 1: reset handler. Then the system exceptions. */
__attribute__((section(".isr_vector"), used))
const vector_t vector_table[16] = {
    {.stack_top = &_estack},
    {Reset_Handler},
    {NMI_Handler},
    {HardFault_Handler},
    {MemManage_Handler},
    {BusFault_Handler},
    {UsageFault_Handler},
    {0}, {0}, {0}, {0},                     /* reserved */
    {SVC_Handler},
    {0}, {0},                               /* reserved (debug monitor, reserved) */
    {PendSV_Handler},
    {SysTick_Handler},
};

void Reset_Handler(void)
{
    /* 1. Copy the initial values of .data from flash (LMA) to SRAM (VMA). */
#ifndef LAB_SKIP_DATA_COPY
    const uint32_t *src = &_sidata;
    for (uint32_t *dst = &_sdata; dst < &_edata;)
        *dst++ = *src++;
#endif
    /* 2. Zero .bss: C guarantees that static objects without an initializer start at zero. */
#ifndef LAB_SKIP_BSS_ZERO
    for (uint32_t *dst = &_sbss; dst < &_ebss;)
        *dst++ = 0u;
#endif
    /* 3. Run the application. A bare-metal main normally never returns; this one reports a result. */
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
