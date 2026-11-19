# Course 08 · Final Exam — Solutions

Exam: [README.md](README.md).

All numbers are recomputed by [verify_08_exam.py](../verify/verify_08_exam.py), mostly by brute force: exhaustive truth tables and minimization, bit-level simulation of the adders and machines, and arrival-time simulation of the prefix networks. The Verilog answers are confirmed by a self-checking testbench, [exam_tb.v](exam_tb.v), which runs Question 5's code under Icarus Verilog and tests the reference design of Question 8 ([exam_designs.v](exam_designs.v)) against a behavioral model.

Each solution names the chapter to revisit if you lost points.

**1.** *(08-01)*

(a) B = 1011 and 6 = 0110, so B6₁₆ = **1011 0110₂**. Unsigned: $128 + 32 + 16 + 4 + 2$ = **182**. As 8-bit two's complement the top bit weighs $-128$: $182 - 256$ = **−74**.

(b) 5A₁₆ + 3C₁₆ = 90 + 60 = 150 = **96₁₆**. As a signed 8-bit number, 96₁₆ = $150 - 256$ = **−106**. Two positive operands gave a negative result, so the addition **overflowed**: +150 lies outside the range −128 to +127. The hardware detects this as $V = C_8 \oplus C_7$, the XOR of the carries out of and into the top bit. Here the carry into bit 7 is 1 and the carry out is 0, so $V = 1$.

(c) The scale is $2^{-7}$, so the stored integer is $-0.40625 \times 128 = -52$. In 8 bits, $-52$ is $256 - 52 = 204$ = **1100 1100₂ = CC₁₆**. The resolution is $2^{-7}$ = **0.0078125**, and the range runs from **−1** to $1 - 2^{-7}$ = **0.9921875**.

(d) Each check bit $p$ covers the positions whose index contains $p$:

- $p_1$ covers positions 1, 3, 5 and 7: bits 1, 0, 0, 0, odd parity, so syndrome bit 1 is set;
- $p_2$ covers 2, 3, 6 and 7: bits 1, 0, 1, 0, even, clear;
- $p_4$ covers 4, 5, 6 and 7: bits 0, 0, 1, 0, odd, set.

The syndrome is $1 + 4$ = **5** (101₂): bit 5 is wrong. Flipping it gives **1100110**, and the data bits at positions 3, 5, 6 and 7 are **0110**. Check: re-encoding 0110 gives 1100110.

**2.** *(08-02)*

(a) $BC$ is the **consensus** of $AB$ and $\overline{A}C$: whenever $BC = 1$, either $A = 1$ (and $AB = 1$) or $A = 0$ (and $\overline{A}C = 1$). So $F = AB + \overline{A}C$. For $G$, the **dual distributive law** gives $(A + B)(A + C) = A + BC$. Multiplying out confirms it: $A + AC + AB + BC = A + BC$, by absorption.

(b) $\overline{A + \overline{B}C} = \overline{A}\cdot\overline{\overline{B}C} = \overline{A}(B + \overline{C})$: a product of the sum $(B + \overline{C})$ and the single literal $\overline{A}$.

(c) The three implementations:

- **AND-OR:** each AND2 is a NAND2 plus an inverter, 6 transistors, and so is the OR2. That gives $3 \times 6$ = **18** transistors.
- **NAND-NAND:** by De Morgan, $AB + CD = \overline{\overline{AB}\cdot\overline{CD}}$, so three NAND2 gates at 4 transistors each give **12** transistors.
- **AOI22 plus inverter:** the AOI22 gives $\overline{AB + CD}$ with 8 transistors (a 4-input compound gate), and the inverter adds 2: **10** transistors.

The compound gate is the smallest. Static CMOS gates invert naturally, so the best implementations work with that.

(d) Parity is 1 in rows 1, 2, 4 and 7: $2 + 4 + 16 + 128$ = **150** (96₁₆). Majority is 1 in rows 3, 5, 6 and 7: $8 + 32 + 64 + 128$ = **232** (E8₁₆).

**3.** *(08-03, 08-04 §3.6)*

The K-map (rows $AB$, columns $CD$, both in the order 00, 01, 11, 10):

| $AB$ \ $CD$ | 00 | 01 | 11 | 10 |
|---|---|---|---|---|
| 00 | 0 | 1 | 0 | 0 |
| 01 | 0 | 1 | 1 | 1 |
| 11 | 1 | 1 | 1 | 0 |
| 10 | 0 | 0 | 1 | 0 |

(a) There are **5** prime implicants: $\overline{A}\,\overline{C}D$ (m1, m5), $\overline{A}BC$ (m6, m7), $AB\overline{C}$ (m12, m13), $ACD$ (m11, m15) and the quad $BD$ (m5, m7, m13, m15). The first four are **essential** (**4** of them): m1, m6, m12 and m11 are each covered by only one prime.

(b) The four essential primes cover every minterm, including m5, m7, m13 and m15, so

$$
F = \overline{A}\,\overline{C}D + \overline{A}BC + AB\overline{C} + ACD ,
$$

with **4** terms and **12** literals. The quad $BD$, the largest group on the map, is **redundant**: each of its four cells is already covered by an essential prime. Starting from the largest group is a heuristic, not a rule; the essential primes come first.

(c) The zeros of $F$ are m0, m2, m3, m4, m8, m9, m10 and m14. Minimizing $\overline{F}$ the same way gives four essential primes and no other cover:

$$
\overline{F} = \overline{A}\,\overline{B}C + \overline{A}\,\overline{C}\,\overline{D} + A\overline{B}\,\overline{C} + AC\overline{D} .
$$

