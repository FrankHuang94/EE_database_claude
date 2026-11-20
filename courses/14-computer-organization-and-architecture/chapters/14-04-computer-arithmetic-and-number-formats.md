<!-- status: verified -->
# 14-04 · Computer Arithmetic and Number Formats

| | |
|---|---|
| **Course** | [14 · Computer Organization and Architecture](../README.md) |
| **University equivalent** | The arithmetic chapter of a computer organization course: integer arithmetic and overflow, multiplication and division instructions, IEEE 754 floating-point arithmetic and rounding (Patterson & Hennessy, *Computer Organization and Design*, RISC-V Edition, ch. 3), with the numerical-error and reduced-precision material of an introductory numerical-computing or ML-systems course |
| **Prerequisites** | [08-01 Number Systems and Codes](../../08-digital-logic-design/chapters/08-01-number-systems-and-codes.md), [08-09 Arithmetic Circuits](../../08-digital-logic-design/chapters/08-09-arithmetic-circuits.md), [14-03 Assembly and the Compilation Stack](14-03-assembly-and-the-compilation-stack.md) |
| **Estimated study hours** | 7 |
| **Last verified** | 2026-11-20 |

**Learning objectives.** After this chapter you can:

1. Predict the results of 32-bit integer operations, including wraparound, signed and unsigned comparisons, overflow detection, and RISC-V's multiply-high and division corner cases.
2. Derive and prove the multiply-and-shift replacement for division by a constant.
3. Carry out floating-point addition by hand with guard, round and sticky bits, apply round-to-nearest-even, and explain fused multiply-add.
4. Bound and compare the error of sequential, pairwise and compensated summation, and explain why AI hardware accumulates in a wider format.
5. Quantize data to INT8 and to block-scaled (MX) formats, size the accumulator, and relate a format's width to its multiplier cost.

---

## 1. Big picture

[08-01](../../08-digital-logic-design/chapters/08-01-number-systems-and-codes.md) defined the number formats: two's complement integers, fixed point, and floating point from FP32 down to FP8. [08-09](../../08-digital-logic-design/chapters/08-09-arithmetic-circuits.md) built the adders and multipliers. This chapter is about what happens when programs *compute* with those formats: which answers the hardware gives, where they differ from mathematics, and how much those differences cost. Every result is exact, wrapped or rounded according to rules that the ISA and the IEEE 754 standard fix bit for bit. Knowing those rules separates a numerical result you can trust from one that is quietly wrong.

- **Integers wrap.** A 32-bit sum that exceeds $2^{31} - 1$ becomes negative, with no error raised in RISC-V. Overflow detection is the programmer's or compiler's job.
- **Division is slow, so compilers avoid it.** Dividing by a constant becomes a multiply and a shift, an exact identity this chapter proves.
- **Floating point rounds after every operation.** Rounding makes addition non-associative and lets errors accumulate. Summing a million numbers naively in FP32 can be wrong in the third significant digit (Example 14-04.5).
- **AI runs on narrow formats.** Training and inference use bfloat16, FP8, FP4 and INT8 with shared scale factors and wide accumulators. The choice of format sets chip area, energy and accuracy, and it is where accelerator vendors compete (14-14).

## 2. Intuition first

**Integers live on a circle, like a car's odometer.** A 32-bit register has $2^{32}$ states. Counting up from the largest value wraps to the smallest, just as an odometer rolls from 999999 to 000000. Whether a pattern means a large positive number or a negative one is a matter of interpretation. The adder does the same thing either way; only comparisons, division, widening and overflow checks care about the interpretation.

**Floating point is scientific notation with a fixed number of digits.** Writing every number as $\pm d.ddd \times 10^e$ with four digits makes 1.234 and 1234 equally precise *relative to their size*. But adding them forces one to adopt the other's exponent: $1234 + 1.234 = 1235.234$, which four digits must round to 1235. The small number's last digits fall off the end. Repeat this a million times, adding 0.1 to a growing total, and the lost pieces add up to a visible error.

**Rounding to nearest, ties to even, is banker's rounding.** Finance learned long ago that always rounding halves up adds an upward drift to sums of many rounded amounts. Rounding halves to the nearest *even* digit sends half the ties up and half down, so the drift cancels on average. IEEE 754 uses the same rule as its default for exactly the same reason.

**Where the analogies break.** Odometers are decimal and rounding in finance is decimal, but computers round in binary. The decimal fraction 0.1 has no finite binary expansion, so it is already rounded when stored, before any arithmetic happens. And unlike a banker, the hardware rounds after *every* operation, millions of times a second, with no one checking.

## 3. Theory

### 3.1 Integer arithmetic in the ISA

RV32I computes on 32-bit words modulo $2^{32}$. ADD, SUB and the shifts produce the low 32 bits of the exact result, and the same ADD instruction serves signed and unsigned integers, because two's complement was designed so that it can (08-01). The interpretation matters in four places:

- **Comparisons.** SLT and BLT compare as signed numbers, SLTU and BLTU as unsigned. The pattern 0xFFFFFFFF is −1 to SLT and 4,294,967,295 to SLTU.
- **Right shifts.** SRA copies the sign bit in from the left (signed division by $2^k$, rounding toward $-\infty$), while SRL shifts in zeros (unsigned).
- **Widening.** Loading a byte with LB sign-extends it, while LBU zero-extends it.
- **Overflow.** An unsigned addition $s = a + b$ carries out exactly when $s < a$ as unsigned numbers (14-02 Problem 13). A signed addition overflows exactly when both operands have the same sign and the result has the other, which is when the sign bit of $(a \oplus s) \wedge (b \oplus s)$ is 1.

RISC-V raises no exception on overflow. C makes unsigned arithmetic wrap modulo $2^{32}$ by definition, but leaves *signed* overflow undefined. Compilers exploit that to optimize, so code that relies on signed wraparound is a classic source of bugs.

### 3.2 Multiplication and division

The product of two 32-bit numbers has up to 64 bits. The M extension provides four multiply instructions [1]:

| Instruction | Result |
|---|---|
| MUL | low 32 bits of the product (the same for signed and unsigned) |
| MULH | high 32 bits, both operands signed |
| MULHU | high 32 bits, both unsigned |
| MULHSU | high 32 bits, first operand signed, second unsigned |

