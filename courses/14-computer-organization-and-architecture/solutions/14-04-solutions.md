# Solutions 14-04 · Computer Arithmetic and Number Formats

Problems: [14-04 problems](../problems/14-04-problems.md) · Chapter: [14-04](../chapters/14-04-computer-arithmetic-and-number-formats.md). Every number below is recomputed by [verify_14_04.py](../verify/verify_14_04.py). The integer results run on the course's RV32IM simulator, the floating-point results are computed in FP32 and checked against exact rational arithmetic, and the division sequences are compiled by clang and tested on random and boundary inputs.

---

## Solutions

### Solution 14-04.1

(a) As unsigned, 0xFFFFFF9C is $2^{32} - 100$ = **4294967196**. As signed it is **−100**.

(b) The arithmetic shift copies the sign bit, giving 0xFFFFFFE7, which is $-100/4$ = **−25**. The logical shift fills with zeros, giving **0x3FFFFFE7**, which is $\lfloor 4294967196/4 \rfloor$ = 1073741799.

### Solution 14-04.2

(a) The sum is $s$ = 0x80000000. As signed numbers, both operands are positive and the result is negative. The test value is $(a \oplus s) \wedge (b \oplus s)$ = 0xC0000000 ∧ 0xC0000000 = 0xC0000000, with sign bit **1**: it overflows. As unsigned numbers, $s \ge a$, so there is no carry: $2^{31}$ fits.

(b) The sum wraps to $s$ = 0x00000001. Since $s < a$ (1 < 0xFFFFFFFF), there is an unsigned carry, **1**. As signed numbers it is $-1 + 2 = 1$: the operands have opposite signs, so it cannot overflow. The test value is 0xFFFFFFFE ∧ 0x00000003 = 0x00000002, with sign bit **0**.

### Solution 14-04.3

`lb` sign-extends: 0xF0 = 1111 0000 has its top bit set, giving 0xFFFFFFF0 = **−16**. `lbu` zero-extends, giving **240**.

### Solution 14-04.4

As unsigned numbers the product is 0x89ABCDEF × 0x12345678 = 0x09CA39E0_E242D208. So MUL = **0xE242D208** and MULHU = **0x09CA39E0**.

As signed numbers, $a$ is negative ($a - 2^{32}$), and the product is smaller by $2^{32}b$, which lowers the high word by $b$: 0x09CA39E0 − 0x12345678 = **0xF795E368**. That is MULH.

The low word is unchanged because subtracting a multiple of $2^{32}$ does not affect the low 32 bits.

### Solution 14-04.5

(a) Quotients round toward zero and remainders take the dividend's sign:

- −7 ÷ −2 gives quotient **3** and remainder −7 − (−2)(3) = **−1**;
- 7 ÷ −2 gives quotient **−3** and remainder 7 − (−2)(−3) = **1**.

(b) DIVU treats 0xFFFFFFFE as $2^{32} - 2$, so the quotient is $2^{31} - 1$ = **0x7FFFFFFF**.

(c) The remainder of a division by zero is the dividend: **5**.

### Solution 14-04.6

(a) $M = \lceil 2^{33}/3 \rceil = (2^{33} + 1)/3$ = **0xAAAAAAAB** (2,863,311,531). Then

$$
\frac{xM}{2^{33}} = \frac{x}{3} + \frac{x}{3 \cdot 2^{33}} .
$$

The error term is below $2^{32}/(3 \cdot 2^{33}) = 1/6$. Write $x = 3q + r$ with $r \le 2$: the fractional part $r/3 \le 2/3$, and $2/3 + 1/6 = 5/6 < 1$. So the floor is always $q$.

(b) The sequence is `lui a1, 0xAAAAB` / `addi a1, a1, -1365` (building 0xAAAAAAAB), `mulhu a0, a0, a1`, `srli a0, a0, 1`. The total shift is **33**. Clang's output must use the same constant and shift, and it does (the verify script compiles it).

