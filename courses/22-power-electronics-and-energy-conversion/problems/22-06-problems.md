# Problems 22-06 · Converter Losses and Wide-Bandgap Switches

Chapter: [22-06](../chapters/22-06-converter-losses-and-wide-bandgap.md) · Worked solutions: [22-06 solutions](../solutions/22-06-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Device values are the chapter's data-sheet typicals unless stated. Values marked "assumed" are illustrative. Problems marked *(lab)* can be checked with `labs/22-06-lab/losses.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 22-06.1 [A]

**Gate drive for a SiC MOSFET.** The 650 V SiC MOSFET has $Q_g$ = 22 nC and is driven from 18 V. Find its gate-drive power at (a) 100 kHz and (b) 500 kHz.

### Problem 22-06.2 [A]

**Overlap at 1 MHz.** A 48 V converter hard-switches 15 A with a 4 ns turn-on and a 6 ns turn-off transition at 1 MHz. Find the overlap loss.

### Problem 22-06.3 [A]

**A linear output capacitance.** A switch has a constant 100 pF output capacitance. At 400 V, find (a) $Q_{oss}$, (b) $E_{oss}$ and (c) the hard turn-on loss per transition in a half bridge.

### Problem 22-06.4 [B]

**Overshoot from loop inductance.** A 48 V half bridge with 100 V switches has a 1.5 nH commutation loop and turns 30 A off in 3 ns. Find (a) the overshoot, (b) the peak drain voltage and (c) the margin to 100 V. (d) What loop inductance keeps the overshoot to 20 V if the current falls in 1.5 ns?

### Problem 22-06.5 [B]

**Dead-time loss with a SiC body diode.** *(lab)* A SiC half bridge carries 20 A through its 4.3 V body diode during each of two dead times per cycle at 100 kHz. Find the loss with dead times of (a) 100 ns and (b) 30 ns.

### Problem 22-06.6 [B]

**Sizing for output-charge loss.** *(lab)* For the 100 V GaN technology, find (a) $R_{DS(on)} \times Q_{oss}$. A high-side switch carries 10 A RMS and hard-switches its $Q_{oss}$ at 48 V and 1 MHz. Treating the loss as $I^2R + Q_{oss}Vf_s$ with $Q_{oss} = (RQ_{oss})/R$, find (b) the optimal on-resistance and (c) the minimum loss.

### Problem 22-06.7 [B]

**A hot SiC MOSFET.** *(lab)* The 650 V SiC MOSFET has 50 mΩ at 25 °C and 82 mΩ at 175 °C (assume linear). It carries 10 A RMS with 15 K/W to a 50 °C ambient (assumed). Find (a) the resistance slope, (b) the junction temperature, (c) the hot resistance, (d) the loss and (e) the runaway current.

### Problem 22-06.8 [B]

**Recovery in a CCM boost.** A 400 V CCM boost at 65 kHz uses the superjunction body diode (3.6 µC) as its rectifier, hard-commutated each cycle. Find (a) the recovery loss. (b) A SiC Schottky diode has no recovery but 30 nC of capacitive charge (assumed). Estimate the corresponding loss.

### Problem 22-06.9 [B]

**Baliga's figure of merit from material constants.** Using $\varepsilon_r$, $\mu$ and $\mathcal{E}_c$ of Si (11.9, 1240 cm²/V·s, 0.3 MV/cm), 4H-SiC (9.7, 980, 3.1) and GaN (10.4, 1000, 4.9), find the figure of merit $\varepsilon\mu\mathcal{E}_c^3$ relative to Si for (a) SiC and (b) GaN. (c) By what factor is SiC's minimum specific on-resistance lower than Si's at the same blocking voltage? (d, e) What ratios do the tabulated figures of merit cited in the chapter give for SiC and GaN, and why do they differ from yours?

### Problem 22-06.10 [C]

**ZVS in a point-of-load buck.** A 48 V GaN buck wants ZVS of its high-side switch by letting the inductor current go negative before each turn-on. With $Q_{oss}$ = 43 nC per switch (take it at 48 V), find the negative current needed for dead times of (a) 5 ns, (b) 10 ns and (c) 20 ns. What does this tell you about ZVS at this voltage?

### Problem 22-06.11 [C]

**A full-bridge LLC at 500 kHz.** A full-bridge LLC from 400 V uses GaN switches ($C_{o(tr)}$ = 88 pF) with a 30 ns dead time. Each leg's switch node must swing in the dead time. The primary sees $\pm V$, so $I_{m,pk} = V/(4L_mf_s)$. Find (a) the minimum switching current, (b) the largest $L_m$ and (c) the RMS magnetizing current at that limit.

### Problem 22-06.12 [C]

**Where silicon and GaN reach 2% loss.** *(lab)* In Example 22-06.6, the conduction loss is fixed and every other loss is proportional to $f_s$. Find the switching-loss slope (W per MHz) for (a) silicon and (b) GaN, and the frequency at which each converter's switch loss reaches 2% of 240 W: (c) silicon and (d) GaN. (e) What is the ratio of the two frequencies?

### Problem 22-06.13 [C]

**The energy condition for ZVS, derived.** During a dead time, an inductance $L$ swings a half bridge's switch node from $V$ to 0. Its current $i$ flows out of the node, and its far end is held at a fixed potential $V_x$. The two switches are identical, with output charge $Q_{oss}$ and stored energy $E_{oss}$ at $V$; their capacitance may be nonlinear. Neglect losses during the swing.

(a) Using energy conservation over the swing, show that $\tfrac12L(I_0^2 - I_1^2) = Q_{oss}(2V_x - V)$, where $I_0$ and $I_1$ are the inductor currents at the start and end of the swing.

(b) Show that the current is never smaller than the lesser of $I_0$ and $I_1$, so the swing completes whenever $I_1 \ge 0$. Hence write the smallest starting current when $V_x = V$, and show that when $V_x \le V/2$ there is no energy limit at all, only the timing condition of §3.7.

A phase-shifted full bridge at 400 V has a 4 µH leakage inductance whose far end sits at the rail the node is leaving. For the GaN switch ($C_{o(tr)}$ = 88 pF), find (c) the output charge and (d) the smallest starting current; then (e) and (f) the same for the superjunction switch ($C_{o(tr)}$ = 1212 pF, $C_{o(er)}$ = 117 pF). (g) What current would the rule $\tfrac12LI^2 \ge 2E_{oss}$ give for the superjunction switch, and (h) by what factor does that understate the true requirement?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Itemize and derive the losses | 1, 2, 4, 5, 8, 12 |
| 2. $Q_{oss}V$ against $E_{oss}$; device comparison | 3, 8, 13 |
| 3. Device-size optimum and figures of merit | 6, 9 |
| 4. Junction temperature and runaway | 7 |
| 5. ZVS and the LLC | 10, 11, 13 |
| 6. Si, SiC and GaN | 8, 9, 12 |
