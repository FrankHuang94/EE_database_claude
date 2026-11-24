# Solutions 19-08 · SRAM Design

Problems: [19-08 problem set](../problems/19-08-problems.md) · Chapter: [19-08](../chapters/19-08-sram-design.md). Every number below is recomputed by [verify_19_08.py](../verify/verify_19_08.py).

---

## Solutions

### Solution 19-08.1

Take the cell during the read, with Q pulled slightly up (0.128 V for the chapter's cell) and QB, BL and BLB at $V_{DD}$:

| Device | Gate drive | Drain–source voltage | State |
|---|---|---|---|
| Q-side access | $V_{GS} = V_{DD} - Q$ | $V_{DD} - Q > 0$ | on, carries the read current |
| Q-side pull-down | $V_{GS} = V_{DD}$ (gate QB) | $Q > 0$ | on, carries the read current |
| QB-side pull-up | $V_{SG} = V_{DD} - Q$ | 0 | channel on, no current |
| QB-side access | $V_{GS} = 0$ (gate, drain and source all at $V_{DD}$) | 0 | off |
| Q-side pull-up | $V_{SG} = 0$ (gate QB) | | off |
| QB-side pull-down | $V_{GS} = Q < V_{TN}$ | | off |

So **2** transistors carry current and **3** have channels on. BL discharges through the Q-side access transistor and pull-down; BLB stays high because QB is already at $V_{DD}$, so its access transistor has no gate drive. An 8T cell has **8** transistors: the extra two form a read port (a transistor gated by the storage node in series with one gated by a read wordline) that discharges a separate read bitline without touching the storage nodes.

### Solution 19-08.2

(a) $2^{18} \times 0.0175\ \mu\text{m}^2$ = **0.00459** mm². (b) $2^{18}/(38 \times 10^6\ \text{bits/mm}^2)$ = **0.00690** mm², half again the cell area.

### Solution 19-08.3

$C_{BL} = 128 \times 0.1 + 10$ = **22.8** fF; $t = 22.8\ \text{fF} \times 0.08\ \text{V}/15\ \mu\text{A}$ = **121.6** ps.

### Solution 19-08.4

Solving §3.2's balance at 0.8 V: $\Delta V$ = **0.113** V, a margin of **0.187** V to $V_{TH}$. The disturbance falls with the supply, but so does the other inverter's switching threshold and, more importantly, the lobes of the butterfly (Problem 9).

### Solution 19-08.5

Set $\Delta V$ = 0.1 V in §3.2: $CR = \tfrac12(1.0 - 0.1 - 0.3)^2/[(0.7)(0.1) - 0.005] = 0.18/0.065$ = **2.77**.

### Solution 19-08.6

Set $V = V_{TH}$ = 0.3 V in §3.3: $PR = 2[(0.7)(0.3) - 0.045]/0.49 = 0.33/0.49$ = **0.673**. With the cell ratio of Problem 5, the three strengths must satisfy $k_P \le 0.673k_A$ and $k_N \ge 2.77k_A$.

### Solution 19-08.7

(a) $Q(5.5)$ = **1.90 × 10⁻⁸**; expected failures $2^{24} \times 1.90 \times 10^{-8}$ = **0.319**; yield $e^{-0.319}$ = **72.7** %.

(b) With up to 4 repairs, the Poisson probability of at most 4 failures is **99.998** %. A handful of spares turns a poor yield into a near-perfect one.

### Solution 19-08.8

(a) $6 \times 10$ = **60** mV, taking $35.5\ \text{fF} \times 0.06/20\ \mu\text{A}$ = **106.5** ps.

(b) $15 \times \ln(1/0.06)$ = **42.2** ps. Lowering the offset (larger, better-matched sense transistors, or offset cancellation) shortens the bitline time directly.

### Solution 19-08.9

| $V_{DD}$ | Hold SNM | Read SNM |
|---|---|---|
| 1.0 V | **0.397** V | **0.226** V |
| 0.8 V | **0.348** V | **0.204** V |
| 0.6 V | **0.300** V | **0.176** V |

The 0.6 V row is optimistic: at $V_{DD} = 2V_{TH}$ the square-law inverter becomes an ideal step, so its hold SNM is exactly $V_{DD}/2$; real cells keep conducting below threshold and lose margin faster. Both margins shrink with the supply while threshold variation, a fixed number of millivolts, does not; the read margin, smallest to begin with, runs out first in the worst cells of a large array. This is why SRAM sets $V_{min}$ and why separate rails and assists exist (§3.8).

### Solution 19-08.10

$e^{-2^{30}Q(z)} = 0.99$ requires $Q(z) = -\ln 0.99/2^{30}$ = **9.36 × 10⁻¹²**, so $z$ = **6.72**: a gigabit needs nearly seven σ of margin without repair, which is why large memories rely on redundancy and ECC.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 19-08.1a | transistors carrying current during the read | 2 | — |
| 19-08.1c | transistors with channels on during the read | 3 | — |
| 19-08.1b | transistors in an 8T cell | 8 | — |
| 19-08.2a | cell area | 0.00459 | mm² |
| 19-08.2b | macro area at 38 Mb/mm² | 0.00690 | mm² |
| 19-08.3a | bitline capacitance | 22.8 | fF |
| 19-08.3b | time for 80 mV | 121.6 | ps |
| 19-08.4a | read disturbance at 0.8 V | 0.113 | V |
| 19-08.4b | margin to VT | 0.187 | V |
| 19-08.5a | cell ratio for 0.1 V | 2.77 | — |
| 19-08.6a | largest pull-up ratio | 0.673 | — |
| 19-08.7a | Q(5.5) | 1.90e-8 | — |
| 19-08.7b | expected failures | 0.319 | — |
| 19-08.7c | yield without repair | 72.7 | % |
| 19-08.7d | yield with 4 repairs | 99.998 | % |
| 19-08.8a | required swing | 60 | mV |
| 19-08.8b | bitline time | 106.5 | ps |
| 19-08.8c | sense time | 42.2 | ps |
| 19-08.9a | hold SNM at 1.0 V | 0.397 | V |
| 19-08.9b | read SNM at 1.0 V | 0.226 | V |
| 19-08.9c | hold SNM at 0.8 V | 0.348 | V |
| 19-08.9d | read SNM at 0.8 V | 0.204 | V |
| 19-08.9e | hold SNM at 0.6 V | 0.300 | V |
| 19-08.9f | read SNM at 0.6 V | 0.176 | V |
| 19-08.10a | required tail probability | 9.36e-12 | — |
| 19-08.10b | required margin | 6.72 | sigma |
