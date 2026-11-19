# Solutions 08-10 · Timing, Metastability and Clock-Domain Crossing

Problems: [08-10 problems](../problems/08-10-problems.md) · Chapter: [08-10](../chapters/08-10-timing-metastability-cdc.md). Every number below is recomputed by [verify_08_10.py](../verify/verify_08_10.py): timing by arrival-time arithmetic on each path, MTBF from the synchronizer equation and, independently, by integrating the failure window over uniformly distributed data arrivals, and the CDC counts by enumerating every possible sample.

---

## Solutions

### Solution 08-10.1

(a) The 520 ps path is critical: $T_c \ge 60 + 520 + 40 = 620$ ps, $f_{\max}$ = **1.61** GHz.

(b) At 1.5 GHz, $T_c$ = 666.7 ps. Slack $= 666.7 - 40 - (60 + t_{pd})$: **46.7** ps and **86.7** ps.

### Solution 08-10.2

(a) $30 + 15 - 25$ = **20** ps.

(b) $20 - 30$ = **−10** ps: a violation.

(c) No: the clock period does not appear in the hold inequality. The fix is to add delay to the short path (or reduce the skew).

### Solution 08-10.3

(a) MTBF $\propto e^{S/\tau}$, so one extra $\tau$ multiplies it by $e$ = **2.718**.

(b) $\ln 10^6$ = **13.8** time constants.

### Solution 08-10.4

At 1.25 GHz, $T_c$ = 800 ps, and the path needs $50 + 700 + 40 = 790$ ps.

(a) Slack $800 - 790$ = **10** ps.

(b) An early capture clock means $\delta = -30$ ps: slack $800 - 30 - 790$ = **−20** ps, a violation.

(c) The shortest cycle is $800 - 25 = 775$ ps: slack **−15** ps.

(d) With both, $50 + t_{pd} + 40 \le 800 - 30 - 25$: $t_{pd} \le$ **655** ps. The clock uncertainty (55 ps here) is a direct tax on every path's logic budget.

### Solution 08-10.5

(a) $T_c = 1200/k + 100$: $k$ = 1 gives 1300 ps, **0.769** GHz; $k$ = 4 gives 400 ps, **2.5** GHz; $k$ = 12 gives 200 ps, **5.0** GHz. As $k \to \infty$, $T_c \to 100$ ps: **10** GHz, set entirely by the registers.

(b) $4 \times 400$ = **1600** ps, against 1300 ps unpipelined.

(c) Doubling the throughput needs $T_c \le 650$ ps: $1200/k \le 550$, so $k \ge 2.18$: **3** stages ($k$ = 2 gives 700 ps, not quite).

### Solution 08-10.6

(a) The slowest stage sets the clock: $500 + 100 = 600$ ps, **1.67** GHz.

(b) $400 + 100 = 500$ ps, **2.0** GHz, with the same total logic and the same number of registers.

### Solution 08-10.7

$T_c$ = 500 ps, so each stage after the first gives $500 - 60 - 40 = 400$ ps $= 16\tau$ of resolution time. The denominator is $T_W F_C F_D = 30 \times 10^{-12} \times 2 \times 10^9 \times 5 \times 10^7 = 3 \times 10^6$ per second.

(a) Two flip-flops, $S$ = 400 ps: MTBF $= e^{16}/(3 \times 10^6)$ = **2.96** s. A failure every few seconds.

(b) Three, $S$ = 800 ps: $e^{32}/(3 \times 10^6)$ = $2.63 \times 10^7$ s = **0.83** years. Four, $S$ = 1200 ps: $e^{48}/(3 \times 10^6)$ = $2.34 \times 10^{14}$ s = **7.4 × 10⁶** years.

(c) **4** flip-flops. At high clock frequencies a cycle is only a few $\tau$ long, which is why high-speed domains use longer synchronizers.

### Solution 08-10.8

$e^{S/\tau} = \text{MTBF} \times T_W F_C F_D = 10^4 \times 3.156 \times 10^7\ \text{s} \times 4 \times 10^6\ \text{s}^{-1} = 1.26 \times 10^{18}$, so $S = 20\ \text{ps} \times \ln(1.26 \times 10^{18})$ = **834** ps.

### Solution 08-10.9

(a) 011 → 100 changes **3** bits: $2^3$ = **8** possible values.

(b) The true value is 3 or 4; the sample can be 0 or 7: an error of up to **4**.

(c) Gray 010 → 110 changes one bit: **2** values.

### Solution 08-10.10

(a) Each pulse toggles the level once, and each level must last 2 destination cycles: **20** ns between pulses, which is **8** source cycles at 2.5 ns.

(b) One pulse per 20 ns: **50** MHz.

### Solution 08-10.11

(a) Two crossings into the 80 MHz domain take $3 \times 12.5 = 37.5$ ns each, and two into the 100 MHz domain $3 \times 10 = 30$ ns each: $2 \times 37.5 + 2 \times 30$ = **135** ns per word.

(b) $1/135\ \text{ns}$ = **7.41** million words per second, $\times 32$ bits = **237** Mb/s. An asynchronous FIFO could move a word on almost every destination cycle, 80 million words per second: the handshake is for occasional transfers.

