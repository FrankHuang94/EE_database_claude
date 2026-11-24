# Solutions 19-10 · The ASIC Flow I: Synthesis and Static Timing Analysis

Problems: [19-10 problem set](../problems/19-10-problems.md) · Chapter: [19-10](../chapters/19-10-synthesis-and-sta.md). Every number below is recomputed by [verify_19_10.py](../verify/verify_19_10.py).

---

## Solutions

### Solution 19-10.1

Fractional positions: $t_s = (0.100 - 0.0531329)/(0.122474 - 0.0531329)$ = **0.6759**; $t_C = (0.0060 - 0.00346659)/(0.00912787 - 0.00346659)$ = **0.4475**.

Along the load at the first slew: $50.4824 + 0.4475 \times (79.7753 - 50.4824)$ = **63.59** ps. At the second slew: $69.8132 + 0.4475 \times (103.8626 - 69.8132)$ = **85.05** ps. Along the slew: $63.59 + 0.6759 \times (85.05 - 63.59)$ = **78.10** ps.

**Check.** The result lies inside the four corner values (50.5 to 103.9 ps) and nearer the higher-slew row, as $t_s > 0.5$ implies.

### Solution 19-10.2

(a) $R_{\text{eff}} = (0.4287654 - 0.0970882)/(0.0632852 - 0.00912787)$ = **6.124** kΩ (ns/pF). $D_0 = 0.0970882 - 6.124 \times 0.00912787$ ns = **41.19** ps.

(b) $D(0.030) = 41.19 + 6.124 \times 30$ ps (pF × kΩ = ns, so 0.030 pF × 6.124 kΩ = 0.1837 ns) = **224.92** ps.

(c) It differs from the table's 225.05 ps by only about **−0.1** ps (**−0.06** %). Once the load dominates the cell's own capacitance, the output current is set mainly by the driving transistor, and the delay grows almost exactly linearly with load. The model fails at very small loads, where the intrinsic delay and the input slew dominate, and its $R_{\text{eff}}$ changes with the input slew (19-02).

### Solution 19-10.3

(a) Forward: H1 = max(0, 10) + 35 = 45; H2 = max(10, 30) + 50 = 80; H3 = 45 + 20 = 65; H4 = max(45, 80) + 45 = 125; H5 (z) = max(65, 125) + 40 = **165** ps; W (w) = 80 + 25 = 105 ps.

Backward: z requires 150 at H5, so H3 and H4 are required at 110. H1 feeds H3 (110 − 20 = 90) and H4 (110 − 45 = 65): **65**. H2 feeds H4 (110 − 45 = 65) and W (120 − 25 = 95): **65**. p: 65 − 35 = 30. q feeds H1 (30) and H2 (65 − 50 = 15): **15**. r: 65 − 50 = 15.

| Node | Arrival | Required | Slack (ps) |
|---|---|---|---|
| p | 0 | 30 | 30 |
| q | 10 | 15 | 5 |
| r | 30 | 15 | −15 |
| H1 | 45 | 65 | 20 |
| H2 | 80 | 65 | −15 |
| H3 | 65 | 110 | 45 |
| H4 | 125 | 110 | −15 |
| H5 (z) | 165 | 150 | −15 |
| W (w) | 105 | 120 | 15 |

(b) Critical path r → H2 → H4 → H5 → z, slack **−15** ps.

(c) To z: p and q each through H1 and then H3 or H4 (four), q and r through H2 and H4 (two); to w: q and r through H2 (two). Total **8**.

(d) Speed H2 up by **15** ps (to 35 ps). Then H2 arrives at 65, H4 at max(45, 65) + 45 = 110 and z at max(65, 110) + 40 = 150: slack 0. No other path fails: the next-longest path to z, q → H1 → H4 → H5, arrives at 10 + 35 + 45 + 40 = 130 ps, and w improves to 90 ps.

### Solution 19-10.4

(a) The inverter and the NAND2 are negative unate, so a rising output comes from a falling input; the buffer is positive unate. Working back from each output edge:

