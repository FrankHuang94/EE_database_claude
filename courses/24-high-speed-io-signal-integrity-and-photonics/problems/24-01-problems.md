# Problems 24-01 · Signal Integrity Fundamentals

Chapter: [24-01](../chapters/24-01-signal-integrity-fundamentals.md) · Worked solutions: [24-01 solutions](../solutions/24-01-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Copper has σ = 5.8 × 10⁷ S/m and μ = μ₀; $c$ = 2.998 × 10⁸ m/s; 1 inch = 25.4 mm and 1 mil = 25.4 µm; 1 Np = 8.686 dB. Use the chapter's first-order models: $R' = R_s/w$ for conductor loss, $\alpha_d = \pi f\sqrt{\varepsilon_r}\tan\delta/c$ for dielectric loss, and the weak-coupling crosstalk formulas with both lines terminated in $Z_0$. Values marked "assumed" are illustrative. Problems marked *(lab)* can be checked with `labs/24-01-lab/si.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 24-01.1 [A]

**Nyquist frequencies.** Find the symbol rate, Nyquist frequency and unit interval of (a) a 106.25 Gb/s PAM4 lane and (b) a 25.78125 Gb/s NRZ lane.

### Problem 24-01.2 [A]

**Skin depth.** Find the skin depth and surface resistance of copper at (a) 4 GHz and (b) 28 GHz.

### Problem 24-01.3 [B]

**Conductor loss of a PCIe trace.** *(lab)* A 4-mil-wide, 42.5 Ω trace of smooth copper carries a 28 GHz Nyquist tone. Find (a) its resistance per metre, (b) its conductor loss in dB/in from the first-order model, (c) the rule-of-thumb value and (d) the loss of 10 inches.

### Problem 24-01.4 [B]

**A premium laminate at 53 GHz.** *(lab)* A laminate has $\varepsilon_r$ = 3.3 and $\tan\delta$ = 0.0015 (assumed). At 53.125 GHz find (a) its dielectric loss per inch, (b) the smooth-copper conductor loss of a 4-mil, 50 Ω trace and (c) the total. (d) How does the total compare with the 1.27–1.8 dB/in used in 802.3dj budgets?

### Problem 24-01.5 [B]

**How rough is too rough?** (a) What rms roughness makes the Hammerstad–Jensen factor 1.5 at 28 GHz? (b) What is the factor for that roughness at 4 GHz?

### Problem 24-01.6 [B]

**Where dielectric loss takes over.** *(lab)* For Example 24-01.2's 5-mil, 50 Ω smooth-copper trace on the FR-4-class laminate ($\varepsilon_r$ = 4.4, $\tan\delta$ = 0.014), find (a) the conductor and dielectric losses at 1 GHz, (b) the frequency at which they are equal and (c) the total loss per inch at that frequency.

### Problem 24-01.7 [B]

**A PCIe 6.0 budget.** PCIe 6.0's 32 dB at 16 GHz has been presented as 8.0 dB for the root complex, 8.5 dB for the add-in card and 15.5 dB for the system board. (a) Check the total. If the board's connector takes 1.5 dB and two vias 0.6 dB each (assumed), how long can the board trace be on (b) Example 24-01.3's Megtron 6 line (0.7097 dB/in) and (c) a laminate at 1.0 dB/in?

### Problem 24-01.8 [B]

**A connector mismatch.** A connector behaves as a 60 Ω section in a 50 Ω system. Find (a) the reflection coefficient, (b) the return loss and (c) the mismatch loss. (d) What range of impedance keeps the return loss at 15 dB or better?

### Problem 24-01.9 [B]

**Ripple between two discontinuities.** Two identical discontinuities with $\lvert\Gamma\rvert$ = 0.15 sit 3 inches apart on a stripline with $\varepsilon_r$ = 3.6. Find (a) the one-way delay between them, (b) the period of the ripple in $\lvert S_{21}\rvert$ and (c) its peak-to-peak size in dB.

### Problem 24-01.10 [B]

**Back-drilling.** *(lab)* (a) Find the notch of a 2.4 mm via stub in $\varepsilon_r$ = 3.7. (b) Back-drilling leaves 0.25 mm; where is the notch now? (c) For PCIe 7.0 (Nyquist 32 GHz), what is the longest stub that keeps the notch above 1.5 times the Nyquist frequency?

### Problem 24-01.11 [C]

**Stripline against microstrip.** Two 50 Ω lines are coupled over 100 mm. The aggressor launches 0.5 V with a 20 ps linear rise. (a) In stripline with $\varepsilon_r$ = 3.6 and $C_m/C = L_m/L$ = 0.03, find the velocity, the coupled delay, the NEXT amplitude and duration, and the FEXT. (b) If the same geometry were microstrip with $C_m/C$ = 0.03 and $L_m/L$ = 0.05 and, for simplicity, the same velocity, what would FEXT be? (c) For that microstrip, what coupled length keeps FEXT within 2% of the aggressor?

### Problem 24-01.12 [C]

**Short coupled lengths.** (a) Starting from $V_{NEXT}(t) = K_b[V_a(t) - V_a(t - 2T_D)]$, show that for a linear aggressor ramp of rise time $t_r$ and a coupled length with $2T_D < t_r$, the NEXT peak is $K_bV_a(2T_D/t_r)$. (b) Evaluate it for $K_b$ = 0.03, a 1 V aggressor, $t_r$ = 30 ps, ℓ = 1 mm and $v$ = 1.5 × 10⁸ m/s, and (c) find the saturation length.

### Problem 24-01.13 [B]

**Ground bounce budget.** Single-ended drivers each switch 12 mA within 80 ps through a shared 0.15 nH return (assumed). How many may switch together if the bounce must stay below 100 mV?

### Problem 24-01.14 [B]

**A core-supply PDN.** A 0.75 V core may vary by 2.5% under a 40 A load step (assumed). Find (a) the target impedance. The package's decoupling path has 15 pH of inductance (assumed). (b) What is its impedance at 100 MHz, and (c) above what frequency does it exceed the target?

### Problem 24-01.15 [A]

**Reading S-parameters.** A channel has $\lvert S_{21}\rvert$ = 0.5 and $\lvert S_{11}\rvert$ = 0.2 at its Nyquist frequency. Find (a) the insertion loss, (b) the return loss and (c) the fraction of the incident power that is neither reflected nor transmitted. Where did it go?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Nyquist frequency, conductor and dielectric loss, roughness | 1, 2, 3, 4, 5, 6 |
| 2. Loss budgets and reach | 4, 7 |
| 3. S-parameters, return loss and ripple | 8, 9, 15 |
| 4. Via stubs | 10 |
| 5. Crosstalk | 11, 12 |
| 6. Ground bounce, PDN and jitter | 13, 14 |