### Solution 14-04.7

(a) The magic numbers and excesses are:

| $k$ | $M_k$ | $e_k = 7M_k - 2^{32+k}$ | $2^k$ |
|---|---|---|---|
| 0 | 613,566,757 | 3 | 1 |
| 1 | 1,227,133,514 | 6 | 2 |
| 2 | 2,454,267,027 | 5 | 4 |

The error term is $xM_k/2^{32+k} - x/7 = x e_k / (7 \cdot 2^{32+k})$. With $x = 7q + r$, the floor stays $q$ as long as $r/7 + x e_k/(7 \cdot 2^{32+k}) < 1$, that is, $r + x e_k/2^{32+k} < 7$.

- **Sufficient:** the worst case has $r = 6$ and $x$ near $2^{32}$, where the condition becomes $e_k \cdot 2^{32}/2^{32+k} < 1$, which holds if $e_k \le 2^k$ (with equality, $x < 2^{32}$ keeps it strict).
- **Necessary:** take the largest 32-bit $x$ with remainder 6. Since $2^{32} \bmod 7$ = 4, that is $x^* = 2^{32} - 5$. For it the condition reads $6 + x^*e_k/2^{32+k} < 7$, i.e. $x^*e_k < 2^{32+k}$. If $e_k \ge 2^k + 1$, then $x^*e_k \ge (2^{32} - 5)(2^k + 1) = 2^{32+k} + 2^{32} - 5 \cdot 2^k - 5 > 2^{32+k}$, because $2^{32}$ dwarfs $5 \cdot 2^k + 5$. So the floor fails at $x^*$. Since $e_k$ is an integer, the shift works if and only if $e_k \le 2^k$.
- **Not met for $k \le 2$:** $e_k$ exceeds $2^k$ in every row of the table. Indeed $x^*$ = 4,294,967,291 gives 613,566,756 for all three shifts, while $\lfloor x^*/7 \rfloor$ = 613,566,755.

(b) For $k$ = 2 the condition fails when $r = 6$ and $5x/2^{34} \ge 1$, that is, $x \ge 2^{34}/5 = 3\,435\,973\,836.8$. The smallest $x \ge 3\,435\,973\,837$ with $x \bmod 7 = 6$ is **3435973841**. There the sequence gives 490,853,406 instead of the correct 490,853,405. Every smaller $x$ is safe: for $r \le 5$ the condition needs $5x/2^{34} \ge 2$, which is beyond $2^{32}$.

(c) For $k = 3$, $M_3 = \lceil 2^{35}/7 \rceil$ = 4,908,534,053, whose excess $e_3$ = 3 does not exceed $2^3$. But $M_3 > 2^{32}$. Write $M_3 = 2^{32} + m$ with $m$ = **0x24924925**, so that $xM_3/2^{32} = x + t$ (up to the floor), where $t = \lfloor xm/2^{32} \rfloor$ is one MULHU. The quotient is then $\lfloor (x + t)/8 \rfloor$. However, $x + t$ can overflow 32 bits, so the sequence computes it as $((x - t)/2 + t)/4$:

- $x - t$ cannot underflow, since $t \le x$;
- halving it before adding $t$ keeps every intermediate below $2^{32}$;
- $\lfloor (x - t)/2 \rfloor + t = \lfloor (x + t)/2 \rfloor$, so shifting right by 2 more gives $\lfloor (x + t)/8 \rfloor$.

Clang emits exactly this sequence, with the constant 0x24924925.

### Solution 14-04.8

(a) 1000 lies in $[2^9, 2^{10})$, where the ulp is $2^{9 - 23} = 2^{-14}$ = **6.1035 × 10⁻⁵**.

