# Solutions 09-04 · Generation, Recombination and the Continuity Equation

Problems: [09-04 problems](../problems/09-04-problems.md) · Chapter: [09-04](../chapters/09-04-generation-recombination-continuity.md). Every number below is recomputed by [verify_09_04.py](../verify/verify_09_04.py): SRH rates from the trap's steady-state occupation solved numerically, transients by integrating the rate equations, spatial profiles by solving the boundary-value problems with finite differences, and temperatures by root finding.

---

## Solutions

### Solution 09-04.1

(a) $\tau_{\text{SRH}} = 1/(10^{-15} \times 2.3\times10^7 \times 5\times10^{11})$ = **87.0** µs.

(b) $\tau_{\text{rad}} = 1/(1.1\times10^{-14} \times 10^{16})$ = **9.09** ms.

(c) $\tau_{\text{Auger}} = 1/(0.3\times10^{-30} \times 10^{32})$ = **33.3** ms.

(d) $1/\tau = 1/87.0 + 1/9090 + 1/33\,300$ (µs⁻¹): $\tau$ = **85.9** µs, SRH-limited.

### Solution 09-04.2

(a) $\Delta E_{Fn} = kT\ln[(N_D + \Delta n)/N_D]$ = **0.0517** meV: negligible.

(b) $p_0 = n_i^2/N_D = 2\times10^4$ cm⁻³, so $p/p_0 \approx 10^{13}/(2\times10^4)$ = **5 × 10⁸**.

(c) $U = \Delta p/\tau_p$ = **5 × 10¹⁸** cm⁻³ s⁻¹. Low-level injection holds: the excess is 0.2% of the doping.

### Solution 09-04.3

(a) $\Delta p = 5\times10^{20} \times 2\times10^{-6}$ = **10¹⁵** cm⁻³, equal to the doping.

(b) No: the excess equals $N_D$, so the majority density doubles, $\Delta p^2$ terms matter and the lifetime itself changes (for mid-gap SRH it rises toward $\tau_{n0} + \tau_{p0}$ at high injection, and Auger terms grow). The steady state must be found from the full rate expression, and conductivity modulation (the rise of the majority density) becomes important, as it does in power diodes conducting heavily.

### Solution 09-04.4

$n_1 = n_ie^{0.25/0.02585}$ = **1.58 × 10¹⁴** cm⁻³ and $p_1 = n_i^2/n_1$, negligible. Under low injection in n-type, $\tau = \tau_{p0}(n_0 + n_1)/n_0 + \tau_{n0}p_1/n_0$.

(a) $N_D$ = 10¹⁵: $\tau = 1\ \mu\text{s} \times (1 + 0.158)$ = **1.158** µs.

(b) $N_D$ = 10¹⁴: $\tau = 1\ \mu\text{s} \times (1 + 1.58)$ = **2.58** µs.

(c) When $n_1$ becomes comparable with $n_0$, an electron captured by the trap is likely to be re-emitted to the conduction band before a hole arrives, so many captures are wasted and the lifetime grows. A mid-gap trap has $n_1 = n_i$, negligible against any practical doping, so nearly every capture leads to recombination and the lifetime is simply $\tau_{p0}$.

### Solution 09-04.5

$I = qn_iWA/2\tau_0 = 1.602\times10^{-19} \times 10^{10} \times 2\times10^{-4} \times 10^{-2}/(2 \times 10^{-5})$ = **1.60 × 10⁻¹⁰** A (160 pA), a current density of **1.60 × 10⁻⁸** A/cm².

### Solution 09-04.6

(a) $\Delta E_{Fp} = kT\ln(1.01)$ = **0.257** meV.

(b) $n \approx 10^{15}$ cm⁻³, so $E_{Fn} - E_i = kT\ln(n/n_i)$ = **0.2976** eV.

(c) $E_{Fn} - E_{Fp} = kT\ln(np/n_i^2)$ = **0.7146** eV.

(d) Dark: $E_i - E_F = kT\ln(10^7)$ = **0.4167** eV. Under light the electron level moved from 0.4167 eV below $E_i$ to 0.2976 eV above it.

### Solution 09-04.7

