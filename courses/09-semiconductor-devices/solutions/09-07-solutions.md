# Solutions 09-07 · The Bipolar Junction Transistor

Problems: [09-07 problems](../problems/09-07-problems.md) · Chapter: [09-07](../chapters/09-07-bipolar-junction-transistor.md). Every number below is recomputed by [verify_09_07.py](../verify/verify_09_07.py), by these routes:

- currents by solving the base and emitter diffusion problems numerically;
- depletion edges by root finding on the junction potential;
- saturation points by solving the Ebers–Moll equations;
- transit times from the numerically solved drift–diffusion profile;
- design values by root finding.

---

## Solutions

### Solution 09-07.1

$V_{CE} = V_{BE} - V_{BC}$.

(a) Base–emitter forward, base–collector reverse: forward active, $V_{CE}$ = **2.75** V.

(b) Both forward: saturation, $V_{CE}$ = **0.15** V.

(c) Both reverse: cutoff, $V_{CE}$ = **2.5** V.

(d) Base–emitter reverse, base–collector forward: reverse active, $V_{CE}$ = **−1.7** V.

### Solution 09-07.2

(a) $\mu_n(5\times10^{18})$ = **136.2** cm²/V·s, so $D_B$ = **3.521** cm²/s.

(b) $I_S = qA_ED_Bn_i^2/(W_BN_B) = 1.602\times10^{-19} \times 4\times10^{-8} \times 3.521 \times 10^{20}/(5\times10^{-6} \times 5\times10^{18})$ = **9.03 × 10⁻²⁰** A, and $V_{BE} = V_T\ln(10^{-4}/I_S)$ = **0.8955** V.

(c) $G_B = N_BW_B/D_B$ = **7.10 × 10¹²** s/cm⁴. The base dopant count is $N_BW_B$ = **2.5 × 10¹³** cm⁻².

### Solution 09-07.3

(a) $\alpha_F = 150/151$ = **0.9934**.

(b) $\beta_F = 0.995/0.005$ = **199**.

(c) $I_B = I_E/(1 + \beta_F)$ = **13.25** µA and $I_C = \alpha_FI_E$ = **1.987** mA.

### Solution 09-07.4

(a) $D_B = V_T\mu_n(10^{17})$ = **20.72** cm²/s and $D_E = V_T\mu_p(10^{19})$ = **1.457** cm²/s. The narrowing factor is $e^{0.050/0.025852}$ = **6.918**.

(b) The emitter-injection limit is

$$
\beta_E = \frac{D_BW_EN_E}{D_EW_BN_B\,e^{\Delta E_g/kT}} = \frac{20.72 \times 0.3 \times 10^{19}}{1.457 \times 0.5 \times 10^{17} \times 6.918} = \mathbf{123.3} .
$$

$L_B = \sqrt{D_B\tau_B}$ = **14.39** µm, so the transport limit is $\beta_T = 2L_B^2/W_B^2$ = **1657**. Combined: $1/\beta_F = 1/123.3 + 1/1657$, giving $\beta_F$ = **115**. Emitter injection dominates even in this rather wide base.

(c) $\gamma = 1/(1 + 1/\beta_E)$ = **0.9920**, $\alpha_T = 1 - W_B^2/2L_B^2$ = **0.99940**, and $\alpha_F = \gamma\alpha_T$ = **0.9914**, which agrees with $\beta_F/(1 + \beta_F)$ to the fourth digit.

### Solution 09-07.5

(a) $D_B$ = 6.807 cm²/s at 10¹⁸ cm⁻³.

- At $N_E$ = 10¹⁹: $D_E$ = 1.457 cm²/s, and $\beta_F = 6.807 \times 10^{19}/(1.457 \times 10^{18} \times e^{0.050/V_T})$ = **6.75**.
- At $N_E$ = 10²⁰: $D_E$ = 1.279 cm²/s, and $\beta_F$ = **13.49**.