The low halves agree for every interpretation, but the high halves differ (Example 14-04.2). For the full 64-bit product, the specification recommends issuing MULH[[S]U] and then MUL with the same operands, a pair that hardware may fuse into one operation [1].

**Division** (DIV, DIVU, REM, REMU) rounds the quotient toward zero, and the remainder takes the sign of the dividend, so $7 \div (-2) = -3$ remainder 1 and $-7 \div 2 = -3$ remainder $-1$. RISC-V defines the two awkward cases instead of trapping [1]:

| Case | Quotient | Remainder |
|---|---|---|
| Division by zero | all bits set (−1, or $2^{32} - 1$ unsigned) | the dividend |
| Signed overflow, $-2^{31} \div -1$ | $-2^{31}$ (the dividend) | 0 |

Without a trap, a divide unit needs no special path into the exception machinery. Software that must detect division by zero adds one branch. C leaves both cases undefined, so portable code must test for them anyway.

**How a divider works: restoring division.** Long division in base 2 needs no guessing: each quotient bit is 0 or 1, and one trial subtraction decides it. To divide an $n$-bit unsigned $x$ by $d \ne 0$, keep a partial remainder $R$, starting at 0, and take the dividend's bits $x_{n-1}, \ldots, x_0$ from the top:

1. Shift a dividend bit in: $T = 2R + x_i$.
2. Trial-subtract: if $T \ge d$, set $q_i = 1$ and $R = T - d$; otherwise $q_i = 0$ and $R = T$.

Why one subtraction suffices: let $X_i = \lfloor x/2^i \rfloor$ be the dividend's top bits and $Q_i$ the quotient bits found so far. The loop keeps the invariant $X_i = Q_id + R$ with $0 \le R < d$. Shifting in a bit gives $X_i = 2X_{i+1} + x_i = 2Q_{i+1}d + T$, and because $R < d$, $T = 2R + x_i \le 2d - 1$. So $T$ holds $d$ at most once, the new bit is $[T \ge d]$, and the invariant carries to the next step. After $n$ steps $X_0 = x$, so $Q$ is the quotient and $R$ the remainder. For 13 ÷ 3 with 4 bits ($x$ = 1101):

| Step | Bit in | $T = 2R + x_i$ | $T \ge 3$? | $R$ after |
|---|---|---|---|---|
| 1 | 1 | 1 | no (0) | 1 |
| 2 | 1 | 3 | yes (1) | 0 |
| 3 | 0 | 0 | no (0) | 0 |
| 4 | 1 | 1 | no (0) | 1 |

The quotient bits read 0100 = 4 and the remainder is 1: 13 = 4 × 3 + 1. Hardware computes $T - d$ every cycle and keeps it only if it is not negative; the name comes from early designs that subtracted first and then added $d$ back ("restored") when the result went negative. This basic divider yields one quotient bit per cycle, 32 cycles for a 32-bit divide. Faster dividers retire 2 or more bits per cycle: *non-restoring* division skips the add-back by letting the remainder go negative, and *SRT* division picks each quotient digit from a redundant set such as {−1, 0, 1} by inspecting only a few leading bits of the remainder, so no full-width comparison sits on the critical path. Problem 14-04.15 traces one division.

**Division by a constant.** A divider produces one or a few quotient bits per cycle, so a 32-bit division takes many cycles, against a few for a multiply (14-06). Compilers therefore replace division by a known constant $d$ with a multiplication by a precomputed "magic number" and a shift. For unsigned 32-bit $x$ and $d = 10$, choose

$$
M = \left\lceil \frac{2^{35}}{10} \right\rceil = \frac{2^{35} + 2}{10} = 3\,435\,973\,837 = \texttt{0xCCCCCCCD} .
$$

The claim is that $\lfloor x/10 \rfloor = \lfloor xM / 2^{35} \rfloor$ for every 32-bit $x$. *Proof.* Write $xM/2^{35} = x/10 + 2x/(10 \cdot 2^{35})$. The added error term is less than $2 \cdot 2^{32}/(10 \cdot 2^{35}) = 1/40$, because $x < 2^{32}$. Write $x = 10q + r$ with $0 \le r \le 9$: then $x/10 = q + r/10$ with $r/10 \le 0.9$, and adding less than $1/40$ keeps the sum below $q + 1$. So the floor is $q$. ∎

In RV32IM this is `mulhu` (which supplies the division by $2^{32}$) followed by `srli` by 3. Clang emits exactly this sequence for `x / 10` (Example 14-04.3). For some divisors the magic number needs 33 bits, and the compiler adds a correction step (Problem 14-04.7).

### 3.3 How floating-point operations round

**The format, briefly** (08-01 §3.6 has the details). A normal FP32 number is $(-1)^s \times 1.f \times 2^{e - 127}$, with 23 stored fraction bits and an implicit leading 1, so its **precision** is $p = 24$ significant bits. The **unit in the last place**, ulp($x$), is the gap between $x$ and the next representable number of the same binade, $2^{e-127-23}$. For $x \in [1, 2)$ it is $2^{-23}$.

**Correct rounding.** IEEE 754 requires the basic operations (add, subtract, multiply, divide, square root and fused multiply-add) to return the exact mathematical result rounded to a representable number by the current rounding mode. The default mode is **round to nearest, ties to even**: choose the nearer neighbour, and on an exact tie choose the one whose last bit is 0. RISC-V encodes it as RNE and also provides round toward zero (RTZ), down (RDN), up (RUP) and to nearest with ties away from zero (RMM) [2]. In round-to-nearest the relative error of one operation is at most the **unit roundoff** $u = 2^{-p}$, which is $2^{-24} \approx 5.96 \times 10^{-8}$ for FP32.

**Addition, step by step.** To add two positive normal numbers $a \ge b$:

1. **Align.** Shift $b$'s significand right by the exponent difference, so that both share $a$'s exponent. Bits shifted beyond the 24-bit significand are not simply dropped. The first two are kept as the **guard** (G) and **round** (R) bits, and every bit beyond them is ORed into a single **sticky** bit (S).
2. **Add** the significands. If the sum reaches 2, shift right by one and increment the exponent (the bit shifted out joins G, R and S).
3. **Round.** Look at the bits below the last place:
   - below one half (G = 0): round down;
   - above one half (G = 1 and R or S = 1): round up;
   - exactly one half (G = 1, R = S = 0): a tie, so round to make the last bit even.

   If rounding up carries out of the significand, renormalize.

