# Problems 14-04 · Computer Arithmetic and Number Formats

Chapter: [14-04](../chapters/14-04-computer-arithmetic-and-number-formats.md) · Worked solutions: [14-04 solutions](../solutions/14-04-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** 32-bit RISC-V integers (RV32IM); FP32 with round to nearest, ties to even, unless stated; hexadecimal patterns are written most significant digit first. "ulp" is the gap between adjacent representable numbers at the value in question.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 14-04.1 [A]

**One pattern, two meanings.** For the 32-bit pattern 0xFFFFFF9C: (a) give its signed and unsigned values; (b) give the results of an arithmetic and of a logical right shift by 2, as patterns and as signed and unsigned numbers respectively.

### Problem 14-04.2 [A]

**Detecting overflow.** (a) Does 0x40000000 + 0x40000000 overflow as signed numbers? As unsigned numbers? (b) Does 0xFFFFFFFF + 0x00000002 overflow as unsigned numbers (a carry out)? As signed? Use the rules of §3.1 and show the test values.

### Problem 14-04.3 [A]

**Loading a byte.** Memory holds the byte 0xF0. What does `lb` load into a register, and what does `lbu` load? Give both as decimal numbers.

### Problem 14-04.4 [B]

**A full 64-bit product.** For $a$ = 0x89ABCDEF and $b$ = 0x12345678, find MUL, MULHU and MULH. Why do MULHU and MULH differ while MUL does not?

### Problem 14-04.5 [B]

**Division conventions.** Give the RV32IM results of (a) DIV and REM for −7 ÷ −2 and for 7 ÷ −2; (b) DIVU of 0xFFFFFFFE by 2; (c) REMU of 5 by 0.

### Problem 14-04.6 [B]

**Dividing by 3.** (a) Find $M = \lceil 2^{33}/3 \rceil$ and prove that $\lfloor xM/2^{33} \rfloor = \lfloor x/3 \rfloor$ for every unsigned 32-bit $x$. (b) Write the RV32IM sequence and say what it should share with clang's output for `x / 3`.

### Problem 14-04.7 [C]

**When 32 bits are not enough: dividing by 7.** (a) For $k$ = 0, 1, 2 find $M_k = \lceil 2^{32+k}/7 \rceil$ and the excess $e_k = 7M_k - 2^{32+k}$. Show that the shift $32 + k$ works for all 32-bit $x$ only if $e_k \le 2^k$, and that no $k \le 2$ qualifies. (b) For $k = 2$, find the smallest $x$ for which $\lfloor xM_2/2^{34} \rfloor \ne \lfloor x/7 \rfloor$. (c) $k = 3$ works but needs a 33-bit $M_3$. Show how the sequence below uses $t = \text{mulhu}(x, M_3 - 2^{32})$ to compute $\lfloor x/7 \rfloor$ without a 33-bit multiply, and give the 32-bit constant:

```text
mulhu t, x, M3_low      # t = (x * (M3 - 2^32)) >> 32
sub   q, x, t
srli  q, q, 1
add   q, q, t
srli  q, q, 2           # q = x / 7
```

### Problem 14-04.8 [B]

**Spacing of FP32 numbers.** (a) Find the ulp of FP32 at 1000. (b) What is the smallest positive integer that FP32 cannot represent exactly, and what does it round to?

### Problem 14-04.9 [B]

**Rounding by hand.** Using guard, round and sticky bits, give the FP32 result (as a bit pattern) of (a) $1.75 + (2^{-24} + 2^{-30})$; (b) $1.75 + 2^{-25}$; (c) $16\,777\,215 + 1.5$.

### Problem 14-04.10 [B]

**Fused or not.** With $a = 1 + 2^{-13}$, $b = 1 - 2^{-13}$ and $c = -1$, all exact in FP32, compute $ab + c$ (a) with a rounded multiply followed by a rounded add, and (b) with a fused multiply-add. Explain the difference.

### Problem 14-04.11 [B]

**How wide must the accumulator be?** A dot product has $K$ = 4096 terms. (a) Evaluate the worst-case relative error bound $(K - 1)u$ for a bfloat16 accumulator ($p$ = 8) and for an FP32 one. (b) What is the smallest precision $p$ for which the bound stays below 1%?

### Problem 14-04.12 [C]

**Clamping in a block-scaled format.** An MX block with FP4 (E2M1) elements has maximum magnitude 7.5. (a) Using the specification's rule, find the scale $X$, the element stored for 7.5 and the error. (b) A designer instead uses $X$ = 2. What is stored for 7.5, and with what error? (c) Over all possible block maxima, what is the largest relative clamping error the specification's rule allows, as a percentage? (d) What does the alternative cost elsewhere in the block?

### Problem 14-04.13 [C]

**Affine quantization.** Activations range over $[-1, 6]$ and are stored as unsigned 8-bit codes 0–255 with $x \approx s(q - z)$. (a) Find $s$ and the integer zero point $z$. (b) Quantize 2.5 and dequantize the result. (c) Why is $z$ an integer, and why does it matter that 0 is exactly representable?

### Problem 14-04.14 [C]

**Sizing accumulators exactly.** (a) An INT8 × INT8 dot product with symmetric operands (magnitudes up to 127) has $K$ = 4096 terms. How many bits, including the sign, does an accumulator need to be safe for every input? (b) Within one MX block, FP4 E2M1 elements multiply to products that are all multiples of 0.25, with magnitude at most 36. How many bits, including the sign, does a fixed-point accumulator need to sum the 32 products of a block exactly? (c) Why is exact block accumulation attractive in hardware?

### Problem 14-04.15 [B]

**A restoring divider by hand.** (a) Trace restoring division of the 8-bit unsigned dividend 200 by 7, one row per step, giving the shifted-in bit, $T = 2R + x_i$, the quotient bit and the new remainder. (b) Check the result. (c) How many cycles does a 32-bit divide take at one quotient bit per cycle, and at two? (d) Explain why one trial subtraction per step is always enough.

### Problem 14-04.16 [B]

**What a narrower format buys.** Use the $p^2$ area model of §3.6, with $p$ counting significand bits including the hidden 1 (FP4 E2M1 has $p$ = 2). (a) How many FP8 E4M3 multipliers fit in the area of one bfloat16 multiplier, and how many FP4 E2M1 multipliers in the area of one FP8 multiplier? (b) A vendor's peak throughput doubles from a 16-bit format to FP8. What fraction of the model's potential gain is that? (c) Name three parts of a MAC array that keep the gain below the model's.

---

## Objective coverage

| Learning objective (chapter 14-04) | Problems |
|---|---|
| 1. Integer results, comparisons, overflow, multiply-high and division | 1, 2, 3, 4, 5, 15 |
| 2. Division by a constant | 6, 7 |
| 3. Floating-point rounding and FMA | 8, 9, 10 |
| 4. Error in sums and accumulator width | 11, 14 |
| 5. Quantization, block scaling and cost | 12, 13, 14, 16 |
