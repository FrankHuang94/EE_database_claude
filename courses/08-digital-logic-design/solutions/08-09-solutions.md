# Solutions 08-09 · Arithmetic Circuits

Problems: [08-09 problems](../problems/08-09-problems.md) · Chapter: [08-09](../chapters/08-09-arithmetic-circuits.md). Every number below is recomputed by [verify_08_09.py](../verify/verify_08_09.py): adders are built as gate networks and timed by arrival-time simulation, multipliers are built as Dadda reductions and checked bit by bit, Booth digits and fixed-point conversions are computed in integer arithmetic, and rounding biases by enumerating every value of the dropped bits.

---

## Solutions

### Solution 08-09.1

(a) $G = A \text{ AND } B$ = 0001 1000 = **24**; $P = A \text{ XOR } B$ = 0110 0111 = **103**.

(b) Carries from bit 0: $C_1 = C_2 = C_3 = 0$ (no generate in bits 0 to 2); $C_4 = G_3 = 1$; $C_5 = G_4 = 1$; $C_6 = P_5C_5 = 1$; $C_7 = P_6C_6 = 1$; $C_8 = G_7 + P_7C_7 = 0$ (bit 7 kills it). The sum is 1001 0111 = **151** with carry out **0**: $92 + 59 = 151$ ✓.

(c) The carry generated at bit 4 rides through bits 5 and 6: **2** bits. (The carry from bit 3 runs into bit 4, which generates its own anyway.)

### Solution 08-09.2

(a) $3 \circ 2 = (0 + 1 \cdot 0,\; 1 \cdot 1) = (0, 1)$ and $1 \circ 0 = (1 + 0 \cdot 0,\; 0) = (1, 0)$; then $(0, 1) \circ (1, 0) = (0 + 1 \cdot 1,\; 0) = (1, 0)$. The other grouping: $1 \circ 0 = (1, 0)$, $2 \circ (1, 0) = (1, 0)$, $3 \circ (1, 0) = (1, 0)$. Both give $G_{3:0}$ = **1**, $P_{3:0}$ = **0**: bit 1 generates a carry, bits 2 and 3 pass it out, and no carry can pass through the whole block because bit 1 does not propagate.

(b) $(0, 0) \circ (1, 0) = (0 + 0 \cdot 1,\; 0) = (0, 0)$: the low block generates a carry but the high block kills it, so $G$ = **0**. $(1, 0) \circ (0, 0) = (1, 0)$: the high block generates by itself, so $G$ = **1**. The operator is not commutative: which block is on top decides whose carry survives.

### Solution 08-09.3

With $n = 32$ and $\log_2 n = 5$:

- Kogge–Stone: $32 \times 5 - 31$ = **129** operators, **5** levels.
- Sklansky: $16 \times 5$ = **80** operators, 5 levels.
- Brent–Kung: $64 - 2 - 5$ = **57** operators, $2 \times 5 - 1$ = **9** levels.

### Solution 08-09.4

(a) $128 \times 15$ = **1.92** ns. (b) $14 \times 15$ = **0.21** ns. (c) $24 \times 15$ = **0.36** ns. (d) $64 \times 6 - 63$ = **321** operators.

In a real 64-bit adder, wire delay and fan-out make the gaps smaller than this model suggests, but the ordering holds: at 15 ps per gate a ripple-carry adder could not even run at 1 GHz.

### Solution 08-09.5

(a) The lowest block's carry-out $C_8$ arrives at $2 \times 8 + 1 = 17$. Each upper block's two candidate results are ready earlier (top sum bit at 14, carry-out at 15, since their carry-in is a constant), so the multiplexers wait only for their select. $C_{16}$ is selected at $17 + 2 = 19$, $C_{24}$ at 21, and the top block's sums and $C_{32}$ at **23** units, against 35 for two 16-bit halves and 64 for ripple carry.

(b) Full adders: $8 + 3 \times 16$ = **56**. Multiplexers: each upper block selects 8 sum bits and its carry-out, $3 \times 9$ = **27**.

### Solution 08-09.6

(a) $C_3 = G_2 + P_2G_1 + P_2P_1G_0 + P_2P_1P_0C_0$: **4** product terms.

(b) $C_8$ has **9** terms, the last with **9** inputs ($P_7 \cdots P_0 C_0$).

(c) The group carries $C_4$, $C_8$, $C_{12}$ and $C_{16}$ (**4** carries), from the groups' $G_{3:0}$, $P_{3:0}$, ..., exactly as the first level computes bit carries from bit signals. The carries inside each group then come from the first-level logic using its group's carry-in.

### Solution 08-09.7

(a) $12 \times 12$ = **144** bits.

(b) Targets below 12: 9, 6, 4, 3, 2: **5** levels (12 → 9 → 6 → 4 → 3 → 2).

