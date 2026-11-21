/* Lab 18-02 self-checking firmware: proves the startup code and the register helpers work. */
#include <stdint.h>
#include "regbits.h"
#include "semihost.h"

/* Memory-mapped core registers (Armv7-M System Control Space). */
#define SCB_CPUID (*(volatile const uint32_t *)0xE000ED00u)
#define SYST_CSR (*(volatile uint32_t *)0xE000E010u)
#define SYST_RVR (*(volatile uint32_t *)0xE000E014u)
#define SYST_CVR (*(volatile uint32_t *)0xE000E018u)

uint32_t magic = 0xC0FFEE42u;               /* .data: initial value lives in flash, copied at reset */
int16_t offsets[4] = {-3, 7, -11, 13};      /* .data */
uint32_t zeros[64];                         /* .bss: must read as zero (global, so the compiler cannot assume it) */
const uint8_t squares[8] = {0, 1, 4, 9, 16, 25, 36, 49}; /* .rodata: stays in flash */

static volatile uint32_t fake_reg = 0xFFFF0000u; /* a "register" in SRAM for the field tests */

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
    /* Startup: .data copied, .bss zeroed, .rodata readable. */
    expect(magic == 0xC0FFEE42u, ".data initial value");
    expect(offsets[0] == -3 && offsets[3] == 13, ".data array");
    int all_zero = 1;
    for (unsigned i = 0; i < 64; i++)
        all_zero &= (zeros[i] == 0u);
    expect(all_zero, ".bss zeroed");
    expect(squares[7] == 49, ".rodata table");
    magic++;                                /* .data is writable because it lives in SRAM */
    expect(magic == 0xC0FFEE43u, ".data writable");

    /* Register fields on a RAM-backed register. */
    reg_write_field(&fake_reg, 8, 4, 0x5u);
    expect(fake_reg == 0xFFFF0500u, "field insert bits [11:8]");
    reg_write_field(&fake_reg, 28, 4, 0x0u);
    expect(fake_reg == 0x0FFF0500u, "field clear bits [31:28]");
    expect(field_extract(fake_reg, 16, 12) == 0xFFFu, "field extract bits [27:16]");

    /* A real core register: CPUID identifies the core (implementer 0x41 = Arm, part 0xC24 = Cortex-M4). */
    uint32_t cpuid = SCB_CPUID;
    expect(field_extract(cpuid, 24, 8) == 0x41u, "CPUID implementer is Arm");
    expect(field_extract(cpuid, 4, 12) == 0xC24u, "CPUID part number is Cortex-M4");

    /* SysTick: program the 24-bit reload register and read it back; bits above 23 are not implemented. */
    SYST_RVR = 0xFFFFFFFFu;
    expect(SYST_RVR == 0x00FFFFFFu, "SysTick reload is 24 bits");
    SYST_RVR = 1000u - 1u;
    SYST_CVR = 0u;                          /* any write clears the current value */
    SYST_CSR = 0x5u;                        /* enable, core clock, no interrupt */
    uint32_t a = SYST_CVR, b = SYST_CVR;
    expect(a <= 999u && b <= 999u, "SysTick counts within its reload range");
    SYST_CSR = 0u;

    if (failures == 0)
        sh_puts("TEST PASSED\n");
    return failures;
}
