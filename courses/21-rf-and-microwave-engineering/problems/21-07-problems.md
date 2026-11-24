# Problems 21-07 · Power Amplifiers

Chapter: [21-07](../chapters/21-07-power-amplifiers.md) · Worked solutions: [21-07 solutions](../solutions/21-07-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Transistors are ideal current sources above the knee voltage $V_k$ and harmonics are shorted unless stated. $x$ is the output amplitude relative to its maximum, so the output power is $x^2$ of peak. "OFDM" means a complex-Gaussian signal whose stated PAPR is set at the PA's saturation, as in Example 21-07.5. Problems marked *(lab)* can be checked with `labs/21-07-lab/pa.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 21-07.1 [A]

**Drain efficiency against PAE.** A 28 GHz PA delivers 20 dBm with 8 dB of gain while drawing 250 mW from its supply. Find (a) its drain efficiency, (b) its input power and (c) its PAE. (d) What gain would bring PAE within one percentage point of the drain efficiency?

### Problem 21-07.2 [A]

**Load lines.** (a) What optimum load does a 2 W PA need from a 5 V supply with a 0.5 V knee? (b) What transformation ratio to 50 Ω is that, and (c) what L-match Q? (d) What load would 40 W need from 3.4 V with a 0.4 V knee, and (e) what transformation ratio?

### Problem 21-07.3 [A]

**Tuned class A and class B with a knee.** With $V_{DD}$ = 5 V and $V_k$ = 0.5 V, find the full-swing drain efficiency of (a) a tuned class-A stage and (b) a class-B stage.

### Problem 21-07.4 [B]

**Two more conduction angles.** *(lab)* For conduction angles of 300° and 150°, find (a, b) the full-swing efficiency, (c, d) the output power relative to class A at the same peak current, and (e, f) the optimum load in units of $V_{DD}/I_{max}$.

### Problem 21-07.5 [B]

**A class-E stage at 900 MHz.** Design an ideal class-E PA for 2 W from 5 V at 900 MHz: find (a) $R$, (b) the shunt capacitance, (c) the excess reactance and (d) its inductance, (e) the peak switch voltage, (f) the DC current and (g) the peak switch current. (h) If the transistor's breakdown is 12 V, what is the highest supply, and (i) how much power would the same $R$ then deliver?

### Problem 21-07.6 [B]

**An imperfect third-harmonic termination.** In the class-F3 amplifier of §3.3, the third-harmonic termination only reaches half the ideal voltage: $V_3 = V_1/18$. (a) Show that the drain voltage's minimum is still at θ = 0, and find the largest $V_1$ relative to $V_{DD}$. (b) What efficiency results?

### Problem 21-07.7 [B]

**Efficiency in back-off.** Find the efficiency of ideal class A, class B and a symmetric Doherty at (a–c) 3 dB, (d–f) 6 dB and (g–i) 10 dB output back-off.

### Problem 21-07.8 [B]

**The value of crest-factor reduction.** *(lab)* Crest-factor reduction lowers an OFDM signal's PAPR to 8 dB. Find the average efficiency of (a) class B and (b) a symmetric Doherty. For 10 W of average output, find the DC power of (c) class B and (d) the Doherty, and (e) the saving.

### Problem 21-07.9 [C]

**An asymmetric Doherty.** The auxiliary device delivers twice the main's peak current (γ = 2); $R_{opt}$ = 25 Ω for the main at 28 V. (a) What load and (b) what inverter impedance are needed? (c) What is the peak power? (d) At what back-off does the first efficiency peak occur, and (e) what power is that? (f) Derive the efficiency above the first peak, and find (g) the dip's location in $x$ and (h) its depth. (i) What is the average efficiency for the 9.64 dB-PAPR OFDM signal?

### Problem 21-07.10 [B]

**When is envelope tracking worth it?** For the 9.64 dB-PAPR OFDM signal, what supply-modulator efficiency makes a class-B ET transmitter match a symmetric Doherty (54.90%), (a) with a 20% supply floor and (b) with perfect tracking?

### Problem 21-07.11 [B]

**ACLR budget.** A PA's two-tone input IIP3 is +5 dBm. (a) What is the highest average input power of an OFDM signal for an ACLR of −38 dBc (the cubic model of §3.4)? For a 100 MHz channel, how wide is the spectrum of (b) the third-order and (c) the fifth-order distortion?

### Problem 21-07.12 [B]

**Third-order predistortion.** A PA follows $y = a_1u + a_3u\lvert u\rvert^2$ with $a_1$ = 10 and $a_3$ = −2 V⁻². (a) Find the predistorter coefficient $b_3$ that cancels the third-order term, and (b) the leading residual coefficient (of $x\lvert x\rvert^4$). At $\lvert x\rvert$ = 0.5, find (c) the original third-order term, (d) the residual and (e) the improvement in dB.

### Problem 21-07.13 [C]

**Clipping as crest-factor reduction.** An OFDM signal is hard-clipped 8 dB above its average power. Using 03-03's results, find (a) the clipping probability, and (b) the EVM caused by the clipping error, given that its power is −39.25 dB relative to the signal. (c) By how many percentage points does the lower PAPR raise a symmetric Doherty's average efficiency compared with 9.64 dB?

### Problem 21-07.14 [A]

**What PAE means for a battery.** A handset PA delivers 26 dBm with 28 dB of gain from a 3.8 V battery. Find (a) the output and (b) the input power, and the battery current at a PAE of (c) 40% and (d) 50%. (e) How much current does the better PA save?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Load line, matching, drain efficiency and PAE | 1, 2, 14 |
| 2. Conduction angle and classes E and F | 3, 4, 5, 6 |
| 3. Back-off and average efficiency | 7, 8, 13 |
| 4. Doherty and envelope tracking | 9, 10 |
| 5. ACLR, predistortion and crest-factor reduction | 11, 12, 13 |
| 6. Evaluating PA claims | 8, 14 |
