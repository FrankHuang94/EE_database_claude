# Problems 09-06 · PN Junction I–V, Capacitance and Breakdown

Chapter: [09-06](../chapters/09-06-pn-junction-iv-and-capacitance.md) · Worked solutions: [09-06 solutions](../solutions/09-06-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** silicon at 300 K with $n_i$ = 1.0 × 10¹⁰ cm⁻³, $V_T = kT/q$ = 25.852 mV, $N_C$ = 3.2 × 10¹⁹ cm⁻³ and $\varepsilon_s$ = 11.7ε₀ = 1.036 × 10⁻¹² F/cm. Mobilities follow the handbook model of 09-03: $\mu_n = 92 + 1268/[1 + (N/1.3\times10^{17})^{0.91}]$ and $\mu_p = 48 + 402/[1 + (N/6.3\times10^{16})^{0.76}]$ cm²/V·s. Auger coefficients are $C_n$ = 1.1 × 10⁻³⁰ and $C_p$ = 0.3 × 10⁻³⁰ cm⁶/s. For other temperatures use the course $n_i(T)$ model (09-02 §3.8, Varshni gap $E_g = 1.17 - 4.73\times10^{-4}T^2/(T + 636)$ eV). Ionization coefficients are those of chapter §3.9. Assume step junctions, the depletion approximation, low-level injection and ideality factor 1 unless a problem says otherwise. Problems marked "numerical" expect a short script or the lab notebook.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 09-06.1 [A]

**The law of the junction.** A P⁺N junction has $N_D$ = 5 × 10¹⁵ cm⁻³ on the n side. (a) Find $p_{n0}$. (b) Find the hole density at the n-side depletion edge at $V_A$ = 0.5 V and at 0.65 V, and compare each with $N_D$. (c) At what forward bias does the excess hole density at the edge reach 10% of $N_D$? (d) At $V_A$ = −0.2 V, what fraction of $p_{n0}$ remains at the edge?

### Problem 09-06.2 [A]

**An N⁺P diode.** A long N⁺P diode has $N_A$ = 10¹⁶ cm⁻³ on the p side, electron lifetime 2 µs there, and area 50 µm × 50 µm. Neglect the current injected into the n⁺ side. (a) Find $\mu_n$, $D_n$ and $L_n$. (b) Find $J_s$ and $I_s$. (c) Find the forward voltage at 1 µA and the current at 0.55 V.

### Problem 09-06.3 [A]

**Reading an ideality factor.** A diode's measured forward characteristic includes the points (0.20 V, 1.00 nA), (0.32 V, 10.2 nA), (0.50 V, 0.200 µA) and (0.56 V, 2.00 µA). (a) Find the ideality factor from the first pair and from the second pair. (b) For each pair, extrapolate to zero bias to find the prefactor $I_0$ of $I = I_0e^{qV/\eta kT}$. (c) Which physical mechanism dominates each range?

### Problem 09-06.4 [B]

**Long or short?** A P⁺N diode has $N_D$ = 10¹⁵ cm⁻³, $\tau_p$ = 10 µs, and an n-side neutral region 20 µm thick ending at an ohmic contact. (a) Find $D_p$ and $L_p$. Is the diode long or short? (b) Find the factor $\coth(W_n/L_p)$ by which its hole saturation current exceeds that of a long diode, and compare with the short-diode estimate $L_p/W_n$. (c) What fraction of the injected holes recombine before reaching the contact? Compare with $W_n^2/2L_p^2$. (d) Compare the transit time with the lifetime.

### Problem 09-06.5 [B]

**Injection efficiency.** An N⁺P junction has $N_D$ = 10¹⁹ cm⁻³ on the n⁺ side and $N_A$ = 10¹⁶ cm⁻³ on the p side, where $\tau_n$ = 1 µs. The n⁺ side's hole lifetime is set by Auger recombination. (a) Find the hole lifetime, $D_p$ and $L_p$ on the n⁺ side, and $D_n$ and $L_n$ on the p side. (b) Treating both sides as long, find both saturation current densities and the fraction of the current carried by electrons injected into the p side (the injection efficiency). (c) The n⁺ region is now only 0.3 µm thick, ending at a contact. Recompute the hole current density and the injection efficiency. (d) Why does this matter for a bipolar transistor's emitter?

### Problem 09-06.6 [B]

**Two currents in one diode.** A diode has an ideal diffusion current with $I_s$ = 1 × 10⁻¹⁵ A and a depletion-region recombination current $I_{r0}e^{qV/2kT}$ with $I_{r0}$ = 1 × 10⁻¹⁰ A. (a) Find the voltage at which the two are equal. (b) Find the total current and the local ideality factor $\eta = (q/kT)\,dV/d\ln I$ at 0.3 V and at 0.6 V. (c) Above what voltage is $\eta$ below 1.1?

### Problem 09-06.7 [C]

**When does diffusion leakage take over?** For the diode of Examples 09-06.1 and 09-06.3 at 5 V reverse bias, the generation current is 7.00 pA and the ideal saturation current 4.973 × 10⁻¹⁶ A at 300 K. Hold the depletion width, $\tau_0$, $D_p$ and $\tau_p$ fixed, so that generation scales as $n_i$ and diffusion as $n_i^2$. (a) Find the ratio $n_i(T)/n_i(300\text{ K})$ at which the two are equal. (b) Using the course $n_i(T)$ model (numerical), find that temperature. (c) Explain how measuring leakage against temperature distinguishes the two mechanisms.

### Problem 09-06.8 [B]

**A diode thermometer.** A diode is driven by a constant 1 µA and has $I_s$ = 2 × 10⁻¹⁵ A at 300 K. (a) Find its voltage at 300 K and $dV/dT$ from the formula of §3.6. (b) Predict the voltage at 375 K by linear extrapolation. (c) Compute it with the full $n_i(T)$ model, holding $D$ and $\tau$ fixed. How large is the error of the linear prediction? (d) A second identical diode carries 8 µA. Find the voltage difference at 300 K and at 375 K.

### Problem 09-06.9 [B]

**When the small-signal model fails.** A long P⁺N diode with $\tau_p$ = 0.5 µs is biased at 50 µA, where its junction capacitance is 2 pF. (a) Find $g_d$, $r_d$ and the low-frequency diffusion capacitance. (b) At 1 MHz, find the exact admittance $Y = g_d\sqrt{1 + j\omega\tau_p} + j\omega C_j$ and the low-frequency model's $g_d + j\omega(C_d + C_j)$. Compare their magnitudes. (c) Express the exact admittance as an effective conductance in parallel with an effective capacitance, and explain the change from the low-frequency values.

### Problem 09-06.10 [B]

**Designing for recovery.** A diode with $\tau_p$ = 200 ns conducts 5 mA and is switched to a reverse current of 2.5 mA. (a) Find the stored charge. (b) Find the storage time by charge control and exactly. (c) What reverse current would make the exact storage time 20 ns? What does charge control predict for that current?

### Problem 09-06.11 [C]

**Avalanche design (numerical).** A one-sided P⁺N junction ($N_A$ = 10¹⁹ cm⁻³) has $N_D$ = 2 × 10¹⁵ cm⁻³. (a) Solve the ionization integral for the peak field, breakdown voltage and depletion width at breakdown. (b) Compare with the fixed-critical-field estimate ($\mathcal E_c$ = 3 × 10⁵ V/cm) and with Hu's rule. (c) Find the doping that gives exactly 100 V, and compare with the doping that Hu's rule predicts.

### Problem 09-06.12 [B]

**A tunneling (Zener) junction.** A symmetric junction has $N_A = N_D$ = 10¹⁸ cm⁻³ (ignore degeneracy). (a) Find $V_{bi}$ and the zero-bias depletion width. (b) At what reverse voltage does the peak field reach 10⁶ V/cm, Hu's tunneling field? What is the depletion width then? (c) At that field, evaluate the electron-initiated ionization integral numerically, with the field falling linearly from the center to each edge. What multiplication factor does avalanche add? (d) What temperature coefficient do you expect for this diode's breakdown voltage, and why?

### Problem 09-06.13 [B]

**Choosing a Schottky metal.** Titanium ($\phi_{Bn}$ = 0.5 V) and platinum (0.9 V) are candidate Schottky contacts on n-type silicon, area 1 mm², with $K$ = 100 A/(cm²·K²). (a) Find $I_0$ for each at 300 K. (b) Find the forward voltage of each at 100 mA. (c) Find each one's $I_0$ at 400 K, assuming the barrier does not change, and the increase factor. (d) Which would you choose for a low-voltage rectifier, and what limits the choice?

### Problem 09-06.14 [C]

**Rectifier losses at temperature.** A 5 A rectifier conducts half the time and blocks 20 V the other half, at a junction temperature of 373.15 K. Compare (i) a Schottky diode, $\phi_{Bn}$ = 0.60 V, area 0.05 cm², $K$ = 100 A/(cm²·K²), and (ii) a PN diode of the same area with $J_s$ = 1 × 10⁻¹² A/cm² at 300 K, scaling as $n_i^2$. Ignore series resistance and treat the reverse current as $I_0$. (a) Find each one's $I_0$ and forward drop at 5 A. (b) Find the conduction loss, the leakage loss and the total for each. (c) For the Schottky diode, show that the total loss is minimized when $I_0 = V_T(\text{duty} \times I_F)/(\text{duty} \times V_R)$, find the optimum barrier height and the minimum loss, and comment on how flat the optimum is.

### Problem 09-06.15 [C]

**Ohmic-contact engineering.** Use the tunneling exponent $(4\pi\phi_B/h)\sqrt{\varepsilon_sm^*/N}$ with $m^*$ = 0.26$m_0$, and assume $\rho_c$ is proportional to $e^{\text{exponent}}$. (a) For $\phi_B$ = 0.6 V, find the exponent at 10²⁰ cm⁻³ and the doping at which it falls to 3. (b) If $\rho_c$ = 1 × 10⁻⁷ Ω·cm² at 10²⁰ cm⁻³, estimate $\rho_c$ at 3 × 10²⁰ cm⁻³. (c) By what factor does lowering the barrier from 0.6 to 0.4 V at 10²⁰ cm⁻³ reduce $\rho_c$? (d) Find the resistance of a 20 nm × 30 nm contact with $\rho_c$ = 1 × 10⁻⁹ Ω·cm². (e) Why might a process use different silicides for n⁺ and p⁺ contacts?

---

## Objective coverage

| Learning objective (chapter 09-06) | Problems |
|---|---|
| 1. Ideal diode equation, long and short diodes, injection efficiency | 1, 2, 4, 5 |
| 2. Non-ideal currents and the ideality factor | 3, 6, 7 |
| 3. Temperature dependence and PTAT | 7, 8 |
| 4. Small-signal model and switching | 9, 10 |
| 5. Avalanche and tunneling breakdown | 11, 12 |
| 6. Schottky diodes and ohmic contacts | 13, 14, 15 |
