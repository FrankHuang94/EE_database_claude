/* Lab 18-11: a constant-time comparison (Solution 18-11.8) and an early-exit one for contrast. The early-exit
 * version also reports how many bytes it examined, which is what its running time follows. */
#ifndef CTCOMPARE_H
#define CTCOMPARE_H
#include <stddef.h>
#include <stdint.h>

static inline int ct_compare(const uint8_t *a, const uint8_t *b, size_t n, size_t *examined)
{
    uint8_t diff = 0;
    size_t i;
    for (i = 0; i < n; i++)
        diff |= (uint8_t)(a[i] ^ b[i]);
    if (examined)
        *examined = i;
    return diff;
}

static inline int early_exit_compare(const uint8_t *a, const uint8_t *b, size_t n, size_t *examined)
{
    size_t i;
    for (i = 0; i < n; i++) {
        if (a[i] != b[i]) {
            if (examined)
                *examined = i + 1;
            return 1;
        }
    }
    if (examined)
        *examined = n;
    return 0;
}

#endif