- Output rising ← buffer input rising ← NAND output rising ← inverter output falling ← x rising: $0 + 20 + 40 + 50$ = **110** ps.
- Output falling ← NAND output falling ← inverter output rising ← x falling: $8 + 30 + 35 + 45$ = **118** ps.

(b) Taking each gate's worst delay and the latest input: $8 + 30 + 40 + 50$ = **128** ps, which is 10 ps pessimistic because no single edge sees all the worst delays.

(c) Inverter and NAND2 (with its other input high it acts as an inverter): negative unate. Buffer: positive unate.

### Solution 19-10.5

(a) The subject tree has three covers:

| Cover | Area (µm²) | Delay (ps) |
|---|---|---|
| `a22oi_1` | 7.5072 | 207.0 |
| `inv_1` + three `nand2_1` | 15.0144 | 63.4 + 77.1 + 77.1 = 217.6 |
| `and2_1` + two `nand2_1` | 13.7632 | 163.0 + 77.1 = 240.1 |

`a22oi_1` is best for both: **7.5072** µm² and **207.0** ps.

(b) Also three covers: `inv_1` + `o21ai_1` (**8.7584** µm², 63.4 + 154.8 = **218.2** ps); `inv_1` + two `nand2_1` + two `inv_1` (18.768 µm², 281.0 ps); `and2_1` + `nand2_1` + two `inv_1` (17.5168 µm², 303.5 ps). The `o21ai_1` cover wins both.

(c) A complex cell implements the whole function in a single stage of series-parallel transistors (19-03), with no internal node to charge and no extra inverter. The multi-cell covers add stages, each with its own intrinsic delay, and more transistors. The complex cell's arcs are slower than a NAND2's, but slower by less than an extra stage.

### Solution 19-10.6

(a) Arrival $0.25 + 0.307 + 0.85 = 1.407$ ns; required $1.5 + 0.20 - 0.051 - 0.08 = 1.569$ ns; setup slack **0.162** ns. $T_{\min} = 1.338$ ns, $f_{\max}$ = **747** MHz.

(b) Arrival $0.25 + 0.307 + 0.10 = 0.657$ ns; required $0.20 - 0.029 + 0.04 = 0.211$ ns; hold slack **0.446** ns.

(c) With setup 0.103 ns the required time is 1.517 ns: setup slack **0.110** ns. The falling-D setup time is twice the rising one, so the data edge that reaches the flip-flop matters, which is why tools check each edge separately.

The negative skew (capture clock 0.05 ns early) cost setup 0.05 ns and gave hold 0.05 ns.

### Solution 19-10.7

(a) Arrival at the output port $0.6 + 1.0 = 1.6$ ns; required $2.5 - 0.7 - 0.1 = 1.7$ ns; slack **0.1** ns.

(b) Arrival at D $0.6 + 1.5 = 2.1$ ns; required $2.5 + 0.3 - 0.1 - 0.1 = 2.6$ ns; slack **0.5** ns.

(c) Arrival at the port $0.3 + 0.3 + 1.2 = 1.8$ ns; required 1.7 ns; slack **−0.1** ns.

(d) The input delay is measured from the ideal clock edge, so a late capture clock in (b) gives the data more time. In (c) the launch is delayed by the latency, but the external register's capture time is fixed by the output delay relative to the ideal edge, so latency eats the budget. That is why output paths often fail after clock-tree insertion, and why I/O timing is constrained with care about which clock edge is the reference.

### Solution 19-10.8

(a) Required $1.5 - 0.10 = 1.40$ ns; arrival $0.30 + 2.5 = 2.80$ ns; slack **−1.40** ns.

(b) The capture edge moves to $2 \times 1.5 = 3.0$ ns: required 2.90 ns; slack **0.10** ns.

(c) The default hold check moves to one period before the new capture edge, 1.5 ns: required $1.5 + 0.05 = 1.55$ ns; earliest arrival $0.30 + 0.4 = 0.70$ ns; hold slack **−0.85** ns, a spurious violation.