(b) The gain rises by only **2.00**. Tenfold doping alone would raise the gain tenfold, but the extra narrowing, $e^{-(0.095 - 0.050)/V_T}$, divides it by 5.70, and the lower hole mobility in the heavier emitter (smaller $D_E$) raises it by 1.139: $10/5.70 \times 1.139$ = 2.00. (The low absolute gains come from $W_E = W_B$; real emitters are thicker.)

### Solution 09-07.6

(a) The gain scales as $D_B/N_B$: $27.0 \times (2.996/6.807) \times (10^{18}/10^{19})$ = **1.19**.

(b) $\Delta E_{gB} = V_T\ln(100/1.19)$ = **0.115** eV, a little more than the 0.1 eV of 20% germanium.

### Solution 09-07.7

(a) With $W = \sqrt{2\varepsilon_s(V_{bi} + 2)(1/N_B + 1/N_C)/q}$, $x_{pB} = WN_C/(N_B + N_C)$, $C' = \varepsilon_s/W$ and $V_A = qN_BW_B/C'$:

| $N_C$ (cm⁻³) | $V_{bi}$ (V) | $W$ (µm) | base side (nm) | $C'$ (fF/µm²) | $V_A$ (V) |
|---|---|---|---|---|---|
| 3 × 10¹⁶ | **0.8618** | **0.3565** | **10.4** | **0.291** | **55.1** |
| 10¹⁷ | 0.8929 | 0.2029 | 18.4 | 0.511 | 31.4 |
| 10¹⁸ | **0.9524** | **0.0874** | **43.7** | **1.186** | **13.5** |

Lighter collector doping moves the depletion region out of the base, raising $V_A$ and lowering the capacitance.

(b) The base-side edge is at **10.2** nm at 0 V and **26.3** nm at 5 V, a move of **16.1** nm. With $W_B$ = 0.1 µm at 2 V, $I_C \propto 1/W_B$ rises by a factor of **1.174** from 0 to 5 V. The linear estimate $1 + 5/31.4$ = **1.159** is close; the difference is because $V_A$ itself varies with bias.

### Solution 09-07.8

(a) $V_{bi,EB} = V_T\ln(10^{20} \times 2\times10^{17}/10^{20})$ = **1.030** V. At 0.7 V forward, the depletion region extends **46.1** nm into the base.

(b) $V_{bi,BC}$ = **0.7918** V; at $V_{CB}$ = 0 the base side is **15.6** nm, so the neutral base is 150 − 46.1 − 15.6 = **88.2** nm.

(c) Root finding on $x_{pE} + x_{pC}(V_{CB})$ = 0.15 µm gives $V_{CB}$ = **34.2** V.

(d) A one-sided junction on 10¹⁶ cm⁻³ avalanches near **54.7** V (Example 09-06.7), so punch-through comes first. At punch-through, the emitter–base barrier is pulled down by the collector, and current flows uncontrolled. A heavier or wider base, or a lighter collector, would be needed for higher ratings.

### Solution 09-07.9

(a) $\alpha_R = 1/2$, so $V_{CE,\text{sat}} = V_T\ln[(2 + \beta_f)/(1 - \beta_f/80)]$:

- **52.0** mV for $\beta_f$ = 5;
- **87.3** mV for $\beta_f$ = 20;
- **127.5** mV for $\beta_f$ = 50.

The closer the forced gain gets to $\beta_F$, the less saturated the transistor and the higher $V_{CE}$.

(b) With $x = e^{0.7/V_T}$ and $y = e^{0.6/V_T}$: $I_C$ = **55.07** µA and $I_B$ = **1.919** µA, so $I_C/I_B$ = **28.7**. The forward-active value would be **57.48** µA. At 0.1 V the transistor is moderately saturated: collector injection removes **4.2**% of the collector current, the forced gain of 28.7 is far below $\beta_F$ = 80, and the base current is **2.67** times its forward-active value $57.48/80$ µA.

### Solution 09-07.10

