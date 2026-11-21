/* Lab 18-03 self-checking firmware: priorities, preemption, tail-chaining, masking, SysTick, the stacked
 * exception frame and a recovered fault, all on the emulated Cortex-M4's real NVIC. */
#include <stdint.h>
#include "nvic.h"
#include "semihost.h"

static int failures;

static void put_hex(const char *label, uint32_t v)
{
    char buf[11];
    buf[0] = '0';
    buf[1] = 'x';
    for (int i = 0; i < 8; i++) {
        unsigned nib = (v >> (28 - 4 * i)) & 0xFu;
        buf[2 + i] = (char)(nib < 10 ? '0' + nib : 'A' + nib - 10);
    }
    buf[10] = 0;
    sh_puts(label);
    sh_puts(" ");
    sh_puts(buf);
    sh_puts("\n");
}
static void expect(int ok, const char *what)
{
    if (!ok) {
        sh_puts("FAIL: ");
        sh_puts(what);
        sh_puts("\n");
        failures++;
    }
}

/* ---- an event log written by handlers: each entry is a small code */
#define LOG_MAX 32
volatile uint8_t event_log[LOG_MAX];
volatile uint32_t n_events;
static void log_event(uint8_t code)
{
    if (n_events < LOG_MAX)
        event_log[n_events] = code;
    n_events++;
}
enum { EV_IRQ0_IN = 1, EV_IRQ0_OUT, EV_IRQ1, EV_IRQ2, EV_PENDSV, EV_SYSTICK };

void IRQ0_Handler(void)                    /* low priority: pends a higher one and a same-priority one */
{
    log_event(EV_IRQ0_IN);
    nvic_set_pending(1);                   /* higher priority: preempts at once */
    nvic_set_pending(2);                   /* same priority as IRQ0: must wait, then tail-chains */
    dsb_isb();
    log_event(EV_IRQ0_OUT);
}
void IRQ1_Handler(void) { log_event(EV_IRQ1); }
void IRQ2_Handler(void) { log_event(EV_IRQ2); }

volatile uint32_t pendsv_runs;
void PendSV_Handler(void) { pendsv_runs++; log_event(EV_PENDSV); }

void IRQ3_Handler(void)                    /* high priority: defers work to PendSV (lowest priority) */
{
    SCB_ICSR = 1u << 28;                   /* PENDSVSET */
    dsb_isb();
    log_event(EV_IRQ1);                    /* PendSV must not have run yet */
}

volatile uint32_t ticks;
void SysTick_Handler(void) { ticks++; }

/* ---- the stacked frame: a naked trampoline passes the stack pointer that holds the frame */
volatile uint32_t frame_pc, frame_xpsr, frame_lr_exc;
void frame_probe_c(uint32_t *frame, uint32_t exc_return)
{
    frame_pc = frame[6];
    frame_xpsr = frame[7];
    frame_lr_exc = exc_return;
}
__attribute__((naked)) void IRQ4_Handler(void)
{
    __asm__ volatile("tst lr, #4\n\t"      /* EXC_RETURN bit 2: which stack holds the frame */
                     "ite eq\n\t"
                     "mrseq r0, msp\n\t"
                     "mrsne r0, psp\n\t"
                     "mov r1, lr\n\t"
                     "b frame_probe_c\n\t");
}

/* ---- a recoverable fault: the handler records the cause and skips the faulting instruction */
volatile uint32_t fault_hfsr, fault_cfsr, fault_bfar, fault_pc;
void hardfault_c(uint32_t *frame)
{
    fault_hfsr = SCB_HFSR;
    fault_cfsr = SCB_CFSR;
    fault_bfar = SCB_BFAR;
    fault_pc = frame[6];
    uint16_t first = *(volatile uint16_t *)frame[6];
    frame[6] += ((first & 0xF800u) >= 0xE800u) ? 4u : 2u; /* 32-bit Thumb-2 encodings start 0b11101..0b11111 */
    SCB_CFSR = fault_cfsr;                 /* write-1-to-clear the sticky status bits */
    SCB_HFSR = fault_hfsr;
}
__attribute__((naked)) void HardFault_Handler(void)
{
    __asm__ volatile("tst lr, #4\n\t"
                     "ite eq\n\t"
                     "mrseq r0, msp\n\t"
                     "mrsne r0, psp\n\t"
                     "b hardfault_c\n\t");
}

volatile uint32_t sink;

