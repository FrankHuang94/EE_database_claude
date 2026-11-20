# Solutions 16-11 · DSP Hardware Architectures

Problems: [16-11 problems](../problems/16-11-problems.md) · Chapter: [16-11](../chapters/16-11-dsp-hardware-architectures.md). Every number below is recomputed by [verify_16_11.py](../verify/verify_16_11.py): widths and budgets from their definitions, look-ahead recursions by simulation against `scipy.signal.lfilter`, CSD forms by an independent digit search, CORDIC against `math` functions, and the fixed-point CORDIC against the committed Verilog test vectors.

---

## Solutions

### Solution 16-11.1

Product: $12 + 18$ = **30** bits. Accumulator: $30 + \lceil\log_2128\rceil$ = **37** bits.

### Solution 16-11.2

Folded: 64 multiplications per output × 100 MS/s = $6.4 \times 10^9$ per second; each block does $5 \times 10^8$: 12.8, so **13** blocks. Without folding: 128 × 10⁸ / (5 × 10⁸) = 25.6, so **26** blocks.

### Solution 16-11.3

$0.875 = 1 - 2^{-3}$: **1** subtractor (binary $0.111_2$ needs 2 adders). $0.9375 = 1 - 2^{-4}$: **1** subtractor (binary $0.1111_2$ needs 3). CSD replaces each run of ones by one addition and one subtraction.

### Solution 16-11.4

Two loops. Through $y[n - 1]$: multiplier and two adders ($2.0 + 0.5 + 0.5 = 3.0$ ns) with one register: 3.0 ns. Through $y[n - 2]$: also a multiplier and two adders, with two registers: 1.5 ns. The iteration bound is the larger, **3.0** ns, so at most **333** MHz.

### Solution 16-11.5

Substituting the recursion into itself three times: $y[n] = a^4y[n - 4] + x[n] + ax[n - 1] + a^2x[n - 2] + a^3x[n - 3]$. For $a = 0.9$: $0.6561y[n - 4] + x[n] + 0.9x[n - 1] + 0.81x[n - 2] + 0.729x[n - 3]$; the simulation matches the original recursion to rounding error. The loop now has four registers: $T_\infty = 2.5/4$ = **0.625** ns (**1.6** GHz).

### Solution 16-11.6

One MAC handles 400 million taps per second, 16 per sample: **25** MS/s. Four MACs: **100** MS/s.

### Solution 16-11.7

$K_8$ = **1.64674**, $K_{16}$ = **1.64676**. The residual angle after $n$ iterations is below $\arctan2^{-(n-1)} \approx 2^{-(n-1)}$; $2^{-(n-1)} \le 2^{-11}$ needs $n$ = **12** iterations ($\arctan2^{-11} = 4.88 \times 10^{-4}$ rad).

### Solution 16-11.8

Vectoring drives $y$ to zero: magnitude **5.0000** (after dividing by $K_{16}$) and angle **53.13°**, against exactly 5 and $\arctan(4/3) = 53.130°$.

### Solution 16-11.9

Per MAC: 8-bit $0.2 + 0.03$ = **0.23** pJ; 32-bit integer $3.1 + 0.1$ = **3.2** pJ; 32-bit floating point $3.7 + 0.9$ = **4.6** pJ. At $10^9$ MACs per second: 0.23 mW, 3.2 mW and 4.6 mW. A 64-bit DRAM access (1.3–2.6 nJ) costs as much as **406 to 812** 32-bit integer MACs.

### Solution 16-11.10

Required: $64 \times 48{,}000$ = **3.07** million MACs per second. M55 peak: $4 \times 10^8$ per second, so **0.768**%. M52 single-beat: $2 \times 10^8$, so **1.54**%. The real load is higher because each MAC needs operand loads, pointer updates and loop control, and the kernel cannot keep the MAC lanes full every cycle; the peak figure is an upper bound on what the hardware can do.

### Solution 16-11.11

With registers after the multipliers and after each adder level, the longest stage is the multiplier: **2.0** ns, **500** MHz. Latency: 1 (multiplier) + 6 (adder levels for 64 inputs) = **7** cycles. The unpipelined tree ran at 200 MHz (5.0 ns).

### Solution 16-11.12

The worst error over the 64 angles is **6.86** LSB. The residual angle after 14 iterations contributes about 2 LSB; the rest comes from the 14 arithmetic right shifts, each of which floors (truncates toward $-\infty$) and so adds a biased error of up to one LSB, accumulating through the iterations. Fixes: carry two or three guard bits in $x$ and $y$ and round once at the output; or round the shifted values instead of flooring.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 16-11.1a | product width | 30 | bits |
| 16-11.1b | accumulator width | 37 | bits |
| 16-11.2a | blocks, folded | 13 | — |
| 16-11.2b | blocks, unfolded | 26 | — |
| 16-11.3a | adders for 0.875 | 1 | — |
| 16-11.3b | adders for 0.9375 | 1 | — |
| 16-11.4a | iteration bound | 3.0 | ns |
| 16-11.4b | maximum rate | 333 | MHz |
| 16-11.5a | iteration bound | 0.625 | ns |
| 16-11.5b | rate | 1.6 | GHz |
| 16-11.6a | rate with one MAC | 25 | MS/s |
| 16-11.6b | rate with four MACs | 100 | MS/s |
| 16-11.7a | K8 | 1.64674 | — |
| 16-11.7b | K16 | 1.64676 | — |
| 16-11.7c | iterations | 12 | — |
| 16-11.8a | magnitude | 5.0000 | — |
| 16-11.8b | angle | 53.13 | ° |
| 16-11.9a | 8-bit MAC energy | 0.23 | pJ |
| 16-11.9b | 32-bit integer MAC energy | 3.2 | pJ |
| 16-11.9c | 32-bit float MAC energy | 4.6 | pJ |
| 16-11.9d | MACs per DRAM access, low | 406 | — |
| 16-11.9e | MACs per DRAM access, high | 812 | — |
| 16-11.10a | MAC rate | 3.07 | M/s |
| 16-11.10b | M55 load | 0.768 | % |
| 16-11.10c | M52 load | 1.54 | % |
| 16-11.11a | critical path | 2.0 | ns |
| 16-11.11b | clock | 500 | MHz |
| 16-11.11c | latency | 7 | cycles |
| 16-11.12a | worst error | 6.86 | LSB |
