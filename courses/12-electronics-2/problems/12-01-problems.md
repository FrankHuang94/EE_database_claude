# Problems 12-01 · Differential Pairs

Chapter: [12-01](../chapters/12-01-differential-pairs.md) · Worked solutions: [12-01 solutions](../solutions/12-01-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** Course 10's: $V_T$ = 25.852 mV; MOS square law with $k_n = \mu_nC_{ox}W/L$, $V_{TN}$ = 0.5 V, λ = 0 unless stated; BJT $g_m = I_C/V_T$, α = 1 unless stated. "Differential output" is $v_{o1} - v_{o2}$.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 12-01.1 [A]

**BJT pair gains.** A BJT pair has $I_{EE}$ = 2 mA and $R_C$ = 2 kΩ, with β = 100. Find each transistor's $g_m$, the differential-output and single-ended differential gains, and the differential input resistance.

### Problem 12-01.2 [A]

**MOS pair basics.** An NMOS pair has $k_n$ = 1 mA/V² and $I_{SS}$ = 100 µA. Find $V_{ov}$, $g_m$ and the input that switches it fully.

### Problem 12-01.3 [A]

**A BJT split.** For a BJT pair with $I_{EE}$ = 1 mA, find $i_{C1}$ at $v_{id}$ = 25 mV.

### Problem 12-01.4 [A]

**Tail-limited CMRR.** A pair has $g_m$ = 1 mA/V per transistor and a tail with $R_{SS}$ = 100 kΩ. Find its single-ended CMRR, as a ratio and in decibels.

### Problem 12-01.5 [B]

**A MOS split.** For the pair of Problem 12-01.2, find the drain currents at $v_{id}$ = 0.1 V.

### Problem 12-01.6 [B]

**Common-mode range.** An NMOS pair on $V_{DD}$ = 3.3 V has $I_{SS}$ = 400 µA, $k_n$ = 4 mA/V², $R_D$ = 5 kΩ, and a tail needing 0.25 V. Find $V_{ov}$ and the input common-mode range.

### Problem 12-01.7 [B]

**Adding offsets.** A MOS pair with $V_{ov}$ = 0.2 V has load resistors mismatched by 2% and a threshold mismatch of 1.5 mV. (a) Find the offset from the loads. (b) Find the total if both push the same way. (c) If instead both are independent random variables with these values as standard deviations, find σ of the total.

### Problem 12-01.8 [B]

**Bipolar offset and drift.** A bipolar pair's $I_S$ values differ by 5%. Find the offset exactly and with the linear approximation, and its drift at 300 K.

### Problem 12-01.9 [B]

**CMRR from $g_m$ mismatch.** A pair with $g_m$ = 1 mA/V, $R_D$ = 10 kΩ and $R_{SS}$ = 100 kΩ has a 1% transconductance mismatch and perfectly matched loads. Derive the common-mode-to-differential gain and find the differential CMRR.

### Problem 12-01.10 [B]

**Degeneration.** A BJT pair with $I_{EE}$ = 1 mA gets 500 Ω emitter resistors in each emitter. Find the effective transconductance per side, $1/(R_E + 1/g_m)$, and compare with the undegenerated $g_m$.

### Problem 12-01.11 [B]

**Sizing for offset.** With $A_{VT}$ = 3.5 mV·µm, what gate area gives σ(ΔV_TN) = 0.5 mV? With $L$ = 1 µm and $C_{ox}$ = 10 fF/µm², estimate each device's gate–source capacitance ($\tfrac23WLC_{ox}$).

### Problem 12-01.12 [C]

**How linear is a MOS pair?** Show that $i_{D1} - i_{D2} = g_mv_{id}\sqrt{1 - v_{id}^2/(4V_{ov}^2)}$. Find the input at which the current difference is 1% below the linear value, as a fraction of $V_{ov}$ and in millivolts for $V_{ov}$ = 0.3162 V, and compare with a BJT pair.

### Problem 12-01.13 [C]

**A CML stage for 50 Ω.** Design a CML buffer with 50 Ω loads and a 300 mV single-ended swing: find $I_{SS}$, $V_{ov}$ with $k_n$ = 150 mA/V², the full-switching input, the output pole with 200 fF per side, and the power from a 1.0 V supply.

### Problem 12-01.14 [C]

**Offset yield.** The offset of Example 12-01.4 is normally distributed with σ = 2.086 mV and zero mean. What fraction of parts meets $\lvert V_{OS}\rvert$ < 5 mV?

---

## Objective coverage

| Learning objective (chapter 12-01) | Problems |
|---|---|
| 1. Large-signal transfer and ranges | 2, 3, 5, 12 |
| 2. Half-circuits, gains and CMRR | 1, 4, 9, 10 |
| 3. Common-mode range and swing | 6 |
| 4. Offset and Pelgrom | 7, 8, 11, 14 |
| 5. Roles: op-amp input, comparator, CML | 13 |
