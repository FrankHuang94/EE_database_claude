# Problems 09-07 · The Bipolar Junction Transistor

Chapter: [09-07](../chapters/09-07-bipolar-junction-transistor.md) · Worked solutions: [09-07 solutions](../solutions/09-07-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** NPN silicon transistors at 300 K with $n_i$ = 1.0 × 10¹⁰ cm⁻³, $V_T$ = 25.852 mV, $\varepsilon_s$ = 1.036 × 10⁻¹² F/cm. Mobilities follow the handbook model of 09-03 (electrons in the base, holes in the emitter): $\mu_n = 92 + 1268/[1 + (N/1.3\times10^{17})^{0.91}]$ and $\mu_p = 48 + 402/[1 + (N/6.3\times10^{16})^{0.76}]$ cm²/V·s. Use Hu's emitter band-gap narrowing (50 meV at 10¹⁹, 95 meV at 10²⁰ cm⁻³) where a problem asks for it. The saturation velocity is $v_{\text{sat}} = 1.53\times10^9\,T^{-0.87}$ cm/s. Uniform doping, step junctions, short base and emitter, low-level injection and $e^{V/V_T} \gg 1$ in forward bias unless stated otherwise.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 09-07.1 [A]

**Operating regions.** For each pair ($V_{BE}$, $V_{BC}$), name the region and find $V_{CE}$: (a) (0.75 V, −2 V); (b) (0.75 V, 0.6 V); (c) (−0.5 V, −3 V); (d) (−1 V, 0.7 V).

### Problem 09-07.2 [A]

**A small, fast transistor.** An NPN has $A_E$ = 4 µm², $W_B$ = 50 nm and $N_B$ = 5 × 10¹⁸ cm⁻³. (a) Find $\mu_n$ and $D_B$ in the base. (b) Find $I_S$ and $V_{BE}$ at 100 µA. (c) Find the base Gummel number and the base dopant count per cm².

### Problem 09-07.3 [A]

**Gains.** (a) Find $\alpha_F$ for $\beta_F$ = 150. (b) Find $\beta_F$ for $\alpha_F$ = 0.995. (c) With $\beta_F$ = 150 and $I_E$ = 2 mA, find $I_B$ and $I_C$.

### Problem 09-07.4 [B]

**Where the base current goes.** A transistor has $N_E$ = 10¹⁹ cm⁻³ (Hu's narrowing applies), $W_E$ = 0.3 µm, $N_B$ = 10¹⁷ cm⁻³, $W_B$ = 0.5 µm and base lifetime $\tau_B$ = 0.1 µs. (a) Find $D_B$, $D_E$ and the narrowing factor. (b) Find the emitter-injection-limited gain and the base-transport-limited gain, and the combined $\beta_F$. (c) Find $\gamma$, $\alpha_T$ and $\alpha_F$, and check $\alpha_F$ against $\beta_F/(1 + \beta_F)$.

### Problem 09-07.5 [B]

**Diminishing returns from emitter doping.** Two transistors have $N_B$ = 10¹⁸ cm⁻³ and $W_E = W_B$, and differ only in emitter doping: 10¹⁹ or 10²⁰ cm⁻³. (a) Using Hu's narrowing, find $\beta_F$ for each. (b) By what factor does tenfold emitter doping raise the gain, and why not by 10?

### Problem 09-07.6 [B]

**Buying base doping with germanium.** Start from the transistor of Example 09-07.2(b) ($\beta_F$ = 27.0 with a 10¹⁸ cm⁻³ silicon base). (a) If the base doping is raised to 10¹⁹ cm⁻³ with the same width, what is $\beta_F$ for a silicon base? (b) What base band-gap reduction would restore $\beta_F$ = 100?

### Problem 09-07.7 [B]

**Collector doping and the Early voltage.** The base has $N_B$ = 10¹⁸ cm⁻³ and $W_B$ = 0.1 µm at $V_{CB}$ = 2 V. (a) For $N_C$ = 3 × 10¹⁶, 10¹⁷ and 10¹⁸ cm⁻³, find the base–collector depletion width, the part of it in the base, the capacitance per µm², and $V_A$. (b) For $N_C$ = 10¹⁷ cm⁻³, how far does the base-side depletion edge move between $V_{CB}$ = 0 and 5 V, and by what factor does $I_C$ change (taking $W_B$ = 0.1 µm at 2 V)? Compare with the linear estimate from $V_A$.

### Problem 09-07.8 [C]

**Punch-through.** A transistor has a metallurgical base thickness of 0.15 µm, $N_B$ = 2 × 10¹⁷ cm⁻³, $N_E$ = 10²⁰ cm⁻³ and a lightly doped collector, $N_C$ = 10¹⁶ cm⁻³. $V_{BE}$ = 0.7 V. (a) Find how far the emitter–base depletion region extends into the base. (b) Find the base-side extent of the base–collector depletion region at $V_{CB}$ = 0 and the neutral base width there. (c) At what $V_{CB}$ do the two depletion regions meet (punch-through)? (d) Compare with the avalanche voltage of a one-sided junction on 10¹⁶ cm⁻³ (09-06), and say which limits this transistor.

### Problem 09-07.9 [B]

**Saturation.** A transistor has $\beta_F$ = 80, $\beta_R$ = 1 and $I_S$ = 10⁻¹⁶ A. (a) Find $V_{CE,\text{sat}}$ for forced gains of 5, 20 and 50. (b) At $V_{BE}$ = 0.7 V and $V_{CE}$ = 0.1 V, use Ebers–Moll to find $I_C$, $I_B$ and $I_C/I_B$, and compare $I_C$ with its forward-active value.

### Problem 09-07.10 [B]

**The high-injection knee.** For the transistor of the worked examples ($A_E$ = 10 µm², $W_B$ = 0.1 µm, $N_B$ = 10¹⁸ cm⁻³): (a) find the $V_{BE}$ at which $n'(0) = N_B$, and the ideal collector current there. (b) At $V_{BE}$ = 1.0 V, find $n'(0)$ from $n'(N_B + n') = n_i^2e^{V_{BE}/V_T}$, the resulting $I_C$, and the ideal (low-injection) prediction.

### Problem 09-07.11 [B]

**An aggressive SiGe base.** A base is 30 nm thick, doped 10¹⁹ cm⁻³, with a 0.15 eV linear germanium grading. The collector depletion region is 0.15 µm wide. (a) Find $D_B$ and the base transit time without grading. (b) Find $\eta$, the drift factor, the graded transit time and the built-in field. (c) Find the collector transit time. (d) Find $f_T$ for both bases, neglecting emitter delay and depletion charging.

### Problem 09-07.12 [B]

**A low-power operating point.** A transistor biased at 0.2 mA has $\beta_F$ = 120, $V_A$ = 40 V, $\tau_F$ = 2 ps, $C_{jE}$ = 5 fF and $C_{jC}$ = 3 fF. (a) Find $g_m$, $r_\pi$, $r_o$, $C_\pi$ and the intrinsic gain. (b) Find $f_T$ and compare with $1/(2\pi\tau_F)$. (c) At what current does the depletion-charging delay equal $\tau_F$?

### Problem 09-07.13 [C]

**Designing for f_max.** A transistor has $f_T$ = 300 GHz and $C_{jC}$ = 2 fF. (a) What base resistance gives $f_{\max}$ = 500 GHz? (b) Find $f_{\max}$ with $r_b$ = 50 Ω. (c) Contacting the base from both sides of the emitter stripe cuts $r_b$ by a factor of 4. By what factor does $f_{\max}$ rise?

### Problem 09-07.14 [B]

**Postponing the Kirk effect.** (a) What collector doping puts the Kirk onset at 3 mA/µm²? (b) At $V_{CB}$ = 1 V with $N_B$ = 10¹⁸ cm⁻³ and $W_B$ = 0.1 µm, compare the base–collector capacitance per µm² and $V_A$ for $N_C$ = 10¹⁷ cm⁻³ and for the doping found in (a). (c) Summarize the trade-off.

### Problem 09-07.15 [C]

**Base overdrive.** A transistor with $\beta_F$ = 50 and $\tau_F$ = 20 ps switches a load that limits $I_C$ to 2 mA. (a) Find the charge-control time constant and the minimum base current that saturates the transistor. (b) What base-current step turns it on (reaches 2 mA) in 0.5 ns? (c) Find the stored charge at the edge of saturation, the charge that base current could sustain, and the excess that turn-off must remove (treat saturation with the same charge-control equation, a simplification).

---

## Objective coverage

| Learning objective (chapter 09-07) | Problems |
|---|---|
| 1. Operation and collector current, Gummel number | 1, 2, 10 |
| 2. Base current, gain, band-gap narrowing, SiGe | 3, 4, 5, 6 |
| 3. Early voltage and output resistance | 7, 8, 14 |
| 4. Ebers–Moll and saturation | 1, 9 |
| 5. Transit times, hybrid-π, f_T, f_max, Kirk effect | 11, 12, 13, 14 |
| 6. Charge-control switching | 15 |
