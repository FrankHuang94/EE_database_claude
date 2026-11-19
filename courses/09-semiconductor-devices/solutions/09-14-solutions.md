# Solutions 09-14 · Optoelectronic Devices

Problems: [09-14 problems](../problems/09-14-problems.md) · Chapter: [09-14](../chapters/09-14-optoelectronic-devices.md). Every number below is recomputed by [verify_09_14.py](../verify/verify_09_14.py), by these routes:

- photon quantities from CODATA constants;
- the dead-time model by a seeded event simulation, checked against the formula;
- the solar-cell operating points by root finding on the implicit diode equation and numerical maximization.

---

## Solutions

### Solution 09-14.1

$\lambda_c = 1.2398/0.661$ = **1.876** µm, so germanium does absorb 1.55 µm light (0.800 eV > 0.661 eV). At 1.31 µm, $\mathcal R = 0.7 \times 1.31/1.2398$ = **0.740** A/W.

### Solution 09-14.2

Each photon carries 0.800 eV = **1.28 × 10⁻¹⁹** J, so 10 µW is **7.80 × 10¹³** photons per second. The photocurrent is $\eta q\Phi$ = 0.8 × 1.602 × 10⁻¹⁹ × 7.80 × 10¹³ = **10.0** µA (a responsivity of **1.00** A/W).

### Solution 09-14.3

Absorbed fraction: $1 - e^{-\alpha d} = 1 - e^{-1}$ = **0.632**. Quantum efficiency: 0.70 × 0.632 = **0.442** bare, and 0.98 × 0.632 = **0.619** coated. Anti-reflection coating is the cheapest 40% gain in any optical detector.

### Solution 09-14.4

$A = \pi(25\text{ µm})^2$ = **1.96 × 10⁻⁵** cm², $C = \varepsilon_sA/W$ = **0.102** pF, and $f_{RC} = 1/(2\pi \times 50 \times C)$ = **31.3** GHz. A wider depletion region lowers $C$ but lengthens the carrier transit time, the other bandwidth limit.

### Solution 09-14.5

The rms noise current is $1\text{ pA}/\sqrt{\text{Hz}} \times \sqrt{10^9\text{ Hz}}$ = **31.6** nA. A 5 nA signal has SNR = **0.158**, buried in noise. With a gain of 20 the signal current is 100 nA and SNR = **3.16**, before accounting for the excess noise of the avalanche. That is the case for APDs in fast, sensitive receivers.

### Solution 09-14.6

Maximum count rate $1/\tau$ = **10⁸** s⁻¹. Recorded rate $m$ = 5 × 10⁷/(1 + 0.5) = **3.33 × 10⁷** s⁻¹: a third of the events are lost. Ambient: 10⁶ s⁻¹ × 1 ns = **0.001** per window (a Poisson mean this small is also the probability).

### Solution 09-14.7

$d_{\max} = c/2f$: **150** m at 1 MHz and **15.0** m at 10 MHz. Faster pulsing collects photons faster but shortens the unambiguous range, unless pulses are coded.

### Solution 09-14.8

$N_{FW}$ = 6000 × (0.8/1.4)² = **1959** electrons. $\text{SNR}_{\max} = \sqrt{1959}$ = **44.3** (**32.9** dB), and $\text{DR}$ = 20 log₁₀(1959/1.5) = **62.3** dB.

### Solution 09-14.9

The signal is 80 electrons. Shot noise (80) and read noise (4) add in quadrature: SNR = 80/√84 = **8.73**, or **18.8** dB. At such low light, every electron of read noise matters.

### Solution 09-14.10

$h\nu = 1.2398/0.63$ = **1.968** eV, electrical efficiency 1.968/2.1 = **0.937**, and wall-plug efficiency 0.85 × 0.7 × 0.937 = **0.558**.

### Solution 09-14.11

(a) $L = \ln(1/R^2)/[2(g_{th} - \alpha_i)]$ = ln(1/0.09)/(2 × 30 cm⁻¹) = **401** µm.

(b) Period $= \lambda_0/(2n)$ = 850/(2 × 3.2) = **132.8** nm.

### Solution 09-14.12

(a) With $R_s$ = 1 Ω·cm², solving the implicit equation and maximizing $VJ$ gives $V_{mp}$ = **0.5729** V, $J_{mp}$ = **38.16** mA/cm², $P_{\max}$ = **21.86** mW/cm², $FF$ = **0.791** and efficiency **21.9**%: one ohm·cm² costs about 1.5 percentage points. $V_{oc}$ is unchanged, because no current flows at open circuit.

(b) At 100 suns: $V_{oc}$ = **0.8097** V, a rise of $V_T\ln 100$ = **0.119** V. The fill factor rises to **0.862**, and the efficiency to **27.9**%. The current is 100 times larger, so the $I^2R$ loss in any series resistance is 10⁴ times larger per unit area: concentrator cells need extremely low series resistance and good cooling.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 09-14.1a | Ge cutoff | 1.876 | µm |
| 09-14.1b | Ge responsivity at 1.31 µm | 0.740 | A/W |
| 09-14.2a | photon rate | 7.80e13 | s⁻¹ |
| 09-14.2b | photocurrent | 10.0 | µA |
| 09-14.2c | photon energy | 1.28e-19 | J |
| 09-14.2d | responsivity | 1.00 | A/W |
| 09-14.3a | absorbed fraction | 0.632 | — |
| 09-14.3b | η, bare | 0.442 | — |
| 09-14.3c | η, coated | 0.619 | — |
| 09-14.4a | area | 1.96e-5 | cm² |
| 09-14.4b | capacitance | 0.102 | pF |
| 09-14.4c | RC bandwidth | 31.3 | GHz |
| 09-14.5a | amplifier noise current | 31.6 | nA |
| 09-14.5b | SNR without gain | 0.158 | — |
| 09-14.5c | SNR with M = 20 | 3.16 | — |
| 09-14.6a | maximum count rate | 1e8 | s⁻¹ |
| 09-14.6b | recorded rate | 3.33e7 | s⁻¹ |
| 09-14.6c | ambient probability per 1 ns | 0.001 | — |
| 09-14.7a | range at 1 MHz | 150 | m |
| 09-14.7b | range at 10 MHz | 15.0 | m |
| 09-14.8a | full well, 0.8 µm | 1959 | e⁻ |
| 09-14.8b | maximum SNR | 44.3 | — |
| 09-14.8c | maximum SNR | 32.9 | dB |
| 09-14.8d | dynamic range | 62.3 | dB |
| 09-14.9a | SNR | 8.73 | — |
| 09-14.9b | SNR | 18.8 | dB |
| 09-14.10a | photon energy | 1.968 | eV |
| 09-14.10b | electrical efficiency | 0.937 | — |
| 09-14.10c | wall-plug efficiency | 0.558 | — |
| 09-14.11a | cavity length | 401 | µm |
| 09-14.11b | DBR period | 132.8 | nm |
| 09-14.12a | V_mp with R_s | 0.5729 | V |
| 09-14.12b | J_mp with R_s | 38.16 | mA/cm² |
| 09-14.12c | P_max with R_s | 21.86 | mW/cm² |
| 09-14.12d | FF with R_s | 0.791 | — |
| 09-14.12e | efficiency with R_s | 21.9 | % |
| 09-14.12f | V_oc at 100 suns | 0.8097 | V |
| 09-14.12g | V_oc rise | 0.119 | V |
| 09-14.12h | FF at 100 suns | 0.862 | — |
| 09-14.12i | efficiency at 100 suns | 27.9 | % |
