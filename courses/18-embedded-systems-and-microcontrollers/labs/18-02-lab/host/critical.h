/* Model solution to Problem 18-02.14: a nestable critical section and an atomic field update.
 *
 * On a Cortex-M target the three intrinsics come from CMSIS (core_cm4.h and friends). On the host,
 * critical_test.c supplies mock versions that model PRIMASK and a pending interrupt.
 * RMW_WINDOW() marks the instant between the read and the write; it is empty on the target. */
#ifndef CRITICAL_H
#define CRITICAL_H
#include <stdint.h>

uint32_t __get_PRIMASK(void);
void __set_PRIMASK(uint32_t primask);
void __disable_irq(void);

#ifndef RMW_WINDOW
#define RMW_WINDOW() ((void)0)
#endif

/* Save the current mask state and disable interrupts. Returns the state to restore. */
static inline uint32_t irq_save(void)
{
    uint32_t state = __get_PRIMASK();
    __disable_irq();
    return state;
}

/* Restore the state saved by irq_save. If interrupts were already disabled on entry (a nested
 * call), they stay disabled: restoring, not enabling, is what makes the section nestable. */
static inline void irq_restore(uint32_t state)
{
    __set_PRIMASK(state);
}

/* Set the width-bit field at bit position pos to value, as one indivisible step with respect to
 * interrupt handlers on this core. */
static inline void field_update_atomic(volatile uint32_t *reg, unsigned pos, unsigned width, uint32_t value)
{
    uint32_t mask = (width >= 32u) ? 0xFFFFFFFFu : (((uint32_t)1u << width) - 1u) << pos;
    uint32_t state = irq_save();
    uint32_t r = *reg;
    RMW_WINDOW();
    *reg = (r & ~mask) | ((value << pos) & mask);
    irq_restore(state);
}

/* The unprotected version, for comparison: the race of Example 18-02.3. */
static inline void field_update_racy(volatile uint32_t *reg, unsigned pos, unsigned width, uint32_t value)
{
    uint32_t mask = (((uint32_t)1u << width) - 1u) << pos;
    uint32_t r = *reg;
    RMW_WINDOW();
    *reg = (r & ~mask) | ((value << pos) & mask);
}
#endif
