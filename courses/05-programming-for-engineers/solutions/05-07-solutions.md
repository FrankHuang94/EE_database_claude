# Solutions 05-07 · Bit Manipulation and Fixed-Width Integers

Problems: [05-07 problems](../problems/05-07-problems.md) · Chapter: [05-07](../chapters/05-07-bit-manipulation.md). Every C block below is compiled with `-Wall -Wextra -Wpedantic -Werror` and the address and undefined-behavior sanitizers, and run, by [verify_05_07.py](../verify/verify_05_07.py), which checks the printed output exactly and recomputes every number in the answer key independently in Python.

---

## Solutions

### Solution 05-07.1

(a) $-1 \equiv 255$ = **`0xFF`**; $-128 \equiv 128$ = **`0x80`**; $+127$ = **`0x7F`**. (b) Read with the negative top weight: `0xFF` = $-128 + 127$ = **−1**; `0x80` = **−128**; `0x7F` = **127**. (c) $12 = 0000\,1100$; inverted, $1111\,0011$; plus one, $1111\,0100$ = **`0xF4`**, which is $-128 + 64 + 32 + 16 + 4 = -12$ ✓.

```c
#include <stdint.h>
#include <stdio.h>

int main(void)
{
    printf("%02X %02X %02X\n", (unsigned)(uint8_t)-1, (unsigned)(uint8_t)-128, (unsigned)(uint8_t)127);
    printf("%d %d %d\n", (int8_t)0xFF, (int8_t)0x80, (int8_t)0x7F);
    uint8_t x = 0x0C;
    printf("%02X\n", (unsigned)(uint8_t)(~x + 1));
    return 0;
}
```

```text
FF 80 7F
-1 -128 127
F4
```