(c) $n^2 - 4n + 3 = 144 - 48 + 3$ = **99** full adders, $n - 1$ = **11** half adders, final adder $2n - 2$ = **22** bits.

### Solution 08-09.8

$-99$ in 8 bits is $256 - 99 = 157$ = 1001 1101, so $b_7 \ldots b_0$ = 1, 0, 0, 1, 1, 1, 0, 1.

| $k$ | triplet $(b_{2k+1}, b_{2k}, b_{2k-1})$ | digit |
|---|---|---|
| 0 | 0, 1, 0 | +1 |
| 1 | 1, 1, 0 | −1 |
| 2 | 0, 1, 1 | +2 |
| 3 | 1, 0, 0 | −2 |

Value: $1 - 1 \times 4 + 2 \times 16 - 2 \times 64 = 1 - 4 + 32 - 128$ = **−99** ✓. Product: $7 \times (1 - 4 + 32 - 128) = 7 - 28 + 224 - 896$ = **−693** ✓. All **4** partial products are nonzero (this multiplier has no runs to exploit), still half the 8 rows of the unrecoded multiplier.

### Solution 08-09.9

(a) $\log_2 64$ = **6** stages of 64 multiplexers: **384**. A 64:1 multiplexer is a tree of 63 two-input multiplexers, so 64 of them need $64 \times 63$ = **4032**, more than ten times as many.

(b) $-40$ is 1101 1000. A logical shift brings in zeros: 0001 1011 = **27**. An arithmetic shift copies the sign bit: 1111 1011 = **−5**, which is $\lfloor -40/8 \rfloor = -5$ exactly.

### Solution 08-09.10

