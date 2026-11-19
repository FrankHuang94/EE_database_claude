# Solutions 08-06 · Latches, Flip-Flops and Sequential Timing

Problems: [08-06 problems](../problems/08-06-problems.md) · Chapter: [08-06](../chapters/08-06-latches-and-flip-flops.md). Every number below is recomputed by [verify_08_06.py](../verify/verify_08_06.py): latches and flip-flops are simulated sample by sample from their gate equations, timing results come from the constraint inequalities evaluated over the stated paths, and the switching threshold is found by solving the square-law current balance numerically.

---

## Solutions

### Solution 08-06.1

A NAND latch holds when both inputs are 1, sets when $\overline{S}$ = 0 and resets when $\overline{R}$ = 0.

(a) Step 1, $\overline{S}$ = 0: set, $Q$ = 1. Step 2: hold, 1. Step 3, $\overline{R}$ = 0: reset, 0. Step 4: hold, 0. Step 5, both 0: each NAND has a 0 input, so both outputs are 1: $Q = \overline{Q} = 1$.

(b) Steps 1, 2 and 5: **3**.

(c) Step 5: **1**. It is the NAND latch's forbidden state, the dual of the NOR latch's $S = R = 1$.

### Solution 08-06.2

Rising edges occur at $t$ = 1 and $t$ = 5.

| $t$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| CLK | 0 | 1 | 1 | 0 | 0 | 1 | 1 | 0 |
| $D$ | 1 | 1 | 0 | 0 | 1 | 0 | 1 | 0 |
| positive latch | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 1 |
| negative latch | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 0 |
| flip-flop | 0 | 1 | 1 | 1 | 1 | 0 | 0 | 0 |

- Positive latch: follows $D$ at $t$ = 1, 2, 5, 6 and holds otherwise: transitions at $t$ = 1, 2, 6: **3**, final **1**.
- Negative latch: follows $D$ at $t$ = 0, 3, 4, 7: transitions at $t$ = 0 (from the initial 0), 3, 4, 7: **4**, final **0**.
- Flip-flop: captures 1 at $t$ = 1 and 0 at $t$ = 5: **2** transitions, final **0**.

The three elements disagree on the final value, from the same inputs: the difference between level-sensitive and edge-triggered storage is not a detail.

### Solution 08-06.3

(a) Setup slack = time $D$ was stable before the edge minus the requirement: $25 - 30$ = **−5** ps.

(b) Hold slack = time $D$ stays stable after the edge minus the requirement: $20 - 15$ = **+5** ps.

(c) Setup is violated. The master latch closes while $D$ is still settling, so the flip-flop may capture the old value, the new value, or go metastable for a while before resolving ([08-10](../chapters/08-10-timing-metastability-cdc.md)).

### Solution 08-06.4

(a) The critical path is the slowest, 650 ps: $T_{c,\min} = 80 + 650 + 50$ = **780** ps, so $f_{\max}$ = **1.28** GHz.

(b) Slack $= 780 - (80 + t_{pd} + 50)$: **250** ps for the 400 ps path, **0** for the 650 ps path, **130** ps for the 520 ps path. Speeding up the two non-critical paths would not raise the clock frequency at all.

### Solution 08-06.5

(a) Hold slack $= 40 + t_{cd} - 70$: **−20**, **+5** and **+20** ps. **1** path violates (the one with 10 ps).

(b) It needs at least 20 ps more: $\lceil 20/12 \rceil$ = **2** buffers (24 ps, leaving +4 ps of slack).

### Solution 08-06.6

(a) $T_c = 1200 + 100 = 1300$ ps: **769** MHz.

(b) Each stage has 300 ps of logic: $T_c = 300 + 100 = 400$ ps: **2.5** GHz.

(c) $1300/400$ = **3.25** times the throughput, not 4: the overhead is paid in every stage.

(d) With $N$ stages, $T_c = 1200/N + 100$, so the speedup $1300/(1200/N + 100)$ approaches $1300/100$ = **13** as $N \to \infty$: the register overhead alone sets the limit, even before latency, power and hazards are considered ([14-06](../../14-computer-organization-and-architecture/chapters/14-06-pipelining-and-hazards.md)).

### Solution 08-06.7

(a) $Q_{\text{next}} = \text{EN}\cdot D + \overline{\text{EN}}\cdot Q$: a 2:1 multiplexer selecting between new data and the current value.

(b) $24 + 16$ = **40** transistors per bit.