Three extra bits suffice for correct rounding of addition. When the signs agree, the sum can overflow by one bit and is normalized by a right shift, so G alone (with S) would do. When the signs differ (effective subtraction), the result can lose its leading bit and is normalized by a one-bit left shift: G moves up into the last kept place and R becomes the new guard bit. Larger cancellations happen only when the exponents differ by at most one, and then the shifted-out bits are exact. S records whether anything at all lies further down. Without the sticky bit, a value just above one half could not be told from an exact tie. Example 14-04.4 works three cases.

**Multiplication** adds exponents and multiplies the 24-bit significands into a 48-bit product, then normalizes and rounds it to 24 bits with the same rule. The 24 × 24 significand array dominates its cost (§3.6).

**Fused multiply-add** (FMA) computes $a \times b + c$ with one rounding instead of two. It is more accurate, is about as fast as a multiply, and is the building block of dot products and matrix multiplication. RISC-V provides it as FMADD.S and its variants [2].

**Special values and flags.**

- **Signed zeros:** $+0 = -0$ compares equal, but $1/(-0) = -\infty$.
- **Infinities** absorb finite values.
- **NaN** ("not a number") results from invalid operations such as $0/0$ or $\infty - \infty$. NaN compares unequal to everything, itself included, so `x != x` is the classic NaN test. RISC-V returns a single **canonical NaN**, 0x7FC00000 in FP32, rather than propagating NaN payloads, which saves hardware [2].
- **Exception flags.** Operations do not trap by default. Instead they set sticky exception flags (invalid, divide by zero, overflow, underflow, inexact) that software can inspect, held in RISC-V's `fflags` register [2].

### 3.4 Error in sums

Rounding after every operation has three consequences that matter in practice.

**Addition is not associative.** $(a + b) + c$ and $a + (b + c)$ round differently. In FP32, $(10^8 + 1) - 10^8 = 0$, because the spacing of FP32 numbers near $10^8$ is 8 and $10^8 + 1$ rounds back to $10^8$, whereas $(10^8 - 10^8) + 1 = 1$. Any change in the order of a reduction (a different number of threads, a compiler reordering, a library update) can change the last bits of a result. Bitwise-reproducible results therefore need a fixed order.

