# Problems 05-07 · Bit Manipulation and Fixed-Width Integers

Chapter: [05-07](../chapters/05-07-bit-manipulation.md) · Worked solutions: [05-07 solutions](../solutions/05-07-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** C17 with `<stdint.h>` types; "Q15" means a 16-bit signed integer scaled by $2^{-15}$. Work each answer by hand (binary or hex) first, then confirm it with a program.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 05-07.1 [A]

**Two's complement by hand.** (a) Write −1, −128 and +127 as 8-bit patterns in hex. (b) What values do the `int8_t` patterns `0xFF`, `0x80` and `0x7F` represent? (c) Negate `0x0C` (12) using "invert and add one".

### Problem 05-07.2 [A]

**Bitwise operators.** For `uint8_t x = 0xA5`, evaluate (as 8-bit results) `x & 0x0F`, `x | 0x40`, `x ^ 0xFF`, `(uint8_t)(x << 2)` and `x >> 3`.

### Problem 05-07.3 [A]

**Ranges and resolutions.** Give the range of `int16_t`, of a 12-bit two's-complement field, and of Q15; and the resolution of Q15 and of Q8.8 (16 bits with 8 fractional bits). What is the largest value Q8.8 can hold?

### Problem 05-07.4 [B]

**Sign-extending odd widths.** Write `int32_t sign_extend(uint32_t field, unsigned bits)` for any width from 1 to 31 using the XOR identity, and evaluate it for the 12-bit fields `0x800`, `0x7FF`, `0xFFF` and the 5-bit field `0x13`.

### Problem 05-07.5 [B]

**A mode field.** A register holds `0xFFFF00F0`. Its `MODE` field occupies bits 6:4. (a) What is the current `MODE`? (b) Write `MODE` = 3 without changing any other bit; give the new register value. (c) What would `reg |= 3u << 4` have produced instead, and why is it wrong?

### Problem 05-07.6 [B]

**Byte order.** (a) List the bytes of `0x0A0B0C0D` at increasing addresses on little- and big-endian machines. (b) A little-endian 32-bit field arrives as `{0x10, 0x27, 0x00, 0x00}`; what is its value? (c) Write a function that swaps the byte order of a `uint32_t` using shifts and masks.

### Problem 05-07.7 [B]

**Choosing a Q format.** (a) Represent −0.3 in Q15 (rounded) and give the representation error. (b) Represent 3.3 V in Q8.8 and give its error. (c) Multiply 0.25 by 0.5 in Q15.

### Problem 05-07.8 [B]

**Power-of-two tricks.** (a) Write `is_pow2(x)` for `uint32_t x` and test it on 0, 1, 64, 96 and 1024. (b) Compute `1234 % 256` with a mask. (c) Write a function returning the smallest power of two ≥ x, and apply it to 1000.

### Problem 05-07.9 [B]

**Counting bits.** (a) How many 1 bits are in `0xF0F0`? (b) What is the parity (1 if the number of 1 bits is odd) of `0x5A`? (c) Write a population count that loops once per *set* bit, using `x &= x - 1`.

### Problem 05-07.10 [C]

**How many bits would the Patriot clock have needed?** Time is computed as ticks × (0.1 chopped to $b$ fractional bits), with one tick every 0.1 s. (a) Confirm that $b$ = 23 gives a drift of 0.3433 s after 100 hours. (b) What drift would $b$ = 24 give? (c) What is the smallest $b$ that keeps the drift below 1 ms after 100 hours? (d) What design would remove the drift entirely?

### Problem 05-07.11 [C]

**Quantization noise, measured.** Convert 100,000 uniformly random values in $[-0.9, 0.9)$ to Q15 by rounding (seed your generator), and measure the RMS conversion error. Compare with $\Delta/\sqrt{12}$, and with the RMS error when truncating (rounding toward −∞) instead. Explain the difference.

### Problem 05-07.12 [C]

**The Internet checksum.** IPv4 headers carry a 16-bit ones'-complement checksum: add the header's 16-bit big-endian words with the checksum field set to 0, fold any carries out of bit 15 back into the low 16 bits, and take the bitwise complement. Compute the checksum of the header words `4500 0073 0000 4000 4011 0000 C0A8 0001 C0A8 00C7` (hex), and show that summing the header *with* the checksum inserted gives `0xFFFF`.

---

## Objective coverage

| Learning objective (chapter 05-07) | Problems |
|---|---|
| 1. Binary, hex and two's complement | 1, 3, 4 |
| 2. Masks, shifts and bit fields | 2, 5, 8, 9 |
| 3. Register access | 5 |
| 4. Byte order and serialization | 6, 12 |
| 5. Fixed point, rounding and quantization | 3, 7, 10, 11 |
