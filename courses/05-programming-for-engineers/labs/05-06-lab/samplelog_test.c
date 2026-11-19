/* samplelog_test.c - self-checking tests for samplelog.c. Prints TEST PASSED or TEST FAILED.
 * Build: cc -std=c17 -Wall -Wextra -Wpedantic -Werror -fsanitize=address,undefined \
 *           samplelog_test.c samplelog.c -o samplelog_test && ./samplelog_test           */
#include <math.h>
#include <stdio.h>
#include <string.h>
#include "samplelog.h"

static int failures = 0;

static void check(int ok, int line)
{
    if (!ok) {
        failures++;
        printf("FAIL: check on line %d\n", line);
    }
}

#define CHECK(condition) check((condition), __LINE__)

int main(void)
{
    samplelog_t log;
    int16_t lo, hi;
    double mean;
    char text[64], tiny[16];

    samplelog_init(&log);
    CHECK(samplelog_stats(&log, &lo, &hi, &mean) == -1);              /* empty log is an error */
    CHECK(samplelog_format(&log, text, sizeof text) == 3 && strcmp(text, "n=0") == 0);

    /* 1000 deterministic samples between -50 and 50: (37 i mod 101) - 50 */
    for (int i = 0; i < 1000; i++) {
        CHECK(samplelog_push(&log, (int16_t)((37 * i) % 101 - 50)) == 0);
    }
    CHECK(log.len == 1000);
    CHECK(log.cap == 1024);                                           /* 8, 16, ..., 1024 */
    CHECK(log.reallocs == 7);
    CHECK(samplelog_stats(&log, &lo, &hi, &mean) == 0);
    CHECK(lo == -50 && hi == 50);
    CHECK(fabs(mean - 0.01) < 1e-12);                                  /* sum 10 over 1000 samples (README) */

    int needed = samplelog_format(&log, text, sizeof text);
    CHECK(strcmp(text, "n=1000 min=-50 max=50 mean=0.01") == 0);
    CHECK(needed == (int)strlen(text));
    int wanted = samplelog_format(&log, tiny, sizeof tiny);            /* truncated, but safe */
    CHECK(wanted == needed && wanted >= (int)sizeof tiny);
    CHECK(strlen(tiny) == sizeof tiny - 1 && strncmp(tiny, text, sizeof tiny - 1) == 0);

    samplelog_free(&log);
    CHECK(log.data == NULL && log.len == 0 && log.cap == 0);

    if (failures == 0) {
        printf("TEST PASSED\n");
        return 0;
    }
    printf("TEST FAILED (%d failures)\n", failures);
    return 1;
}
