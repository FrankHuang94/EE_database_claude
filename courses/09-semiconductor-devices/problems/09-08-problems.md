# Problems 09-08 · The MOS Capacitor

Chapter: [09-08](../chapters/09-08-mos-capacitor.md) · Worked solutions: [09-08 solutions](../solutions/09-08-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** silicon at 300 K with $n_i$ = 1.0 × 10¹⁰ cm⁻³, $V_T$ = 25.852 mV, $E_g$ = 1.12 eV, $N_C$ = 3.2 × 10¹⁹ and $N_V$ = 1.8 × 10¹⁹ cm⁻³, $\chi_{\text{Si}}$ = 4.05 eV, $\varepsilon_s$ = 11.7ε₀ = 1.036 × 10⁻¹² F/cm and $\varepsilon_{ox}$ = 3.9ε₀ = 3.453 × 10⁻¹³ F/cm. An n⁺ poly gate has $\psi_g$ = 4.05 V and a p⁺ poly gate 5.17 V. Body work functions follow from $E_C - E_F$ with Boltzmann statistics. Use the depletion and sheet-charge approximations unless a problem asks for the exact solution of chapter §3.6. "Numerical" problems expect a short script or the lab notebook.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 09-08.1 [A]

**Flat-band voltages.** Find $V_{FB}$ (no oxide charge) for (a) an n⁺ poly gate on p-type silicon with $N_A$ = 10¹⁶ cm⁻³; (b) a p⁺ poly gate on n-type silicon with $N_D$ = 10¹⁷ cm⁻³; (c) a metal gate with work function 4.6 V on the body of (a), ignoring interface effects.

### Problem 09-08.2 [A]

**Capacitance and EOT.** (a) Find $C_{ox}$ for 3 nm of SiO₂. (b) A stack has 0.6 nm of SiO₂ under 4 nm of HfO₂ ($k$ = 21.2). Find its EOT and capacitance per area. (c) How much thicker, physically, is the stack than the SiO₂ film of (a)?

### Problem 09-08.3 [A]

**Accumulation.** A capacitor with a 5 nm oxide is biased 1.5 V below flat band. Find $C_{ox}$, the accumulation charge per area, and the hole sheet density.

### Problem 09-08.4 [B]

**Depletion.** For the chapter's capacitor ($N_A$ = 10¹⁷ cm⁻³, 10 nm oxide, n⁺ gate, $V_{FB}$ = −0.9858 V), find the depletion width and surface potential at $V_g$ = −0.5 V and at +0.2 V.

### Problem 09-08.5 [B]

**Threshold against doping at a thin oxide.** For an n⁺ poly gate and a 3 nm oxide, find $V_{FB}$ and $V_{TH}$ for $N_A$ = 10¹⁶, 10¹⁷ and 10¹⁸ cm⁻³. What does the result suggest about setting thresholds with an n⁺ gate at thin oxides?

### Problem 09-08.6 [B]

**Designing a threshold.** With an n⁺ poly gate and a 3 nm oxide, what body doping gives $V_{TH}$ = 0.4 V?

### Problem 09-08.7 [B]

**A p-channel capacitor.** An n-type body with $N_D$ = 10¹⁷ cm⁻³ has a p⁺ poly gate and a 3 nm oxide. Find $\phi_B$, $V_{FB}$ and $V_{TH}$.

### Problem 09-08.8 [B]

**Inversion charge and channel resistance.** A 2 nm oxide is biased 0.8 V above threshold. (a) Find $C_{ox}$, $Q_{inv}$ and the electron sheet density. (b) With an electron mobility of 250 cm²/V·s in the channel, find the sheet resistance of the inversion layer.

### Problem 09-08.9 [B]

**Exact inversion charge (numerical).** For the chapter's capacitor ($V_{TH}$ = 0.3293 V), solve the exact model at $V_g = V_{TH}$ + 0.5 V and $V_{TH}$ + 1.5 V for $\phi_s$ and the inversion charge (total minus $\sqrt{2qN_A\varepsilon_s(\phi_s - V_T)}$), and compare with the sheet-charge value. What trend do you see?

### Problem 09-08.10 [B]

**A C–V curve by hand.** A capacitor has a 5 nm oxide, $N_A$ = 5 × 10¹⁶ cm⁻³ and an n⁺ gate. Find (a) $C_{ox}$ and $V_{FB}$; (b) the Debye length and $C_{FB}$; (c) $W_{d\max}$ and the high-frequency $C_{\min}$; (d) the depletion width and capacitance at $V_g$ = 0; (e) the slope of $1/C^2$ against $V_g$ in depletion.

### Problem 09-08.11 [B]

**Reading a measured curve.** A 100 µm × 100 µm capacitor with an n⁺ gate on p-type silicon shows a high-frequency $C_{\max}$ = 69.06 pF and $C_{\min}$ = 5.25 pF, and its flat-band voltage is −1.05 V. Extract (a) $T_{ox}$, (b) $N_A$, (c) the ideal flat-band voltage, and (d) the oxide charge.

### Problem 09-08.12 [B]

**Mobile ions.** After a positive bias–temperature stress, a capacitor with a 20 nm oxide shows its flat-band voltage shifted by −0.15 V. Assuming the shift is caused by mobile positive ions drifting to the silicon interface, find their areal density.

### Problem 09-08.13 [B]

**Gate doping and poly depletion.** A 1.5 nm oxide carries 5 MV/cm in inversion, and $T_{inv}$ = 1.5 nm. For n⁺ poly doping of 5 × 10¹⁹, 10²⁰ and 3 × 10²⁰ cm⁻³, find $W_{dpoly}$, $\phi_{poly}$ and $T_{oxe}$.

### Problem 09-08.14 [C]

**Deep depletion.** The chapter's capacitor (no source or drain) is stepped from flat band to $V_g$ = 3 V in a microsecond. (a) Before any electrons arrive, find the deep-depletion width, the surface potential and $C/C_{ox}$. (b) Find the inversion charge the capacitor will eventually hold. (c) If thermal generation in the depletion region ($\tau_0$ = 1 µs) is the only source of electrons, estimate the time to form the inversion layer using the deep-depletion width, and using $W_{d\max}$. Which is an under- and which an over-estimate?

### Problem 09-08.15 [C]

**A CET budget.** A gate stack has a 0.4 nm SiO₂ interfacial layer and an inversion-layer contribution $T_{inv}/3$ = 0.3 nm. (a) What HfO₂ thickness ($k$ = 21.2) gives a CET of 1.0 nm? Of 0.9 nm? (b) If the HfO₂ must be at least 1.5 nm thick for reliability, how thin must the interfacial layer be to reach 0.9 nm?

---

## Objective coverage

| Learning objective (chapter 09-08) | Problems |
|---|---|
| 1. Band diagrams and flat-band voltage | 1, 7, 11, 12 |
| 2. Threshold voltage and inversion charge | 4, 5, 6, 7, 8 |
| 3. Exact surface charge | 9 |
| 4. C–V characteristics and extraction | 10, 11, 14 |
| 5. Thin-dielectric effects, EOT, CET, high-k | 2, 3, 13, 15 |