(d) `-hold 1` moves the hold check back to the launch edge: required 0.05 ns; hold slack **0.65** ns.

### Solution 19-10.9

(a) Arrival $0.50 + 0.10 + 0.25 + 0.05 = 0.90$ ns; required $0.50 + 0.30 + 0.02 = 0.82$ ns; hold slack **0.080** ns.

(b) Arrival $0.92 \times 0.90 = 0.828$ ns; required $1.08 \times 0.80 + 0.02 = 0.884$ ns; hold slack **−0.056** ns.

(c) CRPR credit $(1.08 - 0.92) \times 0.50$ = **0.080** ns; hold slack **0.024** ns.

The common segment, 0.50 ns, is the largest clock delay here; without CRPR, derating it both ways costs more than the whole un-derated margin.

### Solution 19-10.10

(a) $3 \times 4\% $ = **12** % per stage.

(b) Path mean $N\mu$, path σ $\sqrt{N}\sigma$, so the 3σ margin as a fraction of the mean is $3(\sigma/\mu)/\sqrt{N} = 12\%/\sqrt{N}$: **6.0** % at 4 stages, **3.0** % at 16, **1.5** % at 64. It reaches 4 % at $N = 9$ and is at most 4 % for **9** or more stages.

(c) The path variance is $N\sigma^2[1 + (N - 1)\rho]$, so the effective derate is $12\%\sqrt{[1 + (N - 1)\rho]/N}$: **6.0** % at 16 stages and **5.53** % at 64. As $N \to \infty$ it tends to $12\%\sqrt{\rho}$ = **5.37** %.

(d) Statistics remove only the independent (random, local) part of variation. The correlated part, here 20 %, adds coherently along the path and leaves a floor that no amount of averaging lowers; it must still be covered by corners or flat derates.

### Solution 19-10.11

(a) Through A: $100 + 30 + 0.3 \times 20 = 136$ ps, output slew $25 + 0.2 \times 20 = 29$ ps. Through B: $60 + 30 + 0.3 \times 120 = 126$ ps, slew $25 + 0.2 \times 120 = 49$ ps. Graph-based: arrival 136 ps (from A) with slew 49 ps (from B). At H: $136 + 40 + 0.3 \times 49$ = **190.7** ps.

(b) Path through A: $136 + 40 + 0.3 \times 29$ = **184.7** ps. Path through B: $126 + 40 + 0.3 \times 49 = 180.7$ ps. Worst real path: 184.7 ps.

(c) **6.0** ps of pessimism. Graph-based analysis combines the latest arrival with the worst slew; every real path has an arrival no later and a slew no worse, and delay increases with both, so the combination bounds every path from above. Path-based analysis removes the bound's slack on the paths that matter.

### Solution 19-10.12

(a) Typical: arrival $0.20 + 0.25 + 0.20 = 0.65$ ns; required $0.60 + 0.02 = 0.62$ ns; hold slack **0.030** ns.

Slow: clock latencies $0.30$ and $0.90$ ns; $t_{ccq} = 0.325$ ns, logic 0.26 ns, hold time 0.026 ns. Arrival $0.30 + 0.325 + 0.26 = 0.885$ ns; required $0.90 + 0.026 = 0.926$ ns; hold slack **−0.041** ns.

(b) The skew (capture minus launch latency) is a clock-tree delay; at the slow corner it grows from 0.40 to 0.60 ns, faster than the data path that has to cover it. Hold depends on the difference between clock and data delays, and any corner that stretches the clock tree more than the data path can be the hold-limiting one.

(c) At least **0.041** ns at the slow corner, which is $0.041/1.3$ = **0.032** ns at the typical corner (where the hold slack then becomes about 0.062 ns). Hold buffers must be sized at the corner where hold fails, then checked against setup at all corners.

