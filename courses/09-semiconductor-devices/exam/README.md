# Course 09 · Final Exam (Semiconductor Devices)

**Time limit:** 240 minutes.
**Allowed:** a scientific calculator, and the [Course 09 equation sheet](../../../reference/equation-sheets/09-semiconductor-devices.md) printed without its chapter links. No notes, no Python, no simulator.

**Instructions.**

- Answer all 15 questions and show every step.
- Question 1 [A] is worth 5 points, each [B] 8 and Question 15 [C] 12: 121 points in total. 85 or more (about 70%) is a strong pass.
- Within a question the lettered parts carry equal weight.
- Give numerical answers to 3–4 significant figures, with units.
- Question 15 is a short-answer diligence question, graded against the rubric in the solutions.
- Solutions are in a separate file, [solutions.md](solutions.md). Open it only after you finish.

**Conventions.** These are the conventions of the chapters' problem sets.

- **Constants.** 300 K; $V_T$ = 25.852 mV; $q$ = 1.602 × 10⁻¹⁹ C; $\varepsilon_s$ = 11.7ε₀ = 1.036 × 10⁻¹² F/cm and $\varepsilon_{ox}$ = 3.9ε₀ = 3.453 × 10⁻¹³ F/cm; $n_i$ = 1.0 × 10¹⁰ cm⁻³; $E_g$ = 1.12 eV; $N_C$ = 3.2 × 10¹⁹ and $N_V$ = 1.8 × 10¹⁹ cm⁻³; $hc$ = 1.2398 eV·µm; $c$ = 2.998 × 10⁸ m/s.
- **Mobility (silicon, 300 K).** $\mu_n = 92 + 1268/[1 + (N/1.3\times10^{17})^{0.91}]$ and $\mu_p = 48 + 402/[1 + (N/6.3\times10^{16})^{0.76}]$ cm²/V·s, with $N$ the total doping.
- **Doping.** Dopants are fully ionized; $\phi_B = V_T\ln(N_A/n_i)$.
- **MOS.** n⁺ polysilicon gates have $V_{FB} = -(E_C - E_F)_{\text{body}}/q$ with $E_F - E_V = kT\ln(N_V/N_A)$, and no oxide charge.

---

**1 [A] · Crystals and bands.** (09-01)
(a) Silicon's cubic cell (lattice constant 5.431 Å) holds 8 atoms. Find the atom density.
(b) Find the electron conductivity effective mass from $m_l$ = 0.98 $m_0$ and $m_t$ = 0.19 $m_0$.
(c) Find silicon's absorption cutoff wavelength.

**2 [B] · Carriers and the Fermi level.** (09-02)
(a) Silicon is doped with 2 × 10¹⁶ cm⁻³ donors. Find $n_0$, $p_0$, $E_F - E_i$ and $E_C - E_F$.
(b) 1.5 × 10¹⁶ cm⁻³ acceptors are added. Find the new $n_0$, $p_0$ and $E_F - E_i$.
(c) A transistor's depletion region measures 20 nm × 20 nm × 10 nm at 10¹⁸ cm⁻³. Treating the dopant count as Poisson, find the mean count, the probability that the region holds no dopant at all, and the relative spread σ/mean.

**3 [B] · Drift and diffusion.** (09-03)
An n-type silicon layer is doped at 10¹⁶ cm⁻³ and is 2 µm thick.
(a) Find the electron mobility, the resistivity and the sheet resistance.
(b) A resistor is drawn 50 squares long. Find its resistance.
(c) For minority holes in this layer, find the mobility, the diffusion coefficient and, for a 1 µs lifetime, the diffusion length.

**4 [B] · Recombination and generation.** (09-04)
The layer of Question 3 ($n_0$ = 10¹⁶ cm⁻³) contains 10¹³ cm⁻³ mid-gap traps with a hole capture cross section of 10⁻¹⁵ cm²; take the hole thermal velocity as 1.65 × 10⁷ cm/s.
(a) Find the SRH hole lifetime.
(b) Light generates 10²⁰ pairs cm⁻³ s⁻¹ uniformly. Find the steady-state excess hole density and check low-level injection.
(c) Find the quasi-Fermi-level separation $E_{Fn} - E_{Fp}$ under this illumination.
(d) Find the hole diffusion length with this lifetime.

**5 [B] · Junction electrostatics.** (09-05)
An abrupt silicon junction has $N_A$ = 10¹⁸ cm⁻³ and $N_D$ = 10¹⁶ cm⁻³.
(a) Find the built-in potential.
(b) Find the depletion width at zero bias and at −10 V.
(c) At −10 V, find the peak field (use $\mathcal E_{\max} = 2(V_{bi} - V)/W$) and the junction capacitance per area.

**6 [B] · The diode.** (09-06)
The junction of Question 5 is a long P⁺N diode of area 10⁻⁴ cm² with a hole lifetime of 1 µs in the N side.
(a) Find the saturation current $I_0$ (hole injection only).
(b) Find the forward voltage at 1 mA.
(c) At 1 mA, find the small-signal resistance and the diffusion capacitance $C_d = (\tau_p/2)g_d$.
(d) Estimate the breakdown voltage with Hu's rule $V_B \approx 15\text{ V} \times (10^{17}/N)^{0.6}$.

**7 [B] · The bipolar transistor.** (09-07)
An NPN transistor has an emitter area of 10⁻⁶ cm², a base 0.1 µm wide doped 10¹⁷ cm⁻³, and an emitter 0.1 µm wide doped 10¹⁹ cm⁻³ (short regions; ignore band-gap narrowing and recombination).
(a) Find the base electron diffusion coefficient, the saturation current $I_S$ and $I_C$ at $V_{BE}$ = 0.7 V.
(b) Find the current gain limited by emitter injection, $\beta = (D_nN_EW_E)/(D_pN_BW_B)$.
(c) Find the base transit time $W_B^2/2D_n$ and the corresponding $f_T = 1/2\pi\tau_B$, and $g_m$ at the current of (a).

