# Problems 21-02 · Impedance Matching Networks

Chapter: [21-02](../chapters/21-02-impedance-matching-networks.md) · Worked solutions: [21-02 solutions](../solutions/21-02-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Sources are 50 Ω unless stated; "bandwidth" is the 10 dB return-loss band. Problems marked *(lab)* can be checked with `labs/21-02-lab/match.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 21-02.1 [A]

**A gentle match.** Design a low-pass L-network that matches 25 Ω to 50 Ω at 1 GHz: give Q, the reactance and susceptance, and L and C.

### Problem 21-02.2 [A]

**High-pass instead.** Give the high-pass version of Example 21-02.1 (10 Ω to 50 Ω at 2.4 GHz): a series capacitor by the load and a shunt inductor at the 50 Ω side.

### Problem 21-02.3 [B] *(lab)*

**An inductive load.** A load of 30 + j10 Ω at 2 GHz is matched to 50 Ω with a series inductor by the load and a shunt capacitor at the 50 Ω side. Find Q, the added series reactance, L and C.

### Problem 21-02.4 [B] *(lab)*

**Wrong sign to absorb.** A load is 100 Ω in parallel with 2 pF at 1 GHz. A low-pass match would need a shunt capacitance at the load smaller than the 2 pF already there. Design a high-pass match instead (shunt inductor at the load, series capacitor at the 50 Ω side), absorbing the load capacitance into the inductor.

### Problem 21-02.5 [B] *(lab)*

**A π network.** Design a π network with loaded Q = 4 between a 50 Ω source and a 25 Ω load: find the virtual resistance, both shunt susceptances and the series reactance.

### Problem 21-02.6 [B]

**Three steps.** A 2 Ω power-amplifier load is matched to 50 Ω with three L-sections in geometric progression. Find the intermediate resistances and the Q of each section.

### Problem 21-02.7 [B] *(lab)*

**A three-section transformer.** Design a three-section binomial quarter-wave transformer from 50 Ω to 25 Ω and find its fractional bandwidth for $\lvert\Gamma\rvert \le 0.05$.

### Problem 21-02.8 [A]

**Loss.** Estimate the inductor's insertion loss for a $Q_n$ = 1 match and for a $Q_n$ = 5 match, both with $Q_u$ = 10.

### Problem 21-02.9 [B]

**A power-amplifier load line.** A handset PA swings from a 3.4 V supply with a 0.4 V knee and delivers 2 W, so it needs $R_{opt} = (V_{DD} - V_k)^2/(2P)$. Find $R_{opt}$, the transformation ratio to 50 Ω, the Q of one and of two L-sections, and the total inductor loss for each with $Q_u$ = 30.

### Problem 21-02.10 [B]

**Bode–Fano for an antenna model.** Model a small antenna as 50 Ω in parallel with 3 pF. What is the widest band it can be matched over with 10 dB return loss, and with 20 dB?

### Problem 21-02.11 [C] *(lab)*

**A π band-pass between equal resistances.** Design a π network with Q = 3 between 50 Ω and 50 Ω at 2.4 GHz (a harmonic filter that also "matches" 50 Ω to itself). Find $R_v$, the element values in pF and nH, and its 10 dB return-loss bandwidth by simulation.

### Problem 21-02.12 [C]

**How many sections?** Match 2 Ω to 50 Ω with $n$ = 1 to 4 geometric L-sections, each inductor with $Q_u$ = 20. Find the total inductor loss for each $n$ and the best choice. Why does loss not keep falling as $n$ grows?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Complex loads | 3, 4 |
| 2. π and T networks and Q | 5, 11 |
| 3. Wideband: sections and transformers | 6, 7, 12 |
| 4. Loss from component Q | 8, 9, 12 |
| 5. Bode–Fano limit | 10 |
| L-network basics | 1, 2 |