(Converting an out-of-range value such as `0xFF` to `int8_t` is implementation-defined; every mainstream compiler wraps it in two's complement, as shown.)

### Solution 05-07.2

`0xA5` = `1010 0101`.

```c
#include <stdint.h>
#include <stdio.h>

int main(void)
{
    uint8_t x = 0xA5;
    printf("%02X %02X %02X %02X %02X\n", (unsigned)(x & 0x0F), (unsigned)(x | 0x40), (unsigned)(uint8_t)(x ^ 0xFF),
           (unsigned)(uint8_t)(x << 2), (unsigned)(x >> 3));
    return 0;
}
```

```text
05 E5 5A 94 14
```

AND keeps the low nibble, **`0x05`**; OR sets bit 6, **`0xE5`**; XOR with all ones inverts, **`0x5A`**; shifting left by 2 gives `10 1001 0100`, of which 8 bits remain, **`0x94`** (the promoted `int` is `0x294` until it is cast back); shifting right by 3 gives `1 0100` = **`0x14`** (165 / 8 = 20.6, rounded down to 20).

### Solution 05-07.3

`int16_t`: **−32,768 to 32,767**. 12-bit field: **−2048 to 2047**. Q15: **−1 to $1 - 2^{-15}$ (0.999969)**, resolution $2^{-15}$ = **3.05×10⁻⁵**. Q8.8: integers −32,768 to 32,767 scaled by $2^{-8}$, so −128 to $128 - 2^{-8}$; resolution $2^{-8}$ = **0.00390625**, largest value **127.99609375**. Q8.8 trades fraction bits for range: it can hold battery voltages or temperatures directly, at a coarser step.

### Solution 05-07.4

```c
#include <stdint.h>
#include <stdio.h>

static int32_t sign_extend(uint32_t field, unsigned bits)   /* 1 <= bits <= 31, field < 2^bits */
{
    const uint32_t sign = (uint32_t)1 << (bits - 1);
    return (int32_t)((field ^ sign) - sign);
}

int main(void)
{
    printf("%d %d %d %d\n", (int)sign_extend(0x800, 12), (int)sign_extend(0x7FF, 12),
           (int)sign_extend(0xFFF, 12), (int)sign_extend(0x13, 5));
    return 0;
}
```

```text
-2048 2047 -1 -13
```

The results are **−2048**, **2047**, **−1** and, for the 5-bit `0x13` = `10011`, $-16 + 3$ = **−13**. Why it works: XOR with the sign bit maps the negative half $[2^{k-1}, 2^k)$ to $[0, 2^{k-1})$ and the non-negative half up by $2^{k-1}$; subtracting $2^{k-1}$ then lands each value on its signed meaning. (The unsigned subtraction wraps for negative results, and the conversion to `int32_t` reads the wrapped pattern as negative; that conversion is implementation-defined, but every mainstream compiler does it this way.)

### Solution 05-07.5

(a) `0xFFFF00F0`: bits 7:4 are `1111`, so bits 6:4 are `111`: **`MODE` = 7**.

(b) Clear bits 6:4 (mask `0x70`) and OR in $3 \ll 4 = 0x30$: $0xFFFF00F0\ \&\ \sim0x70 = 0xFFFF0080$, then $|\ 0x30$ = **`0xFFFF00B0`**.

```c
#include <stdint.h>
#include <stdio.h>

int main(void)
{
    uint32_t reg = 0xFFFF00F0u;
    unsigned mode = (reg >> 4) & 0x7u;
    uint32_t good = (reg & ~(0x7u << 4)) | ((3u & 0x7u) << 4);
    uint32_t bad = reg | (3u << 4);
    printf("MODE %u; correct 0x%08X (MODE %u); OR only 0x%08X (MODE %u)\n", mode, (unsigned)good,
           (unsigned)((good >> 4) & 0x7u), (unsigned)bad, (unsigned)((bad >> 4) & 0x7u));
    return 0;
}
```

```text
MODE 7; correct 0xFFFF00B0 (MODE 3); OR only 0xFFFF00F0 (MODE 7)
```

(c) OR can only set bits, so OR-ing 3 into a field holding 7 leaves **7**: the register is unchanged (`0xFFFF00F0`). Insertion must clear the field first.

### Solution 05-07.6

(a) Little-endian: `0D 0C 0B 0A`; big-endian: `0A 0B 0C 0D`. (b) Little-endian bytes `10 27 00 00` mean `0x00002710` = **10,000**.

```c
#include <stdint.h>
#include <stdio.h>

static uint32_t get_le32(const uint8_t *p)
{
    return (uint32_t)p[0] | (uint32_t)p[1] << 8 | (uint32_t)p[2] << 16 | (uint32_t)p[3] << 24;
}

static uint32_t bswap32(uint32_t v)
{
    return (v >> 24) | ((v >> 8) & 0x0000FF00u) | ((v << 8) & 0x00FF0000u) | (v << 24);
}

int main(void)
{
    const uint8_t field[4] = {0x10, 0x27, 0x00, 0x00};
    printf("%u 0x%08X\n", (unsigned)get_le32(field), (unsigned)bswap32(0x0A0B0C0Du));
    return 0;
}
```

```text
10000 0x0D0C0B0A
```

(c) `bswap32` moves each byte to the mirror position: `0x0A0B0C0D` becomes `0x0D0C0B0A`. Compilers recognize this pattern and emit a single byte-swap instruction on most processors.

### Solution 05-07.7

(a) $-0.3 \times 32768 = -9830.4$, rounded to **−9830**, which represents $-0.2999878$: an error of $1.22\times10^{-5}$, within half a step ($1.53\times10^{-5}$). (b) $3.3 \times 256 = 844.8$, rounded to **845**, representing 3.30078 V, an error of 0.78 mV (half a step is 1.95 mV). (c) $0.25 \to 8192$, $0.5 \to 16384$; $8192 \times 16384 = 2^{27}$; adding $2^{14}$ and shifting by 15 gives **4096**, exactly 0.125.

```c
#include <math.h>
#include <stdint.h>
#include <stdio.h>

int main(void)
{
    int16_t q = (int16_t)lround(-0.3 * 32768);
    int16_t v = (int16_t)lround(3.3 * 256);
    int32_t prod = ((int32_t)8192 * 16384 + (1 << 14)) >> 15;
    printf("%d (err %.2e), %d (err %.2e V), %d\n", q, q / 32768.0 + 0.3, v, v / 256.0 - 3.3, (int)prod);
    return 0;
}
```

```text
-9830 (err 1.22e-05), 845 (err 7.81e-04 V), 4096
```

### Solution 05-07.8

```c
#include <stdint.h>
#include <stdio.h>

static int is_pow2(uint32_t x) { return x != 0 && (x & (x - 1)) == 0; }

static uint32_t next_pow2(uint32_t x)              /* smallest power of two >= x, for 1 <= x <= 2^31 */
{
    x--;
    x |= x >> 1;  x |= x >> 2;  x |= x >> 4;  x |= x >> 8;  x |= x >> 16;
    return x + 1;
}

int main(void)
{
    printf("%d %d %d %d %d\n", is_pow2(0), is_pow2(1), is_pow2(64), is_pow2(96), is_pow2(1024));
    printf("%u %u\n", 1234u & 255u, (unsigned)next_pow2(1000));
    return 0;
}
```

```text
0 1 1 0 1
210 1024
```

(a) 0 is not a power of two (the `x != 0` guard is needed, because `0 & (0 - 1)` is 0); 1, 64 and 1024 are; 96 (`110 0000`) is not. (b) `1234 & 255` = **210**, the same as `1234 % 256`, because the mask keeps the low 8 bits, which is exactly the remainder modulo $2^8$. (c) **1024**: subtracting 1 and then OR-ing in shifted copies sets every bit below the highest set bit, giving $2^k - 1$; adding 1 gives $2^k$. (The initial decrement makes exact powers of two map to themselves.)

### Solution 05-07.9

(a) `0xF0F0` = `1111 0000 1111 0000`: **8** ones. (b) `0x5A` = `0101 1010`: four ones, even, so parity **0**.

```c
#include <stdint.h>
#include <stdio.h>

static unsigned popcount(uint32_t x)
{
    unsigned n = 0;
    while (x) {
        x &= x - 1;                                /* clears the lowest set bit */
        n++;
    }
    return n;
}

int main(void)
{
    printf("%u %u\n", popcount(0xF0F0u), popcount(0x5Au) & 1u);
    return 0;
}
```

```text
8 0
```

(c) `x &= x - 1` clears exactly the lowest 1 bit (Section 3.7), so the loop runs once per set bit: 8 iterations for `0xF0F0` instead of 32 for a bit-by-bit loop.

### Solution 05-07.10

The chopped constant is $q_b = \lfloor 0.1 \times 2^b \rfloor / 2^b$, and after $N$ ticks the drift is $N(0.1 - q_b)$, with $N = 100 \times 3600 \times 10 = 3.6\times10^6$.

```c
#include <math.h>
#include <stdio.h>

int main(void)
{
    const double ticks = 100.0 * 3600.0 * 10.0;
    for (int b = 23; b <= 32; b++) {
        double q = floor(0.1 * ldexp(1.0, b)) / ldexp(1.0, b);   /* 0.1 chopped to b fractional bits */
        double drift = ticks * (0.1 - q);
        if (b <= 24 || drift < 1e-3) {
            printf("b = %d: drift %.4f s\n", b, drift);
        }
        if (drift < 1e-3) break;
    }
    return 0;
}
```

```text
b = 23: drift 0.3433 s
b = 24: drift 0.1287 s
b = 32: drift 0.0005 s
```

(a) $b$ = 23: **0.3433 s**, matching the GAO's figure ([R-057](../../../reference/research-log.md#r-057--patriot-missile-timing-error)). (b) $b$ = 24: **0.1287 s**, an improvement of more than twofold, because bit 24 of 0.1's binary expansion ($0.000110011\ldots_2$, repeating `0011`) is a 1, which the 24-bit constant now keeps. How much each extra bit helps depends on the digits it captures. (c) The drift first falls below 1 ms at **$b$ = 32** (0.0005 s). (d) Avoid representing 0.1 at all: keep time as an integer count of ticks (exact), and convert to seconds only for display, or multiply by 1/10 as an exact rational (divide by 10). The general lesson: accumulate in exact integers; round only at the edges.

(The `double` arithmetic here is exact for these values: $0.1 \times 2^b$ and the floor are computed without rounding error at this size, which the verify script confirms with exact fractions.)

### Solution 05-07.11

Each value is converted by rounding, $q = \text{round}(x \cdot 2^{15})$, and by truncation toward −∞, $q = \lfloor x \cdot 2^{15} \rfloor$; a small xorshift generator makes the random values identical on every platform.

```c
#include <math.h>
#include <stdint.h>
#include <stdio.h>

static uint32_t state = 1u;
static double uniform(void)                        /* xorshift32 -> [0, 1) */
{
    state ^= state << 13;
    state ^= state >> 17;
    state ^= state << 5;
    return state / 4294967296.0;
}

int main(void)
{
    const double delta = ldexp(1.0, -15);
    double sum_r = 0.0, sum_t = 0.0;
    const int n = 100000;
    for (int i = 0; i < n; i++) {
        double x = -0.9 + 1.8 * uniform();
        double er = round(x / delta) * delta - x;  /* rounding error */
        double et = floor(x / delta) * delta - x;  /* truncation error */
        sum_r += er * er;
        sum_t += et * et;
    }
    printf("rounding RMS %.3e (theory %.3e)\n", sqrt(sum_r / n), delta / sqrt(12.0));
    printf("truncation RMS %.3e (theory %.3e)\n", sqrt(sum_t / n), delta / sqrt(3.0));
    return 0;
}
```

```text
rounding RMS 8.794e-06 (theory 8.810e-06)
truncation RMS 1.763e-05 (theory 1.762e-05)
```

Rounding gives an RMS error of about **8.8×10⁻⁶**, matching $\Delta/\sqrt{12}$ = $3.05\times10^{-5}/3.46$. Truncation's error is uniform on $[-\Delta, 0]$ instead of $[-\Delta/2, \Delta/2]$: its mean is $-\Delta/2$ and its RMS is $\sqrt{\Delta^2/12 + \Delta^2/4} = \Delta/\sqrt{3}$ = **1.76×10⁻⁵**, twice as large, almost all of it a constant *bias* that accumulates in sums and filters (Example 05-07.5). That is the case for rounding in every multiply.

### Solution 05-07.12

```c
#include <stdint.h>
#include <stdio.h>

static uint16_t ones_sum(const uint16_t *w, int n)
{
    uint32_t s = 0;
    for (int i = 0; i < n; i++) {
        s += w[i];
    }
    while (s >> 16) {
        s = (s & 0xFFFFu) + (s >> 16);             /* fold carries back in (end-around carry) */
    }
    return (uint16_t)s;
}

int main(void)
{
    uint16_t hdr[10] = {0x4500, 0x0073, 0x0000, 0x4000, 0x4011, 0x0000, 0xC0A8, 0x0001, 0xC0A8, 0x00C7};
    uint16_t folded = ones_sum(hdr, 10);
    uint16_t checksum = (uint16_t)~folded;
    hdr[5] = checksum;                             /* the checksum field is word 5 */
    printf("sum 0x%04X, checksum 0x%04X, re-check 0x%04X\n", (unsigned)folded, (unsigned)checksum, (unsigned)ones_sum(hdr, 10));
    return 0;
}
```

```text
sum 0x479E, checksum 0xB861, re-check 0xFFFF
```

The 32-bit sum is `0x2479C`; folding the carry gives $0x479C + 0x2$ = `0x479E`; the complement is the checksum **`0xB861`**. A receiver sums all ten words including the checksum; since $x + \sim x$ is all ones, a correct header gives **`0xFFFF`**, and anything else means corruption. Ones'-complement addition makes the result independent of byte order and of the order of the words, which is why it was chosen; it detects all single-bit errors but not, for example, two words swapped.

### Solution 05-07.13

The simulation models the peripheral's rules: a 1 written to a write-1-to-clear bit clears it, the read/write bits take the written value, and the read-only bit ignores writes.

```c
#include <stdint.h>
#include <stdio.h>

#define RXNE    (1u << 0)                       /* read-only: set by hardware when data arrives */
#define OVR     (1u << 1)                       /* write-1-to-clear: overrun */
#define TC      (1u << 2)                       /* write-1-to-clear: transfer complete */
#define RW_MASK (3u << 8)                       /* bits 9:8, interrupt enables, read/write */
#define W1C_MASK (OVR | TC)

static uint32_t status_reg;                     /* stands in for the hardware register */

static void hw_write(uint32_t v)                /* what the peripheral does with a write */
{
    status_reg &= ~(v & W1C_MASK);              /* a 1 written to a W1C bit clears it */
    status_reg = (status_reg & ~RW_MASK) | (v & RW_MASK);   /* R/W bits take the written value */
}                                               /* read-only bits ignore writes */

static void attempt(const char *name, uint32_t (*make_write)(uint32_t read))
{
    status_reg = RXNE | OVR | TC | (1u << 8);   /* 0x107: data waiting, both flags set, IRQ on */
    uint32_t w = make_write(status_reg);
    hw_write(w);
    printf("%-22s wrote 0x%03X, status now 0x%03X\n", name, (unsigned)w, (unsigned)status_reg);
}

static uint32_t naive_rmw(uint32_t r) { return r | OVR; }               /* STATUS |= OVR */
static uint32_t plain_assign(uint32_t r) { (void)r; return OVR; }       /* STATUS = OVR */
static uint32_t keep_rw(uint32_t r) { return (r & RW_MASK) | OVR; }     /* STATUS = (STATUS & RW_MASK) | OVR */

int main(void)
{
    attempt("STATUS |= OVR", naive_rmw);
    attempt("STATUS = OVR", plain_assign);
    attempt("keep R/W bits, add OVR", keep_rw);
    return 0;
}
```

```text
STATUS |= OVR          wrote 0x107, status now 0x101
STATUS = OVR           wrote 0x002, status now 0x005
keep R/W bits, add OVR wrote 0x102, status now 0x105
```

(a) `STATUS |= OVR` reads `0x107` and writes back `0x107`, which contains a 1 in bit 2 as well as bit 1: it clears **both** `OVR` and `TC`, leaving **`0x101`** (257). The transfer-complete event is lost before anyone handled it, a bug that appears only when the two flags happen to be set together.

(b) `STATUS = OVR` writes `0x002`. It clears only `OVR`, but it also writes 0 to the read/write interrupt-enable bits, leaving **`0x005`** (5): the receive interrupt is now silently disabled.

(c) Preserve the read/write bits and write 1 only where a flag should be cleared: `STATUS = (STATUS & RW_MASK) | OVR;` writes `0x102` and leaves **`0x105`** (261), with `OVR` cleared, `TC` still pending and the interrupt still enabled. (Many real parts avoid the problem by design, keeping flags and enables in separate registers, or providing a separate "flag clear" register.)

(d) If `STATUS` is not declared through a `volatile` pointer, the optimizer sees a loop whose condition reads memory that nothing in the loop writes, reads it once, and turns the loop into an infinite one (or deletes it). At `-O0` every read happens, so the bug hides until the release build. Declare the register `volatile`, as in §3.4.

(e) The main loop reads `CTRL` (with `RX_EN` = 1 and `TX_EN` = 0), the interrupt fires, the handler reads `CTRL`, clears `RX_EN`, writes it back and returns; the main loop then writes its stale copy with `TX_EN` set and **`RX_EN` still set**, undoing the handler. Fixes: disable interrupts around the main loop's read-modify-write (a short critical section), or use the peripheral's atomic set/clear registers so that neither side reads and writes back the whole register. `volatile` alone does not help: it makes each access happen, not the three steps indivisible.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 05-07.1a | −1 as an unsigned byte | 255 | — |
| 05-07.1b | int8 value of 0x80 | −128 | — |
| 05-07.1c | negation of 12, unsigned byte | 244 | — |
| 05-07.2a | 0xA5 & 0x0F | 5 | — |
| 05-07.2b | 0xA5 ^ 0xFF | 90 | — |
| 05-07.2c | (uint8_t)(0xA5 << 2) | 148 | — |
| 05-07.2d | 0xA5 >> 3 | 20 | — |
| 05-07.3a | Q15 resolution | 3.05×10^-5 | — |
| 05-07.3b | Q8.8 resolution | 0.00390625 | — |
| 05-07.3c | Q8.8 maximum | 127.99609375 | — |
| 05-07.4a | 5-bit 0x13 sign-extended | −13 | — |
| 05-07.5a | current MODE | 7 | — |
| 05-07.5b | register after MODE = 3 | 4294901936 | — |
| 05-07.6a | little-endian field value | 10000 | — |
| 05-07.7a | −0.3 in Q15 | −9830 | — |
| 05-07.7b | its error | 1.22×10^-5 | — |
| 05-07.7c | 3.3 V in Q8.8 | 845 | — |
| 05-07.7d | 0.25 × 0.5 in Q15 | 4096 | — |
| 05-07.8a | 1234 & 255 | 210 | — |
| 05-07.8b | next power of two ≥ 1000 | 1024 | — |
| 05-07.9a | 1 bits in 0xF0F0 | 8 | — |
| 05-07.9b | parity of 0x5A | 0 | — |
| 05-07.10a | drift with 23 bits | 0.3433 | s |
| 05-07.10b | drift with 24 bits | 0.1287 | s |
| 05-07.10c | bits for drift below 1 ms | 32 | — |
| 05-07.11a | RMS rounding error, theory | 8.81×10^-6 | — |
| 05-07.11b | RMS truncation error, theory | 1.76×10^-5 | — |
| 05-07.12a | IPv4 header checksum | 47201 | — |
| 05-07.12b | re-check sum | 65535 | — |
| 05-07.13a | status after the read-modify-write (0x101) | 257 | — |
| 05-07.13b | status after the plain assignment (0x005) | 5 | — |
| 05-07.13c | status after the correct write (0x105) | 261 | — |