**Cancellation magnifies earlier errors.** Subtracting nearly equal numbers is itself exact (Sterbenz's lemma, for operands within a factor of two of each other), but it removes the leading digits the operands shared and exposes the rounding errors they already carried. The relative error of the difference can be huge.

**Errors accumulate in long sums.** Summing $n$ numbers one after another, $s_{k} = \mathrm{fl}(s_{k-1} + x_k)$, commits $n - 1$ roundings, each of relative size at most $u$ but applied to an ever-larger partial sum. The standard bound is

$$
\lvert \hat{s} - s \rvert \le (n - 1)\,u \sum_{k} \lvert x_k \rvert + O(u^2) .
$$

Two classic remedies reduce the growth.

- **Pairwise summation** adds numbers in a balanced binary tree: pairs, then pairs of pairs. Each value passes through only $\lceil \log_2 n \rceil$ additions, so the factor $n - 1$ becomes $\lceil \log_2 n \rceil$. It costs nothing extra and parallelizes naturally, which is why GPU and accelerator reductions are tree-shaped.
- **Compensated (Kahan) summation** carries a second variable that captures the rounding error of each addition and feeds it back into the next:

  ```text
  y = x_k - c;   t = s + y;   c = (t - s) - y;   s = t
  ```

  Its error bound is about $2u \sum \lvert x_k \rvert$, *independent of n*, at four operations per element instead of one. (Aggressive compiler flags that allow reassociation, such as `-ffast-math`, can simplify $c$ to zero and silently disable it.)

Example 14-04.5 shows all three methods on a million additions, and Figure 1 follows them as $n$ grows.

![Log-log plot of the magnitude of the relative error against the number of terms, from 10 to one million, for summing the FP32 value of 0.1 in FP32. The sequential error climbs roughly in proportion to n, from about 1e-7 to about 1e-2, staying under the dotted (n-1)u bound; pairwise and Kahan errors stay between about 1e-10 and 1.4e-7 without growing.](../../../assets/figures/14-04/summation.svg)

*Figure 1. Relative error of summing $n$ copies of the FP32 value nearest 0.1, every addition in FP32. The sequential error grows roughly in proportion to $n$, with dips where its per-binade biases cancel. Pairwise and compensated (Kahan) summation stay near the precision of a single rounding at every $n$.*

> **Going deeper — why the sequential sum drifts.** Once the partial sum $s$ has grown large, its ulp is coarse, and each added 0.1 is rounded to a whole number of those ulps. In the binade $[2^{16}, 2^{17})$ the ulp is $2^{-7}$, and $0.1/2^{-7} = 12.8$ rounds to 13, so every addition there adds $13 \times 2^{-7} = 0.1015625$ instead of 0.1, a systematic 1.56% excess. The error is not random noise that averages out; it is a bias set by the binade.

**Accumulators in AI hardware.** A dot product of length $K$ accumulates $K$ products. With bfloat16 inputs ($u = 2^{-8}$) and a bfloat16 accumulator, the bound $(K - 1)u$ would exceed 100% for $K$ in the hundreds. Hardware therefore multiplies in a narrow format and **accumulates in a wider one**. Google documents that TPUs multiply in bfloat16 and accumulate in FP32 [3], and the OCP MX specification leaves the dot product's internal precision implementation-defined [4]. How wide an accelerator's accumulator really is, and how often it is flushed to FP32, is a question worth asking (§9).

### 3.5 Narrow formats: scales, blocks and integers

**Why a scale factor.** Narrow formats have little range: FP8 E4M3 spans only 18 binades, FP4 E2M1 only the magnitudes 0.5 to 6 (08-01 §3.6). A tensor's values must be scaled into that range before conversion and scaled back afterwards. Choosing one scale per tensor is cheapest, but a few outliers then force everything else into the coarse low end. Smaller scaling groups track the local range better, at the cost of storing more scales.

**Block scaling (the MX formats).** The OCP Microscaling specification [4] gives every block of $k$ = 32 elements one shared scale $X$, an 8-bit power of two (E8M0 in v1.0, renamed UE8M0 in v1.1), and stores each element in a narrow format (FP8, FP6, FP4 or INT8). Its conversion rule is:

1. Set $X$ to the largest power of two not exceeding $\max_i \lvert V_i \rvert$, divided by the largest power of two representable in the element format.
2. Quantize each $V_i / X$ to the element format, rounding ties to even and clamping values beyond the largest normal to it.

For FP4 (E2M1) the largest power of two is 4, so the block maximum lands in $[4, 8)$ after scaling. Values above 6, the largest E2M1 number, are clamped, an error the rule accepts in exchange for simplicity (Problem 14-04.12). A block costs $8 + 32 \times 4 = 136$ bits, or 4.25 bits per element.

**Integer quantization.** INT8 inference stores real values $x$ as integers $q$ with a scale $s$ (and sometimes a zero point $z$), $x \approx s(q - z)$.

- **Symmetric** quantization (with $z = 0$) suits weights centred on zero. It uses $s = \max\lvert x \rvert / 127$ and $q = \mathrm{round}(x/s)$, clamped to $[-127, 127]$, which leaves −128 unused to keep the range symmetric.
- **Affine** quantization (with $z \ne 0$) suits one-sided data, such as the outputs of ReLU.

In either case the rounding error of an unclamped value is at most $s/2$.

**Integer matrix multiplication.** Products of two INT8 values fit in 16 bits, and they are summed in a 32-bit accumulator. With symmetric operands each product has magnitude at most $127^2 = 16\,129$, so the accumulator cannot overflow for any input as long as

$$
K \le \left\lfloor \frac{2^{31} - 1}{127^2} \right\rfloor = 133\,144
$$

terms. That is ample for typical layer widths. At the end the 32-bit sum is multiplied by $s_a s_w / s_{out}$, usually as a fixed-point multiply and shift, and rounded back to INT8 (**requantization**).

### 3.6 What precision costs

An array multiplier's size grows with the square of its significand width (08-09 §3.5). Counting significand bits including the hidden 1, a first-order area model is $p^2$:

| Format | $p$ | $p^2$ | Relative to FP32 |
|---|---|---|---|
| FP32 | 24 | 576 | 1 |
| FP16 | 11 | 121 | 0.21 |
| bfloat16 | 8 | 64 | 0.11 |
| FP8 E4M3 | 4 | 16 | 0.028 |

The model says a bfloat16 multiplier is about half the size of an FP16 one (64/121) and about a ninth of an FP32 one. Google's description of its bfloat16 hardware gives "about half the size in silicon of a typical FP16 multiplier" and "eight times smaller than an FP32 multiplier" [3], in line with the model (which ignores the exponent logic and the alignment and normalization shifters). Energy follows the same trend (08-09 §3.9: a 32-bit floating-point multiply costs 3.7 pJ at 45 nm, a 16-bit one 1.1 pJ [5]). Narrow formats also halve or quarter the bytes moved per value, which often matters more than the arithmetic (14-09, 14-14).

## 4. Worked examples

### Example 14-04.1 · Wraparound, comparison and overflow (tier A)

**Setup.** In RV32I: (a) what does `add` give for 0x7FFFFFFF + 1, and how do SLT and SLTU compare the result with 0? (b) Does 0x7FFFFFFF + 1 overflow as signed numbers, by the sign rule of §3.1? (c) Compare 0xFFFFFFFF with 1 using SLT and SLTU.

**Solution.** (a) The sum is **0x80000000**. As a signed number it is $-2^{31}$, so `slt` (result < 0) gives **1**; as an unsigned number it is $2^{31}$, so `sltu` (result < 0) gives 0, as nothing is below zero unsigned. (b) Both operands are non-negative and the result is negative, so it overflows: $(a \oplus s) \wedge (b \oplus s)$ = 0xFFFFFFFF ∧ 0x80000001 = 0x80000001, whose sign bit is **1**. (c) As signed numbers, $-1 < 1$, so `slt` gives **1**. As unsigned numbers, $4\,294\,967\,295 > 1$, so `sltu` gives **0**.

**Units check.** Results of comparisons are 0 or 1.

**Sanity check.** The adder produced the same bits in every case; only the instructions that interpret them differ.

### Example 14-04.2 · Multiply high and the corners of division (tier B)

**Setup.** For $a = -3$ and $b = 5$, give MUL, MULH and MULHU. Then give DIV and REM for $7 \div 0$, $-2^{31} \div -1$ and $-7 \div 2$.

**Solution.** The low 32 bits of the product are the same for any interpretation: $-15$, or **0xFFFFFFF1**. As signed numbers the full product is $-15$, whose 64-bit form has high word **0xFFFFFFFF**. As unsigned numbers $a$ is $2^{32} - 3$, and $(2^{32} - 3) \times 5 = 4 \times 2^{32} + (2^{32} - 15)$, so MULHU gives **4**.

Division:

- $7 \div 0$: the quotient is all ones, **−1**, and the remainder is the dividend, 7.
- $-2^{31} \div -1$: the quotient is the dividend, **−2147483648**, and the remainder is 0.
- $-7 \div 2$: the quotient rounds toward zero, **−3**, and the remainder is $-7 - 2(-3)$ = **−1**.

The simulator in the verify script executes all of these and agrees.

**Units check.** All values are 32-bit integers.

**Sanity check.** MULH's all-ones high word is just the sign extension of a small negative product.

### Example 14-04.3 · Dividing by 10 without dividing (tier B)

**Setup.** Verify that $q = \lfloor x \cdot \texttt{0xCCCCCCCD} / 2^{35} \rfloor$ equals $\lfloor x / 10 \rfloor$, write the RV32IM sequence, and check what clang emits for `x / 10` on an unsigned `x`.

**Solution.** §3.2's proof covers every $x < 2^{32}$. The largest error term is $2x/(10 \cdot 2^{35}) < 0.025$, and the fractional part $r/10$ is at most 0.9, so the sum never reaches the next integer. In assembly the sequence is:

```text
lui   a1, 0xCCCCD       # a1 = 0xCCCCD000
addi  a1, a1, -819      # a1 = 0xCCCCCCCD (the LUI part rounded up: -819 = 0xCCD - 0x1000)
mulhu a0, a0, a1        # a0 = (x * M) >> 32
srli  a0, a0, 3         # a0 = (x * M) >> 35
```

That is **4** instructions; the first two only build the constant and are hoisted out of loops. Clang 18 at `-O2` for RV32IM produces this sequence with the same magic number, **0xCCCCCCCD**, and a final shift of **3** (35 bits in all). The verify script compiles it and also checks the identity on 10 million random inputs plus the edge values.

**Units check.** The total shift, 32 from MULHU plus 3, is 35, matching $2^{35}$ in $M$.

**Sanity check.** $M/2^{35} = 0.100000000005821$, just above 0.1. A multiplier slightly *above* $1/10$ cannot make the floor fall short, and the proof shows it never overshoots the next integer.

### Example 14-04.4 · Three FP32 additions and ties to even (tier B)

**Setup.** In FP32 with round to nearest even, compute (a) $1 + 2^{-24}$, (b) $1 + 1.5 \times 2^{-24}$, and (c) $(1 + 2^{-23}) + 2^{-24}$. Give each result's bit pattern.

**Solution.** Near 1, the last place of FP32 is worth $2^{-23}$, so $2^{-24}$ is exactly half an ulp. After alignment, the added value lies in the G, R and S bits.

- **(a)** $2^{-24}$ gives G = 1, R = 0, S = 0: an exact tie. The candidates are 1 (last bit 0) and $1 + 2^{-23}$ (last bit 1). Ties go to even, so the result is 1, **0x3F800000**.
- **(b)** $1.5 \times 2^{-24}$ gives G = 1, R = 1: more than half an ulp, so it rounds up to $1 + 2^{-23}$, **0x3F800001**.
- **(c)** $1 + 2^{-23}$ has last bit 1. Adding half an ulp is again a tie, and now the even neighbour is *above*: $1 + 2^{-22}$, **0x3F800002**.

**Units check.** Patterns are FP32 encodings: 0x3F800000 is 1.0, and each increment adds one ulp.

**Sanity check.** The same tie rounded down in (a) and up in (c). Over many ties the two directions balance, which is the point of the rule.

### Example 14-04.5 · Summing 0.1 a million times (tier B)

**Setup.** Add the FP32 value nearest 0.1 to itself $10^6$ times in FP32, in three ways: one after another; pairwise (recursively split the list in halves and add the two half-sums); and with Kahan summation. Compare with the exact sum of the stored values, $10^6 \times 0.100000001490116\ldots = 100\,000.00149$.

**Solution.** The verify script runs all three in FP32 arithmetic:

| Method | FP32 result | Relative error |
|---|---|---|
| Sequential | **100958.34** | **+0.958**% |
| Pairwise | **99999.99** | about $-9.3 \times 10^{-8}$ |
| Kahan | **100000.0** | about $-1.5 \times 10^{-8}$ |

The sequential sum is wrong in its third significant digit. Its error, about 0.96%, is well inside the bound $(n - 1)u \approx 6\%$ but very far from negligible, and it is a bias from the coarse ulps of the large partial sums ("Going deeper" in §3.4). Kahan summation returns 100000.0, the FP32 number nearest the exact sum (the ulp at $10^5$ is $2^{-7} = 0.0078$), so its error is just the final rounding. Pairwise summation returns 99999.99, one ulp lower: about a hundred thousand times more accurate than the sequential sum, at no extra cost.

**Units check.** Relative errors are dimensionless.

**Sanity check.** Pairwise summation sends each value through only 20 additions ($\log_2 10^6 \approx 20$) instead of up to a million; Kahan carries the lost low-order bits forward. Both cost little next to a wrong third digit.

### Example 14-04.6 · Quantizing to INT8 and to a block-scaled FP4 (tier C)

**Setup.** (a) Quantize $w$ = (0.43, −1.31, 0.027, 0.88, −0.555, 1.12, −0.094, 0.705) to symmetric INT8: find the scale, the codes, the largest error and the signal-to-quantization-noise ratio (SQNR). (b) How many INT8 × INT8 products can an INT32 accumulator sum without any risk of overflow? (c) Quantize $v$ = (0.9, −2.7, 0.15, 5.3, −1.2, 0.04, 3.9, −0.6) as one block in MX style with FP4 E2M1 elements (whose magnitudes are 0, 0.5, 1, 1.5, 2, 3, 4 and 6). Use a block of 8 for illustration; the specification uses 32. Find the scale, the elements and the largest error.

**Solution.** (a) $s = 1.31/127$ = **0.010315**. Then $q = \mathrm{round}(w/s)$ = (42, −127, 3, 85, −54, **109**, −9, 68). Dequantizing, $sq$ differs from $w$ by at most **0.004331**, within the bound $s/2 = 0.005157$. The SQNR, $20\log_{10}$ of the ratio of the signal's RMS to the error's RMS, is **48.1** dB, about what 8 bits give (08-09 §3.8's 6 dB per bit).

(b) $\lfloor (2^{31} - 1)/127^2 \rfloor$ = **133144** products.

(c) $\max \lvert v \rvert = 5.3$. The largest power of two not above it is 4, and the largest power of two in E2M1 is 4, so $X = 4/4$ = **1**. Rounding each $v_i/X$ to the E2M1 grid gives (1, −3, 0, **6**, −1, 0, 4, −0.5). The largest error is at 5.3 → 6: **0.7**, or 13% of that value. The small values 0.15 and 0.04 become 0.

**Units check.** Codes and E2M1 elements are dimensionless; the scale carries the units of $w$ or $v$.

**Sanity check.** FP4 is far coarser than INT8: a 4-bit element has 15 values against 255. MX formats rely on many such blocks, wide accumulation and training that adapts to the grid, not on each value being accurate.

### Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 14-04.1a | 0x7FFFFFFF + 1 | 0x80000000 | — |
| Ex 14-04.1b | slt (result < 0) | 1 | — |
| Ex 14-04.1c | signed-overflow sign bit | 1 | — |
| Ex 14-04.1d | slt (0xFFFFFFFF < 1) | 1 | — |
| Ex 14-04.1e | sltu (0xFFFFFFFF < 1) | 0 | — |
| Ex 14-04.2a | MUL (−3 × 5) | 0xFFFFFFF1 | — |
| Ex 14-04.2b | MULH | 0xFFFFFFFF | — |
| Ex 14-04.2c | MULHU | 4 | — |
| Ex 14-04.2d | DIV 7 ÷ 0 | −1 | — |
| Ex 14-04.2e | DIV −2³¹ ÷ −1 | −2147483648 | — |
| Ex 14-04.2f | DIV −7 ÷ 2 | −3 | — |
| Ex 14-04.2g | REM −7 ÷ 2 | −1 | — |
| Ex 14-04.3a | instructions in the sequence | 4 | — |
| Ex 14-04.3b | magic number | 0xCCCCCCCD | — |
| Ex 14-04.3c | final shift | 3 | bits |
| Ex 14-04.3d | M/2³⁵ | 0.100000000005821 | — |
| Ex 14-04.4a | 1 + 2⁻²⁴ | 0x3F800000 | — |
| Ex 14-04.4b | 1 + 1.5 × 2⁻²⁴ | 0x3F800001 | — |
| Ex 14-04.4c | (1 + 2⁻²³) + 2⁻²⁴ | 0x3F800002 | — |
| Ex 14-04.5a | sequential sum | 100958.34 | — |
| Ex 14-04.5b | sequential relative error | 0.958 | % |
| Ex 14-04.5c | pairwise sum | 99999.99 | — |
| Ex 14-04.5d | Kahan sum | 100000.0 | — |
| Ex 14-04.5e | pairwise relative error | -9.3e-8 | — |
| Ex 14-04.5f | Kahan relative error | -1.5e-8 | — |
| Ex 14-04.5g | bound (n − 1)u | 6 | % |
| Ex 14-04.5h | sequential error, rounded | 0.96 | % |
| Ex 14-04.5i | ulp at 10⁵ | 0.0078 | — |
| Ex 14-04.5j | exact sum of the stored values | 100000.00149 | — |
| Ex 14-04.6a | INT8 scale | 0.010315 | — |
| Ex 14-04.6b | code for 1.12 | 109 | — |
| Ex 14-04.6c | largest INT8 error | 0.004331 | — |
| Ex 14-04.6d | SQNR | 48.1 | dB |
| Ex 14-04.6e | safe INT32 accumulation length | 133144 | products |
| Ex 14-04.6f | MX block scale | 1 | — |
| Txt 14-04.a | restoring division 13 ÷ 3: quotient | 4 | — |
| Txt 14-04.b | restoring division 13 ÷ 3: remainder | 1 | — |
| Txt 14-04.c | 0.1 in ulps of 2⁻⁷ | 12.8 | — |
| Txt 14-04.d | each added 0.1 becomes | 0.1015625 | — |
| Txt 14-04.e | systematic excess | 1.56 | % |
| Ex 14-04.6g | element for 5.3 | 6 | — |
| Ex 14-04.6h | largest FP4 error | 0.7 | — |
| Ex 14-04.6i | INT8 error bound s/2 | 0.005157 | — |
| Ex 14-04.6j | FP4 error as a share of 5.3 | 13 | % |

## 5. Simulate it

The lab, [labs/14-04-lab](../labs/14-04-lab/README.md), is a notebook with four parts:

1. **Integers.** Run the multiply, divide and overflow cases on the course's RV32IM simulator, and search for the magic numbers of other divisors.
2. **Rounding by hand.** Implement FP32 addition in integer arithmetic (align, guard, round and sticky bits, ties to even) and check it against the hardware on 100,000 random pairs.
3. **Summation.** Plot the relative error of sequential, pairwise and Kahan summation against $n$, up to $10^6$ terms.
4. **Quantization.** Quantize Gaussian data to INT8, INT4 and MX FP4 and plot SQNR against bits per element.

**Guided exercise (predict, then run).** **Before Part 3,** predict how the sequential error grows with $n$ (like $n$? $\sqrt{n}$?) and whether pairwise or Kahan is more accurate at $n = 10^6$. (The sequential error grows roughly in proportion to $n$ for this one-signed sum because it is a bias, not noise. Pairwise stays around $10^{-7}$ or below and Kahan around $10^{-8}$; neither grows with $n$, and Kahan's error is just the final rounding.)

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Trap or wrap on integer overflow | Safety (trap); simple, fast hardware (wrap) | Exception logic (trap); silent bugs (wrap) | ISA architect, language designer |
| Hardware divider against multiply-by-reciprocal | Simple code for any divisor | Divider area and latency; magic numbers only for constants | CPU team, compiler team |
| Fused multiply-add | One rounding, higher throughput per op | A three-input datapath; results differ from separate mul + add | ISA architect |
| Narrower element format | Area (about $p^2$), energy, bytes moved | Accuracy; needs scaling and calibration | Accelerator architect, ML team |
| Smaller scaling block | Tracks local range, lower error | More scale storage and logic: an 8-bit scale per 32 FP4 elements costs 4.25 bits per element, per 16 elements 4.5 | Format designers |
| Wider accumulator | Accuracy of long dot products | Area and power in every MAC unit | Accelerator architect |
| Sequential, pairwise or compensated sums | Speed (sequential) or accuracy (pairwise, Kahan) | Accuracy (sequential) or extra operations (Kahan) | Library author |

## 7. Numbers to know

| Quantity | Value | Note |
|---|---|---|
| FP32 precision and unit roundoff | $p = 24$, $u = 2^{-24} \approx 5.96 \times 10^{-8}$ | §3.3 |
| Spacing of FP32 near $10^8$ | 8 | so $10^8 + 1 = 10^8$ |
| Sequential-sum error bound | $(n - 1)u\sum\lvert x \rvert$ | pairwise: $\lceil\log_2 n\rceil u$; Kahan: about $2u$ |
| RISC-V division by zero | quotient −1, remainder = dividend | no trap [1] |
| RISC-V canonical FP32 NaN | 0x7FC00000 | [2] |
| Magic number for unsigned ÷ 10 | 0xCCCCCCCD, then shift by 35 | Example 14-04.3 |
| INT8 × INT8 products before INT32 overflow | 133,144 | symmetric operands |
| MX block | 32 elements + one 8-bit power-of-two scale | 4.25 bits per FP4 element [4] |

## 8. Common mistakes

- **Comparing unsigned values with signed instructions** (or the reverse). 0xFFFFFFFF is less than 1 to SLT and greater to SLTU.
- **Relying on signed overflow in C.** It is undefined, and compilers optimize on the assumption that it never happens.
- **Expecting division by zero to trap.** On RISC-V it returns −1 quietly.
- **Testing floats for exact equality** after arithmetic. Compare with a tolerance scaled to the values' magnitude, or count ulps.
- **Assuming a different summation order gives the same answer.** Parallel and vectorized reductions change the order and the last bits.
- **Accumulating in the input format.** Summing thousands of bfloat16 or FP8 products in the same format loses most of the answer; accumulate wider.
- **Quoting a format without its scaling scheme.** "FP4" without the block size and scale type does not determine accuracy.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **IEEE 754-2019** is the active floating-point standard, superseding 754-2008; a revision project, P754, is open [6, R-210] **[Established]**.
- **bfloat16.** Google describes it as one sign, eight exponent and seven mantissa bits, with FP32's dynamic range. Its Cloud TPU documentation says TPUs multiply in bfloat16 and accumulate in FP32, and that converting FP32 to bfloat16 flushes subnormals to zero [3, R-210] **[Established]**. RISC-V has ratified BF16 extensions, noting that bfloat16 "is not an IEEE-754 standard format" but a valid format under IEEE 754's rules [R-210] **[Established]**.
- **MX formats.** OCP MX v1.0 (Sep 2023) defines MXFP8, MXFP6, MXFP4 and MXINT8 with 32-element blocks and E8M0 scales. It specifies the conversion rule of §3.5 (power-of-two scale, ties-to-even rounding, clamping) and leaves the dot product's internal precision implementation-defined [4, R-210] **[Established]**. Version 1.1 (9 Oct 2026) keeps the formats and block size. It renames the scale type UE8M0, clarifies NaN and out-of-range cases, and lets the conversion raise the scale by one extra power of two (an optional, implementation-defined adjustment). §3.5's rule is the default case [4, R-143] **[Established]**. NVIDIA's NVFP4 uses 16-element blocks with FP8 scales (08-01, [R-143](../../../reference/research-log.md#r-143--block-scaled-ai-number-formats)).

### Why it matters commercially

- **Formats are a competitive weapon.** Vendors quote peak throughput in their narrowest format. NVIDIA's H100 SXM, for example, lists 1,979 TFLOPS for FP16 and 3,958 for FP8 (both with sparsity): one halving of the width, twice the peak (14-14, [R-220](../../../reference/research-log.md#r-220--nvidia-h100-hopper-specifications)) **[Established]**. The $p^2$ model of §3.6 would allow about four times as many FP8 multipliers in the area of the 16-bit ones. Operand bandwidth, register files, accumulators and exponent logic do not shrink as fast as the multipliers, so the delivered gain per halving is closer to 2× (Problem 14-04.16). Comparing chips' "TOPS" requires the same format and the same scaling scheme.
- **Numerical behaviour is part of compatibility.** Customers porting models between accelerators see different results when rounding, accumulator width or summation order differ. Reproducibility guarantees, or their absence, matter in regulated domains.
- **Quantization tooling is a moat.** Getting a model to INT8 or FP4 with negligible accuracy loss needs calibration software, and vendors with mature tools win designs.

### Marketing vs Reality

- **"FP4 with no accuracy loss."** *Reality:* accuracy depends on the model, the scaling scheme, which layers stay in higher precision, and whether the model was trained or fine-tuned for the format. *Sanity check:* ask for accuracy on the customer's model, against an FP16 or BF16 baseline, with the full quantization recipe.
- **"2× the TOPS of the competitor."** *Reality:* often FP4 or sparse figures against FP8 or dense ones. *Sanity check:* normalize to the same format, density and block scaling.
- **"Bit-exact with the GPU."** *Reality:* only if the accumulation order, accumulator width and rounding match. *Sanity check:* ask how reductions are ordered and whether results are deterministic across runs.

### Questions for engineering leaders

1. **"How wide is your accumulator, and how often do you flush to FP32?"**
   *Strong:* the exact width and flush interval, and measured error against an FP32 reference. *Evasive:* "high precision".
2. **"Which scaling scheme do you support: per tensor, per channel, per block, and which block size?"**
   *Strong:* a list tied to the OCP MX specification and other formats, with accuracy data. *Evasive:* "full FP4 support".
3. **"Are your results deterministic run to run?"**
   *Strong:* yes in a defined mode, with its performance cost. *Evasive:* "within tolerance".
4. **"What happens on overflow and NaN in your low-precision paths?"**
   *Strong:* saturation or NaN behaviour per format, documented. *Evasive:* "it doesn't happen in practice".
5. **"How much accuracy do customers lose going from BF16 to FP8, and how much engineering does it take?"**
   *Strong:* measured numbers on named models, and the tooling that achieves them. *Evasive:* "negligible".

## 10. Concept check

**Q1.** Why can the same ADD instruction serve signed and unsigned integers, but SLT and SLTU must differ?

<details><summary>Answer</summary>

Two's complement makes addition modulo $2^{32}$ produce the same bits whatever the interpretation. Ordering, however, depends on the interpretation: 0xFFFFFFFF is the largest unsigned value but −1 signed.

</details>

**Q2.** What does RISC-V return for an integer division by zero, and why not trap?

<details><summary>Answer</summary>

The quotient has all bits set (−1) and the remainder equals the dividend. Defining a result keeps the divider out of the exception machinery. Software that cares adds one branch, and the C language leaves the case undefined anyway.

</details>

**Q3.** Why does rounding need a sticky bit as well as guard and round bits?

<details><summary>Answer</summary>

To distinguish an exact tie (exactly half an ulp, rounded to even) from a value slightly above half (rounded up). The sticky bit records whether any nonzero bit was shifted out beyond the round bit.

</details>

**Q4.** Why is $(10^8 + 1) - 10^8 = 0$ in FP32?

<details><summary>Answer</summary>

Near $10^8$, FP32 numbers are 8 apart, so $10^8 + 1$ rounds back to $10^8$ before the subtraction.

</details>

**Q5.** Why is pairwise summation more accurate than sequential summation, and why does it suit parallel hardware?

<details><summary>Answer</summary>

Each value passes through only about $\log_2 n$ roundings instead of up to $n$, and the tree's independent pairs can be added simultaneously, which is how GPU and accelerator reductions work.

</details>

**Q6.** Why do accelerators multiply in a narrow format but accumulate in a wide one?

<details><summary>Answer</summary>

Products individually tolerate low precision, but a sum of thousands of them accumulates rounding error in proportion to the number of terms times the accumulator's unit roundoff. A wide accumulator keeps that error small at modest cost. Every MAC unit has one (in a systolic array, one per processing element), but an adder grows only linearly with its width, while the multiplier beside it grows with the square of its input width.

</details>

**Q7.** In an MX block with FP4 elements, why can the largest value be clamped?

<details><summary>Answer</summary>

The scale is a power of two chosen so that the block maximum, after scaling, lies between 4 and 8. E2M1's largest value is 6, so a scaled maximum in $(6, 8)$ is clamped to 6. A non-power-of-two scale would avoid that, at more cost.

</details>

Now work the [problem set](../problems/14-04-problems.md).

## 11. Key terms

[Wraparound](../../../reference/glossary.md#wraparound) · [Multiply-high](../../../reference/glossary.md#multiply-high) · [Unit in the last place (ulp)](../../../reference/glossary.md#unit-in-the-last-place-ulp) · [Round to nearest, ties to even](../../../reference/glossary.md#round-to-nearest-ties-to-even) · [Guard, round and sticky bits](../../../reference/glossary.md#guard-round-and-sticky-bits) · [Fused multiply-add (FMA)](../../../reference/glossary.md#fused-multiply-add-fma) · [Unit roundoff](../../../reference/glossary.md#unit-roundoff) · [Catastrophic cancellation](../../../reference/glossary.md#catastrophic-cancellation) · [Pairwise summation](../../../reference/glossary.md#pairwise-summation) · [Kahan summation](../../../reference/glossary.md#kahan-summation) · [Quantization (neural networks)](../../../reference/glossary.md#quantization-neural-networks) · [Block floating point](../../../reference/glossary.md#block-floating-point) · [Requantization](../../../reference/glossary.md#requantization)

## 12. Connections

- **Builds on:** formats and two's complement ([08-01](../../08-digital-logic-design/chapters/08-01-number-systems-and-codes.md)); adders, multipliers and arithmetic energy ([08-09](../../08-digital-logic-design/chapters/08-09-arithmetic-circuits.md)); assembly and compilers ([14-03](14-03-assembly-and-the-compilation-stack.md)); numerical methods ([02-10](../../02-complex-numbers-des-and-linear-algebra/chapters/02-10-numerical-methods.md)).
- **Next:** [14-05 Single-Cycle Datapath and Control](14-05-single-cycle-datapath.md), the hardware that executes these instructions.
- **Used later:** multi-cycle dividers and their stalls ([14-06](14-06-pipelining-and-hazards.md)); vector and tensor arithmetic on GPUs and accelerators ([14-13](14-13-gpus-and-simt.md), [14-14](14-14-ai-accelerators.md)); benchmark precision rules ([14-15](14-15-roofline-and-benchmarks.md)).

## 13. Further study

- D. A. Patterson and J. L. Hennessy, *Computer Organization and Design*, RISC-V Edition, ch. 3 (arithmetic for computers).
- D. Goldberg, "What every computer scientist should know about floating-point arithmetic," *ACM Computing Surveys* 23(1), 1991.
- N. J. Higham, *Accuracy and Stability of Numerical Algorithms*, 2nd ed., SIAM, 2002, ch. 2–4 (rounding error, summation).
- H. S. Warren, *Hacker's Delight*, 2nd ed., ch. 10 (division by constants).
- The OCP MX and OFP8 specifications ([4] and 08-01's sources), and the RISC-V M and F chapters ([1], [2]).

## 14. Sources

1. RISC-V International, *The RISC-V Instruction Set Manual, Volume I*, version 20260120, chapter "M" Extension for Integer Multiplication and Division (multiply-high variants, fused MULH/MUL sequence, division rounding, division-by-zero and overflow semantics). [R-201](../../../reference/research-log.md#r-201--risc-v-unprivileged-isa-manual-version-20260120)
2. Same manual, chapter "F" Extension for Single-Precision Floating-Point (rounding-mode encodings, `fcsr`/`fflags`, canonical NaN 0x7FC00000, FMADD). [R-201](../../../reference/research-log.md#r-201--risc-v-unprivileged-isa-manual-version-20260120)
3. S. Wang and P. Kanwar, "BFloat16: The secret to high performance on Cloud TPUs," Google Cloud Blog, 23 Aug 2019; Google Cloud TPU documentation, "Improve your model's performance with bfloat16" (updated Nov 2026). [R-210](../../../reference/research-log.md#r-210--number-formats-ieee-754-2019-bfloat16-and-ocp-mx-primary-re-check)
4. Open Compute Project, *OCP Microscaling Formats (MX) Specification*, Version 1.0, Sep 2023, §§5–6 (element formats, dot product, conversion from scalar vectors); Version 1.1, 9 Oct 2026, version history and §6.3 ([R-143](../../../reference/research-log.md#r-143--block-scaled-ai-number-formats)). [R-210](../../../reference/research-log.md#r-210--number-formats-ieee-754-2019-bfloat16-and-ocp-mx-primary-re-check)
5. M. Horowitz, "Computing's energy problem (and what we can do about it)," ISSCC 2014, Figure 1.1.9. [R-157](../../../reference/research-log.md#r-157--arithmetic-energy-and-dsp-blocks)
6. IEEE SA, "IEEE 754-2019 — IEEE Standard for Floating-Point Arithmetic" (standard page, read Nov 2026). [R-210](../../../reference/research-log.md#r-210--number-formats-ieee-754-2019-bfloat16-and-ocp-mx-primary-re-check)

Every integer result in this chapter is executed on the course's RV32IM simulator, every floating-point result is computed in FP32 arithmetic and checked against exact rational arithmetic, and the division-by-constant sequence is compiled with clang, by the verify script.
