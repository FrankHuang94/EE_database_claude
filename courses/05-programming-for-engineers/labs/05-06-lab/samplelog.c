/* samplelog.c - implementation of samplelog.h. */
#include <stdio.h>
#include <stdlib.h>
#include "samplelog.h"

#define SAMPLELOG_INITIAL_CAP 8

void samplelog_init(samplelog_t *log)
{
    log->data = NULL;
    log->len = 0;
    log->cap = 0;
    log->reallocs = 0;
}

int samplelog_push(samplelog_t *log, int16_t value)
{
    if (log->len == log->cap) {
        size_t new_cap = log->cap ? 2 * log->cap : SAMPLELOG_INITIAL_CAP;
        int16_t *p = realloc(log->data, new_cap * sizeof *p);   /* realloc(NULL, n) acts as malloc */
        if (p == NULL) {
            return -1;                                          /* old block still valid */
        }
        if (log->cap) {
            log->reallocs++;
        }
        log->data = p;
        log->cap = new_cap;
    }
    log->data[log->len++] = value;
    return 0;
}

int samplelog_stats(const samplelog_t *log, int16_t *min, int16_t *max, double *mean)
{
    if (log->len == 0) {
        return -1;
    }
    int16_t lo = log->data[0], hi = log->data[0];
    int64_t sum = 0;
    for (size_t i = 0; i < log->len; i++) {
        if (log->data[i] < lo) lo = log->data[i];
        if (log->data[i] > hi) hi = log->data[i];
        sum += log->data[i];
    }
    *min = lo;
    *max = hi;
    *mean = (double)sum / (double)log->len;
    return 0;
}

int samplelog_format(const samplelog_t *log, char *dst, size_t size)
{
    int16_t lo, hi;
    double mean;
    if (samplelog_stats(log, &lo, &hi, &mean) != 0) {
        return snprintf(dst, size, "n=0");
    }
    return snprintf(dst, size, "n=%zu min=%d max=%d mean=%.2f", log->len, lo, hi, mean);
}

void samplelog_free(samplelog_t *log)
{
    free(log->data);
    samplelog_init(log);                                        /* no dangling pointer left behind */
}
