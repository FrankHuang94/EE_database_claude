# Problems 22-02 · Steady-State Analysis and the Buck Converter

Chapter: [22-02](../chapters/22-02-buck-converter-steady-state.md) · Worked solutions: [22-02 solutions](../solutions/22-02-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Synchronous bucks in continuous conduction unless stated. $\Delta$ means peak to peak. $D' = 1 - D$, $T_s = 1/f_s$, $K = 2L/(RT_s)$. Values marked "assumed" are illustrative. Problems marked *(lab)* can be checked with `labs/22-02-lab/buck.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 22-02.1 [A]

**Balance the volt-seconds.** A buck runs from 24 V at $D$ = 0.25 and delivers 3 A. (a) Use volt-second balance to find the output voltage. (b) Use charge balance and the input current's waveform to find the average input current, and check the power balance.

### Problem 22-02.2 [A]

**Ripples at 2 MHz.** A phone's buck converts 5.0 V to 1.8 V at 2 A, switching at 2 MHz with a 1 µH inductor and 22 µF of effective output capacitance. Find (a) the duty cycle, (b) the inductor ripple, (c) the ripple ratio, (d) the peak inductor current and (e) the output ripple.

### Problem 22-02.3 [A]

**RMS currents.** *(lab)* For Problem 22-02.2's converter, find the RMS currents in (a) the inductor, (b) the high-side switch, (c) the low-side switch, (d) the input capacitor and (e) the output capacitor.

### Problem 22-02.4 [B]

**When ESR dominates.** A buck at 100 kHz with 2 A of inductor ripple uses a 220 µF electrolytic capacitor with 30 mΩ of ESR. Find (a) the capacitive ripple, (b) the ESR ripple and (c) their conservative sum. (d) What ESR would meet a 20 mV total?

### Problem 22-02.5 [B]

**Conduction losses.** A 5 V to 1.0 V buck delivers 6 A through a 20 mΩ high-side switch, a 10 mΩ low-side switch and a 5 mΩ inductor. Find (a) the duty cycle that holds 1.0 V, (b) $R_{eq}$, (c) the conduction loss and (d) the conduction-limited efficiency.

### Problem 22-02.6 [B]

**Diode or synchronous?** A 12 V to 5 V buck delivers 3 A. Compare a 0.45 V diode with a 15 mΩ synchronous switch in the low-side position, ignoring other losses. Find (a) the duty cycle with the diode, (b) the diode's loss, (c) the synchronous switch's loss at $D$ = 5/12, (d) their ratio and (e, f) each as a percentage of the output power.

### Problem 22-02.7 [B]

**Where DCM begins.** A 24 V to 5 V buck switches at 300 kHz with a 22 µH inductor. Find (a) the inductor ripple and (b) the critical load current. At a 50 Ω load, find (c) $K$, (d) $K_{crit}$ and so the mode.

### Problem 22-02.8 [B]

**The DCM ratio.** For Problem 22-02.7's converter at the 50 Ω load, find (a) the conversion ratio if the duty cycle stays at the CCM value 5/24 (open loop), and (b) the output voltage that would result. (c) What duty cycle $D_1$ restores 5 V?

### Problem 22-02.9 [B]

**A PFM pulse.** A PFM buck applies a fixed 200 ns on-time to convert 4.0 V to 1.2 V with a 1 µH inductor. Find (a) the peak current, (b) the off-time, (c) the charge per pulse and (d) the pulse rate at 10 mA. (e) At what load do the pulses touch end to end, and what is the pulse rate there?

### Problem 22-02.10 [B]

**Two forms of one boundary.** (a) Show that $I < I_{crit}$ and $K < 1 - D$ are the same condition. (b) For Problem 22-02.7's converter, find the load resistance at the boundary and (c) confirm that $K$ there equals $1 - D$.

### Problem 22-02.11 [B]

**Minimum on-time.** A controller's minimum on-time is 50 ns (assumed). (a) What is the highest switching frequency for 20 V to 0.9 V? (b) If the design keeps a 20% margin on on-time (at least 60 ns), what is the limit?

### Problem 22-02.12 [C]

**A complete power-stage design.** Design a buck for 3.3 V at 5 A from 12 V ± 10%, switching at 1 MHz, with a 30% ripple ratio at the highest input, 15 mV of capacitive ripple and 5 mV of ESR ripple, using ceramic capacitors that lose 40% at bias. Find (a) the smallest duty cycle, (b) the inductance, (c) the peak current, (d) the effective and (e) the nominal output capacitance, (f) the ESR budget, (g) the worst-case input-capacitor RMS current and the input voltage at which it occurs, and (h) the smallest on-time.

### Problem 22-02.13 [C]

**A buck from a Li-ion cell, and its dropout.** A 3.3 V rail at 0.3 A runs from a Li-ion cell (4.2 V full) through a buck whose switch and inductor resistances total 0.3 Ω (assumed). Find (a) the duty cycle at 4.2 V, (b) the lowest cell voltage at which it still regulates in 100% mode, and (c) the voltage drop across the converter below that.

### Problem 22-02.14 [C]

**Heating the input capacitors.** A 12 V to 6 V buck delivers 10 A, the worst duty cycle for its input capacitors. Four identical ceramic capacitors, each with 5 mΩ of ESR, share the input current. Find (a) the total RMS input-capacitor current, (b) the RMS current per capacitor, (c) the total heat in the bank and (d) the heat per capacitor.

### Problem 22-02.15 [C]

**Why not minimize the inductor?** (a) Show that, for a fixed $V$, $D$, $f_s$ and $I$, the inductor's peak stored energy $\tfrac12LI_{pk}^2$ is proportional to $g(r) = (1 + r/2)^2/r$, where $r$ is the ripple ratio. (b) Show that $g$ is smallest at $r$ = 2, the CCM–DCM boundary. Find (c) $g(0.3)$, (d) $g(2)$ and (e) the ratio of stored energy at $r$ = 0.3 to that at $r$ = 2. (f) Give two reasons designers nonetheless choose $r$ of 0.2–0.4.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Volt-second and charge balance, small-ripple approximation | 1, 10 |
| 2. Ripples, ESR and RMS currents | 2, 3, 4, 14 |
| 3. Conduction losses and synchronous rectification | 5, 6 |
| 4. CCM/DCM boundary, DCM ratio and PFM | 7, 8, 9, 10 |
| 5. Power-stage design: frequency, L, C, on-time, dropout, derating | 11, 12, 13, 15 |