**8 [B] · The MOS capacitor.** (09-08)
p-type silicon with $N_A$ = 5 × 10¹⁷ cm⁻³ has a 4 nm SiO₂ gate oxide and an n⁺ poly gate.
(a) Find $C_{ox}$, $\phi_B$ and $V_{FB}$.
(b) Find the depletion-charge term $Q_{dep}/C_{ox}$ at threshold and the threshold voltage.
(c) Find $W_{d\max}$ and the minimum high-frequency capacitance, absolute and as a fraction of $C_{ox}$.

**9 [B] · The long-channel MOSFET.** (09-09)
An NMOS with the gate stack of Question 8 has $W$ = 10 µm, $L$ = 1 µm, $\mu_{ns}$ = 300 cm²/V·s, $m$ = 1.25 and $V_{TH}$ = 0.35 V.
(a) At $V_{GS}$ = 1.0 V, find $V_{Dsat}$, $I_{Dsat}$ and $g_m$ in saturation.
(b) Find the subthreshold swing and the off-current at $V_{GS}$ = 0, taking the threshold-defining current as 100 nA × W/L.

**10 [B] · Short-channel effects.** (09-10)
A 50 nm NMOS has a 2 nm oxide, $m$ = 1.2, $\mu_{ns}$ = 200 cm²/V·s and $v_{sat}$ = 8 × 10⁶ cm/s, at 0.6 V overdrive.
(a) Find $\mathcal E_{sat} = 2v_{sat}/\mu_{ns}$, $\mathcal E_{sat}L$, $V_{Dsat}$ and $I_{Dsat}$ per micrometer of width.
(b) A 30 nm device of the same technology has $l_d$ = 8 nm. With Hu's model, find the threshold reduction at $V_{DS}$ = 0.75 V and the factor by which it raises the off-current at $S$ = 75 mV/decade.

**11 [B] · CMOS and scaling.** (09-11)
(a) A square-law inverter has $V_{DD}$ = 0.9 V, $V_{TN} = |V_{TP}|$ = 0.25 V and $k_n/k_p$ = 2.5. Find $V_M$.
(b) Each stage drives 2 fF at 0.8 V with $I_{onN}$ = 120 µA and $I_{onP}$ = 90 µA. Find $\tau_d$ and the frequency of a 31-stage ring oscillator.
(c) 10⁸ such gates switch with activity 0.15 at 2 GHz. Find the dynamic power.
(d) By what factor does power density rise per 0.7× node if voltage stays constant and frequency rises as 1/delay?

**12 [B] · Advanced transistors.** (09-12)
(a) Find the scale length of a double-gate body 6 nm thick with a 1 nm oxide.
(b) For $L$ = 24 nm, use the approximation $u_{\min} \approx 2\sqrt{ab}\,e^{-L/2\lambda}$ with $a$ = 0.2 V and $b = a + V_{DS}$ to estimate the threshold reduction at 0.05 V and 0.7 V, and the DIBL.
(c) A fin is 46 nm tall and 7 nm wide. Find its effective width, and the fins and width needed for at least 300 nm.
(d) A 500 Ω power rail, fed at both ends, carries 0.25 mA of uniformly distributed load. Find the worst IR drop.

**13 [B] · Wide-bandgap power devices.** (09-13)
(a) Design a 1700 V triangular-field drift layer with a fixed critical field: silicon with $\mathcal E_c$ = 2.0 × 10⁵ V/cm, $\varepsilon_r$ = 11.7 and $\mu_n$ = 1350 cm²/V·s; 4H-SiC with 2.5 × 10⁶ V/cm, 9.96 and 1000 cm²/V·s. Find each doping, thickness and specific on-resistance, and the ratio.
(b) A heterojunction emitter adds a 0.15 eV hole barrier. By what factor can the gain rise?
(c) Find the sheet resistance of a 2DEG with 9 × 10¹² cm⁻² electrons at 1800 cm²/V·s.

**14 [B] · Optoelectronics.** (09-14)
(a) Find the responsivity at 905 nm for $\eta$ = 0.6.
(b) Find the round-trip time to a target 150 m away.
(c) A pixel has a full well of 10,000 electrons and 3 electrons of read noise. Find its dynamic range in dB.
(d) A solar cell has $J_{sc}$ = 38 mA/cm² and $J_0$ = 2 × 10⁻¹³ A/cm² under 100 mW/cm². Find $V_{oc}$. The maximum-power voltage satisfies $V = V_{oc} - V_T\ln(1 + V/V_T)$; starting from $V_{oc} - 3V_T$, iterate twice. Then find $J_{mp}$, the fill factor and the efficiency.

**15 [C] · Diligence.** A start-up pitches its 1200 V power transistor: "built on a 3-nanometer-class process, it has ten times lower on-resistance than the best SiC MOSFETs, and our matching LiDAR SPAD has industry-best detection efficiency."
(a) If the tenfold advantage came entirely from the drift layer at equal $\varepsilon\mu$, what critical-field ratio would it require? Is that plausible for any known material? (3 points)
(b) Explain why "3-nanometer-class" says nothing useful about a 1200 V transistor. (3 points)
(c) List three specific measurements or data you would request to test the on-resistance claim, and why. (3 points)
(d) What must accompany a detection-efficiency claim for it to be comparable? (3 points)