int main(void)
{
    /* 1. How many priority bits does this NVIC implement? Unimplemented low bits read as zero. */
    NVIC_IPR(0) = 0xFFu;
    uint8_t prio_mask = NVIC_IPR(0);
    unsigned prio_bits = 0;
    for (uint8_t m = prio_mask; m; m <<= 1)
        prio_bits++;
    expect(prio_bits >= 3 && prio_bits <= 8, "3 to 8 priority bits");
    if (prio_bits == 8) sh_puts("NVIC priority bits: 8\n");
    else if (prio_bits == 4) sh_puts("NVIC priority bits: 4\n");
    else if (prio_bits == 3) sh_puts("NVIC priority bits: 3\n");

    /* 2. Preemption and tail-chaining. */
    nvic_set_priority(0, 0xC0u);
    nvic_set_priority(1, 0x40u);
    nvic_set_priority(2, 0xC0u);
    nvic_enable(0);
    nvic_enable(1);
    nvic_enable(2);
    enable_irq();
    n_events = 0;
    nvic_set_pending(0);
    dsb_isb();
    expect(n_events == 4, "four events");
    expect(event_log[0] == EV_IRQ0_IN && event_log[1] == EV_IRQ1 && event_log[2] == EV_IRQ0_OUT && event_log[3] == EV_IRQ2,
           "order: IRQ0 in, IRQ1 preempts, IRQ0 out, IRQ2 tail-chains");
    put_hex("ORDER", ((uint32_t)event_log[0] << 24) | ((uint32_t)event_log[1] << 16) | ((uint32_t)event_log[2] << 8) | event_log[3]);

    /* 3. Masking: BASEPRI blocks priorities numerically >= its value; PRIMASK blocks all. */
    n_events = 0;
    set_basepri(0x80u);
    nvic_set_pending(2);                   /* priority 0xC0: masked */
    dsb_isb();
    expect(n_events == 0, "BASEPRI 0x80 masks priority 0xC0");
    nvic_set_pending(1);                   /* priority 0x40: not masked */
    dsb_isb();
    expect(n_events == 1 && event_log[0] == EV_IRQ1, "BASEPRI 0x80 lets priority 0x40 through");
    set_basepri(0u);
    dsb_isb();
    expect(n_events == 2 && event_log[1] == EV_IRQ2, "masked interrupt runs when BASEPRI is cleared");
    disable_irq();
    n_events = 0;
    nvic_set_pending(1);
    dsb_isb();
    expect(n_events == 0, "PRIMASK masks everything configurable");
    enable_irq();
    dsb_isb();
    expect(n_events == 1, "pending interrupt runs after PRIMASK is cleared");

    /* 4. PendSV for deferred work. */
    SCB_SHPR3 = (SCB_SHPR3 & 0xFF00FFFFu) | (0xE0u << 16); /* PendSV at the lowest priority */
    nvic_set_priority(3, 0x20u);
    nvic_enable(3);
    n_events = 0;
    nvic_set_pending(3);
    dsb_isb();
    expect(pendsv_runs == 1 && n_events == 2 && event_log[0] == EV_IRQ1 && event_log[1] == EV_PENDSV,
           "PendSV runs after the high-priority handler returns");

    /* 5. The stacked frame. */
    nvic_set_priority(4, 0x80u);
    nvic_enable(4);
    nvic_set_pending(4);
    dsb_isb();
    extern char _etext;
    expect(frame_pc > 0x40u && frame_pc < (uint32_t)&_etext, "stacked PC points into the code");
    expect((frame_xpsr >> 24) & 1u, "stacked xPSR has the Thumb bit");
    expect(frame_lr_exc == 0xFFFFFFF9u, "EXC_RETURN = 0xFFFFFFF9 (thread mode, main stack, no FP state)");
    put_hex("EXC_RETURN", frame_lr_exc);
    put_hex("PRIO_READBACK", prio_mask);

    /* 6. SysTick interrupts. */
    SCB_SHPR3 = (SCB_SHPR3 & 0x00FFFFFFu) | (0x60u << 24);
    ticks = 0;
    SYST_RVR = 10000u - 1u;
    SYST_CVR = 0u;
    SYST_CSR = 0x7u;                       /* enable, interrupt, core clock */
    for (uint32_t guard = 0; ticks < 5u && guard < 200000000u; guard++) {
    }
    SYST_CSR = 0u;
    expect(ticks >= 5u, "five SysTick interrupts");

    /* 7. A bus fault on an unmapped address, escalated to HardFault and recovered. */
    sink = *(volatile uint32_t *)0x50000000u; /* nothing is mapped here on this board */
    expect(fault_hfsr & (1u << 30), "HFSR.FORCED: a configurable fault escalated");
    expect(fault_cfsr & (1u << 9), "CFSR.PRECISERR: precise data bus error");
    expect(fault_cfsr & (1u << 15), "CFSR.BFARVALID");
    expect(fault_bfar == 0x50000000u, "BFAR holds the faulting address");
    put_hex("CFSR", fault_cfsr);
    put_hex("HFSR", fault_hfsr);
    put_hex("BFAR", fault_bfar);

    if (failures == 0)
        sh_puts("TEST PASSED\n");
    return failures;
}