(a) $n_{B0}e^{V_{BE}/V_T} = N_B$ at $V_{BE} = 2V_T\ln(N_B/n_i)$ = **0.9524** V. The ideal current there is $qA_ED_BN_B/W_B$ = **10.9** mA.

(b) Solving the quadratic gives $n'(0)$ = **2.06 × 10¹⁸** cm⁻³ and $I_C = qA_ED_Bn'(0)/W_B$ = **22.5** mA, against an ideal **68.7** mA. Above the knee the current grows as $e^{V_{BE}/2V_T}$. (A full analysis also doubles the effective diffusion coefficient at high injection, the Webster effect, which this simple model omits.)

### Solution 09-07.11

(a) $D_B = V_T\mu_n(10^{19})$ = 2.996 cm²/s and $\tau_B = (3\times10^{-6})^2/(2 \times 2.996)$ = **1.502** ps.

(b) $\xi = 0.15/0.025852$ = **5.802**. The drift factor $[1 - (1 - e^{-\xi})/\xi]/\xi$ = **0.1427**, so $\tau_B$ = **0.429** ps. The field is 0.15 V/30 nm = **5.0 × 10⁴** V/cm.

(c) $\tau_C = 0.15\ \mu\text{m}/(2 \times 1.07\times10^7\text{ cm/s})$ = **0.701** ps.

(d) $f_T = 1/(2\pi(\tau_B + \tau_C))$: **72.3** GHz uniform and **140.9** GHz graded. Once the base is graded, the collector transit dominates; record devices also thin the collector and dope it heavily, accepting the Kirk and breakdown penalties.

### Solution 09-07.12

(a) The hybrid-π parameters:

- $g_m = 0.2\text{ mA}/V_T$ = **7.736** mS;
- $r_\pi = 120/g_m$ = **15.51** kΩ;
- $r_o = 40/0.2\text{ mA}$ = **200** kΩ;
- $C_\pi = \tau_Fg_m + C_{jE}$ = **20.47** fF;
- intrinsic gain $V_A/V_T$ = **1547**.

(b) $f_T = 1/(2\pi[2\text{ ps} + 8\text{ fF} \times V_T/0.2\text{ mA}])$ = **52.5** GHz, below the **79.6** GHz transit-time limit.

(c) $(C_{jE} + C_{jC})V_T/I_C = \tau_F$ at $I_C$ = **0.103** mA. Low-power biasing costs speed through depletion charging, not through the transit time.

### Solution 09-07.13

(a) $r_b = f_T/(8\pi C_{jC}f_{\max}^2) = 3\times10^{11}/(8\pi \times 2\times10^{-15} \times 2.5\times10^{23})$ = **23.9** Ω.

(b) $f_{\max} = \sqrt{3\times10^{11}/(8\pi \times 50 \times 2\times10^{-15})}$ = **345** GHz.

(c) $f_{\max} \propto r_b^{-1/2}$, so a fourfold reduction raises it by a factor of **2**.

### Solution 09-07.14

(a) $N_C = J_K/(qv_{\text{sat}}) = 3\times10^5/(1.602\times10^{-19} \times 1.07\times10^7)$ = **1.75 × 10¹⁷** cm⁻³.

(b) At $V_{CB}$ = 1 V:

- $N_C$ = 10¹⁷: $C'$ = **0.631** fF/µm² and $V_A$ = **25.4** V;
- $N_C$ = 1.75 × 10¹⁷: $C'$ = **0.805** fF/µm² and $V_A$ = **19.9** V.

(c) Raising the Kirk current by **75**% costs **27**% more base–collector capacitance (which lowers $f_{\max}$ and adds Miller feedback) and **22**% less Early voltage (less intrinsic gain), and also lowers the collector breakdown voltage. Designers pick collector doping per product: high-speed variants dope it heavily, high-voltage variants lightly.

### Solution 09-07.15

(a) $\tau_F\beta_F$ = **1.00** ns. To saturate at all, $\beta_FI_B$ must exceed 2 mA: $I_B$ > **40.0** µA.

