<!-- status: reviewed -->
# 05-07 · Bit Manipulation and Fixed-Width Integers

| | |
|---|---|
| **Course** | [05 · Programming for Engineers](../README.md) |
| **University equivalent** | The data-representation and low-level programming units of a computer-systems or embedded course (Bryant and O'Hallaron, *Computer Systems: A Programmer's Perspective*, ch. 2; Valvano, *Embedded Systems*, I/O and fixed-point chapters) |
| **Prerequisites** | [05-05 C Fundamentals](05-05-c-fundamentals.md), [05-06 C Pointers, Arrays and Memory](05-06-c-pointers-and-memory.md) |
| **Estimated study hours** | 8 |
| **Last verified** | 2026-11-19 |

**Learning objectives.** After this chapter you can:

1. Convert between binary, hexadecimal and decimal, and derive and apply the two's-complement representation, including negation and sign extension.
2. Set, clear, toggle, test, extract and insert bit fields with masks and shifts, using unsigned fixed-width types and avoiding the shift pitfalls.
3. Access memory-mapped hardware registers correctly (`volatile`, read-modify-write) and explain why.
4. Serialize and parse multi-byte values independently of the host's byte order, and explain little- and big-endian layouts.
5. Represent fractional quantities in fixed point (Q format), multiply with correct scaling, rounding and saturation, and quantify the quantization error.

## 1. Big picture

Hardware speaks in bits. A microcontroller's timer, ADC or radio is configured by writing patterns of bits into **registers**: one bit enables the block, three bits choose a mode, four bits set a gain, and one read-only bit reports "busy". Sensors deliver 12- or 16-bit readings packed into bytes, communication links carry headers whose fields are a few bits wide, and small processors without floating-point hardware do signal processing in integers that stand for fractions. Writing that code correctly means thinking at the level of individual bits, and knowing exactly how wide each integer is. This chapter is where software meets the register map of a datasheet.