### Solution 08-10.12

(a) The burst lasts $256/250\ \text{MHz} = 1.024$ µs, during which the reader removes $102.4$, so **102** words for certain.

(b) $256 - 102$ = **154** words, plus 3 for synchronizer latency is 157: depth **256**.

(c) $\log_2 256$ = **8** address bits; **9**-bit pointers.

(d) $256$ words every 3 µs is **85.3** million words per second, below the reader's 100 million: the FIFO drains between bursts. (If it were above, no depth would suffice.)

### Solution 08-10.13

(a) Failure rates add: the chip fails at $2000/10^9$ per year, an MTBF of $10^9/2000$ = **5 × 10⁵** years.

(b) $5 \times 10^6 \times 2000 / 10^9$ = **10** failures per year across the fleet. Whether that is acceptable depends on the consequence of a failure: harmless in a toy, unacceptable in a braking controller.

### Solution 08-10.14

(a) The failure count is proportional to $e^{-S/\tau}$, so $10^5/100 = e^{100\ \text{ps}/\tau}$, and $\tau = 100\ \text{ps}/\ln 1000$ = **14.5** ps.

(b) Going from 300 to 900 ps multiplies the count by $e^{-600/\tau} = 1000^{-6} = 10^{-18}$: $10^5 \times 10^{-18}$ = **1e-13** failures, none in practice. This is how $\tau$ is measured: deliberately short resolution times make failures frequent enough to count, and the exponential law extrapolates.

### Solution 08-10.15

(a) The longest register-to-register path runs through the multiplier and the adder: $600 + 300 + 80$ = 980 ps, **1.02** GHz.

(b) Splitting the multiplier means a register between its two halves and another between the multiplier and the adder. The register-to-register paths are then the first half ($300 + 80$ ps), the second half ($300 + 80$ ps) and the adder loop ($300 + 80$ ps): 380 ps each, **2.63** GHz.

(c) The adder's output feeds its own input through the accumulator register: a register placed inside that loop would add a cycle of delay to the feedback, so the loop would add each product to the sum from two cycles ago, a different computation. Loops are pipelined only by changing the algorithm (for example, keeping two interleaved partial sums and adding them at the end), which is how fast floating-point accumulators work.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 08-10.1a | maximum frequency | 1.61 | GHz |
| 08-10.1b | slack, 520 ps path | 46.7 | ps |
| 08-10.1c | slack, 480 ps path | 86.7 | ps |
| 08-10.2a | hold slack | 20 | ps |
| 08-10.2b | hold slack with 30 ps skew | -10 | ps |
| 08-10.3a | MTBF factor per τ | 2.718 | — |
| 08-10.3b | time constants for 10^6 | 13.8 | — |
| 08-10.4a | slack, ideal clock | 10 | ps |
| 08-10.4b | slack, early capture clock | -20 | ps |
| 08-10.4c | slack with jitter | -15 | ps |
| 08-10.4d | logic budget with both | 655 | ps |
| 08-10.5a | frequency, k = 1 | 0.769 | GHz |
| 08-10.5b | frequency, k = 4 | 2.5 | GHz |
| 08-10.5c | frequency, k = 12 | 5.0 | GHz |
| 08-10.5d | limit | 10 | GHz |
| 08-10.5e | latency, k = 4 | 1600 | ps |
| 08-10.5f | stages to double throughput | 3 | — |
| 08-10.6a | unbalanced frequency | 1.67 | GHz |
| 08-10.6b | balanced frequency | 2.0 | GHz |
| 08-10.7a | MTBF, two flip-flops | 2.96 | s |
| 08-10.7b | MTBF, three flip-flops | 0.83 | yr |
| 08-10.7c | MTBF, four flip-flops | 7.4e6 | yr |
| 08-10.7d | flip-flops for 1000 years | 4 | — |
| 08-10.8a | resolution time needed | 834 | ps |
| 08-10.9a | bits changing | 3 | — |
| 08-10.9b | possible binary samples | 8 | — |
| 08-10.9c | largest binary error | 4 | — |
| 08-10.9d | possible Gray samples | 2 | — |
| 08-10.10a | minimum pulse spacing | 20 | ns |
| 08-10.10b | in source cycles | 8 | — |
| 08-10.10c | maximum pulse rate | 50 | MHz |
| 08-10.11a | time per transfer | 135 | ns |
| 08-10.11b | transfer rate | 7.41 | MHz |
| 08-10.11c | data rate | 237 | Mb/s |
| 08-10.12a | words read during a burst | 102 | — |
| 08-10.12b | minimum depth | 154 | — |
| 08-10.12c | chosen depth | 256 | — |
| 08-10.12d | address bits | 8 | — |
| 08-10.12e | pointer bits | 9 | — |
| 08-10.12f | average write rate | 85.3 | MHz |
| 08-10.13a | chip MTBF | 5e5 | yr |
| 08-10.13b | fleet failures per year | 10 | — |
| 08-10.14a | τ | 14.5 | ps |
| 08-10.14b | failures at 900 ps | 1e-13 | — |
| 08-10.15a | unpipelined frequency | 1.02 | GHz |
| 08-10.15b | pipelined frequency | 2.63 | GHz |