(b) $t_{\text{on}} = \tau_F\beta_F\ln[\beta_FI_B/(\beta_FI_B - I_C)]$ = 0.5 ns requires $\beta_FI_B = I_Ce^{0.5}/(e^{0.5} - 1)$ = **5.08** mA, so $I_B$ = **101.7** µA, **2.54** times the minimum.

(c) At the edge of saturation $Q_F = I_C\tau_F$ = **40.0** fC. The base current could sustain $I_B\tau_F\beta_F$ = **101.7** fC, so up to **61.7** fC of excess charge accumulates in saturation and must be removed before turn-off. Faster turn-on by overdrive is paid for in slower turn-off.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 09-07.1a | V_CE, forward active | 2.75 | V |
| 09-07.1b | V_CE, saturation | 0.15 | V |
| 09-07.1c | V_CE, cutoff | 2.5 | V |
| 09-07.1d | V_CE, reverse active | -1.7 | V |
| 09-07.2a | μ_n at 5e18 | 136.2 | cm²/V·s |
| 09-07.2b | D_B | 3.521 | cm²/s |
| 09-07.2c | I_S | 9.03e-20 | A |
| 09-07.2d | V_BE at 100 µA | 0.8955 | V |
| 09-07.2e | Gummel number | 7.10e12 | s/cm⁴ |
| 09-07.2f | base dopants per area | 2.5e13 | cm⁻² |
| 09-07.3a | α_F for β 150 | 0.9934 | — |
| 09-07.3b | β_F for α 0.995 | 199 | — |
| 09-07.3c | I_B | 13.25 | µA |
| 09-07.3d | I_C | 1.987 | mA |
| 09-07.4a | D_B at 1e17 | 20.72 | cm²/s |
| 09-07.4b | D_E at 1e19 | 1.457 | cm²/s |
| 09-07.4c | narrowing factor, 50 meV | 6.918 | — |
| 09-07.4d | emitter-injection limit | 123.3 | — |
| 09-07.4e | L_B | 14.39 | µm |
| 09-07.4f | transport limit | 1657 | — |
| 09-07.4g | β_F | 115 | — |
| 09-07.4h | γ | 0.9920 | — |
| 09-07.4i | α_T | 0.99940 | — |
| 09-07.4j | α_F | 0.9914 | — |
| 09-07.5a | β_F, N_E 1e19 | 6.75 | — |
| 09-07.5b | β_F, N_E 1e20 | 13.49 | — |
| 09-07.5c | gain ratio | 2.00 | — |
| 09-07.5d | extra narrowing factor | 5.70 | — |
| 09-07.6a | β_F with 1e19 silicon base | 1.19 | — |
| 09-07.6b | base narrowing for β 100 | 0.115 | eV |
| 09-07.7a | V_bi, N_C 3e16 | 0.8618 | V |
| 09-07.7b | W, N_C 3e16 | 0.3565 | µm |
| 09-07.7c | base side, N_C 3e16 | 10.4 | nm |
| 09-07.7d | C', N_C 3e16 | 0.291 | fF/µm² |
| 09-07.7e | V_A, N_C 3e16 | 55.1 | V |
| 09-07.7f | V_bi, N_C 1e18 | 0.9524 | V |
| 09-07.7g | W, N_C 1e18 | 0.0874 | µm |
| 09-07.7h | base side, N_C 1e18 | 43.7 | nm |
| 09-07.7i | C', N_C 1e18 | 1.186 | fF/µm² |
| 09-07.7j | V_A, N_C 1e18 | 13.5 | V |
| 09-07.7k | base-side edge at 0 V | 10.2 | nm |
| 09-07.7l | base-side edge at 5 V | 26.3 | nm |
| 09-07.7m | edge movement | 16.1 | nm |
| 09-07.7n | I_C ratio 5 V/0 V | 1.174 | — |
| 09-07.7o | linear estimate | 1.159 | — |
| 09-07.8a | V_bi emitter–base | 1.030 | V |
| 09-07.8b | E–B depletion in base | 46.1 | nm |
| 09-07.8c | V_bi base–collector | 0.7918 | V |
| 09-07.8d | B–C depletion in base at 0 V | 15.6 | nm |
| 09-07.8e | neutral base at 0 V | 88.2 | nm |
| 09-07.8f | punch-through voltage | 34.2 | V |
| 09-07.8g | avalanche voltage from 09-06 | 54.7 | V |
| 09-07.9a | V_CE,sat, β_f 5 | 52.0 | mV |
| 09-07.9b | V_CE,sat, β_f 20 | 87.3 | mV |
| 09-07.9c | V_CE,sat, β_f 50 | 127.5 | mV |
| 09-07.9d | I_C at 0.1 V | 55.07 | µA |
| 09-07.9e | I_B at 0.1 V | 1.919 | µA |
| 09-07.9f | I_C/I_B at 0.1 V | 28.7 | — |
| 09-07.9g | forward-active I_C | 57.48 | µA |
| 09-07.9i | base current relative to forward-active | 2.67 | — |
| 09-07.9h | current lost to collector injection | 4.2 | % |
| 09-07.10a | knee voltage | 0.9524 | V |
| 09-07.10b | ideal current at the knee | 10.9 | mA |
| 09-07.10c | n'(0) at 1.0 V | 2.06e18 | cm⁻³ |
| 09-07.10d | I_C at 1.0 V | 22.5 | mA |
| 09-07.10e | ideal I_C at 1.0 V | 68.7 | mA |
| 09-07.11a | uniform transit time | 1.502 | ps |
| 09-07.11b | ξ | 5.802 | — |
| 09-07.11c | drift factor | 0.1427 | — |
| 09-07.11d | graded transit time | 0.429 | ps |
| 09-07.11e | built-in field | 5.0e4 | V/cm |
| 09-07.11f | collector transit time | 0.701 | ps |
| 09-07.11g | f_T uniform | 72.3 | GHz |
| 09-07.11h | f_T graded | 140.9 | GHz |
| 09-07.12a | g_m | 7.736 | mS |
| 09-07.12b | r_π | 15.51 | kΩ |
| 09-07.12c | r_o | 200 | kΩ |
| 09-07.12d | C_π | 20.47 | fF |
| 09-07.12e | intrinsic gain | 1547 | — |
| 09-07.12f | f_T | 52.5 | GHz |
| 09-07.12g | transit-time limit | 79.6 | GHz |
| 09-07.12h | current for equal delays | 0.103 | mA |
| 09-07.13a | r_b for 500 GHz | 23.9 | Ω |
| 09-07.13b | f_max at 50 Ω | 345 | GHz |
| 09-07.13c | f_max factor | 2 | — |
| 09-07.14a | N_C for 3 mA/µm² | 1.75e17 | cm⁻³ |
| 09-07.14b | C' at 1e17, 1 V | 0.631 | fF/µm² |
| 09-07.14c | V_A at 1e17, 1 V | 25.4 | V |
| 09-07.14d | C' at 1.75e17, 1 V | 0.805 | fF/µm² |
| 09-07.14e | V_A at 1.75e17, 1 V | 19.9 | V |
| 09-07.14f | Kirk current increase | 75 | % |
| 09-07.14g | capacitance increase | 27 | % |
| 09-07.14h | Early voltage decrease | 22 | % |
| 09-07.15a | τ_F β_F | 1.00 | ns |
| 09-07.15b | minimum I_B | 40.0 | µA |
| 09-07.15c | β_F I_B for 0.5 ns | 5.08 | mA |
| 09-07.15d | I_B for 0.5 ns | 101.7 | µA |
| 09-07.15e | charge at saturation edge | 40.0 | fC |
| 09-07.15f | sustainable charge | 101.7 | fC |
| 09-07.15g | excess charge | 61.7 | fC |
| 09-07.15h | I_B over the minimum | 2.54 | — |
