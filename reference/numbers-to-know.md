# Numbers to Know

Typical real-world values an electrical engineer carries in their head. Each chapter's "Numbers to know" section feeds this page. Perishable values (anything that changes with technology generations, standards or markets) carry an **as-of date** and a research-log ID; physical constants and mathematical facts do not.

## Constants and mathematical facts

| Quantity | Value | Notes |
|---|---|---|
| $e$ | 2.71828 | |
| $\ln 2$ | 0.6931 | Half-life of a first-order decay is $\tau\ln 2$ |
| $\ln 9$ | 2.1972 | 10–90 % rise time of a single pole is $\tau\ln 9$ |
| 1 rad | 57.296° | |
| $1 - e^{-1}$ | 0.632 | Fraction of a first-order step completed after one time constant |
| $q$ | $1.602\times10^{-19}$ C | Elementary charge |
| $k$ | $1.381\times10^{-23}$ J/K | Boltzmann constant |
| $kT/q$ at 300 K | 25.85 mV | Thermal voltage $V_T$ |
| $\sqrt{kT/C}$, 1 pF, 300 K | 64.4 µV rms | kT/C noise ([R-009](research-log.md#r-009--ktc-noise)) |

## Frequencies

| Quantity | Value | As of / source |
|---|---|---|
| Power-grid frequency | 50 Hz or 60 Hz (Japan uses both) | [R-006](research-log.md#r-006--power-grid-frequencies) |
| 5G NR FR1 / FR2-1 / FR2-2 | 410–7125 MHz / 24.25–52.6 GHz / 52.6–71 GHz | Nov 2026, [R-003](research-log.md#r-003--3gpp-nr-frequency-ranges) |
| US 6 GHz unlicensed band | 5.925–7.125 GHz | Nov 2026, [R-007](research-log.md#r-007--us-6-ghz-unlicensed-band) |

## On-chip interconnect

| Quantity | Value | As of / source |
|---|---|---|
| Wire capacitance (rule of thumb) | ≈ 0.2 fF/µm | [R-004](research-log.md#r-004--on-chip-interconnect) |

<!-- BEGIN GENERATED (tools/build_reference.py): edit the chapters or glossary.yml, not this block -->

## By chapter

Each chapter's own *Numbers to know* table, in course order. Perishable values carry the chapter's as-of date and research-log ID; check the date before reusing a number. A bare number in brackets, such as [3], cites the Sources list of the chapter the row comes from.

## [00 · Orientation](../courses/00-orientation/README.md)

### [00-01 · The Map of Electrical Engineering](../courses/00-orientation/chapters/00-01-map-of-electrical-engineering.md)

| Quantity | Value | As of / source |
|---|---|---|
| Elementary charge | $1.602\times10^{-19}$ C | constant |
| 1 mAh | 3.6 C | definition |
| 1 Wh | 3600 J | definition |
| Landauer limit at 300 K | $2.87\times10^{-21}$ J per bit erased | physics |
| Global semiconductor sales, 2025 | US\$795.6 B (+26.2%) | Nov 2026, [R-016](research-log.md#r-016--global-semiconductor-market-wsts--sia) |
| Logic and memory share of 2025 market | 37.6% and 28.9% | Nov 2026, [R-016](research-log.md#r-016--global-semiconductor-market-wsts--sia) |
| R&D intensity of large chip companies | about 9% to 26% of revenue | Nov 2026, [R-017](research-log.md#r-017--rd-intensity-latest-fiscal-year-10-k--annual-reports) |

### [00-02 · The Abstraction Stack: Physics to Software](../courses/00-orientation/chapters/00-02-the-abstraction-stack.md)

| Quantity | Value | Note |
|---|---|---|
| Speed of light in vacuum | $3.00\times10^8$ m/s = 30 cm/ns | |
| Signal speed on FR-4 circuit board | ≈ 15 cm/ns ($\varepsilon_r \approx 4$) | Rule of thumb |
| Wavelength at 60 Hz / 1 GHz / 10 GHz (free space) | 5000 km / 30 cm / 3 cm | $\lambda = c/f$ |
| Lumped rule of thumb | size < λ/10, or line delay < $t_r/6$ | Authors vary between $t_r/4$ and $t_r/10$ |
| Reticle limit (max single-exposure die) | 26 mm × 33 mm ≈ 858 mm²; High-NA EUV: 26 mm × 16.5 mm | [R-015](research-log.md#r-015--lithography-exposure-field-the-reticle-limit) |
| $Q(3)$, $Q(6)$, $Q(10)$ | $1.35\times10^{-3}$, $9.87\times10^{-10}$, $7.62\times10^{-24}$ | How fast the Gaussian tail falls |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| N 00-02.a | λ at 1 GHz, free space | 30.0 | cm |
| N 00-02.b | reticle field area | 858 | mm² |
| N 00-02.c | High-NA field area | 429 | mm² |
| N 00-02.d | $Q(3)$ | 1.35×10^-3 | — |
| N 00-02.e | $Q(6)$ | 9.87×10^-10 | — |

### [00-03 · How to Study This Curriculum](../courses/00-orientation/chapters/00-03-how-to-study-this-curriculum.md)

| Quantity | Value | Source |
|---|---|---|
| Retrieval practice vs rereading, 1-week recall | 61% vs 40% | [R-021](research-log.md#r-021--learning-science-evidence) |
| Interleaved vs blocked, 1-week test | 63% vs 20% | [R-021](research-log.md#r-021--learning-science-evidence) |
| Reviews to retain a card for a year (ease 2.5) | about 7 | Example 00-03.4 |
| Daily Anki time at about 3 new cards/day | a few minutes | Example 00-03.4 |
| Mastery bar for a chapter | ≥ 80% of [A] and [B] problems unaided | This curriculum |

### [00-04 · Toolchain Setup Walkthrough](../courses/00-orientation/chapters/00-04-toolchain-walkthrough.md)

| Quantity | Value | Note |
|---|---|---|
| SPICE suffixes | f p n u m k meg g t = 10⁻¹⁵ … 10¹² | `m` = milli; `meg` = mega |
| Default SPICE relative tolerance | 10⁻³ (0.1%) | `reltol` |
| Double-precision machine epsilon | $2.22\times10^{-16}$ | about 16 significant digits |
| Test vectors for an $n$-input block | $2^n$ | 64 inputs → about 585 years at 10⁹ tests/s |
| Newton–Raphson near the solution | correct digits roughly double each step | quadratic convergence |

### [00-05 · How Chip Companies' Engineering Organizations Work](../courses/00-orientation/chapters/00-05-how-chip-companies-are-organized.md)

| Quantity | Value | As of / source |
|---|---|---|
| Fab processing time per mask layer | about 1–1.5 days | [R-020](research-log.md#r-020--fab-cycle-time-and-maskeuv-layer-counts) [Industry estimate] |
| Wafer cycle time, advanced processes | about 14–20 weeks | [R-020](research-log.md#r-020--fab-cycle-time-and-maskeuv-layer-counts) |
| IC/ASIC first-silicon success | 14% (2024), 5% (2026; method changed) | Nov 2026, [R-018](research-log.md#r-018--functional-verification-study-wilson-research-group--siemens-eda) |
| Share of project time in verification | about 49% (2026) | [R-018](research-log.md#r-018--functional-verification-study-wilson-research-group--siemens-eda) |
| Projects behind schedule | about 75% | [R-018](research-log.md#r-018--functional-verification-study-wilson-research-group--siemens-eda) |
| Leading-edge design-cost estimates | hundreds of millions of US$ (e.g., about \$725 M quoted for 2 nm, from scratch) | [Contested], [R-019](research-log.md#r-019--advanced-node-design-and-mask-cost-estimates-contested) |

## [01 · Calculus for Engineers](../courses/01-calculus-for-engineers/README.md)

### [01-01 · Functions, Models and Units](../courses/01-calculus-for-engineers/chapters/01-01-functions-models-and-units.md)

| Quantity | Value | Note |
|---|---|---|
| $e$ | 2.71828 | |
| $\ln 2$, $\ln 10$, $\log_{10}2$ | 0.6931, 2.3026, 0.3010 | |
| 3 dB / 10 dB / 20 dB | ≈ 2× / 10× / 100× power | Amplitude: 1.41×, 3.16×, 10× |
| 0 dBm / 30 dBm | 1 mW / 1 W | −30 dBm = 1 µW |
| Thermal voltage $V_T$ at 300 K | 25.85 mV | $kT/q$ |
| Diode/BJT slope at room temperature | ≈ 59.5 mV per decade of current | $V_T\ln 10$ |
| 1 rad | 57.30° | 60 Hz → $\omega$ = 377 rad/s |
| US 6 GHz Wi-Fi limits | 30 dBm (1 W) EIRP low-power indoor; 36 dBm (≈ 4 W) standard power | As of Nov 2026, [R-007](research-log.md#r-007--us-6-ghz-unlicensed-band) |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| N 01-01.a | 36 dBm in watts | 3.98 | W |
| N 01-01.b | 30 dBm in watts | 1.00 | W |
| N 01-01.c | 5 dBm/MHz in mW per MHz | 3.16 | mW/MHz |

### [01-02 · Limits and Continuity](../courses/01-calculus-for-engineers/chapters/01-02-limits-and-continuity.md)

| Quantity | Value | Note |
|---|---|---|
| $\sin x/x$ at $x = 0.1$ | 0.99833 | Limit 1; error ≈ $x^2/6$ |
| $(1 - \cos x)/x^2$ | → 0.5 | Basis of $\cos x \approx 1 - x^2/2$ |
| $(1 + 1/n)^n$ at $n = 12, 365$ | 2.613, 2.715 | Limit $e = 2.71828$ |
| $e^{-5}$ | 0.0067 | "Settled" after 5τ (within 0.7%) |
| Bisection gain | 10 steps ≈ 1024× ≈ 3 digits | Width $(b - a)/2^n$ |
| First-order filter at corner | −3.01 dB | Asymptote error is largest here |
| High-frequency roll-off per pole | −20 dB/decade | $\lvert H\rvert \sim f_c/f$ |
| Best step for a forward difference in double precision | $h \approx 10^{-8}$ | $\sqrt{\epsilon_{\text{mach}}}$ |
| Amdahl limit with parallel fraction $p$ | $1/(1 - p)$ | $p = 0.95$ → 20× maximum |

### [01-03 · Derivatives: Rates of Change in Circuits](../courses/01-calculus-for-engineers/chapters/01-03-derivatives.md)

| Quantity | Value | Note |
|---|---|---|
| Capacitor current at 1 µF and 1 V/µs | 1 A | $i = C\,dv/dt$: fast edges on big capacitors draw large currents |
| Inductor voltage at 1 µH and 1 A/µs | 1 V | $v = L\,di/dt$ |
| Diode/BJT small-signal resistance at 1 mA | ≈ 26 Ω | $V_T/I$; halves when current doubles |
| Current change per mV at a forward-biased junction | ≈ 3.9% | $1/V_T$ per volt |
| Full-power bandwidth | $SR/(2\pi V_p)$ | 0.3 V/µs and 10 V peak gives 4.8 kHz |
| LM358 slew rate | 0.3 V/µs typ. (0.5 V/µs for LM358B) | TI datasheet, as of Nov 2026 ([R-025](research-log.md#r-025--op-amp-slew-rate-and-bandwidth-ti-lm358)) |
| Best numerical step (double precision) | ≈ $10^{-8}$ forward, ≈ $10^{-5}$ central | Truncation vs rounding |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| N 01-03.a | small-signal resistance at 1 mA | 26 | Ω |
| N 01-03.b | full-power bandwidth, 0.3 V/µs, 10 V peak | 4.8 | kHz |

### [01-04 · Applications of Derivatives](../courses/01-calculus-for-engineers/chapters/01-04-applications-of-derivatives.md)

| Quantity | Value | Note |
|---|---|---|
| Maximum power transfer | $R_L = R_s$, $P_{max} = V_s^2/(4R_s)$, 50% efficiency | Signal, not power, delivery |
| Load error 2× from optimum | 89% of $P_{max}$ | Optima are flat |
| Minimum of $ax + b/x$ | at $\sqrt{b/a}$, value $2\sqrt{ab}$ | The two terms are equal there |
| Newton convergence | digits roughly double per step | Bisection: about 3.3 steps per digit |
| Newton reciprocal from an 8-bit seed to double precision | 3 iterations | 8 → 16 → 32 → 64 bits |
| Small-signal validity for a diode or BJT | swings ≪ $V_T$ ≈ 26 mV | 10% error at about 5 mV |
| Minimum-energy supply in subthreshold CMOS | a few hundred mV | Published studies ([R-027](research-log.md#r-027--subthreshold-and-near-threshold-operation)) |

### [01-05 · Integrals: Accumulating Charge and Energy](../courses/01-calculus-for-engineers/chapters/01-05-integrals.md)

| Quantity | Value | Note |
|---|---|---|
| 1 Ah | 3600 C | 1 mAh = 3.6 C |
| 1 kWh | 3.6 MJ | Electricity billing unit |
| Capacitor energy | ½CV² | 100 µF at 5 V = 1.25 mJ |
| Energy lost charging C from a fixed source | ½CV², any R | Half the source's CV² |
| Area under $Ae^{-t/\tau}$ from 0 to ∞ | $A\tau$ | The "equivalent rectangle" |
| Average of full-wave / half-wave rectified sine | $0.637V_m$ / $0.318V_m$ | $2/\pi$ and $1/\pi$ |
| Average of $\sin^2$ over a period | ½ | Why $P = \tfrac{1}{2}I_m^2R$ and RMS uses √2 |
| Trapezoid / Simpson error order | $h^2$ / $h^4$ | Halving h: ¼ / 1/16 of the error |
| Mains period (60 / 50 Hz) | 16.67 / 20 ms | Integration windows that reject hum |

### [01-06 · Techniques of Integration](../courses/01-calculus-for-engineers/chapters/01-06-techniques-of-integration.md)

| Quantity | Value | Note |
|---|---|---|
| $\int_0^\infty t^ne^{-t}\,dt$ | $n!$ | $\int_0^\infty te^{-t/\tau}dt = \tau^2$ |
| Elmore delay / 50% delay, single pole | 1.443 | $1/\ln 2$ |
| One-pole noise bandwidth | $(\pi/2)f_c$ ≈ 1.571 $f_c$ | 57% more noise power than $f_c$ suggests |
| Thermal noise density, 1 kΩ at 300 K | 4.07 nV/√Hz | $\sqrt{4kTR}$; scales as √R |
| kT/C noise at 1 pF, 300 K | 64.4 µV rms | Independent of R |
| Square-wave fundamental | $4/\pi$ ≈ 1.273 × amplitude; 81% of power | Harmonics $4/(n\pi)$, odd n |
| Gibbs overshoot | ≈ 9% of the jump | Does not shrink with more harmonics |
| p-integrals | $\int_1^\infty x^{-p}$ converges iff $p > 1$ | $1/f$: equal power per decade |

### [01-07 · Applications of Integration](../courses/01-calculus-for-engineers/chapters/01-07-applications-of-integration.md)

| Quantity | Value | Note |
|---|---|---|
| RMS of sine / square / triangle | 0.707 / 1 / 0.577 × peak | Crest factors 1.414 / 1 / 1.732 |
| Sine form factor | 1.111 | Average-responding meters assume it |
| PWM average / RMS | $D V_p$ / $\sqrt{D}V_p$ | Heating uses RMS |
| DC + ripple RMS | $\sqrt{V_{dc}^2 + V_{ac,rms}^2}$ | Orthogonal parts add in quadrature |
| Triangular ripple contribution | $\Delta^2/12$ to $I_{rms}^2$ | Δ = peak-to-peak |
| Usable energy from $V_1$ to $V_1/2$ | 75% of ½CV₁² | |
| 1 eV | $1.602\times10^{-19}$ J | Work on one electron through 1 V |
| Gaussian coverage ±1σ / ±2σ / ±3σ | 68.27 / 95.45 / 99.73 % | Two-sided |
| Quantization noise | Δ/√12 ≈ 0.29 LSB RMS | Uniform error |
| Ideal ADC SNR | 6.02N + 1.76 dB | 12 bits → 74.0 dB |
| MTBF 1,000,000 h | ≈ 114 years | A fleet statistic, not a lifetime (§9) |

### [01-08 · Sequences, Series and Taylor Expansions](../courses/01-calculus-for-engineers/chapters/01-08-sequences-series-and-taylor.md)

| Quantity | Value | Note |
|---|---|---|
| $\sum_{k\ge0}r^k$ | $1/(1 - r)$ for $\lvert r\rvert < 1$ | DC gain of $y[n] = ry[n-1] + x[n]$ |
| Harmonic series, $10^6$ terms | ≈ 14.4 | Diverges, but like $\ln n$ |
| $\sum 1/k^2$ | $\pi^2/6 \approx 1.645$ | Converges ($p = 2$) |
| Terms of $e^x$ for 10⁻⁶ at $x = 1$ | 10 | $e/10! \approx 7.5\times10^{-7}$ |
| Small-angle error at 0.1 rad | 0.17% | $x^2/6$ |
| Feedback gain error | ≈ $1/(A\beta)$ | Loop gain 1000 → 0.1% |
| Exponential-device HD2 | $A/(4V_T)$: 1 mV → 0.97% (−40 dB) | +20 dB per decade of A |
| Exponential-device HD3 | $A^2/(24V_T^2)$: 1 mV → −84 dB | +40 dB per decade of A |
| Leibniz series for π | about 2 million terms per 10⁻⁶ | Machin's formula: 5 terms of each part |

### [01-09 · Multivariable Calculus I: Partial Derivatives and Gradients](../courses/01-calculus-for-engineers/chapters/01-09-multivariable-calculus-1.md)

| Quantity | Value | Note |
|---|---|---|
| Power sensitivity to V and f | elasticities 2 and 1 (3 together under DVFS) | $\partial P/\partial V = 2P/V$ |
| Square-law $g_m$ | $2I_D/(V_{GS} - V_{TH})$ | 99 µA at 0.3 V overdrive → 0.66 mS |
| Output resistance | $r_o \approx V_A/I_D$ (exactly $(V_A + V_{DS})/I_D$ in this model) | Intrinsic gain $g_mr_o \approx 2V_A/V_{ov}$ (exactly $2(V_A + V_{DS})/V_{ov}$) |
| Silicon junction tempco at constant current | ≈ −1.8 to −2 mV/K | $(V - E_g/q - 3kT/q)/T$ |
| PTAT slope of $V_T$ | $k/q$ = 0.0862 mV/K | Used to cancel the junction tempco |
| Silicon bandgap reference output | ≈ 1.2 V | $E_g/q + 3kT/q$ (Problem 01-09.14) |
| Gradient-descent stability | $\eta < 2/h_{max}$, with $h_{max}$ the largest Hessian eigenvalue (curvature) | Condition number sets speed |
| Lagrange multiplier | marginal value of the constraint | Units of objective per unit of constraint |

### [01-10 · Multivariable Calculus II: Multiple, Line and Surface Integrals](../courses/01-calculus-for-engineers/chapters/01-10-multivariable-calculus-2.md)

| Quantity | Value | Note |
|---|---|---|
| Polar / cylindrical / spherical elements | $r\,dr\,d\theta$ / $r\,dr\,d\theta\,dz$ / $r^2\sin\phi\,dr\,d\phi\,d\theta$ | Never forget the Jacobian |
| $\int_{-\infty}^\infty e^{-x^2}dx$ | $\sqrt{\pi}$ ≈ 1.772 | Normalizes the Gaussian |
| Gaussian beam power within $w$ | 86.5% | $1 - e^{-2}$ |
| $\mu_0$ | $1.257\times10^{-6}$ T·m/A | $\oint\vec{B}\cdot d\vec{l} = \mu_0I$ |
| $\varepsilon_0$ | $8.854\times10^{-12}$ F/m | Gauss: flux = $Q/\varepsilon_0$ |
| Field 1 cm from a 1 A wire | 20 µT | $\mu_0I/(2\pi r)$ |
| 300 mm wafer area | 70 686 mm² | ≈ 640 dies of 100 mm² |
| Copper skin depth | ≈ 0.21 mm at 100 kHz, 0.066 mm at 1 MHz | $\sqrt{\rho/(\pi f\mu_0)}$ |

## [02 · Complex Numbers, Differential Equations and Linear Algebra](../courses/02-complex-numbers-des-and-linear-algebra/README.md)

### [02-01 · Complex Numbers, Euler's Formula and Phasors](../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-01-complex-numbers-euler-and-phasors.md)

| Quantity | Value | Note |
|---|---|---|
| Powers of $j$ | $j, -1, -j, 1$, repeating | $1/j = -j$ |
| 1 radian | 57.30° | |
| 3-4-5 triangle angle | $\arctan(4/3) = 53.13^\circ$ | Handy for checking work |
| $\lvert H\rvert$ of a single pole at its corner | $1/\sqrt{2} = 0.7071$ (−3.01 dB), phase −45° | Defines "bandwidth" |
| RMS of a sinusoid | $0.7071 \times$ peak | Peak = RMS × 1.414 |
| Grid frequency (as of Nov 2026) | 50 Hz or 60 Hz, giving $\omega$ = 314.16 or 376.99 rad/s | [R-006](research-log.md#r-006--power-grid-frequencies) |
| Mains peak voltage (as of Nov 2026) | 120 V rms (North America) → 169.7 V peak; 230 V rms (Europe) → 325.3 V peak | Nominal voltages, [R-014](research-log.md#r-014--nominal-mains-voltages) |
| Phase of a time delay | $360^\circ \times f \times t_d$; 1 ns = 360° at 1 GHz | Timing becomes phase at high frequency |
| 4096-QAM (Wi-Fi 7) transmit EVM limit | ≤ −38 dB, an RMS error of 1.26% of the signal | As of Nov 2026, [R-002](research-log.md#r-002--ieee-80211-evm-requirements) |
| 5G NR frequency range FR1 | 410–7125 MHz | As of Nov 2026, [R-003](research-log.md#r-003--3gpp-nr-frequency-ranges) |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| N 02-01.a | 1 rad in degrees | 57.30 | ° |
| N 02-01.b | $\omega$ at 50 Hz | 314.16 | rad/s |
| N 02-01.c | $\omega$ at 60 Hz | 376.99 | rad/s |
| N 02-01.d | peak of 120 V rms | 169.7 | V |
| N 02-01.e | peak of 230 V rms | 325.3 | V |
| N 02-01.f | −38 dB as an RMS ratio | 1.26 | % |
| N 02-01.g | corner magnitude in dB | −3.01 | dB |

### [02-02 · First-Order Linear ODEs](../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-02-first-order-linear-odes.md)

| Quantity | Value | Note |
|---|---|---|
| Fraction of a step complete after τ, 2τ, 3τ, 4τ, 5τ | 63.2%, 86.5%, 95.0%, 98.2%, 99.3% | $1 - e^{-n}$ |
| Time to 50% | $0.693\tau$ | $\tau\ln 2$ |
| 10–90% rise time | $2.197\tau$ | $\tau\ln 9$ |
| Ramp lag | $\tau$ in time, $m\tau$ in value | Constant forever |
| First-order filter at $\omega\tau = 1$ | −3.01 dB, −45° | Corner frequency $1/(2\pi\tau)$ |
| Logistic 10% → 90% | $4.394/r$ | $2\ln 9/r$, independent of $N_0$ |
| Thermal time constant | $R_{th}C_{th}$ | K/W × J/K = s |
| Feedback stretch of τ | $1/(1 - G)$ | $G$ = loop gain; runaway as $G \to 1$ |
| Forward-Euler stability on $y' = -y/\tau$ | $h < 2\tau$ | Backward Euler: any $h$ |
| JEDEC still-air θJA test enclosure | about 305 mm cube | JESD51-2A, as of Nov 2026 ([R-029](research-log.md#r-029--jedec-thermal-test-environments-jesd51-2a)) |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| N 02-02.a | step complete after 1τ | 63.2 | % |
| N 02-02.b | step complete after 2τ | 86.5 | % |
| N 02-02.c | step complete after 3τ | 95.0 | % |
| N 02-02.d | step complete after 4τ | 98.2 | % |
| N 02-02.e | step complete after 5τ | 99.3 | % |
| N 02-02.f | time to 50% in τ | 0.693 | — |
| N 02-02.g | 10–90% rise time in τ | 2.197 | — |
| N 02-02.h | gain at the corner | −3.01 | dB |
| N 02-02.i | logistic 10–90% time × r | 4.394 | — |
| N 02-02.j | one-τ-old input weight | 36.8 | % |

### [02-03 · Second-Order Linear ODEs and the Characteristic Equation](../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-03-second-order-linear-odes.md)

| Quantity | Value | Note |
|---|---|---|
| Overshoot at ζ = 0.3 / 0.5 / 0.707 | 37.2% / 16.3% / 4.3% | Depends only on ζ |
| ζ giving 2% overshoot | 0.78 | Fastest ±2% settling, $3.60/\omega_0$ |
| Critically damped 2% settling | $5.83/\omega_0$ | Not the fastest |
| Quality factor | $Q = 1/(2\zeta)$ | Series RLC: $Q = \omega_0L/R$ |
| Ring-down by a factor $e$ | $Q/\pi$ cycles | Energy loses $2\pi/Q$ per cycle |
| Series RLC critical resistance | $2\sqrt{L/C}$ | Twice the characteristic impedance |
| First droop after a load step | $\approx \Delta I\sqrt{L/C}$ | Light damping |
| PDN target impedance | $V_{DD}\times$ripple / $\Delta I$ | Smith et al. 1999 ([R-032](research-log.md#r-032--pdn-target-impedance-method)) |
| High-stability 5 MHz quartz crystal Q | about 2–3 million | Vig tutorial, as of Nov 2026 ([R-033](research-log.md#r-033--quartz-crystal-resonator-q)) |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| N 02-03.a | overshoot at ζ = 0.3 | 37.2 | % |
| N 02-03.b | overshoot at ζ = 0.5 | 16.3 | % |
| N 02-03.c | overshoot at ζ = 0.707 | 4.3 | % |
| N 02-03.d | ζ for 2 % overshoot | 0.78 | — |
| N 02-03.e | fastest 2 % settling, ω0·ts | 3.60 | — |
| N 02-03.f | critical 2 % settling, ω0·ts | 5.83 | — |

### [02-04 · Forced Response and Resonance](../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-04-forced-response-and-resonance.md)

| Quantity | Value | Note |
|---|---|---|
| Low-pass gain at $\omega_0$ | $Q$, phase −90° | Series RLC capacitor voltage |
| Peak of the low-pass | at $\omega_0\sqrt{1 - 2\zeta^2}$, height $1/(2\zeta\sqrt{1 - \zeta^2})$ | Only for ζ < 0.707 |
| Maximally flat (Butterworth) second order | ζ = 0.707, −3.01 dB at $\omega_0$ | |
| Band-pass half-power bandwidth | $\omega_0/Q$ exactly | $\omega_1\omega_2 = \omega_0^2$ |
| High-frequency roll-off of second order | −40 dB/decade | Phase → −180° |
| Resonant build-up time constant | $2Q/\omega_0$ | $Q/\pi$ cycles |
| NFC / ISO/IEC 14443 carrier and subcarrier | 13.56 MHz; 847.5 kHz ($f_c/16$) | Base rate 106 kbit/s, as of Nov 2026 ([R-034](research-log.md#r-034--nfc-and-isoiec-14443-carrier-and-data-rates)) |
| 32.768 kHz tuning-fork crystal Q | about 40,000–70,000 | Vendor note, as of Nov 2026 ([R-035](research-log.md#r-035--32768-khz-tuning-fork-crystals-q-and-start-up)) |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| N 02-04.a | Butterworth damping ratio | 0.707 | — |
| N 02-04.b | Butterworth gain at ω0 | −3.01 | dB |
| N 02-04.c | NFC subcarrier, 13.56 MHz / 16 | 847.5 | kHz |

### [02-05 · The Laplace Transform for ODEs](../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-05-laplace-transform-for-odes.md)

| Transform pair | | Note |
|---|---|---|
| $1 \leftrightarrow 1/s$; $\delta(t) \leftrightarrow 1$ | $u(t - a) \leftrightarrow e^{-as}/s$ | Step, impulse, delayed step |
| $e^{at} \leftrightarrow 1/(s - a)$ | $te^{at} \leftrightarrow 1/(s - a)^2$ | Real and repeated poles |
| $\cos\omega t \leftrightarrow s/(s^2 + \omega^2)$ | $\sin\omega t \leftrightarrow \omega/(s^2 + \omega^2)$ | Poles on the imaginary axis |
| $e^{-\alpha t}\cos\omega t \leftrightarrow (s + \alpha)/((s + \alpha)^2 + \omega^2)$ | $e^{-\alpha t}\sin\omega t \leftrightarrow \omega/((s + \alpha)^2 + \omega^2)$ | Complex poles |
| $f' \leftrightarrow sF - f(0^-)$ | $\int_0^tf \leftrightarrow F/s$ | Derivative, integral |
| $f(t - a)u(t - a) \leftrightarrow e^{-as}F(s)$ | $e^{at}f \leftrightarrow F(s - a)$ | Delay and shift |
| DC gain of a stable system | $H(0)$ | Final value of the unit-step response |

### [02-06 · Vectors, Matrices and Linear Systems](../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-06-vectors-matrices-and-linear-systems.md)

| Quantity | Typical value | Note |
|---|---|---|
| Dot product of two $n$-vectors | $n$ multiply–adds | |
| $m\times n$ matrix times a vector | $mn$ multiply–adds | Each matrix entry used once |
| $n\times n$ matrix product | $n^3$ multiply–adds = $2n^3$ flops | Doubling $n$ costs 8× |
| LU factorization of an $n\times n$ matrix | $\approx n^3/3$ multiply–adds = $\tfrac23n^3$ flops | HPL counts $\tfrac23n^3 + O(n^2)$ [R-038] |
| Solve with known $\mathbf{L}$, $\mathbf{U}$ | $\approx 2n^2$ flops | One factorization costs as much as about $n/3$ solves |
| Dense double-precision storage | $8n^2$ bytes: **800 MB** at $n = 10^4$ | Memory is often the first limit |
| Double-precision machine epsilon | $2^{-52} \approx$ **2.22×10⁻¹⁶** | About 16 significant digits |
| Nonzeros per row of a 2-D grid's $\mathbf{G}$ | about 5 | Circuit matrices are very sparse |
| H100 SXM ridge point, FP16 dense (as of Nov 2026) | about **295** flops/byte | 989.5 TFLOPS ÷ 3.35 TB/s [R-040] |
| Rubin GPU ridge point, FP16/BF16 dense (as of Nov 2026) | about **208** flops/byte | 4 PFLOPS ÷ 19.2 TB/s, projected [R-040] |
| Google TPU v1 matrix unit | 256×256 = 65,536 8-bit MACs at 700 MHz: **91.75** TOPS, quoted as 92 | [R-039] |
| TOP500 No. 1, Nov 2026 (LineShine) | Rmax **2.198** EFlop/s, **80.36%** of Rpeak | Dense LU, HPL [R-038] |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| N 02-06.a | dense storage at n = 10^4 | 800 | MB |
| N 02-06.b | machine epsilon 2^-52 | 2.22×10^-16 | — |
| N 02-06.c | H100 ridge point | 295 | flop/B |
| N 02-06.d | Rubin ridge point | 208 | flop/B |
| N 02-06.e | TPU v1 peak from MAC count and clock | 91.75 | TOPS |
| N 02-06.f | LineShine Rmax | 2.198 | EFlop/s |
| N 02-06.g | LineShine Rmax/Rpeak | 80.36 | % |

### [02-07 · Determinants, Inverses, Rank and Vector Spaces](../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-07-determinants-inverses-and-vector-spaces.md)

| Quantity | Typical value | Note |
|---|---|---|
| Determinant via LU | $\approx\tfrac23n^3$ flops | The product of the pivots, with the row-exchange sign |
| Determinant by full expansion | $n!$ terms: **2.433×10¹⁸** at $n = 20$ | Never used numerically |
| Inverse | $\approx 2n^3$ flops, **3** times an LU factorization | Solve with the factors instead |
| $\det(c\mathbf{A})$ for $n\times n$ | $c^n\det\mathbf{A}$ | |
| Rank–nullity | $r + (n - r) = n$ | |
| Connected circuit with $n$ nodes and $b$ branches | $n - 1$ independent node equations; $b - n + 1$ independent loops | Rank of the incidence matrix is $n - 1$ |
| Straight-line fit to $m$ points | 2 parameters, $m - 2$ degrees of freedom left for the noise | |
| 5G NR spatial layers (as of Nov 2026) | downlink up to **8**; uplink up to **4** (Release 15), **8** from Release 18 | [R-041] |
| Wi-Fi spatial streams (as of Nov 2026) | up to **8** in both 802.11ax (Wi-Fi 6) and 802.11be-2024 (Wi-Fi 7) | 16 was an early 802.11be target, not adopted [R-042] |
| LoRA on GPT-3 175B, as reported by its authors | **10,000**× fewer trainable parameters, **3**× less GPU memory than full fine-tuning | [R-043] |
| GPS position fix | at least **4** satellites: three coordinates plus the receiver clock offset | Least squares when more are visible [R-044] |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| N 02-07.a | 20! | 2.433×10^18 | — |
| N 02-07.b | inverse cost relative to LU | 3 | — |
| N 02-07.c | NR downlink layers | 8 | — |
| N 02-07.d | NR uplink layers, Release 15 | 4 | — |
| N 02-07.e | NR uplink layers, Release 18 | 8 | — |
| N 02-07.f | Wi-Fi 7 spatial streams | 8 | — |
| N 02-07.g | LoRA trainable-parameter reduction | 10000 | — |
| N 02-07.h | LoRA GPU-memory reduction | 3 | — |
| N 02-07.i | minimum GPS satellites | 4 | — |

### [02-08 · Eigenvalues and Eigenvectors](../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-08-eigenvalues-and-eigenvectors.md)

| Quantity | Typical value | Note |
|---|---|---|
| 2×2 characteristic equation | $\lambda^2 - (\operatorname{tr}\mathbf{A})\lambda + \det\mathbf{A} = 0$ | |
| Sum and product of eigenvalues | trace and determinant | The first two checks to run |
| Stability | discrete time: all $\lvert\lambda\rvert < 1$; continuous time: all $\operatorname{Re}\lambda < 0$ | Poles inside the unit circle, or in the left half-plane |
| Markov convergence | error $\propto\lvert\lambda_2\rvert^k$; at $\lvert\lambda_2\rvert = 0.9$, **43.71** steps to 1% | $\ln0.01/\ln\lvert\lambda_2\rvert$ |
| Complex pair $re^{\pm j\theta}$ | rotates θ per step, scales by $r$; $360°/\theta$ steps per cycle | |
| Coupled resonators | $f_2/f_1 = 1/\sqrt{1 + 2C_c/C}$ | In-phase mode stays at $f_0$ |
| SVD identities | $\prod\sigma_i = \lvert\det\mathbf{A}\rvert$ (square); $\sum\sigma_i^2 = \lVert\mathbf{A}\rVert_F^2$; $\kappa = \sigma_1/\sigma_n$ | |
| 5G NR Type II CSI, maximum rank (as of Nov 2026) | **2** in Release 15; **4** for Enhanced Type II in Release 16 | [R-045] |
| PageRank damping factor (1998 paper) | **0.85** | [R-047] |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| N 02-08.a | steps to 1% at λ2 = 0.9 | 43.71 | — |
| N 02-08.b | Type II CSI maximum rank, Release 15 | 2 | — |
| N 02-08.c | Enhanced Type II CSI maximum rank, Release 16 | 4 | — |
| N 02-08.d | PageRank damping factor | 0.85 | — |

### [02-09 · Systems of Linear ODEs and the Matrix Exponential](../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-09-systems-of-odes-and-matrix-exponential.md)

| Quantity | Typical value | Note |
|---|---|---|
| Solution of $\mathbf{x}' = \mathbf{A}\mathbf{x}$ | $\mathbf{x}(t) = e^{\mathbf{A}t}\mathbf{x}_0 = \sum c_ie^{\lambda_it}\mathbf{v}_i$ | One exponential per mode |
| Laplace pair | $\mathcal{L}\{e^{\mathbf{A}t}\} = (s\mathbf{I} - \mathbf{A})^{-1}$ | Poles are the eigenvalues |
| Transfer function | $H(s) = \mathbf{C}(s\mathbf{I} - \mathbf{A})^{-1}\mathbf{B} + D$ | DC gain $-\mathbf{C}\mathbf{A}^{-1}\mathbf{B} + D$ |
| 2-state stability | $\operatorname{tr}\mathbf{A} < 0$ and $\det\mathbf{A} > 0$ | |
| Determinant of the exponential | $\det e^{\mathbf{A}t} = e^{\operatorname{tr}(\mathbf{A})t}$ | Never zero |
| Exact sampling | $\mathbf{A}_d = e^{\mathbf{A}T}$, poles map as $z = e^{sT}$ | Left half-plane → inside the unit circle |
| Forward Euler stability, real mode λ | $T < 2/\lvert\lambda\rvert$ | The fastest mode sets the limit |
| Memory of a sampled first-order mode | $(\tau/h)\ln100 \approx$ **4.605** $\tau/h$ steps of length $h$ to decay to 1% | |
| Foster thermal impedance | $Z_{th}(t) = \sum R_i(1 - e^{-t/\tau_i})$, $\sum R_i = R_{th}$ | Datasheet format [R-049] |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| N 02-09.a | ln 100 | 4.605 | — |

### [02-10 · Numerical Methods for Engineers](../courses/02-complex-numbers-des-and-linear-algebra/chapters/02-10-numerical-methods.md)

| Quantity | Typical value | Note |
|---|---|---|
| Double-precision machine epsilon | **2.22×10⁻¹⁶** (about 16 digits) | Unit roundoff half of that |
| Single and half precision | 1.19×10⁻⁷ (about 7 digits); 9.77×10⁻⁴ (about 3 digits) | |
| Digits lost to conditioning | about $\log_{10}\kappa$ | |
| Newton near a simple root | correct digits roughly double per iteration | |
| Bisection | 1 bit per step; **3.32** steps per decimal digit | |
| Forward Euler stability, real λ | $h \le 2/\lvert\lambda\rvert$; RK4: $h \lesssim 2.785/\lvert\lambda\rvert$ | |
| ngspice defaults (as of Nov 2026) | reltol $10^{-3}$, vntol 1 µV, abstol 1 pA, GMIN $10^{-12}$ S, 100 DC iterations, trapezoidal integration | [R-053] |
| HPL-MxP versus HPL, Nov 2026 list (El Capitan) | **16.680** EFlop/s mixed precision against **1.809** EFlop/s FP64, a ratio of **9.2** | [R-055] |
| Patriot clock error after 100 h (GAO) | **0.3433** s, a range-gate shift of **687** m | [R-057] |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| N 02-10.a | double machine epsilon | 2.22×10^-16 | — |
| N 02-10.b | bisection steps per decimal digit | 3.32 | — |
| N 02-10.c | FP16 largest finite value | 65504 | — |
| N 02-10.d | FP8 E4M3 largest value | 448 | — |
| N 02-10.e | FP8 E5M2 largest value | 57344 | — |
| N 02-10.f | El Capitan HPL-MxP | 16.680 | EFlop/s |
| N 02-10.g | El Capitan HPL | 1.809 | EFlop/s |
| N 02-10.h | ratio | 9.2 | — |
| N 02-10.i | Patriot timing error after 100 h | 0.3433 | s |
| N 02-10.j | Patriot range-gate shift after 100 h | 687 | m |

## [03 · Probability, Statistics and Random Variables for EE](../courses/03-probability-statistics-and-random-variables/README.md)

### [03-01 · Probability in EE Language](../courses/03-probability-statistics-and-random-variables/chapters/03-01-probability-in-ee-language.md)

| Quantity | Value | Note |
|---|---|---|
| Rare-event rule | $1 - (1 - p)^n \approx np$ when $np \ll 1$ | Union bound; exact form $1 - e^{-np}$ |
| Birthday collisions | likely once $k \approx \sqrt{N}$ | $P \approx 1 - e^{-k^2/(2N)}$ |
| TMR break-even | $R = 0.5$ | TMR helps only above it |
| "Nines" | 99.9%: 8.766 h/yr; 99.99%: 52.60 min/yr; 99.999%: 5.260 min/yr | Downtime per year |
| Defect level | $\approx (1 - T)\ln(1/Y)$ | Williams–Brown, high coverage |
| Zero-error BER test, 95% confidence | about $3/p$ bits ($-\ln0.05/p$) | §9; [R-060](research-log.md#r-060--zero-error-ber-tests-and-confidence) |
| PCIe target BER, Gen 1–5 (NRZ), as of Nov 2026 | $10^{-12}$ | [R-059](research-log.md#r-059--serial-link-bit-error-rate-targets-pcie-and-ethernet) |
| PCIe 6.0 first-bit error rate, as of Nov 2026 | $10^{-6}$, with FEC, CRC and retry | [R-059](research-log.md#r-059--serial-link-bit-error-rate-targets-pcie-and-ethernet) |
| Ethernet 400G/800G/1.6T BER objective, as of Nov 2026 | $10^{-13}$ at the MAC | [R-059](research-log.md#r-059--serial-link-bit-error-rate-targets-pcie-and-ethernet) |
| Automotive and JEDEC qualification sample, as of Nov 2026 (JESD47G; AEC-Q100 per a 2020 NASA summary; current revisions not checked) | 3 lots × 77 units, zero failures | Shows < 1% defective at 90% confidence [R-061](research-log.md#r-061--qualification-sample-sizes-aec-q100-and-jedec-jesd47) |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| N 03-01.a | three-nines downtime | 8.766 | h/yr |
| N 03-01.b | four-nines downtime | 52.60 | min/yr |
| N 03-01.c | five-nines downtime | 5.260 | min/yr |
| N 03-01.d | bits per unit p for a 95% zero-error test | 2.996 | — |
| N 03-01.e | qualification sample, 3 × 77 | 231 | units |
| N 03-01.f | 95% zero-error test at 1e-12, 32 Gb/s | 93.62 | s |
| N 03-01.g | same at 400 Gb/s | 7.489 | s |
| N 03-01.h | 95% zero-error test at 1e-15, 400 Gb/s | 2.080 | h |

### [03-02 · Random Variables and Distributions](../courses/03-probability-statistics-and-random-variables/chapters/03-02-random-variables-and-distributions.md)

| Quantity | Value | Note |
|---|---|---|
| Within ±1σ, ±2σ, ±3σ of a Gaussian mean | 68.27%, 95.45%, 99.73% | $1 - 2Q(k)$ |
| $Q(3)$, $Q(4.5)$, $Q(6)$ | $1.350\times10^{-3}$, $3.398\times10^{-6}$, $9.866\times10^{-10}$ | $Q(4.5)$ is Six Sigma's "3.4 ppm" [R-065](research-log.md#r-065--six-sigma-34-ppm-and-the-15σ-shift) |
| $Q^{-1}$ at $10^{-9}$, $10^{-12}$, $10^{-15}$ | 5.998, 7.034, 7.941 | σ of margin needed |
| BER of ±A in Gaussian noise | $Q(A/\sigma)$; $10^{-12}$ needs 16.94 dB | Threshold midway |
| Total-jitter multiplier $2Q_{\text{BER}}$ | 14.069 at $10^{-12}$; 15.883 at $10^{-15}$ | Industry convention; literal model 13.68 [R-063](research-log.md#r-063--jitter-the-dual-dirac-model-and-the-q-scale) |
| 1 FIT | 1 failure per $10^9$ device-hours | [R-064](research-log.md#r-064--soft-error-rates-and-fit) |
| FPGA block-RAM soft-error rate, as of Nov 2026 | 692 FIT/Mb (65 nm planar) to 11.4 (7 nm FinFET); not monotone (90 nm: 484; 20 nm: 58); neutron-induced | AMD UG116 [R-064](research-log.md#r-064--soft-error-rates-and-fit) |
| Poisson: probability of none | $e^{-\lambda}$ | Poisson yield $e^{-AD_0}$ |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| N 03-02.a | within ±1σ | 68.27 | % |
| N 03-02.b | within ±2σ | 95.45 | % |
| N 03-02.c | within ±3σ | 99.73 | % |
| N 03-02.d | Q(3) | 1.350×10^-3 | — |
| N 03-02.e | Q(4.5) | 3.398×10^-6 | — |
| N 03-02.f | Q(6) | 9.866×10^-10 | — |
| N 03-02.g | inverse Q at 1e-9 | 5.998 | — |
| N 03-02.h | inverse Q at 1e-12 | 7.034 | — |
| N 03-02.i | inverse Q at 1e-15 | 7.941 | — |
| N 03-02.j | 2Q at 1e-12 | 14.069 | — |
| N 03-02.k | 2Q at 1e-15 | 15.883 | — |
| T 03-02.a | Q(1) | 0.1587 | — |
| T 03-02.b | Q(2) | 0.02275 | — |
| T 03-02.c | Q(7) | 1.280×10^-12 | — |
| T 03-02.d | multiplier at 1e-12 with transition density 1 | 14.26 | — |
| T 03-02.m | literal dual-Dirac multiplier at 1e-12, transition density 1/2 | 13.68 | — |
| T 03-02.n | extra eye margin of the convention, Example 03-02.7 | 0.47 | ps |
| T 03-02.o | eye cost of 1e-15 over 1e-12, share of UI | 7.0 | % |
| T 03-02.p | eye cost of 1e-15 over 1e-12, share of remaining eye | 34.18 | % |
| T 03-02.q | block-RAM SER ratio, 65 nm to 7 nm | 60.70 | — |
| T 03-02.r | sum of two 1 ps rms jitters | 1.414 | ps |
| T 03-02.e | upper bound over Q at x = 7, excess | 2 | % |
| T 03-02.f | Q(8) | 6.221×10^-16 | — |
| T 03-02.g | Q(7)/Q(8) | 2057 | — |
| T 03-02.h | A/σ after losing 1 dB from 7.034 | 6.269 | — |
| T 03-02.i | BER after losing 1 dB | 1.811×10^-10 | — |
| T 03-02.j | BER penalty factor for 1 dB | 181 | — |
| T 03-02.k | annual failure probability at 1000 FIT | 0.9 | % |
| T 03-02.l | one million hours | 114 | years |
| Ex 03-02.7g | extra jitter from 1e-12 to 1e-15 | 2.2 | ps |
| Ex 03-02.7h | required cut in random jitter | 18 | % |
| Ex 03-02.2g | expected upsets per device in 5 years | 0.04997 | — |
| Ex 03-02.5e | inverse Q at 1e-6 | 4.753 | — |
| Ex 03-02.7i | allowed total jitter | 21.875 | ps |

### [03-03 · Expectation, Variance and Functions of Random Variables](../courses/03-probability-statistics-and-random-variables/chapters/03-03-expectation-and-functions-of-rvs.md)

| Quantity | Value | Note |
|---|---|---|
| Power decomposition | $\mathbb{E}[V^2] = (\mathbb{E}[V])^2 + \operatorname{Var}(V)$ | total = DC + AC |
| Gaussian mean absolute value | $0.7979\sigma$ ($\sqrt{2/\pi}$) | Average meters read noise 1.049 dB low |
| Chebyshev at ±3σ | at most 11.11% outside | Gaussian: 0.2700% |
| Log-normal mean over median | $e^{\sigma_\ell^2/2}$ | Leakage, lifetimes |
| PAPR, real-waveform convention: sine, triangle | 3.010 dB, 4.771 dB | Crest factor $\sqrt2$, $\sqrt3$ |
| PAPR, envelope convention: constant envelope; complex Gaussian (OFDM limit) at $10^{-4}$ | 0 dB; 9.643 dB | $10\log_{10}\ln(1/p)$; instruments use this convention |
| Measured LTE crest factors (20 MHz; R&S measurement June 2016, checked Nov 2026) | 11.65 dB; uplink SC-FDMA 5.15–6.03 dB | Rohde & Schwarz [R-066](research-log.md#r-066--papr-ccdf-and-crest-factor-of-communication-signals) |
| ADC SNR with Gaussian input, granular only | $6.02N + 4.77 - 20\log_{10}k$ dB | Optimum $k$: 3.924 (8 bits), 5.013 (12 bits) |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| T 03-03.a | MTTF of a single part, r = 1e-5/h | 100000 | h |
| T 03-03.b | MTTF of a parallel pair | 150000 | h |
| T 03-03.c | Chebyshev bound at ±2σ | 25 | % |
| T 03-03.d | Gaussian outside ±2σ | 4.550 | % |
| T 03-03.e | Chebyshev bound at ±3σ | 11.11 | % |
| T 03-03.f | Gaussian outside ±3σ | 0.2700 | % |
| T 03-03.g | Chebyshev k for 1 ppm | 1000 | — |
| T 03-03.h | Gaussian k for 1 ppm two-sided | 4.892 | — |
| T 03-03.i | triangle-wave PAPR | 4.771 | dB |
| T 03-03.j | inverse Q at 5e-5 | 3.891 | — |
| T 03-03.k | real Gaussian PAPR at 1e-4 | 11.80 | dB |
| T 03-03.l | complex Gaussian PAPR at 1e-2 | 6.632 | dB |
| T 03-03.m | complex Gaussian PAPR at 1e-3 | 8.393 | dB |
| T 03-03.o | complex Gaussian PAPR at 1e-6 | 11.40 | dB |
| T 03-03.p | 20 log10 2 | 6.02 | dB |
| T 03-03.q | 10 log10 3 | 4.77 | dB |
| T 03-03.r | optimum loading, 8 bits | 3.924 | — |
| T 03-03.s | optimum SNR, 8 bits | 40.60 | dB |
| T 03-03.t | optimum loading, 12 bits | 5.013 | — |
| T 03-03.u | optimum SNR, 12 bits | 62.71 | dB |
| T 03-03.v | 12-bit SNR at k = 4 | 51.87 | dB |
| T 03-03.w | complex Gaussian exceedance at 11.65 dB | 4.5×10^-7 | — |
| T 03-03.x | real-waveform PAPR gap at 1e-4 | 8.790 | dB |
| T 03-03.y | bound on OFDM peak, 256 subcarriers | 24.08 | dB |
| T 03-03.z | bits wasted by k = 4 at 12 bits | 1.80 | — |

### [03-04 · Joint Distributions, Correlation and the CLT](../courses/03-probability-statistics-and-random-variables/chapters/03-04-joint-distributions-and-clt.md)

| Quantity | Value | Note |
|---|---|---|
| Variance of a sum | $\sigma_X^2 + \sigma_Y^2 + 2\rho\sigma_X\sigma_Y$ | RSS when uncorrelated |
| Total variance | within-group mean variance + variance of group means | Mixtures |
| Standard error of a mean of $n$ | $\sigma/\sqrt n$ | 4× samples for 2× precision |
| SNR gain from averaging $n$ | $10\log_{10}n$ dB | 64 averages: 18.06 dB |
| Differential noise | $\sigma\sqrt{2(1 - \rho)}$ | ρ = 0.9 gives 0.447σ |
| Conditional spread, jointly Gaussian | $\sigma_Y\sqrt{1 - \rho^2}$ | ρ = 0.8 leaves 60% |
| Complex Gaussian with $X_I$, $X_Q$ each $\mathcal{N}(0, \sigma^2)$ | envelope Rayleigh, phase uniform, power exponential with mean $2\sigma^2$ | OFDM, fading, narrowband noise |
| Ethernet KP4 FEC, as of Nov 2026 | RS(544,514), 10-bit symbols, $t = 15$; planned pre-FEC BER about $2.4\times10^{-4}$ for 400G optics | [R-067](research-log.md#r-067--rs544514-kp4-fec-and-pre-fec-ber) |

### [03-05 · Estimation and Hypothesis Testing for Engineers](../courses/03-probability-statistics-and-random-variables/chapters/03-05-estimation-and-hypothesis-testing.md)

| Quantity | Value | Note |
|---|---|---|
| 95% two-sided multipliers | z: 1.960; t: 2.776 (ν = 4), 2.262 (9), 2.045 (29), 1.984 (99) | Use t when σ is estimated |
| Zero failures in $n$ | 95% upper bound ≈ $3/n$ | Rule of three |
| Poisson upper bounds, $c = 0$ | 0.9163 (60%), 2.303 (90%), 2.996 (95%) | $-\ln\alpha$ |
| False alarms in 20 tests at 5% | 64.15% | Adjust α for many tests |
| Cp → ppm (centered) | 1.00: 2700; 1.33: 63; 1.67: 0.57; 2.00: 0.002 | [R-068](research-log.md#r-068--process-capability-and-outlier-screening) |
| AIAG default capability (1995 manuals; current editions not checked) | Cpk ≥ 1.33 stable ongoing; Ppk ≥ 1.67 preliminary or significant | Customer requirements override |
| Robust sigma | interquartile range / 1.349 | AEC-Q001 PAT uses 1.35 |
| Weibull shape | < 1 infant mortality; 1 random; > 1 wear-out | 63.2% failed at α |
| Arrhenius, 0.7 eV, 125 °C → 55 °C | AF = 77.65 (JEDEC's note: 78.6) | 1000 h ≈ 8.9 years |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| T 03-05.a | z multiplier for 95% | 1.960 | — |
| T 03-05.b | t multiplier, 4 df | 2.776 | — |
| T 03-05.c | t multiplier, 29 df | 2.045 | — |
| T 03-05.d | t multiplier, 99 df | 1.984 | — |
| T 03-05.e | 60% Poisson bound, c = 0 | 0.9163 | — |
| T 03-05.f | 60% Poisson bound, c = 1 | 2.022 | — |
| T 03-05.g | 60% Poisson bound, c = 2 | 3.105 | — |
| T 03-05.h | 90% Poisson bound, c = 0 | 2.303 | — |
| T 03-05.i | 90% Poisson bound, c = 1 | 3.890 | — |
| T 03-05.j | 90% Poisson bound, c = 2 | 5.322 | — |
| T 03-05.k | 95% Poisson bound, c = 0 | 2.996 | — |
| T 03-05.l | 95% Poisson bound, c = 1 | 4.744 | — |
| T 03-05.m | 95% Poisson bound, c = 2 | 6.296 | — |
| T 03-05.n | false-alarm probability, 20 tests | 0.6415 | — |
| T 03-05.o | out of spec at Cp = 1 | 2700 | ppm |
| T 03-05.p | out of spec at Cp = 4/3 | 63.34 | ppm |
| T 03-05.q | out of spec at Cp = 5/3 | 0.5733 | ppm |
| T 03-05.r | out of spec at Cp = 2 | 1.973 | ppb |
| T 03-05.s | Gaussian interquartile range in σ | 1.349 | — |
| T 03-05.t | standard error of Cpk 1.5 at n = 30 | 0.21 | — |
| T 03-05.u | fraction failed at the characteristic life | 63.2 | % |
| T 03-05.v | Arrhenius factor with rounded constants | 78.6 | — |
| T 03-05.w | equivalent years, rounded | 8.9 | years |
| T 03-05.x | exact 95% bound, zero failures in 1000 | 0.2991 | % |

### [03-06 · Random Processes Preview: Noise](../courses/03-probability-statistics-and-random-variables/chapters/03-06-random-processes-preview.md)

| Quantity | Value | Note |
|---|---|---|
| Thermal noise of 1 kΩ at 300 K | 4.07 nV/√Hz (scale as $\sqrt R$) | 50 Ω at 290 K: 0.895 nV/√Hz |
| $kT_0$ at 290 K | −174 dBm/Hz (4.00×10⁻²¹ W/Hz) | [R-070](research-log.md#r-070--thermal-noise-reference-kt0-and-290-k) |
| Receiver noise floor | −174 + 10 log₁₀ B + NF dBm | 1 MHz adds 60 dB |
| kT/C at 300 K | 64.4 µV for 1 pF; 20.35 µV for 10 pF | Independent of R |
| Shot noise | $\sqrt{2qI}$: 17.9 pA/√Hz at 1 mA | Exceeds 1 kΩ's thermal noise above 51.7 µA |
| RC noise bandwidth | $(\pi/2)f_{3\text{dB}}$ | 57% wider than −3 dB |
| Effective samples in a record | $T/(2\tau_c)$ | Faster sampling does not help |
| 1/f noise | equal power per decade, $e_w^2f_c\ln10$ | Datasheets quote 0.1–10 Hz |
| Op-amp noise, as of Nov 2026 | bipolar low-noise: 1.1 nV/√Hz at 1 kHz, 80 nVpp in 0.1–10 Hz; zero-drift: 5.2 nV/√Hz flat, 17 nV rms in 0.1–10 Hz | TI datasheets [R-071](research-log.md#r-071--op-amp-noise-specifications-1f-and-zero-drift) |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| T 03-06.a | kT0 | 4.004×10^-21 | W/Hz |
| T 03-06.b | 50 Ω noise density at 290 K | 0.895 | nV/√Hz |
| T 03-06.c | kT/C at 1 pF, 300 K | 64.4 | µV |
| T 03-06.d | RC noise bandwidth over −3 dB bandwidth | 1.571 | — |
| T 03-06.e | white-only 0.1–10 Hz noise at 5.2 nV/√Hz | 16.36 | nV |
| T 03-06.f | 1 MHz bandwidth in dB | 60 | dB |

## [04 · Physics for EE](../courses/04-physics-for-ee/README.md)

### [04-01 · Mechanics Essentials for EE](../courses/04-physics-for-ee/chapters/04-01-mechanics-essentials.md)

| Quantity | Value | Note |
|---|---|---|
| Standard gravity $g_n$ | 9.80665 m/s² | Defined value |
| 1 eV | $1.602\,176\,634\times10^{-19}$ J | Exact since 2019 |
| 1 kWh | 3.6 MJ | 1 Wh = 3600 J |
| 1 mechanical horsepower | ≈ 745.7 W | |
| Drop impact speed | $\sqrt{2gh}$: 5.42 m/s from 1.5 m | |
| Half-sine shock pulse | peak = (π/2) × average | |
| Oscillator | $\omega_0 = \sqrt{k_s/m}$; $Q = m\omega_0/b$ | Amplitude falls by $e$ in $Q/\pi$ cycles |
| Accelerometer sensitivity | $x/a = 1/\omega_0^2$: 15.53 nm per *g* at 4 kHz | |
| Thermomechanical noise | $a_n = \sqrt{4kT\omega_0/(mQ)}$ | 34.99 µ*g*/√Hz for 5 µg, 4 kHz, Q = 0.707 |
| Extensional (thin-bar) sound speed in silicon ⟨110⟩ | ≈ 8.5 km/s | $\sqrt{E/\rho}$; bulk waves are faster |
| Consumer MEMS accelerometer noise, as of Nov 2026 | 160–180 µ*g*/√Hz | Bosch BMI270, BMI323 [R-074](research-log.md#r-074--mems-inertial-sensors-datasheet-figures) |
| 32.768 kHz quartz parabola, as of Nov 2026 | ≈ −0.035 ppm/°C², turnover ≈ 25 °C | Micro Crystal, NDK [R-075](research-log.md#r-075--32768-khz-timing-quartz-crystals-and-mems-oscillators) |

### [04-02 · Charge, Coulomb's Law and Electric Fields](../courses/04-physics-for-ee/chapters/04-02-charge-coulomb-and-electric-fields.md)

| Quantity | Value | Note |
|---|---|---|
| Elementary charge | $e = 1.602\,176\,634\times10^{-19}$ C | Exact |
| Charges per coulomb | 6.242×10¹⁸ | |
| Coulomb constant | $k_e = 1/(4\pi\varepsilon_0)$ ≈ 8.988×10⁹ N·m²/C² | ε₀ = 8.854×10⁻¹² F/m |
| Field of an infinite sheet; between ±σ plates | σ/(2ε₀); σ/ε₀ | Uniform |
| Dipole far field | $2k_ep/r^3$ on axis, $k_ep/r^3$ broadside | Falls as $1/r^3$ |
| Electron after 100 V | ≈ 5.9×10⁶ m/s (2% of c) | $v = \sqrt{2eV/m_e}$ |
| Breakdown field | air ≈ 3 MV/m; thermal SiO₂ > 10 MV/cm | [R-077](research-log.md#r-077--esd-models-targets-and-dielectric-breakdown) |
| HBM network | 100 pF, 1.5 kΩ: 1.333 A peak per 2 kV | JS-001 |
| ESD qualification targets, as of Nov 2026 | 1 kV HBM, 250 V CDM (Industry Council) | [R-077](research-log.md#r-077--esd-models-targets-and-dielectric-breakdown) |

### [04-03 · Gauss's Law](../courses/04-physics-for-ee/chapters/04-03-gauss-law.md)

| Quantity | Value | Note |
|---|---|---|
| Flux per nanocoulomb enclosed | $1\ \text{nC}/\varepsilon_0$ ≈ 112.9 V·m | Independent of surface shape |
| Solid angle of a sphere | 4π ≈ 12.57 sr | |
| Uniform solid sphere | $E = k_eQr/R^3$ inside, $k_eQ/r^2$ outside | Peak at the surface |
| Line or coax | $E = \lambda/(2\pi\varepsilon_0r)$ between conductors, 0 outside a coax | Peak at the inner conductor |
| Sheet; field just outside a conductor | σ/(2ε₀); σ/ε₀ | Factor of 2 from shielding by the metal |
| Relative permittivity | silicon 11.7, thermal SiO₂ 3.9 | [R-078](research-log.md#r-078--gauss-law-applications-silicon-permittivity-capacitive-sensing-and-coulombs-law-tests), [R-077](research-log.md#r-077--esd-models-targets-and-dielectric-breakdown) |
| Junction peak field | $qN_Dx_n/\varepsilon_s$: tens of kV/cm for 10¹⁶ cm⁻³ doping | Triangle profile |
| Capacitive touch, as of Nov 2026 | finger 0.1 pF on a 33 pF pad (benchmark); signals down to 10–15 fF; noise floors 100–500 aF | [R-078](research-log.md#r-078--gauss-law-applications-silicon-permittivity-capacitive-sensing-and-coulombs-law-tests) |

### [04-04 · Electric Potential, Capacitance and Dielectrics](../courses/04-physics-for-ee/chapters/04-04-potential-capacitance-and-dielectrics.md)

| Quantity | Value | Note |
|---|---|---|
| One electron-volt | 1.602×10⁻¹⁹ J | Energy of $e$ through 1 V |
| Parallel plates; coax; sphere | $\varepsilon A/d$; $2\pi\varepsilon\ell/\ln(b/a)$; $4\pi\varepsilon_0R$ | |
| $\varepsilon_0$ in practical units | 8.854 pF/m = 8.854 fF/mm | 1 cm² at 1 mm in air ≈ 0.885 pF |
| Isolated 1 mm sphere; Earth | 0.111 pF; 0.709 mF | |
| Energy density; pressure in air at 3 MV/m | $\tfrac12\varepsilon E^2$; about 40 Pa | |
| Best coax for breakdown | $b/a = e$ | |
| Relative permittivity | SiO₂ 3.9; Si 11.7; HfO₂, ZrO₂ 25; Al₂O₃ 9; SiOCH low-k 2.7–2.9; class 2 ceramics 1000–4000 | [R-079](research-log.md#r-079--dielectric-constants-capacitor-materials-and-dram-cells), [R-078](research-log.md#r-078--gauss-law-applications-silicon-permittivity-capacitive-sensing-and-coulombs-law-tests) |
| DRAM cell capacitance (TechInsights, about 2021–22; checked Nov 2026) | below 10 fF in recent generations (from about 25 fF earlier) | [R-079](research-log.md#r-079--dielectric-constants-capacitor-materials-and-dram-cells) **[Industry estimate]** |

### [04-05 · Current, Resistance and Conduction](../courses/04-physics-for-ee/chapters/04-05-current-resistance-and-conduction.md)

| Quantity | Value | Note |
|---|---|---|
| Copper bulk resistivity | 1.68 µΩ·cm | [R-080](research-log.md#r-080--conduction-interconnect-metals-electromigration-and-backside-power) |
| Copper conduction-electron density | 8.49×10²⁸ m⁻³ | One per atom |
| Copper mean free time; mean free path | about 25 fs; 39–41 nm | Free-electron Drude estimate; first-principles value |
| Drift speed, 1 A in 1 mm² of copper | about 74 µm/s | |
| Copper temperature coefficient | 0.00393 /°C at 20 °C | +31% from 20 to 100 °C |
| Silicon mobilities (lightly doped) | µₙ ≈ 1400, µₚ ≈ 470 cm²/V·s | [R-080](research-log.md#r-080--conduction-interconnect-metals-electromigration-and-backside-power) |
| 1 oz PCB copper | 34 µm; 0.49 mΩ/□ | |
| Distributed-RC 50% delay | 0.38 RC; delay ∝ L² | |
| Electromigration limit, minimum Cu lines (ITRS 2015 projection) | 1.8 MA/cm² (2018) → 0.3 MA/cm² (2026) | **[Industry estimate]** |

### [04-06 · Magnetic Fields and Forces](../courses/04-physics-for-ee/chapters/04-06-magnetic-fields-and-forces.md)

| Quantity | Value | Note |
|---|---|---|
| µ₀ | 1.2566×10⁻⁶ N/A² ≈ 4π×10⁻⁷ | Measured since 2019 |
| Field 1 cm from 1 A | 20 µT | $\mu_0I/(2\pi r)$ |
| Earth's field | roughly 50 µT | Varies with location |
| Electron cyclotron frequency | 28.0 GHz per tesla | Independent of speed |
| Force between parallel wires | 2×10⁻⁷ N/m per A² at 1 m | Defined the ampere until 2019 |
| Solenoid; toroid | $\mu_0nI$; $\mu_0NI/(2\pi r)$ | |
| Hall voltage | $IB/(nqt)$ | Millivolts in semiconductors, sub-µV in metals |
| Saturation flux density, as of Nov 2026 | MnZn ferrite (N87) 0.49 T at 25 °C, 0.39 T at 100 °C; powder cores 1.05–1.5 T; Si steel 1.5–1.8 T | [R-081](research-log.md#r-081--hall-sensors-magnetic-core-materials-and-mram) |
| Hall switch average current, as of Nov 2026 | about 0.5 µA (5 Hz sampling) | [R-081](research-log.md#r-081--hall-sensors-magnetic-core-materials-and-mram) |

### [04-07 · Faraday's Law, Lenz's Law and Inductance](../courses/04-physics-for-ee/chapters/04-07-faraday-lenz-and-inductance.md)

| Quantity | Value | Note |
|---|---|---|
| Faraday's law | ℰ = −N dΦ/dt | 1 Wb/s = 1 V |
| Solenoid; gapped core | $\mu_0N^2A/\ell$; $N^2/\mathcal R$ | $L\propto N^2$ |
| Magnetic energy; density | $\tfrac12LI^2$; $B^2/(2\mu)$ ≈ 0.4 MJ/m³ at 1 T in air | |
| Copper skin depth | 8.4 mm (60 Hz), 0.21 mm (100 kHz), 65 µm (1 MHz), 2.1 µm (1 GHz) | $\delta\propto1/\sqrt f$ |
| Ideal transformer | $v_2/v_1 = N_2/N_1$; impedance × $(N_1/N_2)^2$ | |
| Qi wireless charging, as of Nov 2026 | 5 W (2010) → 15 W (2015) → 25 W (Qi2 25W, 2025); MPP at 360 kHz | [R-082](research-log.md#r-082--inductive-power-transfer-power-inductors-and-integrated-magnetics) |
| On-chip spiral inductor Q | roughly 5–20 at GHz | [R-082](research-log.md#r-082--inductive-power-transfer-power-inductors-and-integrated-magnetics) |

### [04-08 · Energy in Fields and Maxwell's Equations (Preview)](../courses/04-physics-for-ee/chapters/04-08-maxwell-preview.md)

| Quantity | Value | Note |
|---|---|---|
| Speed of light | $c = 299\,792\,458$ m/s = 1/√(µ₀ε₀) | ≈ 30 cm/ns, 0.3 mm/ps |
| Impedance of free space | η₀ ≈ 376.7 Ω | E/H in a plane wave |
| Wave in a dielectric | $v = c/\sqrt{\varepsilon_r}$, $\eta = \eta_0/\sqrt{\varepsilon_r}$ | |
| PCB stripline, ε_r = 4.6 | 7.15 ps/mm (about 180 ps/inch) | [R-083](research-log.md#r-083--board-dielectrics-propagation-5g-bands-and-rf-exposure) |
| Plane-wave intensity | $E_0^2/(2\eta_0)$ | 100 V/m → 13.3 W/m² |
| Dielectric attenuation | $\pi f\sqrt{\varepsilon_r}\tan\delta/c$ Np/m | ∝ f |
| Laminate loss tangents at 10 GHz, as of Nov 2026 | FR-4 class ≈ 0.025; low-loss ≈ 0.004 | [R-083](research-log.md#r-083--board-dielectrics-propagation-5g-bands-and-rf-exposure) |
| 5G NR ranges, as of Nov 2026 | FR1 410–7125 MHz; FR2-1 24.25–52.6 GHz; FR2-2 52.6–71 GHz | 3GPP TS 38.104 v19.6.0 |
| RF exposure, general public | FCC 1.6 W/kg (1 g); ICNIRP 2 W/kg (10 g), 20 W/m² above 6 GHz | [R-083](research-log.md#r-083--board-dielectrics-propagation-5g-bands-and-rf-exposure) |

### [04-09 · Waves and Optics Basics](../courses/04-physics-for-ee/chapters/04-09-waves-and-optics.md)

| Quantity | Value | Note |
|---|---|---|
| Wave speed | $v = \lambda f$; string $\sqrt{F_T/\mu}$; sound in air ≈ 343 m/s; light $c/n$ | |
| Two-slit fringe spacing | λL/d | |
| Diffraction | slit $\lambda/a$; circular aperture $1.22\lambda/D$ | Rayleigh criterion |
| Lithography resolution | $CD = k_1\lambda/\text{NA}$, $k_1 \ge 0.25$ | [R-084](research-log.md#r-084--optical-interconnect-standards-fiber-euv-and-co-packaged-optics) |
| EUV, as of Nov 2026 | 13.5 nm; NA 0.33 → 13 nm CD; NA 0.55 → 8 nm | ASML [R-084](research-log.md#r-084--optical-interconnect-standards-fiber-euv-and-co-packaged-optics) |
| Normal-incidence reflectance | glass 4%; silicon ≈ 31% | $((n_1 - n_2)/(n_1 + n_2))^2$ |
| Fiber NA | $\sqrt{n_1^2 - n_2^2}$, about 0.1 for single-mode | |
| Fiber loss limits (G.652.D cable) | ≤ 0.40 dB/km (1310–1625 nm); ≤ 0.30 dB/km (C-band) | [R-084](research-log.md#r-084--optical-interconnect-standards-fiber-euv-and-co-packaged-optics) |
| Dispersion, standard fiber | ≈ 17 ps/(nm·km) at 1550 nm; near 0 at 1310 nm | |
| 400G Ethernet optics | SR8: 850 nm, 100 m MMF; DR4: 1310 nm, 500 m; FR4: 4 λ, 2 km | IEEE 802.3 |

### [04-10 · Introduction to Quantum Mechanics](../courses/04-physics-for-ee/chapters/04-10-intro-quantum-mechanics.md)

| Quantity | Value | Note |
|---|---|---|
| Planck's constant | $h = 6.626\times10^{-34}$ J·s (exact); $\hbar = 1.055\times10^{-34}$ | |
| Photon energy | 1239.84 eV·nm / λ (≈ 1.24/λ in µm) | 1550 nm ≈ 0.80 eV; 850 nm ≈ 1.46 eV |
| Thermal energy at 300 K | $kT$ ≈ 25.9 meV | |
| Silicon absorption edge | ≈ 1.1 µm ($E_g$ ≈ 1.12 eV) | [R-085](research-log.md#r-085--quantum-effects-in-devices-and-quantum-computing) |
| Electron wavelength | 1.226 nm / √V | 0.12 nm at 100 V |
| Box energies | $E_n = n^2h^2/(8mL^2)$; 0.376 eV for 1 nm | ∝ 1/L², ∝ 1/m |
| Hydrogen ground state | −13.6 eV; Bohr radius 0.0529 nm | |
| Tunneling | $T\sim e^{-2\kappa d}$; ≈ 4× per 0.1 nm for a 2 eV barrier | |
| Thinnest SiO₂ gate in production, as of Nov 2026 | ≈ 1.2 nm (Intel 65 nm), then high-k | [R-085](research-log.md#r-085--quantum-effects-in-devices-and-quantum-computing) |

### [04-11 · Introduction to Solid-State Physics](../courses/04-physics-for-ee/chapters/04-11-intro-solid-state-physics.md)

| Quantity | Value | Note |
|---|---|---|
| Thermal energy at 300 K | $kT$ = 25.85 meV | |
| Silicon lattice | 0.5431 nm; 5.0×10²² atoms/cm³ | [R-086](research-log.md#r-086--crystals-band-gaps-intrinsic-carriers-and-wide-bandgap-markets) |
| Copper free-electron gas | $E_F$ ≈ 7.0 eV, $v_F$ ≈ 1.57×10⁶ m/s, $T_F$ ≈ 82,000 K | |
| Fermi–Dirac edge | 4.4 kT from 90% to 10% (0.11 eV at 300 K) | |
| Band gaps at 300 K | Ge 0.66–0.67, Si 1.12, GaAs 1.42, 4H-SiC ≈ 3.2–3.26, GaN 3.4, diamond 5.5, SiO₂ ≈ 9 eV | [R-086](research-log.md#r-086--crystals-band-gaps-intrinsic-carriers-and-wide-bandgap-markets) |
| Silicon $n_i$ at 300 K | 9.65×10⁹ cm⁻³ (≈10¹⁰; the old 1.45×10¹⁰ is superseded); ≈ 560× higher at 400 K | [R-086](research-log.md#r-086--crystals-band-gaps-intrinsic-carriers-and-wide-bandgap-markets) |

## [05 · Programming for Engineers](../courses/05-programming-for-engineers/README.md)

### [05-01 · Python Fundamentals for Engineers](../courses/05-programming-for-engineers/chapters/05-01-python-fundamentals.md)

| Quantity | Value | Note |
|---|---|---|
| Current Python feature release, as of Nov 2026 | 3.15 (released 9 Oct 2026) | New release every October, supported 5 years ([R-087](research-log.md#r-087--python-releases-floating-point-and-developer-usage)) |
| float64 precision | 53 significant bits ≈ 15–17 decimal digits | IEEE 754-2019 binary64 |
| Machine epsilon | $2^{-52} \approx 2.22\times10^{-16}$ | Gap from 1.0 to the next float |
| Largest float | ≈ 1.8×10³⁰⁸ | Beyond it, float arithmetic gives `inf`; `2.0 ** 1024` and `math.exp(1000)` raise `OverflowError` |
| Integers that floats store exactly | up to $2^{53} \approx 9.0\times10^{15}$ | Above that, gaps exceed 1 |
| Python's `int` | unlimited size | Contrast: C's `int32_t` overflows (undefined behavior) above about 2.1×10⁹ (05-05) |
| Developers using Python (self-selected survey, 2026) | 58% of those answering the language question | Stack Overflow ([R-087](research-log.md#r-087--python-releases-floating-point-and-developer-usage)) |

### [05-02 · NumPy, Vectorization and Numerical Computing](../courses/05-programming-for-engineers/chapters/05-02-numpy-and-vectorization.md)

| Quantity | Value | Note |
|---|---|---|
| float64 | 53-bit significand, ε = 2.2×10⁻¹⁶, max ≈ 1.8×10³⁰⁸ | Default float |
| float32 | 24-bit significand, ε = 1.2×10⁻⁷, max ≈ 3.4×10³⁸, integers exact to 2²⁴ ≈ 1.7×10⁷ | Graphics, AI |
| float16 (IEEE binary16) | 11-bit significand, ε ≈ 9.8×10⁻⁴, max 65504 | [R-056](research-log.md#r-056--low-precision-floating-point-formats) |
| bfloat16 | 8 exponent bits, 7 fraction bits: float32's range, about 3 digits | AI training [R-056](research-log.md#r-056--low-precision-floating-point-formats) |
| int32 / int64 ranges | ±2.1×10⁹ / ±9.2×10¹⁸ | Wrap around beyond |
| RMS of a sine | amplitude/√2 ≈ 0.7071 × amplitude | Example 05-02.1 |
| NumPy releases, as of Nov 2026 | 2.0 (June 2024, NEP 50 promotion rules); 2.5 current (June 2026) | [R-087](research-log.md#r-087--python-releases-floating-point-and-developer-usage) |

### [05-03 · SciPy, SymPy and Matplotlib](../courses/05-programming-for-engineers/chapters/05-03-scipy-sympy-matplotlib.md)

| Quantity | Value | Note |
|---|---|---|
| One time constant of charging | 63.21% of the final value | $1 - e^{-1}$ |
| −3 dB | power ratio ½, amplitude ratio $1/\sqrt2$ ≈ 0.7071 | First-order filter at its corner |
| First-order roll-off | −20 dB per decade | Figure 1 |
| Diode forward voltage (silicon, mA currents) | about 0.6–0.7 V | Example 05-03.1 |
| `solve_ivp` default relative tolerance | 10⁻³ | Tighten for verification |
| Maximum power transfer | $R_L = R_s$, $P = V^2/4R_s$, 50% efficiency | Example 05-03.5 |

### [05-04 · Jupyter, Testing and Reproducible Workflows](../courses/05-programming-for-engineers/chapters/05-04-reproducible-workflows.md)

| Quantity | Value | Note |
|---|---|---|
| `math.isclose` defaults | rel_tol $10^{-9}$, abs_tol 0 | fails for expected value 0 |
| `pytest.approx` defaults | rel $10^{-6}$, abs $10^{-12}$ | |
| `numpy.isclose` defaults | rtol $10^{-5}$, atol $10^{-8}$ | not symmetric in its arguments |
| binary64 machine epsilon (spacing just above 1) | $2^{-52} \approx 2.2\times10^{-16}$; unit roundoff $2^{-53}$ | 05-01 |
| Git hash (SHA-1) | 160 bits, 40 hex digits; 7-digit short form | SHA-256: 256 bits, 64 hex digits |
| Two-sided normal tail beyond 4σ | $6.3\times10^{-5}$ | about 1 in 16,000 |
| Notebooks from GitHub that re-ran without error | 24% (2019 study) | [R-088](research-log.md#r-088--jupyter-notebook-reproducibility) |
| Python developers using pytest / unittest | 53% / 23% (2024 survey) | [R-089](research-log.md#r-089--python-testing-tools-pytest-release-and-usage) |
| Developers using git | 94% (2022 survey) | [R-090](research-log.md#r-090--git-usage-and-hash-functions) |

### [05-05 · C Fundamentals](../courses/05-programming-for-engineers/chapters/05-05-c-fundamentals.md)

| Quantity | Value | Note |
|---|---|---|
| `int` on desktop and 32-bit MCUs | 32 bits: −2,147,483,648 to 2,147,483,647 | at least 16 bits by the standard |
| `long` | 64 bits on Linux/macOS; 32 bits on Windows and Cortex-M | the portability trap |
| 32-bit unsigned maximum | 4,294,967,295 ($2^{32} - 1$) | |
| 16-bit signed range | −32,768 to 32,767 | audio and many ADCs |
| `float` / `double` precision | about 7 / 16 significant digits | 05-02 |
| C standard revisions | C89/C90, C99, C11, C17, C23 (published Oct 2024) | [R-092](research-log.md#r-092--c-language-standards-coding-standards-and-embedded-usage) |
| C share among embedded/IoT developers (constrained devices) | 55% (C++ 36%), 2024 survey | [R-092](research-log.md#r-092--c-language-standards-coding-standards-and-embedded-usage) |
| AddressSanitizer slowdown | typically about 2× (Clang documentation); memory overhead varies | testing only |

### [05-06 · C Pointers, Arrays and Memory](../courses/05-programming-for-engineers/chapters/05-06-c-pointers-and-memory.md)

| Quantity | Value | Note |
|---|---|---|
| Pointer size | 8 bytes (64-bit), 4 bytes (32-bit MCU) | |
| Typical stack size | about 8 MB per desktop thread (Linux default); KB on MCUs | configurable |
| Struct padding rule | each field at a multiple of its alignment (its size, for basic types on common ABIs); total rounded up to the largest alignment | Example 05-06.4 |
| Geometric (doubling) growth | fewer than 2 copies per element on average | Example 05-06.5 |
| Memory-safety share of serious vulnerabilities | about 70% (Microsoft CVEs 2006–2018; Chromium high-severity bugs) | [R-094](research-log.md#r-094--memory-safety-vulnerability-data-and-policy) |
| Android memory-safety share | 76% (2019) → under 20% (2025) | [R-095](research-log.md#r-095--rust-adoption-in-android-and-the-linux-kernel) |
| ASan slowdown | typically about 2× (Clang documentation) | testing only |

### [05-07 · Bit Manipulation and Fixed-Width Integers](../courses/05-programming-for-engineers/chapters/05-07-bit-manipulation.md)

| Quantity | Value | Note |
|---|---|---|
| $n$-bit two's-complement range | $-2^{n-1}$ to $2^{n-1} - 1$ | 8 bit: −128 to 127; 16 bit: −32,768 to 32,767 |
| Q15 range and step | $[-1, 1 - 2^{-15}]$, $\Delta = 3.05\times10^{-5}$ | 16-bit fractional |
| Rounding error | uniform in $\pm\Delta/2$, RMS $\Delta/\sqrt{12} = 0.289\Delta$ | |
| SNR per bit | about 6.02 dB | ideal quantizer, full-scale sine: $6.02N + 1.76$ dB |
| Hex digit | 4 bits; a byte is 2 hex digits | |
| Network byte order | big-endian | x86 and common MCUs are little-endian ([R-096](research-log.md#r-096--processor-byte-order-arm-cortex-m-and-risc-v)) |
| Patriot clock error | $2^{-20}$ relative; 0.3433 s after 100 h | [R-057](research-log.md#r-057--patriot-missile-timing-error) |

### [05-08 · Data Structures and Algorithms You Will Need](../courses/05-programming-for-engineers/chapters/05-08-data-structures-and-algorithms.md)

| Quantity | Value | Note |
|---|---|---|
| $\log_2 10^3$, $10^6$, $10^9$ | about 10, 20, 30 | halvings to search |
| Binary search on $n$ sorted items | $\lfloor\log_2 n\rfloor + 1$ comparisons | |
| Comparison-sort lower bound | $\log_2 n! \approx n\log_2 n - 1.44n$ | merge sort is within lower-order terms |
| Random permutation | $n(n-1)/4$ inversions on average | insertion sort's work |
| Linear probing at α = 0.5 / 0.75 / 0.9 | successful 1.5 / 2.5 / 5.5; unsuccessful 2.5 / 8.5 / 50.5 probes | resize before it fills |
| Heap index arithmetic | children $2i+1$, $2i+2$; parent $\lfloor(i-1)/2\rfloor$ | 0-based |
| UART at 115,200 baud (8N1) | about 11,520 bytes/s | sizing receive buffers |

### [05-09 · Software Engineering Practices](../courses/05-programming-for-engineers/chapters/05-09-software-engineering-practices.md)

| Quantity | Value | Note |
|---|---|---|
| Cyclomatic complexity | decisions + 1; flag above ~10–15 | basis-path test count |
| MC/DC minimum tests | $N + 1$ for $N$ conditions (versus $2^N$ exhaustive) | required for DO-178C Level A ([R-097](research-log.md#r-097--safety-standard-coverage-requirements-and-the-defect-cost-curve)) |
| Escape fraction of a filter chain | $\prod (1 - p_i)$ (independent filters; optimistic) | Example 05-09.4 |
| Sprint length (Scrum) | 1–4 weeks | |
| Semantic version | MAJOR.MINOR.PATCH | breaking / compatible feature / fix |
| FE Software Engineering | 4–6 of 110 questions | [R-001](research-log.md#r-001--ncees-fe-electrical-and-computer-specification) |

## [06 · Circuit Analysis I (DC)](../courses/06-circuit-analysis-1-dc/README.md)

### [06-01 · Charge, Current, Voltage, Power and the Lumped Circuit Abstraction](../courses/06-circuit-analysis-1-dc/chapters/06-01-charge-current-voltage-power.md)

| Quantity | Value | Note |
|---|---|---|
| Elementary charge $e$ | $1.602\,176\,634\times10^{-19}$ C (exact since 2019) | [R-073](research-log.md#r-073--codata-2022-fundamental-constants) |
| Charges per second in 1 A | $6.24\times10^{18}$ | $1/e$ |
| 1 mAh | 3.6 C (charge, not energy) | × voltage for energy |
| 1 Wh | 3600 J | 1 kWh = 3.6 MJ |
| Signal delay in FR-4 stripline ($\varepsilon_r$ = 4.6) | 7.15 ps/mm (≈ 14 cm/ns) | [R-083](research-log.md#r-083--board-dielectrics-propagation-5g-bands-and-rf-exposure) |
| Lumped rule for digital edges | $t_d < t_r/6$ | rule of thumb (00-02) |
| Lumped rule for sinusoids | size $< \lambda/10$ | 60 Hz: $\lambda$ ≈ 5000 km |
| Distribution loss scaling | $P_{\text{loss}}/P = PR/V^2$ | double $V$, quarter the loss |
| AI accelerator power | about 1 kW per device | [R-026](research-log.md#r-026--ai-accelerator-power-ratings) |
| AI rack power (72-GPU class) | about 120 to 142 kW (definitions differ) | [R-098](research-log.md#r-098--usb-power-delivery-rack-power-distribution-and-ai-rack-power) |
| Rack DC bus today; announced next step | 48 V class (≈ 50–54 V); 800 V DC from 2027 | [R-098](research-log.md#r-098--usb-power-delivery-rack-power-distribution-and-ai-rack-power) |
| USB-C power ceiling | 240 W = 48 V × 5 A (100 W = 20 V × 5 A before 2021) | [R-098](research-log.md#r-098--usb-power-delivery-rack-power-distribution-and-ai-rack-power) |
| Data centers' share of world electricity | ≈ 1.5% (2024), ≈ 3% projected for 2030 | [R-099](research-log.md#r-099--data-centre-electricity-use-iea) |
| Low-power MCU | active ≈ 4–75 µA/MHz; sleep ≈ 0.1–3 µA | [R-100](research-log.md#r-100--low-power-mcu-currents-coin-cells-and-cpu-core-voltage-ranges) |
| CR2032 coin cell | 3 V, ≈ 225–254 mAh (load-dependent) | [R-100](research-log.md#r-100--low-power-mcu-currents-coin-cells-and-cpu-core-voltage-ranges) |

### [06-02 · Circuit Elements and Ohm's Law](../courses/06-circuit-analysis-1-dc/chapters/06-02-circuit-elements-and-ohms-law.md)

| Quantity | Value | Note |
|---|---|---|
| Copper resistivity (IACS, 20 °C) | 1.7241 µΩ·cm; 17.2 mΩ per meter for 1 mm² | [R-101](research-log.md#r-101--resistors-preferred-values-film-technologies-copper-and-shunts) |
| Copper temperature coefficient | 0.00393 /°C (+0.39%/°C) | [R-080](research-log.md#r-080--conduction-interconnect-metals-electromigration-and-backside-power) |
| 1 oz PCB copper | ≈ 35 µm; ≈ 0.5 mΩ/□ | ±7–15% with plating and etch |
| E-series steps | E12 ≈ 21%, E24 ≈ 10%, E96 ≈ 2.4% per value | IEC 60063 ([R-101](research-log.md#r-101--resistors-preferred-values-film-technologies-copper-and-shunts)) |
| Thick-film chip resistor | ±1–5%, ±100–200 ppm/K | general purpose |
| Thin-film chip resistor | ±0.1–1%, ±10–50 ppm/K | precision |
| Smallest mainstream chip resistor | 01005 (0.4 × 0.2 mm), about 1/32 W | [R-101](research-log.md#r-101--resistors-preferred-values-film-technologies-copper-and-shunts) |
| "Volts per kilohm" | 1 V / 1 kΩ = 1 mA | mental arithmetic |

### [06-03 · Kirchhoff's Laws, Series/Parallel and Dividers](../courses/06-circuit-analysis-1-dc/chapters/06-03-kirchhoffs-laws.md)

| Quantity | Value | Note |
|---|---|---|
| Independent equations | $n - 1$ KCL, $b - n + 1$ KVL | $b$ total |
| Parallel rules of thumb | $R\parallel R = R/2$; result < smallest resistor | $R_1\parallel R_2 = R_1R_2/(R_1 + R_2)$ |
| Loading error | ≈ $R_{source}/R_L$: 10× load ≈ 9%, 100× ≈ 1% | $R_{source} = R_1\parallel R_2$ for a divider |
| Quarter-bridge output | ≈ $(V/4)(\Delta R/R)$; nonlinearity ≈ $\Delta R/(2R)$ | half: $V\Delta R/(2R)$; full: $V\Delta R/R$ |
| Foil strain-gauge factor | ≈ 2 | [R-102](research-log.md#r-102--strain-gauges-gauge-factor-and-bridge-excitation) |
| Common gauge resistances | 120 Ω and 350 Ω | |
| Equal delta to wye | $R_Y = R_\Delta/3$ | three-phase loads too |

### [06-04 · Nodal Analysis](../courses/06-circuit-analysis-1-dc/chapters/06-04-nodal-analysis.md)

| Quantity | Value | Note |
|---|---|---|
| Unknowns, nodal versus branch method | $n - 1$ versus $2b$ | 50 nodes, 120 branches: 49 versus 240 |
| Nodal matrix entries | diagonal: sum at node; off-diagonal: −(conductance between) | symmetric for R and independent sources |
| MNA size | nodes − 1 + number of voltage sources | |
| Nonzeros in an N × N grid's matrix | about $5N^2$ | out of $N^4$ |
| Dense solve cost | about $n^3/3$ operations | sparse: far less for circuits |
| SPICE origin | SPICE (1973), SPICE2 with MNA (1975), UC Berkeley | [R-054](research-log.md#r-054--spice-and-spice2-origins) |

### [06-05 · Mesh Analysis](../courses/06-circuit-analysis-1-dc/chapters/06-05-mesh-analysis.md)

| Quantity | Value | Note |
|---|---|---|
| Unknowns, mesh method | $b - n + 1$ (minus one per current source) | 50 nodes, 120 branches: 71 |
| Unknowns, nodal method | $n - 1$ (minus one per voltage source) | same circuit: 49 |
| Mesh matrix entries | diagonal: total resistance around the mesh; off-diagonal: −(shared resistance) | symmetric, all meshes clockwise |
| Coupling through a shared return | $v = R_g\,i_{\text{other}}$ | 10 mΩ × 2 A = 20 mV |
| One LSB, 12-bit ADC over 5 V | 1.221 mV | 16 LSB error from a 20 mV offset |

### [06-06 · Dependent Sources](../courses/06-circuit-analysis-1-dc/chapters/06-06-dependent-sources.md)

| Quantity | Value | Note |
|---|---|---|
| VCVS, VCCS, CCVS, CCCS gain units | V/V, S, Ω, A/A | SPICE letters E, G, H, F |
| Bipolar $g_m$ | $I_C/V_T$ = 38.7 mS per mA at 300 K | $V_T$ = 25.85 mV |
| Bipolar $r_\pi$ | $\beta/g_m$ | 2.585 kΩ at 1 mA with $\beta$ = 100 |
| Resistance reflected into a base | $(\beta + 1)R_E$ | 100 Ω → 10.1 kΩ at $\beta$ = 100 |
| Degenerated gain | $\approx -R_D/(R_S + 1/g_m)$ | equals $-g_mR_D/(1 + g_mR_S)$ |
| Miller resistance | $R_f/(1 - \mu)$ | $R_f/(1 + A)$ for inverting gain $-A$ |
| Closed-loop gain error | $\approx 1/(A\beta)$ | $10^{-4}$ for $A = 10^5$, gain 10 |

### [06-07 · Linearity and Superposition](../courses/06-circuit-analysis-1-dc/chapters/06-07-linearity-and-superposition.md)

| Quantity | Value | Note |
|---|---|---|
| Switched-off sources | V → short, I → open | dependent sources stay |
| Cross term in power | $2R\,i'i''$ | zero on average for different frequencies or independent noise |
| Millman's theorem | $V_{eq} = \sum(V_k/R_k)/\sum(1/R_k)$ | parallel practical sources |
| Equal-resistor ladder | Fibonacci ratios | input resistance → 1.618 R |
| Error combination | worst case $\sum\lvert e_k\rvert$; RSS $\sqrt{\sum e_k^2}$ | RSS for independent random errors |

### [06-08 · Thévenin and Norton Equivalents](../courses/06-circuit-analysis-1-dc/chapters/06-08-thevenin-and-norton.md)

| Quantity | Value | Note |
|---|---|---|
| Thévenin–Norton relation | $V_{th} = R_{th}I_N$, $R_{th} = v_{oc}/i_{sc}$ | |
| Loading error | $\approx R_{th}/R_L$ for $R_L \gg R_{th}$ | 1 kΩ into 1 MΩ: 0.1% |
| PoE Type 4 (Class 8) | 52 V min at the PSE, 90 W at the PSE, 71.3 W at the PD, 6.25 Ω worst-case loop | [R-105](research-log.md#r-105--thevenin-and-norton-history-and-power-over-ethernet), as of Nov 2026 |
| PoE Type 2 (Class 4) | 50 V min, 30 W at the PSE, 25.5 W at the PD, 12.5 Ω worst-case loop | [R-105](research-log.md#r-105--thevenin-and-norton-history-and-power-over-ethernet) |
| Maximum PoE voltage | 57 V | all types |
| Typical DMM input resistance | 10 MΩ (many offer > 10 GΩ on low ranges) | see 06-11 |

### [06-09 · Maximum Power Transfer](../courses/06-circuit-analysis-1-dc/chapters/06-09-maximum-power-transfer.md)

| Quantity | Value | Note |
|---|---|---|
| Matched load | $R_L = R_{th}$, $v = V_{th}/2$ | $p_{max} = V_{th}^2/4R_{th}$ |
| Efficiency at the match | 50% | $\eta = R_L/(R_{th} + R_L)$ |
| Power–efficiency tradeoff | $p/p_{max} = 4\eta(1 - \eta)$ | 95% efficient → 19% of max |
| Flatness | a factor 2 off loses 11% | |
| Coax optima (air) | 76.7 Ω (min loss), 30.0 Ω (max power) | $Z_0 = (60/\sqrt{\varepsilon_r})\ln(b/a)$ |
| Standard impedances | 50 Ω (RF, test equipment), 75 Ω (video, cable TV) | [R-106](research-log.md#r-106--the-50-ohm-standard) |

### [06-10 · The Ideal Op-Amp](../courses/06-circuit-analysis-1-dc/chapters/06-10-ideal-op-amp.md)

| Quantity | Value | Note |
|---|---|---|
| Ideal rules (with negative feedback) | $i_\pm = 0$, $v_+ = v_-$ | fail when the output saturates |
| Inverting / non-inverting gain | $-R_2/R_1$ / $1 + R_2/R_1$ | noise gain $1 + R_2/R_1$ in both |
| Difference-amplifier CMRR, tolerance $t$ | $\approx (1 + G)/(4t)$ | 1%, G = 100: 68 dB |
| OPA187 (zero-drift) | $V_{OS}$ 1 µV typ, 10 µV max; $I_B$ ±350 pA max; $A_{OL}$ 160 dB typ; GBW 550 kHz | 25 °C, datasheet SBOS807E ([R-107](research-log.md#r-107--op-amp-datasheets-and-analog-revenue)) |
| LM358 (general purpose) | $V_{OS}$ 3 mV typ, 7 mV max; $I_B$ −20 nA typ, −250 nA max; GBW 0.7 MHz | 25 °C, datasheet SLOS068AB ([R-107](research-log.md#r-107--op-amp-datasheets-and-analog-revenue)) |

### [06-11 · Practical DC Circuits and Measurement](../courses/06-circuit-analysis-1-dc/chapters/06-11-practical-dc-circuits-and-measurement.md)

| Quantity | Value | Note |
|---|---|---|
| Loading error of a voltmeter | $\approx -R_{th}/R_{in}$ | ammeter: $\approx -R_A/R_{th}$ |
| Handheld DMM input resistance | ≈ 10 MΩ ∥ < 100 pF | original Fluke 87 manual ([R-108](research-log.md#r-108--digital-multimeter-specifications)) |
| Bench DMM high-impedance mode | > 10 GΩ on the 100 mV to 10 V ranges | Keysight 34465A, search excerpts ([R-108](research-log.md#r-108--digital-multimeter-specifications)) |
| Handheld DMM DC accuracy | ±(0.05% + 1 count) | Fluke 87V, as of Nov 2026 ([R-108](research-log.md#r-108--digital-multimeter-specifications)) |
| 6½-digit bench DMM, basic DC accuracy | about 30 ppm, 1 year | Keysight 34465A, search excerpts ([R-108](research-log.md#r-108--digital-multimeter-specifications)) |
| Copper | 1.7241 µΩ·cm, +0.393%/°C at 20 °C | IACS (06-02) |
| 1 oz PCB copper | 35 µm, ≈ 0.49 mΩ/□; 0.5 cm wide trace ≈ 1 mΩ/cm | TI SNVA054C ([R-109](research-log.md#r-109--pcb-copper-wire-gauge-and-four-terminal-shunts)) |
| 16 AWG copper wire | 1.291 mm, 13.17 mΩ/m at 20 °C | AWG formula (Example 06-11.6) |
| Four-terminal shunt (Vishay WSK2512) | 0.5 mΩ to 0.2 Ω; ±0.1% to ±1%; ±35 to ±350 ppm/°C by value; 1 W at 70 °C | datasheet, Dec 2023 ([R-109](research-log.md#r-109--pcb-copper-wire-gauge-and-four-terminal-shunts)) |

## [07 · Circuit Analysis II (Transient and AC)](../courses/07-circuit-analysis-2-transient-and-ac/README.md)

### [07-01 · Capacitors and Inductors](../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-01-capacitors-and-inductors.md)

| Quantity | Value | Note |
|---|---|---|
| Rates | 1 mA into 1 µF: 1 V/ms; 1 V across 1 µH: 1 A/µs | $dv/dt = i/C$, $di/dt = v/L$ |
| Energy | $\tfrac12Cv^2$, $\tfrac12Li^2$; 10 µF at 5 V: 125 µJ | zero average power in periodic steady state |
| Ceramic temperature codes | C0G: 0 ± 30 ppm/°C; X5R: ±15% over −55 to 85 °C; X7R: ±15% over −55 to 125 °C | EIA codes as tabulated by Murata ([R-110](research-log.md#r-110--mlccs-dc-bias-temperature-codes-counts-and-market-share)); the codes say nothing about DC bias |
| Class II DC-bias loss (one example) | 1 µF, 6.3 V X5R part: 0.36 µF at 3 V | manufacturer's example, case size not stated ([R-110](research-log.md#r-110--mlccs-dc-bias-temperature-codes-counts-and-market-share)) |
| MLCCs per device | about 1,000 in a high-end smartphone; 3,000–5,000 per car (2021) | Murata ([R-110](research-log.md#r-110--mlccs-dc-bias-temperature-codes-counts-and-market-share)) |
| Aluminum electrolytic life | roughly halves per 10 °C rise (60–95 °C); a low-impedance 105 °C series is rated 8,000–10,000 h at 105 °C | Nippon Chemi-Con ([R-111](research-log.md#r-111--electrolytic-life-supercapacitors-inductor-saturation-and-silicon-capacitors)) |
| Supercapacitor cell | 3,000 F at 3.0 V stores 3.75 Wh, 7.2 Wh/kg | Maxwell K2 datasheet ([R-111](research-log.md#r-111--electrolytic-life-supercapacitors-inductor-saturation-and-silicon-capacitors)) |
| Inductor saturation current | defined at a 20% (Vishay IHLP), 30% (Coilcraft) or 10% and 30% (Würth) drop in $L$ | read the footnote ([R-111](research-log.md#r-111--electrolytic-life-supercapacitors-inductor-saturation-and-silicon-capacitors), [R-082](research-log.md#r-082--inductive-power-transfer-power-inductors-and-integrated-magnetics)) |
| Silicon capacitors for power delivery | about 1.3 µF/mm² (vendor claim) | Murata ([R-111](research-log.md#r-111--electrolytic-life-supercapacitors-inductor-saturation-and-silicon-capacitors)) |

### [07-02 · First-Order RC and RL Transients](../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-02-first-order-rc-rl-transients.md)

| Quantity | Value | Note |
|---|---|---|
| Fraction completed after 1τ, 2τ, 3τ, 5τ | 63.2%, 86.5%, 95.0%, 99.3% | $1 - e^{-n}$ |
| 50% delay | $0.693\tau$ ($\tau\ln 2$) | Gate-delay model |
| 10–90% rise time | $2.197\tau$ ($\tau\ln 9$) | |
| Rise time vs bandwidth | $t_r \approx 0.35/f_{3dB}$ | [R-010](research-log.md#r-010--rise-time-and-bandwidth) |
| Settling to 0.1% | $6.91\tau$ | $\tau\ln 1000$ |
| ADC settling to ½ LSB | $(N+1)\ln 2\cdot\tau$: 6.24τ (8-bit), 9.01τ (12-bit), 11.78τ (16-bit), 14.56τ (20-bit) | [R-008](research-log.md#r-008--sar-adc-settling) |
| Charging loss | ½CV², independent of R | Fundamental |
| kT/C noise at 300 K | 64.4 µV rms (1 pF), 14.4 µV rms (20 pF) | [R-009](research-log.md#r-009--ktc-noise) |
| On-chip wire capacitance | ≈ 0.2 fF/µm | Rule of thumb, [R-004](research-log.md#r-004--on-chip-interconnect) |
| Research-stage tight-pitch wire resistance | as low as 656 Ω/µm (Ru lines, 16 nm pitch, imec 2025) | [Industry estimate], [R-004](research-log.md#r-004--on-chip-interconnect) |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| N 07-02.a | settling to 0.1 % | 6.91 | τ |
| N 07-02.b | 8-bit settling | 6.24 | τ |
| N 07-02.c | 12-bit settling | 9.01 | τ |
| N 07-02.d | 20-bit settling | 14.56 | τ |
| N 07-02.e | kT/C noise, 1 pF | 64.4 | µV |
| N 07-02.f | rise time × bandwidth (single pole) | 0.350 | — |

### [07-03 · Second-Order RLC Transients](../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-03-second-order-rlc-transients.md)

| Quantity | Value | Note |
|---|---|---|
| Overshoot of an all-pole step response | 72.9% (ζ = 0.1), 44.4% (0.25), 16.3% (0.5), 4.3% (0.707), 0 (ζ ≥ 1) | $e^{-\pi\zeta/\sqrt{1 - \zeta^2}}$ |
| Peak of a linear series RLC step, $v_C$ | at most $2V$ | Lossless limit |
| Peak current of a lightly damped series RLC step | about $V/Z_0$ | §3.7 |
| Damping resistor | $R \approx Z_0 = \sqrt{L/C}$; critical damping at $2Z_0$ (series) or $Z_0/2$ (parallel) | §3.4, §3.10 |
| RC snubber capacitor | 2–4 × the parasitic capacitance, 3× near optimal | Todd (Unitrode, 1993), [R-113](research-log.md#r-113--rc-snubbers-and-gate-drive-damping) **[Established]** |
| Hot-plug peaks, bench | 30 V supply, 0.5 µH, 1 µF ceramic: 54 V (onsemi); 24 V through 6 ft of 24-gauge pair into 4.7 µF: 50 V and 26 A (LT3684 datasheet) | [R-112](research-log.md#r-112--hot-plug-overshoot-with-ceramic-input-capacitors) **[Established]** |
| Short cable | 12 in of 18 AWG with the supply: about 500 nH and 120 mΩ | onsemi AND90059, [R-112](research-log.md#r-112--hot-plug-overshoot-with-ceramic-input-capacitors) **[Established]** |
| Probe ground lead | about 150 nH for a 6-inch lead (Tektronix); about 20 nH per inch (Teledyne LeCroy); ground spring 10–20 nH | [R-114](research-log.md#r-114--oscilloscope-probe-ground-lead-ringing) **[Industry estimate]** |
| Probe ringing with a 6-inch lead and about 11 pF | about 125–140 MHz | [R-114](research-log.md#r-114--oscilloscope-probe-ground-lead-ringing) |
| GaN power-loop inductance | about 0.4 nH (EPC, optimized layout) to about 2.5 nH (TI layout example) | [R-115](research-log.md#r-115--gan-power-loop-inductance-switching-speed-and-output-capacitance) **[Industry estimate]** |
| GaN output capacitance | EPC2045: 295 pF typ at 50 V; LMG342xR030: 170 pF typ at 400 V | Datasheets, [R-115](research-log.md#r-115--gan-power-loop-inductance-switching-speed-and-output-capacitance) **[Established]** |
| GaN switching speed | 60 V/ns (EPC2045 buck example); 20–150 V/ns adjustable (LMG342xR030) | [R-115](research-log.md#r-115--gan-power-loop-inductance-switching-speed-and-output-capacitance) |
| Decoupling capacitor ESL | 0.5–1 nH (TI, mid-frequency capacitors) | [R-116](research-log.md#r-116--pdn-target-impedance-in-vendor-practice) **[Established]** |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| N 07-03.a | overshoot at ζ = 0.1 | 72.9 | % |
| N 07-03.b | overshoot at ζ = 0.25 | 44.4 | % |
| N 07-03.c | overshoot at ζ = 0.5 | 16.3 | % |
| N 07-03.d | overshoot at ζ = 0.707 | 4.3 | % |
| N 07-03.e | probe ring, 150 nH and 10.8 pF | 125.0 | MHz |

### [07-04 · Laplace-Domain Circuit Analysis](../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-04-laplace-domain-circuit-analysis.md)

| Quantity | Value | Note |
|---|---|---|
| Inductor initial-condition source | $L\,i(0^-)$ in V·s, or $i(0^-)/s$ in parallel | §3.2 |
| Capacitor initial-condition source | $v(0^-)/s$ in series, or $C\,v(0^-)$ in A·s in parallel | §3.2 |
| ESR zero | $f_z = 1/(2\pi R_{ESR}C)$: about 30 kHz for 10 µF tantalum at 0.5 Ω, above 3 MHz for 10 µF ceramic at 5 mΩ | TI AN-1482, [R-117](research-log.md#r-117--ldo-stability-and-output-capacitor-esr) **[Industry estimate]** (typical ESRs) |
| Legacy LDO ESR window | TPS760xx: at least 2.2 µF with ESR 0.1–20 Ω (datasheet 1998, rev. 2001); TI's 1999 "tunnel of death" example: 0.2–9 Ω at 4.7 µF | [R-117](research-log.md#r-117--ldo-stability-and-output-capacitor-esr) **[Established]** |
| Typical stable ESR ranges | electrolytic-stable LDOs about 0.1–10 Ω; ceramic-stable designs from 0 Ω up to about 0.5 Ω | TI AN-1482 **[Industry estimate]** |
| Current LDOs | "Stable with 1-µF output capacitors" (TPS7A26, TPS7A25); TPS7A20: 1 µF ceramic, ESR ≤ 100 mΩ; onsemi NCP114: no minimum ESR, maximum below 2 Ω | [R-117](research-log.md#r-117--ldo-stability-and-output-capacitor-esr) **[Established]** |
| Phase-margin guideline | at least 45–50° | TI AN-1889, [R-119](research-log.md#r-119--loop-gain-measurement-by-injection) **[Industry estimate]** |
| Loop-injection resistor | 10 Ω (OMICRON Lab); 20 Ω (TI) | [R-119](research-log.md#r-119--loop-gain-measurement-by-injection) |
| Decompensated op-amps | OPA637 stable in gains ≥ 5 (OPA627 unity-gain stable); OPA847 stable for gains ≥ 12, gain–bandwidth 3.9 GHz typical | Datasheets, [R-120](research-log.md#r-120--decompensated-op-amps) **[Established]** |
| Third-order Butterworth step overshoot | 8.15% | Example 07-04.2 |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| N 07-04.a | ESR zero, 0.1 Ω and 2.2 µF | 723.4 | kHz |
| N 07-04.b | ESR zero, 20 Ω and 2.2 µF | 3.617 | kHz |
| N 07-04.c | ESR zero, 10 µF and 0.5 Ω | 31.83 | kHz |

### [07-05 · Sinusoidal Steady State, Phasors and Impedance](../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-05-sinusoidal-steady-state-and-impedance.md)

| Quantity | Value | Note |
|---|---|---|
| Reactance of 1 µF | 3.183 kΩ at 50 Hz, 159.2 Ω at 1 kHz, 0.1592 Ω at 1 MHz | $1/(\omega C)$: falls tenfold per decade of frequency |
| Reactance of 1 µH | 6.283 Ω at 1 MHz, 628.3 Ω at 100 MHz | $\omega L$: rises tenfold per decade |
| Series ↔ parallel conversion | $R_p = R_s(1 + Q^2)$; $C_p = C_s/(1 + D^2)$ | §3.3 |
| Magnitude error ↔ phase error | a relative error $\varepsilon$ in a phasor turns it by at most $\varepsilon$ rad: 0.05% ↔ 0.029° | §9 |
| Bench LCR meters and impedance analyzers | "basic" accuracy 0.05–0.08% in $\lvert Z\rvert$ and 0.03–0.05° in phase, from millihertz to megahertz | R&S LCX, Hioki IM3570, Zurich Instruments MFIA; [R-123](research-log.md#r-123--impedance-measurement-instruments) **[Established]** |
| Body-composition bioimpedance | single frequency most commonly 50 kHz; multifrequency e.g. 5–250 kHz; about 1 kΩ to measure on a wrist device | TI SBAA562; [R-124](research-log.md#r-124--bioimpedance-in-wearables) **[Established]** |
| Battery-cell impedance spectroscopy in a BMS IC | 0.01 Hz to 3.5 kHz; 1% accuracy specified at 200 µΩ with 1 A excitation (a 200 µV response) | TI BQ79826Z-Q1; [R-125](research-log.md#r-125--battery-impedance-spectroscopy-in-bms-ics) **[Established]** |
| Battery production impedance test | 1 kHz, "a long-standing industry standard" | NXP white paper; [R-125](research-log.md#r-125--battery-impedance-spectroscopy-in-bms-ics) **[Established]** |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| N 07-05.a | reactance of 1 µF at 50 Hz | 3.183 | kΩ |
| N 07-05.b | reactance of 1 µF at 1 kHz | 159.2 | Ω |
| N 07-05.c | reactance of 1 µF at 1 MHz | 0.1592 | Ω |
| N 07-05.d | reactance of 1 µH at 1 MHz | 6.283 | Ω |
| N 07-05.e | reactance of 1 µH at 100 MHz | 628.3 | Ω |

### [07-06 · AC Power and Power Factor](../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-06-ac-power-and-power-factor.md)

| Quantity | Value | Note |
|---|---|---|
| RMS of a sinusoid | peak/√2 (230 V RMS = 325 V peak; 120 V = 170 V) | |
| Crest factor | 1.414 (sine), 1.732 (triangle), 1 (square) | |
| Line loss versus PF | ∝ 1/PF²: PF 0.7 roughly doubles loss versus unity | §3.5 |
| PF correction | $Q_C = P(\tan\theta_1 - \tan\theta_2)$ | §3.6 |
| True PF with distortion | $\cos\phi_1/\sqrt{1 + \text{THD}^2}$ | §3.7 |
| Harmonic standard scope | IEC 61000-3-2: equipment ≤ 16 A per phase on public low-voltage networks; edition 5.0 (2018) with amendments 2020 and 2024 | [R-122](research-log.md#r-122--power-factor-harmonics-and-utility-tariffs) **[Established]** |
| Class D threshold | PCs, monitors, TVs from 75 W input; harmonics to the 39th | onsemi PFC handbook, [R-122](research-log.md#r-122--power-factor-harmonics-and-utility-tariffs) **[Industry estimate]** |
| 80 PLUS PF floors (115 V internal) | PF ≥ 0.90 (Standard to Gold), ≥ 0.95 (Platinum and up); Titanium and Ruby at 20% load | [R-122](research-log.md#r-122--power-factor-harmonics-and-utility-tariffs) **[Established]** |
| 80 PLUS data-center Ruby | 90/91/95/96.5/92% efficiency at 5/10/20/50/100% load; PF ≥ 0.96 from 20% load | [R-122](research-log.md#r-122--power-factor-harmonics-and-utility-tariffs) **[Established]** |
| Utility PF thresholds | 0.90 common (Austin Energy, Minnesota Power); 0.95 (City of Dover, DE) | [R-122](research-log.md#r-122--power-factor-harmonics-and-utility-tariffs) **[Established]**, utility-specific |

### [07-07 · Frequency Response and Bode Plots](../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-07-frequency-response-and-bode-plots.md)

| Quantity | Value | Note |
|---|---|---|
| Voltage ratios | ×2 = 6.02 dB; ×√2 = 3.01 dB; ×10 = 20 dB; ×1000 = 60 dB | power ratios: half these |
| Slope of one pole | 20 dB/decade = 6.02 dB/octave | §3.3 |
| Single real pole | −3.01 dB and −45° at the corner; −0.97 dB an octave away; phase-asymptote error ≤ 5.71° | §3.4 |
| Complex pair at $\omega_0$ | $20\lg Q$ above the asymptotes; phase −90° | §3.4 |
| Neper | 1 Np = 8.686 dB; 1 dB = 0.1151 Np | §3.2 |
| dBu reference | 0.7746 V (1 mW in 600 Ω) | §3.2 |
| Rise time × bandwidth | 0.35 (single pole), 0.34 (Gaussian), 0.45 (brick-wall) | §3.7, §9 |
| Cascade of $n$ equal poles | bandwidth × 0.644, 0.510, 0.435 for $n$ = 2, 3, 4 | §3.7 |
| Gain–bandwidth product | closed-loop bandwidth = GBW / noise gain | §3.8 |
| Phase margin of a two-pole loop | 65.5° gives no peaking (ζ = 0.707); 51.8° gives 1.25 dB of peaking and about 16% overshoot | §3.9 |
| A general-purpose CMOS op-amp | TLV9061: GBW 10 MHz, phase margin 55°, slew rate 6.5 V/µs (typical); open-loop gain 130 dB typical, 104 dB minimum | [R-129](research-log.md#r-129--op-amp-frequency-response-specifications) **[Established]** |
| Oscilloscope bandwidth | the −3 dB frequency; "5× rule" for < 2% amplitude error | [R-130](research-log.md#r-130--oscilloscope-bandwidth-and-rise-time) **[Industry estimate]** for the rule |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| N 07-07.a | 1 V RMS across 50 Ω, as a power level | 13.01 | dBm |
| N 07-07.b | +4 dBu as a voltage | 1.228 | V |
| N 07-07.c | dBu reference voltage | 0.7746 | V |
| N 07-07.d | one neper | 8.686 | dB |
| N 07-07.e | one decibel | 0.1151 | Np |
| N 07-07.f | single-pole error one octave from the corner | −0.97 | dB |
| N 07-07.g | single-pole error one decade from the corner | −0.04 | dB |
| N 07-07.h | largest phase-asymptote error | 5.71 | ° |
| N 07-07.i | single-pole phase slope at the corner | 65.96 | °/decade |
| N 07-07.j | phase slope at $\omega_0$ for ζ = 1 | 131.9 | °/decade |
| N 07-07.k | correction at $\omega_0$ for ζ = 0.1 | 13.98 | dB |
| N 07-07.l | phase of a 1 ns delay at 10 MHz | −3.6 | ° |
| N 07-07.m | bandwidth factor, 2 equal poles | 0.644 | — |
| N 07-07.n | bandwidth factor, 3 equal poles | 0.510 | — |
| N 07-07.o | bandwidth factor, 4 equal poles | 0.435 | — |
| N 07-07.p | rise time × bandwidth, Gaussian | 0.34 | — |
| N 07-07.q | rise time × bandwidth, brick-wall | 0.45 | — |
| N 07-07.r | Gaussian rise time / σ | 2.563 | — |
| N 07-07.s | rise-time quadrature rule, largest error for two single poles | 7.5 | % |
| N 07-07.t | bandwidth for a 1 ns single-pole rise time | 350 | MHz |
| N 07-07.u | crossover ratio $\omega_c/\omega_t$, second pole at $\omega_t$ | 0.786 | — |
| N 07-07.v | phase margin, second pole at $\omega_t$ | 51.8 | ° |
| N 07-07.w | closed-loop peaking, second pole at $\omega_t$ | 1.25 | dB |
| N 07-07.x | step overshoot at ζ = 0.5 | 16 | % |
| N 07-07.y | phase margin, second pole at $2\omega_t$ | 65.5 | ° |
| N 07-07.z | ζ for a 30° phase margin | 0.27 | — |
| N 07-07.aa | peaking for a 30° phase margin | 5.7 | dB |
| N 07-07.ab | 07-03's turn-on peak of the LC filter | 9.17 | V |

### [07-08 · Filters and Resonance](../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-08-filters-and-resonance.md)

| Quantity | Value | Note |
|---|---|---|
| Series RLC | $\omega_0 = 1/\sqrt{LC}$; $Q = Z_0/R$; bandwidth $f_0/Q$ | §3.2 |
| Parallel RLC | $Q = R/Z_0$ | §3.3 |
| Butterworth section Q | 0.7071 (n = 2); 1.000 (n = 3); 0.5412, 1.307 (n = 4); 0.6180, 1.618 (n = 5) | §3.7 |
| Attenuation per pole at five times the cutoff | about 14 dB | $20\lg5$ |
| Equal-component Sallen–Key Q sensitivity | $KQ$: 1.12 for a Butterworth section, 8 for $Q$ = 3 | §3.8 |
| One resonator's insertion loss | $-20\lg(1 - Q_L/Q_u)$ | §3.9 |
| Quartz crystal | maximum $Q\cdot f$ ≈ 16 million (f in MHz) for AT-cut; $Q$ ~ $10^6$ in a 5 MHz frequency standard | [R-133](research-log.md#r-133--resonator-q-by-technology) **[Established]** |
| SAW resonator, 433.92 MHz | $Q_u$ = 9000; $Q_L$ = 1458 in 50 Ω | [R-133](research-log.md#r-133--resonator-q-by-technology) **[Established]** |
| BAW/FBAR and advanced SAW | $f\cdot Q$ ≈ $5\times10^{12}$ Hz: about 2500 at 2 GHz | [R-133](research-log.md#r-133--resonator-q-by-technology) **[Established]** (a literature summary) |
| 0603 chip inductor, 27 nH | $Q$ ≥ 40 at 250 MHz; 75 typical at 900 MHz | [R-133](research-log.md#r-133--resonator-q-by-technology) **[Established]** |
| On-chip spiral inductor, 10 nH | "record" $Q$ ≈ 13 at about 1 GHz (2004) | [R-133](research-log.md#r-133--resonator-q-by-technology) **[Established]** (dated) |
| Op-amp gain–bandwidth for an active filter | about 100 × gain × $Q$ × cutoff (rules of thumb) | [R-132](research-log.md#r-132--active-filter-practice) **[Industry estimate]** |
| Anti-alias attenuation for 12 bits | 1 LSB: 72.2 dB; ½ LSB: 78.3 dB | $20\lg2^{12}$, $20\lg2^{13}$ |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| N 07-08.a | Q sensitivity, Butterworth equal-component section | 1.12 | — |
| N 07-08.b | Q sensitivity, Q = 3 section | 8 | — |
| N 07-08.c | Butterworth Q, n = 2 | 0.7071 | — |
| N 07-08.d | Butterworth Q, n = 3 | 1.000 | — |
| N 07-08.e | Butterworth lower Q, n = 4 | 0.5412 | — |
| N 07-08.f | Butterworth higher Q, n = 4 | 1.307 | — |
| N 07-08.g | Butterworth lower Q, n = 5 | 0.6180 | — |
| N 07-08.h | Butterworth higher Q, n = 5 | 1.618 | — |
| N 07-08.i | attenuation per pole at 5× cutoff | 14 | dB |
| N 07-08.j | 1 LSB of 12 bits | 72.2 | dB |
| N 07-08.k | ½ LSB of 12 bits | 78.3 | dB |

### [07-09 · Mutual Inductance and Transformers](../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-09-mutual-inductance-and-transformers.md)

| Quantity | Value | Note |
|---|---|---|
| Coupling coefficient | $0 \le k = M/\sqrt{L_1L_2} \le 1$ | §3.3 |
| Ideal transformer | $V_2/V_1 = N_2/N_1$; $I_2/I_1 = N_1/N_2$; $Z_{in} = (N_1/N_2)^2Z_L$ | §3.5 |
| Transformer equation | $V_{rms} = 4.443\,fNAB_m$ | §3.9 |
| Maximum efficiency | where copper loss = core loss: $x^* = \sqrt{P_{core}/P_{cu}}$ | §3.8 |
| US distribution-transformer efficiency, 50 kVA single-phase liquid-immersed, non-submersible (at 50% load) | 99.11% (from 2016); 99.15% (compliance from 23 Apr 2029) | [R-135](research-log.md#r-135--distribution-transformer-efficiency-standards) **[Established]** (under review, §9) |
| Same, 167 kVA | 99.33% → 99.46% | [R-135](research-log.md#r-135--distribution-transformer-efficiency-standards) **[Established]** |
| Same, low-voltage dry-type three-phase 75 kVA (at 35% load) | 98.60% → 98.88% | [R-135](research-log.md#r-135--distribution-transformer-efficiency-standards) **[Established]** |
| Qi wireless charging | 5 W (v1.0, 2010); 15 W (v1.2, 2015); Magnetic Power Profile at 360 kHz (v2.0, 2023); 25 W (v2.2, 2025) | [R-136](research-log.md#r-136--qi-wireless-charging-versions) **[Established]** |
| GaN charger switching frequency | about 180 kHz at full load (a 65 W GaN reference design) versus "around 100KHz" for silicon | [R-137](research-log.md#r-137--high-frequency-charger-transformers) **[Industry estimate]** (vendor claim) |

### [07-10 · Two-Port Networks](../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-10-two-port-networks.md)

| Quantity | Value | Note |
|---|---|---|
| Reciprocity | $z_{12} = z_{21}$; $h_{12} = -h_{21}$; $AD - BC = 1$; $S_{12} = S_{21}$ | §3.7 |
| Cascade | ABCD matrices multiply; matched insertion losses add in dB | §3.5, §9 |
| Return loss | 10 dB: 10% of the power reflected; 20 dB: 1% | §3.9 |
| Reference impedance | 50 Ω for most RF and test equipment | §3.9 |
| 2N3904 h-parameters (1 mA, 10 V, 1 kHz) | $h_{ie}$ 1–10 kΩ; $h_{re}$ (0.5–8)×10⁻⁴; $h_{fe}$ 100–400; $h_{oe}$ 1–40 µS | [R-138](research-log.md#r-138--transistor-h-parameters-in-datasheets) **[Established]** |
| Flagship vector network analyzers | 10 MHz to 67 GHz (R&S ZNA, Keysight PNA-X), to 110–120 GHz in extended systems; system dynamic range above 129–131 dB at a few GHz | [R-140](research-log.md#r-140--vector-network-analyzers) **[Established]** |
| 100 Gb/s per lane backplane (IEEE 802.3ck objective) | insertion loss ≤ 28 dB at 26.56 GHz | [R-141](research-log.md#r-141--serdes-channel-loss-budgets) **[Established]** |
| 200 Gb/s per lane backplane (IEEE P802.3dj objective) | die-to-die insertion loss ≤ 40 dB at 53.125 GHz | [R-141](research-log.md#r-141--serdes-channel-loss-budgets) **[Established]** |
| PCIe 6.0 channel | pad-to-pad loss < 32 dB at 16 GHz (36 dB for PCIe 5.0) | [R-141](research-log.md#r-141--serdes-channel-loss-budgets) **[Industry estimate]** (work-group slides on a draft) |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| N 07-10.a | power reflected at 10 dB return loss | 10 | % |
| N 07-10.b | power reflected at 20 dB return loss | 1 | % |

### [07-11 · Three-Phase Circuits](../courses/07-circuit-analysis-2-transient-and-ac/chapters/07-11-three-phase-circuits.md)

| Quantity | Value | Note |
|---|---|---|
| Line versus phase (Y) | $V_L = \sqrt3V_p$, line voltage leads by 30° | §3.1 |
| Line versus phase (Δ) | $I_L = \sqrt3I_p$, line current lags by 30° | §3.3 |
| Three-phase power | $P = \sqrt3V_LI_L\cos\theta$ | §3.4 |
| Copper for the same power and loss | 75% of single phase | §3.4 |
| Triplen harmonics | add in the neutral: $3I_3$ | §3.5 |
| Standard low-voltage systems | 230/400 V and 400/690 V (IEC 60038 Ed. 7.0, 2009; consolidated with Amendment 1 as Ed. 7.1, 2021); 120/208 V and 277/480 V in North America | [R-014](research-log.md#r-014--nominal-mains-voltages), [R-142](research-log.md#r-142--three-phase-distribution-voltages) **[Established]** |
| North American data-center alternative | 240/415 V via an autotransformer instead of a 480–208 V PDU transformer | [R-142](research-log.md#r-142--three-phase-distribution-voltages) **[Industry estimate]** |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| N 07-11.a | three-phase copper as a share of single phase | 75 | % |
| N 07-11.b | line voltage for a 230 V phase voltage | 398 | V |

## [08 · Digital Logic Design](../courses/08-digital-logic-design/README.md)

### [08-01 · Number Systems and Codes](../courses/08-digital-logic-design/chapters/08-01-number-systems-and-codes.md)

| Quantity | Value | Note |
|---|---|---|
| Powers of two | $2^{10}$ = 1024 ≈ 10³; $2^{16}$ = 65 536; $2^{32}$ ≈ 4.295 × 10⁹; $2^{64}$ ≈ 1.845 × 10¹⁹ | "kibi" (Ki) = 1024, so 4 GiB = $2^{32}$ bytes |
| Bits to decimal digits | $\log_{10}2$ = 0.3010: $n$ bits carry about $0.3n$ digits; 10 bits ≈ 3 digits | §3.1 |
| Two's-complement ranges | 8-bit −128 to 127; 16-bit −32 768 to 32 767; 32-bit to 2 147 483 647 ≈ 2.147 × 10⁹ | §3.3 |
| Widths that grow | product of $n$- and $m$-bit signed numbers: $n + m$ bits; sum of $N$ terms: $\lceil\log_2 N\rceil$ guard bits | §3.5 |
| Float precision | FP32 ≈ 7.2 digits, FP16 ≈ 3.3, bfloat16 ≈ 2.4, E4M3 ≈ 1.2 | §3.6 table |
| Check-bit overheads | byte parity 1 bit in 9 (11.1%); (72,64) SEC-DED 12.5%; DDR5 on-die SEC (136,128) 6.25%; Ethernet CRC-32 on a 1500-byte payload 0.267% | §3.8, §9 |
| Block-scaled 4-bit formats | MXFP4 4.25 bits per element (32-element blocks); NVFP4 4.5 bits per value (16-value blocks) | [R-143](research-log.md#r-143--block-scaled-ai-number-formats) **[Established]** |
| Unicode | code space U+0000 to U+10FFFF = 1 114 112 code points; Unicode 17.0 (Sep 2025) assigns 159 801 characters, about 14.3% of the space | [R-146](research-log.md#r-146--unicode-releases) **[Established]** |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| N 08-01.a | $2^{32}$ | 4.295e9 | — |
| N 08-01.b | $2^{64}$ | 1.845e19 | — |
| N 08-01.c | $\log_{10}2$ | 0.3010 | — |
| N 08-01.d | largest 32-bit two's-complement value | 2147483647 | — |
| N 08-01.e | byte-parity overhead, 1 bit in 9 | 11.1 | % |
| N 08-01.f | (72,64) SEC-DED overhead | 12.5 | % |
| N 08-01.g | Ethernet CRC-32 overhead on a 1500-byte payload | 0.267 | % |
| N 08-01.h | Unicode code points, U+0000 to U+10FFFF | 1114112 | — |
| N 08-01.i | share of the code space assigned in Unicode 17.0 | 14.3 | % |

### [08-02 · Boolean Algebra and Logic Gates](../courses/08-digital-logic-design/chapters/08-02-boolean-algebra-and-gates.md)

| Quantity | Value | Note |
|---|---|---|
| Functions of $n$ inputs | $2^{2^n}$: 16 for 2, 256 for 3, 65 536 for 4, ≈ 1.845 × 10¹⁹ for 6 | §3.1 |
| Truth-table rows | $2^n$; a 6-input lookup table stores 64 bits | §3.4 |
| Static CMOS transistor counts | inverter 2; NAND2 and NOR2 4; AND2 and OR2 6; $k$-input NAND or NOR $2k$; AOI22 8; static XOR2 12 | §3.8 |
| Series stack height | rarely more than about 4 transistors | §3.8, [19-04](../courses/19-digital-vlsi-design/chapters/19-04-sizing-and-logical-effort.md) |
| Exhaustive checking at 10⁹ vectors per second | 20 inputs: about a millisecond; 40 inputs: about 18 minutes; 64 inputs: about 585 years | §3.5 |
| SKY130 high-density cells (130 nm open PDK) | inverter 2 transistors, NAND2 4, NOR2 4, D flip-flop 24; nMOS 0.65 µm and pMOS 1.0 µm wide at 0.15 µm length | [R-148](research-log.md#r-148--standard-cell-library-structure-sky130) **[Established]** |
| Large-chip transistor counts | NVIDIA B200: 208 billion on two dies (2024); Apple M4: 28 billion (2024) | [R-149](research-log.md#r-149--chip-transistor-counts) **[Established]** (vendor-disclosed) |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| N 08-02.a | exhaustive check of 20 inputs at 10⁹ per second | 1.05 | ms |
| N 08-02.b | exhaustive check of 40 inputs at 10⁹ per second | 18.3 | min |

### [08-03 · Logic Minimization: K-Maps and Beyond](../courses/08-digital-logic-design/chapters/08-03-logic-minimization.md)

| Quantity | Value | Note |
|---|---|---|
| Minterms covered by a term with $k$ of $n$ literals | $2^{n-k}$ | §3.2 |
| Product terms in $n$ variables | $3^n$ (81 for four) | §3.2 |
| Practical K-map limit | 4 variables comfortably, 5–6 with effort | §3.6 |
| Practical limit of exact minimization | tens of inputs; heuristics beyond | §3.6 |
| Espresso | Brayton, Hachtel, McMullen and Sangiovanni-Vincentelli, 1984 (work from 1979 at IBM and UC Berkeley) | [R-150](research-log.md#r-150--logic-synthesis-tools) **[Established]** |
| EDA revenue (FY2025) | Synopsys $7.054 B; Cadence $5.297 B | [R-151](research-log.md#r-151--eda-industry-revenue-and-structure) **[Established]** (company reports) |
| EDA industry revenue, Q2 2026 | $5.71 B in the quarter, +12.2% year on year | [R-151](research-log.md#r-151--eda-industry-revenue-and-structure) **[Industry estimate]** (ESD Alliance survey) |

### [08-04 · Combinational Building Blocks](../courses/08-digital-logic-design/chapters/08-04-combinational-building-blocks.md)

| Quantity | Value | Note |
|---|---|---|
| $2^k$:1 multiplexer tree | $2^k - 1$ two-input muxes in $k$ levels | §3.2 |
| Function with a multiplexer | any $n$-input function from a $2^{n-1}$:1 mux and an inverter | §3.2 |
| Decoder | $n$ inputs, $2^n$ one-hot outputs | §3.3 |
| Full adder | $S = A \oplus B \oplus C_{in}$; $C_{out} = G + P\,C_{in}$ | §3.5 |
| Ripple-carry adder delay | $2n$ gate delays to the top sum bit (unit-delay model) | §3.5 |
| Equality comparator | $n$ XNORs and $\lceil \log_2 n \rceil$ AND levels | §3.7 |
| 74HC151 8:1 multiplexer, 4.5 V, 50 pF load (TI SN74HC151) | data-select-to-output 30 ns typical, 50 ns maximum at 25 °C, 63 ns maximum over the commercial range | [R-152](research-log.md#r-152--discrete-logic-propagation-delays) **[Established]** (datasheet, read from search excerpts) |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| N 08-04.a | SN74HC151 maximum over typical, 25 °C | 1.67 | — |
| N 08-04.b | SN74HC151 full-range maximum over typical | 2.1 | — |

### [08-05 · Introduction to Verilog/SystemVerilog and Testbenches](../courses/08-digital-logic-design/chapters/08-05-verilog-and-testbenches.md)

| Quantity | Value | Note |
|---|---|---|
| Random coverage with $N = M$ vectors | $1 - 1/e$ ≈ 63.2% | §3.8 |
| Random vectors to cover everything | $M H_M \approx M(\ln M + 0.577)$ | §3.8 |
| Practical exhaustive limit | about 20–30 input bits ($10^6$ to $10^9$ vectors) | §3.8 |
| Unsized literal | 32-bit signed integer | §3.4 |
| SystemVerilog standard | IEEE 1800-2023, published 28 Feb 2024; merged Verilog (IEEE 1364-2005) in 2009 | [R-153](research-log.md#r-153--hdl-standards-and-open-source-tools) **[Established]** |
| Open-source tools (Nov 2026) | Icarus Verilog 13.0 (Mar 2026); Verilator 5.054 (Nov 2026); cocotb 2.1.0 (Aug 2026); GTKWave 3.3 stable, 4.0 pre-release | [R-153](research-log.md#r-153--hdl-standards-and-open-source-tools) **[Established]** |

### [08-06 · Latches, Flip-Flops and Sequential Timing](../courses/08-digital-logic-design/chapters/08-06-latches-and-flip-flops.md)

| Quantity | Value | Note |
|---|---|---|
| Setup constraint | $t_{pcq} + t_{pd} + t_{\text{setup}} \le T_c$ | §3.7 |
| Hold constraint | $t_{ccq} + t_{cd} \ge t_{\text{hold}}$, independent of $T_c$ | §3.7 |
| D latch transistor counts | 18 (NAND-based), 10 (transmission gates) | §3.3 |
| SKY130 basic D flip-flop (dfxtp_1, typical corner, 1.8 V, 25 °C) | 24 transistors ([R-148](research-log.md#r-148--standard-cell-library-structure-sky130)); 20.0 µm²; clock-to-Q about 0.3 ns into a few femtofarads; setup 0.05–0.10 ns and hold slightly negative at the fastest slews (hold turns positive with slow clock edges) | [R-154](research-log.md#r-154--flip-flop-timing-data) **[Established]** (library data) |
| TI SN74LVC74A D flip-flop, 3.3 V, 50 pF | setup 3 ns, hold 1 ns, clock-to-Q 5.2 ns maximum | [R-154](research-log.md#r-154--flip-flop-timing-data) **[Established]** (datasheet SCAS287W) |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| N 08-06.a | SKY130 dfxtp_1 clock-to-Q rise, 53 ps clock slew, 3.4 fF | 0.307 | ns |
| N 08-06.b | SKY130 dfxtp_1 clock-to-Q fall, same conditions | 0.297 | ns |
| N 08-06.c | SKY130 dfxtp_1 setup, D rising, fastest slews | 0.051 | ns |
| N 08-06.d | SKY130 dfxtp_1 setup, D falling, fastest slews | 0.103 | ns |
| N 08-06.e | SKY130 dfxtp_1 hold, D rising, fastest slews | -0.029 | ns |
| N 08-06.f | SKY130 dfxtp_1 area | 20.0 | µm² |
| N 08-06.g | SKY130 nand2_1 area | 3.75 | µm² |
| N 08-06.h | flip-flop area in NAND2 equivalents | 5.3 | — |
| N 08-06.i | SKY130 setup, D rising, 1.5 ns clock transition | -0.045 | ns |
| N 08-06.j | SKY130 hold, D rising, 1.5 ns clock transition | 0.058 | ns |

### [08-07 · Registers, Counters and Shift Registers](../courses/08-digital-logic-design/chapters/08-07-registers-counters-shift-registers.md)

| Quantity | Value | Note |
|---|---|---|
| States: ring, Johnson, binary with $n$ flip-flops | $n$, $2n$, $2^n$ | §3.5 |
| Binary counter toggles | about 2 per count; Gray code exactly 1 | §3.3 |
| Ripple counter settling | $n\,t_{cq}$ | §3.4 |
| Maximal LFSR period | $2^n - 1$ (all nonzero states) | §3.6 |
| m-sequence balance | $2^{n-1}$ ones and $2^{n-1} - 1$ zeros per period | §3.6 |
| Standard PRBS polynomials | PRBS7 $x^7 + x^6 + 1$; PRBS15 $x^{15} + x^{14} + 1$; PRBS23 $x^{23} + x^{18} + 1$; PRBS31 $x^{31} + x^{28} + 1$ | [R-155](research-log.md#r-155--prbs-and-lfsr-references) **[Established]** (primitivity machine-checked) |
| PRBS periods | 127; 32 767; 8 388 607; 2 147 483 647 bits | §3.6 |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| N 08-07.a | PRBS7 period | 127 | bit |
| N 08-07.b | PRBS15 period | 32767 | bit |
| N 08-07.c | PRBS23 period | 8388607 | bit |

### [08-08 · Finite State Machines](../courses/08-digital-logic-design/chapters/08-08-finite-state-machines.md)

| Quantity | Value | Note |
|---|---|---|
| Flip-flops for $N$ states | $\lceil \log_2 N \rceil$ binary; $N$ one-hot | §3.4 |
| Illegal codes | $2^{\lceil \log_2 N \rceil} - N$ binary; $2^N - N$ one-hot | §3.7 |
| Transitions to specify | $|S| \cdot 2^k$ for $k$ input bits | §3.1 |
| Mealy versus Moore | Mealy outputs lead by one cycle; Moore needs at most $|S|\cdot|O|$ states | §3.2 |
| Yosys automatic re-encoding | one-hot below 32 states, binary from 32 | [R-156](research-log.md#r-156--fsm-synthesis-and-protocol-state-machines) **[Established]** (read from the source code) |
| SKY130 flip-flop with reset (`dfrtp_1`) | 25.024 µm², about 6.7 NAND2s | [R-156](research-log.md#r-156--fsm-synthesis-and-protocol-state-machines) **[Established]** |

### [08-09 · Arithmetic Circuits](../courses/08-digital-logic-design/chapters/08-09-arithmetic-circuits.md)

| Quantity | Value | Note |
|---|---|---|
| Ripple-carry delay | $2n$ unit gate delays | §3.1, 08-04 |
| Prefix adder levels | $\log_2 n$ (Kogge–Stone, Sklansky); $2\log_2 n - 1$ (Brent–Kung) | §3.3 |
| Kogge–Stone operators | $n\log_2 n - n + 1$ | §3.3 |
| Dadda multiplier | $n^2 - 4n + 3$ full adders; levels 4, 6, 8 for 8, 16, 32 bits | §3.5 |
| Radix-4 Booth | $n/2$ partial products (signed) | §3.6 |
| Barrel shifter | $n\log_2 n$ 2:1 multiplexers | §3.7 |
| SQNR | $6.02b + 1.76$ dB for a full-scale sine | §3.8 |
| Energy per operation, 45 nm | 8-bit add 0.03 pJ, 32-bit add 0.1 pJ; 8-bit multiply 0.2 pJ, 32-bit multiply 3.1 pJ; FP32 add 0.9 pJ, multiply 3.7 pJ | [R-157](research-log.md#r-157--arithmetic-energy-and-dsp-blocks) **[Established]** (Horowitz, ISSCC 2014; read from the paper's figure) |
| FPGA DSP slice (AMD UltraScale+, DSP48E2) | 27 × 18 multiplier, 48-bit accumulator (as of Nov 2026) | [R-157](research-log.md#r-157--arithmetic-energy-and-dsp-blocks) **[Established]** |

### [08-10 · Timing, Metastability and Clock-Domain Crossing](../courses/08-digital-logic-design/chapters/08-10-timing-metastability-cdc.md)

| Quantity | Value | Note |
|---|---|---|
| Synchronizer MTBF | $e^{S/\tau}/(T_W F_C F_D)$ | §3.5; standard form ([R-158](research-log.md#r-158--metastability-and-synchronizers)) |
| MTBF per extra $\tau$ of waiting | ×2.72; per $2.3\,\tau$, ×10 | §3.5 |
| Two-flip-flop resolution time | $S = T_c - t_{pcq} - t_{\text{setup}}$ | §3.5 |
| Metastability time constant $\tau$ | Strongly process- and corner-dependent: one measured 65 nm low-power flip-flop ranged from under about 100 ps to several hundred ps (§9). The examples' 20–40 ps are illustrative | [R-158](research-log.md#r-158--metastability-and-synchronizers) **[Established]** for the measurement |
| Typical synchronizer depth | 2 common, 3 for more margin (Intel Quartus guidance); AMD XPM CDC macros allow 2 to 10 stages, default 4 | [R-158](research-log.md#r-158--metastability-and-synchronizers) **[Established]** |
| Asynchronous FIFO depth | $B(1 - f_r/f_w)$ plus a few words, rounded up to $2^k$ | §3.7 |
| Pipelined latency | $t_{\text{logic}} + k\,t_{\text{reg}}$ | §3.3 |

### [08-11 · Memories and Programmable Logic](../courses/08-digital-logic-design/chapters/08-11-memories-and-programmable-logic.md)

| Quantity | Value | Note |
|---|---|---|
| Memory address bits | $\log_2$(words); row bits $\log_2 R$, column bits $\log_2(C/m)$ | §3.1 |
| ROM size for an $n$-input, $m$-output function | $2^n m$ bits | §3.4 |
| PLA size | $2np + pm$ crosspoints | §3.4 |
| Functions of a $k$-LUT | $2^{2^k}$: 65 536 for $k$ = 4 | §3.4 |
| $k$-LUTs that suffice for any $n$-input function (Shannon, 2:1 multiplexers) | at most $2^{n-k+1} - 1$; fewer with 6-LUTs used as 4:1 multiplexers | §3.4 |
| $k$-LUTs for an $n$-input AND (minimum) | $\lceil (n - 1)/(k - 1) \rceil$ | §3.4 |
| Lattice iCE40 UltraPlus UP5K | 5280 logic cells (4-input LUT + flip-flop), 120 kbit block RAM in 30 blocks, 1 Mbit single-port RAM, 8 DSP blocks (16 × 16 multiply, 32-bit accumulator), 40 nm low-power CMOS | [R-159](research-log.md#r-159--fpga-devices-and-the-fpga-industry) **[Established]** (read from the data sheet) |
| AMD Virtex UltraScale+ VU19P | about 8.9 million system logic cells, 4.09 million LUTs, 3840 DSP slices, 224 Mb on-chip memory | [R-159](research-log.md#r-159--fpga-devices-and-the-fpga-industry) **[Established]** |
| FPGA break-even against ASIC | $N/(f - a)$ units | §3.5 |

### [08-12 · FPGA Implementation Flow](../courses/08-digital-logic-design/chapters/08-12-fpga-implementation-flow.md)

| Quantity | Value | Note |
|---|---|---|
| Flow steps | synthesis → placement → routing → timing analysis → bitstream | §3.1 |
| Routing share of an FPGA critical path | about two thirds in the lab's gate-level adder | Example 08-12.3 (measured) |
| Carry chain versus gate-level adder, iCE40 | about 3× faster | Example 08-12.4 (measured) |
| DSP versus LUT 16 × 16 multiplier, iCE40 | about 1/10 the logic cells, at least 3.9× faster (harness-limited) | Example 08-12.5 (measured) |
| iCE40 UP5K bitstream | 104 090 bytes, independent of design size | Example 08-12.7 (measured) |
| iCE40 UltraPlus configuration time | maximum 140 ms (default frequency), 50 ms (medium) | [R-160](research-log.md#r-160--open-source-fpga-and-asic-flows) **[Established]** (data sheet) |
| Open-source tool versions used here | Yosys 0.71 (tag dated 12 Nov 2026), nextpnr 0.11.1 | [R-160](research-log.md#r-160--open-source-fpga-and-asic-flows) **[Established]** |

## [09 · Semiconductor Devices](../courses/09-semiconductor-devices/README.md)

### [09-01 · Crystals, Energy Bands and the Semiconductor](../courses/09-semiconductor-devices/chapters/09-01-crystals-and-energy-bands.md)

| Quantity | Value | Note |
|---|---|---|
| Silicon lattice constant; atomic density; bond length | 5.431 Å; 5.0 × 10²² cm⁻³; 2.35 Å | [R-086](research-log.md#r-086--crystals-band-gaps-intrinsic-carriers-and-wide-bandgap-markets), Example 09-01.1 |
| Ge, GaAs, InP lattice constants | 5.658, 5.653, 5.870 Å | [3, 4] |
| Band gaps at 300 K | Si 1.12 (indirect), Ge 0.66 (indirect), GaAs 1.42 (direct), Ga$_{0.47}$In$_{0.53}$As 0.74 (direct) eV | [3, 4], Example 09-01.6 |
| Wide-gap materials | GaN ≈ 3.4 eV; 4H-SiC ≈ 3.2–3.3 eV | **[Contested]** beyond the first decimal ([R-161](research-log.md#r-161--crystal-band-structure-and-alloy-parameters)) |
| Silicon gap temperature coefficient | about −0.25 meV/K near 300 K | Example 09-01.6 |
| Silicon effective masses | $m_l$ 0.98, $m_t$ 0.19, $m_{hh}$ 0.49, $m_{lh}$ 0.16 $m_0$; conductivity mass 0.26 $m_0$ | [3], Example 09-01.4 |
| GaAs electron mass | 0.067 $m_0$ at the band edge (about 0.063 $m_0$ at 300 K) | [3, 4] |
| Silicon $N_C$, $N_V$ at 300 K | 2.8 × 10¹⁹, 1.04 × 10¹⁹ cm⁻³ (Hu) or 3.2 × 10¹⁹, 1.8 × 10¹⁹ cm⁻³ (handbook) | Example 09-01.4 |
| Electron affinity | Si 4.05 eV, GaAs 4.07 eV | [3] |
| Band bending | a 1 V potential difference moves the bands by 1 eV | §3.7 |
| Lattice mismatch | Si–Ge 4.2%; AlAs–GaAs 0.14% | Example 09-01.6 |
| Angle between (100) and (111) | 54.74° (the sidewall angle of anisotropic etch pits in (100) silicon) | §3.2 |
| Leading-edge wafer diameter | 300 mm (as of Nov 2026) | [8] **[Established]** |

### [09-02 · Carriers, Doping and the Fermi Level](../courses/09-semiconductor-devices/chapters/09-02-carriers-doping-fermi-level.md)

| Quantity | Value | Note |
|---|---|---|
| $kT$ at 300 K; $kT\ln10$ | 25.85 meV; 59.5 meV per decade of carrier density | §3.4 |
| Silicon $N_C$, $N_V$ at 300 K | 3.2 × 10¹⁹ and 1.8 × 10¹⁹ cm⁻³ (handbook; Hu: 2.8 and 1.04 × 10¹⁹) | [1, 2], 09-01 Example 4 |
| Silicon $n_i$ at 300 K | 1.0 × 10¹⁰ cm⁻³ (course value); 9.65 × 10⁹ cm⁻³ (best measurement) | [3] **[Established]** |
| GaAs, Ge $n_i$ at 300 K | about 2 × 10⁶ and 2 × 10¹³ cm⁻³ | [1], Example 09-02.2 |
| Silicon $n_i$ growth, 300 K → 400 K | about 500-fold | §3.8 |
| Shallow donor and acceptor levels in Si | P 45, As 54, Sb 43 meV; B 45, Al 72, Ga 74, In 157 meV | [1] |
| Hydrogenic estimate | about 26 meV, orbit about 2.4 nm | §3.5 |
| Degeneracy threshold in Si (n-type) | $N_D$ ≈ 1.6 × 10¹⁸ cm⁻³ ($E_F = E_C - 3kT$) | §3.6 |
| Band-gap narrowing (n-type Si) | ≈ 3.5 × 10⁻⁸ $N_D^{1/3}$ eV; 75 meV at 10¹⁹ cm⁻³ | [1] |
| Typical doping levels | 10¹⁴–10¹⁶ cm⁻³ (lightly doped regions), 10¹⁷–10¹⁸ (wells, channels of planar MOSFETs), 10¹⁹–10²⁰ (sources, drains, contacts) | orders of magnitude; device chapters give specifics |

### [09-03 · Carrier Transport: Drift and Diffusion](../courses/09-semiconductor-devices/chapters/09-03-drift-and-diffusion.md)

| Quantity | Value | Note |
|---|---|---|
| Lightly doped Si mobility at 300 K | $\mu_n$ ≈ 1360–1400, $\mu_p$ ≈ 450–470 cm²/V·s | [1, 2] |
| Electron thermal velocity in Si | 2.3 × 10⁷ cm/s | [1], §3.1 |
| Mean free time and path (electrons, lightly doped) | about 0.2 ps; about 45 nm | Example 09-03.1 |
| Saturation velocity at 300 K | electrons 1.07 × 10⁷, holes 8.3 × 10⁶ cm/s | [1] |
| Critical fields at 300 K | electrons about 7 kV/cm, holes about 18 kV/cm | [1] |
| Diffusion coefficients, lightly doped Si | $D_n$ ≈ 35, $D_p$ ≈ 11–12 cm²/s | [1], Example 09-03.6 |
| Einstein relation | $D = (kT/q)\mu$, $kT/q$ = 25.85 mV at 300 K | §3.7 |
| Lattice mobility temperature exponent | $\mu_L \propto T^{-2.2}$ | [1] |
| Silicon optical phonon energy | 63 meV | [1] |
| Resistivity | n-type 10¹⁵ cm⁻³: 4.6 Ω·cm; p-type 10¹⁶ cm⁻³: 1.7 Ω·cm; n-type 10¹⁹ cm⁻³: 5.4 mΩ·cm | Example 09-03.2 |
| Four-point-probe constant (thin sheet) | $R_s$ = 4.532 $V/I$ | §3.4 |
| Transit time at saturation | about 10 ps per µm | Example 09-03.5 |

### [09-04 · Generation, Recombination and the Continuity Equation](../courses/09-semiconductor-devices/chapters/09-04-generation-recombination-continuity.md)

| Quantity | Value | Note |
|---|---|---|
| Radiative coefficient | Si 1.1 × 10⁻¹⁴, GaAs 7 × 10⁻¹⁰ cm³/s | [1] |
| Auger coefficients (Si, 300 K) | $C_n$ 1.1 × 10⁻³⁰, $C_p$ 0.3 × 10⁻³⁰ cm⁶/s | [1] |
| Auger lifetime in n-type Si | 91 µs at 10¹⁷, 9.1 ns at 10¹⁹, 91 ps at 10²⁰ cm⁻³ | Example 09-04.1 |
| SRH lifetime | $1/(\sigma v_{th}N_t)$: 60 µs for 10¹² cm⁻³ traps with σ = 10⁻¹⁵ cm² | Example 09-04.1 |
| Lifetime range in practice | about 1 ms (lightly doped, high-quality Si) down to about 1 ns (heavily doped) | [1], Fig. 1.3.22–23 |
| Gold in silicon | acceptor at $E_C$ − 0.55 eV, σ_n 8 × 10⁻¹⁷, σ_p 9 × 10⁻¹⁵ cm² | [1] |
| Surface recombination velocity | 10² to (6–8) × 10⁴ cm/s; ≤ 0.5 cm/s at a good Si–SiO₂ interface | [1] |
| Intra-band versus inter-band equilibration | about 0.1 ps versus about 1 µs | [2], §3.6 |
| Diffusion length | $\sqrt{D\tau}$: 33 µm for holes with 1 µs at 10¹⁵ cm⁻³ | Example 09-04.6 |
| Generation current | $qn_iW/2\tau_0$: 80 nA/cm² for 1 µm and 1 µs | Example 09-04.7 |

### [09-05 · PN Junction Electrostatics](../courses/09-semiconductor-devices/chapters/09-05-pn-junction-electrostatics.md)

| Quantity | Value | Note |
|---|---|---|
| Silicon permittivity | 11.7 ε₀ = 1.036 × 10⁻¹² F/cm | [1] |
| Built-in potential of silicon junctions | about 0.6–0.9 V; +59.5 mV per decade of either doping | §3.2 |
| Depletion width | $\approx\sqrt{2\varepsilon_s V/qN}$: 0.33 µm at 10¹⁶ cm⁻³ and zero bias; grows as $\sqrt{V}$ (step) or $V^{1/3}$ (graded) | Examples 09-05.2, 09-05.6 |
| Peak field | $2(V_{bi} - V_A)/W$; tens of kV/cm at zero bias | §3.4 |
| Critical (breakdown) field | Si about 3 × 10⁵ V/cm; GaAs about 4 × 10⁵ V/cm | [1] |
| Debye length | $\sqrt{\varepsilon_skT/q^2N}$: 41 nm at 10¹⁶ cm⁻³ | §3.7 |
| Junction capacitance | $\varepsilon_s/W$: about 1 fF/µm² at $W$ = 0.1 µm | [2], §3.9 |
| C–V profiling | slope of $1/C^2$ gives $N$ of the lighter side | §3.9 |

### [09-06 · PN Junction I–V, Capacitance and Breakdown](../courses/09-semiconductor-devices/chapters/09-06-pn-junction-iv-and-capacitance.md)

| Quantity | Value | Note |
|---|---|---|
| Forward-voltage slope | 59.5 mV/decade at 300 K ($\eta$ = 1); 119 mV/decade ($\eta$ = 2) | §3.4, §3.5 |
| Silicon diode forward voltage | about 0.6–0.75 V at practical current densities | Example 09-06.1 |
| Measured saturation current density | 1.8 × 10⁻¹² A/cm² in Hu's measured silicon diode | [2] |
| Temperature coefficient of $V_D$ | about −2 mV/K; $(V_A - V_{g0} - 3V_T)/T$ | §3.6 |
| PTAT voltage | $(k/q)\ln(I_1/I_2)$: 198 µV/K for a ratio of 10 | §3.6 |
| $V_{g0}$ for silicon | 1.20 V | §3.6, Varshni fit [1] |
| Small-signal resistance | $V_T/I$: 25.85 Ω at 1 mA | §3.7 |
| Long-diode diffusion capacitance | $\tau g_d/2$ | §3.7 |
| Storage time ($I_R = I_F$) | 0.23τ exact; 0.69τ by charge control | §3.8 |
| Avalanche breakdown, one-sided Si junction | about 12–15 V at 10¹⁷, 55–65 V at 10¹⁶, 240–350 V at 10¹⁵ cm⁻³ (spread between routes) | §3.9 [1, 2] |
| IC junction breakdown / Si power devices | under 20 V / 100–1,000 V | [2] |
| Tunneling-breakdown field (Si) | about 10⁶ V/cm | [2] |
| Schottky barriers on n-Si | 0.4 (Mg) to 0.9 V (Pt); pinned near 0.7 V | [2] |
| Richardson constant | about 100–120 A/(cm²·K²) | §3.10, [2] |
| Schottky $I_0$ against PN | 10³–10⁸ times larger | [2] |
| Specific contact resistivity | about 10⁻⁷ Ω·cm² for Hu's 0.3 µm TiSi₂ contact | [2] |

### [09-07 · The Bipolar Junction Transistor](../courses/09-semiconductor-devices/chapters/09-07-bipolar-junction-transistor.md)

| Quantity | Value | Note |
|---|---|---|
| Transconductance | $I_C/V_T$: 38.7 mS at 1 mA | §3.9 |
| $V_{BE}$ at practical currents | about 0.7–0.9 V; −2 mV/K | Example 09-07.1, 09-06 |
| Current gain | typically ~100 (Hu's measured SiGe example about 90) | [1] |
| Early voltage | typical ~50 V; intrinsic gain $V_A/V_T$ ≈ 2,000 | [1] |
| Base transit time | $W_B^2/2D_B$: 2.5 ps for 70 nm (Hu); down to ~1 ps with grading | [1] |
| Emitter band-gap narrowing | 50 / 95 / 140 meV at 10¹⁹ / 10²⁰ / 10²¹ cm⁻³ (Hu); larger in the handbook fit | [1, 2] **[Contested]** |
| SiGe band-gap reduction | about 0.1 eV for 20% Ge | [1] |
| Kirk-effect onset | $J_K \approx qN_Cv_{\text{sat}}$: ~1–2 mA/µm² for $N_C$ ≈ 10¹⁷ cm⁻³ | §3.8, [1] |
| $V_{CE,\text{sat}}$ | tens of mV intrinsic; 0.1–0.2 V with series resistance | §3.7 |
| SiGe HBT record | f_T/f_max = 505/720 GHz (IHP, IEDM 2016) | [3] |
| Production SiGe BiCMOS | 300/500 GHz (IHP SG13G2), 470/650 GHz (SG13G3, research and prototyping), as of Feb 2026 | [4] |

### [09-08 · The MOS Capacitor](../courses/09-semiconductor-devices/chapters/09-08-mos-capacitor.md)

| Quantity | Value | Note |
|---|---|---|
| $C_{ox}$ | 345 nF/cm² at 10 nm; 3.45 µF/cm² at 1 nm EOT | §3, Example 09-08.7 |
| Si–SiO₂ barriers | 3.1 eV for electrons, 4.8 eV for holes; SiO₂ gap about 9 eV | [1] |
| Threshold condition | $\phi_s = 2\phi_B$; 0.83 V at 10¹⁷ cm⁻³ | §3.4 |
| Typical NMOS threshold | about 0.4 V (enhancement) | [1] |
| Inversion density, strongly on | a few 10¹² cm⁻² | Example 09-08.2 |
| High-quality interface charge | about 10¹⁰ cm⁻² (vs 7 × 10¹⁴ Si atoms/cm²) | [1] |
| Poly depletion | 1–2 nm; $T_{oxe} - T_{ox}$ ≈ 6–10 Å with $T_{inv}$ | [1] |
| Inversion-layer centroid | about 1.5 nm (high field) to 3 nm (low field) | [1] |
| SiO₂ leakage at 1.2 nm | about 10³ A/cm² | [1] |
| HfO₂ permittivity | $k$ ≈ 24 (Hu), 21.2 (IRDS example) | [1, 3] |
| CET roadmap | 1.0 nm (2024–2025), 0.9 nm (2027 on), IRDS 2024 | [3] |
| SiO₂ breakdown | about 15 MV/cm in a 1 s test; lower for long stress (TDDB) | [1] |

### [09-09 · The Long-Channel MOSFET](../courses/09-semiconductor-devices/chapters/09-09-long-channel-mosfet.md)

| Quantity | Value | Note |
|---|---|---|
| Square law (long channel) | $I_{Dsat} = (W/2mL)\mu C_{ox}V_{ov}^2$ | §3.3 |
| Bulk-charge factor $m$ | typically about 1.2 | [1] |
| Electron surface mobility | 540/[1 + (E/0.9 MV/cm)^1.85] cm²/V·s; ~250–350 at ~1 MV/cm | [1] |
| Hole surface mobility | up to about 185 cm²/V·s | [1] |
| $g_m/I_D$ | $2/V_{ov}$ in strong inversion; ≤ $1/(mV_T)$ in weak inversion (31.0 V⁻¹ for $m$ = 1.246); BJT 38.7 V⁻¹ | §3.6 |
| Subthreshold swing | $m \times 59.5$ mV/decade at 300 K, never below 59.5 | [3] |
| Current-defined threshold | $I_D$ = 100 nA × W/L (some use 200 nA) | [3] |
| Long-channel $f_T$ | $3\mu V_{ov}/(4\pi mL^2)$: ~5 GHz at 1 µm | Example 09-09.6 |
| Off-current targets (roadmap) | about 0.15–0.84 µA/µm for high-performance, ~10⁻⁵ µA/µm for low-standby-power devices (90–22 nm nodes) | [2] |

### [09-10 · Short-Channel Effects and Leakage](../courses/09-semiconductor-devices/chapters/09-10-short-channel-effects-and-leakage.md)

| Quantity | Value | Note |
|---|---|---|
| Inversion-layer $v_{sat}$ | 8 × 10⁶ cm/s (electrons), 6 × 10⁶ cm/s (holes) | [1] |
| Velocity-saturation field | $2v_{sat}/\mu_{ns}$: ~6–9 × 10⁴ V/cm | [1], §3.1 |
| Short-channel $I_{Dsat}$ | $WC_{ox}v_{sat}(V_{ov} - mV_{Dsat})$; linear in $V_{ov}$ | [1] |
| Injection velocity | ~1.6 × 10⁷ cm/s (electrons), 1 × 10⁷ cm/s (holes) | [1] |
| PMOS vs NMOS current | about one half | [1] |
| DIBL model | $\Delta V_{TH} = (V_{DS} + 0.4)e^{-L/l_d}$; minimum $L$ several $l_d$ | [2] |
| Swing limit | 59.5 mV/decade at 300 K, ∝ T | [2] |
| IRDS 2024 HP logic | swing 82 → 70 mV/decade, $V_{DD}$ 0.70 → 0.60 V, $L_g$ 16 → 12 nm (2024–2027) | [4] |
| Tunneling field (Si) | ~10⁶ V/cm | 09-06 |
| Random dopant σ(V_TH) | $(q/C_{ox})\sqrt{N_AW_{dep}/3WL}$: tens of mV for doped nanoscale planar devices | §3.7 |

### [09-11 · CMOS and Scaling: Moore, Dennard and Beyond](../courses/09-semiconductor-devices/chapters/09-11-cmos-and-scaling.md)

| Quantity | Value | Note |
|---|---|---|
| Inverter delay | $\tau_d = (CV_{DD}/4)(1/I_{onN} + 1/I_{onP})$ | [1] |
| Ring oscillator period | $2N\tau_d$ | §3.2 |
| Dynamic power | $\alpha CV_{DD}^2f$ | [1] |
| $W_p/W_n$ for a symmetric inverter | about 2 | [1] |
| Moore 1965 / 1975 | doubling every year / every two years | [3], [4] |
| Node shrink | 0.7× linear, 0.49× area, every 2–3 years (historical) | [2] |
| Constant-field scaling | delay $1/\kappa$, power density constant | §3.5 |
| End of frequency scaling | about 2004; clocks limited to about 5 GHz | [6] |
| Prescott (2004) | about 115 W, about 100 W/cm² | [6] |
| IRDS 2024 "3nm" / "2nm" | G48M24, 160 nm cell / G48M22, 120 nm cell | [7] |
| Intel 18A | 50 nm CPP; 160 and 180 nm cells | [8] |

### [09-12 · Advanced Transistors: FinFET, GAA, CFET and Backside Power](../courses/09-semiconductor-devices/chapters/09-12-finfet-gaa-cfet-backside-power.md)

| Quantity | Value | Note |
|---|---|---|
| Double-gate scale length | $\lambda^2 = (\varepsilon_s/2\varepsilon_{ox})t_{si}t_{ox} + t_{si}^2/8$ | §3.2 |
| Single-gate thin body | $\lambda^2 = (\varepsilon_s/\varepsilon_{ox})t_{si}t_{ox} + t_{si}^2/2$ | §3.2 |
| DIBL scaling | ∝ $e^{-L/2\lambda}$; $L \approx 6\lambda$ for ~30 mV/V in this model | Example 09-12.5 |
| UTB rule of thumb | $T_{si} < L/2$ | [1] |
| FinFET width | $W_{\text{eff}} = 2H_{fin} + W_{fin}$ | [1] |
| Nanosheet width | $N \times 2(W_{sheet} + t_{sheet})$ | §3.4 |
| Ideal multigate swing | 59.5 mV/decade at 300 K | [1] |
| Intel 22 nm tri-gate announced | May 2011 | [3] |
| Samsung 3 nm GAA production start | 30 Jun 2022 | [5] |
| Intel 18A (RibbonFET + PowerVia) HVM | announced Jan 2026 | [6] |
| IRDS: GAA to 2031, then CFET | roadmap | [4] |

### [09-13 · Compound and Wide-Bandgap Semiconductors](../courses/09-semiconductor-devices/chapters/09-13-compound-and-wide-bandgap-semiconductors.md)

| Quantity | Value | Note |
|---|---|---|
| Band gaps (eV) | Si 1.12, GaAs 1.424, InP 1.344, GaN 3.435, 4H-SiC ~3.26 | [1]–[3] |
| Electron mobility (cm²/V·s) | Si ≤ 1400, GaAs ≤ 8500, InP ≤ 5400, 4H-SiC ~1000 | [1], [3] |
| Breakdown field | Si ~3 × 10⁵, GaAs ~4 × 10⁵ V/cm; 4H-SiC ~2.7–3 MV/cm | [1], computed |
| Baliga's limit | $R_{on,sp} = 4V_B^2/\varepsilon\mu\mathcal E_c^3$ | §3.3 |
| SiC vs Si, 1200 V | ~1400× lower ideal $R_{on,sp}$ | Example 09-13.3 |
| AlGaN/GaN 2DEG | ~10¹³ cm⁻² from polarization | Example 09-13.4 |
| HBT gain | ×10 per 60 meV of $\Delta E_g$ at 300 K | §3.5 |

### [09-14 · Optoelectronic Devices](../courses/09-semiconductor-devices/chapters/09-14-optoelectronic-devices.md)

| Quantity | Value | Note |
|---|---|---|
| Photon energy | $E = 1.24/\lambda$ (eV, µm) | [1] |
| Silicon cutoff | ~1.1 µm | §3.1 |
| Maximum responsivity | $\lambda/1.24$ A/W (1.25 A/W at 1.55 µm) | §3.2 |
| Shot noise | $\overline{i_n^2} = 2qIB$ | 03-06 |
| ToF depth | 15 cm per ns of round trip | §3.3 |
| Image-sensor SNR limit | $\sqrt{N}$ electrons | §3.4 |
| Luminous efficacy at 555 nm | 683 lm/W | [1] |
| White-light efficacy limit | ~414 lm/W | [6] |
| Fiber low-loss window | 1.55 µm | [1] |
| Solar cell typical fill factor | ~0.75 | [1] |
| Record lab cells (2026) | mono-Si 28.1%, perovskite–Si tandem 35.2%, III–V concentrator 47.6% | [5] |

## [10 · Electronics I (Microelectronic Circuits)](../courses/10-electronics-1/README.md)

### [10-01 · Diodes and Diode Circuits](../courses/10-electronics-1/chapters/10-01-diodes-and-diode-circuits.md)

| Quantity | Typical value | Note |
|---|---|---|
| Silicon junction forward drop | 0.6–0.7 V at 0.1–1 mA (small diodes); about 1 V at 1 A (rectifiers) | depends on $I_S$, current and temperature |
| Voltage per decade of current | 59.5 mV × $n$ at 300 K | 09-06 |
| Temperature coefficient of forward drop | about −2 mV/K | 09-06 |
| Small-signal resistance | $nV_T/I_D$: 25.9 Ω at 1 mA ($n$ = 1) | |
| Small-signal limit | about 5 mV across the diode for 10% error | §3.4 |
| Half-wave ripple | $I_L/fC$; full-wave $I_L/2fC$ | §3.6 |
| 1N4148 switching diode | $t_{rr}$ ≤ 4 ns, $C_D$ ≤ 4 pF, $V_F$ ≤ 1 V at 10 mA [1] | Vishay data sheet, rev. Nov 2024 |
| 1N4001 rectifier | 1 A average, 30 A surge, $V_F$ ≤ 1.1 V at 1 A, $I_R$ ≤ 5 µA [2] | Vishay, rev. Apr 2020 |
| 1N5817 Schottky | $V_F$ ≤ 0.45 V at 1 A, $I_R$ ≤ 1 mA at 20 V [5] | Vishay, rev. Jul 2020 |
| 1N4733A Zener | 5.1 V ± 5% at 49 mA, $Z_{ZT}$ = 7 Ω typical, 1.3 W [3] | Vishay, rev. Nov 2024 |
| TL431 shunt reference | 2.495 V; 0.2 Ω typical at $V_{KA} = V_{ref}$, ≤ 0.5 Ω; × $(1 + R_1/R_2)$ when programmed higher [4] | TI, rev. May 2024 |

### [10-02 · MOSFET DC Operation and Biasing](../courses/10-electronics-1/chapters/10-02-mosfet-dc-operation-and-biasing.md)

| Quantity | Typical value | Note |
|---|---|---|
| Overdrive | 0.1–0.3 V in analog bias; 0.2–0.5 V or more in discrete bias and switches | larger for speed and matching, smaller for $g_m/I_D$ |
| Threshold spread, discrete MOSFET | 0.7 V min-to-max (BSS138: 0.8–1.5 V) [1] | specified, not typical |
| Threshold temperature coefficient | about −2 mV/K [1] | |
| Fixed-bias current sensitivity | $2\,\delta V_{TN}/V_{ov}$: 50 mV / 0.5 V → 20% | §3.3 |
| Power MOSFET on-resistance | about 1 mΩ at 10 V gate drive (CSD17573Q5B: 0.84 mΩ typical) [2] | 30 V class, 5 × 6 mm package |
| On-resistance rise, 25 → 125 °C | about 1.5× (BSS138 typical 0.7 → 1.1 Ω) [1] | |
| Load switch | 52 mΩ at 5 V, 53 mΩ at 3.3 V typical; 71 mΩ maximum; 2 A (TPS22918) [3] | |

### [10-03 · BJT DC Operation and Biasing](../courses/10-electronics-1/chapters/10-03-bjt-dc-operation-and-biasing.md)

| Quantity | Typical value | Note |
|---|---|---|
| Active $V_{BE}$ (small transistor, mA) | 0.6–0.75 V; 0.7 V for hand analysis | |
| $V_{CE(sat)}$ | 0.1–0.3 V (2N3904: ≤ 0.2 V at 10 mA, ≤ 0.3 V at 50 mA) [1] | at forced β = 10 |
| β spread | 3× between min and max (2N3904: 100–300 at 10 mA) [1] | falls at high current |
| $V_{BE}$ temperature coefficient | about −2 mV/K | 09-06 |
| Current growth at fixed $V_{BE}$ | about 7.7% per K; doubles every ~9 K | §3.3 |
| Small-signal emitter resistance | $V_T/I_C$: 25.9 Ω at 1 mA | 10-04 |
| 2N3904 limits | 40 V $V_{CEO}$, 200 mA, 625 mW, 200 K/W [1] | TO-92 |

### [10-04 · Small-Signal Models](../courses/10-electronics-1/chapters/10-04-small-signal-models.md)

| Quantity | Typical value | Note |
|---|---|---|
| BJT $g_m$ | 38.7 mS per mA | any size, room temperature |
| BJT $r_\pi$ at 1 mA | 2.6 kΩ × (β/100) | |
| BJT intrinsic gain | $V_A/V_T$: 1000–4000 | |
| MOSFET $g_m/I_D$ | 2/$V_{ov}$: 10 V⁻¹ at 0.2 V; up to about 30 V⁻¹ in weak inversion | |
| MOSFET intrinsic gain | 2/($\lambda V_{ov}$): tens for short channels | |
| Small-signal limit | BJT: a few mV ($2V_T$ scale); MOSFET: a fraction of $V_{ov}$ | §3.6 |
| HD₂ | $\hat v/4V_T$ (BJT); $\hat v/4V_{ov}$ (MOSFET) | |
| 2N3904 at 1 mA | $h_{ie}$ 1–10 kΩ, $h_{fe}$ 100–400, $h_{oe}$ 1–40 µS [1] | data-sheet ranges |

### [10-05 · Amplifier Fundamentals](../courses/10-electronics-1/chapters/10-05-amplifier-fundamentals.md)

| Quantity | Value | Note |
|---|---|---|
| 2× power / 2× voltage | 3.01 dB / 6.02 dB | |
| −3 dB | half power, $1/\sqrt2$ voltage | |
| 0 dBm | 1 mW; 0.224 V rms in 50 Ω | |
| 30 dBm | 1 W | |
| Class-A limit | 25% (resistive load), 50% (inductor or transformer) | |
| Class-B limit | 78.5% | 12-07 |
| Class-D audio | over 90% at high output [1] | data sheet; as of Nov 2026 |
| Coupling corner | $1/[2\pi C(R_{sig} + R_i)]$ | |

### [10-06 · MOS Single-Stage Amplifiers](../courses/10-electronics-1/chapters/10-06-mos-single-stage-amplifiers.md)

| Quantity | Typical value | Note |
|---|---|---|
| CS gain with a resistor load | $2V_{RD}/V_{ov}$: about 5 to 20 | |
| CS gain with an active load | $g_mr_o/2$: tens at short channel lengths | |
| Cascode gain | about $(g_mr_o)^2$ | |
| CG input resistance | about $1/(g_m + g_{mb})$: 50 Ω needs 20 mS | |
| Source-follower gain | below $1/(1 + \chi)$: 0.77 to 0.91 for χ = 0.1 to 0.3 | before loading |
| Source-follower output resistance | about $1/(g_m + g_{mb})$: hundreds of ohms | |
| Degeneration factor | $1 + g_mR_S$ on $G_m$ (÷) and $R_{out}$ (×) | |

### [10-07 · BJT Single-Stage Amplifiers](../courses/10-electronics-1/chapters/10-07-bjt-single-stage-amplifiers.md)

| Quantity | Typical value | Note |
|---|---|---|
| BJT CE gain, resistor load | $V_{RC}/V_T$: about 40 per volt across $R_C$ | |
| $r_\pi$ at 1 mA | 2.6 kΩ × (β/100) | |
| $r_e$ at 1 mA | about 26 Ω | |
| Reflection | × (β + 1) into the base, ÷ (β + 1) into the emitter | |
| Degenerated $R_{out}$ ceiling | about $\beta r_o$ | |
| Emitter-follower gain | 0.9–0.99 into moderate loads | no body effect |
| 2N3904 $h_{fe}$ at 1 mA | 100–400 [1] | data sheet |
| SiGe HBT $f_T/f_{max}$ (IHP SG13G2) | 300/500 GHz [2] | as of Feb 2026 |

### [10-08 · Current Sources and Current Mirrors](../courses/10-electronics-1/chapters/10-08-current-sources-and-mirrors.md)

| Quantity | Typical value | Note |
|---|---|---|
| Basic MOS mirror error | $\lambda\Delta V_{DS}$: several percent per volt at short L | |
| Basic mirror $R_{out}$ | $r_o$ | |
| Cascode mirror $R_{out}$ | about $g_mr_o^2$, tens of times $r_o$ | |
| Compliance | $V_{ov}$ (basic), $V_{TN} + 2V_{ov}$ (cascode), $2V_{ov}$ (low-voltage cascode) | |
| Bipolar base-current error | $2/\beta$ (basic), $2/\beta^2$ (helper, Wilson) | |
| Mismatch | $\sigma(\Delta I/I) = (2/V_{ov})A_{VT}/\sqrt{WL}$ | Pelgrom [1] |
| Resistor-referenced bias | supply sensitivity about $1/(V_{DD} - V_{GS})$ per volt | |

### [10-09 · Real Op-Amps: Non-Idealities](../courses/10-electronics-1/chapters/10-09-real-op-amps-nonidealities.md)

| Quantity | Typical value | Note |
|---|---|---|
| Gain error | noise gain / $A_{OL}$ | |
| Closed-loop bandwidth | GBW / noise gain | single pole |
| Full-power bandwidth | SR / (2π $V_p$) | |
| 1% and 0.1% in-band | below 0.14 and 0.045 of $f_{-3dB}$ | |
| General-purpose CMOS RRIO (TLV9062) | 10 MHz, 6.5 V/µs, 1.6 mV max, 0.5 pA, 538 µA [1] | data sheet, Rev. N 2026 |
| Zero-drift CMOS (OPA333) | 350 kHz, 0.16 V/µs, 10 µV max, 0.05 µV/°C max, 17 µA [2] | data sheet, Rev. E 2015 |
| Low-noise bipolar (OPA1611) | 40 MHz (G = 1), 27 V/µs, 500 µV max, 1.1 nV/√Hz, 3.6 mA [3] | data sheet, Rev. C 2014 |

### [10-10 · Op-Amp Application Circuits](../courses/10-electronics-1/chapters/10-10-op-amp-application-circuits.md)

| Quantity | Value | Note |
|---|---|---|
| Difference-amp CMRR | $(1 + K)/(4\varepsilon)$ worst case: 54 dB for $K$ = 1, 0.1% | |
| INA CMRR | multiplied by the first-stage gain; integrated parts trimmed to 100 dB class [1] | |
| Lossy integrator corner | $1/(2\pi RCA_0)$ | |
| Rectifier dead time | $2V_D/\text{SR}$ | |
| Schmitt hysteresis | $V_{DD}R_1/R_2$ | non-inverting form |
| TIA natural frequency | $\sqrt{\text{GBW}/(2\pi R_FC_{in})}$ | |
| TIA Q without $C_F$ | $\sqrt{2\pi\,\text{GBW}\,R_FC_{in}}$ | |
| Fast low-power comparator | about 50 ns at 40 µA (TLV3201) [2] | data sheet, May 2024 |

## [11 · Signals and Systems](../courses/11-signals-and-systems/README.md)

### [11-01 · Signals: Classification and Operations](../courses/11-signals-and-systems/chapters/11-01-signals-classification-and-operations.md)

| Quantity | Value | Note |
|---|---|---|
| Sinusoid RMS | $A/\sqrt2 \approx 0.7071A$; power $A^2/2$ | DT exception at $\omega = 0, \pi$ |
| Complex exponential power | $\lvert C\rvert^2$ | Constant magnitude |
| Energy of $Ae^{-at}u(t)$ | $A^2/2a$ | DT: $A^2/(1 - r^2)$ for $Ar^nu[n]$ |
| Energy under time scaling $x(at)$ | $E/\lvert a\rvert$ | Shifts and reversals preserve energy |
| $\delta(at)$ | $\delta(t)/\lvert a\rvert$ | δ(t) has units of 1/s |
| Highest DT frequency | $\omega = \pi$ rad/sample, i.e. $f_s/2$ | $(-1)^n$ |
| Mains frequencies | 50 Hz and 60 Hz | ECG and audio interferers |
| Audio sampling | 48 kHz (codec test condition [2]); 44.1 kHz for CD audio | As of Nov 2026 |
| ECG AFE data rates | 125 SPS to 8 kSPS, 24-bit (ADS1292R) [1] | As of Nov 2026 |
| PCIe 6.0 | 64 GT/s with PAM4, 2 bits per symbol [3, 4] | As of Nov 2026 |

### [11-02 · Systems and Their Properties](../courses/11-signals-and-systems/chapters/11-02-system-properties.md)

| Quantity | Value | Note |
|---|---|---|
| Distortion in dB | 10% = −20 dB, 1% = −40 dB, 0.1% = −60 dB | $20\log_{10}$ of the amplitude ratio |
| HD2, HD3 from a polynomial | $a_2A/(2a_1)$, $a_3A^2/(4a_1)$ | +20 and +40 dB per decade of amplitude |
| IM2, IM3 amplitudes | $a_2A_1A_2$; $\tfrac34a_3A_1^2A_2$ | IM3 falls at $2f_1 - f_2$, next to the signals |
| Bound of $y[n] = a\,y[n-1] + x[n]$ | $B/(1 - \lvert a\rvert)$ | Stable only for $\lvert a\rvert < 1$ |
| Linear-phase FIR latency | $(N - 1)/2$ samples | 50 samples (1.042 ms) for 101 taps at 48 kHz |
| Bipolar HD2 | about $A/(4V_T)$: 1% at about 1 mV | Problem 11-02.6 |
| OPA1611 THD+N, 1 kHz | 0.000015% (−136.5 dB) [1] | As of Nov 2026 |
| Audio codec ADC THD+N | −85 dB typ, −70 dB max (TLV320AIC3204) [2] | As of Nov 2026 |

### [11-03 · Convolution](../courses/11-signals-and-systems/chapters/11-03-convolution.md)

| Quantity | Value | Note |
|---|---|---|
| Output length | $L_x + L_h - 1$ | Supports add |
| Area (DC gain) | $\sum y = \sum x\sum h$ | Fastest check |
| Worst-case gain | $\sum\lvert h\rvert$ | Stability and overflow |
| FIR cost | $M$ MACs per output sample | $Mf_s$ MAC/s per channel |
| Conv-layer cost | $HWC_{in}C_{out}k^2$ MACs | 115.6 M for 3 × 3, 64 → 64, 56 × 56 |
| One RC stage, 10–90% rise | $\tau\ln9 \approx 2.2\tau$ | Two buffered stages: about $3.36\tau$ |
| ADS1292R sinc³ filter at 500 SPS | 766 taps at 128 kHz, about 6 ms | As of Nov 2026 [4] |
| TPU v1 MAC array | 65,536 8-bit MACs at 700 MHz, 92 TOPS peak [2] | 2017 paper |

### [11-04 · LTI Systems and Differential/Difference Equations](../courses/11-signals-and-systems/chapters/11-04-lti-systems-and-differential-equations.md)

| Quantity | Value | Note |
|---|---|---|
| DT stability | All characteristic roots inside the unit circle | CT: all in the left half-plane |
| First-order DT impulse response | $a^nu[n]$ | Root $a$ |
| Second-order resonator | $h[n] = r^n\sin((n+1)\theta)/\sin\theta$ | Ringing period $2\pi/\theta$ samples |
| First-order CT impulse response | $\frac1\tau e^{-t/\tau}u(t)$ | Jumps to $1/\tau$ |
| Series RLC (capacitor) impulse response | $(\omega_0^2/\omega_d)e^{-\alpha t}\sin\omega_dt$ | Slope jumps by $\omega_0^2$ |
| Biquad cost | 5 MACs; 4 delays (DF-I) or 2 (DF-II) | CMSIS-DSP DF-I: 5 coefficients, 4 states per stage [2] |
| Eigenvalue | $H(z) = \sum h[k]z^{-k}$; $H(s) = \int h(\tau)e^{-s\tau}d\tau$ | Rational: $B/A$ from the equation |

### [11-05 · Fourier Series](../courses/11-signals-and-systems/chapters/11-05-fourier-series.md)

| Quantity | Value | Note |
|---|---|---|
| Square wave (±A) | $A_k = 4A/(\pi k)$, odd $k$; fundamental $1.27A$ | Fundamental holds $8/\pi^2 \approx 81\%$ of the power; THD ≈ 48% |
| Triangle (±A) | $A_k = 8A/(\pi^2k^2)$, odd $k$ | 3rd harmonic −19.1 dB |
| Pulse train | $c_k = AD\operatorname{sinc}(kD)e^{-j\pi kD}$ | Zeros at $k = 1/D, 2/D, \dots$ |
| Full-wave rectified sine | DC $0.637V_p$; first ripple term $0.424V_p$ at $2f$ | Ripple falls as $1/m^2$ |
| Gibbs overshoot | 1.179 for a ±1 jump (8.95% of the jump) | Does not shrink with $N$ |
| Decay rate | Jump: $1/k$; kink: $1/k^2$ | Smoother is narrower |
| Class-D switching frequencies (TPA3116D2) | 400 kHz to 1.2 MHz, pin-selectable [1] | As of Nov 2026 |

### [11-06 · The Continuous-Time Fourier Transform](../courses/11-signals-and-systems/chapters/11-06-continuous-time-fourier-transform.md)

| Quantity | Value | Note |
|---|---|---|
| $e^{-at}u(t)$ | $1/(a + j\omega)$; −3 dB at ω = a | 99% of energy within 63.7a |
| Rectangular pulse, width $T$ | $T\operatorname{sinc}(fT)$; first null $1/T$ | 90.3% of energy inside the first null; 77.4% inside $1/(2T)$ |
| Gaussian, width σ | $\sigma\sqrt{2\pi}e^{-\sigma^2\omega^2/2}$ | Minimum time–bandwidth product |
| Ideal low-pass step response | Overshoot 1.0895 | Gibbs |
| Rise time and bandwidth | $t_r \approx 0.35/f_{3dB}$ | 0.350 single pole, 0.340 Gaussian |
| Cascade rise time | $\sqrt{\sum t_{r,i}^2}$ | Exact for Gaussians |
| PCIe 5.0/6.0 Nyquist | 16 GHz; 6.0 channel loss < 32 dB there | As of Nov 2026 [2, 3] |
| ADS1292R bandwidth | $0.262f_{DR}$ = 131 Hz at 500 SPS | From sinc³ [1] |

### [11-07 · The Discrete-Time Fourier Transform](../courses/11-signals-and-systems/chapters/11-07-discrete-time-fourier-transform.md)

| Quantity | Value | Note |
|---|---|---|
| DT frequency | $\omega = 2\pi f/f_s$; π is $f_s/2$ | Spectrum periodic in 2π |
| $a^nu[n]$ | $1/(1 - ae^{-j\omega})$ | DC gain $1/(1 - a)$ |
| $L$-point boxcar | Dirichlet kernel; nulls at $2\pi k/L$ | Main lobe $4\pi/L$ wide |
| Ideal DT low-pass | $h[n] = \sin(\omega_cn)/(\pi n)$ | Truncation → Gibbs ripple |
| Symmetric FIR of $N$ taps | Group delay $(N - 1)/2$ samples | Exactly linear phase |
| Window trade | Rectangular: about 27 dB stopband (21 taps); Hamming: about 50 dB | Hamming's transition about twice as wide |
| Resolution | $\Delta f \approx 1/T_{obs} = f_s/N$ | Zero-padding does not help |

### [11-08 · The Laplace Transform and System Functions](../courses/11-signals-and-systems/chapters/11-08-laplace-transform-and-system-functions.md)

| Quantity | Value | Note |
|---|---|---|
| $e^{-at}u(t)$ | $1/(s + a)$, ROC right of $-a$ | The left-sided version has the same formula, ROC to the left |
| Causal and stable | All poles with $\operatorname{Re} < 0$ | ROC contains the $j\omega$ axis |
| Second-order poles | Radius ω₀; ζ = cos θ from the negative real axis | $Q = 1/(2\zeta)$ |
| Resonance bandwidth | $2\alpha = \omega_0/Q$ | Exact for the band-pass form; approximate peak location for $Q \gg 1$ |
| Gain at ω₀ (all-pole second order) | Q, at −90° | Any damping |
| Butterworth | $1/\sqrt{1 + (\omega/\omega_c)^{2n}}$; poles on a circle | n = 2: ζ = 0.7071 |
| First-order all-pass | $(a - s)/(a + s)$; delay $2/a$ at DC | Magnitude 1 everywhere |
| 802.3ck reference CTLE | Zero at $Gf_z$; poles 21.25 and 53.125 GHz; $g_{DC}$ −20 to 0 dB | As of the draft 3.1 configuration (Nov 2021) [1] |

### [11-09 · The z-Transform](../courses/11-signals-and-systems/chapters/11-09-z-transform.md)

| Quantity | Value | Note |
|---|---|---|
| $a^nu[n]$ | $1/(1 - az^{-1})$, ROC $\lvert z\rvert > \lvert a\rvert$ | Left-sided twin: same formula, inside |
| Causal and stable | All poles with $\lvert p\rvert < 1$ | ROC contains the unit circle |
| Biquad stability | $\lvert a_2\rvert < 1$, $\lvert a_1\rvert < 1 + a_2$ | For $1 + a_1z^{-1} + a_2z^{-2}$ |
| Pole near the circle | Bandwidth ≈ $2(1 - r)$ rad/sample; time constant ≈ $1/(1 - r)$ samples | Same fact twice |
| Sampling map | $z = e^{sT}$; radius $e^{-\alpha T}$, angle $\omega_dT$ | Left half-plane → inside the disk |
| Bilinear warping | $\Omega = (2/T)\tan(\omega/2)$ | Negligible when $\Omega T \ll 1$ |
| Boxcar of $L$ samples | Zeros at $e^{j2\pi k/L}$, $k \ne 0$ | The Dirichlet nulls |

### [11-10 · Sampling, Aliasing and Reconstruction](../courses/11-signals-and-systems/chapters/11-10-sampling-aliasing-reconstruction.md)

| Quantity | Value | Note |
|---|---|---|
| Sampling theorem | $f_s > 2f_M$ | Strict inequality |
| Alias of $f_0$ | $\lvert f_0 - kf_s\rvert \le f_s/2$ | Phase flips when folded from a reversed zone |
| First alias onto the band edge | $f_s - f_B$ | Sets the anti-aliasing requirement |
| Zero-order hold | $\operatorname{sinc}(f/f_s)$; −3.92 dB at $f_s/2$; delay $T/2$ | Images at $kf_s \pm f$ |
| Ideal ADC SNR | $6.02N + 1.76$ dB | Full-scale sine, uniform error |
| Oversampling gain | $10\log_{10}(\text{OSR})$ dB | Without noise shaping |
| Jitter-limited SNR | $-20\log_{10}(2\pi f_0\sigma_t)$ | 100 fs at 70 MHz: about 87 dB |
| Band-pass sampling | $2f_H/n \le f_s \le 2f_L/(n - 1)$ | Odd $n$ upright, even $n$ inverted |

### [11-11 · Modulation and Filtering Applications](../courses/11-signals-and-systems/chapters/11-11-modulation-and-filtering-applications.md)

| Quantity | Value | Note |
|---|---|---|
| DSB-SC bandwidth | $2W$ | Two sidebands |
| Coherent demodulation | Output ∝ cos φ | Lost at 90° |
| AM efficiency | $m^2P_x/(1 + m^2P_x)$; 1/3 for a tone at m = 1 | Carrier carries no information |
| Envelope detector | $1/f_c \ll RC \le \sqrt{1 - m^2}/(m\omega_m)$ | Diagonal clipping above |
| Image frequency | $f_{RF} + 2f_{IF}$ (high-side LO) | Must be filtered before the mixer |
| Shannon capacity | $B\log_2(1 + \text{SNR})$ | ≈ 1 bit/s/Hz per 3 dB at high SNR |

## [12 · Electronics II](../courses/12-electronics-2/README.md)

### [12-01 · Differential Pairs](../courses/12-electronics-2/chapters/12-01-differential-pairs.md)

| Quantity | Value | Note |
|---|---|---|
| BJT pair linear range | ≈ ±9 mV for 1% linearity; switched by ≈ ±4V_T | tanh(v_id/2V_T) |
| MOS pair full switching | $\sqrt2V_{ov}$ | Linear range scales with $V_{ov}$ |
| Differential gain | $g_mR_D$ (differential output) | Half-circuit |
| Single-ended CMRR | ≈ $g_mR_{SS}$ | Set by the tail |
| Differential CMRR with mismatch | ≈ $(R_D/\Delta R_D)(1 + 2g_mR_{SS})$ | Set by matching |
| MOS offset | $\Delta V_{TN} + (V_{ov}/2)(\Delta R/R + \Delta k/k)$ | Magnitudes; signs vary |
| BJT offset | $V_T(\Delta R/R + \Delta I_S/I_S)$; drift $V_{OS}/T$ | 3.3 µV/K per mV at 300 K |
| Pelgrom | σ(ΔV_TN) = A_VT/√(WL) | 4× area for half the offset |

### [12-02 · Active Loads, Cascodes and Multistage Amplifiers](../courses/12-electronics-2/chapters/12-02-active-loads-cascodes-multistage.md)

| Quantity | Value | Note |
|---|---|---|
| Resistor-load CS gain | $2V_{RD}/V_{ov}$: single digits at 1.8 V | Independent of current |
| Active-load CS gain | $g_mr_o/2 = 1/(\lambda V_{ov})$ | Tens in short-channel processes |
| Cascode output resistance | $\approx g_mr_o^2$ | ×$g_mr_o$ over one device |
| Cascode open-circuit gain | $g_{m1}r_{o1}(1 + g_{m2}r_{o2}) \approx (g_mr_o)^2$ | Halved by a matching cascode load |
| Five-transistor OTA | $A_d = g_m(r_{o2} \parallel r_{o4})$; $A_{cm} \approx 1/(2g_{m3}R_{SS})$ | Single-ended output |
| Telescopic swing per side | $V_{DD} - 5V_{ov}$ | Five stacked overdrives |
| Two-stage gain | $\approx (g_mr_o)^2/4$ | Second pole needs compensation |
| Input-referred offset | $V_{OS1} + V_{OS2}/A_1 + \cdots$ | First stage dominates |

### [12-03 · Frequency Response: Device Capacitances, Miller Effect, Poles and Zeros](../courses/12-electronics-2/chapters/12-03-frequency-response-miller-poles-zeros.md)

| Quantity | Value | Note |
|---|---|---|
| $C_{gs}$ in saturation | $\tfrac23WLC_{ox} + WC_{ov}$ | 09-09 |
| $C_{gd}$ | $WC_{ov}$ (overlap only) | Multiplied by Miller |
| $f_T$ | $g_m/[2\pi(C_{gs} + C_{gd})]$ | Device, output shorted |
| Bipolar $C_\pi$ | $\tau_Fg_m + C_{je}$ | Grows with current |
| Miller capacitance | $C(1 + A_v)$ | At the input of an inverting gain |
| CS dominant pole | $1/b_1$, $b_1 = R_S[C_{gs} + C_{gd}(1 + g_mR_L)] + R_L(C_{gd} + C_L)$ | Errs low if poles are close |
| CS right-half-plane zero | $g_m/C_{gd}$ | Phase lag without gain loss |
| Single-stage gain–bandwidth | ≈ $g_m/[2\pi(C_L + C_{gd})]$ | Output-limited case |
| SiGe HBT $f_T/f_{max}$ | 300/500 GHz (IHP SG13G2) [2] | As of Feb 2026 |

### [12-04 · High-Frequency Analysis Methods](../courses/12-electronics-2/chapters/12-04-high-frequency-analysis-methods.md)

| Quantity | Value | Note |
|---|---|---|
| OCTC bandwidth | $1/\sum R_{i0}C_i$ | Exact $b_1$; a lower bound if every pole is real |
| Bridging-capacitor resistance (CS) | $R_S + R_L + g_mR_SR_L$ | Miller without a gain assumption |
| Second pole | $\approx b_1/b_2$ | $b_2$ from zero-value pairs |
| SCTC low corner | $\sum 1/(R_{is}C_i)$ | Exact sum of low poles; an upper bound if they are real |
| Split poles | $1/(g_{m2}R_1R_2C_c)$ and $\approx g_{m2}/(C_1 + C_2)$ | $C_c \gg C_1$ |
| Follower Q | $\sqrt{g_mR_S\Sigma}/(C_{gs} + C_L + g_mR_SC_{gd})$ | Peaks above about $1/\sqrt2$ |

### [12-05 · Feedback: Theory and the Four Topologies](../courses/12-electronics-2/chapters/12-05-feedback-topologies.md)

| Quantity | Value | Note |
|---|---|---|
| Closed-loop gain | $A/(1 + T) = (1/\beta)\,T/(1 + T)$ | Error ≈ $1/T$ |
| Sensitivity | $dA_f/A_f = (dA/A)/(1 + T)$ | β not desensitized |
| Single-pole bandwidth | $\omega_p(1 + T_0)$; GBW constant | |
| Impedances | ×$(1 + T)$ for series, ÷$(1 + T)$ for shunt | Input mixing and output sampling |
| Asymptotic gain | $A_f = A_\infty T/(1 + T) + A_{\mathrm{dir}}/(1 + T)$ | No A/β split needed |
| Blackman | $Z = Z^{(0)}(1 + T_{sc})/(1 + T_{oc})$ | Any port |

### [12-06 · Stability and Frequency Compensation](../courses/12-electronics-2/chapters/12-06-stability-and-compensation.md)

| Quantity | Value | Note |
|---|---|---|
| Phase margin | $180^\circ + \angle T(j\omega_c)$ | Target 45°–70° |
| Gain margin | $-20\log\lvert T(j\omega_{180})\rvert$ | Target ≥ 10 dB |
| Two-pole loop | $Q = \sqrt{f_u/f_2}$ | 60° at $f_2 = 1.5f_u$ |
| 60° phase margin | 8.8% overshoot, 0.28 dB peaking | 45°: about 23% overshoot |
| Miller GBW | $g_{m1}/(2\pi C_c)$ | Independent of output resistances |
| Non-dominant pole | $\approx g_{m2}/C_L$ | Falls with load capacitance |
| RHP zero | $g_{m2}/C_c$ | Push it beyond 10× GBW |
| Rules of thumb | $g_{m2} \approx 10g_{m1}$, $C_c \approx 0.22C_L$ | About 60° |
| Nulling resistor | $1/g_{m2}$ removes the zero; $(1 + C_L/C_c)/g_{m2}$ cancels $p_2$ | New pole near $1/(R_zC_1)$ |

### [12-07 · Output Stages and Power Amplifiers](../courses/12-electronics-2/chapters/12-07-output-stages.md)

| Quantity | Value | Note |
|---|---|---|
| Class A efficiency | ≤ 25% (resistive load) | Worst at idle |
| Class B efficiency | $(\pi/4)V_{op}/V_{CC}$, ≤ 78.54% | Linear in amplitude |
| Class B worst dissipation | $2V_{CC}^2/(\pi^2R_L)$ at $V_{op} = 2V_{CC}/\pi$ | 50% efficiency there |
| Crossover dead band | about ±0.6 V for bipolar stages | Fixed by class AB bias |
| Class AB translinear | $i_Ni_P = I_Q^2$ | Output resistance $V_T/(2I_Q)$ at idle |
| $V_{BE}$ multiplier | $V_{BB} = V_{BE}(1 + R_1/R_2)$ | Tracks −2 mV/°C × $(1 + R_1/R_2)$ |
| Junction temperature | $T_J = T_A + P_D\sum\theta$ | $T_{J,max}$ ≈ 150 °C for silicon |
| Class D efficiency | > 90% at high output | Fixed losses dominate at low output |
| Class D audio switching | hundreds of kHz | e.g. 450 kHz in the TPA3255 [1] |

### [12-08 · Op-Amp Internals](../courses/12-electronics-2/chapters/12-08-op-amp-internals.md)

| Quantity | Value | Note |
|---|---|---|
| Two-stage gain | $g_{m1}R_1 \cdot g_{m6}R_2$ | each about $1/(\lambda V_{ov})$, $10^3$–$10^4$ total |
| GBW (two-stage) | $g_{m1}/(2\pi C_c)$ | GBW (folded cascode) $g_{m1}/(2\pi C_L)$ |
| Slew rate | $I_{SS}/C_c$; falling also ≤ $(I_7 - I_{SS})/C_L$ | NMOS pair, PMOS M6; the edge on which M6 cuts off |
| SR/ω_u | $V_{ov1}$ (MOS), $2V_T$ ≈ 52 mV (bipolar) | MOS slews faster per GBW |
| Full-power bandwidth | $\text{SR}/(2\pi V_p)$ | Amplitude-dependent |
| CM error without CMFB | $\Delta I\cdot R_{out}$ | Divided by $1 + g_{m,cm}R_{out}$ with CMFB |
| Rail-to-rail $g_m$ seam | 2× in the overlap | Constant-$g_m$ halves each pair's $g_m$ there |

### [12-09 · Oscillators](../courses/12-electronics-2/chapters/12-09-oscillators.md)

| Quantity | Value | Note |
|---|---|---|
| Barkhausen | $L(j\omega_0) = 1$ | Start with 1.2–3× gain |
| Wien bridge | $\omega_0 = 1/(RC)$, gain 3 | Low distortion with AGC |
| RC phase shift (3 sections) | $\omega_0 = \sqrt6/(RC)$, gain 29 | Inverting |
| Colpitts | $\omega_0^2 = (C_1 + C_2)/(LC_1C_2)$, $g_mR \ge C_2/C_1$ | Exact boundary |
| Cross-coupled pair | $-2/g_m$; start if $g_m > 2/R_p$ | $R_p = Q\omega_0L$ |
| Crystal | $Q$ ≈ $10^4$–$10^6$; $f_p = f_s\sqrt{1 + C_m/C_0}$ | Pulls by ppm with $C_L$ |
| Ring oscillator | $f = 1/(2Nt_{pd})$ | Three stages need gain 2 |
| Watch crystal | 32.768 kHz = 2¹⁵ Hz | Divides to 1 Hz in 15 flip-flops |

### [12-10 · Noise in Circuits](../courses/12-electronics-2/chapters/12-10-noise-in-circuits.md)

| Quantity | Value | Note |
|---|---|---|
| Thermal noise | $4kTR$; 1 kΩ ≈ 4.07 nV/√Hz at 300 K | 50 Ω ≈ 0.91 nV/√Hz |
| Shot noise | $2qI$; 1 mA ≈ 17.9 pA/√Hz | |
| kT/C | 64.4 µV at 1 pF (300 K) | ∝ $1/\sqrt C$ |
| MOSFET input noise | $4kT\gamma/g_m$, γ ≈ 2/3 long-channel | Plus 1/f |
| BJT input noise | $2kT/g_m$ | $R_{eq} = 1/(2g_m)$ |
| Flicker integration | $S_wf_c\ln(f_2/f_1)$ | Each decade the same |
| Noise figure | $F = 1 + (e_n^2 + i_n^2R_s^2)/(4kTR_s)$ | $R_{opt} = e_n/i_n$ |

## [13 · Electromagnetics](../courses/13-electromagnetics/README.md)

### [13-01 · Vector Calculus Refresher](../courses/13-electromagnetics/chapters/13-01-vector-calculus-refresher.md)

| Quantity | Value | Note |
|---|---|---|
| Scale factors | cylindrical $(1, \rho, 1)$; spherical $(1, r, r\sin\theta)$ | Distances per coordinate step |
| Sphere | area $4\pi r^2$, volume $\tfrac43\pi r^3$ | $\int\sin\theta\,d\theta\,d\phi = 4\pi$ |
| Source-free radial fields | $1/r^2$ (spherical), $1/\rho$ (cylindrical) | Point and line charges |
| Curl-free azimuthal field | $1/\rho$ | Field outside a wire |
| Laplace radial solutions | $a + b/r$, $a + b\ln\rho$ | Point and line charge potentials |
| $\nabla^2(1/r)$ | $-4\pi\delta^3(\vec{r})$ | Point source |

### [13-02 · Electrostatics: Boundary Conditions and Boundary-Value Problems](../courses/13-electromagnetics/chapters/13-02-electrostatics-boundary-value-problems.md)

| Quantity | Value | Note |
|---|---|---|
| $\varepsilon_0$ | 8.854 pF/m | Measured (since the 2019 SI revision) to about ten significant figures |
| SiO₂ relative permittivity | 3.9 | The reference for equivalent oxide thickness |
| Air breakdown | ≈ 3 MV/m | Centimetre gaps at sea level; lower for long gaps, higher for tiny ones |
| Coaxial cable, 50 Ω class | ≈ 100 pF/m | Belden 8262 (RG-58 type) specifies 101 pF/m [2] |
| FR-4 class laminate Dk | ≈ 4 (falls with frequency) | 370HR: 4.17 at 1 GHz, 3.92 at 10 GHz [1] |
| Laplace's equation | Each point the average of its neighbours | No interior maxima or minima |

### [13-03 · Magnetostatics and Inductance](../courses/13-electromagnetics/chapters/13-03-magnetostatics-and-inductance.md)

| Quantity | Value | Note |
|---|---|---|
| $\mu_0$ | 1.2566 µH/m (≈ 4π × 10⁻⁷ H/m) | Measured since the 2019 SI revision |
| Field 1 cm from 10 A | 200 µT | About four times the Earth's field |
| Internal inductance of a round wire (DC) | 50 nH/m | $\mu_0/8\pi$, independent of radius |
| Bond wire | ≈ 1 nH/mm | Rule of thumb [1]; grows logarithmically with length |
| Coaxial and other TEM lines | $L'C' = \mu\varepsilon$ | One determines the other |
| Air gap reluctance | $\mu_r$ times the same length of core | Gaps dominate magnetic circuits |

### [13-04 · Maxwell's Equations and Time-Varying Fields](../courses/13-electromagnetics/chapters/13-04-maxwells-equations.md)

| Quantity | Value | Note |
|---|---|---|
| Speed of light | 299,792,458 m/s | Defined; $1/\sqrt{\mu_0\varepsilon_0}$ |
| Impedance of free space | 376.7 Ω | $\sqrt{\mu_0/\varepsilon_0}$, ≈ 120π |
| Copper conductivity | 5.8 × 10⁷ S/m | $\sigma/\omega\varepsilon_0 \approx 10^9$ at 1 GHz |
| Seawater crossover | ≈ 900 MHz | $\sigma$ ≈ 4 S/m, $\varepsilon_r$ ≈ 81 |
| Lumped-circuit limit | about λ/10 | 1.5 cm at 1 GHz on FR-4-like board |
| FCC general-population power-density limit | 1 mW/cm² (10 W/m²) above 1.5 GHz | As of Nov 2026 [1] |
| Peak spatial SAR limits | 1.6 W/kg over 1 g (FCC); 2 W/kg over 10 g (ICNIRP 2020) | As of Nov 2026 [1], [2] |

### [13-05 · Plane Waves in Lossless and Lossy Media](../courses/13-electromagnetics/chapters/13-05-plane-waves.md)

| Quantity | Value | Note |
|---|---|---|
| Impedance of free space | 376.7 Ω | ≈ 120π; $\eta_0/\sqrt{\varepsilon_r}$ in a dielectric |
| Copper conductivity (100% IACS, 20 °C) | 5.8 × 10⁷ S/m | 1.7241 µΩ·cm [1] |
| Copper skin depth | 8.5 mm at 60 Hz; 66 µm at 1 MHz; 2.1 µm at 1 GHz | $\propto 1/\sqrt f$ |
| Copper surface resistance | 8.25 mΩ at 1 GHz | $\propto\sqrt f$ |
| 1 neper | 8.686 dB | Field falls by $e$ |
| Dielectric loss, FR-4-like at 10 GHz | about 0.36 dB/cm (tan δ = 0.02) to **0.45** dB/cm (370HR data sheet) | $\propto f$ at constant $\tan\delta$ |
| Linear antenna on a circular wave | −3 dB | Any orientation |

### [13-06 · Reflection and Transmission of Waves](../courses/13-electromagnetics/chapters/13-06-reflection-and-transmission.md)

| Quantity | Value | Note |
|---|---|---|
| Uncoated glass reflection | 4% per surface | $n$ = 1.5 |
| Glass-to-air critical angle | 41.8° | $\arcsin(1/1.5)$ |
| Air-to-glass Brewster angle | 56.3° | $\arctan 1.5$ |
| Perfect conductor | Γ = −1 | Field zero at the surface; maxima at λ/4 |
| Single-mode fibre attenuation (G.652.D cable, 1530–1565 nm) | ≤ 0.30 dB/km | As of Nov 2026 [1] |
| Solid copper foil at 1 GHz | > 200 dB shielding | Openings dominate in practice |

### [13-07 · Transmission Lines: Time Domain](../courses/13-electromagnetics/chapters/13-07-transmission-lines-time-domain.md)

| Quantity | Value | Note |
|---|---|---|
| Coax (solid PE) delay | about 5 ns/m | $v \approx 2c/3$ |
| Board stripline delay ($\varepsilon_r$ ≈ 4) | about 6.7 ps/mm | 170 ps per inch |
| Reflection from an open / short / match | +1 / −1 / 0 | Voltage reflection coefficient |
| Critical length guideline | delay > rise time / 6 | A rule of thumb; 2.5 mm at 100 ps on FR-4-like board |
| USB 2.0 cable | 90 Ω ±15% differential | As of Nov 2026 [1] |
| PCIe Gen 3/4 board traces | 85 Ω ±5% differential | Vendor guidance, as of Nov 2026 [2] |

### [13-08 · Transmission Lines: Sinusoidal Steady State](../courses/13-electromagnetics/chapters/13-08-transmission-lines-sinusoidal-steady-state.md)

| Quantity | Value | Note |
|---|---|---|
| λ/4 line | $Z_{in} = Z_0^2/Z_L$ | Inverts; open ↔ short |
| λ/2 line | $Z_{in} = Z_L$ | Repeats |
| VSWR 1.5 | Γ = 0.2, RL 14.0 dB, ML 0.18 dB | Common component spec |
| VSWR 2 | Γ = 1/3, RL 9.5 dB, ML 0.51 dB | Common antenna spec |
| Loss masking | RL improves by 2 dB per dB of line loss | Measure at the device |
| RG-58 at 1 GHz | 0.71 dB/m | 21.5 dB/100 ft, as of Nov 2026 [1] |

### [13-09 · The Smith Chart and Impedance Matching](../courses/13-electromagnetics/chapters/13-09-smith-chart-and-matching.md)

| Quantity | Value | Note |
|---|---|---|
| Chart centre | Γ = 0, $z$ = 1 | Perfect match |
| One full turn | λ/2 of line | Clockwise toward the generator |
| Admittance | Rotate 180° | $y$ = $z$ with Γ → −Γ |
| L-network Q | $\sqrt{R_{high}/R_{low} - 1}$ | 2 for a 5:1 step |
| Bode–Fano (parallel RC) | $\Delta f \le 1/[2RC\ln(1/\Gamma_m)]$ | 4.3 GHz at 20 dB for 50 Ω ∥ 1 pF |
| 50 Ω | Between 30 Ω (max power) and 77 Ω (min loss) for air coax | Derived in §9 |

### [13-10 · Waveguides and Resonators](../courses/13-electromagnetics/chapters/13-10-waveguides-and-resonators.md)

| Quantity | Value | Note |
|---|---|---|
| TE₁₀ cutoff | $c/2a$ | 6.557 GHz for WR-90 (a = 22.86 mm) |
| Phase × group velocity | $c^2$ | Phase faster, group slower than light |
| Below cutoff | ≈ 27 dB per guide width | $\alpha \approx \pi/a$ |
| Copper X-band waveguide loss | ≈ 0.1 dB/m | Against ≈ 1 dB/m for small coax |
| Copper X-band cavity Q | several thousand | $Q \sim$ volume/(area × δ) |
| Single-mode condition | V < 2.405 | First zero of $J_0$ |
| Standard single-mode fibre MFD (1310 nm) | 8.6–9.2 µm nominal | G.652.D, as of Nov 2026 [2] |

### [13-11 · Radiation and Antenna Fundamentals](../courses/13-electromagnetics/chapters/13-11-radiation-and-antennas.md)

| Quantity | Value | Note |
|---|---|---|
| Hertzian dipole | D = 1.5 (1.76 dBi); $R_{rad} \approx 789(\ell/\lambda)^2$ Ω | Doughnut pattern, HPBW 90° |
| Half-wave dipole | D = 1.64 (2.15 dBi); $R_{rad}$ ≈ 73 Ω | HPBW 78° |
| Effective aperture | $G\lambda^2/4\pi$ | 20 cm² for a dipole at 2.4 GHz |
| Free-space path loss | $20\log_{10}(4\pi R/\lambda)$ | 80 dB for 100 m at 2.4 GHz |
| Array gain | +3 dB per doubling of elements | At about λ/2 spacing |
| Far-field distance | $2D_a^2/\lambda$ | 80 m for a 1 m dish at 12 GHz |
| 6 GHz indoor Wi-Fi limit (US) | 30 dBm EIRP, 5 dBm/MHz | As of Nov 2026 [2] |

## [14 · Computer Organization and Architecture](../courses/14-computer-organization-and-architecture/README.md)

### [14-01 · Performance, Power and the Iron Law](../courses/14-computer-organization-and-architecture/chapters/14-01-performance-power-iron-law.md)

| Quantity | Value | Note |
|---|---|---|
| Iron law | $T = \text{IC} \times \text{CPI}/f$ | §3.2 |
| Amdahl ceiling | $1/(1 - p)$ | 90% parallel → 10× at most |
| Dynamic power | $\alpha CV^2f$, energy $\alpha CV^2$ per cycle | 07-02, 09-11 |
| Power against frequency with DVFS | roughly $f^3$ near the top of the range | §3.5 |
| Subthreshold swing limit | about 60 mV/decade at 300 K | 09-10 |
| End of clock-rate scaling | about 2004, clocks around 5 GHz | IRDS [1] |
| Energy per operation, 45 nm at 0.9 V | 32-bit add 0.1 pJ; 32-bit FP multiply 3.7 pJ; 64-bit read from a 32 KB cache 20 pJ; DRAM access 1.3–2.6 nJ; about 70 pJ of overhead per instruction on a simple core | Horowitz, ISSCC 2014 [2]: one DRAM access costs as much energy as more than 10,000 32-bit additions, which is why data movement, not arithmetic, dominates energy |

### [14-02 · Instruction Set Architecture: RISC-V, Arm and x86](../courses/14-computer-organization-and-architecture/chapters/14-02-isa-risc-v-arm-x86.md)

| Quantity | Value | Note |
|---|---|---|
| RV32I instruction | 32 bits; opcode in bits 6–0; rd 11–7, rs1 19–15, rs2 24–20 | §3.3 |
| I/S immediate range | −2048 to +2047 | 12 bits |
| Branch reach | −4096 to +4094 bytes | 13-bit even offset |
| JAL reach | ±1 MiB | 21-bit even offset |
| x86-64 instruction length | 1 to 15 bytes | §3.6 |
| Compressed RISC-V saving | 44% on the array-sum loop | Example 14-02.5 |
| RISC-V NOP | 0x00000013 (`addi x0, x0, 0`) | canonical encoding |

### [14-03 · Assembly and the Compilation Stack](../courses/14-computer-organization-and-architecture/chapters/14-03-assembly-and-the-compilation-stack.md)

| Quantity | Value | Note |
|---|---|---|
| Argument registers (RISC-V) | 8 (a0–a7); a0–a1 also return values | psABI [2] |
| Callee-saved integer registers | 12 (s0–s11), plus sp | psABI [2] |
| Stack alignment at a call | 16 bytes | psABI [2] |
| ILP32 sizes | `char` 1, `short` 2, `int`/`long`/pointer 4, `long long`/`double` 8 | LP64: `long` and pointers 8 |
| Call before and after relaxation | AUIPC + JALR (8 bytes) → JAL (4 bytes), within ±1 MiB | [3] |
| Recursive `fib(n)`, hand-written | $21F(n+1) - 18$ instructions | Example 14-03.4 |

### [14-04 · Computer Arithmetic and Number Formats](../courses/14-computer-organization-and-architecture/chapters/14-04-computer-arithmetic-and-number-formats.md)

| Quantity | Value | Note |
|---|---|---|
| FP32 precision and unit roundoff | $p = 24$, $u = 2^{-24} \approx 5.96 \times 10^{-8}$ | §3.3 |
| Spacing of FP32 near $10^8$ | 8 | so $10^8 + 1 = 10^8$ |
| Sequential-sum error bound | $(n - 1)u\sum\lvert x \rvert$ | pairwise: $\lceil\log_2 n\rceil u$; Kahan: about $2u$ |
| RISC-V division by zero | quotient −1, remainder = dividend | no trap [1] |
| RISC-V canonical FP32 NaN | 0x7FC00000 | [2] |
| Magic number for unsigned ÷ 10 | 0xCCCCCCCD, then shift by 35 | Example 14-04.3 |
| INT8 × INT8 products before INT32 overflow | 133,144 | symmetric operands |
| MX block | 32 elements + one 8-bit power-of-two scale | 4.25 bits per FP4 element [4] |

### [14-05 · Single-Cycle Datapath and Control](../courses/14-computer-organization-and-architecture/chapters/14-05-single-cycle-datapath.md)

| Quantity | Value | Note |
|---|---|---|
| Single-cycle CPI | 1 | by construction |
| Longest path | the load: two memory accesses, register read, ALU, write-back | §3.4 |
| Example clock period | 730 ps (1.37 GHz) | illustrative delays, Example 14-05.3 |
| Typical single-cycle efficiency | 70–80% of an ideal variable cycle | Examples 14-05.4 and 14-05.6 |
| Register file ports for one instruction per cycle | 2 read, 1 write | §3.1 |
| Lab core | about 200 lines of Verilog; RV32I without byte/halfword memory access, FENCE or CSRs | lab |

### [14-06 · Pipelining and Hazards](../courses/14-computer-organization-and-architecture/chapters/14-06-pipelining-and-hazards.md)

| Quantity | Value | Note |
|---|---|---|
| Cycles for $N$ instructions on a $k$-stage pipeline | $N + (k - 1)$ + stalls + flush penalties | §3.5 |
| Load-use stall in the five-stage pipeline | 1 cycle | even with forwarding |
| Taken-branch penalty, resolved in EX | 2 cycles | 1 if resolved in ID |
| Forwarding paths into EX | 2 (from EX/MEM and MEM/WB) | plus register-file write-through |
| Example clock period | 285 ps (3.51 GHz) against 730 ps single-cycle | illustrative delays |
| Optimal depth (simple model) | $k^* = \sqrt{t_{\text{logic}}/(c\,t_{\text{reg}})}$ | §3.6 |

### [14-07 · Branch Prediction and Speculation](../courses/14-computer-organization-and-architecture/chapters/14-07-branch-prediction-and-speculation.md)

| Quantity | Value | Note |
|---|---|---|
| CPI cost of mispredictions | $b \times m \times P$ | §3.1 |
| Loop branch, 1-bit against 2-bit | 2 against 1 mispredictions per loop execution | Example 14-07.2 |
| Random-data branch | about 50% mispredicted, whatever the predictor | Example 14-07.6 |
| Five-stage penalty (resolved in EX) | 2 cycles | 14-06 |
| Example deep-pipeline penalty | 15 cycles | illustrative |
| Zen 5 front end | 16K-entry L1 BTB, 52-entry return stack | AMD, Hot Chips 2024 [4] |
| Spectre and Meltdown disclosure | reported 1 Jun 2017; public 3 Jan 2018 | [2] |

### [14-08 · Out-of-Order and Superscalar Execution](../courses/14-computer-organization-and-architecture/chapters/14-08-out-of-order-and-superscalar.md)

| Quantity | Value | Note |
|---|---|---|
| Name dependences | WAR and WAW, removed by renaming | §3.1 |
| Dataflow limit | IPC ≤ $N$ / critical path | §3.1 |
| Window needed to hide latency $L$ at width $w$ | about $w \times L$ entries | Little's law |
| Zen 5 | 8-wide dispatch and retire; 448-entry ROB; 240 integer physical registers; 6 ALUs | AMD, Hot Chips 2024 [1] |
| Pointer chasing | IPC ≈ instructions per node / load latency, whatever the width | Example 14-08.5 |

### [14-09 · Memory Hierarchy and Caches](../courses/14-computer-organization-and-architecture/chapters/14-09-memory-hierarchy-and-caches.md)

| Quantity | Value | Note |
|---|---|---|
| Energy per 64-bit read, 45 nm | 10 pJ (8 KB), 20 pJ (32 KB), 100 pJ (1 MB) cache; 1.3–2.6 nJ DRAM | Horowitz [1, R-208] |
| AMAT | $t_\text{hit} + m \, t_\text{penalty}$, nested for each level | §3.3 |
| Sets | $S = C/(B \cdot A)$ | §3.2 |
| Bandwidth from MLP | outstanding misses × $B$ / latency | Little's law |
| HBM3 / HBM3E / HBM4 per stack | 819 GB/s / above 1.2 TB/s / up to 2 TB/s | [2–4, R-214] |
| Zen 5 caches | L1 data 48 KB 12-way; L2 1 MB 16-way; L3 32 MB per 8-core complex | AMD, Hot Chips 2024 [5, R-212] |
| DRAM load latency | of order 100 ns: the round figure this chapter's examples use, not a sourced measurement | Illustrative; measure the target system (lab extension) |

### [14-10 · Virtual Memory, TLBs and the OS Interface](../courses/14-computer-organization-and-architecture/chapters/14-10-virtual-memory.md)

| Quantity | Value | Note |
|---|---|---|
| Base page | 4 KiB (offset 12 bits) | RISC-V [1, R-215]; also the usual base page on x86 and Arm systems |
| Sv32 | 2 levels, 4-byte PTEs, 4 MiB megapages | [1, R-215] |
| Sv39 / Sv48 / Sv57 | 3 / 4 / 5 levels, 8-byte PTEs; 2 MiB, 1 GiB, 512 GiB and (Sv57) 256 TiB superpages | [1, R-215] |
| TLB reach | entries × page size | 64 × 4 KiB = 256 KiB |
| RISC-V cause codes | 8 ecall from U; 12, 13, 15 instruction, load, store page faults; interrupts 5/7 S/M timer, 9/11 S/M external | [2, R-215] |
| VIPT limit | cache size ≤ page size × ways | §3.4 |
| Disk page fault | milliseconds from a hard disk, millions of cycles (Example 14-10.3); less from a solid-state drive, but still far beyond any cache miss | Example 14-10.3 |

### [14-11 · I/O, Buses and Interconnect](../courses/14-computer-organization-and-architecture/chapters/14-11-io-buses-and-interconnect.md)

| Quantity | Value | Note |
|---|---|---|
| UART, 8N1 | 10 bits per byte; 115,200 baud ≈ 11.5 kB/s | Example 14-11.1 |
| Interrupt overhead | hundreds to thousands of cycles per interrupt | §3.2 |
| AXI channels | AW, W, B, AR, R, each with VALID/READY | [1, R-217] |
| Mesh average hops | $2(k^2-1)/(3k) \approx 2k/3$ | §3.5 |
| PCIe encodings | 8b/10b (1.0–2.0), 128b/130b (3.0–5.0), PAM4 with Flits (6.0+) | [2, 3, R-216] |
| PCIe per-lane rates | 8, 16, 32, 64, 128 GT/s for 3.0 to 7.0; 256 GT/s target for 8.0 | [2, 3, R-216] |
| CXL 4.0 | 128 GT/s (Nov 2025) | [4, R-217] |

### [14-12 · Multicore, Coherence and Memory Consistency](../courses/14-computer-organization-and-architecture/chapters/14-12-multicore-coherence-consistency.md)

| Quantity | Value | Note |
|---|---|---|
| Coherence granularity | one cache block, typically 64 bytes | §3.5 |
| MESI read-then-write of private data | 1 bus transaction (MSI: 2) | Example 14-12.2 |
| Full-map directory overhead | about $N/(8B)$ of data: 12.5% at 64 cores, 64 B blocks | Example 14-12.4 |
| SB litmus test | SC: 3 outcomes; TSO: 4 (adds 0, 0) | [2, R-219] |
| x86 | TSO-like: stores ordered, a store may be overtaken by a later load | [2, R-219] |
| RISC-V | RVWMO by default; optional Ztso | [3, R-218] |

### [14-13 · GPUs and SIMT](../courses/14-computer-organization-and-architecture/chapters/14-13-gpus-and-simt.md)

| Quantity | Value | Note |
|---|---|---|
| Warp | 32 threads | NVIDIA |
| Shared memory | 32 banks of 4 bytes; conflict degree $\gcd(s, 32)$ | §3.5 |
| Sector / line | 32 bytes / 128 bytes | §3.5 |
| Warps to hide latency | $1 + L/k$ per scheduler | §3.6 |
| H100 SXM | 132 SMs, 16,896 FP32 lanes, 528 tensor cores, 50 MB L2, 80 GB HBM3 at 3.35 TB/s, up to 700 W | [1, R-220] |
| H100 SXM throughput | FP32 67 TFLOPS; BF16 tensor 1,979 sparse (989.5 dense) | [1, R-220] |
| Blackwell (GB200 NVL72) | 72 GPUs, 13.4 TB HBM3E at 576 TB/s per rack; about 8 TB/s per GPU | [2, R-221] |

### [14-14 · AI Accelerators: Systolic Arrays, Dataflow and Low Precision](../courses/14-computer-organization-and-architecture/chapters/14-14-ai-accelerators.md)

| Quantity | Value | Note |
|---|---|---|
| Systolic latency | $K + M + N - 2$ cycles; utilization $MKN/(P^2 T)$ | §3.2 |
| Energy, 45 nm | INT8 multiply 0.2 pJ; 32 KB SRAM 20 pJ per 64 bits; DRAM 1.3–2.6 nJ | [1, R-208] |
| Reuse to beat movement (INT8) | about 22 (32 KB SRAM), about 1400 (DRAM) | Example 14-14.4 |
| Quantization SQNR | about 6 dB per bit | §3.5 |
| TPU v4 | 8 × (128 × 128) MXUs, 1050 MHz, 275 TFLOPS, 32 GiB HBM2 at 1200 GB/s | [2, R-222] |
| TPU7x (Ironwood) | 2307 TFLOPS BF16, 4614 FP8, 192 GiB at 7380 GB/s, pods of 9216 | [2, R-222] |
| LLM decoding, batch 1 | about 1 FLOP per byte of BF16 weights | Example 14-14.6 |

### [14-15 · The Roofline Model, Benchmarks and How They Are Gamed](../courses/14-computer-organization-and-architecture/chapters/14-15-roofline-and-benchmarks.md)

| Quantity | Value | Note |
|---|---|---|
| Roofline | attainable = min(peak, bandwidth × intensity) | §3.1 |
| H100 ridge points | 20 FLOP/B (FP32), about 295 (dense BF16) | [1, R-220] |
| Vector add / SAXPY intensity | 1/12 and 1/6 FLOP/B (FP32) | §3.2 |
| SPEC CPU | ratio = reference time / measured time; geometric mean; base mandatory | [2, R-223] |
| SPEC CPU 2026 | 52 benchmarks; released May 2026; CPU 2017 retired 17 Nov 2026 | [2, R-223] |
| MLPerf | Closed against Open; single stream, multistream, server, offline | [3, R-224] |
| Geekbench 6 | baseline 2500; integer 65%, floating point 35% | [4, R-225] |

## [15 · Control Systems](../courses/15-control-systems/README.md)

### [15-01 · Modeling Dynamic Systems](../courses/15-control-systems/chapters/15-01-modeling-dynamic-systems.md)

| Quantity | Typical value | Source |
|---|---|---|
| Silicon thermal conductivity, 300 K | 130–148 W/(m·K) (sources differ with sample purity) | [2, R-228] |
| Silicon specific heat, density | 0.7 J/(g·K); 2.329 g/cm³ | [2, R-228] |
| Heat capacity of a 10 × 10 × 0.75 mm³ die | about 0.12 J/K | Derived (§3.6) |
| Thermal time constants of a chip's cooling path | milliseconds (die), seconds (spreader), minutes (heat sink) | Example 15-01.3 (illustrative) |
| Motor: stall current against running current | often tens of times larger | Example 15-01.2 |
| Linearization of $\sin\theta$ | error about 1.5% of θ at 17°, 4.6% at 30° | §3.7 (from $\theta^2/6$) |
| Pendulum period error from amplitude | +1.7% at 30°, +18% at 90° | Example 15-01.5 |

### [15-02 · Transfer Functions and Block Diagrams](../courses/15-control-systems/chapters/15-02-transfer-functions-and-block-diagrams.md)

| Quantity | Value | Source |
|---|---|---|
| Closed-loop gain for large loop gain | $\to 1/H$ (the feedback path) | §3.3 |
| Steady-state error of a proportional loop with plant DC gain 1 | $1/(1 + K)$ | Example 15-02.4 |
| Effect of loop gain on a plant pole at $-a$ (proportional control, first-order plant) | moves to $-(a + K)$ | Example 15-02.4 |
| $S + T$ | exactly 1 at every frequency | §3.4 |
| PLL natural frequency and damping (charge pump, series RC filter) | $\omega_n = \sqrt{I_{cp}K_v/(2\pi NC)}$, $\zeta = RC\omega_n/2$ | §3.6 |

### [15-03 · Time Response and Specifications](../courses/15-control-systems/chapters/15-03-time-response.md)

| Quantity | Value | Source |
|---|---|---|
| First-order rise time (10–90%) | 2.20 τ | §3.2 |
| First-order settling time to 2%, 0.1% | 3.91 τ, 6.91 τ | §3.2 |
| Rise time × bandwidth, first order | 0.35 | §3.2 |
| Settling to ½ LSB at 12 and 16 bits | 9.0 τ and 11.8 τ | §3.2 |
| Overshoot at $\zeta$ = 0.5, 0.707, 0.8 | 16.3%, 4.3%, 1.5% | §3.3 |
| Settling-time rule (2%) | $t_s \approx 4/\sigma$ | §3.3 |
| Rise-time rule | $t_r \approx 1.8/\omega_n$ (within about 25% of exact for $0.4 \le \zeta \le 0.7$) | §3.3 |
| Dominance rule | other poles more than 5σ to the left | §3.5 |
| A precision JFET op-amp's settling time to 0.01% (10 V step, gain −1), as of Nov 2026 | 120 ns (SOIC version) and 550 ns (TO-99 version) of the same part number | [1, R-230] |

### [15-04 · Feedback Properties and Steady-State Error](../courses/15-control-systems/chapters/15-04-feedback-and-steady-state-error.md)

| Quantity | Value | Source |
|---|---|---|
| Sensitivity to the forward path | $S = 1/(1 + L)$; a loop gain of 100 gives about 1% | §3.1 |
| Sensitivity to the feedback path | $\approx -1$ | §3.1 |
| Step error, type 0 | $1/(1 + K_p)$ | §3.3 |
| Ramp error, type 1 | $1/K_v$ | §3.3 |
| Parabola error, type 2 | $1/K_a$ | §3.3 |
| Input-disturbance offset with proportional control and a plant integrator | $d/C(0)$ | §3.4 |
| PLL phase error during a frequency sweep $\alpha$ (type 2) | $\alpha/\omega_n^2$ | Example 15-04.5 |
| Op-amp closed-loop error at loop gain $\lvert L\rvert$ with $L$ near −90° | about $1/\lvert L\rvert$ as a complex error, mostly phase; the quadrature part of the magnitude error is about $1/(2\lvert L\rvert^2)$, plus the in-phase DC error $1/(1 + A_0\beta)$ | Example 15-04.6 |

### [15-05 · Stability and the Routh–Hurwitz Criterion](../courses/15-control-systems/chapters/15-05-stability-routh-hurwitz.md)

| Quantity | Value | Source |
|---|---|---|
| Stability of a cubic $a_3s^3 + a_2s^2 + a_1s + a_0$ | positive coefficients and $a_2a_1 > a_3a_0$ | §3.3 |
| Largest stable gain, three identical poles | 8 (18 dB), oscillation at $\sqrt3\,\omega_0$ | Example 15-05.3 |
| Minimum stage gain of an $n$-stage ring oscillator (identical single-pole stages) | $1/\cos(180°/n)$: 2 for three stages, 1.24 for five | Example 15-05.3, Problem 15-05.7 |
| Ring-oscillator frequency, $n$ single-pole stages | $\omega_0\tan(180°/n)$ | Problem 15-05.7 |
| Third-order PLL | stable for any $K$ if $\tau_z > \tau_p$ | Example 15-05.5 |

### [15-06 · Root Locus](../courses/15-control-systems/chapters/15-06-root-locus.md)

| Quantity | Value | Source |
|---|---|---|
| Asymptote angles for $n - m$ = 1, 2, 3, 4 | 180°; ±90°; ±60° and 180°; ±45° and ±135° | §3.2 |
| Centroid | $(\sum p - \sum z)/(n - m)$ | §3.2 |
| Two poles at 0 and $-a$, gain $K$ | vertical line at $-a/2$; settling time fixed at about $8/a$ | Example 15-06.1 |
| Two poles and a zero to their left | circle centered at the zero, radius $\sqrt{\lvert z - p_1\rvert\,\lvert z - p_2\rvert}$ | §3.5 |
| Smallest damping on that circle | $\cos\theta$ with $\sin\theta$ = radius / distance from origin to the zero | Example 15-06.6 |

### [15-07 · Frequency-Domain Design: Bode, Nyquist and Margins](../courses/15-control-systems/chapters/15-07-frequency-domain-design.md)

| Quantity | Value | Source |
|---|---|---|
| Phase margin against damping | PM ≈ 100ζ (deg) up to ζ ≈ 0.7; 45° ↔ ζ ≈ 0.42; 65.5° ↔ ζ = 0.707 | §3.4 |
| Common design targets | PM 45°–70°, GM ≥ 6–10 dB, $M_s$ ≤ 1.3–2 | §3.7 and practice |
| Delay margin | PM (rad) / $\omega_c$ | §3.2 |
| Phase of a delay | $-\omega T$: −57.3° per radian of $\omega T$ | §3.5 |
| Two-pole op-amp at unity gain | PM = 90° − arctan($f_c/f_2$) with the true crossover $f_c$: 65.5° for $f_2$ = 2 GBW, 76.3° for $f_2$ = 4 GBW, 51.8° for $f_2$ = GBW (with $f_c \approx$ GBW: 63.4°, 76.0°, 45.0°) | Example 15-07.6, §3.8, lab |
| Third-order PLL, best margin | $\arctan[(b - 1)/(2\sqrt b)]$ at $\omega_c = 1/\sqrt{\tau_z\tau_p}$, $b = \tau_z/\tau_p$ | §3.8 |
| Bode's integral | 0 for stable open loops; $\pi\sum\mathrm{Re}\,p_k$ otherwise | §3.7 |

### [15-08 · PID Control](../courses/15-control-systems/chapters/15-08-pid-control.md)

| Quantity | Value | Source |
|---|---|---|
| PID transfer function | $K_p(1 + 1/(T_is) + T_ds)$; zeros real when $T_i \ge 4T_d$ | §3.1 |
| Ziegler–Nichols PID | $0.6K_u$, $P_u/2$, $P_u/8$: about 30° phase margin, 40–50% overshoot | §3.6, Example 15-08.3 |
| Tyreus–Luyben PID | $K_u/2.2$, $2.2P_u$, $P_u/6.3$ | §3.6 |
| SIMC PI | $K_p = \tau/[K(\tau_c + \theta)]$, $T_i = \min[\tau, 4(\tau_c + \theta)]$, default $\tau_c = \theta$ | §3.6 |
| Derivative filter | $N$ = 5 to 20; high-frequency gain $K_p(1 + N)$ | §3.8 |
| PI zero below crossover | a factor of 3 to 10 costs about 18° to 6° of phase | §3.5 |

### [15-09 · Lead and Lag Compensation](../courses/15-control-systems/chapters/15-09-lead-lag-compensation.md)

| Quantity | Value | Source |
|---|---|---|
| Lead maximum phase | $\arcsin[(\alpha - 1)/(\alpha + 1)]$: 19.5° at α = 2, 36.9° at 4, 54.9° at 10, 61.9° at 16 | §3.1 |
| Lead frequency and gain at the peak | $\omega_m = 1/(T\sqrt\alpha)$, gain $\sqrt\alpha$ | §3.1 |
| Lag zero placement | about a decade below crossover, costing about 5° | §3.2 |
| Extra lead allowance | 5° to 10° above the computed deficiency | §3.3 |
| Type III compensator | integrator, two zeros near $f_0$, two poles above crossover; crossover ≤ $f_{sw}/10$ | §3.7 |

### [15-10 · State-Space Introduction](../courses/15-control-systems/chapters/15-10-state-space-introduction.md)

| Quantity | Value | Source |
|---|---|---|
| Solution | $\mathbf{x}(t) = e^{At}\mathbf{x}(0) + \int_0^te^{A(t - \tau)}B\mathbf{u}\,d\tau$ | §3.2 |
| Controllability / observability tests | rank $[B\ AB\ \cdots\ A^{n-1}B] = n$; rank of the stacked $C, CA, \ldots$ = $n$ | §3.4–3.5 |
| Reference scaling | $N = -1/[C(A - BK)^{-1}B]$ | §3.6 |
| Observer speed | 2 to 10 times the controller's poles | §3.7 |
| Separation principle | closed-loop poles = eig($A - BK$) ∪ eig($A - LC$) | §3.7 |

### [15-11 · Digital Control](../courses/15-control-systems/chapters/15-11-digital-control.md)

| Quantity | Value | Source |
|---|---|---|
| Pole mapping | $z = e^{sT}$; stable means inside the unit circle | §3.1 |
| Phase lag of a ZOH | about $\omega T/2$ radians | §3.5 |
| Sample rate rule | 10 to 30 times the closed-loop bandwidth | §3.5 |
| Digital power control delay | about 1 to 1.5 switching periods | Example 15-11.6 |
| Second-order Jury test | $\lvert a_0\rvert < 1$, $1 \pm a_1 + a_0 > 0$ | §3.4 |
| Tustin PI | $u_k = u_{k-1} + (K_p + K_iT/2)e_k + (-K_p + K_iT/2)e_{k-1}$ | §3.3 |

### [15-12 · Applications: PLLs, Voltage Regulators and Thermal Management](../courses/15-control-systems/chapters/15-12-control-applications-pll-regulators-thermal.md)

| Quantity | Value | Source |
|---|---|---|
| Maximum-margin third-order PLL | $\sqrt b = \tan\text{PM} + \sec\text{PM}$; $b$ = 13.9 for 60° | §3.2 |
| Its closed-loop poles | $-\omega_c$, and a pair with $\omega_n = \omega_c$, $\zeta = (\sqrt b - 1)/2$ | §3.2 |
| PLL bandwidth limit from PFD sampling | $f_c \lesssim f_{ref}/10$ (about 18° at the limit) | §3.2 |
| Noise-optimal PLL bandwidth | near the crossing of reference-path and VCO noise | §3.2, Example 15-12.5 |
| Jitter from phase | $\phi_{rms}/(2\pi f_{out})$ | §3.2 |
| Load-step droop, load line | $\Delta I/(\omega_0C)$ with $\omega_0 = g/C$ the crossover | §3.4 |
| Load-step droop, critically damped PI | $(2/e)\,\Delta I/(\omega_0C)$ at $t = 2/\omega_0$; crossover $1.029\,\omega_0$ | §3.4 |
| DVFS order | voltage up before frequency; frequency down before voltage | §3.5 |
| Sustained thermal power | $(T_{lim} - T_A)/R_{total}$ | §3.6 |
| Decay of permitted power (two nodes) | time constant $C_H(R_{JC} \parallel R_{CA})$ | §3.6 |
| ACPI passive-cooling sampling period | `_TSP` in tenths of seconds; `_TFP` (since ACPI 6.0) in milliseconds, overriding `_TSP` (as of Nov 2026) | [R-232] |
| Linux power-allocator defaults (as of Nov 2026) | $k_{pu} = 2P_{sus}/(T_{set} - T_{on})$, $k_{po} = P_{sus}/(T_{set} - T_{on})$, $k_d$ = 0 | [R-231] |
| Linux power-allocator typical setting (as of Nov 2026) | $k_i$ "typically" 1 or 2 (a recommendation, not a default) | [R-231] |

## [16 · Digital Signal Processing](../courses/16-digital-signal-processing/README.md)

### [16-01 · Discrete-Time Signals and Systems Review](../courses/16-digital-signal-processing/chapters/16-01-discrete-time-systems-review.md)

| Quantity | Value | Source |
|---|---|---|
| Audio sample rates | 44.1 kHz (CD), 48 kHz (professional and video); voice 8 kHz (narrowband), 16 kHz (wideband) | Long-standing industry conventions |
| Digital frequency | $\omega = 2\pi f/f_s$ rad/sample; Nyquist at $\omega = \pi$ | §3.1 |
| $N$-point moving average | Nulls at $mf_s/N$; delay $(N - 1)/2$ samples; noise variance gain $1/N$ | §3.6, §3.4 |
| EMA with factor $\alpha$ | Time constant $\approx 1/\alpha - 1/2$ samples; noise gain $\alpha/(2 - \alpha)$ | §3.4 |
| Accumulator growth | $\lceil\log_2 N\rceil$ extra bits for a sum of $N$ terms | §3.7 |
| Energy per operation, 45 nm, 0.9 V | 32-bit integer multiply 3.1 pJ, add 0.1 pJ; 8-bit multiply 0.2 pJ; 64-bit read of an 8 KB SRAM 10 pJ; DRAM 1.3–2.6 nJ; about 70 pJ per instruction of processor overhead | Horowitz, ISSCC 2014 [1] (R-208) **[Established]** |

The 45 nm energies are a decade-old reference point; newer processes lower every entry, so use them for ratios (memory access against arithmetic, overhead against operation), not for absolute power in a current product.

### [16-02 · DTFT and z-Transform for DSP](../courses/16-digital-signal-processing/chapters/16-02-dtft-and-z-transform-for-dsp.md)

| Quantity | Value | Source |
|---|---|---|
| Pole at radius $r$ near the circle | −3 dB width $\approx 2(1 - r)$ rad/sample; time constant $\approx 1/(1 - r)$ samples; width × time constant ≈ 2 | §3.3 |
| Resonator peak and $Q$ | Peak $\approx 1/(1 - r)$ with zeros at ±1; $Q \approx \omega_0/[2(1 - r)]$ | §3.3, Example 16-02.3 |
| Group delay of a pole at its own angle | $\rho/(1 - \rho)$ samples | §3.4 |
| First-order all-pass $(z^{-1} - a)/(1 - az^{-1})$ | Delay $(1 + a)/(1 - a)$ at DC, $(1 - a)/(1 + a)$ at $\pi$ | §3.6 |
| Symmetric FIR of length $N$ | Group delay $(N - 1)/2$ samples | §3.4 |
| Delayed FIR inverse of a precursor $\rho$ | Residual $\rho^K$ after $K$ taps and $K - 1$ symbols of added delay | §3.7, Example 16-02.5 |

### [16-03 · The DFT and Its Properties](../courses/16-digital-signal-processing/chapters/16-03-the-dft.md)

| Quantity | Value | Source |
|---|---|---|
| Bin spacing | $f_s/N$ = 1 / record length | §3.2 |
| On-bin tone of amplitude $A$ | $\lvert X[k_0]\rvert = AN/2$ in each of bins $k_0$ and $N - k_0$ | §3.2 |
| Worst-case scalloping (rectangular window, tone halfway between bins) | −3.92 dB ($2/\pi$) for long records | 16-05 preview; Example 16-03.2 shows −1.68 dB at a third of a bin; Problem 16-03.8 |
| Circular = linear convolution | $N \ge L + M - 1$ | §3.5 |
| Direct DFT against FFT | $N^2$ against about $(N/2)\log_2N$ complex multiplies | §3.1, 16-04 |
| FFT convolution crossover (simple model) | 44 taps; best FFT size roughly 5–10 times the filter length | Example 16-03.5 |

### [16-04 · The FFT Algorithm](../courses/16-digital-signal-processing/chapters/16-04-the-fft.md)

| Quantity | Value | Source |
|---|---|---|
| Direct DFT | $N^2$ complex multiplications | §3.1 |
| Radix-2 FFT | $\frac N2\log_2N$ butterflies and multiplications; $N\log_2N$ complex additions | §3.2 |
| Non-trivial twiddles, radix-2 | $\frac N2\log_2N - \frac{3N}2 + 2$ (3,586 for $N$ = 1024) | §3.5 |
| Radix-4 | $\frac{3N}8\log_2N$ complex multiplications (75% of radix-2) | §3.6 |
| R2SDF pipeline | $\log_2N$ butterflies, $\log_2N - 2$ general multipliers, $N - 1$ delay words, one sample per clock | §3.7 |
| Word growth | up to $\log_2N$ bits for real data, $\log_2N + 1$ for complex; up to $1 + \sqrt2$ per stage in a component | §3.8 |
| Scaled fixed-point FFT noise | about 3 dB of SNR lost per doubling of $N$ (half a bit per stage) | §3.8 |
| Origin | Cooley and Tukey, 1965 [1] | Established |

### [16-05 · Spectral Analysis and Windowing](../courses/16-digital-signal-processing/chapters/16-05-spectral-analysis-and-windowing.md)

| Quantity | Value | Source |
|---|---|---|
| Rectangular window | ENBW 1 bin, −13.3 dB sidelobes, −3.92 dB worst scalloping | §3.2 |
| Hann window | CG 0.5, ENBW 1.5 bins, −31.5 dB sidelobes, −1.42 dB scalloping | §3.2 [1] |
| 4-term Blackman–Harris | ENBW 2.0 bins, −92 dB sidelobes | §3.2 [1] |
| Ideal ADC SNR | $6.02B + 1.76$ dB (74.0 dB at 12 bits, 98.1 dB at 16 bits) | §3.5 |
| FFT processing gain | $10\log_{10}(N/2)$ dB (rectangular) | §3.4 |
| Periodogram bin | standard deviation equal to the mean; $1/\sqrt K$ with $K$ averages | §3.4 |
| ENOB | $(\text{SINAD} - 1.76)/6.02$ for a full-scale test | §3.5 |

### [16-06 · FIR Filter Design](../courses/16-digital-signal-processing/chapters/16-06-fir-filter-design.md)

| Quantity | Value | Source |
|---|---|---|
| Gibbs overshoot of truncation | 8.95% of the jump; first stopband sidelobe about −21 dB, for any length | §3.3 |
| Gain at a window design's cutoff | 0.5 (−6 dB) | §3.3 |
| Window-method errors | rectangular −21 dB, Hann −44 dB, Hamming about −53 dB, Blackman −75 dB | §3.4 |
| Window-method transition | $\Delta\omega \approx 2\pi D/M$ with $D$ ≈ 0.9, 3.1, 3.3, 5.6 | §3.4 |
| Kaiser formulas | $\beta = 0.1102(A - 8.7)$ for $A > 50$; $M = (A - 8)/(2.285\Delta\omega)$ | §3.5 [2] |
| Equiripple order estimate | $M \approx (-10\log_{10}(\delta_p\delta_s) - 13)/(2.324\Delta\omega)$ | §3.7 [3] |
| Linear-phase delay | $M/2$ samples | §3.2 |
| Multipliers with folding | $\lceil (M + 1)/2\rceil$ | §3.8 |
| 0.1 dB peak-to-peak ripple | $\delta_p$ = 0.00576; 60 dB is $\delta_s$ = 0.001 | §3.1 |

### [16-07 · IIR Filter Design](../courses/16-digital-signal-processing/chapters/16-07-iir-filter-design.md)

| Quantity | Value | Source |
|---|---|---|
| Butterworth order | $N \ge \log_{10}D/(2\log_{10}(\Omega_s/\Omega_p))$; −3.01 dB at $\Omega_c$; $20N$ dB/decade | §3.1 |
| Chebyshev order | $N \ge \operatorname{arccosh}\sqrt D/\operatorname{arccosh}(\Omega_s/\Omega_p)$ | §3.2 |
| Bilinear warping | $\Omega = 2f_s\tan(\omega/2)$; prewarp the band edges | §3.4 |
| Pole delay at its own angle | $\rho/(1 - \rho)$ samples (19 at 0.95, 99 at 0.99) | §3.6 |
| Running example (48 kHz, 4 → 5 kHz, 0.1/60 dB) | Butterworth 38, Chebyshev 14, elliptic 8, equiripple FIR 137 taps | Examples 16-07.4–5, 16-06.5 |
| Biquad cost | 5 multiplications in general; 3 for a section with zeros on the unit circle and $b_0 = b_2 = 1$ | Example 16-07.5, 16-08 |

### [16-08 · Filter Structures and Implementation](../courses/16-digital-signal-processing/chapters/16-08-filter-structures.md)

| Quantity | Value | Source |
|---|---|---|
| DF I / DF II / cascade costs, order $N$ | DF I and DF II: $2N + 1$ multipliers, $2N$ vs $N$ delays; a cascade of $N/2$ biquads: $5N/2$ multipliers (5 per biquad) | §3.2–3.3 |
| Transposed FIR critical path | one multiplier + one adder, any length | §3.1 |
| Pole sensitivity | $\partial p_i/\partial a_k = -p_i^{N-k}/\prod_{j\ne i}(p_i - p_j)$ | §3.4 |
| Direct-form biquad angle sensitivity | $1/(2\rho\sin\theta)$: large near DC and Nyquist | §3.4 |
| Lattice stability | all $\lvert k_m\rvert < 1$ | §3.5 |
| Biquad accumulator | 35 bits for five 16 × 16 products; 40 bits common | §3.6 |

### [16-09 · Multirate DSP: Decimation, Interpolation and Polyphase](../courses/16-digital-signal-processing/chapters/16-09-multirate-dsp.md)

| Quantity | Value | Source |
|---|---|---|
| Downsampled spectrum | $\frac1M\sum_k X(e^{j(\omega - 2\pi k)/M})$ | §3.1 |
| Upsampled spectrum | $X(e^{j\omega L})$; interpolation gain $L$ | §3.2 |
| Polyphase saving | factor $M$ (decimation) or $L$ (interpolation) | §3.5 |
| 44.1 → 48 kHz | $L/M = 160/147$ | §3.3 |
| Half-band filter | middle tap 1/2, every other tap zero, $n = 4K + 3$ taps with $K + 1$ folded multipliers | §3.6 |
| CIC | $\lvert\sin(\pi fR/f_s)/\sin(\pi f/f_s)\rvert^N$; growth $N\log_2R$ bits; wrap-around arithmetic | §3.7 [1] |

### [16-10 · Quantization and Fixed-Point Effects](../courses/16-digital-signal-processing/chapters/16-10-quantization-and-fixed-point.md)

| Quantity | Value | Source |
|---|---|---|
| Rounding noise | $\Delta^2/12$, white, if the signal is busy | §3.2 |
| SQNR of a full-scale sine | $6.02N + 1.76$ dB (74.0 dB at 12 bits, 98.1 dB at 16) | §3.2 |
| Gaussian loading | $6.02N + 4.77 - 20\log_{10}L$ dB before clipping; optimum $L \approx 5$ (12 bits) to 6 (16 bits) | §3.3 |
| Q1.15 | range [−1, 1), step $3.05 \times 10^{-5}$ | §3.1 |
| TPDF dither | ±1 LSB triangular; total error $\Delta^2/4$ (+4.8 dB) | §3.2 |
| Noise gain | $\sum g[n]^2$ from the rounding point to the output | §3.4 |
| First-order dead band | $\lvert k\rvert \le 1/(2(1 - \lvert a\rvert))$ LSB | §3.7 |

### [16-11 · DSP Hardware Architectures](../courses/16-digital-signal-processing/chapters/16-11-dsp-hardware-architectures.md)

| Quantity | Value | Source |
|---|---|---|
| MAC widths | product $b_x + b_c$; accumulator + $\lceil\log_2N\rceil$ guard bits (40-bit for 16 × 16, 256 taps) | §3.1 |
| Hardware budget | multipliers = $\lceil$(mults per output × $f_s$)/$f_{\text{clk}}\rceil$ | §3.2 |
| Iteration bound | $\max_\ell T_\ell/D_\ell$; look-ahead by $M$ divides it by $M$ | §3.4 |
| Energy at 45 nm | 8-bit mult 0.2 pJ, 32-bit mult 3.1 pJ, 32-bit add 0.1 pJ, instruction ≈ 70 pJ, DRAM 1.3–2.6 nJ | §3.6, R-208 |
| CORDIC | gain 1.64676, range ±99.88°, about one bit per iteration | §3.7 |

## [17 · Communication Systems](../courses/17-communication-systems/README.md)

### [17-01 · Random Processes and Power Spectral Density](../courses/17-communication-systems/chapters/17-01-random-processes-and-psd.md)

| Quantity | Value | Source |
|---|---|---|
| Thermal noise density at 290 K | $kT_0$ = $4.00 \times 10^{-21}$ W/Hz = −174 dBm/Hz | Physics (§3.4 units, Example 17-01.6) |
| Resistor voltage noise at 300 K | $\sqrt{4kTR}$ = 4.07 nV/√Hz for 1 kΩ (scales as $\sqrt R$) | 03-06 |
| One-pole noise bandwidth | $B_N = (\pi/2)f_{3\text{dB}}$; correlation time $RC$ | §3.5 |
| Capacitor noise | $\sqrt{kT/C}$: 64 µV for 1 pF, 2.0 µV for 1 nF at 300 K, any $R$ or $L$ | Example 17-01.3 |
| Polar NRZ spectrum | $A^2T\operatorname{sinc}^2(fT)$: nulls at $k/T$; 90.3% of power below $1/T$, 77.4% below $1/(2T)$ | §3.8 |
| Band-limited white Gaussian noise | independent samples every $1/(2B)$, each of variance $N_0B$ | §3.6 |
| Wideband noise sampled unfiltered | in-band density rises by about $2B_N/f_s$ | §3.7 |
| I/Q noise components | each with the full bandpass power; uncorrelated at the same instant | §3.9 |

### [17-02 · Noise and SNR in Communication Systems](../courses/17-communication-systems/chapters/17-02-noise-and-snr.md)

| Quantity | Value | Note |
|---|---|---|
| $kT_0$, $T_0$ = 290 K | −173.98 dBm/Hz ≈ −174 dBm/Hz | $4.004 \times 10^{-21}$ W/Hz [R-257] |
| Noise in 1 MHz / 20 MHz | −114 / −101 dBm | add NF for a receiver's floor |
| Noise temperature for NF 0.5 / 1 / 3 dB | 35 / 75 / 289 K | $T_e = (F - 1)290$ |
| Room-temperature loss | NF = loss | 1 dB of cable = 1 dB of NF |
| GPS L1 C/A minimum received power | −128.5 dBm (−158.5 dBW) | IS-GPS-200N, 3 dBi antenna [R-259] |
| GPS $C/N_0$ at minimum power | 46.9 dB-Hz | 100 K antenna, NF 1.4 dB (Example 17-02.6) |
| 3GPP NR UE REFSENS, n78, 10 MHz, 2 Rx | −95.8 dBm | NF 10 dB assumed [R-260] |
| Wi-Fi minimum sensitivity, 20 MHz | −82 dBm (BPSK 1/2) to −57 dBm (256-QAM 5/6) | 802.11ac table, as of Nov 2026 [R-261] |
| Cellular or GNSS LNA noise figure | 0.5–1.5 dB typical | data sheets, as of Nov 2026 [R-262] |
| Shannon limit | $E_b/N_0$ = −1.59 dB | 17-07 |

### [17-03 · Analog Modulation (Brief)](../courses/17-communication-systems/chapters/17-03-analog-modulation.md)

| Quantity | Value | Note |
|---|---|---|
| Carrier nulls of tone FM | β = 2.405, 5.520 | used to calibrate deviation |
| Carson bandwidth | $2(\Delta f + W)$ | about 99% of power for β ≳ 1 |
| AM power efficiency, tone, 100% | 1/3 (−4.77 dB) | |
| FM gain, tone | $\tfrac32\beta^2$; β = 5 → 15.7 dB | above threshold |
| FM threshold | CNR ≈ 10 dB in $B_T$ | rule of thumb |
| SSB over AM, equal peak power | 9.03 dB | |
| De-emphasis improvement, 15 kHz | 13.2 dB (75 µs), 10.2 dB (50 µs) | |
| FM broadcast | ±75 kHz = 100%; 200 kHz channels; 75 µs (US) or 50 µs (Europe) | as of Nov 2026 [R-263], [R-264] |
| FM stereo composite | pilot 19 kHz; L − R DSB-SC on 38 kHz, 23–53 kHz | [R-263] |
| AM broadcast spacing | 10 kHz (Americas), 9 kHz (GE75 plan) | [R-265] |
| European aviation voice | AM, 8.33 kHz channels, 117.975–137 MHz | [R-266] |

### [17-04 · Baseband Digital Transmission](../courses/17-communication-systems/chapters/17-04-baseband-digital-transmission.md)

| Quantity | Value | Note |
|---|---|---|
| Nyquist rate | $2B$ symbols/s in bandwidth $B$ | minimum bandwidth $1/(2T)$ |
| Raised-cosine bandwidth | $(1 + \alpha)/(2T)$ baseband, $(1 + \alpha)/T$ passband | α typically 0.1–0.5 |
| PAM4 eye penalty | −9.54 dB (equal peak), −6.99 dB (equal power) | |
| $\mathbb{E}[a^2]$ for M-PAM, spacing 2 | $(M^2 - 1)/3$ | 1, 5, 21 for M = 2, 4, 8 |
| NRZ / Manchester power below $1/T$ | 90.3% / 64.5% | |
| Block-code overhead | 25% (8b/10b), 3.125% (64b/66b), 1.5625% (128b/130b) | |
| One-pole channel | eye closes at $\approx 9.1f_{3\text{dB}}$ | 50% eye at $\approx 4.5f_{3\text{dB}}$ |
| 3GPP UTRA RRC roll-off | 0.22 at 3.84 Msymbol/s | [R-258] |

### [17-05 · Matched Filters and Optimal Detection](../courses/17-communication-systems/chapters/17-05-matched-filters-and-detection.md)

| Quantity | Value | Note |
|---|---|---|
| Matched-filter peak SNR | $2E/N_0$ | independent of pulse shape |
| BPSK BER | $Q(\sqrt{2E_b/N_0})$; 9.59 dB for $10^{-5}$, 10.53 dB for $10^{-6}$ | |
| Orthogonal or on-off BER | $Q(\sqrt{E_b/N_0})$ | 3 dB worse than antipodal |
| Error probability between two points | $Q(d/\sqrt{2N_0})$ | noise variance $N_0/2$ per dimension |
| $Q^{-1}$ | 4.265 ($10^{-5}$), 4.753 ($10^{-6}$), 7.034 ($10^{-12}$), 7.349 ($10^{-13}$) | |
| Best one-pole filter on a rectangular pulse | −0.89 dB at $f_{3\text{dB}} \approx 0.2/T$ | |
| PAM4 penalty at $10^{-6}$ | 3.87 dB in $E_b/N_0$ | |

### [17-06 · Bandpass Digital Modulation and BER](../courses/17-communication-systems/chapters/17-06-bandpass-digital-modulation.md)

| Quantity | Value | Note |
|---|---|---|
| BPSK and QPSK BER | $Q(\sqrt{2E_b/N_0})$; 9.59 dB at $10^{-5}$ | QPSK doubles the rate at the same BER |
| Efficiency penalty per bit vs QPSK | 8-PSK 3.57 dB; 16-QAM 3.98; 64-QAM 8.45; 256-QAM 13.27; 1024-QAM 18.34 dB | asymptotic |
| 16-QAM over 16-PSK | 4.20 dB | |
| Peak-to-average | 16-QAM 2.55 dB, 64-QAM 3.68 dB | symbols only, before pulse shaping |
| DPSK / noncoherent FSK penalty at $10^{-5}$ | 0.75 dB / 3.76 dB over BPSK | |
| EVM ↔ SNR | 17.5% ↔ 15.1 dB; 3.5% ↔ 29.1 dB; 2.5% ↔ 32.0 dB | if noise-like |
| NR EVM limits (BS) | QPSK 17.5%, 16-QAM 12.5%, 64-QAM 8%, 256-QAM 3.5%, 1024-QAM 2.5% (≤ 4.2 GHz) | TS 38.104, as of Nov 2026 [R-275] |
| DVB-S2 QPSK 1/2 | $E_s/N_0$ = 1.00 dB at 0.989 b/symbol | 1.07 dB from Shannon [R-276] |

### [17-07 · Information Theory and Shannon Capacity](../courses/17-communication-systems/chapters/17-07-information-theory-and-shannon.md)

| Quantity | Value | Note |
|---|---|---|
| Shannon–Hartley | $C = B\log_2(1 + S/N)$ | complex baseband: $B$ = RF bandwidth |
| Ultimate Shannon limit | $E_b/N_0$ = ln 2 = −1.59 dB | infinite bandwidth |
| Limit at η = 1, 2, 4, 6 b/s/Hz | 0, 1.76, 5.74, 10.21 dB | $(2^\eta - 1)/\eta$ |
| Infinite-bandwidth capacity | $1.443\,S/N_0$ | power-limited regime |
| High-SNR slope | about 3 dB per extra b/s/Hz | bandwidth-limited regime |
| BSC capacity | $1 - h(p)$; 0.919 at 1% | |
| Soft vs hard decisions | ≈ 1.6 dB at rate 1/2 (BPSK) | |
| Uncoded gap at $10^{-5}$ | ≈ 7.6–7.8 dB | QPSK to 64-QAM |

### [17-08 · Channel Coding](../courses/17-communication-systems/chapters/17-08-channel-coding.md)

| Quantity | Value | Note |
|---|---|---|
| Correctable errors | $t = \lfloor(d_{min} - 1)/2\rfloor$ | detect $d_{min} - 1$; erasures $d_{min} - 1$ |
| Asymptotic gain | soft $10\log_{10}(Rd_{min})$, hard ≈ $10\log_{10}(R(t + 1))$ | soft ≈ 3 dB better asymptotically |
| Hamming (7,4) | $d_{min}$ = 3; gain 2.34 dB soft, 0.58 dB hard | perfect code |
| SEC-DED for 64 bits | 8 check bits, (72,64), 12.5% | 08-01 |
| CRC of degree r | all bursts ≤ r; misses ≈ $2^{-r}$ of random errors | NR: CRC24A/B/C, 16, 11, 6 [R-279] |
| (7,5) convolutional code | $d_{free}$ = 5, 4 states, 3.98 dB soft | $T(D) = D^5/(1 - 2D)$ |
| (171,133), K = 7 | $d_{free}$ = 10, 64 states; ≈ 4.2 dB at $10^{-5}$ | CCSDS, 802.11 [R-281] |
| KP4 RS(544,514) | t = 15, 5.84% overhead, raw BER ≈ 2.4 × 10⁻⁴ for $10^{-12}$ | independent errors [R-280] |
| NR LDPC | BG1 rate ≥ 1/3, ≤ 8448 bits; BG2 rate ≥ 1/5, ≤ 3840 bits | $Z_c$ ≤ 384 [R-279] |
| NR polar | mother code ≤ 512 bits (broadcast, downlink control), ≤ 1024 bits (uplink control) | control and broadcast [R-279] |
| Best long codes | ≈ 0.5–1 dB from the constrained limit | DVB-S2 QPSK 1/2: 0.89 dB |

### [17-09 · Wireless Channels: Fading and Multipath](../courses/17-communication-systems/chapters/17-09-wireless-channels.md)

| Quantity | Value | Note |
|---|---|---|
| Free-space loss | $32.45 + 20\log f_{\text{MHz}} + 20\log d_{\text{km}}$ dB | P.525 rounds to 32.4 [R-282] |
| Free-space slope | 20 dB/decade (6 dB per doubling) | two-ray beyond breakpoint: 40 dB/decade |
| Two-ray breakpoint | $4h_th_r/\lambda$ | 700 m for 10 m and 1.5 m at 3.5 GHz |
| UMi shadowing σ | 4 dB LOS, 7.82 dB NLOS | TR 38.901 [R-283] |
| 90% coverage margin | 1.28 σ | 95%: 1.64 σ |
| Median delay spread | ≈ 20 ns indoor to ≈ 270 ns urban macro NLOS | TR 38.901 [R-284] |
| Coherence bandwidth (50%) | $0.276/\tau_{rms}$ (exponential PDP) | rule of thumb $1/(5\tau_{rms})$ |
| Doppler | $f_D = vf_c/c$: 389 Hz at 3.5 GHz, 120 km/h | |
| Coherence time (50%) | $0.242/f_D$ | |
| Rayleigh outage | ≈ $10^{-M/10}$ for margin M dB | one decade per 10 dB |
| BPSK in Rayleigh | $\approx 1/(4\bar\gamma)$; 44 dB for $10^{-5}$ | AWGN: 9.6 dB |
| NR numerology | 14 symbols/slot, $2^\mu$ slots/ms, $15 \cdot 2^\mu$ kHz | [R-285] |

### [17-10 · OFDM](../courses/17-communication-systems/chapters/17-10-ofdm.md)

Rows citing the research log describe the standards as of Nov 2026.

| Quantity | Value | Note |
|---|---|---|
| Orthogonal spacing | $\Delta f = 1/T$ | sinc spectra, zeros at neighbours |
| NR numerology | $15 \cdot 2^\mu$ kHz, μ = 0–6; 14 symbols per slot; $2^\mu$ slots per ms | [R-285] |
| NR normal CP | $144/2048$ of $T$: 4.69 μs (15 kHz), 2.34 μs (30 kHz), 0.59 μs (120 kHz) | 6.57% of the symbol [R-286] |
| NR 100 MHz carrier | 273 RB at 30 kHz = 3276 subcarriers, 98.28 MHz | guard 845 kHz/side [R-287] |
| Resource block | 12 subcarriers | [R-285] |
| CFO ICI | $(\pi\varepsilon)^2/3$: −34.8 dB at 1%, −14.8 dB at 10% | ε = offset/spacing |
| Doppler ICI | $(\pi f_D/\Delta f)^2/6$ | Clarke model |
| PAPR at $10^{-3}$ | ≈ $\ln(N/10^{-3})$: 10.4–11.8 dB for 64–3276 subcarriers | +0.1–0.4 dB oversampled |
| DFT-spread OFDM | several dB lower PAPR than OFDM | NR uplink option [R-286] |

### [17-11 · MIMO and Beamforming Basics](../courses/17-communication-systems/chapters/17-11-mimo-and-beamforming.md)

Rows citing the research log describe the standards as of Nov 2026.

| Quantity | Value | Note |
|---|---|---|
| MRC | SNR = $\|\mathbf h\|^2E_s/N_0$; mean $N\bar\gamma$; diversity $N$ | matched filter in space |
| Selection combining | mean $\bar\gamma\sum1/k$ (1.5 for 2, 2.08 for 4) | diversity $N$ |
| Alamouti 2×1 | diversity 2, rate 1, 3 dB below 1×2 MRC | no CSI at transmitter |
| ULA, $d = \lambda/2$ | gain $N$; HPBW ≈ $101.5°/N$ at broadside | grating-free: $d \le \lambda/(1 + \sin\theta_0)$ |
| MIMO capacity | $\log_2\det(\mathbf I + \tfrac{\rho}{N_t}\mathbf H\mathbf H^H)$ | slope = rank ≤ $\min(N_t, N_r)$ |
| Ergodic at 20 dB | 5.88 (1×1), 11.29 (2×2), 22.1 (4×4) b/s/Hz | i.i.d. Rayleigh |
| ZF diversity | $N_r - N_t + 1$ per stream | |
| NR layers | up to 8 DL (2 codewords above 4); UE ≥ 4 where 4Rx mandatory | [R-289], [R-290] |
| NR peak rate | ≈ 2.34 Gb/s per 100 MHz FR1 carrier with 4 layers of 256-QAM | TS 38.306 [R-289] |

### [17-12 · Multiple Access, Cellular and Wi-Fi Systems](../courses/17-communication-systems/chapters/17-12-multiple-access-and-cellular-wifi.md)

Rows citing the research log describe the standards as of Nov 2026.

| Quantity | Value | Note |
|---|---|---|
| CDMA processing gain | $R_c/R_b$ | single-cell users ≈ $1 + G_p/(E_b/I_0)$ |
| Hexagonal reuse | $D/R = \sqrt{3N}$; $N = i^2 + ij + j^2$ | SIR ≈ $(\sqrt{3N})^n/6$ |
| Edge SIR ($n$ = 4) | 11.3 dB ($N$ = 3), 18.7 dB ($N$ = 7) | $N$ = 1: formula 1.8 dB, but a cell corner is below −3 dB |
| ALOHA maximum | 0.184 (pure, $G$ = 0.5), 0.368 (slotted, $G$ = 1) | |
| CSMA slot success | $n\tau(1 - \tau)^{n-1}$; best ≈ $1/e$ at τ = $1/n$ | |
| Erlang B | 10 channels at 5 Erl: 1.84%; 20 Erl at 2%: 28 channels | trunking gain |
| Multi-user diversity | mean of best of $K$ = $\bar\gamma\sum_{k\le K}1/k$ | 1.65× rate for 10 users at 10 dB |
| HARQ | throughput $(1 - p^M)/\sum_{k<M}p^k$ | 0.9 at $p$ = 0.1 |
| 3GPP releases | Rel-15 frozen 2019; Rel-19 complete Dec 2025; Rel-20 Stage 3 Mar 2027 | [R-291] |

### [17-13 · Computer Networks Fundamentals](../courses/17-communication-systems/chapters/17-13-computer-networks-fundamentals.md)

| Quantity | Value | Note |
|---|---|---|
| Header sizes | Ethernet 14 + 4 FCS; IPv4 20; IPv6 40; TCP 20; UDP 8 bytes | [R-292], [R-293] |
| Ethernet payload | 46–1500 bytes; + 8 preamble/SFD + 12 inter-frame gap on the wire | [R-292] |
| Wire efficiency | 94.9% for 1460-byte TCP/IPv4 payloads | |
| Minimum-frame rate | 14.88 Mpps at 10 Gb/s | 84 bytes per frame |
| IPv4 subnet | $2^{32-p} - 2$ usable hosts | private: 10/8, 172.16/12, 192.168/16 |
| IPv6 | 128-bit addresses; minimum link MTU 1280 bytes | [R-293] |
| TCP window | ≤ 65 535 bytes unscaled; scale shift ≤ 14 (window < $2^{30}$) | [R-294] |
| Window-limited rate | $W/\text{RTT}$; BDP = $R \times$ RTT | |
| Loss-limited rate | $(\text{MSS}/\text{RTT})\sqrt{3/(2p)}$ | AIMD |
| RTO | SRTT + 4 RTTVAR, at least 1 s | RFC 6298 [R-294] |
| M/M/1 | $T = 1/(\mu - \lambda)$; 5× service time at 80% load | |

## [18 · Embedded Systems and Microcontrollers](../courses/18-embedded-systems-and-microcontrollers/README.md)

### [18-01 · Microcontroller Architecture](../courses/18-embedded-systems-and-microcontrollers/chapters/18-01-microcontroller-architecture.md)

| Quantity | Value | Note |
|---|---|---|
| Cortex-M address space | 4 GiB; code at 0x0000 0000, SRAM at 0x2000 0000, peripherals at 0x4000 0000, core registers at 0xE000 0000 | Armv7-M/Armv8-M default map |
| Reset sequence | word 0 → MSP, word 1 → PC (LSB = 1 for Thumb) | vector table at address 0 by default |
| Bit-band alias | base + 32 × byte offset + 4 × bit | Armv7-M only; 1 MiB regions |
| Flash wait states | $\lceil f\,t_{acc}\rceil - 1$; bands of 25–50 MHz per wait state on current parts | more at lower voltage; SAM D5x, RA6M5 [R-300] |
| Interrupt entry | 12 cycles on Cortex-M3/M4 (6 when tail-chaining), 15 on M0+, at zero wait states | Arm TRMs [R-298]; 18-03 |
| Core performance | 2.46 (M0+), 3.54 (M4), 4.10 (M33), 5.29 (M7) CoreMark/MHz | Arm, from zero-wait-state memory [R-297] |
| AHB peak | 4 bytes per clock per slave port | APB: ≥ 2 cycles per access |
| RTC crystal | 32 768 Hz = $2^{15}$ Hz | 1 Hz from a 15-bit counter |
| USB full-speed clock tolerance | ±0.25% (2500 ppm) | USB 2.0 §7.1.11 |
| Internal RC accuracy | about ±1% after trim | fine for a UART, not for USB or radios |

### [18-02 · Bare-Metal C and the Build Toolchain](../courses/18-embedded-systems-and-microcontrollers/chapters/18-02-bare-metal-c-and-toolchain.md)

| Quantity | Value | Note |
|---|---|---|
| Flash used | text + data | `data` = initial values of initialized variables |
| SRAM used | data + bss + stack + heap | heap often zero in embedded firmware |
| Vector table | 4 bytes per entry; 16 system entries + one per interrupt | word 0 = initial SP, word 1 = reset handler (odd: Thumb) |
| Exception frame | 32 bytes (8 words); 104 bytes (26 words) with FPU state | Armv7-M; one per nesting level |
| Field positions in a 32-bit register | 528 (lsb, width) pairs | the lab tests all of them |
| Code size by optimization level | −41% from `-O2` to `-Oz` (lab firmware, clang 18) | real firmware: usually less |
| Startup time | (copy words × c + zero words × c) / reset clock | milliseconds for tens of KiB at a few MHz |
| Dual-image updates | usable code space < half the flash | 18-08 |

### [18-03 · Interrupts, Exceptions and Timers](../courses/18-embedded-systems-and-microcontrollers/chapters/18-03-interrupts-exceptions-timers.md)

| Quantity | Value | Note |
|---|---|---|
| Interrupt entry | 12 cycles (M3, M4), 15 (M0+, M23), 12–14 (M7) | zero wait states [R-298] |
| Return and tail-chain | 12 and 6 cycles (M3, M4) | [R-298] |
| Interrupts per NVIC | up to 496 (Armv7-M/Armv8-M architecture), 32 (Armv6-M) | cores and chips implement fewer [R-304] |
| Implemented priority bits | 3–8 (Armv7-M); 2 (Armv6-M); 4 on STM32F4 | lower number = more urgent [R-304] |
| Stack frame | 8 words (32 bytes); 26 words (104 bytes) with FP state | 18-02 §3.7 |
| SysTick | 24-bit down-counter; 1 ms at 168 MHz = reload 167 999 | longest period $2^{24}/f$ |
| PWM trade-off | $f_{PWM} \cdot 2^{bits} = f_{clk}$ (edge-aligned) | center-aligned: half |
| Capture arithmetic | difference modulo $2^N$ | one wrap is harmless |
| Watchdog timeout | prescaler × reload / $f_{LSI}$ | design to the shortest; budget for the longest |

### [18-04 · DMA and Data Movement](../courses/18-embedded-systems-and-microcontrollers/chapters/18-04-dma-and-data-movement.md)

| Quantity | Value | Note |
|---|---|---|
| Load with one interrupt per item | $r\,c_{item}/f$ | 18-03 |
| Load with DMA blocks | $(r/N)\,c_{block}/f$ | $N$ items per block |
| Ping-pong bound | $N \ge (a + L)f_s/(1 - bf_s)$ | $k$ buffers: $N \ge \max\big((a + L)f_s/((k - 1) - bf_s),\ af_s/(1 - bf_s)\big)$ |
| Worst latency of a block scheme | $N/f_s + L + a + bN$ | first sample of a block |
| Circular buffer | $S > r_{bytes}\,t_{service}$; head $= S -$ remaining | power-of-two sizes |
| Contention | stall ≈ $p\rho$ | removed by separate banks |
| DMA controllers | up to 32 channels (SAM D5x, PL230); 2 × 8 streams (STM32F4) | [R-305] |
| Cache line (Cortex-M7) | 32 bytes | align and pad DMA buffers |

### [18-05 · Peripherals and Serial Buses: GPIO, UART, SPI, I²C](../courses/18-embedded-systems-and-microcontrollers/chapters/18-05-gpio-uart-spi-i2c.md)

| Quantity | Value | Note |
|---|---|---|
| UART 8N1 | 10 bits per byte, 80% efficiency | 115 200 baud = 11 520 bytes/s |
| UART tolerance (ideal 16× receiver) | sender −5.3% to +4.6% | real receivers: keep total within ±2% [R-306] |
| SPI modes | CPOL = idle clock level, CPHA = sample on first (0) or second (1) edge | no formal standard [R-306] |
| I²C speeds | 100 k, 400 k, 1 M, 3.4 Mbit/s (+5 Mbit/s write-only) | Sm, Fm, Fm+, Hs, UFm [R-306] |
| I²C rise time, capacitance | 1000/300/120 ns; 400/400/550 pF | Sm/Fm/Fm+ [R-306] |
| I²C sink | 0.4 V at 3 mA (20 mA Fm+); Fm also 0.6 V at 6 mA | sets $R_{p,min}$ |
| Rise time 30–70% | $0.8473R_pC_b$ | from the RC solution |
| I3C | 12.5 MHz SCL, about 11 Mbit/s SDR; about 30 Mbit/s HDR | [R-306] |
| CMOS input thresholds | $V_{IH(min)} = 0.7V_{DD}$, $V_{IL(max)} = 0.3V_{DD}$ | typical |
| GPIO limits (example part) | 6 mA per standard pin, 80 mA total, ±2 mA injection | TI MSPM0G350x [R-306] |

### [18-06 · Analog Interfaces: ADC, DAC and PWM](../courses/18-embedded-systems-and-microcontrollers/chapters/18-06-adc-dac-pwm.md)

| Quantity | Value | Note |
|---|---|---|
| SQNR of an ideal ADC | $6.02N + 1.76$ dB | full-scale sine; 74.0 dB at 12 bits |
| 12-bit LSB at 3.3 V | 0.806 mV | |
| Settling for 12 bits | 9.01 time constants | $\ln 2^{13}$ |
| Typical MCU S/H | a few pF, 0.5–several kΩ switch | 3.3 pF and 0.5 kΩ on MSPM0G350x [R-307] |
| S/H as a resistor | $1/(fC_{sh})$ | 3.03 MΩ for 3.3 pF at 100 kHz |
| Averaging gain | ½ bit per doubling, 1 bit per ×4 | needs ≳ 0.5 LSB rms noise |
| ZOH droop | −0.91 dB at $f_s/4$, −3.92 dB at $f_s/2$ | $\operatorname{sinc}(f/f_s)$ |
| PWM ripple (RC, $T \ll \tau$) | $V_HD(1 - D)T/\tau$ | worst at $D = \frac12$ |
| PWM frequency | $f_{clk}/2^N$ | 62.5 kHz at 10 bits from 64 MHz |
| MCU ADC example | 12-bit, 4 Msps, ENOB 11.1 (12.5 with 16× averaging) | TI MSPM0G350x [R-307] |
| MCU ADC example | "12-bit with 8.7 ENOB", 500 ksps | Raspberry Pi RP2040 [R-307] |

### [18-07 · RTOS Concepts](../courses/18-embedded-systems-and-microcontrollers/chapters/18-07-rtos-concepts.md)

| Quantity | Value | Note |
|---|---|---|
| Liu & Layland bound | 1, 0.828, 0.780, … → 0.693 | $n(2^{1/n} - 1)$ for $n$ = 1, 2, 3, ∞ |
| Hyperbolic bound | $\prod (U_i + 1) \le 2$ | sufficient, sharper |
| EDF (one core, implicit deadlines) | $U \le 1$ | necessary and sufficient |
| Kernel overhead | $f_{tick}c_{tick} + n_{sw}c_{sw}$ | 0.4% in Example 18-07.1 |
| Cortex-M switch | saves R4–R11 (+ S16–S31) in PendSV | hardware stacks the rest |
| Exception frame on a task stack | 32 bytes (104 with FPU) | 18-02 §3.7 |
| Queue slots | $\lfloor S/P \rfloor + 1$ | stall $S$, period $P$ |
| FreeRTOS | V11.3.3 (Oct 2026); 202604 LTS | [R-308] |
| Zephyr | 4.5.0 (Oct 2026); LTS 3.7, next LTS 4.6 (Apr 2027) | [R-308] |

### [18-08 · Boot, Bootloaders and Firmware Update](../courses/18-embedded-systems-and-microcontrollers/chapters/18-08-boot-and-firmware-update.md)

| Quantity | Value | Note |
|---|---|---|
| Largest image, two slots | $(F - B)/2$ | minus scratch and trailers |
| Installation time | $n\,k\,(t_{erase} + t_{program})$ | $k$ = 1 overwrite, 3 swap via scratch |
| Scratch erases per update | one per image sector | wear |
| In-place update | unbootable for the whole write | never without a recovery path |
| MCUboot | v2.5.0 (Oct 2026); overwrite, swap (scratch, move, offset), direct-xip, ram-load | [R-309] |
| IETF SUIT | RFC 9019 (2021), RFC 9124 (2022), manifest draft -38 in RFC Editor queue (Nov 2026) | [R-309] |
| Arm PSA Firmware Update API | 1.0.1 (Sep 2025) | [R-309] |

### [18-09 · Ultra-Low-Power Design](../courses/18-embedded-systems-and-microcontrollers/chapters/18-09-ultra-low-power-design.md)

| Quantity | Value | Note |
|---|---|---|
| Dynamic power | $C_{sw}V^2f$ | energy per cycle $\propto V^2$ |
| Average current | $I_{sleep} + \sum I_kt_k/T$ | |
| Battery life | $\eta Q/(\bar I + I_{sd})$ | |
| Break-even | $Q_{tr}/(I_{shallow} - I_{deep})$ | |
| 1 mAh | 3.6 C | |
| LDO efficiency | at most $V_{out}/V_{in}$ | 48.6% from 3.7 to 1.8 V |
| Pulse droop | $IR_{int}(1 - e^{-t/R_{int}C})$ | |
| ULP MCU standby (RTC, SRAM kept) | about 0.5–1.5 µA typical at 25 °C | rises steeply with temperature [R-310] |
| BLE radio (0 dBm) | about 5 mA RX or TX with DC/DC | TI CC2340R5 [R-310] |
| CR2032 | 225 mAh at 0.2 mA | Panasonic [R-310] |

### [18-10 · Sensors: IMU, PPG, MEMS and Audio](../courses/18-embedded-systems-and-microcontrollers/chapters/18-10-sensors.md)

| Quantity | Value | Note |
|---|---|---|
| Static deflection | $a/\omega_0^2$ | 15.5 nm per g at 4 kHz |
| Differential capacitance | $2C_0x/d$ | |
| Thermomechanical noise | $\sqrt{4k_BT\omega_0/(mQ)}$ | |
| rms from density | $n\sqrt{B}$ | |
| Coriolis acceleration | $2\Omega v$ | |
| Angle random walk | $60N/\sqrt2$ °/√h for a one-sided $N$ in °/s/√Hz (the shortcut $60N$ assumes two-sided) | |
| Complementary filter | $\tau = \alpha\Delta t/(1 - \alpha)$; bias error $b\tau$ | |
| PPG perfusion index | around 1% at the wrist | lower when cold |
| 94 dB SPL | 1 Pa rms | microphone reference |
| Barometric gradient | about −12 Pa/m near sea level | 1 Pa ≈ 8 cm |
| MEMS accelerometer noise | about 150–200 µg/√Hz | BMI270, BMI323 [R-311] |
| MEMS gyroscope noise | about 0.007 °/s/√Hz | BMI270, BMI323 [R-311] |
| IMU current | about 10 µA (accelerometer, low power) to about 1 mA (with gyroscope) | [R-311] |
| Digital microphone | −26 dBFS, about 65 dBA SNR, a few hundred µA | ICS-43434 [R-311] |

### [18-11 · Hardware Security](../courses/18-embedded-systems-and-microcontrollers/chapters/18-11-hardware-security.md)

| Quantity | Value | Note |
|---|---|---|
| Brute force | $(2^n + 1)/2$ guesses on average | 128 bits is out of reach |
| Timing leak | at most 256 guesses per leaked byte | |
| CPA traces | $N \approx (z/\rho)^2$, $\rho = \sqrt{2/(2 + \sigma^2)}$ | Hamming-weight leakage |
| Repetition code | $P_{bit} = \sum_{k > n/2}\binom{n}{k}p^k(1 - p)^{n - k}$ | |
| SRAM PUF bit errors | about 3–5% at enrollment temperature, up to 20.5% at extremes | [R-312] |
| Glitch time to success | $1/(pr)$; redundant checks $\approx p^2$ | |
| PSA Certified | Levels 1–4; 319 certifications (Nov 2026) | [R-312] |
| EU CRA | in force 10 Dec 2024; reporting from 11 Sep 2026; main obligations 11 Dec 2027 | [R-312] |

## [19 · Digital VLSI Design](../courses/19-digital-vlsi-design/README.md)

### [19-01 · The CMOS Inverter: Static Characteristics](../courses/19-digital-vlsi-design/chapters/19-01-cmos-inverter-static.md)

| Quantity | Value | Notes |
|---|---|---|
| Static CMOS output levels | $V_{OH} = V_{DD}$, $V_{OL}$ = 0 | No static current except leakage |
| Symmetric switching threshold | $V_{DD}/2$ | Needs $k_n = k_p$ and matched thresholds |
| Symmetric noise margins | $(3V_{DD} + 2V_{TH})/8$ each | Square law, λ = 0; about 40–45% of $V_{DD}$ |
| Long-channel symmetric sizing | $W_p/W_n = \mu_n/\mu_p$, about 2–3 | Less with velocity saturation |
| Gain at $V_M$ | $\approx 2/(\lambda V_{ov})$, tens to a few hundred | Symmetric, square law |
| $\sigma_{V_M}$ | $\sigma_{VT}/\sqrt2$ | Symmetric, independent thresholds |
| Thermal voltage $kT/q$ | 25.85 mV at 300 K | |
| Minimum supply for gain | $2V_T\ln(1 + n)$, 36–50 mV | Subthreshold; practical designs need a few hundred mV |

### [19-02 · The CMOS Inverter: Dynamic Behavior and Delay](../courses/19-digital-vlsi-design/chapters/19-02-cmos-inverter-dynamic.md)

| Quantity | Value | Notes |
|---|---|---|
| RC step to 50% | $\ln 2\,RC$ = 0.69 $RC$ | |
| $R_{eq}$ | $\approx 3V_{DD}/(4I_{sat})$ | Average of $V/I$ over the transition |
| Intrinsic delay | $t_{p0} = 0.69R_{eq}C_{int}$, independent of size | |
| FO4 delay | $t_{p0}(1 + 4/\gamma)$: $5t_{p0}$ to $9t_{p0}$ | γ = $C_{int}/C_g$ from 1 (textbook convention) to 0.5 (the FO1/FO4 rule) |
| Ring oscillator | $f = 1/(2Nt_p)$ | $t_p$ here includes input-slope effects |
| EDP-optimal supply | $3V_{TH}/(3 - \alpha)$: 1.5–3 $V_{TH}$ | α from 1 to 2 |

### [19-03 · Combinational Logic Families](../courses/19-digital-vlsi-design/chapters/19-03-logic-families.md)

| Quantity | Value | Notes |
|---|---|---|
| Static gate transistor count | $2N$ | $N$ inputs |
| Input capacitance relative to inverter, $\mu$ = 2 | NAND2 4/3, NAND3 5/3, NOR2 5/3, NOR3 7/3 | Logical effort (19-04) |
| Elmore estimate | $0.69\sum_m C_mR_{km}$ | Exact for one RC; up to about 9% low for long ladders |
| NAND-$N$ stack Elmore constant | $RcN(N - 1)/2 + R[(1 + \mu)cN + C_{ext}]$ | Quadratic internal term plus linear output term |
| Chain of $n$ equal RC sections | $RC\,n(n + 1)/2$ | Quadratic in length |
| Pseudo-NMOS ratio | $k_n/k_p \gtrsim 4$ | For $V_{OL}$ near 0.1 V |
| Optimal buffer spacing | $m_{opt} \approx 1.7\sqrt{t_{buf}/RC}$ | TG chains and wires |
| Charge-sharing boundary | $C_a/C_L = V_{TN}/(V_{DD} - V_{TN})$ | No body effect |
| Dynamic hold time | $C_L\Delta V/I_{leak}$ | Sets a minimum clock |

### [19-04 · Transistor Sizing and Logical Effort](../courses/19-digital-vlsi-design/chapters/19-04-sizing-and-logical-effort.md)

| Quantity | Value | Notes |
|---|---|---|
| Stage delay | $d = gh + p$ | In units of $\tau = 0.69RC_{inv}$ |
| $g$ of NAND2, NOR2, NAND3, NOR3 | 4/3, 5/3, 5/3, 7/3 | $\mu$ = 2 |
| Parasitic delay of $n$-input NAND/NOR | $np_{inv}$, $p_{inv} \approx 1$ | Ignores internal nodes |
| Minimum path delay | $NF^{1/N} + P$, $F = GBH$ | Equal stage efforts |
| Best stage effort | ρ = 3.59 ($p_{inv}$ = 1); rule of thumb 4 | Within 9% for 2.4–6 |
| Best number of stages | $\log_\rho F \approx \log_4 F$ | Round to polarity |
| FO4 delay | 5τ | One optimally loaded stage |

### [19-05 · Interconnect](../courses/19-digital-vlsi-design/chapters/19-05-interconnect.md)

| Quantity | Value | Notes |
|---|---|---|
| Bulk Cu resistivity | 1.7 µΩ·cm | Narrow lines up to about 10× higher at 10 nm ([R-315]) |
| Wire capacitance per length | about 0.2 fF/µm | Roughly constant across nodes |
| Distributed line 50% delay | 0.38 $RC$ | Lumped 0.69 $RC$, Elmore 0.35 $RC$ |
| Driver–wire–load delay | $0.69R_d(C_w + C_L) + R_w(0.38C_w + 0.69C_L)$ | |
| Optimal repeaters | $k = \sqrt{0.38R_wC_w/(0.69R_0C_0)}$, $h = \sqrt{R_0C_w/(R_wC_0)}$ | |
| Repeated delay | $2.41\sqrt{R_0C_0\,rc}\,L$ | Linear in $L$ |
| Floating victim | $\Delta V_{agg}C_c/(C_c + C_g)$ | |
| Miller coupling factor | 0, 1 or 2 | Same, quiet, opposite |

### [19-06 · Power and Low-Power Design](../courses/19-digital-vlsi-design/chapters/19-06-power-and-low-power-design.md)

| Quantity | Value | Notes |
|---|---|---|
| Energy per full switching cycle | $CV_{DD}^2$ | Half dissipated charging, half discharging |
| Dynamic power | $\alpha CV_{DD}^2f$ | α = 1 for clocks |
| Short-circuit power | $(\beta/12)(V_{DD} - 2V_{TH})^3\tau/T$ | Upper bound; zero for $V_{DD} < 2V_{TH}$ in the square-law model |
| Subthreshold slope | $nV_T\ln 10$ ≈ 60 $n$ mV/decade at 300 K | |
| Leakage vs threshold | ×10 per $S$ of threshold lowering | |
| Stack effect | ~10× or more, mostly from DIBL | |
| Minimum-energy point | $L_de^{-x}(x-2) = 2\alpha$, $x = V/(nV_T)$ | Typically 0.2–0.4 V |
| Power-gating break-even | $E_{wake}/P_{leak,saved}$ | |

### [19-07 · Sequential Circuits, Timing and Clocking](../courses/19-digital-vlsi-design/chapters/19-07-sequential-timing-and-clocking.md)

| Quantity | Value | Notes |
|---|---|---|
| Setup constraint | $T_c \ge t_{pcq} + t_{pd} + t_{setup} - \delta + t_{jitter}$ | δ = capture − launch clock |
| Hold constraint | $t_{ccq} + t_{cd} \ge t_{hold} + \delta$ | Independent of $T_c$ |
| Pipelined cycle | $t_L/N + t_o$ | Latency $t_L + Nt_o$ |
| Time borrowing | up to $T_c/2 - t_{setup}$ | Two-phase, 50% duty |
| Metastable resolution | $\Delta v = \Delta v_0e^{t/\tau}$, $\tau = C/g_m$ | |
| MTBF | $e^{t_r/\tau}/(T_0f_{clk}f_{data})$ | ×$e^{T_c/\tau}$ per extra stage |

### [19-08 · SRAM Design](../courses/19-digital-vlsi-design/chapters/19-08-sram-design.md)

| Quantity | Value | Notes |
|---|---|---|
| Cell transistors | 6 (2 P, 2 N, 2 A) | 8T adds a read port |
| Cell ratio $k_N/k_A$ | ≈ 1.5–2.5 | Read stability |
| Pull-up ratio $k_P/k_A$ | ≲ 0.67 here (conservative); W/L rules near 1–1.5 | Writability; the PMOS's lower mobility explains the difference |
| Bitline swing at sensing | ≈ 100 mV | Set by sense-amplifier offset |
| Bitline time | $C_{BL}\Delta V_{BL}/I_{cell}$ | |
| Design margin | ≈ 6σ | Billions of cells |
| Array yield | $e^{-NQ(\mu/\sigma)}$ | Before repair |

### [19-09 · Layout, Design Rules and Standard Cells](../courses/19-digital-vlsi-design/chapters/19-09-layout-and-standard-cells.md)

| Quantity | Value | Notes |
|---|---|---|
| Contacted vs uncontacted pitch | 8λ vs 5λ | This chapter's illustrative rules |
| Euler path exists | 0 or 2 odd-degree nodes | Connected graph |
| SKY130 minimum poly width | 0.150 µm | [R-314] |
| SKY130 `hd` site | 0.46 × 2.72 µm, 9 met1 tracks | [R-317] |
| SKY130 `hd` routed density | 160 kGates/mm² or better (`hdll`: 120) | [R-317] |
| Core area | $\sum A_{cells}/u$ | $u$ ≈ 0.6–0.8 |

### [19-10 · The ASIC Flow I: Synthesis and Static Timing Analysis](../courses/19-digital-vlsi-design/chapters/19-10-synthesis-and-sta.md)

| Quantity | Value | Notes |
|---|---|---|
| Bilinear interpolation | $(1 - t_s)(1 - t_C)D_{00} + (1 - t_s)t_CD_{01} + t_s(1 - t_C)D_{10} + t_st_CD_{11}$ | Exact for $a + bs + cC + dsC$ |
| Effective resistance | slope of delay vs load, ns/pF = kΩ | SKY130 `inv_1`, tt: 5.64 kΩ rise, 3.33 kΩ fall |
| SKY130 `inv_1` delay, tt | about 54–76 ps at 0.08 ns slew and 5 fF | Example 1 (rise 75.9, fall 53.4) |
| Slow-corner penalty, SKY130 `inv_1` | 1.33× (rise) and 1.62× (fall), ss_100C_1v60 vs tt | Same slew and load as Example 1; lab Part 1 |
| Setup slack | $T_c + L_2 - t_{\text{setup}} - U - (L_1 + t_{pcq} + t_{pd})$ | |
| Hold slack | $L_1 + t_{ccq} + t_{cd} - (L_2 + t_{\text{hold}} + U)$ | No $T_c$ |
| Output-port required time | $T_c - d_{\text{out}}$ | |
| CRPR credit | $(k_L - k_E) \times$ common clock delay | |
| Path sigma | $\sigma\sqrt{N + N(N-1)\rho}$ | $\sqrt{N}\sigma$ if independent |
| Multicycle pairing | setup $N$, hold $N - 1$ | |
| Paths through $n$ diamonds | $2^n$ | Nodes grow as $n$ |
| SKY130 `sky130_fd_sc_hd` corners | 16 (6 ff, 8 ss, 2 tt) | As of Nov 2026 [R-318] |
| Open-flow SKY130 reference clocks | 1.1–8.0 ns, no uncertainty or derate | OpenROAD-flow-scripts, Nov 2026 [R-318]; not signoff settings |
| Example derates in open tools | ±10 % (OpenSTA example), ±5 % (one SKY130 design) | Examples, not norms [R-318] |
| Signoff scenarios at FinFET nodes | "hundreds" | [Industry estimate], 2015 [R-318] |

### [19-11 · The ASIC Flow II: Floorplan, Place and Route, Signoff](../courses/19-digital-vlsi-design/chapters/19-11-place-route-signoff.md)

| Quantity | Value | Notes |
|---|---|---|
| Core area | $A_{\text{cells}}/u$ | Rows rounded up |
| Strap IR drop | $IR/8$ (both ends), $IR/2$ (one end) | Uniform load; $\propto L^2$ |
| Largest feed spacing | $\sqrt{8\Delta V_{\max}/(ri)}$ | |
| HPWL | $\Delta x + \Delta y$ | Exact for 2–3 pins, a lower bound otherwise |
| Tree lengths | HPWL ≤ RSMT ≤ RMST ≤ 1.5 RSMT | Hanan; Hwang |
| Zero-skew tap | $x = \dfrac{t_2 - t_1 + rL(C_2 + cL/2)}{r(C_1 + C_2 + cL)}$ | Elmore |
| H-tree, $k$ levels | $4^k$ sinks; path $D(1 - 2^{-k})$; total $1.5D(2^k - 1)$ | Square of side $D$ |
| Routed-net 50 % delay | $R_{\text{eff}}(C_w + C_L) + R_w(0.38C_w + 0.69C_L)$ | $R_{\text{eff}}$ = Liberty slope = ln 2 × $R_{\text{eq}}$ |
| Elmore constant of a net | $R_{\text{eq}}(C_w + C_L) + R_w(C_w/2 + C_L)$ | Upper bound; use for balancing |
| Clock power | $C_{\text{clk}}V_{DD}^2f$ | Activity 1 |
| SKY130 metal stack | li1 plus 5 metals; 0.125 Ω/□ (met1, met2), 0.047 (met3, met4), about 0.029 (met5) | As of Nov 2026 [R-319] |
| SKY130 minimum width / pitch | 0.14/0.34 µm (met1); 0.30/0.68 (met3); 1.6/3.4 (met5) | Tech LEF and DRC manual [R-319] |
| SKY130 EM limit (average) | 2.8 mA/µm (met1, met2), 6.8 (met3, met4), 10.17 (met5) at 90 °C | Tech LEF comments only [R-319] |
| SKY130 antenna limit, metal 1 | ratio 400 without a diode, on sidewall area (perimeter × thickness) | DRC manual [R-319]; see 19-09 §3.5 |
| Open-flow SKY130 targets | core utilization 35–50 %, placement density 0.60 | ORFS reference designs, Nov 2026 [R-319] |

### [19-12 · Design for Test: Scan, BIST and ATPG](../courses/19-digital-vlsi-design/chapters/19-12-design-for-test.md)

| Quantity | Value | Notes |
|---|---|---|
| Defect level | $1 - Y^{1-T} \approx (1 - T)(-\ln Y)$ | Williams–Brown |
| Stuck-at faults | $2 \times$ lines (stems + fanout branches) | Collapsing removes equivalents |
| Tests for an $n$-input AND or NAND | $n + 1$ | |
| Random patterns to detect with confidence $P_d$ | $\ln(1 - P_d)/\ln(1 - p)$ | $p = 2^{-k}$ for $k$ required inputs |
| Scan test cycles | $P(L + 1) + L$ | $L = \lceil F/C \rceil$ |
| Scan test data | $\approx 2FP$ bits | Before compression |
| Compression | ≈ internal chains / scan pins | Same pattern count |
| Maximal LFSR period | $2^n - 1$ | Primitive polynomial |
| MISR aliasing | $\approx 2^{-n}$ | Exactly $(2^{n(m-1)} - 1)/(2^{nm} - 1)$ if every nonzero error stream is equally likely |
| March C− | $10n$ operations | |
| Scan gate overhead (classic estimate) | $4n_{\text{sff}}/(n_g + 10n_{\text{sff}})$; 6.7 % for 100k gates, 2k flip-flops | 2001 teaching data [R-320] |
| Cost of test | under 2–3 % of IC revenue | ITRS 2015 [R-320] |
| Compression in production | "often 100X or more" | Vendor claim, Nov 2026 [R-320] |
| ISO 26262 hardware metrics (ASIL B/C/D) | single-point ≥90/97/99 %; latent ≥60/80/90 % | In-field diagnostic coverage, not test coverage [R-320] |
| Silent data corruption | "a few mercurial cores per several thousand machines" (Google 2021) | [R-320] |

### [19-13 · Verification: Simulation, UVM, Formal and Emulation](../courses/19-digital-vlsi-design/chapters/19-13-verification-methods.md)

| Quantity | Value | Notes |
|---|---|---|
| Random samples to fill $n$ equal bins | $nH_n \approx n\ln n + 0.577n + \tfrac12$ | 54 for 16 bins (08-05) |
| Unequal bins | $E[T] = \sum_{S \ne \emptyset} (-1)^{\lvert S\rvert+1}/p(S) \ge 1/p_{\min}$ | The rarest bin dominates |
| Random detection of a bug that needs $m$ specific input bits | $p = 2^{-m}$; 99 % confidence needs about $4.6 \times 2^{m}$ vectors | Formal finds it directly |
| Round-robin worst wait | $N - 1$ grants to others | Fixed priority: unbounded |
| ROBDD of $\sum_{i=1}^n x_iy_i$ | $2n$ (interleaved) vs $2^{n+1} - 2$ (separated) | Order decides size |
| ROBDD of an adder's sum bit $i$ (interleaved) | $3i + 3$ nodes | Multipliers: exponential for every order |
| BMC completeness | bound ≥ diameter | Otherwise "no bug within $k$" only |
| k-induction | base: BMC to depth $k - 1$; step over all states | Fails on counterexamples to induction |
| Boot of an OS (illustrative $2 \times 10^9$ cycles) | 231 days at 100 Hz, 33 min at 1 MHz, 100 s at 20 MHz | Simulation, emulation, FPGA prototype |

## [20 · Analog and Mixed-Signal IC Design](../courses/20-analog-and-mixed-signal-ic-design/README.md)

### [20-01 · Analog Design Fundamentals in Nanometer CMOS](../courses/20-analog-and-mixed-signal-ic-design/chapters/20-01-analog-design-fundamentals-gm-id.md)

| Quantity | Typical value | Note |
|---|---|---|
| Weak-inversion limit of $g_m/I_D$ | $1/(nV_T)$: **28** to **32** S/A at 300 K for $n$ = 1.4 to 1.2 | Physics; falls as $1/T$ |
| Bipolar $g_m/I_C$ | 38.7 S/A at 300 K | The MOSFET's ceiling without the $1/n$ divider |
| $g_m/I_D$ at $IC$ = 1 | 62% of the limit | Center of moderate inversion |
| Working range of $g_m/I_D$ | about 5 to 25 S/A | Low for speed, high for power |
| Square-law error | "20–60%" in strong inversion; "a factor of two or even more" in moderate inversion | Jespers and Murmann [3] |
| $V_{DS,sat}$ | about $4V_T$ ≈ **103** mV in weak inversion; about $V_P = V_{ov}/n$ in strong | Weak inversion: current within 2% of saturation at $V_T\ln 50$ = **3.91** $V_T$. The $n = 1$ square law says $V_{ov}$ |
| Velocity-saturated $f_T$ limit | $3v_{sat}/(4\pi L)$: 127 GHz at 0.15 µm (T130 model) | Real devices lower: overlap and wiring capacitance |
| Measured peak NMOS $f_T$, 32 nm to 12 nm | 230 to 445 GHz (most above 300 GHz) | Peak current density, RF layout; as of Nov 2026 [R-322] |
| IRDS intrinsic delay $CV/I$ | 1.061 ps (2024) to 0.624 ps (2039) | NMOS, FO3 load [R-314] |
| FinFET self-gain $g_m/g_{ds}$ | 40 (N) and 34 (P) in a 14 nm FinFET process | Single company; bias not stated [R-322] |
| SKY130 thin-oxide NMOS | $L_{min}$ = 0.15 µm, $t_{ox}$ = 4.148 nm ($C_{ox}$ ≈ **8.3** fF/µm²), BSIM4 4.5 models | Open PDK [R-322]; close to T130's 8.6 fF/µm² |

### [20-02 · Two-Stage Op-Amp Design](../courses/20-analog-and-mixed-signal-ic-design/chapters/20-02-two-stage-op-amp-design.md)

| Quantity | Typical value | Note |
|---|---|---|
| Two-pole PM at $p_2 = 1.5\,\omega_u$ | 60.0° (exact) | crossover at 0.866 $\omega_u$ |
| PM at $p_2 = 2\,\omega_u$ | 65.5° | a sensible design target |
| Fastest 0.1% settling of a two-pole loop | about 74° PM, 3.44/$\omega_u$ | 6.91/$\omega_u$ for a single pole |
| SR / $\omega_u$ | $2/(g_m/I_D)_1$: **0.111** V at 18 S/A; $2nV_T$ = **67.2** mV in weak inversion | 12-08 for bipolar and square law |
| NMC Butterworth GBW | $g_{m3}/(4C_L)$ | half a two-stage op-amp's at equal output $g_m$ |
| Second-stage share of current (Miller) | 88% in Example 20-02.3 | set by $p_2$ (Miller) or by slew (indirect) |
| Op-amp figure of merit $f_uC_L/I$ | 566 MHz·pF/mA for Example 20-02.3; **4.4 × 10⁴** to **6.8 × 10⁶** for published large-load multistage OTAs | definitions vary (per mA or per mW) [R-324] |
| Commercial precision CMOS op-amps (as of Nov 2026) | 90 kHz at 2.9 µA (OPA379) to 5.5 MHz at 760 µA (OPA376) | typical datasheet values [R-325] |
| Commercial high-speed amplifiers (as of Nov 2026) | 50 MHz at 592 µA (OPA837); 850 MHz, 1500 V/µs at 10.1 mA (THS4541 FDA) | typical datasheet values [R-325] |
| Datasheet DC PSRR (as of Nov 2026) | 100–120 dB (1–10 µV/V) | DC only; it falls with frequency (§3.10) [R-325] |

### [20-03 · Bandgap and Voltage References](../courses/20-analog-and-mixed-signal-ic-design/chapters/20-03-bandgap-references.md)

| Quantity | Typical value | Note |
|---|---|---|
| $V_{BE}$ temperature coefficient | about −1.8 to −2.1 mV/K | depends on current density and bias (Problem 20-03.1) |
| PTAT slope $(k/q)\ln N$ | 179.2 µV/K ($N$ = 8), 273.9 µV/K ($N$ = 24) | exact |
| Bandgap output ("magic voltage") | about 1.24–1.25 V | 1.2526 V for T130; 1.239–1.242 V from Tsividis's fits [1] |
| Curvature-limited box TC, first order | about 9 ppm/K (−40 to 125 °C), 4 ppm/K (0 to 70 °C) | T130, η − 1 = 2 |
| Untrimmed spread | several tenths of a percent to about 1% | ±0.71% over seven samples (Chen et al., 2021); 0.5–1.0% initial error for bandgap products (TI, 1999) [R-326], [R-327] |
| Single-trim CMOS bandgaps (as of Nov 2026) | ±0.15% to +0.02%/−0.12% (3σ), −40 to 125 °C | published JSSC results [R-326] |
| Commercial precision references (as of Nov 2026) | ±0.025–0.05% initial, 2–3 ppm/°C | TI REF7025, REF5025 data sheets [R-327] |
| Commercial low-power references (as of Nov 2026) | ±0.05%, 6–12 ppm/°C at 72 µA to 0.65 µA | TI REF3425, REF35250 [R-327] |
| Long-term drift | about 20–40 ppm in the first 1000 h (REF5025 22 ppm, REF3425 25 ppm, REF35250 40 ppm) | data-sheet values, package dependent [R-327] |

### [20-04 · Low-Dropout Regulators](../courses/20-analog-and-mixed-signal-ic-design/chapters/20-04-ldo-regulators.md)

| Quantity | Typical value | Note |
|---|---|---|
| Efficiency bound | $V_{out}/V_{in}$ | exact; times the current efficiency $I_L/(I_L + I_Q)$ |
| PMOS LDO dropout at rated current (as of Nov 2026) | about 100–300 mV | TI TPS7A20: 140 mV max at 300 mA; TLV755P: 215 mV max at 500 mA; TPS7A83A: 200 mV max at 2 A [R-330] |
| Quiescent current of discrete LDOs (as of Nov 2026) | 25 nA to 15 mA | TPS7A02 nanopower (25 nA typ) to TPS7A94 ultra-low-noise (15 mA ground current) [R-330] |
| PSRR of good discrete LDOs (as of Nov 2026) | 55–110 dB at 1 kHz; about 45–52 dB at 1 MHz | TPS7A20: 45 dB at 1 MHz (20 mA); TPS7A94: 51 dB at 1 MHz (750 mA); TLV755P: 52 dB [R-330] |
| Output noise, 10 Hz–100 kHz (as of Nov 2026) | 0.46 µVrms to 130 µVrms | TPS7A94 vs TPS7A02 [R-330] |
| Minimum output capacitor, discrete LDOs | 1 to 22 µF depending on the part (the lowest-noise part cited needs only 4.7 µF) | data-sheet requirements [R-330] |
| On-chip output capacitance | tens of pF to about 1 nF | 100 pF (Milliken et al., 2007), 0.6 nF (Hazucha et al., 2005) [R-328] |
| Response time $C\Delta V/\Delta I$ of a fast on-chip LDO | about 0.5 ns | 0.54 ns: 90 mV droop, 100 mA step, 0.6 nF, 90 nm (Hazucha et al., 2005) [R-328] |
| Processor digital LDO current density (as of Nov 2026) | tens to hundreds of A/mm² | 40 A/mm² (5 nm, 2021), 263 A/mm² (3 nm, 2024) [R-329] |

### [20-05 · Comparators and Sample-and-Hold Circuits](../courses/20-analog-and-mixed-signal-ic-design/chapters/20-05-comparators-and-sample-and-hold.md)

| Quantity | Typical value | Note |
|---|---|---|
| $\sqrt{kT/C}$ at 300 K | 64.4 µV at 1 pF; 20.4 µV at 10 pF | exact; capacitance ×4 per bit of resolution |
| Jitter-limited SNR | $-20\log_{10}(2\pi f_{in}\sigma_t)$ | 64 dB at 1 GHz with 100 fs; −20 dB per decade [7] |
| Best sampling jitter (as of Nov 2026) | tens of femtoseconds | 50 fs stated in an ISSCC 2016 abstract; 50–90 fs on current TI RF-sampling ADC data sheets [R-332], [R-333] |
| Dynamic comparator noise (as of Nov 2026) | about 0.3–1.5 mV for latch-type designs; under 50 µV with dynamic preamplifiers | 1.5 mV at 92 fJ (double tail, 90 nm, 2007); 46 µV at 1 pJ (FIA, 180 nm, 2020); 38 µV at 0.48 pJ (28 nm, 2025) [R-331] |
| Comparator offset, uncalibrated | several mV | 8 mV σ (90 nm, 2007); 4.7 mV in a 28 nm design example; 1.69 mV after calibration [R-331] |
| Regeneration time constant | about 20 ps (90 nm) to about 2.5–3 ps (28 nm and below) | 19 ps derived from 44 ps per decade (Schinkel, 2007); 2.5 ps (Razavi's 28 nm example); about 3 ps "in leading-edge technology" (Murmann, 2022) [R-331], [R-332] |
| Code (metastability) error rate of RF-sampling ADCs (as of Nov 2026) | 10⁻¹⁵ to 10⁻¹⁸ errors per sample | TI ADC32RF55 and ADC12DJ5200RF data sheets [R-333] |
| Flash-ADC metastability, measured | below 10⁻¹² errors per cycle with error reduction, about 10⁻⁴ estimated without | Portmann and Meng, 1996 [R-331] |

### [20-06 · Data Converter Fundamentals](../courses/20-analog-and-mixed-signal-ic-design/chapters/20-06-data-converter-fundamentals.md)

| Quantity | Typical value | Note |
|---|---|---|
| Ideal SQNR, full-scale sine | $6.02N + 1.76$ dB | 74.0 dB at 12 bits, 98.1 dB at 16 bits; exact |
| SQNR penalty for a Gaussian signal at ±4σ | 7.27 dB below a uniform signal, 9.0 dB below a sine | crest factor; exact |
| Processing gain | $10\log_{10}(f_s/2B)$ | 3 dB (half a bit) per doubling of oversampling |
| Thermal limit on the Schreier figure | about 192 dB at 300 K (the survey's $8kT\cdot\text{SNR}$ line); 194.8 dB for an ideal class-B sampler with a Nyquist-frequency input | $10\log_{10}(1/16kT)$ and $10\log_{10}(1/8kT)$ (§3.6) |
| Thermal noise floor of pipeline ADCs (as of 2010) | about 70–74 dB for a 14-bit pipeline, 77–80 dB for a 16-bit ADC | TI *Analog Applications Journal* SLYT379 [R-332] |
| RF-sampling ADC noise density (as of Nov 2026) | about −150 to −156 dBFS/Hz | TI ADC12DJ5200RF: −150.4 dBFS/Hz (dual channel, 0.8 Vpp); ADC32RF55: −155.6 dBFS/Hz [R-334] |
| SNR across frequency of a 12-bit RF-sampling ADC (as of Nov 2026) | 55.6 dBFS at 347 MHz falling to 49.6 dBFS at 8.0 GHz | TI ADC12DJ5200RF, dual-channel mode [R-334] |
| Low-speed state of the art (as of 2022) | at the "8kTSNR energy limit" | Murmann, ISSCC 2022 short course [R-334] |
| Best published Walden figure (as of Nov 2026) | 0.35 fJ/conversion-step | 10-bit SAR at 200 kS/s, 65 nm (Bindra et al., VLSI 2019), from the survey [R-336] |
| Best published Schreier figure (as of Nov 2026) | 189.2 dB (oversampled); 186.8 dB (Nyquist rate) | noise-shaping SAR, 1 kHz bandwidth (Zhao et al., ISSCC 2025); SAR-ISDM (Hsieh and Hsieh, ISSCC 2018) [R-336] |
| Best Schreier figure at high speed (as of Nov 2026) | 181.5 dB at 130 MS/s; 173.3 dB at 1 GS/s; 159.3 dB at 12 GS/s | Wang and Kuo (ISSCC 2022); Cao et al. (ISSCC 2025); Cao et al. (ISSCC 2024) [R-336] |

### [20-07 · Nyquist ADCs: Flash, SAR and Pipeline](../courses/20-analog-and-mixed-signal-ic-design/chapters/20-07-nyquist-adcs.md)

| Quantity | Typical value | Note |
|---|---|---|
| Flash comparators | $2^N - 1$; used to about 6 bits | Murmann's short course: "Typically use for B≤6" [3] |
| Flash comparator area for fixed yield | fourfold per bit, on top of the doubling count | Pelgrom scaling (Example 20-07.1) |
| SAR cycles per sample | $N$ comparisons, plus any redundant ones | §3.2, §3.3 |
| SAR switching energy, 10 bits, differential | 1363.3 (conventional) and 255.5 (monotonic) $C_uV_{REF}^2$ | Example 20-07.3; Liu et al. report "about 81%" less energy and 50% less capacitance [2] |
| 1.5-bit stage offset tolerance | $\pm V_{REF}/4$ | Razavi, citing Lewis et al. [5] |
| Residue-amplifier gain | $A > 2^{N-1}/\beta$: about 73 dB at 12 bits, 86 dB at 14 bits | Example 20-07.5, Problem 20-07.8 |
| Noise of a stage-scaled pipeline | about $2kT/C_1$ | §3.4 |
| Two-channel skew for 60 dBc at 500 MHz | 0.64 ps | Example 20-07.7 |
| Best Schreier figure by speed (as of Nov 2026) | 186.8 dB (SAR, < 1 MS/s); 181.5 dB (pipelined-SAR, 130 MS/s); 173.3 dB (pipeline, 1 GS/s); 159.3 dB (interleaved pipeline, 12 GS/s); 150.1 dB (interleaved SAR, 200 GS/s) | Murmann survey [11], [12] [R-339] |
| Fastest published (as of Nov 2026) | single-channel SAR 2.4 GS/s (7 b, 2017); interleaved 200 GS/s (8 b, 2024) | [11], [12] [R-339] |
| Commercial precision SAR (as of Nov 2026) | 18 b, 1 MS/s, 5.5 mW, SINAD 99.9 dB at 1 kHz: a Schreier figure of about **179.5** dB | TI ADS8881 [15] [R-340] |
| Commercial RF-sampling interleaved ADC (as of Nov 2026) | 12 b, up to 10.4 GS/s, 4.0–5.0 W whole chip | TI ADC12DJ5200RF [10] [R-340] |

### [20-08 · Oversampling and Sigma-Delta Converters](../courses/20-analog-and-mixed-signal-ic-design/chapters/20-08-sigma-delta-converters.md)

| Quantity | Typical value | Note |
|---|---|---|
| SQNR gain per doubling of the OSR | 3 dB without shaping; 9.0, 15.1, 21.1, 27.1 dB for $L$ = 1 to 4 | exact; Schreier's "(6N+3) dB/octave" [5] |
| NTF penalty $10\log_{10}[\pi^{2L}/(2L + 1)]$ | 5.2 dB ($L$ = 1), 12.9 dB ($L$ = 2) | Johns and Martin's constants [6] |
| Convention offset for 1-bit SQNR formulas | 6.02 dB | full scale referenced to Δ or to the ±1 DAC levels (§3.3) |
| Linear model against simulation, 1-bit, near full scale | model optimistic by roughly 5 dB | Schreier's simulations at OSR 128 [5] |
| Lee's rule | peak NTF gain ≤ 2 (Lee, 1987); about 1.5 in practice | neither necessary nor sufficient [5] |
| Op-amp gain | about OSR for a single loop (35 at OSR 64); about OSR² for a MASH (928) | §3.5, §3.6 |
| CIC order | $K \ge L + 1$ | [6] |
| Best Schreier figure, oversampled (as of Nov 2026) | 189.2 dB (noise-shaping SAR, 1 kHz band); 185.3 dB (discrete-time ΔΣ, 20 kHz band) | Murmann survey [13], [14] [R-343] |
| Widest continuous-time ΔΣ bandwidth in the survey (as of Nov 2026) | 360 MHz at 5 GS/s, 158 mW (2022) | [13], [14] [R-343] |
| Precision ΔΣ ADC (as of Nov 2026) | third-order switched-capacitor modulator at 12.8 MHz; DR 111.5 dB at 200 kSPS (about **18.2** effective bits); THD −125 dB; 4.3–33 mW by speed mode | TI ADS127L21 [15] [R-344] |
| PDM MEMS microphone (as of Nov 2026) | 2.4–3.1 MHz clock (OSR **60** for 20 kHz at 2.4 MHz), 68–69 dB(A) SNR, 0.3–1 mA | Infineon IM69D130; TDK T5838, "a fifth order Σ-Δ modulator" [16] [R-344] |
| ECG and biopotential front end (as of Nov 2026) | second-order modulator; 0.75 mW per channel (ADS1298), 335 µW per channel (ADS1292, decimation ratio **256** at 500 SPS) | TI data sheets [15] [R-344] |

### [20-09 · DACs](../courses/20-analog-and-mixed-signal-ic-design/chapters/20-09-dacs.md)

| Quantity | Typical value | Note |
|---|---|---|
| NRZ droop at $f_s/2$ | −3.92 dB | $20\log_{10}(2/\pi)$; exact |
| RZ and mixed-mode peak output | −6 dBFS and −2.8 dBFS | TI DAC39RF10 Table 7-1 [12]; §3.7's formula peaks at **0.742** $f_s$ with **−2.80** dB |
| Unit mismatch for 99.7% INL yield | $\sigma_u \approx 0.5/(1.82\sqrt{2^N})$: 0.43% at 12 bits | Brownian-bridge result [5]; Example 20-09.3 |
| Output-impedance harmonics | $n$-th harmonic ≈ $(xN_t/4)^{n-1}$; differential cancels even orders | [6], [7] |
| Glitch impulse units | nV·s for precision DACs, pV·s for fast current-steering DACs | not an energy, despite the name [13] |
| Precision 20-bit R-2R DAC (as of Nov 2026) | INL ±4 LSB max (−40 to 125 °C); glitch 1 nV·s; settling 1 µs to 0.1% FSR, 2.5 µs to ±1 LSB | TI DAC11001A [13] [R-348] |
| 16-bit string DAC (as of Nov 2026) | INL ±12 LSB max, DNL ±1 LSB (monotonic), glitch 0.1 nV·s | TI DAC8568 [13] [R-348] |
| 16-bit RF-sampling DAC (as of Nov 2026) | 10.24 GS/s; SFDR 85 dBc at 97 MHz, 61 dBc at 3 GHz; NSD −150 to −160 dBFS/Hz; 3.7–5.1 W | TI DAC39RF10 [12] [R-348] |
| Audio ΔΣ DAC (as of Nov 2026) | DR 112 dB (A-weighted), THD+N −93 dB | TI PCM5102A [14] [R-348] |
| MCU DAC (as of Nov 2026) | 12-bit, 1 MS/s, INL ±4 LSB, settling 0.8 µs | TI MSPM0G3507 [14] [R-348] |
| Fastest published DACs (as of Nov 2026) | 8-bit 60–160 GS/s in 5 nm (coherent optics, ISSCC 2024); 14-bit 20 GS/s RF DAC with ≈70 dBc IMD3 to 8.9 GHz (ISSCC 2026) | [10] [R-347] |

### [20-10 · PLLs and Jitter](../courses/20-analog-and-mixed-signal-ic-design/chapters/20-10-plls-and-jitter.md)

| Quantity | Typical value | Note |
|---|---|---|
| Loop bandwidth against reference | $f_c \lesssim f_{ref}/10$ by design; sampled-loop instability near $f_{ref}/3$ (about 28–33%) | Gardner [1], Hanumolu et al. [2], Banerjee [3] **[Established]** |
| Phase-noise convention | $\mathcal{L}(f)$ single-sideband; one-sided $S_\phi = 2\mathcal{L}$; $\sigma_\phi^2 = \int S_\phi\,df = 2\int\mathcal{L}\,df$ | NIST [9], Banerjee [3] **[Established]** |
| Peak-to-peak against rms for Gaussian jitter | about $2Q^{-1}(1/2N)$ times σ: **6.58** for $10^3$ edges, **12.2** for $10^9$, **14.3** for $10^{12}$ (our computation; the table stops at $10^9$) | Banerjee's table [3]; a peak-to-peak number grows with the observation |
| LC oscillator FoM | ideal (F = 1, all power in the tank) **196.8** dB for Q = 10; Razavi: about 186 dB for a simple cross-coupled VCO with Q = 10 at 300 K, about 196 dB for a class-C design with Q ≈ 16 | Leeson [4]; Razavi [10] |
| Best published PLL FoM (as of Nov 2026) | −263.1 dB: 20.3 fs at 19 GHz for 12 mW (integer-N sampling PLL, 28 nm, 2021) | [12] [R-350] **[Established]** |
| Best fractional-N PLL (as of Nov 2026) | 21.6 fs, −260.7 dB, worst-case fractional spur −67.4 dBc (14 GHz, 28 nm, ISSCC 2026) | [12] [R-350] **[Established]** |
| Lowest jitter in the public survey (as of Nov 2026) | 15.8 fs rms (13 GHz charge-pump PLL, ISSCC 2025); the band is not stated in the abstract, so it cannot be ranked against the band-stated records above | [12] [R-350] |
| Commercial RF synthesizer (as of Nov 2026) | TI LMX2594: 10 MHz–15 GHz; 45 fs rms at 7.5 GHz (100 Hz–100 MHz); −110 dBc/Hz at 100 kHz on 15 GHz; normalized in-band floor −236 dBc/Hz | [13] [R-351] |
| SerDes reference clock (as of Nov 2026) | 112G PAM4: about 100 fs rms at 312.5 MHz (12 kHz–20 MHz in TI's example SerDes table; Renesas states no band); with a 4 MHz high-pass filter, 90 fs (112G) and 35 fs (224G) | TI and Renesas notes [14] [R-352] **[Industry estimate]** |
| PCIe reference-clock limit (as of Nov 2026) | Gen 5: 0.15 ps rms; Gen 6: 0.1 ps rms, both after the standard's clock-recovery filters | TI SNAA386 table, not the PCI-SIG text [14] [R-352] |
| MCU system PLL (as of Nov 2026) | TI MSPM0G3507: period jitter 45 ps rms and cycle-to-cycle 60 ps rms at 80 MHz; supply current 316 µA (specified at a 160 MHz VCO frequency) | [15] [R-351] |
| 77 GHz radar chirp PLL (as of Nov 2026) | TI AWR2944: −96 dBc/Hz at 1 MHz offset (76–77 GHz); ramps to 250 MHz/µs | [15] [R-351] |
| 5G EVM budget | 256QAM base-station EVM 3.5%: if the LO took all of it, **2.0**° rms, **199** fs at 28 GHz | 3GPP TS 38.104 [16]; our arithmetic |

### [20-11 · Layout, Matching and PVT Variation](../courses/20-analog-and-mixed-signal-ic-design/chapters/20-11-layout-matching-pvt.md)

| Quantity | Typical value | Note |
|---|---|---|
| $A_{VT}$ rule of thumb | ≈ 1 mV·µm per nm of gate oxide | Pelgrom; Boser's course notes [4], [9] **[Established]** |
| $A_{VT}$ by process | 2.5 µm: 30 (n) / 35 (p); 180 nm: ≈ 5; 65 nm: 3.5; 28 nm bulk HKMG: 2.4; 20 nm: 1.9; 28/14 nm FD-SOI: ≈ 1.3–1.4; 14 nm SOI FinFET: 1.4 (n) / 0.7 (p) mV·µm | [1], [4], [6], with 180 nm from Boser's notes [9] [R-353], [R-354]; definitions vary by $\sqrt2$ [5] **[Industry estimate]** |
| $A_{VT}$ at 7 nm, 5 nm, GAA (as of Nov 2026) | no public measured value found | foundry data are in confidential design kits |
| Gain factor $A_\beta$ | 1–2 %·µm | [4] |
| Other components | bipolar $V_{BE}$ ≈ 0.3 mV·µm; resistors 0.5–5 %·µm; capacitors ≈ 0.3%/√(C in fF) | Pelgrom's summary [4] |
| A small 65 nm pair (1 µm × 0.06 µm) | σ(ΔV_TH) ≈ **14.3** mV | from $A_{VT}$ = 3.5 mV·µm; our arithmetic |
| Pelgrom's 1989 pair (20 µm × 20 µm) | σ(ΔV_TH) ≈ **1.5** mV | from $A_{VT}$ = 30 mV·µm; our arithmetic |
| Well-proximity shift | up to 100 mV within about 1 µm of the well edge (0.18 µm, 2003); 33% for 40 nm I/O devices against 1.87% at 16 nm FinFET | [7] [R-355] |
| Layout-dependent bias shift | 20–30% (well proximity, STI stress) | Drennan et al. [7] |
| Supply and temperature corners | $V_{DD}$ ±10%; commercial 0 to 70 °C; industrial −40 to 85 °C; AEC-Q100 grades 3/2/1/0: −40 °C to 85/105/125/150 °C | [9], [11] [R-356] **[Established]** |
| Two-sided Gaussian tails | 3σ: 2700 ppm; 4σ: **63** ppm; 4.5σ: 6.8 ppm; 5σ: **0.57** ppm; 6σ: **0.0020** ppm | exact |
| Monte Carlo precision on σ (95%) | 100 runs: −12% to +16%; 1000 runs: ±4–5% | §3.7 |
| Analog area per node (as of 2019) | 0.8–0.9× per node, against 0.5× for logic and SRAM | Loke et al. [12] **[Industry estimate]** |
| Wire capacitance | ≈ 0.2 fF/µm, about a tenth of gate capacitance per µm of width | course teaching value [9] |

### [20-12 · Why Analog Does Not Scale Like Digital](../courses/20-analog-and-mixed-signal-ic-design/chapters/20-12-why-analog-does-not-scale.md)

| Quantity | Typical value | Note |
|---|---|---|
| Supply history | 5 V (early 1990s) → 1.8 V (180 nm) → 1.1 V (65 nm) → 0.8 V (7 nm, roadmap) | Annema et al.; ITRS via Stillmaker and Baas [2], [3] |
| Logic $V_{DD}$ roadmap (as of Nov 2026) | 0.70 V now, 0.60 V from 2027; raised to 0.75 V in 2021 for FinFET leakage | IRDS 2024 [3] [R-357] **[Industry estimate]** |
| Threshold at the same node | $V_{t,sat}$ ≈ 0.16 V (high performance) to 0.29 V (high density) | IRDS 2024; $V_{DD}/V_{t}$ ≈ **2.4** [3] |
| Analog and I/O supplies | many I/Os still signal at 1.8 V "despite core VDD reduction"; precision analog uses thick-oxide devices or separate, higher supplies | Loke [6] |
| $A_{VT}$ | ≈ 1 mV·µm per nm of oxide; 3.5 mV·µm at 65 nm; 0.7–1.4 mV·µm in fully depleted FinFET and FD-SOI devices | ITRS 2003, Pelgrom; IEDM 2013 [4] [R-358] |
| Mismatch energy against kT | $C_{ox}A_{VT}^2$ ≈ 30–70 times kT | Example 20-12.4; Pelgrom's slides say 70 [4] **[Contested]** (definition-dependent) |
| FinFET intrinsic gain | "3×" (Loke, Qualcomm; baseline not stated); 3.8 times 28 nm planar (Jeong et al., Samsung, 14 nm RF FinFET) | [6], [7] |
| Analog and I/O area per node | 0.8–0.9×, against 0.5× for logic and SRAM; IRDS assumes 0.9× per node | Loke; IRDS 2024 [3], [6] **[Industry estimate]** |
| TSMC N3 against N5 (2020 claim) | logic up to 1.7×, SRAM 1.2×, analog 1.1× density | press report of TSMC's symposium [9] **[Industry estimate]** |
| ADC energy trend | median Walden FoM down about 575× from 1997–99 to 2024–26; best Schreier FoM 189.2 dB (2025, 0.18 µm), **2.6** dB below the 191.8 dB thermal line | Murmann's survey; our extraction [8] [R-359] |
| Wafer price (estimates) | 28 nm $2,891 → 7 nm $9,346 → 5 nm $16,988 (2020 model) | CSET [10] **[Industry estimate]** |

## [21 · RF and Microwave Engineering](../courses/21-rf-and-microwave-engineering/README.md)

### [21-01 · S-Parameters and Network Analysis](../courses/21-rf-and-microwave-engineering/chapters/21-01-s-parameters.md)

| Quantity | Typical value | Note |
|---|---|---|
| Return loss 10 dB | $\lvert\Gamma\rvert$ = **0.316**, VSWR **1.92**, mismatch loss **0.46** dB | A common antenna and module specification |
| Return loss 20 dB | $\lvert\Gamma\rvert$ = **0.100**, VSWR **1.22**, mismatch loss **0.04** dB | A good instrument or connector port |
| Reference impedance | 50 Ω (RF instruments and coax), 75 Ω (video and cable TV), 100 Ω differential (high-speed serial links) | Conventions, not physics [Established] |
| VNA system dynamic range, 10 Hz IF bandwidth | specified 129 to 146 dB from about 0.5 to 50 GHz (typical up to 151 dB; much less below 50 MHz); typical 96 to 111 dB up to 110 GHz | Three vendors' data sheets, Aug 2022 to Aug 2026 [R-362] |
| Narrower IF bandwidth | **10** dB more dynamic range per decade of bandwidth | Receiver noise power is proportional to bandwidth |
| Residual errors after a coaxial calibration | directivity 46 to 60 dB, source match 31 to 43 dB (46 dB typical), load match 42 to 58 dB | Two vendors' specified values (typical where stated), as of Apr–Aug 2026 [R-362] |
| Adapter with VSWR 1.5 after calibration | effective directivity about **14** dB | HP application note [9, R-361] |
| Return-loss uncertainty with 46 dB residual directivity and 43 dB source match | 20 dB reads as **19.6** to **20.5** dB; 35 dB as **32.8** to **37.9** dB | Worst-case phases of those two terms only (Marketing vs Reality, §9) |
| Unconditional stability | $K > 1$ and $\lvert\Delta\rvert < 1$, or $\mu > 1$ | At every frequency where the device has gain |

### [21-02 · Impedance Matching Networks](../courses/21-rf-and-microwave-engineering/chapters/21-02-impedance-matching-networks.md)

| Quantity | Typical value | Note |
|---|---|---|
| L-network Q for a ratio $r = R_{high}/R_{low}$ | $\sqrt{r - 1}$: **2** at 5:1, **3** at 10:1, **4.90** at 25:1 | Bandwidth falls as 1/Q |
| 10 dB return-loss band of one L-section | about **0.76**/Q (fractional) | Example 21-02.1 |
| 10 dB return loss | $\lvert\Gamma\rvert$ = **0.316** | The usual "matched" threshold for bandwidth |
| Match loss from the inductor | $10\log_{10}(1 + Q_n/Q_u)$: 0.79 dB at $Q_n/Q_u$ = 0.2, 1.38 dB at 3/8 | Example 21-02.5 |
| Bode–Fano bound, 50 Ω ∥ 1 pF | **4.34** GHz at $\lvert\Gamma\rvert \le 0.1$; **8.69** GHz at $\lvert\Gamma\rvert \le 0.316$ | Inversely proportional to RC |
| On-chip spiral inductors | Q "up to 40" in a 1998 thick-copper process; a patterned ground shield raises Q "up to 33%" | Best cases, not typical [5, 6, R-365] |
| Spiral-inductance hand formulas | within about 3% of a field solver, against about 20% for older expressions | Mohan et al., 1999 [8, R-365] |
| LNA input return loss in data sheets | 9 dB min, 13 dB typical (a 2.6 GHz LNA); 6 dB min, 7 dB typical (a Wi-Fi 7 front-end receive path) | Dec 2023 and Sep 2024 data sheets [12, 13, R-366] |

### [21-03 · Noise Figure and Linearity](../courses/21-rf-and-microwave-engineering/chapters/21-03-noise-figure-and-linearity.md)

| Quantity | Typical value | Note |
|---|---|---|
| $kT_0$ | −173.98 dBm/Hz (−174) | 290 K reference [5, 10] |
| IIP3 − P1dB | 9.64 dB for a pure cubic; 8.96 dB for a differential pair; 8 to 13 dB in four LNA and front-end data sheets | Model result, not a rule (§9) [R-369] |
| IM3 slope | 3 dB per dB; IM3 level $-2(\text{IIP3} - P_{in})$ dBc | Small-signal region only |
| SFDR | $\tfrac23(\text{IIP3} - N_{floor})$ | 3 dB of IIP3 buys 2 dB |
| Bipolar transistor IIP3 | $\sqrt8\,V_T$ = 73 mV peak (−12.7 dBm across 50 Ω) | Degeneration raises it |
| Differential-pair IIP3 | $4V_T$ = 103 mV peak (differential) | Even orders cancel |
| Discrete LNA noise figure | 0.6 dB typical (1.1 dB max) at 2.6 GHz; 1.6 dB typical at 5.5 GHz | Infineon data sheets, 2021 and 2023 [R-369] |
| Wi-Fi 7 front-end receive path | NF 1.8 dB typical, IIP3 +8 dBm, IP1dB −5 dBm | Qorvo QPF4609, Sep 2024 [R-369] |
| 77 GHz single-chip radar receiver | NF 12 to 15 dB | TI AWR2944 and AWR1843 data sheets [R-369] |
| 5G handset NF assumed by 3GPP | about 9 dB (legacy bands, inferred), 10 to 10.5 dB (n77–n79, stated) | TR 38.817-01 [9, R-368] |
| 5G reference sensitivity, two receivers | −100.0 dBm (n1, 5 MHz); −85.54 dBm by formula, −85.6 dBm rounded down (n78, 100 MHz) | TS 38.101-1 V19.7.0, Sep 2026 [8, R-368] |
| 5G wide-band intermodulation test | two interferers of −46 dBm each (one CW, one modulated), wanted 6 to 9 dB above REFSENS | TS 38.101-1 §7.8.2 [8, R-368] |
| Y-factor limit | not used when NF exceeds the source's ENR by more than about 10 dB | Agilent AN 57-1 [5] |

### [21-04 · Low-Noise Amplifiers](../courses/21-rf-and-microwave-engineering/chapters/21-04-low-noise-amplifiers.md)

| Quantity | Typical value | Note |
|---|---|---|
| Resistive termination | NF ≥ 3.01 dB | Before any amplifier noise |
| Common-gate input at match | $1 + \gamma/\alpha$: 2.2 dB ($\gamma/\alpha$ = 2/3) to 3.0 dB (1) | Match fixes $g_m = 1/R_s$ |
| Long-channel noise constants | $\gamma$ = 2/3, $\delta$ = 4/3, $\lvert c\rvert$ = 0.395 | Short-channel values contested (§9) [8] |
| Device $F_{min}$ with induced gate noise | $1 + 2(\omega_0/\omega_T)\sqrt{\delta\gamma(1 - \lvert c\rvert^2)/5}$: **0.32** dB at $f_0/f_T$ = 0.1 | Long-channel constants [3, 8] |
| Discrete GNSS LNA | NF 0.55 dB typ (1.0 max), gain 19.6 dB, 2.5 mA at 1.8 V (**4.5** mW) | Infineon BGA524N6, 2021 [R-373] |
| Base-station LNA | NF 0.6 dB typ (1.0 max), gain 34 dB, 120 mA at 5 V (**0.60** W) | Skyworks SKY67177-11, Aug 2025 [R-373] |
| mmWave CMOS LNA research | 2.2 dB minimum at 36.5 GHz (65 nm); 2.3 dB minimum (3.2 dB band average) at 60–74 GHz; 3.4–6.5 dB at 70–86 GHz | 2023–2026 papers [R-372] |
| Single-chip 77 GHz radar receiver | NF 12–15 dB (whole receive chain) | TI data sheets [R-373] |
| Published CMOS LNAs surveyed | about 500 over 20 years; more than 30 figures of merit in use | Belostotski and Klumperink, 2022 [8] |

### [21-05 · Mixers](../courses/21-rf-and-microwave-engineering/chapters/21-05-mixers.md)

| Quantity | Typical value | Note |
|---|---|---|
| Commutating mixer conversion gain | $2/\pi$ (−3.92 dB) single- and double-balanced; $1/\pi$ for a single-switch (0/1) mixer | Ideal hard switching |
| LO-harmonic responses | 3rd: −13.46 dB, 5th: −17.90 dB (9.5 and 14 dB below the fundamental) | Square-wave LO |
| Noise folding, noiseless switching mixer | SSB 3.92 dB unfiltered; 3 dB from the image alone | $s^2 = 1$ |
| Image rejection | $4/(\varepsilon^2 + \theta^2)$: 40 dB at 1% and 1°; "30–40 dB" typical on chip without calibration; 57–62 dB with calibration or special frequency plans | [2, 7, 12, 13] |
| Passive diode mixer | conversion loss about 5 dB, IP3 15 dBm at +7 dBm LO; 23 dBm at +17 dBm LO | Mini-Circuits ADE-1+/ADE-1H+ [10] |
| Passive mixer noise figure | about equal to its conversion loss (6.9 dB at 5 GHz) | Mini-Circuits MDB-24H+ [10] |
| Single-chip radar receiver image rejection | 30 dB | TI AWR1843 [R-373] |
| N-path filter | BW $= 1/(\pi NR_sC)$; centre loss 1.82 dB (N = 4), 0.45 dB (N = 8) | Ideal switches |

### [21-06 · Oscillators and VCOs](../courses/21-rf-and-microwave-engineering/chapters/21-06-oscillators-and-vcos.md)

| Quantity | Typical value | Note |
|---|---|---|
| Ideal-tank ISF | $\Gamma = -\sin\theta$, $\Gamma_{rms}$ = 0.707 | Half of white noise becomes phase noise |
| FoM bound | $10\log_{10}[2Q^2(1\text{ mW})/(FkT)]$: 196.8 dB at Q = 10, F = 1 | 20-10 |
| Best LC VCO FoM, 1–9 GHz | about 189–195 dB | [7, 8, 9, 10] (as of Nov 2026) |
| Best VCO FoM, 25–30 GHz | about 184–193 dB in JSSC designs; 195 dB claimed for a sub-milliwatt design | [10, 11, 12] (as of Nov 2026) |
| Integrated synthesizer VCO | about −128 to −132 dBc/Hz at 1 MHz from 6–8 GHz | TI LMX2595, LMX2820 [13] |
| 77 GHz radar LO | −93 to −96 dBc/Hz at 1 MHz | TI AWR2944, AWR1843 [14] |
| Division by N | $-20\log_{10}N$: 6.02 dB per divide-by-2 | Until the divider's noise floor |
| Class-C improvement over class-B | 3.9 dB, theoretical, same current | [8] |
| Quadrature error | ≤0.25° (QVCO, 1.8 GHz) to 0.9° (28 GHz coupled-PLL QVCO) | [12] |
| Lock range | $(f_0/2Q)(I_{inj}/I_{osc})$: about 2 MHz at 5 GHz, Q = 11.5, 1% | §3.8 |

### [21-07 · Power Amplifiers](../courses/21-rf-and-microwave-engineering/chapters/21-07-power-amplifiers.md)

| Quantity | Value | Note |
|---|---|---|
| Ideal tuned class A | 50% (×(1 − V_k/V_DD)) | §3.1 |
| Ideal class B | π/4 = 78.5% | §3.2 |
| Class F, third harmonic only | 88.4% maximally flat ($V_3 = V_1/9$); 90.7% maximum ($V_3 = V_1/6$) | §3.3 [3] |
| Class E | P = 0.5768 V_DD²/R; ωCR = 0.1836; X/R = 1.1525; peak 3.56 V_DD and 2.86 I_DC | §3.3 |
| Class-B efficiency at 6 dB back-off | 39.3% | $(\pi/4)x$ |
| Symmetric Doherty | 78.5% at 6.02 dB back-off and at peak, 69.8% dip | §3.5 |
| Asymmetric Doherty, γ = 2 | first peak at 9.54 dB back-off | §3.5 |
| Average efficiency for a 9.64 dB-PAPR OFDM signal | class B 29.2%, Doherty 54.9%, ET (20% floor, 85% modulator) 65.5% | Examples 21-07.5, 21-07.7 |
| ACLR of a cubic PA | $2(P_{in} - \text{IIP3}) - 4.77$ dB | §3.4 |
| Distortion bandwidth | $k$-th order spans $k$ times the channel | §3.7 |
| NR handset limits | 23 dBm (power class 3); NR ACLR 30 dB; 256-QAM EVM 3.5%; MPR up to 6.5 dB | 3GPP TS 38.101-1 V19.7.0 [4] (as of Nov 2026) |
| NR base-station limits | ACLR 45 dB; 1024-QAM EVM 2.5% | TS 38.104 V19.6.0 [5] |
| FR2 handset ACLR | 16–17 dB | TS 38.101-2 [4] |
| Wi-Fi 7 4096-QAM EVM | −38 dB | [6] |
| OFDM/NR PAPR at 0.01% | about 10–12 dB raw (TI quotes 10–15 dB), 6.5–8 dB after CFR | [7] |
| GaN MMIC Doherty, 4–6 GHz | 38.5–46.5% drain efficiency at 6 dB back-off | [9] (2022) |
| 28 GHz silicon Doherty | 38% PAE at P1dB; 15–21% average with 64/256-QAM | [11] (2026) |

### [21-08 · Transceiver Architectures](../courses/21-rf-and-microwave-engineering/chapters/21-08-transceiver-architectures.md)

| Quantity | Value | Note |
|---|---|---|
| Image distance | $2f_{IF}$ from the wanted signal | §3.1 |
| Preselector selectivity per order | $20\log_{10}x_{im}$ dB | Butterworth, §3.1 |
| Half-IF spur | $f_{LO} \mp f_{IF}/2$ | §3.2 |
| I/Q-mismatch EVM floor | $10^{-\text{IRR}/20}$; 40 dB IRR → 1% | §3.3 |
| Jitter-limited SNR | $-20\log_{10}(2\pi f\sigma_t)$: 62.5 dB at 2.4 GHz, 54.5 dB at 6 GHz for 50 fs | §3.5 |
| RF-sampling ADC | NSD about −150 to −155 dBFS/Hz, NF about 19–30 dB | TI AFE7950 [7] (as of Nov 2026) |
| RF-sampling transceiver power | about 1 W per active chain | AFE7950, 4T4R2F [7] |
| Low-IF BLE receiver | 266 µW, 72% of it in LO generation | [10] (2022) |
| Wi-Fi 7 transceiver EVM floor | −42.6 to −46.1 dB | [9] (2023–2024) |

### [21-09 · The RF Front End: Filters, Switches and Modules](../courses/21-rf-and-microwave-engineering/chapters/21-09-rf-front-end.md)

| Quantity | Value | Note |
|---|---|---|
| Acoustic velocity | ~4 km/s (SAW on LiTaO₃) to ~11 km/s (bulk AlN) | §2; wavelength at 2 GHz 2–5.5 µm |
| Resonance spacing | $(f_p - f_s)/f_s \approx C_m/2C_0$ | §3.1 |
| AlN BAW coupling | $k^2_{eff}$ ≈ 6.6%, spacing ≈ 2.8% | [3]; Example 21-09.1 |
| High-coupling resonators (research) | ScAlN FBAR > 20% (2024); XBAR ~25%, spacing ~11% (2019) | [6], [7] |
| Resonator Q | > 4000 (IHP-SAW, 2017); 3585 (AlN FBAR at 5 GHz, 2004); ~300 (first XBARs) | [3], [5], [6] |
| TCF | ≈ −40 ppm/°C plain LiTaO₃ SAW (implied); −8 IHP-SAW; ~27 (magnitude) FBAR | [4], [5] |
| Ladder bandwidth | at most ≈ 2 × the resonance spacing | §3.2 |
| Duplexer TX-to-RX isolation | 50–55 dB guaranteed minimum | [2], [11] |
| Duplexer or quadplexer loss | 2.0–2.8 dB typical, 3.0–3.8 dB maximum | [11] |
| Handset transmit power | 23 dBm at the antenna (NR power class 3) | 21-07 |
| SOI switch figure of merit | ~100–120 fs (process); 378 fs for one shipping tuner part | [9], [12], [17] |
| Mismatch loss | 0.18 dB at VSWR 1.5; 1.25 dB at 3; 3.10 dB at 6 | §3.6 |
| Mobile RFFE market | $15.4 billion (2024) [Industry estimate] | [15] |

### [21-10 · Antennas, Arrays, Beamforming and mmWave](../courses/21-rf-and-microwave-engineering/chapters/21-10-antennas-arrays-mmwave.md)

| Quantity | Value | Note |
|---|---|---|
| Half wavelength | 5.35 mm at 28 GHz; 3.84 mm at 39 GHz; 1.95 mm at 77 GHz | Array cell size |
| Patch element gain | about 5–8 dBi | §3.2 |
| Chu bound | $Q \ge 1/(ka)^3 + 1/ka$; VSWR-2 bandwidth $0.707/Q$ | §3.3 |
| Cosine scan loss | 1.5 dB at 45°, 3.0 dB at 60° | §3.4 |
| Squint bandwidth | $0.886/[N(d/\lambda_0)\sin\theta_0]$ | §3.5 |
| Phase quantization | 3 bits: 0.22 dB loss; each bit −6 dB floor | §3.6 |
| EIRP scaling | $20\log_{10}N$ + element gain + element power | §3.7 |
| 5G FR2 handset (PC3, n257) | ≥ 22.4 dBm peak EIRP; ≤ 23 dBm TRP, ≤ 43 dBm EIRP; ≥ 11.5 dBm at the 50 %-tile | [1] (as of Sep 2026) |
| US mmWave EIRP caps | 43 dBm mobile; 75 dBm per 100 MHz base station; 40 dBm average at 57–71 GHz | [2] |
| Gaseous absorption (sea level, standard atmosphere, 7.5 g/m³ water vapour) | about 0.1 dB/km at 28–39 GHz; about 15 dB/km near 60 GHz | [3] |
| Rain, 25 mm/h | 4.6 dB/km at 28 GHz; 10.1 dB/km at 60 GHz | [3] |
| Hand blockage (3GPP model) | 30 dB | [4] |
| 28 GHz beamformer ICs | 32 elements per IC; 54 dBm EIRP from 64 dual-polarized elements | [6] |
| AiP vs on-chip antenna efficiency (60 GHz) | above 90% vs below 12% | [9] |

### [21-11 · Link Budgets](../courses/21-rf-and-microwave-engineering/chapters/21-11-link-budgets.md)

| Quantity | Value | Note |
|---|---|---|
| Thermal noise | −174 dBm/Hz | 17-02 |
| Range per dB | ×1.12 (n = 2), ×1.07 (n = 3.5) | §3.1 |
| Shannon limit | $E_b/N_0$ ≥ −1.59 dB | §3.2 |
| Rayleigh margin | 9.8 dB (10%), 20 dB (1%) | §3.3 |
| Bluetooth LE sensitivity, specification | −70 dBm (1M, 2M), −82 dBm (Coded S = 8) | [1] (Core 6.2) |
| Bluetooth LE sensitivity, real parts | about −95 to −99 dBm (1M), −102 to −106 dBm (Coded) | [2] (as of Nov 2026) |
| Wi-Fi minimum sensitivity, 20 MHz | −82 dBm (MCS0) to −52 dBm (MCS11); 3 dB higher (less sensitive) per bandwidth doubling [Established; secondary source] | [3] |
| 2.4 GHz power limits | US 30 dBm conducted + 6 dBi; EU 20 dBm EIRP | [4] |
| NR UE power classes | 23 / 26 / 29 / 31 dBm | [5] |
| 3GPP coupling-loss targets | 164 dB (massive IoT, 160 b/s); 140–143 dB (eMBB extreme coverage) | [5] |
| Shadowing σ (3GPP) | 4 dB (LOS), 6–8 dB (NLOS) | [6] |
| Satellite to handheld (LEO 600 km, S-band) | G/T −31.6 dB/K; path loss 159 dB; uplink CNR about 3 dB in 360 kHz | [7] |
| GPS L1 C/A minimum | −128.5 dBm | [9] |

### [21-12 · Modem Baseband Architecture and Wireless Standards](../courses/21-rf-and-microwave-engineering/chapters/21-12-modem-baseband-and-standards.md)

| Quantity | Value | Note |
|---|---|---|
| NR peak per 100 MHz carrier (FR1, 4 layers) | 2.34 Gb/s (256-QAM), 2.92 Gb/s (1024-QAM) | §3.1 |
| ITU 5G peak vs experienced rate | 20 Gb/s vs 100 Mb/s (5th percentile) | [2] |
| Modem peak claims (2025–2026) | 10–12.5 Gb/s downlink, 3.5–3.7 Gb/s uplink | [11] (vendor claims, as of Nov 2026) |
| US median 5G download (best operator, H1 2026) | 314 Mb/s | [12] |
| HARQ processes | 16 per cell, up to 32 by capability | [4] |
| Soft-buffer rate cap $R_{LBRM}$ | 2/3 | [3] |
| RLC round trip for L2 sizing | 50 / 40 / 30 / 20 ms at 15 / 30 / 60 / 120 kHz | [1] |
| LDPC decoder state of the art | 118.3 Gb/s, 5.14 pJ/b, 2.35 mm² (16 nm, 2026) | [13] |
| Wi-Fi 7 | ≤ 8 streams; 2882 Mb/s per stream at 320 MHz | [5] |
| UWB channel | 499.2 MHz (channels 5 and 9 at 6489.6 and 7987.2 MHz) | [6] |
| GPS chips | L1 C/A 1.023 Mchip/s (293 m); L5 10.23 Mchip/s (29.3 m) | [8] |
| LEO Doppler at 2 GHz (600 km) | up to about ±46 kHz | §3.6 |
| First normative 6G release | 3GPP Release 21: Stage 3 Dec 2028, ASN.1 Mar 2029 | [10] |

## [22 · Power Electronics and Energy Conversion](../courses/22-power-electronics-and-energy-conversion/README.md)

### [22-01 · Power Conversion Principles](../courses/22-power-electronics-and-energy-conversion/chapters/22-01-power-conversion-principles.md)

| Quantity | Typical value | Source |
|---|---|---|
| 80 PLUS Titanium, 230 V redundant supplies (10/20/50/100% load) | 90 / 94 / 96 / 91% | [1] (as of Nov 2026) |
| 80 PLUS Ruby, 230 V redundant supplies (5/10/20/50/100%) | 90 / 91 / 95 / 96.5 / 92% | [1] (as of Nov 2026) |
| EU and US external supplies above 49 W (to 250 W), basic-voltage (output ≥ 6 V) single-voltage AC-DC | ≥ 88.0% average active efficiency; ≤ 0.21 W no-load | [2, 3] |
| AC-DC external supplies of 49 W or less | ≤ 0.10 W no-load | [2, 3] |
| USB Power Delivery maximum | 240 W (48 V × 5 A), Revision 3.3 (Oct 2026) | [4] |
| Ultra-low-quiescent LDO / buck for wearables | 25 nA / 60 nA quiescent; buck 80% at 1 µA | [5] |
| GaN 65 W USB-PD adapter reference | 25.29 W/in³ (box unstated); 92.8–94.3% at full load | [6] |
| GaN totem-pole PFC stage | 99–99.2% peak; 120 W/in³ open frame | [7] |
| AI server supplies, 2024–26 references | 97.5% peak; 100–137 W/in³ | [8–10] |
| ORv3 power shelf | six 5.5 kW supplies = 33 kW per 1OU shelf; about 48 W/in³ per supply | [11] |
| 48 V to 12 V intermediate bus converter | 97.7%; 1300 W/in³ "without connector" | [12] |
| Charging loss through any resistance | ½CV², half the energy delivered | §3.4 |

### [22-02 · Steady-State Analysis and the Buck Converter](../courses/22-power-electronics-and-energy-conversion/chapters/22-02-buck-converter-steady-state.md)

| Quantity | Typical value | Source |
|---|---|---|
| Inductor ripple design rule | 20–40% of the output current | [1] |
| Output capacitance for a ripple target | $\Delta i_L/(8f_s\Delta v)$ | §3.3, [1] |
| Ceramic capacitor loss at rated DC voltage | 35–65% (10 µF, 6.3 V, X7R, 0805, three vendors) | [4] (2019) |
| Input capacitor RMS current | about $I\sqrt{D(1 - D)}$, at most about $I/2$ | §3.3 |
| Industrial buck minimum on-time | 68 ns | [2] |
| Wearable buck PFM on-time and PWM frequency | $(V_{OUT}/V_{IN}) \times 556$ ns; about 1.8 MHz | [3] |
| Wearable buck PFM pulse rate at 1 µA (3.6 V to 1.8 V, 2.2 µH) | about 16 Hz | Example 22-02.6 |
| Diode drop against synchronous switch at 1.2 V, 10 A | 4.3 W against 0.45 W total conduction loss | Example 22-02.4 |

### [22-03 · Boost, Buck-Boost and Other Topologies](../courses/22-power-electronics-and-energy-conversion/chapters/22-03-boost-buck-boost-topologies.md)

| Quantity | Typical value | Source |
|---|---|---|
| Conversion ratios (CCM) | buck $D$; boost $1/D'$; buck-boost and Ćuk $-D/D'$; SEPIC $D/D'$ | §3 |
| Boost maximum gain with winding resistance | $\tfrac12\sqrt{R/R_L}$, at 50% efficiency | §3.2 |
| Boost CCM–DCM boundary | $K_{crit} = DD'^2$, at most 4/27 at $D$ = 1/3 | §3.5 |
| Single-cell boost (commercial) | 0.5–5.5 V in, 94% at 3.6 V to 5 V, 1.5 A; 47/68 mΩ switches; 1 MHz | [2] |
| Low-voltage four-switch buck-boost | 1.3–5.5 V in, 1.8–5.2 V out, 2 A at 3.3 V; 0.47 µH; 11 µA quiescent | [1] |
| PFC boost output bus | 400 V, above the highest line peak (391.7 V at 277 V AC) | [3], Example 22-03.7 |

### [22-04 · Isolated Converters: Flyback and Forward](../courses/22-power-electronics-and-energy-conversion/chapters/22-04-isolated-converters.md)

| Quantity | Typical value | Source |
|---|---|---|
| Flyback ratio and switch voltage | $V = (V_{in}/n)\,D/D'$; $V_{in} + nV$ plus spike | §3.2 |
| Forward ratio and reset limit | $V = DV_{in}/n$; $D_{max} = 1/(1 + N_3/N_1)$ = 0.5 for $N_3 = N_1$; switch $2V_{in}$ | §3.4 |
| Clamp energy per cycle | $\tfrac12L_{lk}I_{pk}^2\,V_c/(V_c - V_R)$ | §3.3 |
| 65 W GaN QR flyback reference | 32:5 turns; 76–163 kHz; 92.8–94.3% at full load | [1] |
| ES1 (touch-safe) limits, IEC 62368-1 | 30 V RMS, 60 V DC; 0.5 mA RMS touch current below 1 kHz | [3] |
| Mains transient, ≤ 300 V line to neutral | 1.5 / 2.5 / 4.0 / 6.0 kV for OVC I–IV | [4] |
| Reinforced creepage, 400 V, PD2 | 4.0 / 5.6 / 8.0 mm for material groups I–III | [4] |
| Y1 capacitor rating | 500 VAC; 4000 VAC test; 8 kV impulse | [5] |

### [22-05 · Magnetics Design](../courses/22-power-electronics-and-energy-conversion/chapters/22-05-magnetics-design.md)

| Quantity | Value | Source |
|---|---|---|
| $\mu_0$ | $4\pi \times 10^{-7}$ H/m (to 1 part in 10⁹) | SI |
| Energy density at 0.3 T in air | 35.8 kJ/m³ = 35.8 µJ/mm³ | §3.2 |
| MnZn ferrite $B_{sat}$ (3C95) | about 530 mT at 25 °C, 410 mT at 100 °C | [1] |
| MnZn ferrite loss (3C95, 100 kHz, 200 mT) | about 350 kW/m³ at 25 °C, 290 kW/m³ at 100 °C | [1] |
| Ferrite resistivity (3C95) | about 5 Ω·m | [1] |
| Nanocrystalline (VITROPERM 800) | $B_{sat}$ 1.24 T; ≤ 80 W/kg at 100 kHz, 0.3 T; 1.15 µΩ·m | [3] |
| Powder cores $B_{sat}$ | about 1.05 T (Kool Mµ), 1.5 T (High Flux) | R-081 |
| Steinmetz exponents (N87, sine fit) | $\alpha$ = 1.635, $\beta$ = 2.253 | [4] |
| Copper resistivity | 17.24 nΩ·m at 20 °C; +0.393%/K; 22.66 nΩ·m at 100 °C | [7] |
| Skin depth in copper, 100 kHz | 0.209 mm (20 °C), 0.240 mm (100 °C) | §3.5 |
| Optimum transformer loss split | $P_{fe}/P_{cu} = 2/\beta$ ≈ 0.89 for $\beta$ = 2.253 | §3.6 |

### [22-06 · Converter Losses and Wide-Bandgap Switches](../courses/22-power-electronics-and-energy-conversion/chapters/22-06-converter-losses-and-wide-bandgap.md)

| Quantity | Value | Source |
|---|---|---|
| Critical field (at 10¹⁶ cm⁻³): Si / 4H-SiC / GaN | 0.3 / 3.1 / 4.9 (projected) MV/cm; GaN [Contested] | [5] |
| Baliga FOM relative to Si | about 700 (SiC), 3200 (GaN) | [5] |
| 650 V GaN, 55 mΩ class | $Q_g$ 4.7 nC, $Q_{oss}$ 35 nC, $Q_{rr}$ 0, $R_{DS(on)}$ ×2.2 at 150 °C | [1] |
| 650 V SiC, 50 mΩ class | $Q_g$ 22 nC, $Q_{oss}$ 47 nC, body-diode $V_{SD}$ 4.3 V | [2] |
| 600 V Si superjunction, 45 mΩ class | $Q_g$ 90 nC, $C_{o(tr)}$ 1212 pF, $Q_{rr}$ 3.6 µC | [4] |
| 100 V class $R \cdot Q_g$ | 131 (Si) vs 26.4 (GaN) mΩ·nC | [6], [7] |
| 1200 V SiC short-circuit withstand (where rated) | 3 µs at 800 V | [8] |
| Hard turn-on loss in a half bridge | $Q_{oss}V$ per transition | §3.3 |
| ZVS condition | $I \ge 2Q_{oss}/t_d$ | §3.7 |

### [22-07 · Converter Dynamics and Control](../courses/22-power-electronics-and-energy-conversion/chapters/22-07-converter-dynamics-and-control.md)

| Quantity | Value | Source |
|---|---|---|
| Buck control-to-output | $V_g/(1 + sL/R + s^2LC)$; $f_0 = 1/(2\pi\sqrt{LC})$, $Q = R\sqrt{C/L}$ | §3.1 |
| Boost RHP zero | $f_{RHP} = D'^2R/(2\pi L)$; resonance at $D'/(2\pi\sqrt{LC})$ | §3.2 |
| Typical phase margin target | 45–60° | 15-07 |
| k-factor | $k = \tan((B/2 + 90°)/2)$ for a type-III boost $B$ | §3.3 |
| Slope compensation for all duty cycles | $m_a > m_2/2$; $m_a = m_2$ is deadbeat | §3.4 |
| Load-step droop estimate | $\Delta V \approx \Delta I/(2\pi f_cC)$ | §3.5 |
| Delay phase cost | $360° \cdot f_c t_d$ | §3.5 |

### [22-08 · PMICs and Power Management for SoCs](../courses/22-power-electronics-and-energy-conversion/chapters/22-08-pmics.md)

| Quantity | Typical value | Source |
|---|---|---|
| Cascaded efficiency | $\eta_{buck}V_{out}/V_{mid}$ | §3.2 |
| PFM–PWM crossover | where $(R_p - R)I^2 + k_{PFM}I + V_{in}I_q = P_f$; tens to a hundred-odd mA | §3.3 |
| DVS capacitor current | $CS$; 2 A for 200 µF at 10 mV/µs | §3.5 |
| AVS saving | $1 - (V_2/V_1)^2$; 40 mV at 0.8 V is about 10% | §3.6 |
| Load-switch soft-start energy | $\tfrac12CV^2$ in the switch, whatever the ramp | §3.7 |
| Gating break-even | $(CV^2 + E_{state})/P_{leak}$ | §3.8 |
| Application-processor PMIC (as of Nov 2026) | 3–6 bucks of 2–4 A and 4–11 LDOs of 0.3–0.5 A per device | [1], [3], [4] |
| Wearable converter quiescent current (as of Nov 2026) | 60 nA (a single buck) to about 1 µA (a PMIC with two bucks in auto mode) | [2], [5] |
| DVS slew rates (as of Nov 2026) | about 0.3–33 mV/µs, programmable; 1–40 mV/µs over AVSBus | [4], [8] |
| DVS voltage resolution (as of Nov 2026) | 25 mV to 1 mV per step | [3], [4], [8] |
| Control buses (as of Nov 2026) | I²C at 0.1–1 MHz (3.4 MHz high-speed); SPMI to 26 MHz; AVSBus to 50 MHz | [3], [4], [6], [7] |

### [22-09 · Batteries, Charging and Fuel Gauging](../courses/22-power-electronics-and-energy-conversion/chapters/22-09-batteries-charging-fuel-gauging.md)

| Quantity | Typical value | Source |
|---|---|---|
| Cell voltage | $E = -\Delta G/(nF)$; 3.6–3.85 V nominal for cobalt- and nickel-based cells, about 3.2–3.3 V for LFP | §3.1, [1], [11] |
| Charge voltage | 4.20 V (± 0.05 V) typical; JEITA warm band ≤ 4.10 V | [3], [11], [12], [21] |
| Discharge cut-off | 2.5–3.0 V | [11], [12] |
| Specific energy (as of Nov 2026) | 230–260 Wh/kg for high-energy 21700 cells; 150–220 Wh/kg chemistry range | [1], [11], [27] |
| Internal resistance (as of Nov 2026) | 10 mΩ (1 kHz) and 16 mΩ (DC pulse) for a 4.2 Ah 21700; < 0.5 Ω (1 kHz) for a 50 mAh coin cell | [11], [12] |
| CV time constant | $RC_{eff}$, with $C_{eff} = Q/(dV_{OC}/dz)$ | §3.4 |
| Charger termination and precharge | about 10% of $I_{cc}$; precharge 10–20% of $I_{cc}$ below 2.5–3.0 V | [14], [15] |
| Linear-charger efficiency | $V_{bat}/V_{in}$ | §3.5 |
| 2:1 switched-capacitor charger (as of Nov 2026) | 98.1% peak at up to 8 A (vendor claim) | [16] |
| Gauge relaxation criterion | $dV/dt$ < 4 µV/s; about 30 min to hours | [6], [19] |
| Cycle life (as of Nov 2026) | 500–1500 full cycles to 80% for consumer nickel-based cells; 2500–9000 for LFP in lab tests | [8], [13], [18] |
| Self-discharge | about 1–2% per month, plus about 3% per month for a protection circuit [Industry estimate] | [25] |
| Calendar fade | $\propto \sqrt t$; faster at high SOC and temperature; store at 30–50% SOC | §3.7, [17], [21] |
| Cold | 71% of 25 °C capacity at −20 °C and 1C for one 18650 cell | [13] |

### [22-10 · Datacenter Power Delivery](../courses/22-power-electronics-and-energy-conversion/chapters/22-10-datacenter-power-delivery.md)

| Quantity | Typical value | Source |
|---|---|---|
| Conductor loss | $P^2R/V^2$; a uniformly tapped busbar loses $I^2R/3$ | §3.2 |
| Multiphase summed ripple | $(V_{in}T/L)(ND - m)(m + 1 - ND)/N$; zero when $ND$ is an integer | §3.4 |
| Load line | $R_{LL} = (V_{max} - V_{min})/I_{max}$ | §3.5 |
| Target impedance, first droop | $Z_t = \Delta V/\Delta I$; first droop $\approx \Delta I\sqrt{L/C}$ at $1/(4f_0)$ | §3.6 |
| AI rack power (as of Nov 2026) | about 120 kW (GB200 NVL72) today; racks of 800 kW to 1 MW and more specified | [1], [6] |
| Rack distribution (as of Nov 2026) | 48–54 V DC (ORv3: 51 V nominal, 46–52 V); ±400 V or 800 V DC for megawatt racks | [2], [5], [6], [33] |
| Rack PSU and bus converter efficiency (as of Nov 2026) | PSU 97.5% peak; 48 → 12 V converters 96.6–97.5%; OCP requirement 97% at full load | [8], [16], [19] |
| Smart power stage (as of Nov 2026) | 60–90 A per phase in a 5 × 6 mm package, switching up to 1–1.25 MHz | [21], [34], [35] |
| Processor load lines (as of Nov 2026) | about 1 mΩ for 200–300 A processors; ±20–22 mV tolerance band | [22], [23] |
| Client processor PDN | path inductance ~1 nH, current slew ~20 A/ns | [24] |
| Accelerator power (as of Nov 2026) | up to 1400 W per GPU; 2× rated power for up to 20 µs in OAM specs | [10], [26] |
| Busbar design | ≤ 30 °C rise; about 1.5–2.5 A/mm² for single bars (larger bars lower) | [30] |
| PUE (2025) | 1.09 (Google fleet) against 1.54 (industry survey) | [18] |

### [22-11 · Electric Machines and Drives](../courses/22-power-electronics-and-energy-conversion/chapters/22-11-electric-machines.md)

| Quantity | Typical value | Source |
|---|---|---|
| DC motor | $E_a = k\omega$, $T = kI_a$, $\omega = V/k - R_aT/k^2$ | §3.2 |
| Synchronous speed | $n_s = 120f/P$ rpm: 1500 (50 Hz) or 1800 (60 Hz) for 4 poles | §3.3 |
| Induction power split | rotor loss $sP_{ag}$, mechanical $(1 - s)P_{ag}$; rated slip about 1–5% | §3.4, [10] |
| Synchronous power | $P = 3VE_f\sin\delta/X_s$, pull-out at 90° | §3.5 |
| Inverter line voltage | $0.612mV_{dc}$ rms (sine-triangle); up to $0.707V_{dc}$ (space vector) | §3.6 |
| Fans and pumps | power ∝ speed³; 20% less speed saves about half the power | §3.6, [11] |
| Motors' share of electricity (as of Nov 2026) | 43–46% of global use (2006 data); 53% (2023, different method) | [1], [2] |
| IE classes, 11 kW 4-pole 50 Hz | IE1 87.6%, IE2 89.8%, IE3 91.4%, IE4 93.3% minimum | [4], [8], [22] |
| Regulation (as of Nov 2026) | EU: IE3 for 0.75–1000 kW since July 2021, IE4 for 75–200 kW since July 2023; US: IE4 levels for 100–250 hp from June 2027 | [4], [5], [6] |
| NEMA design B | starting current 600–700%, breakdown torque 175–300%, slip 1–5% of rated | [10] |
| Drive losses | 2–5% at nominal torque and speed, 10–30% at a quarter of each [Industry estimate] | [1] |
| EV traction (as of Nov 2026) | more than 90% PM synchronous; 1–2 kg of magnet per motor; peak motor efficiency above 97% | [12], [20], [21] |

### [22-12 · Power Systems Fundamentals](../courses/22-power-electronics-and-energy-conversion/chapters/22-12-power-systems-fundamentals.md)

| Quantity | Typical value | Source |
|---|---|---|
| Per-unit bases | $Z_b = V_b^2/S_b$, $I_b = S_b/(\sqrt3V_b)$ | §3.1 |
| Overhead lines (60 Hz) | 0.33–0.49 Ω/km; $Z_c$ 250–380 Ω; SIL 140 MW (230 kV) to 2250 MW (765 kV); $X/R$ 9–26 | [16] |
| Two-bus power | $P = V_1V_2\sin\delta/X$; stability limit at 90° | §3.3 |
| Ground fault | $3V_f/(Z_1 + Z_2 + Z_0)$ | §3.4 |
| RoCoF | $\Delta Pf_0/(2HS)$; above 1 Hz/s not manageable by protection | §3.5, [5] |
| Inertia constants | nuclear 5.9 s, gas and coal 4.2 s, hydro 2.7–3.7 s, wind and solar 0 | [5] |
| Governor droop | typically 5% | §3.5 |
| US generation mix, 2025 | gas 40.9%, nuclear 17.7%, coal 16.6%, wind 10.4%, utility solar 6.8%, hydro 5.5% | [4] |
| US datacenters (as of Nov 2026) | 192 TWh, 4.7% of US electricity in 2024; 9.5–15.3% projected for 2030 | [2] |
| Global datacenters (as of Nov 2026) | about 415 TWh, 1.5% of world electricity in 2024; about 945 TWh in 2030 (base case) | [3] |
| US battery storage (as of Nov 2026) | 43.6 GW at end of 2025; nearly 52 GW by mid-2026 | [17] |
| Interconnection queue (as of Nov 2026) | about 2,061 GW active at end of 2025; request to operation over 5 years | [15] |

## [23 · Memory and Storage Technology](../courses/23-memory-and-storage-technology/README.md)

### [23-01 · The Memory Hierarchy and the Memory Wall](../courses/23-memory-and-storage-technology/chapters/23-01-memory-hierarchy-and-memory-wall.md)

| Quantity | Value | Source |
|---|---|---|
| Energy, 45 nm, 0.9 V | 32-bit FP multiply 3.7 pJ; 32-bit SRAM read (8 KB) 5 pJ; 32-bit DRAM read 640 pJ | Horowitz [1], [2] |
| On-chip wire | about 0.2 fF/µm; about 28 fJ per bit per mm at 0.75 V, random data | 19-05; §3.2 |
| HBM2 access energy (modelled, 2017) | about 3.9 pJ/bit: 2.24 on-die movement, 0.3 I/O, 1.21 activation | [3] |
| H200 HBM3E, measured (as of Oct 2026) | up to 248 W at 4.52 TB/s sustained (94% of 4.8 TB/s peak), about 35% of 700 W | [4] |
| GPU memory (as of Nov 2026) | H100 80 GB, 3.35 TB/s; H200 141 GB, 4.8 TB/s; Blackwell Ultra 288 GB, 8 TB/s; Rubin 288 GB HBM4, 19.2 TB/s | [5], [7] |
| HBM3E stack (as of Nov 2026) | 1,024 bits, above 9.2 Gb/s per pin, above 1.2 TB/s, 36 GB in 12-high | [8] |
| Desktop DDR5 (2024) | dual-channel DDR5-6000: 96 GB/s; "just over 70 ns" latency | [12] |
| DRAM latency trend | tRCD and tRC improved 30.5% and 26.3% while cost per bit fell 16× (11 years) | [11] |
| Memory wall | peak FLOPS 3.0×, DRAM bandwidth 1.6×, interconnect 1.4× per two years (20-year fit) | [9] |
| Little's law | data in flight = bandwidth × latency | §3.5 |
| KV cache | $2Ln_{kv}d_hb_{kv}$ bytes per token; decode attention intensity $2(n_q/n_{kv})/b_{kv}$ | §3.7 |

### [23-02 · SRAM Technology](../courses/23-memory-and-storage-technology/chapters/23-02-sram-technology.md)

| Quantity | Value | Source |
|---|---|---|
| HD bitcell (TSMC) | N5 0.021 µm²; N3 0.0199 µm²; N3E 0.021 µm²; N2 0.021 µm² | [1], [3] |
| HD bitcell (Intel) | Intel 7 0.0312 µm²; Intel 4 0.024 µm²; 18A 0.021 µm² | [1], [3] |
| Best macro density (ISSCC 2025) | 38.1 Mb/mm² (Intel 18A and TSMC N2), about 80% array efficiency | [1]; Example 23-02.1 |
| TSMC N2 SRAM gain | 11% over N3; N3 was 6% over N5 | [2] |
| Bitline length (TSMC) | 256 cells, extended to 512 at N2 for "close to 10 percent" density | [1] |
| Next shrink (reported, Dec 2026 paper) | A14 HD cell under 0.017 µm² | [4] |
| Sigma for a large array | about 6 to 7 (Example 23-02.3) | §3.3 |
| Read disturb, equal pass gate and pull-down | $(V_{DD} - V_{TN})(1 - 1/\sqrt2)$ | §3.4 |
| Dual-rail ranges (Synopsys 3 nm) | cells 540 mV–1.4 V; periphery to 380 mV | [1] |

### [23-03 · DRAM Cells, Arrays and Refresh](../courses/23-memory-and-storage-technology/chapters/23-03-dram-cells-arrays-refresh.md)

| Quantity | Typical value | Note |
|---|---|---|
| Storage capacitance | below 10 fF (D1z, D1a); 5–6 fF projected for D1c | [Industry estimate], TechInsights [8] |
| Bitline-to-cell capacitance ratio | about 5–10 | assumed in this chapter's examples |
| Read signal | tens of millivolts | §3.1 |
| Cell size | 6F²; about 1,500 nm² at F = 15.9 nm | §3.5, [7] |
| DDR5 supplies | $V_{DD}$ = 1.1 V, $V_{PP}$ = 1.8 V | Micron data sheet [1] |
| Refresh window and interval | DDR4: 64 ms, 7.8125 µs (≤ 85 °C); DDR5: 32 ms, 3.906 µs | [1], [2] |
| DDR4 tRFC1 | 160 / 260 / 350 / 350 ns for 2 / 4 / 8 / 16 Gb | [2] |
| Core timings | DDR4-3200: 13.75 ns; DDR5-6400: 16 ns (tAA = tRCD = tRP) | [1], [2] |
| Refresh overhead | a few percent; doubles when hot | Example 23-03.7 |
| Row-hammer threshold | 139K (DDR3, 2014); down to 4.8k per aggressor (LPDDR4, 2020) | [5], [6] |
| Banks per device | DDR4 x8: 16 in 4 groups; DDR5 x8: 32 in 8 groups | [1], [2] |

### [23-04 · DRAM Interfaces: DDR, LPDDR and GDDR](../courses/23-memory-and-storage-technology/chapters/23-04-dram-interfaces.md)

| Quantity | Typical value | Note |
|---|---|---|
| Prefetch | DDR4 8n; DDR5 16n; LPDDR5X 16n or 32n | [1], [2], [4] |
| Core column rate | about 300–600 MHz | Example 23-04.1 |
| UI | 156 ps at 6400 MT/s; 104 ps at 9600 MT/s | |
| I/O supply | DDR4 1.2 V POD; DDR5 1.1 V POD; LPDDR5X 0.5 V LVSTL | [1], [2], [4] |
| Termination and driver | tens of ohms (DDR4: 34–240 Ω ODT, 34 or 48 Ω drivers) | [2] |
| Trace delay | about 6–7 ps/mm on FR-4-class boards | Example 23-04.6 (assumed permittivity) |
| Top pin rates (as of Nov 2026) | DDR5 MRDIMM 8800 MT/s (JEDEC bins to 8800); LPDDR5X 10.7 Gb/s; GDDR7 28–30 Gb/s shipping | [9], [8], [12], [14], [15] |
| Peak bandwidth | DDR5-6400 DIMM 51.2 GB/s; LPDDR5X x16 channel 19.2 GB/s; RTX 5090 1.79 TB/s | Example 23-04.2 |
| PAM eye penalty | PAM3 6.02 dB; PAM4 9.54 dB | §3.7 |

### [23-05 · HBM in Depth](../courses/23-memory-and-storage-technology/chapters/23-05-hbm-in-depth.md)

| Quantity | Typical value | Note |
|---|---|---|
| Interface width | 1,024 bits (HBM3/3E); 2,048 bits (HBM4) | [1], [2] |
| Channels | 16 × 2 pseudo-channels (HBM3); 32 × 2 (HBM4) | [1], [2] |
| Pin rate | 6.4 Gb/s (HBM3 spec); 9.6 Gb/s (HBM3E); 8 Gb/s (HBM4 spec), 10–13 Gb/s shipping or announced | [1], [2], [4], [6], [7] |
| Bandwidth per stack | 0.82 TB/s (HBM3) → 1.2 (HBM3E) → 2–3.3 TB/s (HBM4) | Example 23-05.1 |
| Capacity per stack | 24–36 GB common; up to 48–64 GB | [2], [4], [5] |
| Stack height | 775 µm (HBM4, reported) | [3], [9] |
| TSVs per die | over 20,000 (SK hynix HBM4) | [9] |
| Wafers per bit vs conventional DRAM | about 2.5–2.9× (derived from TrendForce shares) | Example 23-05.7 |
| GPU memory | 288 GB at 8 TB/s (Blackwell Ultra); 288 GB at 19.2 TB/s (Rubin) | [10], [11] |

### [23-06 · NAND Flash and 3D NAND](../courses/23-memory-and-storage-technology/chapters/23-06-nand-flash-and-3d-nand.md)

| Quantity | Typical value | Note |
|---|---|---|
| Electrons per volt of threshold shift | about 100 | Example 23-06.1 (assumed 16 aF) |
| Program voltage | about 15–20 V | §3.2 |
| Endurance | falls with bits per cell | Die ratings are rarely published; Example 23-06.7's cycle counts are assumptions [7] |
| JESD218 retention | client 1 year at 30 °C; enterprise 3 months at 40 °C | [7] |
| Layer counts | 218 (Kioxia BiCS8) to 321 (SK hynix) in production by late 2024; 332 (BiCS10) sampling in Jul 2026 | [2], [3], [5] |
| Areal density | 28.5 Gb/mm² (Samsung 280-layer QLC); 37.6 Gb/mm² (Kioxia 2 Tb QLC) | [2], [6] |
| Interface speed | 3.2 Gb/s (V9) to 4.8 Gb/s (BiCS10) | [1], [5] |
| Page size | 16 KiB per plane (typical) | |

### [23-07 · SSD Controllers and Storage Systems](../courses/23-memory-and-storage-technology/chapters/23-07-ssd-controllers.md)

| Quantity | Typical value | Note |
|---|---|---|
| Mapping-table DRAM | about 1 GB per TB at 4 KiB units | §3.2 |
| Random-write amplification | 7.8 at 7% OP, 2.5 at 28% OP (FIFO model) | Example 23-07.3; real workloads lower |
| Enterprise endurance options | 1 DWPD (read-intensive), 3 DWPD (mixed use) | Kioxia CM10 [7]; Micron 9650 PRO 1 DWPD [6] |
| PCIe 5.0 x4 / PCIe 6.0 x4 | 15.75 GB/s / 32 GB/s raw per direction | [3], [4] |
| PCIe 6.0 enterprise SSD (Feb 2026) | 28 GB/s read, 14 GB/s write, 5.4 M IOPS, up to 25 W | Micron 9650 [5], [6] |
| Largest shipping SSD (May 2026) | 245 TB, up to 30 W | Micron 6600 ION [8] |
| JESD218 UBER targets | 10⁻¹⁵ client, 10⁻¹⁶ enterprise | 23-06 |

### [23-08 · Emerging Memories: MRAM, ReRAM, PCM, FeRAM](../courses/23-memory-and-storage-technology/chapters/23-08-emerging-memories.md)

| Quantity | Typical value | Note |
|---|---|---|
| Conductance quantum | 77.5 µS (12.9 kΩ) | Physical constant |
| MRAM thermal stability for 10-year retention | about 60 at operating temperature | Example 23-08.2 |
| MRAM write energy | about 1 pJ | Table 1 [1]; Example 23-08.3 |
| PCM RESET energy | a few pJ | Table 1 [1] |
| Endurance | MRAM/FeRAM 10¹⁵–10¹⁶; ReRAM 10¹²; PCM >10⁷; NOR 10⁴–10⁶ | Best demonstrated [1] |
| TSMC 16 nm automotive eMRAM | 1 M cycles, 20-year retention at 150 °C | [3] |
| TSMC eReRAM (2020) | 10-year retention at 125 °C, 10,000 cycles | [2] |
| Everspin 1 Gb STT-MRAM (28 nm) | 105.1 mm², 9.75 Mb/mm², 0.0396 µm² cell | [9] |

### [23-09 · Compute-in-Memory and Near-Memory Computing](../courses/23-memory-and-storage-technology/chapters/23-09-compute-in-memory.md)

| Quantity | Typical value | Note |
|---|---|---|
| DRAM read vs FP32 MAC (45 nm) | 640 pJ vs 4.6 pJ | Horowitz [9], 23-01 |
| Effective bits from device variation | about 4 at 5%, 6 at 1% | Example 23-09.3 |
| HBM-PIM (2021) | 1.2 TFLOPS FP16 per 6 GB stack | [1] |
| LPDDR5X-PIM (Hot Chips 2026) | 614 GB/s vs 76.8 GB/s; 3.01× tokens/s | [2] |
| IBM HERMES (PCM, 14 nm) | 64 cores of 256 × 256; 63.1 TOPS at 9.76 TOPS/W, 8-bit I/O in the one-phase (low-precision) mode; 16.1 TOPS at 2.48 TOPS/W in the four-phase mode used for its accuracy results | [4], [14] |
| EnCharge EN100 card | 200 TOPS at 8.25 W | [6] |
| d-Matrix Corsair card | 2,400 TFLOPS (8-bit dense), 600 W TDP | [7] |

## [24 · High-Speed I/O, Signal Integrity and Photonics](../courses/24-high-speed-io-signal-integrity-and-photonics/README.md)

### [24-01 · Signal Integrity Fundamentals](../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-01-signal-integrity-fundamentals.md)

| Quantity | Typical value | Source |
|---|---|---|
| Copper skin depth | 2.09 µm at 1 GHz; 0.52 µm at 16 GHz | 13-05; Example 24-01.2 |
| Conductor-loss rule | $36\sqrt{f_{GHz}}/(w_{mil}Z_0)$ dB/in, smooth copper | §3.2 |
| Dielectric-loss rule | $2.3\,f_{GHz}\tan\delta\sqrt{\varepsilon_r}$ dB/in | §3.3 |
| Laminate loss at 16 GHz (TI model, as of Jun 2023) | FR-4 1.289, Megtron 6 0.336 dB/in | [1] |
| PCB loss at 53 GHz (802.3dj working values, 2023–2024) | 1.27–1.8 dB/in; cabled host about 0.35 dB/in | [2], [3] |
| Package trace loss at 53 GHz | 0.15–0.21 dB/mm | [2] |
| PCIe 5.0 budget | 36 dB at 16 GHz | [1] |
| PCIe 6.0 budget | 32 dB at 16 GHz | [9] |
| PCIe 7.0 budget (as reported, 2024–2025) | 36 dB at 32 GHz | [7] |
| 802.3dj die-to-die budget | 40 dB at 53.125 GHz; passive copper about 1 m | [5] |
| PCIe trace impedance | 85 Ω differential (42.5 Ω per line) | [8] |

### [24-02 · Eye Diagrams, Jitter and BER](../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-02-eye-diagrams-jitter-ber.md)

| Quantity | Value | Source |
|---|---|---|
| $Q^{-1}$ at 10⁻⁶, 10⁻⁹, 10⁻¹², 10⁻¹⁵ | 4.75, 6.00, 7.03, 7.94 | Example 24-02.1 |
| Dual-Dirac multiplier at 10⁻¹² | 14.07 | [1] |
| Zero-error test length at 95% | 3/BER bits | §3.8, [9] |
| PCIe reference-clock limit (as reported) | 0.15 ps (5.0), 0.1 ps (6.0), 67 fs (7.0) rms | [3], [4] |
| PCIe 6.0/7.0 error target | FBER 10⁻⁶ before FEC | [7], [8] |
| KP4 FEC input BER for a 10⁻¹³-equivalent frame loss ratio | about 3 × 10⁻⁴ random; under 2 × 10⁻⁴ with bursts | [8] |
| 802.3dj DER₀ (as adopted, 2023) | 2 × 10⁻⁴ backplane/cable; 2.67 × 10⁻⁵ AUIs combined | [6] |
| 802.3dj jitter corner | 4 MHz (106.25 GBd/26,562.5) | [6] |
| COM pass threshold | 3 dB | [5] |

### [24-03 · SerDes Architecture and Equalization](../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-03-serdes-architecture.md)

| Quantity | Value | Source |
|---|---|---|
| CML against SST driver power, same swing and supply | 4 : 1 | §3.2 |
| Comparators per unrolled DFE tap | NRZ 2; PAM4 12 | §3.5 |
| Bang-bang detector gain | about 0.8/σ per UI | §3.7 |
| PAM4 break-even loss at its Nyquist frequency | 9.5–23 dB (dielectric to conductor) | §3.9 |
| Long-reach SerDes, 2021–22 | 112 Gb/s, >40–50 dB, 4.5–6 pJ/b (boundary not stated in the abstracts) | [3] |
| Long-reach SerDes, 2024–26 | 212–224 Gb/s, 40–55 dB, about 2–3 pJ/b analog | [1], [2] |
| DSP's share of a DSP SerDes | about half (4.1 against 1.89 pJ/b at 128 Gb/s) | [2] |
| Time-interleaved ADCs | 6–7 bits, 64- to 128-way | [1], [4], [R-235] |

### [24-04 · DSP-Based SerDes and FEC](../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-04-dsp-serdes-and-fec.md)

| Quantity | Value | Source |
|---|---|---|
| Jitter-limited SNR | $-20\log_{10}(2\pi f\sigma_t)$; 35.6 dB at 26.56 GHz and 100 fs | §3.2 |
| SerDes ADCs | 6–7 bits, 64- to 128-way interleaved | [R-235], [R-507], [R-509], [R-511] |
| MLSD gain on $h = (1, \alpha)$, α ≤ 1 | $10\log_{10}(1 + \alpha^2)$, 3 dB at α = 1 | §3.4 |
| KP4 NCG (BPSK convention) | about 6.8 dB, 2.2 × 10⁻⁴ to 10⁻¹⁵ | Example 24-04.7 |
| Inner-code threshold and rate | 4.85 × 10⁻³; 113.4375 GBd lanes | [R-513] |
| RS(544,514) latency, 100 G lanes | about 151 ns (51 + 100), 212 ns interleaved | [R-512] |
| PCIe 6.0 FEC target | "<10ns" TX + RX; flit 2 ns at x16 | [R-514] |
| DSP share of SerDes power | about half (4.1 against 1.89 pJ/b) | [R-509] |

### [24-05 · Interconnect Standards: PCIe, CXL and Ethernet](../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-05-pcie-cxl-ethernet.md)

| Quantity | Value | Source |
|---|---|---|
| PCIe rates | 2.5, 5, 8, 16, 32, 64, 128 GT/s; 256 targeted for 2028 | [R-216], [R-515] |
| PCIe x16 raw bidirectional | 256 GB/s (6.0), 512 GB/s (7.0), 1 TB/s (8.0 target) | [R-216] |
| Encodings | 8b/10b 80%; 128b/130b 98.5%; flit 236 of 256 bytes for TLPs | §3.1 |
| CXL generations | 2.0 (2020) pooling; 3.0 (2022) 64 GT/s fabrics; 4.0 (Nov 2025) 128 GT/s | [R-217], [R-516] |
| Ethernet 200 Gb/s lane | 212.5 Gb/s, 106.25 GBd PAM4, 53.125 GHz Nyquist | [R-234] |
| Spec to product lag | at least 12–18 months (journalist's estimate) | [R-515] |
| UALink | 200G 1.0 April 2025 (200 GT/s lanes, x1–x4 ports, up to 1,024 accelerators); 2.0-series specifications April 2026 | [R-518], [R-523] |
| Ultra Ethernet | 1.0 June 2025; 1.1 October 2026 | [R-517] |

### [24-06 · Die-to-Die Links, Memory PHYs and Scale-Up Fabrics](../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-06-d2d-memory-phys-scale-up.md)

| Quantity | Value | Source |
|---|---|---|
| Unterminated wire energy | $CV^2/4$ per bit; about 0.02–0.05 pJ/b for package wires | §3.1, 23-05 |
| UCIe energy targets | 0.5 (S), 0.25 (A), under 0.05 (3D at 9 µm) pJ/b | [R-524] |
| UCIe rates | to 32 GT/s (1.x, 2.0); 48 and 64 GT/s (3.0, Aug 2025) | [R-524] |
| UCIe-A shoreline target | 165–1,317 GB/s/mm | [R-524] |
| UCIe latency target | under 2 ns TX + RX | [R-524] |
| HBM4 | 2048 bits × 8 Gb/s = 2 TB/s per stack (JEDEC, Apr 2025) | [R-520] |
| NVLink 5 | 18 links × 100 GB/s = 1.8 TB/s per GPU (both directions) | [R-521] |
| UALink 200G 1.0 | x1–x4 at 200 GT/s per lane; 1,024 accelerators; under 4 m | [R-523] |

### [24-07 · Photonics Fundamentals](../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-07-photonics-fundamentals.md)

| Quantity | Value | Source |
|---|---|---|
| Single-mode cabled loss (a G.652.D fiber's datasheet) | ≤ 0.36 dB/km at 1310 nm; ≤ 0.22 dB/km at 1550 nm | [R-526] |
| Dispersion (G.652.D) | ≤ 3.5 ps/(nm·km) at 1285–1330 nm; ≤ 18 at 1550 nm | [R-526] |
| Fiber latency | 4.9 µs/km (≈ 5 ns/m) | §3.1 |
| Multimode EMB at 850 nm | 2,000 (OM3), 4,700 (OM4/OM5) MHz·km | [R-526] |
| Ideal responsivity | 0.69 / 1.06 / 1.25 A/W at 850 / 1310 / 1550 nm | Example 24-07.1 |
| Silicon depletion modulator | $V_\pi L$ ≈ 2 V·cm; MZM ≈ 200 fJ/bit; ring < 40 fJ/bit | [R-530] |
| TFLN modulator | ≈ 2 V·cm, < 0.5 dB loss, ≈ 100 GHz | [R-530] |
| PAM4 optical penalty | 4.77 dB (optical) | §3.5 |
| CWDM4 grid | 1271, 1291, 1311, 1331 nm | [R-529] |
| 800G PMD reaches (802.3df, 2023 draft text) | VR8 50 m, SR8 100 m, DR8 500 m, DR8-2 2 km | [R-528] |

### [24-08 · Silicon Photonics and Optical Transceivers](../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-08-silicon-photonics.md)

| Quantity | Value | Source |
|---|---|---|
| Cutoff wavelengths | Si 1107 nm; Ge ≈ 1550 nm (direct); InGaAs ≈ 1650 nm | Example 24-08.1 |
| Indices near 1550 nm | Si ≈ 3.48, SiO₂ ≈ 1.44 | Chrostowski & Hochberg |
| Single-mode silicon thickness | < 0.25 µm at 1550 nm | Example 24-08.2 |
| Single-mode fiber MFD | 9.2 µm at 1310 nm | [R-526] |
| Bare fiber-to-silicon coupling | ≈ −13 dB without mode conversion | Example 24-08.3 |
| Grating coupler steer | ≈ 0.1°/nm | Example 24-08.4 |
| 800G twin-port DR4 module (as of Nov 2026) | 16 W typical, 17 W max | [R-533] |
| 1.6T twin-port DR4 module (as of Nov 2026) | 33.5 W max | [R-534] |
| Pluggable energy per bit | ≈ 20 pJ/bit | Example 24-08.8 |
| Retimed vs linear | $1/Q^2$ adds linearly; BER adds when retimed | §3.8 |

### [24-09 · Linear-Drive and Co-Packaged Optics](../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-09-lpo-and-cpo.md)

Perishable rows are as of Nov 2026; the date column gives the source's own date.

| Quantity | Value | Dated | Source |
|---|---|---|---|
| Pluggable electrical path at 200 Gb/s | up to ≈ 22 dB; CPO ≈ 4 dB | NVIDIA, Aug 2025 | [R-543] |
| Retimed pluggable, 800 Gb/s | 16–18 W per port, 20–22.5 pJ/bit | datasheet read Nov 2026; press Oct 2025 | [R-533], [R-545] |
| Broadcom CPO per 800G port | 6.4 → 5.5 → 3.5 W (Humboldt → Bailly → Davisson) | Oct 2025 | [R-545] |
| LPO MSA specifications | 100G-DR-LPO, 400G-FR4-LPO | Mar 2025, Sep 2025 | [R-541] |
| ELSFP power classes | 11 to 26 dBm per wavelength per core | OIF-ELSFP-02.0, Jan 2025 | [R-548] |
| Spectrum-6 / Davisson switch | 102.4 Tb/s, 512 lanes of 200 Gb/s | 2026 / Oct 2025 | [R-550], [R-545] |
| Zero-failure 95% bound | $\lambda_U = 3.00/T$ | timeless | §3.4 |
| Next lane rate | 400 Gb/s per lane in development | OFC 2026 | [R-551] |

## [25 · Semiconductor Fabrication, Packaging, Test and Reliability](../courses/25-fabrication-packaging-test-and-reliability/README.md)

### [25-01 · Process Flow Overview: FEOL, MOL and BEOL](../courses/25-fabrication-packaging-test-and-reliability/chapters/25-01-process-flow-overview.md)

Perishable rows are as of Nov 2026; the date column gives the source's own date.

| Quantity | Value | Dated | Source |
|---|---|---|---|
| Process steps per wafer | 400–1,400 | 2021 | [R-020] |
| Wafer cycle time | ≈ 12 weeks average; 14–20 weeks advanced | 2021 | [R-020] |
| Days per mask layer | ≈ 1–1.5 | 2017 | [R-020] |
| EUV layers | N5 "over 10", N3 "over 20" | Oct 2020 | [R-558] |
| TSMC capacity and shipments | > 17 M and ≈ 15 M 12-inch-equivalent wafers in 2025 | Apr 2026 | [R-559] |
| Silicon consumed by oxidation | 0.44 × oxide thickness | timeless | §3.2 |
| Bulk copper resistivity | 1.68 µΩ·cm | timeless | 04-05 |
| BEOL processing temperature | about 400 °C or below | timeless | §3.1 |
| Wafer area, 300 mm | 707 cm² | timeless | Example 25-01.1 |

### [25-02 · Lithography: DUV, Multipatterning, EUV and High-NA](../courses/25-fabrication-packaging-test-and-reliability/chapters/25-02-lithography.md)

Perishable rows are as of Nov 2026; the date column gives the source's own date.

| Quantity | Value | Dated | Source |
|---|---|---|---|
| Resolution floor, dense lines | $k_1$ = 0.25 | timeless | §3.2 |
| ArF immersion scanner | 1.35 NA, ≤ 38 nm, ≥ 310 wph | Nov 2026 page | [R-562] |
| Low-NA EUV (NXE:3800E) | 0.33 NA, 13 nm, ≥ 220 wph at 30 mJ/cm² | Nov 2026 page | [R-560] |
| High-NA EUV (EXE:5200B) | 0.55 NA, 8 nm, ≥ 175 wph at 50 mJ/cm² | Nov 2026 page | [R-561] |
| EUV scanner prices | ≈ €150–200 M Low-NA; €350 M–$400 M High-NA | 2021–2026 reports | [R-564] |
| EUV source power | ≈ 600 W production; 1,000 W demonstrated | Feb 2026 | [R-567] |
| ASML EUV systems recognized | 48 in 2025 (4 High-NA) | 2025 annual report | [R-563] |
| Photon energy | 91.8 eV (13.5 nm), 6.42 eV (193 nm) | timeless | §3.6 |
| Field size | 26 × 33 mm; High-NA 26 × 16.5 mm | Nov 2026 | [R-561] |

### [25-03 · Deposition, Etch, CMP, Implant and Metrology](../courses/25-fabrication-packaging-test-and-reliability/chapters/25-03-deposition-etch-cmp-implant-metrology.md)

Perishable rows are as of Nov 2026; the date column gives the source's own date.

| Quantity | Value | Dated | Source |
|---|---|---|---|
| Wafer fab equipment market | $116.9 B (2025); $143.9 B forecast (2026) | Jul 2026 | [R-568] |
| WFE 2026 by application | foundry/logic $78.0 B, DRAM $38.8 B, NAND $13.9 B | Jul 2026 | [R-568] |
| IC equipment market (TechInsights) | $136.2 B (2025), +13% | Jul 2026 | [R-569] |
| Top five equipment suppliers | ASML, Applied Materials, Lam Research, Tokyo Electron, KLA | 2025 | [R-569] |
| Boron intrinsic diffusivity | $D_0$ = 0.76 cm²/s, $E_a$ = 3.46 eV | textbook | §3.7 |
| Faraday's constant | 96,485 C/mol | timeless | §3.3 |
| Si and Ge lattice constants | 0.5431 nm and 0.5658 nm | timeless | §3.3 |
| Gauge acceptance | $P/T \lesssim 0.1$ good, $\gtrsim 0.3$ inadequate | rule of thumb | §3.8 |

### [25-04 · Yield Models and Die Cost](../courses/25-fabrication-packaging-test-and-reliability/chapters/25-04-yield-and-die-cost.md)

Perishable rows are as of Nov 2026; the date column gives the source's own date.

| Quantity | Value | Dated | Source |
|---|---|---|---|
| Leading-edge wafer prices (reported) | N3 ≈ $18.5–20 k; N2 ≈ $25–30 k+; Samsung 2 nm reportedly ≈ $20 k | 2023–2025 reports | [R-575], [R-574] |
| 2 nm fab capital (estimate) | ≈ $28 B for ≈ 50,000 wafer starts/month | Dec 2023 | [R-575] |
| Modelled 5 nm and 7 nm wafer prices (2020) | $16,988 and $9,346 | Apr 2020 | [R-576] |
| Absolute leading-edge $D_0$ | not published; TSMC shows only relative trends | 2025–2026 | [R-572] |
| Poisson yield at $AD_0$ = 1 | 0.368 | timeless | §3.2 |
| 300 mm dies per wafer, 100 mm² | ≈ 640 by formula | timeless | Example 25-04.3 |

### [25-05 · Foundries, PDKs and Specialty Processes](../courses/25-fabrication-packaging-test-and-reliability/chapters/25-05-foundries-pdks-specialty-processes.md)

Perishable rows are as of Nov 2026; the date column gives the source's own date.

| Quantity | Value | Dated | Source |
|---|---|---|---|
| Top-10 foundry revenue, 2Q26 | $53.49 B; TSMC 72.5%, Samsung 5.9%, SMIC 5.4% | Sep 2026 | [R-578] |
| TSMC node mix, 3Q26 | 2 nm 8%, 3 nm 33%, 5 nm 28%, 7 nm 10% of wafer revenue | Oct 2026 | [R-579] |
| TSMC process technologies and customers, 2025 | 305 technologies, 534 customers | Apr 2026 | [R-579] |
| MPW price, GF 22 nm FD-SOI via Europractice | €17,820/mm² standard, 4 mm² minimum | 2026 schedule | [R-581] |
| FD-SOI back-gate coupling | tens of mV per volt; rises as BOX thins | timeless | §3.5 |

### [25-06 · Packaging I: Wire Bond, Flip-Chip, Substrates, SiP and PoP](../courses/25-fabrication-packaging-test-and-reliability/chapters/25-06-packaging-fundamentals.md)

Perishable rows are as of Nov 2026; the date column gives the source's own date.

| Quantity | Value | Dated | Source |
|---|---|---|---|
| Top-10 OSAT revenue | $41.56 B (2024); ASE $18.54 B, Amkor $6.32 B, JCET $5 B | May 2025 | [R-582] |
| Build-up film supply | Ajinomoto, a reported ≥ 95% | Sep 2026 | [R-583] |
| Substrate makers | Unimicron, Ibiden, Shinko ≈ three-quarters | Sep 2026 | [R-583] |
| ABF price rise | ≈ 30% from 3Q26 | Sep 2026 | [R-583] |
| AI substrate size roadmap | 90 × 90 mm (2026) → 110 × 110 mm (2028) | Sep 2026 | [R-583] |
| InFO thickness reduction (A10) | ≈ 30% against PoP | Oct 2016 | [R-584] |
| Silicon CTE | ≈ 2.6 ppm/K | timeless | §3.5 |
| Bond-wire inductance | ≈ 1 nH per mm | timeless | 13-03 |

### [25-07 · Packaging II: 2.5D, 3D, Hybrid Bonding and Chiplets](../courses/25-fabrication-packaging-test-and-reliability/chapters/25-07-advanced-packaging-and-chiplets.md)

Perishable rows are as of Nov 2026; the date column gives the source's own date.

| Quantity | Value | Dated | Source |
|---|---|---|---|
| Scanner field | 26 × 33 mm = 858 mm² (TSMC quotes 830 mm² usable) | timeless / Apr 2025 | 25-02, [R-586] |
| CoWoS-S interposer | ≈ 3.3× reticle, ≈ 2,700–2,830 mm² | 2025 | [R-586] |
| CoWoS in volume | 5.5× reticle, up to 12 HBM stacks, yield > 98% (TSMC) | Apr 2026 | [R-587] |
| CoWoS roadmap | 9.5× (2027), 14× (2028), > 14× with 24 HBM5E (2029) | Apr 2026 | [R-587] |
| CoWoS capacity estimates | ≈ 0.9–1.4 × 10⁵ wafers/month for 2026 (TSMC only) | 2025–2026 | [R-588] |
| SoIC hybrid-bond pitch | 9 µm (2023) → 6 µm (2025) → 4.5 µm (2029) | Apr 2026 | [R-589] |
| Foveros Direct | 9 µm shipping (1H26); 3 µm described | Sep 2026 | [R-590] |
| EMIB bump pitch | 55 → 45 µm; 35 µm validated, 25 µm in test | Jul 2026 | [R-591] |
| Thermocompression bonding floor | ≈ 25 µm pitch (Samsung via ZDNet) **[Industry estimate]** | Nov 2026 | [R-592] |
| Research hybrid bonding | W2W 200 nm (overlay < 40 nm); D2W 1 µm | May 2026 | [R-593] |
| HBM stack height limit | 720 → 775 µm; ≈ 900 µm under discussion | 2026 | [R-594] |
| Copper and oxide expansion | ≈ 17 and ≈ 0.5 ppm/K | timeless | §3.5 |
| Overlay rule of thumb | ≈ pitch/4 | May 2026 | [R-593] |

### [25-08 · Thermal Engineering](../courses/25-fabrication-packaging-test-and-reliability/chapters/25-08-thermal-engineering.md)

Perishable rows are as of Nov 2026; the date column gives the source's own date.

| Quantity | Value | Dated | Source |
|---|---|---|---|
| Thermal conductivity | Si ≈ 150, Cu ≈ 400, Al alloys ≈ 150–235 W/(m·K); polymer TIMs a few W/(m·K) | timeless | [S1] (metals, silicon); TIMs typical |
| Convection coefficient | forced air ≈ 25–250; forced liquid ≈ 10²–2 × 10⁴ W/(m²·K) | timeless | [S1] |
| Water against air, per volume | ≈ 3,470× the heat capacity | timeless | §3.4 |
| NVIDIA B200 (HGX) | configurable up to 1,000 W per GPU | undated datasheet | [R-596] |
| NVIDIA B300 | up to 1,100 W (HGX, cloud listing); ≈ 1,400 W (report) | 2024–2025 | [R-596] |
| NVIDIA Rubin GPU | 1.8 kW and 2.3 kW power profiles (reported) | Feb 2026 | [R-597] |
| AMD MI350X / MI355X / MI455X | 1,000 W air / 1,400 W liquid / up to 2,500 W liquid (TBP) | 2025–2026 | [R-598] |
| AI racks (NVL72 class) | ≈ 120–142 kW; Rubin up to ≈ 230 kW reported | 2024–2026 | [R-600], [R-601] |
| Liquid-cooling penetration, AI chips | ≈ 33% (2025) → 53% (2026e) → ≈ 60% (2027e) | Aug 2026 | [R-602] |
| Junction limits | 95 / 105 / 125 °C by grade; 150 °C typical absolute maximum | 2025 | [R-604] |

### [25-09 · Reliability Physics](../courses/25-fabrication-packaging-test-and-reliability/chapters/25-09-reliability-physics.md)

Perishable rows are as of Nov 2026; the date column gives the source's own date.

| Quantity | Value | Dated | Source |
|---|---|---|---|
| Boltzmann constant | 8.617 × 10⁻⁵ eV/K | timeless | §3.1 |
| Cu EM activation energy (Cu/SiCN interface) | ≈ 0.90 eV; early-failure mode 0.83 eV | 2009 | [R-606] |
| Black's current exponent | 1 (growth) to 2 (nucleation); observed ≈ 1–3 | thesis review | [R-605] |
| NBTI time exponent | R-D theory 1/6–1/2; delayed measurements ≈ 0.2–0.3 | 2008 | [R-608] |
| HBM model | 100 pF, 1.5 kΩ | standard | 04-02 |
| HTOL confidence level in industrial FIT | 60% typical | Jun 2023 | [R-610] |
| JEDEC failure-mechanism reference | JEP122H, Sep 2016 | Sep 2016 | [R-609] |
| FIT | 1 failure per 10⁹ device-hours | definition | [R-610] |

### [25-10 · Qualification and Functional Safety](../courses/25-fabrication-packaging-test-and-reliability/chapters/25-10-qualification-and-functional-safety.md)

Perishable rows are as of Nov 2026; the date column gives the source's own date.

| Quantity | Value | Dated | Source |
|---|---|---|---|
| JEDEC qualification standard | JESD47N, current since Aug 2026 | Aug 2026 | [R-611] |
| AEC-Q100 revision | Rev J, 11 Aug 2023 | Aug 2023 | [R-612] |
| AEC-Q100 grades (ambient) | 0: −40/150; 1: −40/125; 2: −40/105; 3: −40/85 °C | Aug 2023 | [R-612] |
| TC, Grades 0 and 1 | −55/150 °C, 1,500 and 1,000 cycles | Aug 2023 | [R-612] |
| ISO 26262 | 2nd ed. Dec 2018; 3rd ed. at DIS ballot from Oct 2026, publication expected about 2027 | Oct 2026 | [R-613] |
| Hardware metrics ASIL B/C/D | SPFM ≥ 90/97/99%; LFM ≥ 60/80/90%; PMHF < 100/100/10 FIT | 2018 edition | [R-614] |
| Classical qualification sample | 3 lots × 77 units, zero failures (major stresses; not verified against Rev J) | — | 03-01, 03-05 |
| Components per car (illustrative) | ~10,000 semiconductor components | Jun 2022 | [R-615] |

### [25-11 · Test: ATE, Wafer Sort, Burn-In and Binning](../courses/25-fabrication-packaging-test-and-reliability/chapters/25-11-test-ate-sort-burn-in.md)

Perishable rows are as of Nov 2026; the date column gives the source's own date.

| Quantity | Value | Dated | Source |
|---|---|---|---|
| Historical cost of test | ≈ 2% of manufacturing cost | 2020–2021 | [R-618] |
| Cost of test on leading AI parts | toward 5–7% of ASP (one VC estimate) | May 2026 | [R-618] |
| ATE market CY2025 | ≈ $9.0 B, +50% (one VC estimate); two vendors ≈ 90%+ | May 2026 | [R-618] |
| Advantest tester share | 58% (CY2024) → 65% (CY2025), company estimate | 2026 | [R-616] |
| Advantest FY2025 | ¥1,128.6 B sales, 44.2% operating margin | Apr 2026 | [R-616] |
| Teradyne 2025 | $3.19 B revenue; ≈ 50% of "VIP compute" test (company belief) | Feb 2026 | [R-617] |
| FormFactor FY2025 | $785.0 M revenue (probe cards) | Feb 2026 | [R-619] |
| Multisite efficiency | defined $1 - (T_N - T_1)/((N - 1)T_1)$ | timeless | §3.2 |

### [25-12 · Post-Silicon Validation and Bring-Up](../courses/25-fabrication-packaging-test-and-reliability/chapters/25-12-post-silicon-validation.md)

Perishable rows are as of Nov 2026; the date column gives the source's own date.

| Quantity | Value | Dated | Source |
|---|---|---|---|
| First-silicon success, IC/ASIC | 14% (2024); 5% (2026; method changed in 2024) | Sep 2026 | [R-621], [R-622] |
| Projects behind schedule | 75% (2024); about three in four (2026) | Oct 2026 | [R-621], [R-622] |
| Leading-edge mask set | ≈ $10–20 M (3–5 nm) to $20–30 M (3 nm), toward $40 M beyond (estimates) | 2022–2026 | [R-623] |
| Design cost, large leading-edge chip | ≈ $650 M (3 nm, IBS); ≈ $725 M (large 2 nm chip, from scratch without IP); contested | 2020–2023 | [R-623] |
| Trace window | depth / clock frequency | timeless | §3.2 |
| Characterization sample for σ to ±10% | 194 parts at 95% (large-sample); 234 (exact) | timeless | §3.3 |

## [26 · Engineering Design and Professional Practice](../courses/26-engineering-design-and-professional-practice/README.md)

### [26-01 · Requirements, Specifications and the Design Process](../courses/26-engineering-design-and-professional-practice/chapters/26-01-requirements-and-specifications.md)

| Quantity | Value | Note |
|---|---|---|
| Two-sided Gaussian fraction outside ±3σ | **0.27**% (**2,700** ppm) | Timeless; **63** ppm at ±4σ, **0.57** ppm at ±5σ |
| RSS against worst case for $n$ equal contributions | $\sqrt n$ against $n$ | Timeless; independence assumed |
| Relative cost to fix a requirements error, by phase found | 1 (requirements); 3–8 (design); 7–16 (build); 21–78 (integration and test); 29 to more than 1,500 (operations) | NASA study of spacecraft-class systems, 2004 [R-625] **[Contested]** for chips |
| Verification methods | Test, analysis, inspection, demonstration | NASA SE Handbook, Rev 2 (2016) [R-626] |
| IC/ASIC projects behind schedule | About 75% (2024; 66% historically) | Wilson Research Group / Siemens EDA, 2024 [R-621] |
| IC/ASIC first-silicon success | 5% (2026); 14% (2024); about 30% historically | Wilson Research Group; methodology changed in 2024 [R-621], [R-622] |

### [26-02 · Design Reviews, Documentation and Standards Bodies](../courses/26-engineering-design-and-professional-practice/chapters/26-02-design-reviews-and-standards.md)

| Quantity | Value | Note |
|---|---|---|
| Fraction found by $k$ independent reviewers | $1 - (1 - p)^k$ | Timeless; independence assumed |
| Capture–recapture estimate | $\hat N = n_1n_2/m$ | Timeless; equal findability assumed |
| IEEE SA ballot thresholds | 75% return; 75% approval of Approve + Do Not Approve; invalid at ≥30% abstentions | IEEE SA Standards Board Operations Manual, approved January 2026 [R-632] |
| ETSI FRAND undertaking | Requested immediately once an essential IPR is brought to ETSI's attention; the owner is asked to give the irrevocable FRAND undertaking within three months | ETSI IPR Policy, clause 6.1 [R-633] |
| 3GPP releases | Rel-19 functional freeze September 2025, protocols stable 12 December 2025; Rel-20 projected March and June 2027 | 3GPP release table, as of November 2026 [R-634] |
| PCIe | 7.0 (128.0 GT/s) released to members 11 June 2025; 8.0 planned by 2028 | PCI-SIG, via secondary reprints [R-273] |

### [26-03 · Engineering Economics I: NRE, Die Cost, ASP and Gross Margin](../courses/26-engineering-design-and-professional-practice/chapters/26-03-engineering-economics-1.md)

| Quantity | Value | Note |
|---|---|---|
| FE Engineering Economics share | 5–8 of 110 questions | NCEES FE E&C specification [R-636] |
| Leading-edge wafer price estimates | About $18,500 (N3) and over $30,000 (N2) per wafer, as reported Dec 2023 to Oct 2024 | Industry estimates; no published price lists [R-575] |
| Leading-edge mask set and NRE | Mask set above $10 M at 7 nm, $10–40 M at 3–5 nm; NRE $30 M to over $100 M | Industry estimates [R-623] **[Contested]** |
| Gross margin, AI accelerator leader | NVIDIA FY2026 GAAP 71.1% (Q4 FY2026 75.0%) | Company results, 25 Feb 2026 [R-637] |
| Gross margin, leading foundry | TSMC 3Q26 66.4% | Company results [R-579] |
| Markup from margin | GM/(1 − GM) | Timeless |
| Capital recovery | $P(A/P, i, n) - S(A/F, i, n)$ | Timeless |

### [26-04 · Engineering Economics II: Build, Buy or License; Node; Chiplets; ASIC vs Merchant](../courses/26-engineering-design-and-professional-practice/chapters/26-04-engineering-economics-2.md)

- **Arm's revenue model** (FYE26, year to March 2026): royalties $2.61 B and licensing $2.31 B of $4.92 B revenue, so royalties were **53.0**% [R-638]. In Q2 FYE27 licensing grew 50% to $773 M while royalties were $670 M, **46.4**% of revenue [R-638] **[Established]**.
- **Royalty per chip rises with each architecture** (as of fiscal 2024): "the typical royalty fee for Armv9 was around double the fee for Armv8", and Arm's CEO said in July 2025 that its first Compute Subsystems were "delivering double the royalty of Armv9" [R-639] **[Established, company statements]**.
- **Synopsys Design IP:** **$1.75 B** in fiscal 2025, 24.8% of Synopsys revenue, down **8.1**% from **$1.91 B** [R-640]. Cadence's IP business grew "nearly 25%" in 2025 [R-641] **[Established]**.
- **Custom AI silicon:** Broadcom's AI semiconductor revenue (custom accelerators plus AI networking) was $16.7 B in its quarter ended Aug 2026, up 221% [R-642]; Marvell's custom revenue was $1.5 B in its fiscal 2026 [R-643] **[Established]**.
- **Wafer prices** (reports, 2023–2024): about $18,500–20,000 for N3 and $25,000–30,000 or more for N2 [R-575] **[Industry estimate]**.
- **Mask sets:** more than $10 M at 7 nm, approaching $40 M at 3 nm, by one analyst's estimate (SemiAnalysis, Jul 2022) [R-321] **[Industry estimate]**.
- **Density gains, N3 over N5:** "up to" 1.7× logic, 1.2× SRAM, 1.1× analog [R-360]; N3E's SRAM bitcell did not shrink from N5's 0.021 µm² [R-464] **[Industry estimate: vendor claims via press]**.
- **Chiplet cost:** AMD estimated the manufacturing cost of its first EPYC chiplet package at about 0.59 of a monolithic die's, with about 10% more silicon [R-360] **[Industry estimate]**.

### [26-05 · Schedule and Risk: Why Respins Happen](../courses/26-engineering-design-and-professional-practice/chapters/26-05-schedule-and-respin-risk.md)

- **First-silicon success** (IC/ASIC, Wilson Research Group/Siemens survey): 5% in 2026, 14% in 2024, about 30–33% from 2010 to 2020; the survey's recruitment method changed in 2024 [R-018] **[Industry estimate]**.
- **Respin causes (2024):** logic or functional flaws contributed to about half of IC/ASIC respins, analog issues to about 30% and reliability to about 21%, with clocking, timing, power, IR drop, firmware and safety each about 12–15% and security about 8%; a respin can have several causes [R-645] **[Industry estimate: read from the survey's chart]**.
- **Schedules:** about three out of four IC/ASIC and FPGA projects miss their original schedule, against about two in three historically [R-018, R-321, R-645] **[Industry estimate]**.
- **Verification share:** about 49% of IC/ASIC project time in 2026 [R-018] **[Industry estimate]**.
- **Fab time:** about 12 weeks on average and 14–20 weeks at advanced nodes (2021 report); about 1–1.5 days per mask layer and about 80–85 mask layers at 7 nm (2017 report) [R-020] **[Industry estimate]**.
- **Mask sets:** more than $10 M at 7 nm and toward $40 M at 3 nm by one analyst's estimate (SemiAnalysis, Jul 2022) [R-321] **[Industry estimate]**.
- **The cost of an escape:** Intel's 1994 FDIV replacement charge was $475 M pre-tax [R-321] **[Established]**.

### [26-06 · Engineering Team Structures and Sizing](../courses/26-engineering-design-and-professional-practice/chapters/26-06-team-structures-and-sizing.md)

- **R&D scale** (fiscal years 2025–2026): NVIDIA reported about 42,000 employees of whom about 31,000 work in R&D, with R&D at 8.6% of revenue; AMD, Intel and Qualcomm spent 23–26% of revenue on R&D [R-017] **[Established for R&D spending; Industry estimate for headcount splits]**.
- **Verification and design engineers:** about one-to-one at the mean peak on IC/ASIC projects, up to 5-to-1 in segments such as processors (2022 study); verification demand grew 6.2% a year against 2.7% for design over 2007–2022 [R-651] **[Industry estimate]**.
- **Design-services revenue mix:** GUC 24% NRE and 75% turnkey in 2025; Socionext about 19% NRE [R-652] **[Established]**.
- **Verification share of project time:** about 49% (2026 study) [R-018] **[Industry estimate]**.
- **Design cost of a leading-edge SoC:** IBS estimates (July 2022, via Arm's prospectus) of about $249 M at 7 nm and $725 M at 2 nm, disputed as 50–66% too high [R-019] **[Contested]**.

### [26-07 · Engineering Ethics and Professional Responsibility](../courses/26-engineering-design-and-professional-practice/chapters/26-07-engineering-ethics.md)

- **FE exam:** Ethics and Professional Practice, 4–6 questions (codes of ethics, intellectual property, safety) [R-655] **[Established]**.
- **Licensure:** a PE typically needs about four years of experience after an accredited degree, plus the FE and PE exams [R-655] **[Established]**.
- **ISO 26262 targets:** below 100 FIT (ASIL B, C) and below 10 FIT (ASIL D) for hardware failures violating a safety goal [R-614] **[Established]**.
- **Zero-failure bound:** 95% upper bound ≈ 3/T (the "rule of three"; exactly 2.996/T).
- **IP terms (US):** patents 20 years from filing; mask works 10 years, to the end of the calendar year [R-658] **[Established]**.
- **Export thresholds (ECCN 3A090, 2023):** TPP ≥ 4800, or TPP ≥ 1600 with performance density ≥ 5.92 [R-659] **[Established, as of Nov 2026; rules change often]**.
- **Case anchors:** Therac-25, six massive overdoses in 1985–1987 [R-656]; Challenger, launched over its contractor's engineers' objections (1986 report) [R-657]; Pentium FDIV, a $475 M replacement charge [R-321].

## [27 · System Architectures (Case-Study Course)](../courses/27-system-architectures/README.md)

### [27-01 · Method: Analyzing a System End to End](../courses/27-system-architectures/chapters/27-01-system-analysis-method.md)

| Quantity | Value | Note |
|---|---|---|
| LDO efficiency | at most $V_{out}/V_{in}$ | Timeless; 1.8 V from 3.7 V is at best 48.6% |
| Converters in series | efficiencies multiply | Timeless |
| Shadow price of a watt under a cap | $1/(3P_{dyn})$ per W | Timeless model, $P_{dyn} \propto f^3$ (14-01) |
| Decode speed | about bandwidth ÷ bytes of weights per token | Timeless model; ignores KV-cache traffic |
| HBM2 access energy | about 3.9 pJ/bit | O'Connor et al., MICRO 2017 [R-459] |
| Ridge point | peak rate ÷ bandwidth | Timeless |
| Burst duration | $\tau\ln[(T_\infty - T_0)/(T_\infty - T_{max})]$ | Timeless; one dominant time constant |

### [27-02 · The Smartphone SoC](../courses/27-system-architectures/chapters/27-02-smartphone-soc.md)

| Quantity | Value | Note |
|---|---|---|
| Smartphones shipped, 2025 | about 1.26 billion, +1.9% | IDC preliminary, Jan 2026 [R-666] |
| Flagship AP die area | about 99 (A19 Pro), 126 (8 Elite Gen 5), 141 mm² (Dimensity 9500) | Die-photo measurements, 2025 [R-664] **[Industry estimate]** |
| Phone memory bus | 64-bit, standard | [R-664] |
| LPDDR5X-10667, 64-bit | about 85 GB/s peak | Arithmetic from the data rate [R-662] |
| LPDDR6 data rate | 10,667–14,400 MT/s | JEDEC, July 2025, as reported [R-667] |
| Full-load CPU power | about 12 W (A19 Pro) to 19 W (8 Elite Gen 5) | Third-party measurement, Sep–Oct 2025 [R-664] **[Industry estimate]** |
| AP share of a flagship BOM | about 15% (A19 Pro, iPhone 17 Pro Max) | TechInsights, 2025 [R-665] **[Industry estimate]** |
| Memory share of a Pro iPhone BOM | about 10% (2025) to about 34% (3Q26) | TrendForce, Aug 2026 [R-665] **[Industry estimate]** |
| Flagship battery | 5,088 mAh (iPhone 17 Pro Max, eSIM) | Apple, as reported, Sep 2025 [R-669] |

### [27-03 · Wearables I: The Smartwatch](../courses/27-system-architectures/chapters/27-03-wearables-smartwatch.md)

| Quantity | Value | Note |
|---|---|---|
| Smartwatch battery energy | 1.461 Wh (Series 12, 46 mm), 2.444 Wh (Ultra 4) | Teardown labels, Oct 2026 [R-671] |
| Smartwatch battery capacity | 325 / 455 mAh (Pixel Watch 4, 41/45 mm); 390 / 445 mAh (Galaxy Watch9, 40/44 mm); 800 mAh (Galaxy Watch Ultra2) | Manufacturer specifications, 2025–2026 [R-672] |
| Rated life, everyday use | 24 h (Series 12); 50 h (Ultra 4); 30 / 40 h with always-on display (Pixel Watch 4) | Manufacturer profiles [R-670, R-672] |
| Implied average battery power | at most 60.9 mW (Series 12), 48.9 mW (Ultra 4) | Our arithmetic: rated energy over rated life |
| Implied average current | 10.8 mA (Pixel Watch 4, 41 mm), 11.4 mA (45 mm) | Our arithmetic: mAh over rated hours |
| Always-on display, multi-day watch | 16 days with gesture wake against 7 days always-on (fēnix 8 AMOLED, 47 mm), 2.29 times the average power | Garmin manual, Nov 2026 [R-674] |
| Peak and minimum brightness | 2000 nits peak, 1 nit minimum (Series 12); 3,000 nits (Galaxy Watch9) | [R-670, R-672] |
| Always-on refresh | down to 1 Hz (LTPO3) | Apple, Sep 2026 [R-670] |
| Watch application processors | Exynos W1000 (5 cores, 3 nm); Qualcomm SDW6100 (5 cores, 3 nm); W5+ Gen 1 (4 nm SoC with a 22 nm always-on co-processor) | [R-672, R-673] |
| Display share of watch BOM | 22.6–32.3% (four Android watches) | TechInsights, Jun 2026 [R-675] **[Industry estimate]** |
| AP share of a watch's visible BOM | 15.9% ($23.90 of $150.38, Series 11 5G) | TechInsights [R-675] **[Industry estimate]** |
| Smartwatch shipments | 34.8 million in Q1 2025 (+4.8%); about 37 million in Q2 2026 (−4.2%; derived from IDC's share and total) | IDC [R-675] **[Industry estimate]**; the two figures come from different IDC trackers whose definitions may differ |
| BLE timing | empty packet 80 µs (1M PHY); inter-frame space 150 µs; payload up to 251 octets | [R-676] (physics of the standard: stable) |
| Sleep-clock accuracy | at most ±500 ppm allowed; about 50 ppm with a crystal | [R-676] |
| BLE radio currents | about 3.6–5.3 mA receiving, 4.1–6.4 mA transmitting at 0 dBm | Vendor data sheets [R-406] |
| Accelerometer, low-power mode | about 10 µA (accelerometer only, 25 Hz) | Bosch BMI270 data sheet [R-074] |

### [27-04 · Wearables II: Earbuds and Smart Glasses / XR](../courses/27-system-architectures/chapters/27-04-wearables-earbuds-and-glasses.md)

| Quantity | Value | Note |
|---|---|---|
| Earbud listening time per charge (ANC on) | 8 h (AirPods Pro 3, Pixel Buds Pro 2); 6 h (Galaxy Buds4 Pro) | Manufacturer ratings, 2024–2026 [R-677] |
| Earbud and case cells | 61 / 530 mAh (Galaxy Buds4 Pro); 1.334 Wh case (AirPods Pro 3) | Samsung; iFixit [R-677] |
| ANC's cost in rated life | 7/6 (Samsung) to 12/8 (Google): ANC adds **17**–**50**% to average power | Our arithmetic on vendor ratings [R-677] |
| Earbud audio SoC compute | eNPU 64 GOPS; DSP 2 × 500 MHz + 1 × 250 MHz (Qualcomm S7 Pro Gen 1) | Vendor brief [R-678] **[Industry estimate]** |
| LC3 frame durations | 7.5 and 10 ms; 8–48 kHz; 20–400 bytes per frame (liblc3) | [R-678] |
| Glasses battery | 160 → 210 mAh (Ray-Ban Meta Gen 1 → Gen 2); 248 mAh, 960 mWh (Ray-Ban Display) | Meta; iFixit [R-679] |
| Glasses rated life | 8 h typical (Ray-Ban Meta Gen 2); 6 h mixed use (Ray-Ban Display) | Meta [R-679] |
| Display share of glasses BOM | 50.8% (Ray-Ban Display) | TechInsights, Jun 2026 [R-679] **[Industry estimate]** |
| Glasses power targets | about 200 mW average for all day on 3 Wh; about 1–2 W sustained at a ~40 °C touch limit | Meta research paper [R-682] |
| Headset pixels | 23 million (Vision Pro M5); 2 × 3,552 × 3,840 = **27** million (Galaxy XR) | Apple, Samsung [R-680] |
| Headset rated life | 2.5 h general use (Vision Pro M5); 2 h (Galaxy XR) | [R-680] |
| Headset weight | 750–800 g plus a 353 g battery (Vision Pro M5); 545 g plus 302 g (Galaxy XR) | [R-680] |
| Passthrough latency | "within 12 milliseconds" (Apple R1) | Apple, Oct 2025 [R-680] |
| Motion-to-photon target | under 15–20 ms ("broad consensus") | IEEE Network, 2018 [R-682] |

### [27-05 · The PC SoC](../courses/27-system-architectures/chapters/27-05-pc-soc.md)

Product figures are vendor specifications as of Nov 2026.

| Quantity | Value | Note |
|---|---|---|
| PC shipments | 284.7 million in 2025 (+8.1%); 62.7 million in Q3 2026 (−20.1%) | IDC [R-687] **[Industry estimate]** |
| Copilot+ PC minimum | NPU 40+ TOPS, 16 GB RAM, 256 GB storage | Microsoft [R-686] |
| NPU peak | up to 50 TOPS (Ryzen AI Max+ 395); up to 60 TOPS (Ryzen AI 400) | AMD [R-684] |
| Unified-memory bandwidth | 153 GB/s (M5); 170 GB/s (M6); 307 / 614 GB/s (M5 Pro / Max); 256 GB/s (Strix Halo, 256-bit LPDDR5X-8000) | Apple, AMD [R-683, R-684] |
| Unified-memory capacity | up to 128 GB (M5 Max, Strix Halo); 96 GB assignable to Strix Halo's GPU | [R-683, R-684] |
| Laptop chip power | default 55 W, configurable 45–120 W (Strix Halo) | AMD [R-684] |
| Laptop battery and rating | 72.4 Wh, up to 24 h video (14-inch MacBook Pro, M6): **3.02** W average | Apple; our arithmetic [R-683] |
| Memory on package | up to 40% lower PHY power, up to 250 mm² board area saved (Lunar Lake) | Intel, Hot Chips 2024 [R-685] **[Industry estimate]** |
| Modern Standby target | ≥ 9 days; DRIPS ≥ 98% "Excellent", ≥ 80% required | Microsoft [R-686] |
| Chiplet laptop packages | 3 dies on InFO-oS (Strix Halo); two dies in Apple's Fusion Architecture (M5 Pro/Max) | [R-683, R-684] |

### [27-06 · Automotive E/E Architecture and ADAS Compute](../courses/27-system-architectures/chapters/27-06-automotive-ee-architecture.md)

Product and market figures are as of Nov 2026.

| Quantity | Value | Note |
|---|---|---|
| Classic CAN | up to 135 bits per 8-byte frame; 270 µs at 500 kb/s | Arithmetic from the frame format (§3.2) |
| CAN FD | up to 64 data bytes, faster data phase | §3.2 |
| CAN XL | 20 Mb/s and higher; 1–2048 data bytes | CiA [R-689] |
| Automotive Ethernet standards | 10BASE-T1S in IEEE 802.3cg-2019; multi-gigabit PHYs in 802.3ch-2020; 25 Gb/s in 802.3cy-2023 | IEEE [R-689, R-700] |
| Camera link standard | MIPI A-PHY v2.1 (Sep 2026): up to 15 m, 24 and 32 Gb/s gears; IEEE 2977-2021 | MIPI [R-700] |
| ADAS SoC | 34 TOPS int8, 7 nm (EyeQ 6 High); 5 TOPS (EyeQ 6 Lite) | Mobileye [R-688] |
| Automated-driving tiers | "2x", "> 3x", "> 4x" EyeQ 6 High (SuperVision, Chauffeur, Drive), as Mobileye writes them | Mobileye [R-688] |
| Robotaxi compute | dual DRIVE AGX Thor SoCs (Hyperion) | NVIDIA [R-688] |
| Central-compute SoC | up to 1,000 INT8 TOPS, 64 GB LPDDR5X, up to 273 GB/s (DRIVE AGX Thor); up to 400 TOPS on 3 nm (Renesas R-Car X5H, sampling) | NVIDIA, Renesas [R-700] |
| ECU and harness consolidation | 17 → 7 ECUs and 2.6 km less wiring (Rivian R1, 2024); harness about 600 m shorter and about 30% lighter (BMW iX3, 2026) | Rivian; Infineon [R-700] |
| Automotive semiconductor market | US$ 74.4 B in 2025 (2024: 69.9 B) | TechInsights via Infineon [R-700] **[Industry estimate]** |
| Cyber-security and update rules | UN R155 and R156 in force 22 Jan 2021 | EU Official Journal [R-700] |
| Camera raw data | 2.88 Gb/s for 8 MP, 30 fps, 12-bit | Arithmetic (§3.3) |
| ASIL hardware targets | < 100 FIT (ASIL B, C), < 10 FIT (ASIL D) | ISO 26262-5 via 26-07 [R-614] |
| Distance per 100 ms | **1.4** m at 50 km/h, **3.6** m at 130 km/h | Arithmetic (§3.5) |

### [27-07 · The AI Datacenter Server and Rack](../courses/27-system-architectures/chapters/27-07-ai-datacenter-server-and-rack.md)

| Quantity | Typical value (as of Nov 2026) | Source |
|---|---|---|
| Rack-scale system | 72 GPUs and 36 CPUs in one NVLink domain, liquid-cooled (GB200 NVL72) | [R-690] |
| Rack HBM and bandwidth | 13.4 TB at 576 TB/s (GB200 NVL72); GB300 1.5× the HBM | [R-690] |
| Scale-up bandwidth per accelerator | 1.8 TB/s NVLink (both directions); 1.2 TB/s ICI (Ironwood) | [R-690], [R-693] |
| Accelerator memory | 288 GB at 8 TB/s (MI355X); 192 GB at 7.37 TB/s (Ironwood) | [R-692], [R-693] |
| Accelerator power | 1400 W typical board power (MI355X); 700 W TDP (H100, as used for Llama 3) | [R-692], [R-694] |
| Dense FP8 machine balance | about 625 FLOP/byte (MI355X, Ironwood) | Example 27-07.1 |
| Rack power | 120–142 kW for NVL72-class racks, depending on definition | [R-098], [R-600] |
| Next rack power step | 800 V DC for 1 MW racks from 2027 (NVIDIA plan) | [R-691] |
| PUE | 1.09 (Google fleet); 1.54 (2025 industry survey average) | [R-445] |
| Training MFU | 38–43% BF16 (Llama 3 405B on up to 16K H100) | [R-694] |
| Large-job interruptions | 419 unexpected in 54 days on up to 16K GPUs; more than 90% effective training time | [R-694] |
| Rules of thumb (timeless) | Training $\approx 6ND$ FLOP; ring all-reduce $2(p-1)S/(pB)$; Young's interval $\sqrt{2\delta M}$; job MTBF $m/N$ | §3 |

### [27-08 · Edge AI and IoT](../courses/27-system-architectures/chapters/27-08-edge-ai-and-iot.md)

| Quantity | Typical value (as of Nov 2026) | Source |
|---|---|---|
| Connected IoT devices | 21.1 billion expected at the end of 2025 (Wi-Fi 32%, Bluetooth 24% of connections) | [R-699] |
| Microcontroller NPU | Ethos-U85: 128–2048 MACs, up to 4 TOPs at 1 GHz, transformer support | [R-695] |
| Edge-AI benchmark | MLPerf Tiny: keyword spotting, visual wake words, image classification, anomaly detection; µJ per inference | [R-696] |
| Reference keyword-spotting model | 38.6K parameters, 52.5 KB, 90% accuracy target | [R-696] |
| LoRa demodulator SNR | −7.5 dB at SF7 to −20 dB at SF12, in 2.5 dB steps | [R-274] |
| LoRa radio currents (SX1276) | Transmit 29 mA at +13 dBm, 120 mA at +20 dBm; receive 10.8 mA; sleep 0.2 µA | [R-697] |
| EU 868 MHz duty cycles | 0.1%, 1% or 10% by sub-band; 1% for the common LoRaWAN channels | [R-698] |
| Community-network fair use | 30 s uplink airtime and 10 downlinks per node per day (The Things Network) | [R-698] |
| EU Cyber Resilience Act | In force 10 Dec 2024; reporting from 11 Sep 2026; main obligations from 11 Dec 2027; support at least 5 years | [R-312] |
| Rules of thumb (timeless) | DS-conv MAC ratio $1/C_{\text{out}} + 1/k^2$; $T_s = 2^{SF}/BW$; $C = 2E/(V_{\max}^2 - V_{\min}^2)$ | §3 |

## [28 · Technical Diligence and Engineering Leadership Fluency](../courses/28-technical-diligence-and-leadership-fluency/README.md)

### [28-01 · A Framework for Evaluating a Chip Company's Technology](../courses/28-technical-diligence-and-leadership-fluency/chapters/28-01-technology-evaluation-framework.md)

Figures are as of Nov 2026 unless dated otherwise.

| Quantity | Value | Note |
|---|---|---|
| IC/ASIC first-silicon success | 5% (2026), 14% (2024); about 30–33% in 2010–2020 and 24% in 2022 | Wilson Research Group / Siemens EDA [R-018, R-621, R-622] **[Established as reported; trend Contested]** |
| Projects behind schedule | about 75% (2024 and 2026), against about 66% historically | Same surveys [R-018, R-645] **[Established as reported]** |
| Spins before production (2024) | 1: 14%, 2: 25%, 3: 28%, 4: 16%, 5: 10%, 6: 4%; mean **2.95** | Chart readings [R-645]; mean derived (Example 28-01.4) |
| Leading-edge NRE and mask sets | NRE \$30–100 M+, mask set \$10–20 M at 3–5 nm (2026); about \$40 M mask sets at 3 nm (2022 estimate) | [R-623] **[Industry estimate; Contested]** |
| From-scratch design cost | about \$249 M (7 nm) and \$725 M (2 nm) | IBS via Arm's F-1 [R-019] **[Contested]** |
| R&D intensity | 8.6% (NVIDIA FY2026) to 26.1% (Intel FY2025) of revenue | 10-K filings [R-017] **[Established]** |
| Earn-out example | \$3.25 B upfront plus up to about \$2.25 B on revenue milestones (Marvell–Celestial AI, 2025) | [R-547] **[Established: company announcement]** |
| Evidence needed from 20% to 80% | likelihood ratio **16** | §3.3 |

### [28-02 · Validating Claims: TOPS/W, Benchmarks, Tapeout Status](../courses/28-technical-diligence-and-leadership-fluency/chapters/28-02-validating-claims.md)

Figures are as of Nov 2026 unless dated otherwise.

| Quantity | Value | Note |
|---|---|---|
| Ops per MAC | 2 (multiply + add) | Convention behind TOPS |
| Precision and sparsity factors | 2 per halving of operand width; 2 for 2:4 sparsity | §3.1; NVIDIA prints "sparse \| dense" [R-147] |
| Export-control TPP | $2 \times \text{MacTOPS} \times$ bit length; threshold 4800 (= 600 int8 TOPS) | ECCN 3A090 (2023 text) [R-659] **[Established]** |
| 45 nm energy (0.9 V) | 8-bit multiply 0.2 pJ, add 0.03 pJ; 32-bit SRAM read (8 KB) 5 pJ; 32-bit DRAM read 640 pJ | Horowitz, ISSCC 2014 [R-208, R-458] **[Established]** |
| HBM2 access energy | about 3.9 pJ/bit | O'Connor et al., MICRO-50, 2017 [R-459] **[Established, modeled]** |
| Efficiency to energy | 50 TOPS/W = **20** fJ/op; 100 TOPS/W = 10 fJ/op | §3.2 |
| Fab cycle time | 14–20 weeks at advanced nodes (2021); 1–1.5 days per mask layer (2017) | [R-020] **[Industry estimate]** |
| Qualification life test | 1000 h at $T_j \ge$ 125 °C, 3 lots × 77 units, 0 fails (JESD47G, 2009) | [R-061] **[Established]** |
| Best of N | $\operatorname{E}[Z_{(N)}]$ = 1.16, **1.54**, 1.87 for N = 5, 10, 20 | §3.4 |

### [28-03 · Maturity Scales for Silicon](../courses/28-technical-diligence-and-leadership-fluency/chapters/28-03-silicon-maturity-scales.md)

Figures are as of Nov 2026 unless dated otherwise.

| Quantity | Value | Note |
|---|---|---|
| Technology readiness levels | TRL 1 (research beginning) to TRL 9 (flight proven); TRL 6 a functional prototype | NASA [R-701] **[Established]** |
| First-silicon success | 5% (2026; about 3–8% given the sample), 14% (2024) of IC/ASIC projects | [R-018, R-622] **[Established as reported; trend Contested]** |
| Minimum HTOL qualification | 1000 h at $T_j \ge$ 125 °C, 3 lots × 77, 0 failures (JESD47G, 2009) | [R-061] **[Established]** |
| Arrhenius AF, 0.7 eV, 55 → 125 °C | **77.6** exact; 78.6 with rounded constants | [R-610] **[Established]** |
| FIT bound, minimum HTOL | about **51** FIT (60%), 128 FIT (90%) at 0.7 eV, 55 °C | Example 28-03.3 |
| Industrial confidence level | 60% "typical for industrial calculations" | TI [R-610] **[Established]** |
| AEC-Q100 grades | 0: −40 to +150 °C; 1: −40 to +125 °C; 2: −40 to +105 °C; 3: −40 to +85 °C ambient | Rev J [R-612] **[Established]** |

### [28-04 · Domain Question Banks I: Digital/CPU, AI Accelerators, Memory, Interconnect and Optics](../courses/28-technical-diligence-and-leadership-fluency/chapters/28-04-question-banks-digital-ai-memory-interconnect.md)

Figures are as of Nov 2026 unless dated otherwise.

| Quantity | Value | Note |
|---|---|---|
| N2 against N3E | power −25% to −30%, or performance +10% to +15% | Vendor claims via press [R-552] |
| HBM3E | 1,024-bit interface, up to 9.2–9.6 Gb/s, about 1.2 TB/s per stack | [R-475] |
| HBM4 (JEDEC) | 2,048-bit, up to 8 Gb/s, about 2 TB/s per stack, up to 64 GB | JESD270-4 [R-520] |
| HBM4 (announced) | 11.7 Gb/s, up to 13 Gb/s, "up to 3.3 TB/s" per stack | Samsung [R-475] |
| Memory power | about 248 W, 35% of 700 W, on H200 at 4.52 TB/s | Preprint measurement [R-459] **[Industry estimate]** |
| 200G-class SerDes | about 2–3 pJ/bit analog over 40–55 dB | ISSCC/VLSI papers [R-509] |
| UCIe targets | 0.5 pJ/bit (standard), 0.25 pJ/bit (advanced); shoreline up to about 1.3 TB/s per mm | [R-524] |
| Optics per port | 25 W pluggable against 5 W CPO (port speed not stated) | NVIDIA [R-543] **[Industry estimate]** |
| External laser classes | up to 26 dBm per fiber core | OIF ELSFP [R-548] |
| Decode intensity | about $2B/b_w$ FLOP per byte | §3.2 |

### [28-05 · Domain Question Banks II: Analog/Mixed-Signal, RF, Power, Packaging, Embedded](../courses/28-technical-diligence-and-leadership-fluency/chapters/28-05-question-banks-analog-rf-power-packaging-embedded.md)

Figures are as of Nov 2026 unless dated otherwise.

| Quantity | Value | Note |
|---|---|---|
| Ideal quantizer SNR | $6.02N + 1.76$ dB | 20-06 |
| Schreier figure on the 8kT·SNR line | about 191.8 dB at 300 K (ideal class-B bound 194.8 dB) | §3.1, from [R-336] and 20-06 |
| Best published Schreier figures | 189.2 dB (oversampled, 1 kHz); 186.8 dB (Nyquist); 173.3 dB (≥ 1 GS/s); 159.3 dB (≥ 10 GS/s) | Murmann survey, Aug 2026 [R-336] |
| Best Walden figure | 0.35 fJ/conv-step (unchanged since 2019) | [R-336] |
| Jitter-limited SNR | $-20\log_{10}(2\pi f_{in}\sigma_t)$; 50 fs at 2 GHz gives 64.0 dB | [R-332] |
| Best PLL jitter | about 16–21 fs integrated at 10–20 GHz | [R-350] **[Established]** |
| Ideal class-B efficiency | 78.5% at peak, $(\pi/4)\,10^{-\text{BO}/20}$ at back-off | 21-07 |
| GaN Doherty (published) | 38.5–46.5% drain efficiency at 6 dB back-off (one MMIC, 4.1–5.6 GHz); 51–53% at 8 W average | [R-385] **[Established]** |
| 3GPP EVM | 3.5% (256-QAM), 2.5% (1024-QAM, carriers up to 4.2 GHz; 2.8% above) at a base station | [R-275] **[Established: standard]** |
| 8 kW server PSU | 97.5% (vendor) or 98% (press); 100 W/in³ | [R-423] |
| Flip-chip, microbump, hybrid-bond pitch | about 130, 50 and 9 µm; hybrid bonding to 4.5 µm by 2029 | [R-589] **[Industry estimate: roadmap]** |
| MCU active current | 101 µA/MHz (CoreMark) against 55 µA/MHz (`while(1)`) | MSPM0G3507 [R-310] |
| MCU standby | 1.5 µA typical at 25 °C, 4 µA typical at 85 °C | MSPM0G3507 [R-310] |
| CR2032 | 225 mAh at 0.2 mA (Panasonic; other vendors differ) | [R-310] **[Established: data sheet]** |
| ISO 26262 SPFM | ≥ 90%, 97%, 99% (ASIL B, C, D) | [R-614] **[Established: standard]** |

### [28-06 · Red Flags and Green Flags](../courses/28-technical-diligence-and-leadership-fluency/chapters/28-06-red-and-green-flags.md)

Figures are as of Nov 2026 unless dated otherwise.

| Quantity | Value | Note |
|---|---|---|
| First-silicon success (IC/ASIC) | about 30% historically; 24% (2022); 14% (2024); 5% (2026) | Wilson/Siemens studies; recruitment changed between 2022 and 2024 [R-621], [R-321], [R-622] **[Industry estimate]** |
| Projects behind schedule | about 66% historically; 75% (2024) | [R-621] **[Industry estimate]** |
| Spins before production (2024) | 1: 14%, 2: 25%, 3: 28%, 4: 16%, 5: 10%, 6: 4% (chart readings) | [R-645] **[Industry estimate]** |
| Causes of respins (2024) | logic/functional about 50%, analog about 30% | [R-645] **[Industry estimate]** |
| Verification to design engineers | about 1:1 mean peak per project; up to about 5:1 in processors (2022) | [R-651] **[Industry estimate]** |
| ASIC design-service NRE share | GUC 24% (2025); Socionext 19.1% (FY2025) | [R-652] **[Established: company results]** |
| False alarms | $1 - (1 - f)^n \approx 1 - e^{-nf}$ | §3.2 |
| Effective number of customers | $1/\text{HHI}$ | §3.5 |

### [28-07 · Evaluating Engineering Teams](../courses/28-technical-diligence-and-leadership-fluency/chapters/28-07-evaluating-engineering-teams.md)

Figures are as of Nov 2026 unless dated otherwise.

| Quantity | Value | Note |
|---|---|---|
| First-silicon success (IC/ASIC) | about 30% historically; 14% (2024); 5% (2026) | [R-621], [R-321] **[Industry estimate]** |
| Projects behind schedule | 75% (2024) | [R-621] **[Industry estimate]** |
| Verification to design engineers | about 1:1 mean peak per project; up to about 5:1 in processors | 2022 study [R-651] **[Industry estimate]** |
| Design engineers' time on verification | 49% (2022) | [R-651] **[Industry estimate]** |
| Pairwise channels | $n(n - 1)/2$ | Brooks [R-650] |
| Beta posterior mean | $(\alpha_0 + s)/(n_0 + n)$ | §3.1 |
| Capability loss with $k$ owners | $q^k$ (independent departures) | §3.3 |

### [28-08 · Post-Acquisition Integration Risk](../courses/28-technical-diligence-and-leadership-fluency/chapters/28-08-integration-risk.md)

Figures are as of Nov 2026 unless dated otherwise.

| Quantity | Value | Note |
|---|---|---|
| Annuity factor, 5 years at 10% | 3.791 | §3.1 |
| Synergy value, late and partial | $\rho(1 + r)^{-d}$ of plan | §3.1 |
| Lost gross profit from delay (fixed window) | $m \cdot R \cdot d_m/12$ | §3.2 |
| Parallel paths | $1 - (1 - p_1)(1 - p_2)$ if independent | §3.3 |
| Arm royalty share of revenue | about 53% (FY2026: \$2,613M of \$4,920M) | Form 20-F [R-204] **[Established]** |
| Armv9 royalty against Armv8 | "around double" (fiscal 2024) | [R-639] **[Established: company statement]** |
| 3A090.a thresholds | TPP ≥ 4800, or TPP ≥ 1600 with density ≥ 5.92 | 2023 rule text [R-659] **[Established; not legal advice]** |
| Celestial AI terms | about $3.25B upfront, up to about $2.25B contingent (through FY2029) | Marvell [R-547] **[Established: company announcement]** |

### [28-09 · The Business ↔ Engineering Translation Table](../courses/28-technical-diligence-and-leadership-fluency/chapters/28-09-business-engineering-translation.md)

Figures are as of Nov 2026 unless dated otherwise.

| Quantity | Value | Note |
|---|---|---|
| N3 and N2 wafer prices | about \$18,500 (IBS: about \$20,000) and above \$30,000 per 300 mm wafer (reported 2023–2024) | Reports, not price lists [R-575] **[Industry estimate]** |
| Leading-edge mask set | about \$10–20M (2026 estimate) to about \$40M (2022 estimate) at 3–5 nm | [R-321], [R-623] **[Industry estimate; Contested]** |
| Die-cost elasticity to area | about $1 + AD_0$, plus an edge term | §3.2 |
| Gross margin | $1 - (C_{\text{die}} + C_{\text{pkg+test}})/\text{ASP}$ | §3.1 |
| Lifetime energy cost | $P \cdot \text{PUE} \cdot h \cdot p_e$ | §3.4 |
| Field failures | $\lambda N t \times 10^{-9}$ (λ in FIT) | §3.5 |
| US datacenter electricity, 2024 | about 192 TWh, 4.7% of US use | LBNL [R-452] **[Established]** |

### [28-10 · Conversation Scenarios](../courses/28-technical-diligence-and-leadership-fluency/chapters/28-10-conversation-scenarios.md)

The pocket card of §3.5 is the reference for this chapter. Perishable facts used in the scenarios:

| Quantity | Value | Note |
|---|---|---|
| First-silicon success base rate | about 14% (2024 study) | [R-621] **[Industry estimate]** |
| N3 wafer price | about $18,500 | [R-575] **[Industry estimate]** |
| 3A090.a TPP threshold | 4800 (2023 text) | [R-659] |
| Expected maximum of ten standard normals | 1.54 | 28-02 |
| Zero-failure 95% bound | $3.0/T$ | 28-03 |

<!-- END GENERATED -->