---

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 19-10.1a | fractional slew position | 0.6759 | — |
| 19-10.1b | fractional load position | 0.4475 | — |
| 19-10.1c | delay at first slew | 63.59 | ps |
| 19-10.1d | delay at second slew | 85.05 | ps |
| 19-10.1e | interpolated fall delay | 78.10 | ps |
| 19-10.2a | effective resistance | 6.124 | kΩ |
| 19-10.2b | intercept D0 | 41.19 | ps |
| 19-10.2c | linear prediction at 0.030 pF | 224.92 | ps |
| 19-10.2d | linear minus bilinear | -0.1 | ps |
| 19-10.2e | linear minus bilinear, relative | -0.06 | % |
| 19-10.3a | arrival at z | 165 | ps |
| 19-10.3b | required time at H1 | 65 | ps |
| 19-10.3c | required time at q | 15 | ps |
| 19-10.3d | worst slack | -15 | ps |
| 19-10.3e | number of paths | 8 | — |
| 19-10.3f | speed-up needed at H2 | 15 | ps |
| 19-10.3g | next-longest path to z | 130 | ps |
| 19-10.4a | rising output arrival | 110 | ps |
| 19-10.4b | falling output arrival | 118 | ps |
| 19-10.4c | edge-blind arrival | 128 | ps |
| 19-10.5a | best area, AOI22 tree | 7.5072 | µm² |
| 19-10.5b | best delay, AOI22 tree | 207.0 | ps |
| 19-10.5c | inv plus three nand2 delay | 217.6 | ps |
| 19-10.5d | and2 plus two nand2 delay | 240.1 | ps |
| 19-10.5e | best area, (A+B)C tree | 8.7584 | µm² |
| 19-10.5f | best delay, (A+B)C tree | 218.2 | ps |
| 19-10.5g | covers of each tree | 3 | — |
| 19-10.5h | nand2-and-inverter cover delay, (A+B)C | 281.0 | ps |
| 19-10.5i | and2 cover delay, (A+B)C | 303.5 | ps |
| 19-10.6a | setup slack | 0.162 | ns |
| 19-10.6b | maximum frequency | 747 | MHz |
| 19-10.6c | hold slack | 0.446 | ns |
| 19-10.6d | setup slack with falling D | 0.110 | ns |
| 19-10.7a | feed-through slack | 0.1 | ns |
| 19-10.7b | input-to-register slack | 0.5 | ns |
| 19-10.7c | register-to-output slack | -0.1 | ns |
| 19-10.8a | single-cycle setup slack | -1.40 | ns |
| 19-10.8b | multicycle setup slack | 0.10 | ns |
| 19-10.8c | hold slack, setup multicycle only | -0.85 | ns |
| 19-10.8d | hold slack with hold multicycle | 0.65 | ns |
| 19-10.9a | hold slack, no derates | 0.080 | ns |
| 19-10.9b | hold slack, derates, no CRPR | -0.056 | ns |
| 19-10.9c | CRPR credit | 0.080 | ns |
| 19-10.9d | hold slack with CRPR | 0.024 | ns |
| 19-10.10a | flat per-stage derate | 12 | % |
| 19-10.10b | effective derate, 4 stages | 6.0 | % |
| 19-10.10c | effective derate, 16 stages | 3.0 | % |
| 19-10.10d | effective derate, 64 stages | 1.5 | % |
| 19-10.10e | depth for at most 4 percent | 9 | stages |
| 19-10.10f | correlated derate, 16 stages | 6.0 | % |
| 19-10.10g | correlated derate, 64 stages | 5.53 | % |
| 19-10.10h | correlated derate limit | 5.37 | % |
| 19-10.11a | graph-based arrival at H | 190.7 | ps |
| 19-10.11b | path-based arrival through A | 184.7 | ps |
| 19-10.11c | path-based arrival through B | 180.7 | ps |
| 19-10.11d | graph-based pessimism | 6.0 | ps |
| 19-10.12a | hold slack, typical | 0.030 | ns |
| 19-10.12b | hold slack, slow | -0.041 | ns |
| 19-10.12c | hold buffer at slow corner | 0.041 | ns |
| 19-10.12d | same buffer at typical corner | 0.032 | ns |
| 19-10.12e | typical hold slack after fix | 0.062 | ns |
