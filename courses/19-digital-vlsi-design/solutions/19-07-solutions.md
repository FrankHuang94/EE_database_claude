# Solutions 19-07 · Sequential Circuits, Timing and Clocking

Problems: [19-07 problem set](../problems/19-07-problems.md) · Chapter: [19-07](../chapters/19-07-sequential-timing-and-clocking.md). Every number below is recomputed by [verify_19_07.py](../verify/verify_19_07.py).

---

## Solutions

### Solution 19-07.1

$T_c = 40 + 500 + 25$ = **565** ps, so $f_{max}$ = **1.77** GHz.

### Solution 19-07.2

(a) $30 + 0 - 10$ = **20** ps of slack.

(b) Any skew above **20** ps violates hold. Flip-flops are designed with $t_{ccq} > t_{hold}$ precisely so that shift registers survive modest skew.

### Solution 19-07.3

(a) 60/15 = **4** FO4. (b) 4/20 = **20** % of the cycle is spent on sequencing rather than logic.

### Solution 19-07.4

Setup: $700 \ge 665 - \delta$, so $\delta \ge$ **−35** ps. Hold: $65 \ge 20 + \delta$, so $\delta \le$ **45** ps.

### Solution 19-07.5

$400 - 70 - 15 - 20$ = **295** ps of logic, 74% of the cycle.

### Solution 19-07.6

4 GHz is 250 ps, so each stage may hold 200 ps of logic: $N = \lceil 1200/200\rceil$ = **6** stages, with latency $6 \times 250$ = **1500** ps, 25% more than the logic alone.

### Solution 19-07.7

50/250 = **20** % overhead. With 12 stages, $T_c$ = 100 + 50 = 150 ps: **6.67** GHz, with a third of each cycle now overhead.

### Solution 19-07.8

(a) $T_c/2 - t_{setup}$ = 200 − 15 = **185** ps.

(b) The loop needs $260 + 90 + 2 \times 20$ = **390** ps ≤ 400 ps, so it works. The first half-cycle's data arrives $260 + 20$ = 280 ps after its latch opens, **80** ps into the next half-cycle: well within the 185 ps limit.

### Solution 19-07.9

(a) τ = 5 fF/200 µS = **25** ps.

(b) $\tau\ln(10\ \text{mV}/10\ \mu\text{V}) = 25 \times \ln 1000$ = **172.7** ps.

### Solution 19-07.10

(a) $T_0f_{clk}f_{data} = 10\ \text{ps} \times 2\ \text{GHz} \times 50\ \text{MHz} = 10^6$ s⁻¹, so MTBF $= e^{450/15}/10^6 = e^{30}/10^6$ = **1.07 × 10⁷** s, about **124** days: not enough for a product.

(b) $t_r = \tau\ln(\text{MTBF} \times 10^6) = 15\ \text{ps} \times \ln(3.156 \times 10^{14})$ = **500.8** ps, slightly more than the 450 ps available.

(c) $e^{950/15}/10^6$ s ≈ **1.01 × 10¹⁴** years. One more cycle of latency buys an astronomically safe margin.

### Solution 19-07.11

(a) Time per instruction $T(N) = (t_L/N + t_o)(1 + bN) = t_L/N + bt_L + t_o + bt_oN$. Setting $dT/dN = -t_L/N^2 + bt_o = 0$ gives $N_{opt} = \sqrt{t_L/(bt_o)}$.

(b) $N_{opt} = \sqrt{2000/6}$ = **18.3**. At 18 stages, $T$ = **479.1** ps (19 stages: 479.3 ps). Unpipelined, $(2000 + 60)(1.1)$ = **2266** ps, so pipelining gives **4.73** times the performance, far less than the **12.0**-fold cut in cycle time (from 2060 to **171.1** ps; the logic per stage falls **18**-fold).

### Solution 19-07.12

(a) Near $V_M$, each inverter delivers a small-signal current $-g_m$ times its input deviation into the other node. For deviations $u_1, u_2$: $C\dot u_1 = -g_mu_2$ and $C\dot u_2 = -g_mu_1$, so the difference obeys $C\dot{\Delta u} = g_m\Delta u$, growing as $e^{t/\tau}$ with $\tau = C/g_m$. With $g_m = g_{mn} + g_{mp}$ and each saturated square-law device contributing $kV_{ov}$, $g_m = 2kV_{ov}$.

(b) Doubling $k$ doubles $g_m$: τ = **50** ps.

(c) If $C$ doubles with width as well, τ is unchanged: as with intrinsic delay (19-02), a latch made only of its own capacitance gains nothing from being wider. Fast synchronizer flip-flops minimize the extra load on their storage nodes.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 19-07.1a | minimum period | 565 | ps |
| 19-07.1b | maximum frequency | 1.77 | GHz |
| 19-07.2a | hold slack | 20 | ps |
| 19-07.2b | skew that violates hold | 20 | ps |
| 19-07.3a | overhead in FO4 | 4 | — |
| 19-07.3b | overhead share | 20 | % |
| 19-07.4a | lowest skew | -35 | ps |
| 19-07.4b | highest skew | 45 | ps |
| 19-07.5a | logic budget | 295 | ps |
| 19-07.5b | logic share | 74 | % |
| 19-07.6a | stages | 6 | — |
| 19-07.6b | latency | 1500 | ps |
| 19-07.6c | latency increase | 25 | % |
| 19-07.7a | overhead share at 4 GHz | 20 | % |
| 19-07.7b | frequency with 12 stages | 6.67 | GHz |
| 19-07.8a | maximum borrowing | 185 | ps |
| 19-07.8b | loop requirement | 390 | ps |
| 19-07.8c | borrowing used | 80 | ps |
| 19-07.9a | time constant | 25 | ps |
| 19-07.9b | extra resolution time | 172.7 | ps |
| 19-07.10a | MTBF, two flip-flops | 1.07e7 | s |
| 19-07.10b | MTBF in days | 124 | days |
| 19-07.10e | ten years times the failure-rate denominator | 3.156e14 | — |
| 19-07.10c | resolution time for 10 years | 500.8 | ps |
| 19-07.10d | MTBF, three flip-flops | 1.01e14 | years |
| 19-07.11a | optimal depth | 18.3 | — |
| 19-07.11b | time per instruction, 18 stages | 479.1 | ps |
| 19-07.11c | time per instruction, 19 stages | 479.3 | ps |
| 19-07.11d | time per instruction, unpipelined | 2266 | ps |
| 19-07.11e | speed-up | 4.73 | — |
| 19-07.11f | cycle time, 18 stages | 171.1 | ps |
| 19-07.11g | cycle-time reduction | 12.0 | — |
| 19-07.11h | logic-per-stage reduction | 18 | — |
| 19-07.12a | tau with twice the width | 50 | ps |