(c) $32 \times 16$ = **512** multiplexer transistors. A clock-gating cell stops the clock to all 32 flip-flops when EN = 0, which also saves the clock power they would burn reloading their own values.

### Solution 08-06.8

(a) Synchronous: the reset is first sampled at the edge at **16** ns. Asynchronous: immediately, at **13** ns.

(b) The next edge after 29.5 ns is at 32 ns, **2.5** ns after the release. With a 1 ns recovery requirement the margin is **1.5** ns.

### Solution 08-06.9

(a) $T_{c,\min} = 5.2 + 3.5 + 3$ = **11.7** ns, $f_{\max}$ = **85.5** MHz.

(b) The gate's *minimum* (contamination) delay, together with the flip-flop's minimum clock-to-Q, is needed for the hold check $t_{ccq} + t_{cd} \ge t_{\text{hold}}$ = 1 ns. Maximum delays, which datasheets emphasize, say nothing about hold. Many logic datasheets give no minimum delay at all, in which case designers assume zero and check that the flip-flop's own minimum clock-to-Q covers the hold time.

### Solution 08-06.10

(a) With $\beta_n = \beta_p$, $\sqrt{\beta_n/\beta_p} = 1$: $V_M = (1.8 - 0.45 + 0.45)/2$ = **0.9** V, exactly half the supply, as symmetry demands.

(b) $\sqrt{4} = 2$: $V_M = (1.8 - 0.45 + 0.9)/3$ = **0.75** V.

(c) A stronger nMOS can match the pMOS's current with less gate drive, so the balance point moves **down**, toward ground. Designers size pMOS devices wider to pull $V_M$ back toward the middle, which equalizes noise margins and rise and fall delays ([19-01](../../19-digital-vlsi-design/chapters/19-01-cmos-inverter-static.md)).

### Solution 08-06.11

$t = \tau \ln(\Delta V/\Delta V_0) = 20\ \text{ps} \times \ln(0.9/0.001) = 20 \times 6.802$ = **136** ps.

From 1 µV: $20 \times \ln(900\,000) = 20 \times 13.71$ = **274** ps. Each factor of 1000 in the starting difference adds $\tau \ln 1000 = 138$ ps: the resolution time grows only logarithmically as the initial imbalance shrinks, but it grows without limit as $\Delta V_0 \to 0$. That unbounded tail is metastability ([08-10](../chapters/08-10-timing-metastability-cdc.md)).

### Solution 08-06.12

(a) Measured at the pins, the latch's window moves 25 ps later:

- setup: $20 - 25$ = **−5** ps;
- hold: $15 + 25$ = **40** ps;
- clock-to-Q: $45 + 25$ = **70** ps.

(b) Window width $= t_{\text{setup}} + t_{\text{hold}} = -5 + 40$ = **35** ps, the same as the latch's $20 + 15$.

(c) The master closes 25 ps after the pin's edge, but needs only 20 ps of setup before *that* moment, so $D$ may still change until 5 ps after the pin's edge. A negative setup time is no contradiction: setup and hold are just the edges of a window, measured from a reference that need not lie inside it.

### Solution 08-06.13

(a) Let the launching register's clock edge be at $t = 0$ and the receiving register's at $t_{\text{skew}}$ (and its next one at $T_c + t_{\text{skew}}$).

- Setup: new data arrives by $t_{pcq} + t_{pd}$ and must precede the receiving edge by $t_{\text{setup}}$: $t_{pcq} + t_{pd} + t_{\text{setup}} \le T_c + t_{\text{skew}}$.
- Hold: the receiving register needs its old data stable until $t_{\text{skew}} + t_{\text{hold}}$; new data can arrive as early as $t_{ccq} + t_{cd}$: $t_{ccq} + t_{cd} \ge t_{\text{hold}} + t_{\text{skew}}$.

(b) $T_{c,\min} = 50 + 300 + 40 - 30$ = **360** ps: $f_{\max}$ = **2.78** GHz, faster than the 390 ps without skew.

(c) Hold slack $= 30 + 40 - (60 + 30)$ = **−20** ps: the same path that met hold with 10 ps to spare without skew now fails. A late receiving clock gives the long path more time (helping setup) and gives the short path more time to corrupt the capture (hurting hold). Skew in the other direction does the reverse. [08-10](../chapters/08-10-timing-metastability-cdc.md) develops this.

### Solution 08-06.14

(a) Each latch: two transmission gates ($2 \times 2 = 4$) and two inverters ($2 \times 2 = 4$), 8 transistors; two latches, 16; one shared clock inverter, 2. Total **18**.