(a) $d\Delta p/dt = G_L - \Delta p/\tau_p$ with $\Delta p(0) = 0$ gives $\Delta p(t) = G_L\tau_p(1 - e^{-t/\tau_p})$ (02-02).

(b) Final excess $G_L\tau_p$ = **5 × 10¹⁴** cm⁻³; 90% is reached at $t = \tau_p\ln10$ = **11.5** µs.

### Solution 09-04.8

$\mu_n(10^{16})$ = **1248** cm²/V·s, $D_n = 0.025852 \times 1248$ = **32.26** cm²/s, $L_n = \sqrt{32.26 \times 10^{-5}}$ cm = **179.6** µm, and $J_n = qD_n\Delta n(0)/L_n$ = **2.88** mA/cm².

### Solution 09-04.9

(a) $D_n = 0.025852 \times 801.3$ = **20.72** cm²/s and $L_n = \sqrt{20.72 \times 10^{-7}}$ cm = **14.39** µm.

(b) $L_n/W$ = **28.8**: a short base.

(c) $W^2/2L_n^2$ = **6.0 × 10⁻⁴**: 0.06% of electrons recombine.

(d) $W^2/2D_n$ = **60.3** ps.

### Solution 09-04.10

(a) In steady state, $D_p\Delta p'' - \Delta p/\tau_p + G_L = 0$. The particular solution is $G_L\tau_p$ and the decaying homogeneous solution $e^{-x/L_p}$, so $\Delta p = G_L\tau_p(1 - Ae^{-x/L_p})$. At the surface, holes flowing toward it ($x$ decreasing) recombine there: $D_p\Delta p'(0) = S\Delta p(0)$, i.e. $D_pG_L\tau_pA/L_p = SG_L\tau_p(1 - A)$, so $A = S/(S + D_p/L_p)$.

(b) $D_p$ = 11.21 cm²/s and $L_p$ = 33.48 µm (Example 09-04.6), so $D_p/L_p$ = **3348** cm/s. For $S$ = 10⁴ cm/s: $A$ = **0.749** and $\Delta p(0)/G_L\tau_p$ = **0.251**. For $S$ = 10 cm/s: $A$ = **0.00298** and $\Delta p(0)/G_L\tau_p$ = **0.997**. (Here $G_L\tau_p$ = 10¹³ cm⁻³.)

(c) A bad surface drains three quarters of the excess at the surface and depletes carriers within a diffusion length of it, exactly where sunlight generates most carriers. Passivation, cutting $S$ far below $D_p/L_p$, keeps them for collection.

### Solution 09-04.11

(a) $2S/W = 2 \times 10/0.03$ = 666.7 s⁻¹, so $\tau_{\text{eff}} = 1/(1000 + 666.7)$ s = **600** µs.

(b) $SW/2D_p = 10 \times 0.03/(2 \times 11.21)$ = **0.0134** ≪ 1, so the carriers stay nearly uniform across the wafer and the simple formula holds.

(c) Even this good passivation lowers the reported lifetime from 1 ms to 600 µs; an unpassivated surface ($S$ ~ 10⁴ cm/s) would hide the bulk entirely (the lab finds about 9 µs). Testers passivate both surfaces so the measurement reflects the bulk.

### Solution 09-04.12

(a) $\tau = 1/(C_nN_D^2) = 1/(1.1\times10^{-30} \times 10^{40})$ = **90.9** ps.

(b) $\mu_p(10^{20})$ = **49.5** cm²/V·s, $D_p$ = **1.279** cm²/s, $L_p = \sqrt{1.279 \times 9.09\times10^{-11}}$ cm = **107.8** nm.

(c) The diffusion length is about half the emitter depth, so the emitter is neither cleanly long nor short; most injected holes recombine inside it, which is one reason heavily doped emitters limit bipolar gain and solar-cell voltage (09-07, 09-14).

### Solution 09-04.13

$N_t = 1/(\sigma_pv_{th,p}\tau_p) = 1/(9.0\times10^{-15} \times 1.65\times10^7 \times 5\times10^{-8})$ = **1.35 × 10¹⁴** cm⁻³.

### Solution 09-04.14

