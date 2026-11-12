# Notation and Conventions

This is the single source of truth for symbols, units and sign conventions across all 29 courses. Every chapter follows it. If a chapter must deviate (for example, to match a dominant textbook convention in a specialty field), it says so explicitly at the point of use and links here.

## 1. Numbers, units and formatting

| Convention | Rule | Example |
|---|---|---|
| Units | SI throughout. A space between number and unit; engineering prefixes (p, n, µ, m, k, M, G). | 10 kΩ, 4.7 µF, 2.4 GHz |
| Units in math | Upright text: `\text{}` or `\,\mathrm{}` | $\tau = 2.2\ \text{ms}$ |
| Significant figures | Final answers to 3–4 significant figures unless the data justify more. Intermediate values carried at full precision. | $v = 1.43\ \text{V}$ |
| Decimal sign | Point, not comma. Thousands separated by a thin space or comma only in prose. | 1 000 000 or 1,000,000 |
| Logarithms | $\ln$ = natural log; $\log_{10}$ written explicitly; $\log_2$ for information. Never a bare "log". | $\ln 2 = 0.693$ |
| Decibels | Power ratio: $10\log_{10}(P_2/P_1)$. Amplitude ratio (same impedance): $20\log_{10}(V_2/V_1)$. dBm = dB relative to 1 mW; dBV = relative to 1 V rms. | 3 dB ≈ 2× power |
| Angles | Radians in all formulas. Degrees only for reporting phase, always with the ° symbol. | $\phi = 30^\circ = \pi/6$ |
| Numerical tolerance | Published answers are correctly rounded; see `tools/eeverify.py`. | |

## 2. Complex numbers and phasors

| Symbol | Meaning |
|---|---|
| $j$ | Imaginary unit, $j^2 = -1$ (EE convention; $i$ is reserved for current) |
| $z = x + jy$ | Rectangular form; $x = \operatorname{Re}\{z\}$, $y = \operatorname{Im}\{z\}$ |
| $z = r e^{j\theta} = r\angle\theta$ | Exponential and polar forms; $r = \lvert z\rvert \ge 0$, $\theta = \angle z = \arg z$ |
| $z^*$ | Complex conjugate, $x - jy$ |
| $\mathbf{V}, \mathbf{I}$ | **Phasors** (bold upright capitals). Peak-amplitude convention, cosine reference: $v(t) = V_m\cos(\omega t + \phi) \;\leftrightarrow\; \mathbf{V} = V_m\angle\phi$ |
| $\mathbf{V}_{\text{rms}}$ | RMS phasor, $\mathbf{V}/\sqrt{2}$, used only in AC-power work and always subscripted |
| $Z, Y$ | Impedance and admittance (complex numbers, **not** phasors, so not bold): $Z = R + jX$, $Y = G + jB$ |
| $\omega$, $f$ | Angular frequency (rad/s) and frequency (Hz), $\omega = 2\pi f$; period $T = 1/f$ |

## 3. Circuit variables and sign conventions

The total-, DC-, small-signal- and phasor-quantity convention (Sedra & Smith style):

| Quantity | Symbol style | Example |
|---|---|---|
| Total instantaneous | lowercase symbol, UPPERCASE subscript | $v_{GS}(t) = V_{GS} + v_{gs}(t)$ |
| DC (bias) | UPPERCASE symbol, UPPERCASE subscript | $V_{GS}$, $I_D$ |
| Small-signal (incremental) | lowercase symbol, lowercase subscript | $v_{gs}$, $i_d$ |
| Phasor of a small signal | bold UPPERCASE symbol, lowercase subscript | $\mathbf{V}_{gs}$ |
| Generic time-domain circuit variable | lowercase | $v(t)$, $i(t)$, $v_C(t)$, $i_L(t)$ |

- **Passive sign convention:** current is referenced *into* the terminal marked +. Then $p = vi$ is the power **absorbed** by the element (negative means it delivers power).
- **Node voltages** are referenced to ground: $v_A$ is the voltage of node A relative to ground; $v_{AB} = v_A - v_B$.
- **Switching instants:** $t_0^-$ is just before the switch event and $t_0^+$ just after; $v_C$ and $i_L$ are continuous across $t_0$.
- **Time constant** $\tau$ (s). **Undamped natural frequency** $\omega_0$ (rad/s). **Damping ratio** $\zeta$. **Neper frequency** $\alpha$ (1/s). **Quality factor** $Q$.
- **Op-amps:** open-loop gain $A$ (or $A_0$ at DC), unity-gain frequency $\omega_t$ / $f_t$; feedback factor $\beta$; loop gain $L = A\beta$ (in Course 12, $T$ is also used where the textbook does).

## 4. Signals and transforms

| Domain | Notation |
|---|---|
| Continuous-time signal | $x(t)$; unit step $u(t)$; unit impulse $\delta(t)$ |
| Discrete-time signal | $x[n]$; unit step $u[n]$; unit sample $\delta[n]$ |
| Laplace transform | $X(s)$, $s = \sigma + j\omega$; transfer function $H(s)$ |
| Continuous-time Fourier transform | $X(j\omega)$ (Signals & Systems, Control); $X(f)$ in Hz (Communications, DSP spectra). Each chapter states which. |
| Discrete-time Fourier transform | $X(e^{j\omega})$, $\omega$ in rad/sample |
| DFT | $X[k]$, $k = 0,\dots,N-1$ |
| z-transform | $X(z)$ |
| Convolution | $x * h$ |
| Frequency response | $H(j\omega)$, magnitude $\lvert H\rvert$ (or in dB), phase $\angle H$ |

