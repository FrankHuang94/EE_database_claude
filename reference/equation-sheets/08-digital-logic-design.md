# Equation Sheet · 08 Digital Logic Design

The relations to know cold from Course 08, each with its conditions and the chapter that derives it.

Conventions:

- "$n$-bit" numbers are two's complement unless called unsigned;
- a signed Q$m$.$f$ number has $m$ integer bits (including the sign) and $f$ fractional bits;
- minterm $m_i$ has $i$ = the inputs read as a binary number, with the first variable most significant;
- in the unit-delay model every gate and inverter takes 1 unit;
- $t_{pcq}$, $t_{ccq}$ are clock-to-Q propagation and contamination delays, $t_{pd}$, $t_{cd}$ those of the logic;
- skew $\delta$ is positive when the capture clock is late.

## Numbers and codes

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Unsigned $n$ bits: 0 to $2^n - 1$. Two's complement: $-2^{n-1}$ to $2^{n-1} - 1$, value $= -b_{n-1}2^{n-1} + \sum_{i<n-1} b_i2^i$ | Negate: invert and add 1. Sign-extend by copying the top bit | [08-01](../../courses/08-digital-logic-design/chapters/08-01-number-systems-and-codes.md) |
| Overflow $V = C_n \oplus C_{n-1}$: two operands of the same sign give a result of the other sign | Unsigned overflow is the carry out $C_n$ | [08-01](../../courses/08-digital-logic-design/chapters/08-01-number-systems-and-codes.md) |
| Q$m$.$f$: resolution $2^{-f}$, range $-2^{m-1}$ to $2^{m-1} - 2^{-f}$ | Store round($x \cdot 2^f$) | [08-01](../../courses/08-digital-logic-design/chapters/08-01-number-systems-and-codes.md) |
| Products: $a$-bit × $b$-bit needs $a + b$ bits; Q$m_1$.$f_1$ × Q$m_2$.$f_2$ = Q$(m_1 + m_2)$.$(f_1 + f_2)$. Sums of $N$ terms: $\lceil\log_2 N\rceil$ guard bits | The extra product bit is needed only for (most negative)² | [08-01](../../courses/08-digital-logic-design/chapters/08-01-number-systems-and-codes.md), [08-09](../../courses/08-digital-logic-design/chapters/08-09-arithmetic-circuits.md) |
| Quantization error RMS = LSB/$\sqrt{12}$; SQNR = $6.02b + 1.76$ dB for a full-scale sine | Truncation biases by about −½ LSB; round to nearest to remove it | [08-01](../../courses/08-digital-logic-design/chapters/08-01-number-systems-and-codes.md), [08-09](../../courses/08-digital-logic-design/chapters/08-09-arithmetic-circuits.md) |
| Float: $x = (-1)^s \times 1.F \times 2^{E - \text{bias}}$, bias $= 2^{e-1} - 1$ | IEEE formats: exponent all zeros for zero and subnormals, all ones for ∞ and NaN | [08-01](../../courses/08-digital-logic-design/chapters/08-01-number-systems-and-codes.md) |
| Gray code $g = b \oplus (b \gg 1)$; back: $b_i = g_{n-1} \oplus \cdots \oplus g_i$ | Successive codes differ in one bit, including the wrap (for $2^k$ entries) | [08-01](../../courses/08-digital-logic-design/chapters/08-01-number-systems-and-codes.md) |
| Minimum distance $d$: detects $d - 1$ errors, corrects $\lfloor (d - 1)/2 \rfloor$ | Parity: $d = 2$; Hamming: 3; SEC-DED: 4 | [08-01](../../courses/08-digital-logic-design/chapters/08-01-number-systems-and-codes.md) |
| Hamming SEC: smallest $r$ with $2^r \ge k + r + 1$; SEC-DED adds 1 bit. Syndrome = position of the error | Check bits at positions 1, 2, 4, …; (72,64) for 64 data bits | [08-01](../../courses/08-digital-logic-design/chapters/08-01-number-systems-and-codes.md) |
| CRC: transmit $M(x)x^r$ plus the remainder of $M(x)x^r \div g(x)$ (mod-2 arithmetic) | A well-chosen degree-$r$ $g(x)$ catches every burst of length ≤ $r$ | [08-01](../../courses/08-digital-logic-design/chapters/08-01-number-systems-and-codes.md) |

## Boolean algebra and minimization