De Morgan turns it into the minimal product of sums, again **4** terms and **12** literals:

$$
F = (A + B + \overline{C})(A + C + D)(\overline{A} + B + C)(\overline{A} + \overline{C} + D) .
$$

(d) **Yes.** A static-1 hazard can occur when a single input change moves between two adjacent 1-cells covered by different product terms. Here those pairs are the four cells of the quad $BD$:

- m5 ↔ m7 ($C$ changes, with $A = 0$, $B = D = 1$);
- m5 ↔ m13 ($A$ changes);
- m7 ↔ m15 ($A$ changes);
- m13 ↔ m15 ($C$ changes).

That is **4** transitions. Adding the redundant prime **$BD$** covers all four, giving a hazard-free sum of 5 terms and 14 literals. The term that minimization threw away is exactly the consensus term that hazard removal needs. Whether to add it depends on whether the output feeds something that sees glitches, such as an asynchronous reset or a clock gate. A synchronous design that samples after the logic settles can ignore static hazards.

(e) With m3 and m9 free, $D$ covers m1, m3, m5, m7, m9, m11, m13 and m15 (using both don't cares). Only m6 and m12 remain, covered by $\overline{A}BC$ and $AB\overline{C}$:

$$
F = D + \overline{A}BC + AB\overline{C} ,
$$

with **3** terms and **7** literals instead of 4 and 12.

**4.** *(08-04)*

(a) Group the truth table by $AB$:

| $AB$ | $G$ for $C = 0, 1$ | Data input |
|---|---|---|
| 00 | 0, 1 (m1) | $D_0 = C$ |
| 01 | 1, 0 (m2) | $D_1 = \overline{C}$ |
| 10 | 0, 0 | $D_2 = 0$ |
| 11 | 1, 1 (m6, m7) | $D_3 = 1$ |

(b) A 3:8 decoder raises exactly one output $Y_i$, the minterm $m_i$. So $G = Y_1 + Y_2 + Y_6 + Y_7$, one 4-input OR.

(c) First subtraction:

- $0101 - 0111$: $\overline{B}$ = 1000, and $0101 + 1000 + 1$ = **1110₂**, which is **−2** = 5 − 7.
- The carries: bit 0 gives $1 + 0 + 1$, sum 0, carry 1; bit 1, $0 + 0 + 1$, sum 1, carry 0; bit 2, $1 + 0 + 0$, sum 1, carry 0; bit 3, $0 + 1 + 0$, sum 1, carry 0.
- So $C_4 = 0$ and $C_3 = 0$, giving $V = 0$: the result is correct.
- In subtraction a carry out of 0 means a **borrow**: as unsigned numbers, 5 < 7.

Second subtraction:

- $0110 - 1101$, that is $6 - (-3)$: $\overline{B}$ = 0010, and $0110 + 0010 + 1$ = **1001₂**, which reads as **−7**.
- The carries: bit 0, $0 + 0 + 1$, sum 1, carry 0; bit 1, $1 + 1 + 0$, sum 0, carry 1; bit 2, $1 + 0 + 1$, sum 0, carry 1; bit 3, $0 + 0 + 1$, sum 1, carry 0.
- So $C_4 = 0$ and $C_3 = 1$, giving $V = 1$: **overflow**. The true answer, +9, lies outside the 4-bit range −8 to +7, so the result wrapped.

(d) Through one full adder:

- from $A$ or $B$ to $C_{out}$ is 3 units (XOR, AND, OR);
- from $C_{in}$ to $C_{out}$ is 2 units;
- from $C_{in}$ to $S$ is 1 unit.

The slowest sum bit is reached after $3 + 2(n - 2) + 1 = 2n$ = **32** units, and the carry out after $3 + 2(n - 1) = 2n + 1$ = **33** units. At 20 ps per unit these are **640** ps and **660** ps.

**5.** *(08-05)*

(a) **`c` = 5**, **`p` = 21**, **`q` = 156**.

- Verilog sizes an expression by its context, which includes the left-hand side. For `c`, everything is 4 bits: $9 + 12 = 21$ wraps to $21 - 16 = 5$.
- For `p`, the operands are extended to 8 bits before adding, so the carry is kept: 21.
- `{a, b}` concatenates 1001 and 1100 into 1001 1100₂ = 156.

(b) **`w1` = −6**, **`w2` = 19**, **`w3` = −3**.

- `s` = 1010₂ is −6, and assigning it to a wider signed variable sign-extends it to 1111 1010₂, still −6.
- In `s + a`, `a` is unsigned. If any operand is unsigned, the **whole expression is unsigned**, so `s` is zero-extended to 0000 1010₂ = 10, and $10 + 9 = 19$. This is the classic signedness trap: the sum one probably meant, $-6 + 9 = 3$, needs `$signed({1'b0, a})` (08-05 §3.5).
- `s >>> 1` is a signed expression: `s` is sign-extended to 8 bits and shifted right arithmetically, giving 1111 1101₂ = −3.

(c) Nonblocking assignments (`<=`) all read their right-hand sides before any update, so the first block **swaps**: after one edge `x` = 0 and `y` = 1, and after two edges `x` = 1 and `y` = 0.

Blocking assignments (`=`) execute in order. `u = v` sets `u` to 0, then `v = u` copies that new 0. After one edge `u` = 0 and `v` = 0, and they stay 0 after the second edge. The **nonblocking** block describes two flip-flops exchanging values, which is real hardware. The blocking one loses `u`'s original value. Use nonblocking assignments in clocked blocks.

(d) The `case` has no branch for `sel` = 11, so `y` must keep its old value in that case. The block therefore describes storage, and synthesis infers a **latch**, which is unintended and hazardous for timing. Fix it by adding a `default: y = 1'b0;` (or `y = a0;`), or by assigning `y` a default value before the `case`.

(e) The inputs are 16 + 16 + 1 = 33 bits, so there are $2^{33}$ = **8 589 934 592** (≈ **8.590 × 10⁹**) combinations. At $10^6$ per second the run takes **8590** s, about **2.386** hours: feasible. A 32-bit adder with carry-in has $2^{65}$ combinations, which would take about **1.169 × 10⁶** years. Wide datapaths are verified with random and corner-case vectors, structured tests (for example, every carry-chain length) and formal equivalence checking, not exhaustively.

**6.** *(08-06)*

(a) Results:

- **Latch** $Q$: 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1. It follows $D$ whenever CLK = 1 (samples 2–3, 6–7 and 10–11) and holds otherwise. It changes **5** times (at samples 2, 3, 7, 10 and 11).
- **Flip-flop** $Q$: 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0. It captures $D$ only at the rising edges (samples 2, 6 and 10, where $D$ = 1, 0 and 0). It changes **2** times (at samples 2 and 6).

The latch passes every change of $D$ during the high phase through to $Q$; the flip-flop samples once per cycle.

(b) $T_c \ge t_{pcq} + t_{pd} + t_{\text{setup}} = 70 + 615 + 55$ = **740** ps, so $f_{\max}$ = **1.351** GHz. Hold slack is $t_{ccq} + t_{cd} - t_{\text{hold}} = 45 + 5 - 60$ = **−10** ps, a **violation**.

(c) Each buffer adds 8 ps of contamination delay, so $\lceil 10/8 \rceil$ = **2** buffers are needed, giving a hold slack of $-10 + 16$ = **+6** ps. They add $2 \times 12 = 24$ ps to the short path's maximum delay, which is nowhere near the 615 ps critical path, so **$f_{\max}$ does not change**. The clock period does not appear in the hold constraint. A hold violation is a race between the new data and the capture at the *same* edge, so no clock frequency fixes it.

(d) Each stage has $615/3 = 205$ ps of logic, so $T_c = 70 + 205 + 55$ = **330** ps and $f_{\max}$ = **3.030** GHz. Throughput rises by $740/330$ = **2.242** times, not 3, because every stage pays the 125 ps register overhead. Latency rises from 740 ps to $3 \times 330$ = **990** ps.

**7.** *(08-07)*

(a) The sequence is 0000 → 1000 → 1100 → 1110 → 1111 → 0111 → 0011 → 0001 → 0000. That is **8** states ($2n$), leaving $16 - 8$ = **8** unused.

(b) The states, as $Q_1Q_2Q_3Q_4$:

1000, 0100, 0010, 1001, 1100, 0110, 1011, 0101, 1010, 1101, 1110, 1111, 0111, 0011, 0001, then back to 1000.

- The period is **15** = $2^4 - 1$, every nonzero state, so $x^4 + x^3 + 1$ is primitive.
- The output $Q_4$ over one period is **000100110101111**.
- It contains **8** ones and 7 zeros, as every maximal-length sequence has: $2^{n-1}$ ones and $2^{n-1} - 1$ zeros.

(c) Binary **256**; ring **8**; Johnson **16**; maximal LFSR **255** (all states except 00000000).

(d) Bit 0 toggles first, and each falling output toggles the next stage one clock-to-Q later: 0111 → **0110** → **0100** → **0000** → 1000. These are three transient values: 6, 4 and 0. A decoder for 0000 sees that state for one clock-to-Q delay and may produce a glitch pulse, which is harmful if it drives a clock, reset or enable. Decode ripple counters only after they settle, or use a synchronous counter.

**8.** *(08-08)*

(a) Overlapping allowed means that after a detection the machine keeps the longest suffix that is still a prefix of 1101.

**Mealy machine, 4 states:**

| State | Meaning | $x = 0$: next, $z$ | $x = 1$: next, $z$ |
|---|---|---|---|
| $A$ | nothing useful | $A$, 0 | $B$, 0 |
| $B$ | seen 1 | $A$, 0 | $C$, 0 |
| $C$ | seen 11 | $D$, 0 | $C$, 0 |
| $D$ | seen 110 | $A$, 0 | $B$, **1** |

From $C$, another 1 keeps "11". From $D$, a 1 completes 1101, and the suffix "1" is the start of a new pattern, so the machine goes to $B$. That is the overlap.

**Moore machine, 5 states:** the same four, with output 0, plus $E$ ("seen 1101", output 1). $D$ goes to $E$ on 1. From $E$, a 0 goes to $A$ (11010 ends in "10", which is no prefix of 1101) and a 1 goes to $C$ (11011 ends in "11"). The Moore machine needs **5** states because its output depends only on the state, so detection needs a state of its own. The Mealy machine needs **4**.

(b) Writing the table with $q_1q_0x$ gives these next states and outputs:

| $q_1q_0$ | $x$ | $q_1^+q_0^+$ | $z$ |
|---|---|---|---|
| 00 ($A$) | 0 / 1 | 00 / 01 | 0 / 0 |
| 01 ($B$) | 0 / 1 | 00 / 11 | 0 / 0 |
| 11 ($C$) | 0 / 1 | 10 / 11 | 0 / 0 |
| 10 ($D$) | 0 / 1 | 00 / 01 | 0 / 1 |

Minimizing each column:

- $q_0^+$ equals $x$ in every row, so $q_0^+ = x$.
- $q_1^+ = 1$ for $(q_1q_0x)$ = 011, 110 and 111, so $q_1^+ = q_0x + q_1q_0$.
- $z = 1$ only for 101, so $z = q_1\overline{q_0}x$.

Total: $1 + 4 + 3$ = **8** literals. This encoding gives $q_0$ the meaning "the last input was 1", which is why its equation is a single wire.

(c) **Mealy:** $z = 1$ in cycles **3, 6 and 11**: inputs 0–3, 3–6 and 8–11 each read 1, 1, 0, 1. The detections at 3 and 6 share cycle 3's input, which is the overlap. **Moore:** $z = 1$ in cycles **4, 7 and 12**, one cycle later: the Moore machine must first enter state $E$ at the clock edge that ends the detecting cycle. The Mealy output is earlier but combinationally depends on $x$, so it can glitch and lengthen paths. A registered Mealy output has the Moore timing.

(d) The reference design is `det1101_mealy` in [exam_designs.v](exam_designs.v):

```verilog
module det1101_mealy (input wire clk, input wire rst, input wire x, output wire z);
    localparam [1:0] A = 2'b00, B = 2'b01, C = 2'b11, D = 2'b10;
    reg [1:0] state, next;
    always @(posedge clk)                    // state register
        if (rst) state <= A;
        else     state <= next;
    always @(*) begin                        // next-state logic
        case (state)
            A: next = x ? B : A;
            B: next = x ? C : A;
            C: next = x ? C : D;
            default: next = x ? B : A;       // D
        endcase
    end
    assign z = (state == D) & x;             // Mealy output
endmodule
```

The four codes are all used, so there is no illegal state to recover from. Flip-flops:

- the Moore machine needs **3** with binary encoding and **5** with one-hot;
- the Mealy machine needs **2** binary and **4** one-hot.

The testbench checks both machines on the stream of (c) and on 4000 random bits.

**9.** *(08-09)*

(a) Ripple carry takes $2n$ = **128** units.

| Network | Operators | Levels | Delay (units) | Speed-up |
|---|---|---|---|---|
| Kogge–Stone | $n\log_2 n - n + 1$ = **321** | **6** | 14 | $128/14$ = **9.143** |
| Sklansky | $(n/2)\log_2 n$ = **192** | **6** | 16 | **8.000** |
| Brent–Kung | $2n - 2 - \log_2 n$ = **120** | $2\log_2 n - 1$ = **11** | 24 | $128/24$ = **5.333** |

For a **low-power microcontroller**, choose Brent–Kung or even ripple carry: an address adder at tens of MHz has time to spare, and Brent–Kung uses 120 operators with fan-out 1 and short wires, against Kogge–Stone's 321 with long wires. For a **server core's critical ALU**, Kogge–Stone's minimum levels and fan-out are worth its area and energy, because the adder sets the clock. Sklansky is the compromise, but it has a fan-out of $n/2$ = 32 on its last level.

(b) $n^2 - 4n + 3 = 256 - 64 + 3$ = **195** full adders, $n - 1$ = **15** half adders, and a final adder of $2n - 2$ = **30** bits.

(c) The operands and their product:

- $0.75 \times 2^{15}$ = **24 576** and $-0.5 \times 2^{15}$ = **−16 384**.
- Their integer product is **−402 653 184**, in Q2.30 (32 bits).
- Shifting right by 15 returns to Q1.15: **−12 288** = $-0.375 \times 2^{15}$. The product is exact, so no rounding is needed.
- The one product that does not fit is $(-1) \times (-1) = +1$: $(-32\,768)^2 = 2^{30}$, which in Q1.15 would be 32 768, one above the largest value, 32 767. The hardware should **saturate** to 32 767 (0.99997), not wrap to −1.

(d) A sum of $N$ terms needs $\lceil\log_2 N\rceil$ = 6 guard bits, so the accumulator needs $32 + 6$ = **38** bits.

(e) $\log_2 32$ = **5** levels of 32 multiplexers: **160** two-input multiplexers.

**10.** *(08-10)*

(a) R1 → R2 needs $50 + 560 + 40 = 650$ ps and R2 → R3 needs $50 + 520 + 40 = 610$ ps. The minimum period is **650** ps, so $f_{\max}$ = **1.538** GHz. The hold slack of R1 → R2 is $30 + 30 - 35$ = **25** ps.

(b) With R2's clock 60 ps late:

- R1 → R2 gains 60 ps: it needs $650 - 60$ = **590** ps.
- R2 → R3 launches 60 ps late into an on-time capture edge (skew −60 ps for that path): it needs $610 + 60$ = **670** ps.
- The period becomes **670** ps, $f_{\max}$ = **1.493** GHz, *slower* than before.
- The hold slack of R1 → R2 becomes $25 - 60$ = **−35** ps, a violation no clock frequency can fix.

A bad idea on both counts: skew lent to one path is taken from the next.

(c) The two paths need $650 - \delta$ and $610 + \delta$. They balance at $\delta$ = **20** ps, giving $T_c$ = **630** ps and $f_{\max}$ = **1.587** GHz. The hold slack of R1 → R2 is $25 - 20$ = **5** ps: met, but thin.

(d) Cycle-to-cycle jitter can shorten any one period, so both setup checks lose 25 ps: $T_c$ = **655** ps (1.527 GHz). The hold check compares the launch and capture at the *same* edge, so cycle-to-cycle jitter does not affect it.

**11.** *(08-11)*

(a) $2^{17} \times 32$ = **4 194 304** bits (4 Mbit), with **17** address bits. A square array has $\sqrt{4\,194\,304}$ = **2048** rows and **2048** columns, holding $2048/32$ = **64** words per row. The row decoder takes $\log_2 2048$ = **11** address bits and the column multiplexers $\log_2 64$ = **6**.

(b) A 4 × 4 multiplier ROM has $2^8$ addresses of 8 bits: **2048** bits. An 8 × 8 multiplier ROM has $2^{16}$ addresses of 16 bits: **1 048 576** bits (1 Mbit), which is why multipliers are logic, not tables.

(c) With 4-input LUTs, three LUTs each AND four inputs, and a fourth ANDs their outputs: **4** LUTs in **2** levels. With 6-input LUTs, two first-level LUTs and one second-level LUT: **3** LUTs in **2** levels.

(d) Each read port selects 1 of 32 registers for each of 64 bits, using $32 - 1 = 31$ two-input multiplexers per bit. That is $64 \times 31 = 1984$ per port and **7936** for four ports. Ports, not storage, dominate the cost of multi-ported register files.

**12.** *(08-12)*

(a) Logic cells $1584/5280$ = **30.00**%; block RAMs $6/30$ = **20.00**%; DSP blocks $2/8$ = **25.00**%; I/O $21/39$ = **53.85**%.

(b) The critical path totals $1.39 + 8.62 + 13.47 + 0.82$ = **24.30** ns, so $f_{\max}$ = $1000/24.30$ = **41.15** MHz. At 48 MHz the period is 20.83 ns, so the slack is **−3.467** ns: the design **fails**. Routing is $13.47/24.30$ = **55.43**% of the path.

(c) A 3% gain reaches about **42.39** MHz, still short of 48 MHz. Seed sweeps close gaps of a few percent, not the **16.6**% needed here ($48/41.15 - 1$). Pipelined, each stage carries half of the $8.62 + 13.47 = 22.09$ ns, plus the $1.39 + 0.82 = 2.21$ ns overhead: $11.045 + 2.21 = 13.255$ ns, giving **75.44** MHz and a slack of **+7.578** ns at 48 MHz. The cost is one cycle of latency and the pipeline registers.

(d) Static timing analysis reports slack *against the constraint it is given*. At 12 MHz (83.3 ns) a 24.3 ns path passes easily, but that says nothing about 48 MHz. Constrain the clock at its real frequency (48 MHz, with margin for the internal oscillator's tolerance) and re-run place and route. The placer and router also optimize toward the constraint, so a correct constraint changes the result, not just the report.

**13.** *(08-01, 08-09, 08-11)*

(a) The product of two 8-bit signed numbers needs **16** bits. The extremes are:

- each product lies between $(-128)(127) = -16\,256$ and $(-128)(-128) = +16\,384$;
- the largest dot product is $256 \times 16\,384$ = **4 194 304** = $2^{22}$;
- the most negative is $256 \times (-16\,256)$ = **−4 161 536**.

A signed $k$-bit accumulator holds $-2^{k-1}$ to $2^{k-1} - 1$. With **24** bits the range is ±8 388 608, enough. With 23 bits the maximum would be $2^{22} - 1 = 4\,194\,303$, one short of the worst case. This agrees with the guard-bit rule: $16 + \log_2 256 = 24$.

(b) $0.2 + 0.1$ = **0.3** pJ per MAC. Per inference $2.5 \times 10^6 \times 0.3$ pJ = **0.75** µJ, and at 10 inferences per second, **7.5** µW.

(c) Weight fetches, eight weights per 64-bit read:

- **(i) SRAM, every use:** one 20 pJ read delivers eight weights, so **2.5** pJ per weight use. Per inference that is $2.5 \times 10^6 \times 2.5$ pJ = **6.25** µJ, or **62.5** µW: **8.333** times the arithmetic.
- **(ii) SRAM once, then reuse:** only $25\,000/8 = 3125$ reads per inference, $3125 \times 20$ pJ = **0.0625** µJ, **0.08333** times the arithmetic. Reuse cut the fetch energy a hundredfold, to a twelfth of the arithmetic.
- **(iii) DRAM, every use:** 1300/8 = **162.5** pJ per weight use, so **406.3** µJ per inference and **4.063** mW, **541.7** times the arithmetic.

The arithmetic is the cheap part unless data movement is organized. The energy goes into moving data, so always-on accelerators keep the weights in small local SRAM, reuse every fetched operand as many times as possible and avoid DRAM entirely. These are 45 nm figures and smaller nodes lower all of them, but the ratio between arithmetic and data movement has persisted (08-09 §9).

(d) Clock frequency:

- Without pipelining, $1.1 + 0.6 + 0.1 = 1.8$ ns, so **555.6** MHz.
- With a register after the multiplier, the longer stage sets the period: $1.1 + 0.1 = 1.2$ ns, **833.3** MHz.
- The application needs only $2.5 \times 10^6 \times 10$ = $2.5 \times 10^7$ MACs per second: **25** MHz with one unit.

The clock period, 40 ns, is 22 times the unpipelined delay, so **pipelining would add registers, energy and latency for nothing**. Spend the margin on **lower supply voltage** instead: dynamic energy per operation scales roughly with $V^2$ (08-09 §3.9), and slower gates at low voltage still fit easily in 40 ns. Clock-gate the unit between inferences, too. Throughput requirements, not maximum frequency, should set the design.

**14.** *(08-01, 08-07, 08-10)*

(a) Binary 7 = 0111 and 8 = 1000: **4** bits change. Gray code is $g = b \oplus (b \gg 1)$: 7 → **0100** and 8 → **1100**, so **1** bit changes.

If the receiving clock samples a binary pointer mid-change, each synchronizer resolves independently. The reader may then see any mix of old and new bits, such as 1111 = 15 or 0000, a pointer value that never existed, and could read empty slots or overwrite unread data. With Gray code only one bit is in flight, so the synchronized value is either the old pointer or the new one, both of which are safe.

(b) The flows during the burst:

- The burst lasts $256 \times 10$ ns = **2.56** µs.
- The reader starts after 3 read cycles (40 ns) and reads for 2.52 µs: $2.52\ \mu\text{s} \times 75$ MHz = **189** samples.
- Peak occupancy, at the end of the burst, is $256 - 189$ = **67** samples.
- A depth of **128** is the next power of two. The standard pointer scheme needs one: each pointer is a binary counter converted to Gray code, which wraps with a single-bit change only when the counter wraps at a power of two, and the full test assumes it (08-10 §3.7).
- Sustained operation needs the reader to drain each burst before the next fills the FIFO. On average, 256 samples at 75 MHz take **3.413** µs, the shortest sustainable interval between burst starts.

(c) 128 entries need 7 address bits, and each pointer carries **8** bits. The extra wrap bit distinguishes full (same address, different wrap bit) from empty (identical pointers). Each 8-bit pointer crosses through 8 two-stage synchronizers, so two crossings use $2 \times 8 \times 2$ = **32** flip-flops.

(d) $T_c$ = 800 ps, and each stage contributes $800 - 50 - 30 = 720$ ps. The denominator is $T_W F_C F_D = 20\ \text{ps} \times 1.25\ \text{GHz} \times 10^8\ \text{s}^{-1} = 2.5 \times 10^6$ s⁻¹.

- Two stages: $S/\tau = 720/25 = 28.8$, so MTBF $= e^{28.8}/(2.5 \times 10^6)$ = **1.287 × 10⁶** s, only about **14.90** days. A product with this synchronizer would fail in the field.
- Three stages: $S/\tau = 57.6$, so MTBF = **4.144 × 10¹⁸** s, about **1.313 × 10¹¹** years.

**Ship three stages.** The cost is one more cycle of latency on the pointer crossing, which slightly delays the full and empty flags, a conservative error. At 75 MHz, two stages were astronomically safe. Raising the clock to 1.25 GHz cut $S$ by a factor of about 18 and took the exponent with it.

**15.** *(08-07, 08-09, 08-10, 08-12)* **Rubric:** 2 points per claim, 1 for identifying the flaw and 1 for a question that would expose it. Each part lists the minimum acceptable flaw first; any one of the other points earns the flaw point too. A question earns its point if the answer to it would confirm or refute the claim with data.

(a) **Minimum flaw:** a TOPS figure means nothing without the operand format, the sparsity assumption and the utilization. It is usually a peak: MAC units × 2 × clock, at the narrowest format and often counting skipped zeros (08-09 §9). Other acceptable points:

- Delivered throughput is often limited by memory bandwidth and data movement, not arithmetic (Question 13).
- Energy per inference, not TOPS, is what matters in an edge product.
- The frequency behind the peak may hold only at the highest voltage and with good cooling.

*Ask:* "What throughput and energy per inference do you measure on our target network, at what format, batch size and sparsity?"

(b) **Minimum flaw:** "closed timing" means nothing without the corners, constraints and margins. Other acceptable points:

- Setup must pass at the slow corner (low voltage, high or low temperature, slow process), and hold at the fast corner.
- The analysis must use extracted parasitics after routing, with clock uncertainty for jitter and skew and on-chip variation derates.
- Every clock domain and crossing must be correctly constrained; a missing or false-path constraint hides failures (Question 12d).

*Ask:* "What were the worst setup and hold slacks at each sign-off corner, with what clock uncertainty and derates, and how many paths were excluded by exceptions?"

(c) **Minimum flaw:** a synchronizer only makes failure *unlikely*. The MTBF grows exponentially with resolution time but is never infinite (08-10 §3.5). Other acceptable points:

- The MTBF depends on $\tau$ at the worst operating corner, on the clock and data rates, and on the number of crossings in the chip and the fleet; these multiply into a field failure rate (Question 14d).
- Multi-bit values must not be synchronized bit by bit, except Gray-coded counters. They need a handshake or a FIFO, or the bits reconverge inconsistently.
- Pulses shorter than the destination clock period can be missed.

*Ask:* "What is the computed MTBF at the worst corner, summed over all crossings and devices in the field, and how did you verify the crossings structurally (a CDC checking tool)?"

(d) **Minimum flaw:** an LFSR is linear and completely predictable. Anyone who observes $2n$ = 64 consecutive output bits can solve for the taps and state by linear algebra over GF(2) (the Berlekamp–Massey algorithm does it efficiently) and then compute every past and future bit (08-07). Other acceptable points:

- The power-up state of the seed register is a poor and often repeatable entropy source, so many devices may share keys.
- A 32-bit state allows at most $2^{32}$ different keys, which can be searched exhaustively.

*Ask:* "What is your entropy source, how is it health-tested, and which standardized cryptographic random-number generator turns it into keys?"

---

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| X08.1a | B6 hex, unsigned | 182 | — |
| X08.1b | B6 hex, signed | -74 | — |
| X08.1c | 5A + 3C hex, as an unsigned integer | 150 | — |
| X08.1d | 5A + 3C hex, signed result | -106 | — |
| X08.1e | -0.40625 in Q1.7, stored integer | -52 | — |
| X08.1f | -0.40625 in Q1.7, bit pattern as unsigned | 204 | — |
| X08.1g | Q1.7 resolution | 0.0078125 | — |
| X08.1h | Q1.7 maximum | 0.9921875 | — |
| X08.1i | Hamming syndrome | 5 | — |
| X08.1j | corrected code word, as an integer | 102 | — |
| X08.1k | data bits, as an integer | 6 | — |
| X08.1l | overflow flag V for 5A + 3C | 1 | — |
| X08.2a | transistors, AND-OR | 18 | — |
| X08.2b | transistors, NAND-NAND | 12 | — |
| X08.2c | transistors, AOI22 + inverter | 10 | — |
| X08.2d | lookup-table integer, parity | 150 | — |
| X08.2e | lookup-table integer, majority | 232 | — |
| X08.3a | prime implicants | 5 | — |
| X08.3b | essential prime implicants | 4 | — |
| X08.3c | minimal SOP terms | 4 | — |
| X08.3d | minimal SOP literals | 12 | — |
| X08.3e | minimal POS literals | 12 | — |
| X08.3f | hazardous single-input transitions | 4 | — |
| X08.3g | hazard-free SOP literals | 14 | — |
| X08.3h | SOP terms with don't cares | 3 | — |
| X08.3i | SOP literals with don't cares | 7 | — |
| X08.4a | 0101 - 0111, signed result | -2 | — |
| X08.4b | 0110 - 1101, result read as signed | -7 | — |
| X08.4c | 16-bit ripple, slowest sum bit | 32 | units |
| X08.4d | 16-bit ripple, carry out | 33 | units |
| X08.4e | slowest sum bit at 20 ps per unit | 640 | ps |
| X08.4f | carry out at 20 ps per unit | 660 | ps |
| X08.4g | 0101 - 0111, carry out | 0 | — |
| X08.4h | 0101 - 0111, overflow flag | 0 | — |
| X08.4i | 0110 - 1101, carry out | 0 | — |
| X08.4j | 0110 - 1101, overflow flag | 1 | — |
| X08.5a | c | 5 | — |
| X08.5b | p | 21 | — |
| X08.5c | q | 156 | — |
| X08.5d | w1 | -6 | — |
| X08.5e | w2 | 19 | — |
| X08.5f | w3 | -3 | — |
| X08.5g | input combinations, 16-bit adder with carry-in | 8.590e9 | — |
| X08.5h | exhaustive run time | 8590 | s |
| X08.5i | exhaustive run time | 2.386 | h |
| X08.5j | exhaustive run time, 32-bit adder | 1.169e6 | years |
| X08.5k | x after one edge | 0 | — |
| X08.5l | y after one edge | 1 | — |
| X08.5m | u after one edge | 0 | — |
| X08.5n | v after one edge | 0 | — |
| X08.5o | x after two edges | 1 | — |
| X08.5p | y after two edges | 0 | — |
| X08.6a | latch output changes | 5 | — |
| X08.6b | flip-flop output changes | 2 | — |
| X08.6c | minimum period | 740 | ps |
| X08.6d | maximum frequency | 1.351 | GHz |
| X08.6e | hold slack | -10 | ps |
| X08.6f | buffers needed | 2 | — |
| X08.6g | hold slack with buffers | 6 | ps |
| X08.6h | pipelined period | 330 | ps |
| X08.6i | pipelined frequency | 3.030 | GHz |
| X08.6j | throughput gain | 2.242 | — |
| X08.6k | pipelined latency | 990 | ps |
| X08.7a | Johnson states used | 8 | — |
| X08.7b | Johnson states unused | 8 | — |
| X08.7c | LFSR period | 15 | — |
| X08.7d | LFSR output bits, as an integer (first bit most significant) | 2479 | — |
| X08.7e | ones per period | 8 | — |
| X08.7f | 8-bit binary counter states | 256 | — |
| X08.7g | 8-bit ring counter states | 8 | — |
| X08.7h | 8-bit Johnson counter states | 16 | — |
| X08.7i | 8-bit maximal LFSR states | 255 | — |
| X08.8a | Moore states | 5 | — |
| X08.8b | Mealy states | 4 | — |
| X08.8c | Mealy equation literals | 8 | — |
| X08.8d | Mealy detections (cycles 3, 6, 11) | 3 | — |
| X08.8e | first Moore detection cycle | 4 | — |
| X08.8j | second Moore detection cycle | 7 | — |
| X08.8k | third Moore detection cycle | 12 | — |
| X08.8l | Mealy detection cycles, first | 3 | — |
| X08.8m | Mealy detection cycles, second | 6 | — |
| X08.8n | Mealy detection cycles, third | 11 | — |
| X08.8f | Moore flip-flops, binary | 3 | — |
| X08.8g | Moore flip-flops, one-hot | 5 | — |
| X08.8h | Mealy flip-flops, binary | 2 | — |
| X08.8i | Mealy flip-flops, one-hot | 4 | — |
| X08.9a | 64-bit ripple delay | 128 | units |
| X08.9b | Kogge–Stone operators | 321 | — |
| X08.9c | Sklansky operators | 192 | — |
| X08.9d | Brent–Kung operators | 120 | — |
| X08.9e | Kogge–Stone and Sklansky levels | 6 | — |
| X08.9f | Brent–Kung levels | 11 | — |
| X08.9g | Kogge–Stone speed-up | 9.143 | — |
| X08.9h | Sklansky speed-up | 8.000 | — |
| X08.9i | Brent–Kung speed-up | 5.333 | — |
| X08.9j | Dadda full adders | 195 | — |
| X08.9k | Dadda half adders | 15 | — |
| X08.9l | Dadda final adder width | 30 | bits |
| X08.9m | 0.75 in Q1.15 | 24576 | — |
| X08.9n | -0.5 in Q1.15 | -16384 | — |
| X08.9o | integer product (Q2.30) | -402653184 | — |
| X08.9p | Q1.15 result | -12288 | — |
| X08.9q | accumulator width | 38 | bits |
| X08.9r | barrel shifter multiplexers | 160 | — |
| X08.9s | barrel shifter levels | 5 | — |
| X08.10a | minimum period, no skew | 650 | ps |
| X08.10b | maximum frequency, no skew | 1.538 | GHz |
| X08.10c | hold slack, no skew | 25 | ps |
| X08.10d | R1 to R2 period with 60 ps skew | 590 | ps |
| X08.10e | R2 to R3 period with 60 ps skew | 670 | ps |
| X08.10f | maximum frequency with 60 ps skew | 1.493 | GHz |
| X08.10g | hold slack with 60 ps skew | -35 | ps |
| X08.10h | optimum skew | 20 | ps |
| X08.10i | balanced period | 630 | ps |
| X08.10j | balanced frequency | 1.587 | GHz |
| X08.10k | hold slack at optimum skew | 5 | ps |
| X08.10l | period with jitter | 655 | ps |
| X08.10m | frequency with jitter | 1.527 | GHz |
| X08.11a | SRAM bits | 4194304 | — |
| X08.11b | SRAM address bits | 17 | — |
| X08.11c | rows (and columns) | 2048 | — |
| X08.11d | words per row | 64 | — |
| X08.11e | row address bits | 11 | — |
| X08.11f | column address bits | 6 | — |
| X08.11g | 4 x 4 multiplier ROM bits | 2048 | — |
| X08.11h | 8 x 8 multiplier ROM bits | 1048576 | — |
| X08.11i | 4-input LUTs for a 12-input AND | 4 | — |
| X08.11j | 6-input LUTs for a 12-input AND | 3 | — |
| X08.11k | LUT levels | 2 | — |
| X08.11l | read-port multiplexers | 7936 | — |
| X08.12a | logic-cell utilization | 30.00 | % |
| X08.12b | block-RAM utilization | 20.00 | % |
| X08.12c | DSP utilization | 25.00 | % |
| X08.12d | I/O utilization | 53.85 | % |
| X08.12e | critical path | 24.30 | ns |
| X08.12f | maximum frequency | 41.15 | MHz |
| X08.12g | slack at 48 MHz | -3.467 | ns |
| X08.12h | routing share | 55.43 | % |
| X08.12i | frequency after a 3% gain | 42.39 | MHz |
| X08.12j | pipelined frequency | 75.44 | MHz |
| X08.12k | pipelined slack at 48 MHz | 7.578 | ns |
| X08.12l | frequency gap to 48 MHz | 16.6 | % |
| X08.13a | product width | 16 | bits |
| X08.13b | largest dot product | 4194304 | — |
| X08.13c | most negative dot product | -4161536 | — |
| X08.13d | accumulator width | 24 | bits |
| X08.13e | arithmetic energy per MAC | 0.3 | pJ |
| X08.13f | arithmetic energy per inference | 0.75 | µJ |
| X08.13g | arithmetic power | 7.5 | µW |
| X08.13h | SRAM energy per weight | 2.5 | pJ |
| X08.13i | SRAM energy per inference | 6.25 | µJ |
| X08.13j | SRAM power | 62.5 | µW |
| X08.13k | SRAM over arithmetic | 8.333 | — |
| X08.13l | DRAM energy per weight | 162.5 | pJ |
| X08.13m | DRAM energy per inference | 406.3 | µJ |
| X08.13n | DRAM power | 4.063 | mW |
| X08.13o | DRAM over arithmetic | 541.7 | — |
| X08.13p | unpipelined frequency | 555.6 | MHz |
| X08.13q | pipelined frequency | 833.3 | MHz |
| X08.13r | required clock with one MAC | 25 | MHz |
| X08.13s | SRAM energy per inference with reuse | 0.0625 | µJ |
| X08.13t | with reuse, over arithmetic | 0.08333 | — |
| X08.14a | binary bits changing, 7 to 8 | 4 | — |
| X08.14b | Gray bits changing, 7 to 8 | 1 | — |
| X08.14c | Gray code of 7, as an integer | 4 | — |
| X08.14d | Gray code of 8, as an integer | 12 | — |
| X08.14e | burst duration | 2.56 | µs |
| X08.14f | samples read during the burst | 189 | — |
| X08.14g | peak occupancy | 67 | — |
| X08.14h | chosen depth | 128 | — |
| X08.14i | shortest burst interval | 3.413 | µs |
| X08.14j | pointer width | 8 | bits |
| X08.14k | synchronizer flip-flops | 32 | — |
| X08.14l | MTBF, two stages | 1.287e6 | s |
| X08.14m | MTBF, two stages | 14.90 | days |
| X08.14n | MTBF, three stages | 4.144e18 | s |
| X08.14o | MTBF, three stages | 1.313e11 | years |
