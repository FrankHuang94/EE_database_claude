# Problems 08-09 · Arithmetic Circuits

Chapter: [08-09](../chapters/08-09-arithmetic-circuits.md) · Worked solutions: [08-09 solutions](../solutions/08-09-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** the unit-delay model of chapter §3.1 (every two-input gate 1 unit; a $\circ$ operator 2 units on $G$; a 2:1 multiplexer 2 units, with the select's complement available; the carry-in folded into bit 0's generate). Bit 0 is the least significant. Signed numbers are two's complement.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 08-09.1 [A]

**Generate and propagate.** For the 8-bit addition $A$ = 0101 1100 (92) and $B$ = 0011 1011 (59) with $C_0 = 0$: (a) give $G$ and $P$ as integers; (b) give the sum and the carry out; (c) through how many bits does the longest carry chain propagate?

### Problem 08-09.2 [A]

**The prefix operator.** Bits 3 to 0 have $(G, P)$ = (0, 1), (0, 1), (1, 0), (0, 0). (a) Compute $(G_{3:0}, P_{3:0})$ by combining $((3 \circ 2) \circ (1 \circ 0))$, and check that $(3 \circ (2 \circ (1 \circ 0)))$ gives the same. (b) Compute $(0, 0) \circ (1, 0)$ and $(1, 0) \circ (0, 0)$, and explain the difference in words.

### Problem 08-09.3 [A]

**Counting operators.** For 32-bit adders, give the number of $\circ$ operators and the number of levels of Kogge–Stone, Sklansky and Brent–Kung networks.

### Problem 08-09.4 [B]

**A 64-bit adder in picoseconds.** With 15 ps per unit, what is the delay to the slowest sum bit of a 64-bit (a) ripple-carry, (b) Kogge–Stone and (c) Brent–Kung adder, given that the arrival-time simulation of the chapter gives 128, 14 and 24 units? (d) How many operators does the 64-bit Kogge–Stone network use?

### Problem 08-09.5 [B]

**Carry-select in four blocks.** A 32-bit carry-select adder uses four 8-bit blocks: the lowest is one 8-bit ripple adder, and each of the others is a pair of 8-bit ripple adders (carry-in 0 and 1) followed by multiplexers selecting the 8 sum bits and the block carry-out. (a) What is its delay? (b) How many full adders and multiplexers does it use?

### Problem 08-09.6 [B]

**Lookahead equations.** (a) Write $C_3$ in flat lookahead form and count its product terms. (b) How many product terms, and what largest fan-in, would a flat $C_8$ have? (c) A 16-bit adder uses four 4-bit lookahead groups and a second lookahead level. Which carries does the second level compute directly?

### Problem 08-09.7 [B]

**A 12 × 12 Dadda multiplier.** (a) How many partial-product bits are there? (b) List the Dadda targets used and the number of levels. (c) How many full adders and half adders does the reduction use, and how wide is the final adder?

### Problem 08-09.8 [B]

**Booth recoding of a negative multiplier.** Recode $B = -99$ (8-bit two's complement) into radix-4 Booth digits, check their value, and compute $7 \times (-99)$ from the digits. How many nonzero partial products are there?

### Problem 08-09.9 [B]

**Shifters.** (a) How many stages and 2:1 multiplexers does a 64-bit logarithmic barrel shifter need? How many would 64 separate 64:1 multiplexers built from 2:1 multiplexers need? (b) The 8-bit pattern for $-40$ is shifted right by 3. What results do a logical and an arithmetic right shift give, as signed integers?

### Problem 08-09.10 [B]

**Choosing a Q format.** A sensor gain is stored in Q4.12 (16 bits, with the chapter's convention that the 4 integer bits include the sign). (a) What are the largest representable value and the resolution? (b) Store $e = 2.718281828\ldots$ by rounding to the nearest code: what is the integer code, and what is the representation error?

### Problem 08-09.11 [B]

**Sizing a filter datapath.** A 256-tap filter multiplies signed 12-bit ADC samples by signed 16-bit coefficients. (a) How many bits does each product need? (b) How wide must the accumulator be to never overflow?

### Problem 08-09.12 [B]

**How many bits for a given SQNR?** (a) What is the SQNR of a full-scale sine quantized to 12 bits? (b) How many bits are needed for at least 90 dB? (c) What is the SQNR of 24-bit audio?

### Problem 08-09.13 [C]

**Rounding bias.** A Q2.30 product is converted to Q1.15 by dropping 15 bits. Assume the dropped 15 bits are uniformly distributed over all their values. (a) What is the mean error, in LSBs of the result, of truncation? (b) Of round-half-up (add $2^{14}$, then drop)? (c) A recursive filter performs 1000 such conversions whose errors add. What is the accumulated bias in each case?

### Problem 08-09.14 [C]

**Guard bits in an FPGA DSP slice.** A DSP slice has a 27 × 18 signed multiplier and a 48-bit accumulator. (a) How wide is a full 27 × 18 product, how many guard bits remain, and how many worst-case products can be accumulated without overflow? (b) Repeat for 18 × 18 products.

### Problem 08-09.15 [C]

**The energy of a MAC.** Using the 45 nm estimates of chapter §3.9, take an INT8 MAC as an 8-bit multiply plus a 32-bit add, and an FP32 MAC as a 32-bit floating-point multiply plus add. (a) What are their energies, and the energy of $10^{12}$ of each? What is the ratio? (b) How many INT8 MACs cost as much as one 64-bit read from a 32 KB cache? (c) If every INT8 MAC needed one such cache read for its operands, what fraction of the energy would the arithmetic be?

---

## Objective coverage

| Learning objective (chapter 08-09) | Problems |
|---|---|
| 1. Generate, propagate, prefix operator, lookahead | 1, 2, 6 |
| 2. Ripple, carry-select and prefix adders | 3, 4, 5 |
| 3. Multipliers and Booth recoding | 7, 8, 14 |
| 4. Shifters | 9 |
| 5. Fixed-point datapaths | 10, 11, 12, 13, 14 |
| 6. Energy of arithmetic | 15 |