With $J_{\text{gen}} \propto n_i$ and $J_{\text{diff}} \propto n_i^2$, their ratio scales as $1/n_i$: it falls from 100 to 1 when $n_i$ has grown 100-fold. Solving $n_i(T)/n_i(300\ \text{K})$ = 100 gives $T$ = **367.8** K (**94.7** °C).

### Solution 09-04.15

(a) $\tau_{\text{rad}} = 1/(7\times10^{-10} \times 10^{17})$ = **14.3** ns.

(b) $1/\tau = 1/14.3 + 1/10$ (ns⁻¹): $\tau$ = **5.88** ns.

(c) $\eta = (1/\tau_{\text{rad}})/(1/\tau)$ = **0.412**: 41% of recombinations emit light. LED makers raise it by lowering defect density (longer $\tau_{\text{SRH}}$) and by heterostructures that confine carriers (09-14).

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 09-04.1a | SRH lifetime | 87.0 | µs |
| 09-04.1b | radiative lifetime | 9.09 | ms |
| 09-04.1c | Auger lifetime | 33.3 | ms |
| 09-04.1d | combined lifetime | 85.9 | µs |
| 09-04.2a | shift of E_Fn | 0.0517 | meV |
| 09-04.2b | rise of the hole density | 5e8 | — |
| 09-04.2c | net recombination rate | 5e18 | cm⁻³ s⁻¹ |
| 09-04.2d | excess as fraction of doping | 0.2 | % |
| 09-04.3a | predicted excess | 1e15 | cm⁻³ |
| 09-04.4a | n_1 | 1.58e14 | cm⁻³ |
| 09-04.4b | lifetime at 1e15 | 1.158 | µs |
| 09-04.4c | lifetime at 1e14 | 2.58 | µs |
| 09-04.5a | generation current | 1.60e-10 | A |
| 09-04.5b | generation current density | 1.60e-8 | A/cm² |
| 09-04.6a | shift of E_Fp | 0.257 | meV |
| 09-04.6b | E_Fn − E_i | 0.2976 | eV |
| 09-04.6c | splitting | 0.7146 | eV |
| 09-04.6d | E_i − E_F in the dark | 0.4167 | eV |
| 09-04.7a | final excess | 5e14 | cm⁻³ |
| 09-04.7b | time to 90% | 11.5 | µs |
| 09-04.8a | μ_n at 1e16 | 1248 | cm²/V·s |
| 09-04.8b | D_n | 32.26 | cm²/s |
| 09-04.8c | L_n | 179.6 | µm |
| 09-04.8d | electron current density | 2.88 | mA/cm² |
| 09-04.9a | D_n at 1e17 | 20.72 | cm²/s |
| 09-04.9b | L_n | 14.39 | µm |
| 09-04.9c | L_n/W | 28.8 | — |
| 09-04.9d | fraction recombining | 6.0e-4 | — |
| 09-04.9e | transit time | 60.3 | ps |
| 09-04.10a | D_p/L_p | 3348 | cm/s |
| 09-04.10b | A for S = 1e4 | 0.749 | — |
| 09-04.10c | surface excess ratio, S = 1e4 | 0.251 | — |
| 09-04.10d | A for S = 10 | 0.00298 | — |
| 09-04.10e | surface excess ratio, S = 10 | 0.997 | — |
| 09-04.10f | G_L τ_p | 1e13 | cm⁻³ |
| 09-04.11a | effective lifetime | 600 | µs |
| 09-04.11b | S W/2D_p | 0.0134 | — |
| 09-04.12a | Auger lifetime at 1e20 | 90.9 | ps |
| 09-04.12b | μ_p at 1e20 | 49.5 | cm²/V·s |
| 09-04.12c | D_p at 1e20 | 1.279 | cm²/s |
| 09-04.12d | L_p at 1e20 | 107.8 | nm |
| 09-04.13a | gold concentration | 1.35e14 | cm⁻³ |
| 09-04.14a | crossover temperature | 367.8 | K |
| 09-04.14b | crossover in °C | 94.7 | °C |
| 09-04.15a | GaAs radiative lifetime | 14.3 | ns |
| 09-04.15b | combined lifetime | 5.88 | ns |
| 09-04.15c | internal radiative efficiency | 0.412 | — |
