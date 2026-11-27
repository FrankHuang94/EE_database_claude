#include "notify.h"

static void put16(uint8_t *p, uint16_t v) { p[0] = (uint8_t)(v & 0xFFu); p[1] = (uint8_t)(v >> 8); }
static void put32(uint8_t *p, uint32_t v) { put16(p, (uint16_t)(v & 0xFFFFu)); put16(p + 2, (uint16_t)(v >> 16)); }
static uint16_t get16(const uint8_t *p) { return (uint16_t)(p[0] | (uint16_t)(p[1] << 8)); }
static uint32_t get32(const uint8_t *p) { return (uint32_t)get16(p) | ((uint32_t)get16(p + 2) << 16); }

size_t notify_pack(const notify_t *n, uint8_t *out, size_t out_len)
{
    if (n == NULL || out == NULL || out_len < NOTIFY_LEN) return 0;
    out[0] = NOTIFY_VERSION;
    out[1] = n->seq;
    put16(out + 2, n->hr_deci_bpm > 3000u ? 3000u : n->hr_deci_bpm);
    out[4] = n->confidence > 100u ? 100u : n->confidence;
    out[5] = (uint8_t)(n->flags & 0x0Fu);
    put32(out + 6, n->steps);
    put16(out + 10, n->cell_mv);
    put16(out + 12, (uint16_t)n->skin_centi_c);
    put16(out + 14, n->activity);
    put16(out + 16, n->dropped);
    out[18] = 0;
    out[19] = 0;
    return NOTIFY_LEN;
}

int notify_unpack(const uint8_t *in, size_t in_len, notify_t *n)
{
    if (in == NULL || n == NULL || in_len < NOTIFY_LEN) return -1;
    if (in[0] != NOTIFY_VERSION || in[18] != 0 || in[19] != 0) return -1;
    n->seq = in[1];
    n->hr_deci_bpm = get16(in + 2);
    n->confidence = in[4];
    n->flags = in[5];
    n->steps = get32(in + 6);
    n->cell_mv = get16(in + 10);
    n->skin_centi_c = (int16_t)get16(in + 12);
    n->activity = get16(in + 14);
    n->dropped = get16(in + 16);
    return 0;
}