(b) With 24 bits of precision, every integer up to $2^{24}$ is exact. Above $2^{24}$ the spacing is 2, so **16777217** ($2^{24} + 1$) is the first integer that cannot be represented. It lies exactly halfway between $2^{24}$ and $2^{24} + 2$, and ties go to the even significand, so it rounds to **16777216**.

### Solution 14-04.9

Near 1.75 (binade $[1, 2)$) the ulp is $2^{-23}$.

(a) $2^{-24} + 2^{-30}$ is half an ulp plus a little, so G = 1 and the $2^{-30}$ term sets S = 1. That is above half, so it rounds up: $1.75 + 2^{-23}$ = **0x3FE00001**.

(b) $2^{-25}$ is a quarter of an ulp: G = 0 and R = 1, below half, so it rounds down to 1.75 = **0x3FE00000**.

(c) The exact sum 16,777,216.5 lies in $[2^{24}, 2^{25})$, where the spacing is 2. The neighbours are 16,777,216 and 16,777,218, and it is nearer the first, so the result is 16,777,216 = **0x4B800000**. The 0.5 was lost entirely.

### Solution 14-04.10

The exact product is $ab = 1 - 2^{-26}$. Just below 1 the FP32 spacing is $2^{-24}$, so the nearest FP32 numbers are 1 and $1 - 2^{-24}$, and $1 - 2^{-26}$ is nearer 1.

(a) The rounded product is 1, and $1 - 1$ = **0**.

(b) The FMA adds $c$ to the exact product and rounds once: $1 - 2^{-26} - 1 = -2^{-26}$ = **−1.4901 × 10⁻⁸**, exactly representable.

The separate multiply threw away the very bits the subtraction needed (cancellation, §3.4). The FMA keeps them. This is why FMA-based algorithms can compute exact products and residuals, and why results can differ between machines that do and do not fuse.

### Solution 14-04.11

(a) For bfloat16, $u = 2^{-8}$, so the bound is $4095 \times 2^{-8}$ = **16.00**, a 1600% worst case: useless. For FP32, $4095 \times 2^{-24}$ = **2.441 × 10⁻⁴**, or 0.024%.

(b) The bound is below 1% when $4095 \times 2^{-p} < 0.01$, that is, $p > \log_2(409\,500) = 18.6$. So $p$ = **19** bits suffice. FP32 ($p$ = 24) qualifies; FP16 ($p$ = 11) and bfloat16 do not.

The bound is a worst case. Typical errors grow more like $\sqrt{K}u$ when rounding errors have random signs, but the worst case is what a hardware designer must survive.

### Solution 14-04.12

(a) The largest power of two not above 7.5 is 4, and E2M1's largest power of two is 4, so $X$ = **1**. The scaled value 7.5 exceeds the largest E2M1 value, 6, so it is clamped to **6**: an error of **1.5** (20%).

(b) With $X$ = 2, the scaled value is 3.75, which rounds to 4 (between 3 and 4 the nearer is 4) and represents 8: an error of **0.5**.

(c) Under the specification's rule, a scaled maximum lies in $[4, 8)$, and anything above 6 is clamped to 6. The relative error $(m - 6)/m$ approaches $2/8$ = **25**% as the scaled maximum approaches 8.

(d) Doubling the scale doubles the spacing for every other element of the block. With $X$ = 2 the smallest nonzero value is 1 instead of 0.5, so anything below 0.5 (instead of below 0.25) flushes to zero, and every small value is stored half as precisely. The power-of-two rule protects small values and accepts occasional clamping of the largest. Formats with finer blocks or non-power-of-two scales, such as NVFP4's E4M3 scales, are designed to reduce this trade-off.

### Solution 14-04.13

(a) The range $6 - (-1) = 7$ is spread over 255 steps: $s = 7/255$ = **0.027451**. Zero must map to an integer code $z$ with $0 = s(z - z)$, and $-1$ should map to code 0, so $z = \mathrm{round}(1/s) = \mathrm{round}(36.43)$ = **36**.