(a) Q4.12 has 4 integer bits including the sign and 12 fraction bits, so its range is $[-2^{3},\, 2^{3} - 2^{-12}]$: largest value $8 - 2^{-12}$ = **7.99976**, resolution $2^{-12}$ = **2.44e-4**. (Some vendors' documentation counts integer bits without the sign and would call this format Q3.12; check which convention a document uses.)

(b) $e \times 4096 = 11\,134.08\ldots$, which rounds to **11134**. Its value is $11134/4096 = 2.718262$, an error of **−2.01e-5**, below half the resolution (1.22e-4) as it must be.

### Solution 08-09.11

(a) A signed $m$-bit by signed $n$-bit product needs $m + n$ bits: **28** (the extreme $(-2^{11})(-2^{15}) = 2^{26}$ needs a 28-bit signed result).

(b) $28 + \lceil \log_2 256 \rceil$ = **36** bits.

### Solution 08-09.12

(a) $6.02 \times 12 + 1.76$ = **74.0** dB.

(b) $6.02b + 1.76 \ge 90$ gives $b \ge 14.66$: **15** bits.

(c) $10\log_{10}(1.5 \cdot 2^{48})$ = **146.3** dB ($6.02 \times 24 + 1.76$ gives 146.2 because the coefficients are rounded; the exact ones are 6.0206 and 1.7609), far beyond any analog front end; 24-bit audio formats carry headroom and processing margin, not a real 146 dB.

### Solution 08-09.13

Let the dropped bits be $r$, an integer from 0 to $2^{15} - 1$; one result LSB is $2^{15}$ in these units.

(a) Truncation discards $r$: error $-r/2^{15}$ LSB, whose mean is $-\dfrac{(2^{15} - 1)/2}{2^{15}}$ = **−0.49998** LSB.

(b) Round-half-up adds $2^{14}$ first. For $r < 2^{14}$ the result rounds down, error $-r/2^{15}$; for $r \ge 2^{14}$ it rounds up, error $(2^{15} - r)/2^{15}$. Summing over all $r$:

$$
\sum_{r=0}^{2^{14}-1}(-r) + \sum_{r=2^{14}}^{2^{15}-1}(2^{15} - r) = -\frac{(2^{14} - 1)2^{14}}{2} + \frac{2^{14}(2^{14} + 1)}{2} = 2^{14},
$$

so the mean error is $2^{14}/(2^{15} \cdot 2^{15}) = 2^{-16}$ = **1.53e-5** LSB: the tiny upward bias of rounding exact halves up.

(c) Truncation: $1000 \times (-0.49998)$ = **−500.0** LSB, a drift of 500 LSBs. Rounding: $1000 \times 1.53 \times 10^{-5}$ = **0.0153** LSB, negligible. (Round-half-to-even removes even that.)

### Solution 08-09.14

(a) $27 + 18$ = **45** bits, leaving $48 - 45$ = **3** guard bits: $2^3$ = **8** worst-case products.

(b) $18 + 18$ = **36** bits, **12** guard bits: $2^{12}$ = **4096** products.

The first case shows why full-width 27 × 18 products are usually scaled or accumulated over short sums, and why DSP slices cascade their accumulators.

### Solution 08-09.15

(a) INT8 MAC: $0.2 + 0.1$ = **0.3** pJ; $10^{12}$ of them use **0.3** J. FP32 MAC: $3.7 + 0.9$ = **4.6** pJ, so **4.6** J. Ratio $4.6/0.3$ = **15.3**.

(b) $20/0.3$ = **66.7** MACs per 32 KB cache read.

(c) $0.3/(0.3 + 20)$ = **1.48**%: the arithmetic would be a rounding error in the energy bill. Accelerators exist to make each operand fetched from memory feed many MACs (data reuse), not mainly to make MACs cheaper.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 08-09.1a | G | 24 | — |
| 08-09.1b | P | 103 | — |
| 08-09.1c | sum | 151 | — |
| 08-09.1d | carry out | 0 | — |
| 08-09.1e | longest propagate run | 2 | bit |
| 08-09.2a | $G_{3:0}$ | 1 | — |
| 08-09.2b | $P_{3:0}$ | 0 | — |
| 08-09.2c | G of (0, 0) ∘ (1, 0) | 0 | — |
| 08-09.2d | G of (1, 0) ∘ (0, 0) | 1 | — |
| 08-09.3a | Kogge–Stone operators, 32 bits | 129 | — |
| 08-09.3b | Kogge–Stone levels | 5 | — |
| 08-09.3c | Sklansky operators | 80 | — |
| 08-09.3d | Brent–Kung operators | 57 | — |
| 08-09.3e | Brent–Kung levels | 9 | — |
| 08-09.4a | ripple delay, 64 bits | 1.92 | ns |
| 08-09.4b | Kogge–Stone delay | 0.21 | ns |
| 08-09.4c | Brent–Kung delay | 0.36 | ns |
| 08-09.4d | Kogge–Stone operators, 64 bits | 321 | — |
| 08-09.5a | carry-select delay, 4 × 8 | 23 | unit |
| 08-09.5b | full adders | 56 | — |
| 08-09.5c | multiplexers | 27 | — |
| 08-09.6a | terms in $C_3$ | 4 | — |
| 08-09.6b | terms in a flat $C_8$ | 9 | — |
| 08-09.6c | fan-in of a flat $C_8$ | 9 | — |
| 08-09.6d | second-level carries | 4 | — |
| 08-09.7a | partial-product bits | 144 | — |
| 08-09.7b | levels | 5 | — |
| 08-09.7c | full adders | 99 | — |
| 08-09.7d | half adders | 11 | — |
| 08-09.7e | final adder width | 22 | bit |
| 08-09.8a | value of the digits | -99 | — |
| 08-09.8b | product | -693 | — |
| 08-09.8c | nonzero partial products | 4 | — |
| 08-09.9a | stages | 6 | — |
| 08-09.9b | barrel-shifter multiplexers | 384 | — |
| 08-09.9c | multiplexers for 64 separate 64:1 | 4032 | — |
| 08-09.9d | logical right shift | 27 | — |
| 08-09.9e | arithmetic right shift | -5 | — |
| 08-09.10a | largest value | 7.99976 | — |
| 08-09.10b | resolution | 2.44e-4 | — |
| 08-09.10c | code for e | 11134 | — |
| 08-09.10d | representation error | -2.01e-5 | — |
| 08-09.11a | product width | 28 | bit |
| 08-09.11b | accumulator width | 36 | bit |
| 08-09.12a | SQNR, 12 bits | 74.0 | dB |
| 08-09.12b | bits for 90 dB | 15 | — |
| 08-09.12c | SQNR, 24 bits | 146.3 | dB |
| 08-09.13a | truncation mean error | -0.49998 | LSB |
| 08-09.13b | rounding mean error | 1.53e-5 | LSB |
| 08-09.13c | truncation bias after 1000 | -500.0 | LSB |
| 08-09.13d | rounding bias after 1000 | 0.0153 | LSB |
| 08-09.14a | 27 × 18 product width | 45 | bit |
| 08-09.14b | guard bits | 3 | bit |
| 08-09.14c | worst-case products | 8 | — |
| 08-09.14d | 18 × 18 product width | 36 | bit |
| 08-09.14e | guard bits | 12 | bit |
| 08-09.14f | worst-case products | 4096 | — |
| 08-09.15a | INT8 MAC energy | 0.3 | pJ |
| 08-09.15b | FP32 MAC energy | 4.6 | pJ |
| 08-09.15c | energy ratio | 15.3 | — |
| 08-09.15d | INT8 MACs per cache read | 66.7 | — |
| 08-09.15e | arithmetic share with a cache read per MAC | 1.48 | % |
