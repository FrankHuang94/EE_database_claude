/* adc_test.c - self-checking tests for adc.c. Prints TEST PASSED or TEST FAILED.
 * Build and run:  cc -std=c17 -Wall -Wextra -Wpedantic -Werror -fsanitize=address,undefined \
 *                    -fno-sanitize-recover=all adc_test.c adc.c -lm -o adc_test && ./adc_test   */
#include <math.h>
#include <stdio.h>
#include "adc.h"

static int failures = 0;

static void check(int ok, int line)
{
    if (!ok) {
        failures++;
        printf("FAIL: check on line %d\n", line);
    }
}

#define CHECK(condition) check((condition), __LINE__)   /* __LINE__: the line where CHECK is used */

int main(void)
{
    /* ADC conversion: known cases worked by hand (12-bit, 3.3 V; 10-bit, 5 V). */
    CHECK(adc_to_mv(0, 12, 3300) == 0);
    CHECK(adc_to_mv(2048, 12, 3300) == 1650);            /* mid-scale: exactly half */
    CHECK(adc_to_mv(1000, 12, 3300) == 806);             /* 805.66 rounds up */
    CHECK(adc_to_mv(4095, 12, 3300) == 3299);            /* 3299.19 rounds down */
    CHECK(adc_to_mv(700, 10, 5000) == 3418);             /* 3417.97 rounds up */
    /* Invalid inputs are rejected, not converted. */
    CHECK(adc_to_mv(4096, 12, 3300) == -1);
    CHECK(adc_to_mv(-1, 12, 3300) == -1);
    /* Filter: alpha and settling, against 1 - exp(-0.1) and ln(1/tol) * tau / t_s. */
    CHECK(fabs(ema_alpha(1e-3, 10e-3) - 0.0951626) < 1e-6);
    CHECK(ema_settle_samples(1e-3, 10e-3, 0.01) == 47);
    CHECK(ema_settle_samples(0.5e-3, 2e-3, 1e-3) == 28);
    /* Inputs that would never settle return -1 instead of hanging. */
    CHECK(ema_settle_samples(1e-3, 10e-3, 1e-20) == -1);   /* tol below double's rounding near 1 */
    CHECK(ema_settle_samples(1e-20, 1.0, 0.01) == -1);     /* alpha = 1 - exp(-1e-20) rounds to 0 */

    if (failures == 0) {
        printf("TEST PASSED\n");
        return 0;
    }
    printf("TEST FAILED (%d failures)\n", failures);
    return 1;
}