(b) The extra **6** transistors are, most likely, local clock buffering (generating both clock phases inside the cell, so the clock pin sees a single small load and the phases are clean) and an output buffer that isolates the storage node from whatever $Q$ drives. Both improve robustness: a flip-flop whose internal state could be disturbed by its own output load, or whose clock phases overlap, can fail. (This is an interpretation of a common design pattern; the cell's netlist, not its documentation, is the source here.)

### Solution 08-06.15

(a) Suppose the ring is at rest and one node rises. After 20 ps the next node falls, after 40 ps the third rises, and after 60 ps the change returns to the first node *inverted* (three inversions): it falls. Another 60 ps and it rises again. No consistent static state exists with an odd number of inversions, so the ring oscillates with period $2 \times 3 \times 20$ = **120** ps, frequency **8.33** GHz. Such ring oscillators are used deliberately to measure gate delay on test chips.

(b) Two inverters form the bistable latch of §3.1: no oscillation, a stored bit.

(c) Rule 2: every feedback loop must contain a register. A combinational loop either oscillates (odd inversions) or stores state (even inversions) with timing that no static analysis can check. With a flip-flop in the loop, the loop changes only at clock edges and its behavior is analyzed by the two constraints of §3.7.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 08-06.1a | steps with $Q$ = 1 | 3 | — |
| 08-06.1b | steps with both outputs 1 | 1 | — |
| 08-06.2a | positive latch transitions | 3 | — |
| 08-06.2b | positive latch final output | 1 | — |
| 08-06.2c | negative latch transitions | 4 | — |
| 08-06.2d | negative latch final output | 0 | — |
| 08-06.2e | flip-flop transitions | 2 | — |
| 08-06.2f | flip-flop final output | 0 | — |
| 08-06.3a | setup slack | -5 | ps |
| 08-06.3b | hold slack | 5 | ps |
| 08-06.4a | minimum clock period | 780 | ps |
| 08-06.4b | maximum frequency | 1.28 | GHz |
| 08-06.4c | slack of the 400 ps path | 250 | ps |
| 08-06.4d | slack of the 650 ps path | 0 | ps |
| 08-06.4e | slack of the 520 ps path | 130 | ps |
| 08-06.5a | hold slack, 10 ps path | -20 | ps |
| 08-06.5b | hold slack, 35 ps path | 5 | ps |
| 08-06.5c | hold slack, 50 ps path | 20 | ps |
| 08-06.5d | violating paths | 1 | — |
| 08-06.5e | buffers needed | 2 | — |
| 08-06.6a | one stage | 769 | MHz |
| 08-06.6b | four stages | 2.5 | GHz |
| 08-06.6c | speedup with four stages | 3.25 | — |
| 08-06.6d | limiting speedup | 13 | — |
| 08-06.7a | transistors per enabled bit | 40 | — |
| 08-06.7b | multiplexer transistors in a 32-bit register | 512 | — |
| 08-06.8a | synchronous reset takes effect | 16 | ns |
| 08-06.8b | asynchronous reset takes effect | 13 | ns |
| 08-06.8c | release-to-edge time | 2.5 | ns |
| 08-06.8d | recovery margin | 1.5 | ns |
| 08-06.9a | minimum period | 11.7 | ns |
| 08-06.9b | maximum frequency | 85.5 | MHz |
| 08-06.10a | $V_M$ with $\beta_n = \beta_p$ | 0.9 | V |
| 08-06.10b | $V_M$ with $\beta_n = 4\beta_p$ | 0.75 | V |
| 08-06.11a | time from 1 mV to 0.9 V | 136 | ps |
| 08-06.11b | time from 1 µV to 0.9 V | 274 | ps |
| 08-06.11c | added time per factor of 1000 | 138 | ps |
| 08-06.12a | flip-flop setup | -5 | ps |
| 08-06.12b | flip-flop hold | 40 | ps |
| 08-06.12c | flip-flop clock-to-Q | 70 | ps |
| 08-06.12d | capture-window width | 35 | ps |
| 08-06.13a | minimum period with skew | 360 | ps |
| 08-06.13b | maximum frequency with skew | 2.78 | GHz |
| 08-06.13c | hold slack with skew | -20 | ps |
| 08-06.14a | transistors, transmission-gate flip-flop | 18 | — |
| 08-06.14b | extra transistors in the SKY130 cell | 6 | — |
| 08-06.15a | ring-oscillator period | 120 | ps |
| 08-06.15b | ring-oscillator frequency | 8.33 | GHz |
