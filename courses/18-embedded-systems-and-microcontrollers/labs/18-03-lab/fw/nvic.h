/* Minimal Armv7-M core-peripheral definitions (the subset this lab uses; CMSIS-Core defines the full set). */
#ifndef NVIC_H
#define NVIC_H
#include <stdint.h>

#define REG32(a) (*(volatile uint32_t *)(a))
#define REG8(a) (*(volatile uint8_t *)(a))

#define NVIC_ISER(n) REG32(0xE000E100u + 4u * (n)) /* set-enable */
#define NVIC_ICER(n) REG32(0xE000E180u + 4u * (n)) /* clear-enable */
#define NVIC_ISPR(n) REG32(0xE000E200u + 4u * (n)) /* set-pending */
#define NVIC_ICPR(n) REG32(0xE000E280u + 4u * (n)) /* clear-pending */
#define NVIC_IABR(n) REG32(0xE000E300u + 4u * (n)) /* active bits */
#define NVIC_IPR(irq) REG8(0xE000E400u + (irq))     /* one priority byte per interrupt */
#define SCB_ICSR REG32(0xE000ED04u)                 /* interrupt control and state */
#define SCB_VTOR REG32(0xE000ED08u)
#define SCB_AIRCR REG32(0xE000ED0Cu)
#define SCB_SHPR3 REG32(0xE000ED20u)                /* priorities of PendSV (bits 23:16) and SysTick (31:24) */
#define SCB_SHCSR REG32(0xE000ED24u)
#define SCB_CFSR REG32(0xE000ED28u)                 /* configurable fault status */
#define SCB_HFSR REG32(0xE000ED2Cu)                 /* hard fault status */
#define SCB_BFAR REG32(0xE000ED38u)                 /* bus fault address */
#define SYST_CSR REG32(0xE000E010u)
#define SYST_RVR REG32(0xE000E014u)
#define SYST_CVR REG32(0xE000E018u)

static inline void nvic_enable(unsigned irq) { NVIC_ISER(irq >> 5) = 1u << (irq & 31u); }
static inline void nvic_disable(unsigned irq) { NVIC_ICER(irq >> 5) = 1u << (irq & 31u); }
static inline void nvic_set_pending(unsigned irq) { NVIC_ISPR(irq >> 5) = 1u << (irq & 31u); }
static inline void nvic_set_priority(unsigned irq, uint8_t prio) { NVIC_IPR(irq) = prio; }

static inline void enable_irq(void) { __asm__ volatile("cpsie i" ::: "memory"); }
static inline void disable_irq(void) { __asm__ volatile("cpsid i" ::: "memory"); }
static inline void set_basepri(uint32_t v) { __asm__ volatile("msr basepri, %0" ::"r"(v) : "memory"); }
static inline uint32_t get_ipsr(void)
{
    uint32_t r;
    __asm__ volatile("mrs %0, ipsr" : "=r"(r));
    return r;
}
static inline void dsb_isb(void) { __asm__ volatile("dsb\n\tisb" ::: "memory"); }
#endif
