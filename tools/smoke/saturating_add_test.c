/* Self-checking test for saturating_add.c; prints TEST PASSED on success. */
#include <stdint.h>
#include <stdio.h>

uint8_t sat_add_u8(uint8_t a, uint8_t b);

int main(void)
{
    int failures = 0;
    for (unsigned a = 0; a <= UINT8_MAX; a++) {
        for (unsigned b = 0; b <= UINT8_MAX; b++) {
            unsigned expect = a + b > UINT8_MAX ? UINT8_MAX : a + b;
            if (sat_add_u8((uint8_t)a, (uint8_t)b) != expect) {
                printf("mismatch: %u + %u\n", a, b);
                failures++;
            }
        }
    }
    puts(failures ? "TEST FAILED" : "TEST PASSED");
    return failures != 0;
}