(b) $q = \mathrm{round}(2.5/s) + z = \mathrm{round}(91.07) + 36$ = **127**. Dequantized, $s(127 - 36)$ = **2.4980**.

(c) An integer zero point makes the real value 0 exactly representable, as code $z$. That matters because zero padding, ReLU outputs and sparse weights are exactly zero in the model: an inexact zero would add a bias to every padded convolution and every masked element. The integer $z$ also lets integer matrix kernels fold the zero point into a few correction terms.

### Solution 14-04.14

(a) The largest possible sum is $4096 \times 127^2$ = 66,064,384, which is below $2^{26}$ = 67,108,864. So 26 magnitude bits plus a sign give **27** bits: an INT32 accumulator has 5 bits to spare.

(b) In units of 0.25, each product is an integer of magnitude at most 144, and 32 of them sum to at most 4608. That is below $2^{13}$ = 8192, so 13 magnitude bits plus a sign give **14** bits for an exact block sum.

(c) Exact fixed-point accumulation inside a block needs only a small integer adder tree: no alignment shifters, no rounding, and no dependence on summation order. Only the block results, scaled by the two blocks' power-of-two scales (an exponent addition), need a floating-point accumulator. This is a large part of why block-scaled FP4 is cheap in hardware.

### Solution 14-04.15

(a) 200 = 1100 1000 in binary and $d$ = 7. Each step shifts the next bit into $T = 2R + x_i$ and subtracts 7 if it fits:

<!-- trace 200/7 -->

| Step | Bit in | $T$ | $T \ge 7$? | $R$ after |
|---|---|---|---|---|
| 1 | 1 | 1 | no (0) | 1 |
| 2 | 1 | 3 | no (0) | 3 |
| 3 | 0 | 6 | no (0) | 6 |
| 4 | 0 | 12 | yes (1) | 5 |
| 5 | 1 | 11 | yes (1) | 4 |
| 6 | 0 | 8 | yes (1) | 1 |
| 7 | 0 | 2 | no (0) | 2 |
| 8 | 0 | 4 | no (0) | 4 |

The quotient bits read 0001 1100 = **28**, and the remainder is **4**.

(b) 28 × 7 + 4 = 196 + 4 = 200, and 4 < 7.

(c) At one bit per cycle a 32-bit quotient needs **32** cycles. At two bits per cycle (radix 4) it needs **16**.

(d) The remainder entering a step satisfies $R < d$, so $T = 2R + x_i \le 2(d - 1) + 1 = 2d - 1 < 2d$. $T$ therefore contains $d$ at most once, and a single compare-and-subtract settles the bit. In the trace, $T$ never exceeds 2 × 7 − 1 = 13 (its largest value is 12).

### Solution 14-04.16

(a) bfloat16 has $p$ = 8, so $p^2$ = 64. FP8 E4M3 has $p$ = 4, so $p^2$ = 16: **4** FP8 multipliers fit in one bfloat16 multiplier's area. FP4 E2M1 has $p$ = 2, so $p^2$ = 4, and **4** FP4 multipliers fit in one FP8 multiplier's area.

(b) Doubling achieves 2 of the model's 4, i.e. **50**% of the potential gain.