- **Firmware and drivers:** every peripheral register access is a mask-and-shift operation (Section 3.4).
- **Communication protocols:** packet headers, checksums and byte order decide whether two devices understand each other (Section 3.5).
- **Low-power signal processing:** fixed-point arithmetic lets a few-milliwatt MCU filter sensor data without a floating-point unit; the same idea, at 8 bits and below, underlies the integer formats used for neural-network inference on edge and datacenter accelerators (Section 3.6).
- **Failures:** integer width and conversion mistakes have destroyed a rocket and could have cut all AC power on an airliner (05-05, [R-093](../../../reference/research-log.md#r-093--software-failures-from-numeric-conversions-and-counters)).

## 2. Intuition first

**A register is a row of labeled switches.** A 32-bit control register is 32 switches, numbered 0 (rightmost, least significant) to 31. A **mask** is a stencil: a pattern with 1s exactly over the switches you care about. OR-ing with the mask turns those switches on; AND-ing with its complement turns them off; AND-ing with the mask itself reads them, hiding the rest. **Shifting** slides the pattern left or right, which is how you move a value into the field's position.

**Two's complement is an odometer.** A 4-digit odometer reading 0000 that rolls back one mile shows 9999. In binary, an 8-bit counter at 00000000 that steps back once shows 11111111, and two's complement simply *agrees to call that −1*. Everything else follows: 11111110 is −2, and the counter's ordinary adder now handles negative numbers with no extra hardware.

**Fixed point is money in cents.** Banking software never stores \$12.34 as a floating-point number; it stores the integer 1234 and remembers that the unit is a cent. Fixed-point arithmetic does the same in base 2: the integer 24,576 with an agreed scale of $2^{-15}$ means 0.75. Addition works directly on the integers; multiplication needs a rescale (cents × cents are "cent²", so you divide by 100), and every result is rounded to the nearest cent. *Where the analogy breaks:* money needs only addition and multiplication by rates, and its range is generous; signal processing multiplies constantly, and a 16-bit integer's range is small enough that overflow is a design concern in every line.

## 3. Theory

### 3.1 Bits, hex and fixed-width types

An $n$-bit pattern $b_{n-1}\dots b_1 b_0$ read as an **unsigned** number has value

$$
U = \sum_{i=0}^{n-1} b_i\, 2^i, \qquad 0 \le U \le 2^n - 1.
$$

**Hexadecimal** groups bits in fours (a **nibble**), each written as one digit 0–9, A–F: `0xA5` is `1010 0101`, which is 165. Hex is the language of datasheets because each digit maps to exactly four bits; in C, `0x` marks a hex literal. Since C23, `0b10100101` is a binary literal too (GCC and Clang accepted it earlier as an extension).

Bit manipulation needs integers of *known* width, so this chapter uses `<stdint.h>` throughout: `uint8_t`, `uint16_t`, `uint32_t`, `uint64_t` and their signed counterparts (05-05). Constants of a given width are written with suffixes or macros (`1u`, `UINT32_C(1)`), and `<inttypes.h>` provides matching `printf` formats such as `PRIx32` and `PRId16`, because the right specifier for `uint32_t` differs between platforms.

### 3.2 Two's complement, derived

**Definition.** An $n$-bit two's-complement pattern represents

$$
S = -b_{n-1}\,2^{n-1} + \sum_{i=0}^{n-2} b_i\, 2^i,
$$

so the top bit carries a *negative* weight. The range is $-2^{n-1}$ to $2^{n-1} - 1$: −128 to 127 for 8 bits. The same pattern read as unsigned is $U = S + b_{n-1}2^n$; that is, $S \equiv U \pmod{2^n}$. This is why one adder serves both interpretations: addition modulo $2^n$ gives the right bits whether you read them as signed or unsigned, and only overflow detection differs.

**Negation is "invert and add one".** The bitwise complement $\sim x$ flips every bit, so $x + \sim x$ is all ones, $2^n - 1$. Therefore

$$
\sim x + 1 = 2^n - x \equiv -x \pmod{2^n}.
$$

For example, $5 = 00000101$; inverting gives $11111010$; adding 1 gives $11111011$, which is $-128 + 64 + 32 + 16 + 8 + 2 + 1 = -5$ ✓. One quirk: the most negative value has no positive partner. Negating −128 in 8 bits gives −128 again, and in C, `-INT_MIN` overflows (undefined behavior).

**Sign extension.** To widen a signed value, copy its sign bit into all the new high bits: 8-bit −5 = `0xFB` becomes 16-bit `0xFFFB`. C does this automatically when converting `int8_t` to `int16_t`. Sensors, however, often deliver signed values in odd widths such as 12 bits packed inside a 16-bit word, and then the code must sign-extend by hand. A neat portable identity for a $k$-bit field $x$ (stored as an unsigned value in $[0, 2^k)$) is

$$
\text{signed}(x) = (x \oplus 2^{k-1}) - 2^{k-1},
$$

where $\oplus$ is XOR: flipping the sign bit maps the field's two halves into the right order, and subtracting $2^{k-1}$ re-centers it (Example 05-07.1).

### 3.3 Bitwise operators and the masking idioms

| Operator | Meaning | Example (`a = 0b1100`, `b = 0b1010`) |
|---|---|---|
| `a & b` | AND: 1 where both are 1 | `0b1000` |
| `a \| b` | OR: 1 where either is 1 | `0b1110` |
| `a ^ b` | XOR: 1 where they differ | `0b0110` |
| `~a` | NOT: flip every bit | `...11110011` |
| `a << k` | shift left $k$ places (×$2^k$) | `0b1100 << 1` = `0b11000` |
| `a >> k` | shift right $k$ places (÷$2^k$, rounding down for unsigned) | `0b1100 >> 2` = `0b11` |

With a mask `m` (for one bit at position $n$, `m = 1u << n`), the four everyday idioms are:

- **set:** `reg |= m;`
- **clear:** `reg &= ~m;`
- **toggle:** `reg ^= m;`
- **test:** `if (reg & m) ...`

A **bit field** of width $w$ at position $p$ uses the mask `((1u << w) - 1) << p`. To **extract** it, shift down and mask; to **insert** a value, clear the field and OR in the shifted value:

$$
\begin{aligned}
\text{field} &= (\text{reg} \gg p)\ \&\ (2^w - 1),\\
\text{reg} &= (\text{reg}\ \&\ \sim((2^w - 1) \ll p))\ |\ ((\text{value}\ \&\ (2^w - 1)) \ll p).
\end{aligned}
$$

Masking `value` before shifting it in keeps an out-of-range value from spilling into neighboring fields.

**Shift pitfalls.** Use unsigned operands for bit manipulation. Shifting by a negative amount or by the type's width or more is undefined (`1u << 32` for a 32-bit `unsigned`). Left-shifting a 1 into or past the sign bit of a signed type is also undefined: `1 << 31` with 32-bit `int` overflows, while `1u << 31` is fine. Right-shifting a negative signed value is implementation-defined (every mainstream compiler copies the sign bit, an *arithmetic* shift, but portable code should not rely on it). And remember integer promotion (05-05): `uint8_t x = 0x80; x << 1` is the `int` 256, not 0; only storing it back into a `uint8_t` truncates it.

### 3.4 Talking to hardware: memory-mapped registers and `volatile`

On a microcontroller, a peripheral's registers appear at fixed addresses in the memory map. Firmware reaches a register through a pointer to that address, conventionally wrapped in a macro or a struct that mirrors the datasheet's register layout:

```c
// fragment
#define ADC_BASE   0x40012000u                                  /* illustrative address, not a real part */
#define ADC_CTRL   (*(volatile uint32_t *)(ADC_BASE + 0x00u))
#define ADC_DATA   (*(volatile uint32_t *)(ADC_BASE + 0x04u))

ADC_CTRL |= 1u << 0;                                            /* enable the converter */
while (ADC_CTRL & (1u << 31)) { }                               /* wait while BUSY is set */
uint32_t code = ADC_DATA & 0xFFFu;                              /* 12-bit result */
```

**`volatile`** tells the compiler that every read and write of this object has an effect it cannot see, so it must perform each one, in order, exactly as written. Without it, the optimizer would read the BUSY bit once, conclude that nothing in the loop changes it, and spin forever; or it would merge or delete "redundant" writes that were in fact commands to the hardware. `volatile` is also needed for variables shared with interrupt handlers. It does *not* make an operation atomic.

**Read-modify-write hazards.** `ADC_CTRL |= m` is three steps: read the register, OR in the bit, write it back. If an interrupt handler modifies the same register between the read and the write, its change is lost. Firmware avoids this by briefly disabling interrupts around the update, or by using hardware support: many microcontrollers provide separate "set" and "clear" registers in which writing a 1 to a bit position sets or clears just that bit atomically. Some status bits are cleared by writing 1 to them ("write-1-to-clear"), so a careless read-modify-write that writes back a 1 it read clears a flag it never meant to touch. Datasheets document each bit's access type (read/write, read-only, write-1-to-clear) for exactly this reason.

C also offers **bit-field struct members** (`unsigned mode : 3;`), which look convenient for register maps, but the order of bits within the storage unit, padding and access width are implementation-defined, so portable register code and most coding standards prefer explicit masks and shifts.

### 3.5 Byte order (endianness)

A 32-bit value occupies four bytes, and processors disagree about which byte goes at the lowest address. **Little-endian** machines store the least significant byte first; **big-endian** machines store the most significant byte first. For `0x0A0B0C0D`:

| Address offset | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| little-endian | `0D` | `0C` | `0B` | `0A` |
| big-endian | `0A` | `0B` | `0C` | `0D` |

All x86 processors are little-endian. Arm Cortex-M cores leave the data endianness to the chip vendor (little-endian or byte-invariant big-endian), and mainstream parts such as STM32 microcontrollers are little-endian; RISC-V allows either, and fetches instructions little-endian regardless ([R-096](../../../reference/research-log.md#r-096--processor-byte-order-arm-cortex-m-and-risc-v)) **[Established]**. Meanwhile, Internet protocols transmit multi-byte fields most significant byte first ("network byte order", which is big-endian), and many sensor and file formats specify one order or the other.

Byte order matters whenever bytes cross a boundary between machines or between memory and a wire. The portable solution never depends on the host's own order: build values from bytes with shifts, and split them into bytes the same way.

```c
#include <stdint.h>
#include <stdio.h>

static uint32_t get_be32(const uint8_t *p)            /* big-endian bytes -> value */
{
    return (uint32_t)p[0] << 24 | (uint32_t)p[1] << 16 | (uint32_t)p[2] << 8 | (uint32_t)p[3];
}

static void put_le32(uint8_t *p, uint32_t v)          /* value -> little-endian bytes */
{
    p[0] = (uint8_t)v;
    p[1] = (uint8_t)(v >> 8);
    p[2] = (uint8_t)(v >> 16);
    p[3] = (uint8_t)(v >> 24);
}

int main(void)
{
    const uint8_t wire[4] = {0x0A, 0x0B, 0x0C, 0x0D};
    uint8_t out[4];
    uint32_t v = get_be32(wire);
    put_le32(out, v);
    printf("value 0x%08X, little-endian bytes %02X %02X %02X %02X\n", (unsigned)v, out[0], out[1], out[2], out[3]);
    return 0;
}
```

```text
value 0x0A0B0C0D, little-endian bytes 0D 0C 0B 0A
```

The same source gives the same result on every machine, whatever its own byte order. The tempting alternative, copying bytes straight into a `uint32_t` (or casting a `uint8_t *` to a `uint32_t *`), gives different answers on little- and big-endian hosts, and the cast can also violate alignment and C's aliasing rules. (`memcpy` into a variable is the legal way to reinterpret bytes when you do want the host's own order.)

### 3.6 Fixed-point arithmetic

A **fixed-point** number is an integer $q$ with an agreed scale $2^{-f}$: it represents $x = q \cdot 2^{-f}$, where $f$ is the number of **fractional bits**. The common notation **Q$m$.$f$** (or just Q$f$) gives $m$ integer bits and $f$ fractional bits. The most used format in audio and control is **Q15**: a 16-bit signed integer standing for a fraction in $[-1, 1 - 2^{-15}]$, with resolution $2^{-15} \approx 3.05\times10^{-5}$.

**Conversion.** To store a real $x$: $q = \text{round}(x \cdot 2^{f})$, clamped to the type's range. To read back: $x = q / 2^{f}$.

**Addition** of two numbers with the same format is integer addition: $(q_1 + q_2)2^{-f}$. It can overflow, so DSP code uses **saturating** addition, which clamps to the largest or smallest value instead of wrapping (a wrapped audio sample jumps from loud positive to loud negative, a click; a saturated one merely clips).

**Multiplication** changes the scale: $(q_1 2^{-f})(q_2 2^{-f}) = q_1 q_2\, 2^{-2f}$. The product of two Q15 numbers is a Q30 number in a 32-bit integer, and converting back means shifting right by 15. Adding $2^{14}$ (half of $2^{15}$) before the shift **rounds** to nearest instead of truncating toward −∞, which halves the worst-case error and removes its bias. One product overflows: $(-1)\times(-1) = +1$, which Q15 cannot represent, so the result is saturated to $1 - 2^{-15}$.

**Quantization error.** Rounding to the nearest multiple of $\Delta = 2^{-f}$ leaves an error in $[-\Delta/2, \Delta/2]$. If the error is equally likely anywhere in that interval (a good model for busy signals), its mean is 0 and its standard deviation is (03-03)

$$
\sigma_q = \sqrt{\frac{1}{\Delta}\int_{-\Delta/2}^{\Delta/2} e^2\, de} = \frac{\Delta}{\sqrt{12}}.
$$

The same formula gives the noise of an ideal $N$-bit ADC, and from it the famous $6.02N + 1.76$ dB signal-to-noise ratio for a full-scale sine (Course 20). Every fractional bit added halves $\Delta$ and buys about 6 dB.

**Representation error that accumulates.** Most decimal fractions are not exact in binary. 0.1 is $0.000110011001100\ldots_2$, repeating forever. The Patriot missile system's clock counted tenths of a second and multiplied by 0.1 stored with 23 fractional bits, *chopped* (truncated) rather than rounded. The chopped value is $0.1(1 - 2^{-20})$, too small by $2^{-20}$ of itself, so a time computed from the tick count fell behind the true time by $2^{-20}$ of the elapsed time: 0.3433 s after 100 hours of continuous operation. A uniform lag like that would have done little harm on its own, because tracking uses the *difference* between the times of two radar pulses, and the same relative error in both times nearly cancels. The failure came from an inconsistency: during the Gulf deployment the software had been modified, and a more accurate time conversion was used for one of the two times but not the other, so a truncated time was subtracted from an accurate one, the 0.3433 s did not cancel, and the tracking gate was misplaced by 687 m (02-10; [R-057](../../../reference/research-log.md#r-057--patriot-missile-timing-error)) **[Established]**. A small per-operation error, multiplied by millions of ticks, became a failure when two parts of the code disagreed about it: a lesson in consistency as much as in precision.

> **Going deeper — fixed point and neural-network inference.** Quantized inference stores weights and activations as 8-bit (or narrower) integers with a scale factor per tensor or per channel, multiplies them in integer arithmetic with wide accumulators, and rescales the result: exactly the Q-format pattern above, with the scale chosen per layer instead of fixed at $2^{-15}$. The engineering questions are the same too: how many bits keep the error acceptable, where to round, and how to avoid overflow in the accumulators. **Deeper:** see companion repo *LLM Inference Engineering*.

### 3.7 A few bit tricks worth knowing

- **Power of two:** a positive integer $x$ is a power of two exactly when `(x & (x - 1)) == 0`, because subtracting 1 flips the lowest 1 bit and every bit below it.
- **Cheap modulo:** for $n$ a power of two, `x % n` equals `x & (n - 1)` for unsigned `x`. Ring buffers (05-08) use this with sizes like 256 or 1024.
- **Lowest set bit:** `x & -x` (for unsigned `x`) isolates it.
- **Counting 1 bits (population count)** and finding the highest set bit have compiler built-ins (`__builtin_popcount`) and, in C23, standard functions in `<stdbit.h>`; many processors execute them in one instruction, while others (small microcontrollers) need a short loop or table.
- **Parity** (whether the number of 1 bits is odd) is the basis of simple error detection; XOR-ing all the bits computes it.

## 4. Worked examples

### Example 05-07.1 · Decoding a 12-bit temperature reading

**Setup.** A digital temperature sensor returns a 12-bit two's-complement value in the upper 12 bits of a 16-bit register; the least significant bit of the 12-bit value is 0.0625 °C. (a) Encode −100 as an 8-bit two's-complement pattern. (b) The register reads `0xF380`. Find the 12-bit field, its signed value, and the temperature.

**Solution.** (a) $-100 \equiv 256 - 100 = 156$ = `0x9C` (`1001 1100`). Check with the definition: $-128 + 16 + 8 + 4 = -100$ ✓.

(b) Shifting right by 4 removes the unused low nibble: `0xF380 >> 4` = `0xF38` = 3896. The 12-bit sign bit (bit 11, worth 2048) is set, so the value is negative: $3896 - 4096 = -200$. With the XOR identity, $(3896 \oplus 2048) - 2048 = 1848 - 2048 = -200$ ✓. The temperature is $-200 \times 0.0625$ = **−12.5 °C**.

```c
#include <stdint.h>
#include <stdio.h>

static int16_t sign_extend12(uint16_t field)          /* field in [0, 4096) */
{
    return (int16_t)((field ^ 0x800u) - 0x800u);
}

int main(void)
{
    uint16_t reg = 0xF380u;
    uint16_t field = reg >> 4;
    int16_t value = sign_extend12(field);
    printf("int8 -100 = 0x%02X; field 0x%03X = %d; T = %.4f C\n",
           (unsigned)(uint8_t)-100, (unsigned)field, value, value * 0.0625);
    printf("extremes: %d %d %d\n", sign_extend12(0x7FF), sign_extend12(0x800), sign_extend12(0xFFF));
    return 0;
}
```

```text
int8 -100 = 0x9C; field 0xF38 = -200; T = -12.5000 C
extremes: 2047 -2048 -1
```

The extremes confirm the 12-bit range: `0x7FF` is +2047, `0x800` is −2048, `0xFFF` is −1. (On most compilers the signed 16-bit register value could also be shifted right *arithmetically* by 4, but that relies on implementation-defined behavior; the XOR form does not.)

**Units check.** counts × °C/count = °C ✓.

**Sanity check.** 12 bits at 0.0625 °C span −128 °C to +127.94 °C, comfortably covering the usual −40 °C to +125 °C rating ✓.

### Example 05-07.2 · Configuring a peripheral register

**Setup.** A (hypothetical) ADC control register has: bit 0 `EN` (enable), bits 3:1 `MODE` (3 bits), bits 11:8 `GAIN` (4 bits), bit 31 `BUSY` (read-only). Starting from 0, enable the ADC with `MODE` = 5 and `GAIN` = 9; then disable it without disturbing the other fields. Finally, decode the value `0x80000D35` read back from the hardware.

**Solution.** Insert each field with the formula of Section 3.3: `EN` contributes $1$; `MODE` = 5 = `101` at bit 1 contributes $5 \times 2 = 10$ = `0xA`; `GAIN` = 9 at bit 8 contributes $9 \times 256$ = `0x900`. Total **`0x0000090B`**. Clearing `EN` gives **`0x0000090A`**.

```c
#include <stdint.h>
#include <stdio.h>

#define FIELD_MASK(width, pos)  ((((uint32_t)1 << (width)) - 1u) << (pos))

static uint32_t field_get(uint32_t reg, unsigned width, unsigned pos)
{
    return (reg & FIELD_MASK(width, pos)) >> pos;
}

static uint32_t field_set(uint32_t reg, unsigned width, unsigned pos, uint32_t value)
{
    return (reg & ~FIELD_MASK(width, pos)) | ((value << pos) & FIELD_MASK(width, pos));
}

enum { EN_POS = 0, MODE_POS = 1, MODE_W = 3, GAIN_POS = 8, GAIN_W = 4, BUSY_POS = 31 };

int main(void)
{
    uint32_t ctrl = 0;
    ctrl |= (uint32_t)1 << EN_POS;
    ctrl = field_set(ctrl, MODE_W, MODE_POS, 5);
    ctrl = field_set(ctrl, GAIN_W, GAIN_POS, 9);
    printf("configured 0x%08X\n", (unsigned)ctrl);
    ctrl &= ~((uint32_t)1 << EN_POS);
    printf("disabled   0x%08X\n", (unsigned)ctrl);

    uint32_t rd = 0x80000D35u;
    printf("EN %u, MODE %u, GAIN %u, BUSY %u\n", (unsigned)field_get(rd, 1, EN_POS), (unsigned)field_get(rd, MODE_W, MODE_POS),
           (unsigned)field_get(rd, GAIN_W, GAIN_POS), (unsigned)field_get(rd, 1, BUSY_POS));
    printf("GAIN = 20 truncates to %u\n", (unsigned)field_get(field_set(0, GAIN_W, GAIN_POS, 20), GAIN_W, GAIN_POS));
    return 0;
}
```

```text
configured 0x0000090B
disabled   0x0000090A
EN 1, MODE 2, GAIN 13, BUSY 1
GAIN = 20 truncates to 4
```

Decoding `0x80000D35`: the low byte `0x35` = `0011 0101`: `EN` (bit 0) = **1**; bits 3:1 = `010` = **2**; `GAIN` = `0xD` = **13**; bit 31 set, so `BUSY` = **1**. The last line shows the protective mask: asking for `GAIN` = 20 (`10100`) keeps only the low 4 bits, 4, instead of corrupting bit 12. (Whether silently truncating is acceptable is a design choice; a driver might instead reject out-of-range values.)

**Sanity check.** `0x90B` = 2315 = $1 + 10 + 2304$ ✓.

### Example 05-07.3 · Reading a big-endian field from a packet

**Setup.** A sensor packet arrives as bytes `{0xA5, 0x01, 0xF4, 0xFF, 0x38}`: a start byte, then a big-endian unsigned 16-bit sample count, then a big-endian *signed* 16-bit offset. Parse both fields portably. What would a little-endian reading of the count give?

**Solution.**

```c
#include <stdint.h>
#include <stdio.h>

static uint16_t get_be16(const uint8_t *p) { return (uint16_t)(p[0] << 8 | p[1]); }
static uint16_t get_le16(const uint8_t *p) { return (uint16_t)(p[1] << 8 | p[0]); }

int main(void)
{
    const uint8_t pkt[5] = {0xA5, 0x01, 0xF4, 0xFF, 0x38};
    uint16_t count = get_be16(&pkt[1]);
    uint16_t raw = get_be16(&pkt[3]);
    int16_t offset = (int16_t)((raw ^ 0x8000u) - 0x8000u);      /* sign-extend a 16-bit field */
    printf("count %u (little-endian misread: %u), offset %d\n", (unsigned)count, (unsigned)get_le16(&pkt[1]), offset);
    return 0;
}
```

```text
count 500 (little-endian misread: 62465), offset -200
```

Big-endian `01 F4` is $1 \times 256 + 244$ = **500**; misread as little-endian it would be $0xF401$ = **62,465**, a plausible-looking but absurd count, which is how byte-order bugs usually show up. The offset `FF 38` is `0xFF38` = 65,336 unsigned, which as a signed 16-bit value is $65{,}336 - 65{,}536$ = **−200**.

**Sanity check.** $500 = 0x01F4$ ✓.

### Example 05-07.4 · Multiplying in Q15

**Setup.** (a) Compute $0.5 \times (-0.75)$ in Q15. (b) Represent 0.7 in Q15 and compute $0.7^2$ with rounding; compare with 0.49. (c) What happens to $(-1)\times(-1)$?

**Solution.** In Q15, $0.5 \to 16384$, $-0.75 \to -24576$, $0.7 \to \text{round}(0.7 \times 32768) = \text{round}(22937.6) = 22938$ (which is really 0.700012).

```c
#include <stdint.h>
#include <stdio.h>

static int16_t q15_mul(int16_t a, int16_t b)
{
    int32_t p = (int32_t)a * b;                        /* Q30 product in 32 bits */
    p = (p + (1 << 14)) >> 15;                         /* round, back to Q15 */
    if (p > INT16_MAX) p = INT16_MAX;                  /* only (-1) x (-1) can exceed */
    return (int16_t)p;
}

int main(void)
{
    int16_t half = 16384, m075 = -24576, p07 = 22938, minus1 = INT16_MIN;
    int16_t a = q15_mul(half, m075), b = q15_mul(p07, p07), c = q15_mul(minus1, minus1);
    printf("%d -> %.6f\n", a, a / 32768.0);
    printf("%d -> %.6f (exact 0.49, error %.2e)\n", b, b / 32768.0, b / 32768.0 - 0.49);
    printf("%d -> %.6f (saturated)\n", c, c / 32768.0);
    return 0;
}
```

```text
-12288 -> -0.375000
16057 -> 0.490021 (exact 0.49, error 2.08e-05)
32767 -> 0.999969 (saturated)
```

(a) $16384 \times (-24576) = -402{,}653{,}184$; shifting right by 15 gives **−12288**, which is exactly −0.375. (b) $22938^2 = 526{,}151{,}844$; adding $2^{14}$ and shifting gives **16057**, i.e. 0.490021, an error of $2.1\times10^{-5}$, below one Q15 step ($3.05\times10^{-5}$); most of it comes from representing 0.7 itself. (c) $(-32768)^2 = 2^{30}$, which shifted is $2^{15}$ = 32,768, one more than `INT16_MAX`; it saturates to **32767** (0.99997). (The right shift of a negative product relies on the compiler's arithmetic shift, implementation-defined but universal; strictly portable code divides with rounding instead.)

**Units check.** The Q30 product has scale $2^{-30}$; the shift by 15 restores $2^{-15}$ ✓.

**Sanity check.** $0.5 \times 0.75 = 0.375$, and $0.375 \times 32768 = 12288$ ✓.

### Example 05-07.5 · The dead band of a fixed-point filter

**Setup.** The exponential moving-average filter of 05-05 (a first-order recursive, or IIR, filter), $y \leftarrow y + \alpha(x - y)$, is implemented in Q15 on an MCU without a floating-point unit, with $\alpha = 1 - e^{-0.1}$ and the update `y += (alpha_q * (x - y)) >> 15` (a truncating, arithmetic shift). The input steps from 0 to $x$ = 10,000 (in Q15 counts). (a) Find `alpha_q`. (b) Where does the output stop, and why? (c) How does rounding the update change that?

**Solution.** (a) $\alpha_q = \text{round}(0.0951626 \times 32768) = \text{round}(3118.3)$ = **3118**.

(b) The update is $\lfloor 3118\,(x - y)/32768 \rfloor$, which is 0 as soon as $3118\,(x - y) < 32768$, that is when the gap $x - y$ falls below $32768/3118 = 10.51$. The output then stops for good, at most 10 counts short of the input: a **dead band** of about $1/\alpha$ least-significant bits, in which the filter cannot move. A floating-point filter would creep on forever toward 10,000.

```c
#include <stdint.h>
#include <stdio.h>

static int32_t settle(int32_t alpha_q, int32_t x, int round_update, int *steps)
{
    int32_t y = 0;
    for (*steps = 0; *steps < 100000; (*steps)++) {
        int32_t delta = round_update ? (alpha_q * (x - y) + (1 << 14)) >> 15 : (alpha_q * (x - y)) >> 15;
        if (delta == 0) break;                         /* stuck: the update rounds to nothing */
        y += delta;
    }
    return y;
}

int main(void)
{
    int steps;
    int32_t y_trunc = settle(3118, 10000, 0, &steps);
    printf("truncating: stops at %d after %d steps (gap %d)\n", y_trunc, steps, 10000 - y_trunc);
    int32_t y_round = settle(3118, 10000, 1, &steps);
    printf("rounding:   stops at %d after %d steps (gap %d)\n", y_round, steps, 10000 - y_round);
    return 0;
}
```

```text
truncating: stops at 9990 after 75 steps (gap 10)
rounding:   stops at 9995 after 74 steps (gap 5)
```

The truncating filter stops **10** counts short. (c) Rounding makes the update nonzero until the gap falls below $16384/3118 = 5.25$, so the rounding filter stops **5** counts short, half the dead band. For a temperature or battery-voltage filter, a dead band of a few counts may be harmless; for a slow control loop it causes a steady offset. Fixes include more fractional bits in the state (a 32-bit accumulator holding $y$ in Q31, say) and adding the truncation error back on the next step ("error feedback").

**Units check.** $\alpha$ is dimensionless; the dead band is in counts, the unit of $x$ and $y$ ✓.

**Sanity check.** The dead band scales as $1/\alpha$: a slower filter (smaller α) has a wider dead band, the price of smoothing in limited precision ✓.

### Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| T 05-07.a | Q15 resolution | 3.05×10^-5 | — |
| T 05-07.b | Patriot clock: relative error of chopped 0.1 | 9.54×10^-7 | — |
| T 05-07.c | Patriot drift after 100 h | 0.3433 | s |
| Ex 05-07.1a | −100 as an unsigned 8-bit pattern | 156 | — |
| Ex 05-07.1b | 12-bit field value (unsigned) | 3896 | — |
| Ex 05-07.1c | signed value | −200 | — |
| Ex 05-07.1d | temperature | −12.5 | °C |
| Ex 05-07.2a | configured register | 2315 | — |
| Ex 05-07.2b | after disabling | 2314 | — |
| Ex 05-07.2c | decoded MODE | 2 | — |
| Ex 05-07.2d | decoded GAIN | 13 | — |
| Ex 05-07.3a | sample count | 500 | — |
| Ex 05-07.3b | little-endian misread | 62465 | — |
| Ex 05-07.3c | signed offset | −200 | — |
| Ex 05-07.4a | Q15 product 0.5 × (−0.75) | −12288 | — |
| Ex 05-07.4b | Q15 0.7 | 22938 | — |
| Ex 05-07.4c | Q15 0.7² (rounded) | 16057 | — |
| Ex 05-07.4d | saturated (−1) × (−1) | 32767 | — |
| Ex 05-07.5a | α in Q15 | 3118 | — |
| Ex 05-07.5b | dead band, truncating update | 10 | counts |
| Ex 05-07.5c | dead band, rounding update | 5 | counts |

## 5. Simulate it

Open [labs/05-07-lab/](../labs/05-07-lab/README.md): a small C "bits toolkit" (`bits.c`) with a self-checking test, run by [`tools/run_c.py`](../../../tools/run_c.py). It contains:

1. **Field helpers and a simulated register:** set, clear, extract and insert fields on a variable standing in for a peripheral register, including a write-1-to-clear status bit. *Predict first:* what does a naive read-modify-write do to a pending flag?
2. **Portable byte order:** big- and little-endian get/put functions, round-trip tests, and a test that the host's own byte order does not matter.
3. **Q15 arithmetic:** conversion, rounded and saturating multiply, saturating add, and the measured quantization error of 10,000 conversions against the $\Delta/\sqrt{12}$ prediction.
4. **Bit tricks:** population count, parity and power-of-two tests checked against slow reference implementations over every 16-bit value.

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Fixed point versus floating point | Fixed: runs on MCUs without an FPU, lower energy and area, deterministic | Range and scaling managed by hand; overflow and dead-band risks | Firmware / DSP engineer, set by the chip choice |
| Fractional bits (Q format) | More bits: smaller quantization error (≈6 dB per bit) | Less headroom before overflow; wider accumulators | DSP engineer |
| Rounding versus truncation | Rounding: half the error, no bias | A few extra operations per multiply | DSP engineer |
| Saturating versus wrapping arithmetic | Saturation: graceful clipping instead of wild jumps | Extra compare (or a special instruction) per operation | DSP / control engineer |
| Masks and shifts versus C bit-field structs | Masks: portable, explicit access width | More verbose code | Coding standard (MISRA restricts bit-fields) |
| Native byte order versus explicit serialization | Explicit: portable and correct on any host | A few more instructions per field | Protocol / driver engineer |
| Integer width for inference (INT8 versus 16-bit or float) | Narrower: less memory and energy per operation | Accuracy loss, calibration effort | ML systems architect |

## 7. Numbers to know

| Quantity | Value | Note |
|---|---|---|
| $n$-bit two's-complement range | $-2^{n-1}$ to $2^{n-1} - 1$ | 8 bit: −128 to 127; 16 bit: −32,768 to 32,767 |
| Q15 range and step | $[-1, 1 - 2^{-15}]$, $\Delta = 3.05\times10^{-5}$ | 16-bit fractional |
| Rounding error | uniform in $\pm\Delta/2$, RMS $\Delta/\sqrt{12} = 0.289\Delta$ | |
| SNR per bit | about 6.02 dB | ideal quantizer, full-scale sine: $6.02N + 1.76$ dB |
| Hex digit | 4 bits; a byte is 2 hex digits | |
| Network byte order | big-endian | x86 and common MCUs are little-endian ([R-096](../../../reference/research-log.md#r-096--processor-byte-order-arm-cortex-m-and-risc-v)) |
| Patriot clock error | $2^{-20}$ relative; 0.3433 s after 100 h | [R-057](../../../reference/research-log.md#r-057--patriot-missile-timing-error) |

## 8. Common mistakes

1. **Bit manipulation on signed types,** and `1 << 31` with a 32-bit `int` (undefined). Use unsigned types and `1u` or `UINT32_C(1)`.
2. **Shifting by the width or more** (`x << 32` for 32-bit `x`), often from a computed shift amount. Check the range.
3. **Forgetting to clear a field before OR-ing in a new value,** or to mask the new value, so old bits or overflow bits corrupt neighbors.
4. **Missing `volatile` on hardware registers or variables shared with interrupts,** so the compiler optimizes away reads and writes.
5. **Read-modify-write on registers with write-1-to-clear bits,** or racing with an interrupt. Read the datasheet's access types; use set/clear registers or critical sections.
6. **Casting byte buffers to `uint32_t *`** and assuming the host's byte order. Serialize with shifts.
7. **Forgetting to rescale after a fixed-point multiply,** or truncating where rounding was needed; and wrapping instead of saturating.
8. **Assuming sign extension happens by itself** for odd-width fields such as 12-bit sensor values.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **Byte order is settled by market, not by standard.** x86 is little-endian; Arm lets licensees choose the data endianness of Cortex-M cores, and mainstream MCU families such as STM32 are little-endian; the current RISC-V specification allows little-, big- or bi-endian data memory but always fetches instructions little-endian, and its authors note that little-endian systems "are currently dominant commercially" ([R-096](../../../reference/research-log.md#r-096--processor-byte-order-arm-cortex-m-and-risc-v)) **[Established]**. Big-endian survives in network protocols and some legacy and networking processors, so serialization code must still be explicit.
- **The language is catching up with the hardware.** C23 added binary literals, digit separators, `<stdbit.h>` (population count, leading and trailing zeros, and similar functions), `<stdckdint.h>` (checked addition, subtraction and multiplication that report overflow) and bit-precise `_BitInt(N)` integer types, and it made two's complement mandatory ([R-092](../../../reference/research-log.md#r-092--c-language-standards-coding-standards-and-embedded-usage)) **[Established]**. Toolchain support arrives gradually: GCC added `_BitInt` in version 14 and `#embed` in 15.
- **Low-precision integer arithmetic is central to AI hardware.** Inference accelerators and NPUs in phones, wearables and datacenters execute 8-bit and narrower integer (and narrow floating-point) operations, because each halving of width roughly halves memory traffic and multiplier energy; the quantization arithmetic is the fixed-point arithmetic of Section 3.6 **[Established]** for the principle. **Deeper:** see companion repo *LLM Inference Engineering*.

### Why it matters commercially

Bit-level details are where hardware and software teams' work meets, and where integration fails. A register map is a contract between a chip's designers and its software developers; mistakes in it (an undocumented write-1-to-clear bit, a field whose reset value differs from the datasheet) surface as driver bugs at customers. A sensor or radio whose data format is clearly specified (byte order, sign, scaling, units) integrates in days; an ambiguous one costs weeks. In diligence on an MCU, sensor or connectivity target, the quality of register documentation, the hardware abstraction layer and the example code is a direct proxy for customer support costs and design-win velocity. In AI hardware, claims about "INT8 TOPS" and "INT4 support" are claims about fixed-point arithmetic, and the accuracy cost of quantization is part of every honest benchmark.

### Marketing vs Reality

- **"Supports INT4 inference at twice the INT8 throughput."** *Reality:* throughput doubles only if the model's accuracy holds at 4 bits, which depends on the model and the quantization method; ask for accuracy on the customer's model, not peak TOPS.
- **"16-bit ADC."** *Reality:* resolution is not accuracy. The effective number of bits (ENOB), set by noise and nonlinearity, is often several bits lower (Course 20). Ask for ENOB and SNR at the operating conditions.
- **"Drop-in compatible register map."** *Reality:* check reset values, reserved-bit behavior, access types and timing, not just field positions. Ask for the list of differences.
- **"Fixed-point implementation matches floating-point to within 0.01%."** *Reality:* average error can be tiny while a dead band, limit cycle or overflow appears in a corner case. Ask how worst cases were tested.

### Questions for engineering leaders

1. **"How is your register map documented and kept in sync with the RTL?"** *Strong:* generated from one machine-readable source (for example IP-XACT or SystemRDL) into RTL, C headers and documentation. *Evasive:* "Engineers update the PDF."
2. **"How do you handle byte order and alignment in your protocol stack?"** *Strong:* explicit serialization, tested on both orders or with fuzzing. *Evasive:* "Everything we ship is little-endian."
3. **"Which arithmetic does your DSP or control code use, and how did you choose the formats?"** *Strong:* a quantization and overflow analysis per stage, with saturation and test vectors from the floating-point model. *Evasive:* "We converted the floats to ints."
4. **"What accuracy loss does your INT8 or INT4 path show on representative models, and how is calibration done?"** *Strong:* numbers per model and method. *Evasive:* peak TOPS only.

## 10. Concept check

1. Why does `~x + 1` equal `-x` in two's complement?

   <details><summary>Answer</summary>

   `x + ~x` is all ones, $2^n - 1$, so `~x + 1` $= 2^n - x$, which is congruent to $-x$ modulo $2^n$; $n$-bit arithmetic is modulo $2^n$, so that bit pattern is $-x$.

   </details>

2. Write expressions to set bit 5, clear bit 5, toggle bit 5 and test bit 5 of a `uint32_t r`.

   <details><summary>Answer</summary>

   `r |= 1u << 5;` `r &= ~(1u << 5);` `r ^= 1u << 5;` `if (r & (1u << 5))`.

   </details>

3. How do you extract a 4-bit field at bits 11:8, and insert the value `v` there?

   <details><summary>Answer</summary>

   Extract: `(r >> 8) & 0xFu`. Insert: `r = (r & ~(0xFu << 8)) | ((v & 0xFu) << 8);` clear the field, then OR in the masked, shifted value.

   </details>

4. Why must a hardware register be accessed through a `volatile` pointer, and what does `volatile` not provide?

   <details><summary>Answer</summary>

   The register changes or acts outside the program's view, so every read and write must really happen, in order; without `volatile` the compiler may cache a read or remove "redundant" writes. `volatile` does not make a read-modify-write atomic or protect against interrupts.

   </details>

5. How is `0x12345678` laid out in memory on a little-endian machine, and how should portable code read a big-endian 32-bit field from a byte buffer?

   <details><summary>Answer</summary>

   Bytes `78 56 34 12` at increasing addresses. Portable code assembles it with shifts: `(uint32_t)p[0] << 24 | (uint32_t)p[1] << 16 | (uint32_t)p[2] << 8 | p[3]`, which gives the same answer on every host.

   </details>

6. What does the integer 24,576 represent in Q15, and why must a Q15 product be shifted right by 15?

   <details><summary>Answer</summary>

   $24{,}576/32{,}768 = 0.75$. The product of two Q15 integers carries the scale $2^{-15}\times2^{-15} = 2^{-30}$ (Q30); shifting right by 15 restores the $2^{-15}$ scale.

   </details>

7. What is the RMS error of rounding to a step $\Delta$, and how much does one extra fractional bit improve the SNR?

   <details><summary>Answer</summary>

   $\Delta/\sqrt{12}$, assuming the error is uniform over $\pm\Delta/2$. One more bit halves $\Delta$, improving the SNR by $20\log_{10}2 \approx 6.02$ dB.

   </details>

8. Why did the Patriot clock drift, and why did the drift grow with time?

   <details><summary>Answer</summary>

   0.1 has no exact binary representation; chopped to 23 fractional bits it was too small by $2^{-20}$ of its value. Time was computed as ticks × (stored 0.1), so the error was a fixed fraction of the elapsed time: proportional to how long the system had been running, 0.3433 s after 100 hours. On its own that lag would largely have cancelled, because tracking subtracts two times; it caused the failure because a modified routine converted one of the two times more accurately than the other, so the errors no longer matched.

   </details>

Now work the [problem set](../problems/05-07-problems.md).

## 11. Key terms

[Two's complement](../../../reference/glossary.md#twos-complement) ·
[Sign extension](../../../reference/glossary.md#sign-extension) ·
[Bit mask](../../../reference/glossary.md#bit-mask) ·
[Bit field](../../../reference/glossary.md#bit-field) ·
[Memory-mapped I/O](../../../reference/glossary.md#memory-mapped-i-o) ·
[Volatile](../../../reference/glossary.md#volatile) ·
[Endianness](../../../reference/glossary.md#endianness) ·
[Fixed-point arithmetic](../../../reference/glossary.md#fixed-point-arithmetic) ·
[Q format](../../../reference/glossary.md#q-format) ·
[Saturation arithmetic](../../../reference/glossary.md#saturation-arithmetic) ·
[Quantization noise](../../../reference/glossary.md#quantization-noise)

## 12. Connections

- **Builds on:** [05-05](05-05-c-fundamentals.md) (integer types, promotion, undefined behavior), [05-06](05-06-c-pointers-and-memory.md) (pointers, byte buffers, structs), [05-02](05-02-numpy-and-vectorization.md) (fixed-width dtypes and wrap-around) and [03-03](../../03-probability-statistics-and-random-variables/chapters/03-03-expectation-and-functions-of-rvs.md) (the variance of a uniform error).
- **Next:** [05-08 Data Structures and Algorithms](05-08-data-structures-and-algorithms.md), where ring buffers use power-of-two masks and hash tables use bit mixing.
- **Used later:** [08-01](../../08-digital-logic-design/chapters/08-01-number-systems-and-codes.md) and [08-09](../../08-digital-logic-design/chapters/08-09-arithmetic-circuits.md) build these number formats in logic; [16 · Digital Signal Processing](../../16-digital-signal-processing/README.md) uses fixed-point filters; [18 · Embedded Systems](../../18-embedded-systems-and-microcontrollers/README.md) programs real peripheral registers; [20 · Analog and Mixed-Signal IC Design](../../20-analog-and-mixed-signal-ic-design/README.md) derives ADC quantization noise.

## 13. Further study

- Bryant and O'Hallaron, *Computer Systems: A Programmer's Perspective*, 3rd ed., chapter 2 ("Representing and Manipulating Information"): the definitive treatment of integer representations and their arithmetic.
- Warren, H. S., *Hacker's Delight*, 2nd ed., chapters 2–5: bit-manipulation techniques with proofs.
- Valvano, J. W., *Embedded Systems: Introduction to ARM Cortex-M Microcontrollers*, the chapters on I/O registers and fixed-point numbers (free online editions exist).
- Lyons, R. G., *Understanding Digital Signal Processing*, 3rd ed., chapter 12 ("Digital Data Formats and Their Effects").

## 14. Sources

1. Bryant and O'Hallaron, 3rd ed., 2016; Warren, *Hacker's Delight*, 2nd ed., Addison-Wesley, 2012.
2. ISO/IEC 9899:2024 (C23): two's complement, `<stdbit.h>`, `<stdckdint.h>`, `_BitInt`. [R-092]
3. Arm, *Cortex-M4 Devices Generic User Guide* (DUI 0553A); STMicroelectronics PM0214; RISC-V International, *The RISC-V Instruction Set Manual* (v20260120). [R-096]
4. U.S. GAO, GAO/IMTEC-92-26 (1992); Skeel, "Roundoff Error and the Patriot Missile", *SIAM News* 25(4), 1992. [R-057]
5. Ariane 501 Inquiry Board report (1996); FAA AD 2015-09-07 (2015). [R-093]
