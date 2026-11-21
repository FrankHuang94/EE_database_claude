/* Arm semihosting: the debugger (here QEMU) services a BKPT 0xAB trap. */
#ifndef SEMIHOST_H
#define SEMIHOST_H
#include <stdint.h>

#define SYS_WRITE0 0x04u                    /* print a NUL-terminated string */
#define SYS_EXIT 0x18u                      /* report an exception (used to end the program) */
#define ADP_Stopped_ApplicationExit 0x20026u /* "normal exit": QEMU exits with status 0 */
#define ADP_Stopped_RunTimeErrorUnknown 0x20023u /* QEMU exits with status 1 */

static inline uint32_t semihost(uint32_t op, const void *arg)
{
    register uint32_t r0 __asm__("r0") = op;
    register const void *r1 __asm__("r1") = arg;
    __asm__ volatile("bkpt 0xAB" : "+r"(r0) : "r"(r1) : "memory");
    return r0;
}

static inline void sh_puts(const char *s) { semihost(SYS_WRITE0, s); }

static inline void sh_exit(int ok)
{
    semihost(SYS_EXIT, (const void *)(uintptr_t)(ok ? ADP_Stopped_ApplicationExit : ADP_Stopped_RunTimeErrorUnknown));
}
#endif