| Relation | Conditions / notes | Chapter |
|---|---|---|
| De Morgan: $\overline{AB} = \overline{A} + \overline{B}$, $\overline{A + B} = \overline{A}\,\overline{B}$ | Push bubbles; NAND-NAND = AND-OR | [08-02](../../courses/08-digital-logic-design/chapters/08-02-boolean-algebra-and-gates.md) |
| Absorption $A + AB = A$; $A + \overline{A}B = A + B$; dual distributive $A + BC = (A + B)(A + C)$ | Every theorem has a dual (swap AND/OR, 0/1) | [08-02](../../courses/08-digital-logic-design/chapters/08-02-boolean-algebra-and-gates.md) |
| Consensus: $AB + \overline{A}C + BC = AB + \overline{A}C$ | The consensus term is redundant logically but removes static-1 hazards | [08-02](../../courses/08-digital-logic-design/chapters/08-02-boolean-algebra-and-gates.md), [08-04](../../courses/08-digital-logic-design/chapters/08-04-combinational-building-blocks.md) |
| Shannon: $f = \overline{x}\,f_{x=0} + x\,f_{x=1}$ | The basis of multiplexers, LUTs and equivalence checking | [08-02](../../courses/08-digital-logic-design/chapters/08-02-boolean-algebra-and-gates.md) |
| $2^{2^n}$ functions of $n$ inputs; truth table $2^n$ rows; a term with $k$ of $n$ literals covers $2^{n-k}$ minterms | Lookup-table integer: row $i$'s output is bit $i$ | [08-02](../../courses/08-digital-logic-design/chapters/08-02-boolean-algebra-and-gates.md), [08-03](../../courses/08-digital-logic-design/chapters/08-03-logic-minimization.md) |
| Static CMOS: $k$-input NAND/NOR $2k$ transistors, inverter 2, AND/OR = inverting gate + inverter; AOI22 8 | Series stacks rarely exceed about 4 | [08-02](../../courses/08-digital-logic-design/chapters/08-02-boolean-algebra-and-gates.md) |
| K-map: group 1s (and don't cares) in rectangles of $2^k$ adjacent cells, Gray-ordered; essential primes first | POS: group the 0s to get $\overline{F}$, then De Morgan | [08-03](../../courses/08-digital-logic-design/chapters/08-03-logic-minimization.md) |

## Combinational blocks and Verilog

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $2^k$:1 multiplexer: $2^k - 1$ two-input muxes in $k$ levels; any $n$-input function from a $2^{n-1}$:1 mux with data in $\{0, 1, x, \overline{x}\}$ | Decoder: $n$ inputs, $2^n$ one-hot outputs (one minterm each) | [08-04](../../courses/08-digital-logic-design/chapters/08-04-combinational-building-blocks.md) |
| Full adder: $S = A \oplus B \oplus C_{in}$, $C_{out} = AB + C_{in}(A \oplus B) = G + PC_{in}$ | $G = AB$, $P = A \oplus B$ | [08-04](../../courses/08-digital-logic-design/chapters/08-04-combinational-building-blocks.md) |
| Ripple-carry: top sum bit at $2n$ units, carry out at $2n + 1$ | Subtract: $A + \overline{B} + 1$ | [08-04](../../courses/08-digital-logic-design/chapters/08-04-combinational-building-blocks.md) |
| Verilog widths: an expression is sized by its largest operand *and* its destination; any unsigned operand makes the expression unsigned | `>>>` shifts in the sign bit only for `signed` operands | [08-05](../../courses/08-digital-logic-design/chapters/08-05-verilog-and-testbenches.md) |
| Clocked blocks use `<=`; combinational `always @(*)` uses `=` and assigns every output on every path | A missing branch infers a latch | [08-05](../../courses/08-digital-logic-design/chapters/08-05-verilog-and-testbenches.md) |
| Random testing with $N = M$ vectors covers $1 - 1/e$ ≈ 63.2% of $M$ cases; full coverage takes about $M(\ln M + 0.577)$ | Exhaustive is practical to about 20–30 input bits | [08-05](../../courses/08-digital-logic-design/chapters/08-05-verilog-and-testbenches.md) |

## Sequential circuits

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Setup: $t_{pcq} + t_{pd} + t_{\text{setup}} \le T_c$ | Use the slowest delays at the slow corner | [08-06](../../courses/08-digital-logic-design/chapters/08-06-latches-and-flip-flops.md) |
| Hold: $t_{ccq} + t_{cd} \ge t_{\text{hold}}$ | No $T_c$: fix with delay on the short path, never with the clock | [08-06](../../courses/08-digital-logic-design/chapters/08-06-latches-and-flip-flops.md) |
| With skew: $T_c \ge t_{pcq} + t_{pd} + t_{\text{setup}} - \delta$; $t_{ccq} + t_{cd} \ge \delta + t_{\text{hold}}$. Jitter $t_j$ adds to the setup side | Skew lent to one path is taken from the next | [08-10](../../courses/08-digital-logic-design/chapters/08-10-timing-metastability-cdc.md) |
| Pipelining into $k$ stages: $T_c = t_{\text{logic}}/k + t_{\text{reg}}$; latency $t_{\text{logic}} + k\,t_{\text{reg}}$ | $t_{\text{reg}} = t_{pcq} + t_{\text{setup}}$ | [08-06](../../courses/08-digital-logic-design/chapters/08-06-latches-and-flip-flops.md), [08-10](../../courses/08-digital-logic-design/chapters/08-10-timing-metastability-cdc.md) |
| States with $n$ flip-flops: ring $n$, Johnson $2n$, binary $2^n$, maximal LFSR $2^n - 1$ | Ripple counters settle in $n\,t_{cq}$ and pass through false states | [08-07](../../courses/08-digital-logic-design/chapters/08-07-registers-counters-shift-registers.md) |
| Fibonacci LFSR $x^n + x^k + 1$: $Q_1^{\text{next}} = Q_n \oplus Q_k$. m-sequence: $2^{n-1}$ ones, $2^{n-1} - 1$ zeros per period | Maximal iff the polynomial is primitive | [08-07](../../courses/08-digital-logic-design/chapters/08-07-registers-counters-shift-registers.md) |
| FSM flip-flops: $\lceil\log_2 N\rceil$ binary, $N$ one-hot; illegal codes $2^{\lceil\log_2 N\rceil} - N$ and $2^N - N$ | Mealy outputs lead Moore by one cycle; Mealy never needs more states | [08-08](../../courses/08-digital-logic-design/chapters/08-08-finite-state-machines.md) |

## Arithmetic

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Prefix operator $(G, P)_{i:j} = (G_{i:k} + P_{i:k}G_{k-1:j},\ P_{i:k}P_{k-1:j})$; carry $C_i = G_{i-1:0}$ | Fold $C_0$ into bit 0's generate | [08-09](../../courses/08-digital-logic-design/chapters/08-09-arithmetic-circuits.md) |
| Kogge–Stone: $\log_2 n$ levels, $n\log_2 n - n + 1$ operators. Sklansky: $\log_2 n$ levels, $(n/2)\log_2 n$, fan-out $n/2$. Brent–Kung: $2\log_2 n - 1$ levels, $2n - 2 - \log_2 n$ | Ripple $2n$ units | [08-09](../../courses/08-digital-logic-design/chapters/08-09-arithmetic-circuits.md) |
| Dadda $n \times n$: $n^2 - 4n + 3$ full adders, $n - 1$ half adders, final adder $2n - 2$ bits; levels 4, 6, 8 for 8, 16, 32 bits | Radix-4 Booth: $n/2$ partial products | [08-09](../../courses/08-digital-logic-design/chapters/08-09-arithmetic-circuits.md) |
| Barrel shifter: $n\log_2 n$ two-input muxes in $\log_2 n$ levels | | [08-09](../../courses/08-digital-logic-design/chapters/08-09-arithmetic-circuits.md) |

## Metastability and clock-domain crossing

| Relation | Conditions / notes | Chapter |
|---|---|---|
| MTBF $= e^{S/\tau}/(T_W F_C F_D)$; two-flip-flop $S = T_c - t_{pcq} - t_{\text{setup}}$, each extra stage adds the same | Each $\tau$ of extra time multiplies MTBF by $e$; $2.3\tau$ by 10 | [08-10](../../courses/08-digital-logic-design/chapters/08-10-timing-metastability-cdc.md) |
| Multi-bit values cross with Gray-coded counters, a handshake or an asynchronous FIFO; never bit by bit | Flags from synchronized pointers are conservative | [08-10](../../courses/08-digital-logic-design/chapters/08-10-timing-metastability-cdc.md) |
| FIFO depth to absorb a burst of $B$: $B(1 - f_r/f_w)$ plus synchronizer latency, rounded up to $2^k$; pointers $k + 1$ bits | Average rates must also balance | [08-10](../../courses/08-digital-logic-design/chapters/08-10-timing-metastability-cdc.md) |

## Memories, programmable logic and FPGA flow

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Address bits $\log_2(\text{words})$; array $R$ rows × $C$ columns: row bits $\log_2 R$, column bits $\log_2(C/m)$ for $m$-bit words | Roughly square arrays keep the decoders and wires short | [08-11](../../courses/08-digital-logic-design/chapters/08-11-memories-and-programmable-logic.md) |
| ROM: $2^n m$ bits. PLA: $2np + pm$ crosspoints | $p$ product terms | [08-11](../../courses/08-digital-logic-design/chapters/08-11-memories-and-programmable-logic.md) |
| A $k$-LUT implements any of $2^{2^k}$ functions; worst case for $n$ inputs $2^{n-k+1} - 1$ LUTs (Shannon) | Register-file read port: $w(R - 1)$ two-input muxes | [08-11](../../courses/08-digital-logic-design/chapters/08-11-memories-and-programmable-logic.md) |
| FPGA vs ASIC break-even: $N/(f - a)$ units for NRE $N$, unit costs $f$ (FPGA) and $a$ (ASIC) | Plus schedule, risk and flexibility | [08-11](../../courses/08-digital-logic-design/chapters/08-11-memories-and-programmable-logic.md) |
| Flow: synthesis → placement → routing → timing analysis → bitstream. $f_{\max} = 1/(\text{clock-to-Q} + \text{logic} + \text{routing} + \text{setup})$; slack = constraint period − path | Slack is only as meaningful as the constraint | [08-12](../../courses/08-digital-logic-design/chapters/08-12-fpga-implementation-flow.md) |
