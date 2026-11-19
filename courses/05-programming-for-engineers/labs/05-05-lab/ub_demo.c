/* ub_demo.c - a deliberate signed overflow, for Lab 05-05 Part 3.
 * It compiles cleanly; run it with and without -fsanitize=undefined and compare. */
#include <limits.h>
#include <stdio.h>

int main(void)
{
    volatile int counter = INT_MAX;     /* volatile: the compiler must really do the addition */
    counter = counter + 1;              /* undefined behavior: signed overflow */
    printf("counter = %d\n", counter);
    return 0;
}
