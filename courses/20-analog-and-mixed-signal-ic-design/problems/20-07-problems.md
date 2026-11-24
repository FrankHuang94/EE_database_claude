# Problems 20-07 · Nyquist ADCs: Flash, SAR and Pipeline

Chapter: [20-07](../chapters/20-07-nyquist-adcs.md) · Worked solutions: [20-07 solutions](../solutions/20-07-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Energies in $C_uV_{REF}^2$ for differential arrays (§3.2's formulas). 1.5-bit stages have thresholds at $\pm V_{REF}/4$ and residue $2v - DV_{REF}$. $kT$ = 4.1419 × 10⁻²¹ J. Two-channel interleaving spurs: offset $\Delta o^2/(2A^2)$, gain $(\alpha/2)^2$, skew $(\pi f_{in}\Delta t)^2$ relative to the signal. Problems marked *(lab)* can be checked with `labs/20-07-lab/nyq.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 20-07.1 [A]

**Flash counts.** How many comparators do 5-, 7- and 9-bit flash ADCs need? By what factor does the comparator count grow per bit?

### Problem 20-07.2 [A] *(lab)*

**A bubble.** A 3-bit flash produces the thermometer code 1110100 (comparator 1 first). What do a ones-counting encoder and a first-transition encoder output?

### Problem 20-07.3 [B]

**A 5-bit SAR.** Trace a 5-bit charge-redistribution SAR ($V_{REF}$ = 1 V) converting 0.73 V: give $v_x$ after each trial and the final code.

### Problem 20-07.4 [B]

**Switching energy across resolution.** Using §3.2's formulas, find the conventional and monotonic switching energies for 8 and 12 bits and the saving in each case.

### Problem 20-07.5 [B]

**DAC settling budget.** A synchronous 12-bit SAR at 100 MS/s spends 3 ns tracking and divides the remaining 7 ns equally among 12 decisions. What is the time per decision, and the largest DAC time constant that settles a full-scale step to half an LSB within it?

### Problem 20-07.6 [B]

**Redundancy margins.** For the weights 480, 256, 128, 64, 32, 32, 16, 8, 4, 2, 1, find the margin $m_k$ of every decision. Which decisions have no margin, and why does that not matter?

### Problem 20-07.7 [B]

**Through a pipeline.** Trace $v_{in}$ = 0.62 V ($V_{REF}$ = 1 V) through three 1.5-bit stages: give each $D$ and residue.

### Problem 20-07.8 [B]

**Op-amp gain for 14 bits.** A 14-bit pipeline's first stage has β = 0.4. What op-amp gain does it need, in V/V and dB?

### Problem 20-07.9 [A]

**Offset tolerance.** With $V_{REF}$ = 0.5 V, how much comparator offset can a 1.5-bit stage tolerate? How much can a 1-bit stage (one comparator at 0, residue $2v - DV_{REF}$ with $D = \pm1$) tolerate, and why?

### Problem 20-07.10 [B]

**Noise of three stages.** With $C_1$ = 1 pF and stage gains of 2, find the input-referred kT/C noise (µV rms) for stage capacitors 1, 0.5, 0.25 pF and for 1, 1, 1 pF, and the noise of the first stage alone.

### Problem 20-07.11 [A]

**Offset spur.** A two-channel interleaved ADC has a 2 mV offset difference and a 0.5 V-amplitude input. Find the spur's level and frequency.

### Problem 20-07.12 [B]

**A 10 GS/s target.** A two-channel interleaved 10 GS/s ADC must keep interleaving spurs at −50 dBc for inputs up to 5 GHz. Find the allowed gain mismatch and timing skew.

### Problem 20-07.13 [C]

**Choosing by figure of merit.** Estimate the power of (a) a 14-bit, 100 MS/s Nyquist ADC with 80 dB SNDR built at a Schreier figure of 180 dB, and (b) an 8-bit, 20 GS/s ADC with 45 dB SNDR at 150 dB. Which architectures (§9) would you expect for each?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Flash, SAR and pipeline trade-offs | 1, 2, 13 |
| 2. SAR operation and switching energy | 3, 4, 5 |
| 3. Redundancy | 6, 9 |
| 4. Pipeline residue, gain and noise | 7, 8, 10 |
| 5. Interleaving spurs | 11, 12 |
| 6. Architecture choice | 13 |