(c) Any three of the following. Operand delivery: each halving of width halves the bytes per value, but feeding four times as many multipliers needs twice the bytes per cycle from registers and buffers. Accumulators: products are summed in FP32 or wide integers whatever the input width, so the adders do not shrink. Exponent and alignment logic, and per-block scaling for MX formats. Wiring and control. The multiplier itself is only part of a MAC unit's area and energy.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 14-04.1a | unsigned value | 4294967196 | — |
| 14-04.1b | signed value | −100 | — |
| 14-04.1c | arithmetic shift right by 2 | −25 | — |
| 14-04.1d | logical shift right by 2 | 0x3FFFFFE7 | — |
| 14-04.2a | signed-overflow sign bit, 0x40000000 + 0x40000000 | 1 | — |
| 14-04.2b | unsigned carry, 0xFFFFFFFF + 2 | 1 | — |
| 14-04.2c | signed-overflow sign bit, 0xFFFFFFFF + 2 | 0 | — |
| 14-04.3a | lb of 0xF0 | −16 | — |
| 14-04.3b | lbu of 0xF0 | 240 | — |
| 14-04.4a | MUL | 0xE242D208 | — |
| 14-04.4b | MULHU | 0x09CA39E0 | — |
| 14-04.4c | MULH | 0xF795E368 | — |
| 14-04.5a | DIV −7 ÷ −2 | 3 | — |
| 14-04.5b | REM −7 ÷ −2 | −1 | — |
| 14-04.5c | DIV 7 ÷ −2 | −3 | — |
| 14-04.5d | REM 7 ÷ −2 | 1 | — |
| 14-04.5e | DIVU 0xFFFFFFFE ÷ 2 | 0x7FFFFFFF | — |
| 14-04.5f | REMU 5 ÷ 0 | 5 | — |
| 14-04.6a | magic number for ÷ 3 | 0xAAAAAAAB | — |
| 14-04.6b | total shift | 33 | bits |
| 14-04.7a | smallest failing x for k = 2 | 3435973841 | — |
| 14-04.7b | low 32 bits of M3 | 0x24924925 | — |
| 14-04.7c | necessity witness x* | 4294967291 | — |
| 14-04.7d | shifted result at x*, k = 0 to 2 | 613566756 | — |
| 14-04.7e | true quotient at x* | 613566755 | — |
| 14-04.8a | ulp of FP32 at 1000 | 6.1035e-5 | — |
| 14-04.8b | smallest unrepresentable integer | 16777217 | — |
| 14-04.8c | it rounds to | 16777216 | — |
| 14-04.9a | 1.75 + (2⁻²⁴ + 2⁻³⁰) | 0x3FE00001 | — |
| 14-04.9b | 1.75 + 2⁻²⁵ | 0x3FE00000 | — |
| 14-04.9c | 16777215 + 1.5 | 0x4B800000 | — |
| 14-04.10a | separate multiply and add | 0 | — |
| 14-04.10b | fused multiply-add | −1.4901e-8 | — |
| 14-04.11a | bound, bfloat16 accumulator | 16.00 | — |
| 14-04.11b | bound, FP32 accumulator | 2.441e-4 | — |
| 14-04.11c | minimum precision for 1% | 19 | bits |
| 14-04.12a | MX scale | 1 | — |
| 14-04.12b | stored element for 7.5 | 6 | — |
| 14-04.12c | clamping error | 1.5 | — |
| 14-04.12d | error with X = 2 | 0.5 | — |
| 14-04.12e | worst-case relative clamping error | 25 | % |
| 14-04.13a | scale | 0.027451 | — |
| 14-04.13b | zero point | 36 | — |
| 14-04.13c | code for 2.5 | 127 | — |
| 14-04.13d | dequantized value | 2.4980 | — |
| 14-04.14a | INT8 accumulator bits, K = 4096 | 27 | bits |
| 14-04.14b | exact FP4 block accumulator bits | 14 | bits |
| 14-04.15a | quotient of 200 ÷ 7 | 28 | — |
| 14-04.15b | remainder | 4 | — |
| 14-04.15c | cycles at one bit per cycle | 32 | — |
| 14-04.15d | cycles at two bits per cycle | 16 | — |
| 14-04.15e | largest possible T for d = 7 | 13 | — |
| 14-04.15f | largest T in the trace | 12 | — |
| 14-04.16a | FP8 multipliers per bfloat16 multiplier | 4 | — |
| 14-04.16b | FP4 multipliers per FP8 multiplier | 4 | — |
| 14-04.16c | share of the model's gain | 50 | % |