## 5. Linear algebra

| Object | Notation |
|---|---|
| Scalar | italic: $a$, $\lambda$ |
| Column vector | bold lowercase: $\mathbf{x}$ |
| Matrix | bold uppercase: $\mathbf{A}$ |
| Transpose, conjugate transpose | $\mathbf{A}^\mathsf{T}$, $\mathbf{A}^\mathsf{H}$ |
| Identity, inverse, determinant | $\mathbf{I}$, $\mathbf{A}^{-1}$, $\det\mathbf{A}$ |

Bold uppercase is shared by matrices and phasors. Context always disambiguates (e.g., the AC nodal equation $\mathbf{Y}\mathbf{V} = \mathbf{I}$ has an admittance *matrix* $\mathbf{Y}$ multiplying a *vector of node-voltage phasors* $\mathbf{V}$), and chapters say so when both appear.

## 6. Fields and electromagnetics

| Quantity | Notation |
|---|---|
| Vector field (time domain) | arrow: $\vec{E}(\vec{r}, t)$, $\vec{H}$, $\vec{D}$, $\vec{B}$, $\vec{J}$ |
| Phasor vector field | tilde + arrow: $\tilde{\vec{E}}(\vec{r})$ |
| Unit vectors | hat: $\hat{x}, \hat{r}, \hat{\phi}$ |
| Permittivity, permeability | $\varepsilon = \varepsilon_r\varepsilon_0$, $\mu = \mu_r\mu_0$ |
| Characteristic / intrinsic impedance | $Z_0$ (line), $\eta$ (medium) |
| Reflection coefficient | $\Gamma$ |
| Propagation constant | $\gamma = \alpha + j\beta$ |

## 7. Devices and semiconductors

| Symbol | Meaning (units) |
|---|---|
| $q$ | Elementary charge, $1.602\times10^{-19}$ C |
| $k$ | Boltzmann constant, $1.381\times10^{-23}$ J/K ($8.617\times10^{-5}$ eV/K) |
| $V_T = kT/q$ | **Thermal voltage** (≈ 25.85 mV at 300 K) |
| $V_{TH}$ | **MOSFET threshold voltage** (written $V_{TH}$ to avoid any clash with $V_T$) |
| $n, p$; $n_i$ | Electron and hole concentrations; intrinsic concentration (cm⁻³) |
| $N_A, N_D$ | Acceptor and donor doping (cm⁻³) |
| $E_C, E_V, E_F, E_g$ | Conduction/valence band edges, Fermi level, bandgap (eV) |
| $\mu_n, \mu_p$ | Electron and hole mobility (cm²/V·s). The same Greek letter as permeability; context disambiguates. |
| $C_{ox}$ | Gate-oxide capacitance per unit area (F/m² or fF/µm²) |
| $g_m, r_o, r_\pi, \beta$ | Transconductance, output resistance, BJT base resistance, BJT current gain |
| $\lambda$ | Channel-length modulation (1/V); also wavelength in EM and optics, with context making it clear |

Semiconductor work conventionally uses cm and eV. Chapters convert to SI explicitly when combining with circuit quantities.

## 8. Probability and noise

| Symbol | Meaning |
|---|---|
| $P(A)$, $p_X(x)$, $f_X(x)$, $F_X(x)$ | Probability, PMF, PDF, CDF |
| $\mathbb{E}[X]$, $\operatorname{Var}(X)$, $\sigma_X$ | Expectation, variance, standard deviation |
| $Q(x)$ | Gaussian tail probability, $Q(x) = P(Z > x)$ for $Z \sim \mathcal{N}(0,1)$ |
| $R_X(\tau)$, $S_X(f)$ | Autocorrelation and power spectral density |
| $N_0/2$ | Two-sided white-noise PSD (W/Hz) |
| $\overline{v_n^2}$ | Mean-square noise voltage (V²), with spectral density $\overline{v_n^2}/\Delta f$ (V²/Hz) |

## 9. Digital and architecture

- Verilog/SystemVerilog code uses `snake_case` for signals and `UPPER_CASE` for parameters; active-low signals end in `_n` (e.g., `rst_n`).
- Number bases: `0x` prefix for hexadecimal, `0b` for binary in prose and C; Verilog literals as `8'hFF`.
- Bit numbering: bit 0 is the least-significant bit.
- Performance: CPI, IPC, $f_{clk}$; energy in J (pJ/op, pJ/bit), power in W.

## 10. Problem and answer labeling

- Problems are numbered `NN-MM.k` (course-chapter.problem) and tagged by tier: **[A]** concept/recall, **[B]** standard exam level, **[C]** challenge/design.
- Worked examples are numbered *Example NN-MM.k* and keyed as `Ex NN-MM.k` in answer keys.
- Every published number appears in an `<!-- answer-key -->` table and is checked by a script in the course's `verify/` folder.
