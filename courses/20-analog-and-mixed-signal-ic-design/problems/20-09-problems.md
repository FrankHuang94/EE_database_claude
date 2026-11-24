# Problems 20-09 · DACs

Chapter: [20-09](../chapters/20-09-dacs.md) · Worked solutions: [20-09 solutions](../solutions/20-09-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** DNL and INL are endpoint-referenced, in LSB. Unit errors are independent with relative standard deviation σ_u. A single transistor's threshold has standard deviation $A_{VT}/\sqrt{2WL}$. NRZ response: $\text{sinc}(f/f_s)$; RZ: $\tfrac12\text{sinc}(f/2f_s)$; mixed mode: $\text{sinc}(f/2f_s)\sin(\pi f/2f_s)$, where $\text{sinc}(u) = \sin(\pi u)/(\pi u)$. Problems marked *(lab)* can be checked with `labs/20-09-lab/dac.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 20-09.1 [A]

**A 12-bit string DAC.** With $V_{REF}$ = 2.5 V, find the LSB, the output for code 3000 and the number of resistors.

### Problem 20-09.2 [A]

**A 4-bit ladder.** Using the Thévenin argument of §3.2, find the output of a 4-bit voltage-mode R-2R ladder for code 1011 (binary) as a fraction of $V_{REF}$, and its output resistance.

### Problem 20-09.3 [A]

**Counting cells.** A 16-bit current-steering DAC has 5 unary MSBs and 11 binary LSBs. How many unary cells are there, how many binary cells, and how many LSB units does each unary cell carry?

### Problem 20-09.4 [B]

**DNL at the major carry.** With σ_u = 0.1%, find σ(DNL) at the worst transition of a 16-bit binary DAC and of a 16-bit DAC segmented 4 + 12 (4 unary bits, 12 binary bits).

### Problem 20-09.5 [B] *(lab)*

**INL yield.** A 14-bit unary DAC must keep |INL| ≤ ½ LSB with 99.73% yield. Find σ_u from the mid-scale estimate and from the exact (Kolmogorov) rule with λ = 1.818.

### Problem 20-09.6 [B]

**Unit area.** For the exact σ_u of Problem 5, $A_{VT}$ = 3.5 mV·µm and $V_{ov}$ = 0.5 V, find the unit-transistor area and the total area of 16,383 units.

### Problem 20-09.7 [B]

**Output impedance for 10 bits.** A 10-bit unary DAC drives 50 Ω single-ended. What unit output impedance keeps INL within ½ LSB, and what HD2 does that impedance give for a full-scale sine?

### Problem 20-09.8 [B] *(lab)*

**Differential cancellation.** A 10-bit unary DAC has $xN_t$ = 0.01. Find the single-ended HD2 and the differential HD3, first from the estimates of §3.5 and then exactly.

### Problem 20-09.9 [A]

**Images.** A 1 GS/s NRZ DAC outputs 400 MHz. Find the droop at 400 MHz, the level of the image at 600 MHz, and how far the image sits below the signal.

### Problem 20-09.10 [B]

**Passband flatness.** Over the first Nyquist zone (DC to $f_s/2$), how much does an NRZ output's gain vary, and how much does an RZ output's gain vary?

### Problem 20-09.11 [B]

**Second-zone synthesis.** An RF DAC synthesizes a carrier at $0.7f_s$. Compare the mixed-mode and NRZ gains there.

### Problem 20-09.12 [B]

**Glitches at 10 bits.** A 1 V full-scale, 10-bit DAC has 100 ps of skew between its newly switched cells and the cells turning off at the mid-scale transition (511 → 512). Find the glitch impulse for a binary design and for a 4 + 6 segmented design.

### Problem 20-09.13 [A]

**Settling 18 bits.** An 18-bit DAC must settle to ½ LSB in 2 µs after a full-scale step, with a single-pole output. Find the largest time constant and the minimum bandwidth.

### Problem 20-09.14 [C] *(lab)*

**Data-weighted averaging.** An 8-element DAC with DWA receives the codes 3, 5, 2 (the pointer starts at element 0). Which elements are used each time, where is the pointer after each sample, and why does the mismatch error of the first two samples sum to zero?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Resistor and current-steering outputs and their errors | 1, 2, 7 |
| 2. Segmentation | 3, 4, 12 |
| 3. Mismatch, yield and area | 5, 6 |
| 4. Output impedance and differential outputs | 7, 8 |
| 5. Sinc response, images, settling | 9, 10, 11, 13 |
| 6. Dynamic element matching | 14 |
