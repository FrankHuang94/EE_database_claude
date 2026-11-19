/* samplelog.h - a growable log of 16-bit samples, for Lab 05-06. */
#ifndef SAMPLELOG_H
#define SAMPLELOG_H

#include <stddef.h>
#include <stdint.h>

typedef struct {
    int16_t *data;      /* heap block owned by the log; NULL while empty */
    size_t len;         /* samples stored */
    size_t cap;         /* samples the block can hold */
    unsigned reallocs;  /* times the block had to grow (for the lab's measurements) */
} samplelog_t;

/* Start an empty log. */
void samplelog_init(samplelog_t *log);

/* Append one sample; returns 0, or -1 if memory ran out (the log is unchanged). */
int samplelog_push(samplelog_t *log, int16_t value);

/* Minimum, maximum and mean of the stored samples; returns 0, or -1 if the log is empty. */
int samplelog_stats(const samplelog_t *log, int16_t *min, int16_t *max, double *mean);

/* Write "n=<len> min=<min> max=<max> mean=<mean, 2 decimals>" into dst (size bytes).
 * Returns the length the full text needs, so a result >= size means it was truncated. */
int samplelog_format(const samplelog_t *log, char *dst, size_t size);

/* Release the log's memory and leave it empty. */
void samplelog_free(samplelog_t *log);

#endif /* SAMPLELOG_H */
