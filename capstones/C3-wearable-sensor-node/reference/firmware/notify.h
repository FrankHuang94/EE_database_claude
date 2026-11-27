/* C3 reference firmware: the 20-octet heart-rate and activity notification sent once per connection event.
 * Little-endian layout (offset: field):
 *   0: version (1)            1: sequence number      2-3: heart rate, 0.1 bpm   4: confidence, 0-100 %
 *   5: flags (bit 0 contact, bit 1 motion, bit 2 low battery, bit 3 PPG overflow since last notification)
 *   6-9: step count           10-11: cell voltage, mV  12-13: skin temperature, 0.01 degC (signed)
 *   14-15: activity counts    16-17: PPG samples dropped (saturating)   18-19: reserved, zero
 */
#ifndef C3_NOTIFY_H
#define C3_NOTIFY_H

#include <stddef.h>
#include <stdint.h>

#define NOTIFY_LEN 20u
#define NOTIFY_VERSION 1u

enum { FLAG_CONTACT = 1u, FLAG_MOTION = 2u, FLAG_LOW_BATTERY = 4u, FLAG_PPG_OVERFLOW = 8u };

typedef struct {
    uint8_t seq;
    uint16_t hr_deci_bpm;   /* 0 .. 3000 (0 to 300.0 bpm); larger values saturate */
    uint8_t confidence;     /* 0 .. 100; larger values saturate */
    uint8_t flags;
    uint32_t steps;
    uint16_t cell_mv;
    int16_t skin_centi_c;
    uint16_t activity;
    uint16_t dropped;       /* set with notify_sat16(ring_dropped(...)) */
} notify_t;

/* Saturates a 32-bit count into the 16-bit "PPG samples dropped" field. */
static inline uint16_t notify_sat16(uint32_t v) { return v > 0xFFFFu ? (uint16_t)0xFFFFu : (uint16_t)v; }

/* Writes NOTIFY_LEN octets; returns the number written (0 if out is NULL or too small). */
size_t notify_pack(const notify_t *n, uint8_t *out, size_t out_len);
/* Parses NOTIFY_LEN octets; returns 0 on success, -1 on a short buffer, a wrong version or non-zero reserved bytes. */
int notify_unpack(const uint8_t *in, size_t in_len, notify_t *n);

#endif
