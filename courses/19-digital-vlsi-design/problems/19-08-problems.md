# Problems 19-08 · SRAM Design

Chapter: [19-08](../chapters/19-08-sram-design.md) · Worked solutions: [19-08 solutions](../solutions/19-08-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Square-law transistors with λ = 0; $V_{TN} = \lvert V_{TP}\rvert = V_T$. Access, pull-down and pull-up strengths $k_A$, $k_N$, $k_P$; cell ratio $CR = k_N/k_A$, pull-up ratio $PR = k_P/k_A$. Conservative criteria: read disturbance below $V_T$; write level below $V_T$. $Q(z)$ is the standard normal tail; array yield without repair is $e^{-NQ}$. Problems marked *(lab)* can be checked with `labs/19-08-lab/sram.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 19-08.1 [A]

**Who conducts?** A 6T cell stores 0 at Q and 1 at QB and is being read with both bitlines precharged high. Which of its six transistors conduct, and which bitline discharges? How many transistors does an 8T cell have, and what do the extra two do?

### Problem 19-08.2 [A]

**Area.** A 256 Kib array (2¹⁸ bits) uses 0.0175 µm² cells. (a) What area do the cells take? (b) What would the macro occupy at 38 Mb/mm²?

### Problem 19-08.3 [A]

**Bitline time.** A bitline serves 128 cells at 0.1 fF each plus 10 fF of wire; the cell current is 15 µA. How long does an 80 mV swing take?

### Problem 19-08.4 [B]

**Read disturb at a lower supply.** For $V_{DD}$ = 0.8 V, $V_T$ = 0.3 V and $CR$ = 1.5, find the read disturbance and its margin to $V_T$.

### Problem 19-08.5 [B]

**Choosing the cell ratio.** With $V_{DD}$ = 1.0 V and $V_T$ = 0.3 V, what cell ratio limits the read disturbance to 0.1 V?

### Problem 19-08.6 [B]

**Choosing the pull-up ratio.** With $V_{DD}$ = 1.0 V and $V_T$ = 0.3 V, what is the largest pull-up ratio that still writes the node below $V_T$?

### Problem 19-08.7 [B] *(lab)*

**Yield with a little repair.** A 16 Mib array (2²⁴ cells) has 5.5σ of margin. (a) Find the failure probability per cell, the expected failures and the yield without repair. (b) What is the yield if up to 4 failing cells can be repaired?

### Problem 19-08.8 [B]

**Sense-amplifier offset.** A sense amplifier's offset has a standard deviation of 10 mV, and the design requires 6σ. (a) What bitline swing is needed, and how long does it take with Example 19-08.4's bitline (35.5 fF, 20 µA)? (b) How long does the amplifier (τ = 15 ps) take to reach 1.0 V from that swing?

### Problem 19-08.9 [C] *(lab)*

**SNM against supply.** For the cell of Example 19-08.6 ($V_T$ = 0.3 V, $k_N$ = 200, $k_P$ = 100, $k_A$ = 100 µA/V²), compute the hold and read SNM at 1.0, 0.8 and 0.6 V, and explain why SRAM limits the minimum supply.

### Problem 19-08.10 [C]

**Margin for a gigabit.** What margin, in σ, does a 1 Gib array (2³⁰ cells) need for 99% yield without repair?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Cell operation, read disturb and write level | 1, 4, 5, 6 |
| 2. Static noise margin | 9 |
| 3. Bitlines and sense amplifiers | 3, 8 |
| 4. Area, density and yield | 2, 7, 10 |
| 5. Minimum voltage and its remedies | 4, 9 |
