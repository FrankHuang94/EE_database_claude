# Equation Sheet · 21 RF and Microwave Engineering

The relations to know cold from Course 21, each with its conditions and the chapter that derives it.

Conventions:

- phasors are peak amplitudes; power waves $a$, $b$ are in $\sqrt{\text{W}}$ with $P = \tfrac12\lvert a\rvert^2$; $Z_0$ = 50 Ω unless stated;
- $T_0$ = 290 K, so $kT_0$ = −174 dBm/Hz and $10\log_{10}k$ = −228.6 dBW/K/Hz;
- noise figure NF = $10\log_{10}F$; gains and IIP3s add in **linear** units in the cascade formulas and in dB everywhere else;
- intercept points are input-referred (IIP3, IIP2) unless written OIP3; phase noise $\mathcal L(\Delta f)$ is single-sideband, in dBc/Hz;
- symbols reused between chapters: $Q$ is a quality factor (matching, resonators, antennas), and $Q^{-1}(\cdot)$ the inverse Gaussian tail function; η is a drain or PA efficiency (21-07; written $\eta_{PA}$ in 21-10, where radiation efficiency is $e_r$), or a spectral efficiency (21-11; the cell load there is $X$); $N$ is a number of elements, paths, repetitions or FFT points, or a divide ratio; $n$ is a number of matching sections (21-02), a harmonic index (21-05), a filter order (21-08) or a path-loss exponent (21-11);
- matrices ($S$, $Z$, $I$) are written in plain type, as in 21-01, rather than in the bold of notation.md.

## S-parameters and two-ports

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $a = (\mathbf V + Z_0\mathbf I)/(2\sqrt{Z_0})$, $b = (\mathbf V - Z_0\mathbf I)/(2\sqrt{Z_0})$; $P = \tfrac12(\lvert a\rvert^2 - \lvert b\rvert^2)$ | Power waves, real $Z_0$ | [21-01](../../courses/21-rf-and-microwave-engineering/chapters/21-01-s-parameters.md) |
| $\Gamma = b/a = (Z - Z_0)/(Z + Z_0)$; return loss $-20\log_{10}\lvert\Gamma\rvert$; VSWR $(1 + \lvert\Gamma\rvert)/(1 - \lvert\Gamma\rvert)$ | One port | [21-01](../../courses/21-rf-and-microwave-engineering/chapters/21-01-s-parameters.md) |
| $S_{ij} = b_i/a_j$ with all other ports matched ($a_k = 0$) | Definition | [21-01](../../courses/21-rf-and-microwave-engineering/chapters/21-01-s-parameters.md) |
| Series $Z$: $S_{21} = 2Z_0/(Z + 2Z_0)$, $S_{11} = Z/(Z + 2Z_0)$ | Shunt $Y$: replace $Z/Z_0$ by $Y Z_0$ and change the sign of $S_{11}$ | [21-01](../../courses/21-rf-and-microwave-engineering/chapters/21-01-s-parameters.md) |
| $S = (Z - Z_0I)(Z + Z_0I)^{-1}$, $Z = Z_0(I + S)(I - S)^{-1}$ | Matrix conversions | [21-01](../../courses/21-rf-and-microwave-engineering/chapters/21-01-s-parameters.md) |
| $S_{21} = 2/\Delta_A$, $S_{11} = (A + B/Z_0 - CZ_0 - D)/\Delta_A$, $\Delta_A = A + B/Z_0 + CZ_0 + D$ | ABCD to S; cascade in ABCD or T, never in S | [21-01](../../courses/21-rf-and-microwave-engineering/chapters/21-01-s-parameters.md) |
| Lossless: $S^HS = I$; reciprocal: $S = S^T$ | Unitarity and reciprocity | [21-01](../../courses/21-rf-and-microwave-engineering/chapters/21-01-s-parameters.md) |
| Reference-plane shift: $S'_{ij} = S_{ij}e^{-j(\theta_i + \theta_j)}$ | De-embedding a line of electrical length θ | [21-01](../../courses/21-rf-and-microwave-engineering/chapters/21-01-s-parameters.md) |
| One-port error model $\Gamma_m = e_{00} + e_{10}e_{01}\Gamma/(1 - e_{11}\Gamma)$ | Three standards (SOL) solve it | [21-01](../../courses/21-rf-and-microwave-engineering/chapters/21-01-s-parameters.md) |
| $\Gamma_{in} = S_{11} + S_{12}S_{21}\Gamma_L/(1 - S_{22}\Gamma_L)$ | Unilateral when $S_{12} = 0$ | [21-01](../../courses/21-rf-and-microwave-engineering/chapters/21-01-s-parameters.md) |
| $K = \dfrac{1 - \lvert S_{11}\rvert^2 - \lvert S_{22}\rvert^2 + \lvert\Delta\rvert^2}{2\lvert S_{12}S_{21}\rvert} > 1$ and $\lvert\Delta\rvert < 1$, or $\mu > 1$ | Unconditional stability; $\Delta = S_{11}S_{22} - S_{12}S_{21}$; $\mu = \dfrac{1 - \lvert S_{11}\rvert^2}{\lvert S_{22} - \Delta S_{11}^*\rvert + \lvert S_{12}S_{21}\rvert}$ is the distance from the centre of the $\Gamma_L$ plane to the nearest unstable load | [21-01](../../courses/21-rf-and-microwave-engineering/chapters/21-01-s-parameters.md) |
| $G_{max} = \lvert S_{21}/S_{12}\rvert(K - \sqrt{K^2 - 1})$; MSG $= \lvert S_{21}/S_{12}\rvert$ | Simultaneous conjugate match exists only when unconditionally stable | [21-01](../../courses/21-rf-and-microwave-engineering/chapters/21-01-s-parameters.md) |

## Impedance matching

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $Q = \sqrt{R_{high}/R_{low} - 1}$; $\lvert X\rvert = QR_{low}$, $\lvert B\rvert = Q/R_{high}$ | L-network: low-pass (series L, shunt C) or high-pass (series C, shunt L) form | [21-02](../../courses/21-rf-and-microwave-engineering/chapters/21-02-impedance-matching-networks.md) |
| $\Delta f/f_0 \approx 2\Gamma_m\sqrt{1 + Q^2}/Q^2 \to 2\Gamma_m/Q$ | Bandwidth to reflection $\Gamma_m$ (first order); the limit for $Q \gg 1$ | [21-02](../../courses/21-rf-and-microwave-engineering/chapters/21-02-impedance-matching-networks.md) |
| π network: $R_v = R_{high}/(Q^2 + 1)$, then two L-sections to $R_v$ | Sets $Q$ above the L-network's | [21-02](../../courses/21-rf-and-microwave-engineering/chapters/21-02-impedance-matching-networks.md) |
| $n$ sections: $R_k = R_{low}(R_{high}/R_{low})^{k/n}$, $Q_{sec} = \sqrt{(R_{high}/R_{low})^{1/n} - 1}$ | Lower $Q$, wider band | [21-02](../../courses/21-rf-and-microwave-engineering/chapters/21-02-impedance-matching-networks.md) |
| Quarter-wave: $Z_1 = \sqrt{Z_0Z_L}$; small reflections $\Gamma_n \approx \tfrac12\ln(Z_{n+1}/Z_n)$; binomial: $\ln(Z_{n+1}/Z_n) = 2^{-N}\binom{N}{n}\ln(Z_L/Z_0)$ | Binomial (maximally flat) and Chebyshev (equal ripple) transformers | [21-02](../../courses/21-rf-and-microwave-engineering/chapters/21-02-impedance-matching-networks.md) |
| $\text{IL} = 10\log_{10}(1 + Q_n/Q_u)$ dB | Network $Q_n$ against component $Q_u$ | [21-02](../../courses/21-rf-and-microwave-engineering/chapters/21-02-impedance-matching-networks.md) |
| Bode–Fano: $\displaystyle\int_0^\infty\ln\frac{1}{\lvert\Gamma\rvert}\,d\omega \le \frac{\pi}{RC}$; flat: $\Delta f \le 1/[2RC\ln(1/\Gamma_m)]$ | Parallel RC load; no network beats it | [21-02](../../courses/21-rf-and-microwave-engineering/chapters/21-02-impedance-matching-networks.md) |

## Noise figure and linearity

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $F = (S_i/N_i)/(S_o/N_o) = 1 + T_e/T_0$ | Source at $T_0$ | [21-03](../../courses/21-rf-and-microwave-engineering/chapters/21-03-noise-figure-and-linearity.md) |
| $F_{tot} = F_1 + (F_2 - 1)/G_1 + (F_3 - 1)/(G_1G_2) + \cdots$ | Friis; available gains, linear; a passive loss $L$ has $F = L$ | [21-03](../../courses/21-rf-and-microwave-engineering/chapters/21-03-noise-figure-and-linearity.md) |
| $F = F_{min} + (R_n/G_s)\lvert Y_s - Y_{opt}\rvert^2$ | Noise parameters $F_{min}$, $R_n$, $Y_{opt}$ | [21-03](../../courses/21-rf-and-microwave-engineering/chapters/21-03-noise-figure-and-linearity.md) |
| Y-factor: $F = \text{ENR}/(Y - 1)$, $T_e = (T_h - YT_c)/(Y - 1)$ | Cold source at $T_0$ | [21-03](../../courses/21-rf-and-microwave-engineering/chapters/21-03-noise-figure-and-linearity.md) |
| $A_{1dB} = \sqrt{0.145\lvert a_1/a_3\rvert}$, $A_{IIP3} = \sqrt{\tfrac43\lvert a_1/a_3\rvert}$; IIP3 − P1dB = 9.64 dB | Memoryless cubic | [21-03](../../courses/21-rf-and-microwave-engineering/chapters/21-03-noise-figure-and-linearity.md) |
| $\text{IIP3} = P_{in} + (P_{fund} - P_{IM3})/2$; $\text{IIP2} = P_{in} + (P_{fund} - P_{IM2})$ | From a two-tone test, dBm per tone | [21-03](../../courses/21-rf-and-microwave-engineering/chapters/21-03-noise-figure-and-linearity.md) |
| $1/\text{IIP3}_{tot} = 1/\text{IIP3}_1 + G_1/\text{IIP3}_2 + G_1G_2/\text{IIP3}_3 + \cdots$ | Linear (mW); worst case, coherent addition | [21-03](../../courses/21-rf-and-microwave-engineering/chapters/21-03-noise-figure-and-linearity.md) |
| Blocker desensitization: gain $\times(1 - 2A_B^2/A_{IIP3}^2)$ | Compressive $a_3$ | [21-03](../../courses/21-rf-and-microwave-engineering/chapters/21-03-noise-figure-and-linearity.md) |
| Reciprocal mixing: $N_{rm} = P_B + \mathcal L(\Delta f) + 10\log_{10}B$ dBm | LO phase noise on a blocker | [21-03](../../courses/21-rf-and-microwave-engineering/chapters/21-03-noise-figure-and-linearity.md) |
| $P_{sens} = -174 + 10\log_{10}B + \text{NF} + \text{SNR}_{min}$ dBm | Sensitivity | [21-03](../../courses/21-rf-and-microwave-engineering/chapters/21-03-noise-figure-and-linearity.md) |
| $\text{SFDR} = \tfrac23(\text{IIP3} - N_{floor})$ dB, $N_{floor} = -174 + 10\log_{10}B + \text{NF}$ | IM3 at the noise floor | [21-03](../../courses/21-rf-and-microwave-engineering/chapters/21-03-noise-figure-and-linearity.md) |

## Low-noise amplifiers

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Resistive shunt termination: $F = 1 + R_s/R_T = 2$ (3.01 dB) | Matched, before any gain | [21-04](../../courses/21-rf-and-microwave-engineering/chapters/21-04-low-noise-amplifiers.md) |
| Common gate: $F = 1 + (\gamma/\alpha)/(g_mR_s) = 1 + \gamma/\alpha$ at $g_mR_s = 1$ | Matched input | [21-04](../../courses/21-rf-and-microwave-engineering/chapters/21-04-low-noise-amplifiers.md) |
| $Z_{in} = sL_s + 1/(sC_{gs}) + \omega_TL_s$; match: $\omega_TL_s = R_s$, $\omega_0^2(L_g + L_s)C_{gs} = 1$ | Inductive source degeneration | [21-04](../../courses/21-rf-and-microwave-engineering/chapters/21-04-low-noise-amplifiers.md) |
| $Q_{in} = 1/(2\omega_0R_sC_{gs})$, $G_m = \omega_T/(2\omega_0R_s)$ | Effective transconductance | [21-04](../../courses/21-rf-and-microwave-engineering/chapters/21-04-low-noise-amplifiers.md) |
| $F = 1 + (\gamma/\alpha)g_mR_s(\omega_0/\omega_T)^2$; with gate-inductor loss $r_g$, $F = 1 + r_g/R_s + (\gamma/\alpha)(g_m/R_s)(R_s + r_g)^2(\omega_0/\omega_T)^2$ | Channel noise only (no induced gate noise); re-matched so that $r_g + \omega_TL_s = R_s$ | [21-04](../../courses/21-rf-and-microwave-engineering/chapters/21-04-low-noise-amplifiers.md) |
| Source-referred IIP3 is $20\log_{10}Q_{in}$ dB below the device's own | The input network's voltage gain $Q_{in}$ | [21-04](../../courses/21-rf-and-microwave-engineering/chapters/21-04-low-noise-amplifiers.md) |
| Gain to keep the second stage within Δ dB: $G_1 = (F_2 - 1)/[F_1(10^{\Delta/10} - 1)]$ | From Friis | [21-04](../../courses/21-rf-and-microwave-engineering/chapters/21-04-low-noise-amplifiers.md) |
| Noise cancelling: $g_{m2}R_2 = g_{m1}R_1$, $g_{m1} = 1/R_s$ | Cancels the matching device's noise | [21-04](../../courses/21-rf-and-microwave-engineering/chapters/21-04-low-noise-amplifiers.md) |

## Mixers

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\cos\omega_{RF}t\cos\omega_{LO}t = \tfrac12[\cos(\omega_{RF} - \omega_{LO})t + \cos(\omega_{RF} + \omega_{LO})t]$ | Ideal multiplier | [21-05](../../courses/21-rf-and-microwave-engineering/chapters/21-05-mixers.md) |
| Square-wave LO: $G_c = 2/\pi$ (−3.92 dB); active: $G_c = (2/\pi)g_mR_L$ | Hard switching | [21-05](../../courses/21-rf-and-microwave-engineering/chapters/21-05-mixers.md) |
| SSB noise figure of an ideal switching mixer: $\pi^2/4$ (3.92 dB) | Unfiltered white source noise: the image band (3 dB) and the odd-harmonic bands (0.92 dB) fold to the IF | [21-05](../../courses/21-rf-and-microwave-engineering/chapters/21-05-mixers.md) |
| $\text{IRR} = \dfrac{1 + 2(1 + \varepsilon)\cos\theta + (1 + \varepsilon)^2}{1 - 2(1 + \varepsilon)\cos\theta + (1 + \varepsilon)^2} \approx 4/(\varepsilon^2 + \theta^2)$ | Gain error ε, phase error θ (rad) | [21-05](../../courses/21-rf-and-microwave-engineering/chapters/21-05-mixers.md) |
| Harmonic-reject: square-wave LOs at −45°, 0, +45° weighted 1, $\sqrt2$, 1; $n$th harmonic $\propto \tfrac1n[\sqrt2 + 2\cos(n\cdot45°)]$ | Cancels the 3rd and 5th; 7th and 9th remain | [21-05](../../courses/21-rf-and-microwave-engineering/chapters/21-05-mixers.md) |
| N-path filter: $\text{BW}_{3dB} = 1/(\pi NR_sC)$, gain $[(N/\pi)\sin(\pi/N)]^2$ | High-Q bandpass from switches | [21-05](../../courses/21-rf-and-microwave-engineering/chapters/21-05-mixers.md) |

## Oscillators and VCOs

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $1/Q = 1/Q_L + 1/Q_C$; $R_p = Q\omega_0L$ | Tank loss in parallel form | [21-06](../../courses/21-rf-and-microwave-engineering/chapters/21-06-oscillators-and-vcos.md) |
| Start-up: $G(V) > 1/R_p$; envelope $dV/dt = \tfrac{V}{2C}[G(V) - 1/R_p]$, $\tau_A = 2R_pC = 2Q/\omega_0$ | Describing function | [21-06](../../courses/21-rf-and-microwave-engineering/chapters/21-06-oscillators-and-vcos.md) |
| Hard-switched cross-coupled pair: $V = (2/\pi)I_{tail}R_p$; $\eta = V/(\pi V_{DD})$ | Current-limited regime; $V$ and $R_p$ differential | [21-06](../../courses/21-rf-and-microwave-engineering/chapters/21-06-oscillators-and-vcos.md) |
| Tank thermal noise: $\mathcal L(\Delta f) = kT/(R_pC^2V^2\Delta\omega^2) = \dfrac{2kT}{P_s}\left(\dfrac{\omega_0}{2Q\Delta\omega}\right)^2$ | Leeson's $1/f^2$ region, $F$ = 1 | [21-06](../../courses/21-rf-and-microwave-engineering/chapters/21-06-oscillators-and-vcos.md) |
| ISF: $\mathcal L(\Delta f) = \Gamma_{rms}^2S_i/(2q_{max}^2\Delta\omega^2)$; $1/f^3$ corner $\omega_{1/f}\Gamma_{dc}^2/\Gamma_{rms}^2$ | Hajimiri–Lee | [21-06](../../courses/21-rf-and-microwave-engineering/chapters/21-06-oscillators-and-vcos.md) |
| $\text{FoM} = -\mathcal L + 20\log_{10}(f_0/\Delta f) - 10\log_{10}(P_{DC}/1\ \text{mW})$ | dB, higher is better; published LC VCOs about 184–195 dB (as of Nov 2026) | [21-06](../../courses/21-rf-and-microwave-engineering/chapters/21-06-oscillators-and-vcos.md) |
| $f_{max}/f_{min} = \sqrt{C_{max}/C_{min}}$; $\Delta f/f \approx -\tfrac12\Delta C/C$ | Tuning range | [21-06](../../courses/21-rf-and-microwave-engineering/chapters/21-06-oscillators-and-vcos.md) |
| FM spur $20\log_{10}[K_{VCO}V_m/(2f_m)]$ dBc; $\mathcal L = K_{VCO}^2S_v/(2\Delta f^2)$ | Control-line tone or noise | [21-06](../../courses/21-rf-and-microwave-engineering/chapters/21-06-oscillators-and-vcos.md) |
| Divider by $N$: $\mathcal L_{out} = \mathcal L_{in} - 20\log_{10}N$ | Ideal division | [21-06](../../courses/21-rf-and-microwave-engineering/chapters/21-06-oscillators-and-vcos.md) |
| $\phi_{rms}^2 = 2\int\mathcal L(f)\,df$; EVM ≈ $\phi_{rms}$; for $\mathcal L_0/[1 + (f/f_c)^2]$, $\phi_{rms} = \sqrt{\pi\mathcal L_0f_c}$ | Integrated phase noise, $\mathcal L$ linear per Hz | [21-06](../../courses/21-rf-and-microwave-engineering/chapters/21-06-oscillators-and-vcos.md) |
| Injection locking range $\omega_L \approx (\omega_0/2Q)(I_{inj}/I_{osc})$ | Adler | [21-06](../../courses/21-rf-and-microwave-engineering/chapters/21-06-oscillators-and-vcos.md) |

## Power amplifiers

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $R_{opt} = (V_{DD} - V_k)^2/(2P_{out})$ | Load line, knee $V_k$ | [21-07](../../courses/21-rf-and-microwave-engineering/chapters/21-07-power-amplifiers.md) |
| Class A: $\eta = \tfrac12(1 - V_k/V_{DD})$; B: π/4 = 78.5% | Full swing (class A with knee $V_k$, class B ideal) | [21-07](../../courses/21-rf-and-microwave-engineering/chapters/21-07-power-amplifiers.md) |
| Back-off to amplitude $x$ of maximum: $\eta_A = \tfrac12x^2$, $\eta_B = (\pi/4)x$ | Ideal devices, fixed supply | [21-07](../../courses/21-rf-and-microwave-engineering/chapters/21-07-power-amplifiers.md) |
| $\eta(\alpha) = \dfrac{\alpha - \sin\alpha}{2[2\sin(\alpha/2) - \alpha\cos(\alpha/2)]}$ | Reduced conduction angle α | [21-07](../../courses/21-rf-and-microwave-engineering/chapters/21-07-power-amplifiers.md) |
| Class F (3rd harmonic): $\eta = \tfrac98\cdot\tfrac\pi4$ = 88.36% maximally flat ($V_3 = V_1/9$); maximum $(2/\sqrt3)(\pi/4)$ = 90.69% at $V_3 = V_1/6$ | One harmonic termination | [21-07](../../courses/21-rf-and-microwave-engineering/chapters/21-07-power-amplifiers.md) |
| Class E: $P_{out} = 0.5768V_{DD}^2/R$, $\omega CR = 0.1836$, $X/R = 1.1525$ | Zero-voltage switching, 50% duty | [21-07](../../courses/21-rf-and-microwave-engineering/chapters/21-07-power-amplifiers.md) |
| Average efficiency $\bar\eta = \mathbb E[x^2]/\mathbb E[x^2/\eta(x)]$ | Over the envelope distribution | [21-07](../../courses/21-rf-and-microwave-engineering/chapters/21-07-power-amplifiers.md) |
| ACLR (dBc) $= 2(P_{in} - \text{IIP3}) - 4.77$ | Cubic envelope model, complex-Gaussian signal with a flat spectrum of width B, adjacent channel of equal width; only below saturation (no clipping of the peaks) | [21-07](../../courses/21-rf-and-microwave-engineering/chapters/21-07-power-amplifiers.md) |
| Doherty: $\eta = \tfrac\pi2x$ ($x \le \tfrac12$), $\tfrac\pi2x^2/(3x - 1)$ ($x > \tfrac12$) | Symmetric, ideal class B | [21-07](../../courses/21-rf-and-microwave-engineering/chapters/21-07-power-amplifiers.md) |
| $\eta_{ET} = \eta_{PA}\eta_{mod}$ | Envelope tracking | [21-07](../../courses/21-rf-and-microwave-engineering/chapters/21-07-power-amplifiers.md) |
| DPD: $y = a_1x + (a_1b_3 + a_3)x\lvert x\rvert^2$, so $b_3 = -a_3/a_1$ | Third-order predistortion | [21-07](../../courses/21-rf-and-microwave-engineering/chapters/21-07-power-amplifiers.md) |

## Transceiver architectures

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $f_{im} = f_{LO} + f_{IF} = f_{RF} + 2f_{IF}$ (high-side LO); $f_{im} = f_{LO} - f_{IF} = f_{RF} - 2f_{IF}$ (low-side) | The image sits on the far side of the LO | [21-08](../../courses/21-rf-and-microwave-engineering/chapters/21-08-transceiver-architectures.md) |
| Butterworth rejection $10\log_{10}(1 + x^{2n})$, $x = (f_0/B)(f/f_0 - f_0/f)$ | Bandpass preselector, order $n$ | [21-08](../../courses/21-rf-and-microwave-engineering/chapters/21-08-transceiver-architectures.md) |
| Spurs at $\lvert mf_{LO} - nf_{RF}\rvert = f_{IF}$; half-IF: $f_{RF} = f_{LO} \mp f_{IF}/2$ | $m = n = 2$ | [21-08](../../courses/21-rf-and-microwave-engineering/chapters/21-08-transceiver-architectures.md) |
| $\text{IRR}_{req} \ge (P_{adj} - P_{wanted}) + \text{SNR}_{req}$ | Low-IF image is the adjacent channel | [21-08](../../courses/21-rf-and-microwave-engineering/chapters/21-08-transceiver-architectures.md) |
| Complex filter $H = \omega_p/[\omega_p + j(\omega - \omega_{IF})]$ | Shifted low-pass | [21-08](../../courses/21-rf-and-microwave-engineering/chapters/21-08-transceiver-architectures.md) |
| $\text{SNR}_{jitter} = -20\log_{10}(2\pi f_{in}\sigma_t)$ | Full-scale sine | [21-08](../../courses/21-rf-and-microwave-engineering/chapters/21-08-transceiver-architectures.md) |
| $\text{NF}_{ADC} = \text{NSD (dBFS/Hz)} + P_{FS}\ (\text{dBm}) + 174$ | Direct sampling | [21-08](../../courses/21-rf-and-microwave-engineering/chapters/21-08-transceiver-architectures.md) |

## The RF front end

| Relation | Conditions / notes | Chapter |
|---|---|---|
| BVD: $Z = 1/\{sC_0 + 1/[R_m + sL_m + 1/(sC_m)]\}$; $f_p = f_s\sqrt{1 + C_m/C_0}$ | Acoustic resonator | [21-09](../../courses/21-rf-and-microwave-engineering/chapters/21-09-rf-front-end.md) |
| $k^2_{eff} = x\cot x$, $x = (\pi/2)(f_s/f_p)$; ≈ $(\pi^2/4)(f_p - f_s)/f_p$ | Coupling sets the filter's bandwidth | [21-09](../../courses/21-rf-and-microwave-engineering/chapters/21-09-rf-front-end.md) |
| Edge drift $\Delta f = f\cdot\text{TCF}\cdot\Delta T$ | TCF in ppm/°C | [21-09](../../courses/21-rf-and-microwave-engineering/chapters/21-09-rf-front-end.md) |
| Series switch: on $\text{IL} = 20\log_{10}(1 + R_{on}/2Z_0)$; off $\lvert S_{21}\rvert = x/\sqrt{1 + x^2}$, $x = 2Z_0\omega C_{off}$ | Figure of merit $R_{on}C_{off}$, $f_c = 1/(2\pi R_{on}C_{off})$ | [21-09](../../courses/21-rf-and-microwave-engineering/chapters/21-09-rf-front-end.md) |
| Stacking $N$: $R_{on} \times N$, $C_{off}/N$, voltage $V_{pk}(1 + \lvert\Gamma\rvert)/N$ per device | Power handling | [21-09](../../courses/21-rf-and-microwave-engineering/chapters/21-09-rf-front-end.md) |
| Mismatch loss $L_{mm} = -10\log_{10}(1 - \lvert\Gamma\rvert^2)$ | Antenna tuners recover it | [21-09](../../courses/21-rf-and-microwave-engineering/chapters/21-09-rf-front-end.md) |

## Antennas and arrays

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Patch: $W = \dfrac{c}{2f_0}\sqrt{\dfrac{2}{\varepsilon_r + 1}}$, $L = \dfrac{c}{2f_0\sqrt{\varepsilon_{eff}}} - 2\Delta L$ | Transmission-line model, Hammerstad fringing $\Delta L$ | [21-10](../../courses/21-rf-and-microwave-engineering/chapters/21-10-antennas-arrays-mmwave.md) |
| Chu–McLean: $Q_{min} = 1/(ka)^3 + 1/(ka)$; $B = (s - 1)/(Q\sqrt s)$ (0.707/Q at VSWR 2); $Q_{total} = e_rQ_{rad}$ | Small antennas, $a$ the enclosing radius | [21-10](../../courses/21-rf-and-microwave-engineering/chapters/21-10-antennas-arrays-mmwave.md) |
| Planar array $G(\theta_0) \approx NG_e(\theta_0)$; scan loss $-10\log_{10}\cos\theta_0$ dB | Ideal aperture element | [21-10](../../courses/21-rf-and-microwave-engineering/chapters/21-10-antennas-arrays-mmwave.md) |
| No grating lobes: $d \le \lambda/(1 + \lvert\sin\theta_{max}\rvert)$ | At the highest frequency | [21-10](../../courses/21-rf-and-microwave-engineering/chapters/21-10-antennas-arrays-mmwave.md) |
| Squint: $\sin\theta_{beam} = (f_0/f)\sin\theta_0$; $B_{3dB}/f_0 \approx 0.886/[N(d/\lambda_0)\sin\theta_0]$ | Phase shifters; large-$N$ approximation | [21-10](../../courses/21-rf-and-microwave-engineering/chapters/21-10-antennas-arrays-mmwave.md) |
| Phase quantization: $S = (\sin x/x)^2$, $x = \pi/2^b$; floor $(1 - S)/N$; rms error $180°/(2^b\sqrt3)$ | Decorrelated errors | [21-10](../../courses/21-rf-and-microwave-engineering/chapters/21-10-antennas-arrays-mmwave.md) |
| $\text{EIRP} = N^2P_eG_e$ (+20 log N dB); receive SNR and $G/T$ grow as $N$ | Coherent combining | [21-10](../../courses/21-rf-and-microwave-engineering/chapters/21-10-antennas-arrays-mmwave.md) |
| $N^* = \sqrt{E/(G_e\eta_{PA}P_{oh})}$, $P_{DC}(N^*) = 2\sqrt{EP_{oh}/(G_e\eta_{PA})}$ | DC-optimal element count | [21-10](../../courses/21-rf-and-microwave-engineering/chapters/21-10-antennas-arrays-mmwave.md) |
| $P_{ADC} = \text{FoM}\cdot2^{ENOB}f_s$ per converter, $2N$ converters | Digital beamforming cost (Walden) | [21-10](../../courses/21-rf-and-microwave-engineering/chapters/21-10-antennas-arrays-mmwave.md) |
| Virtual array: $N_{TX}N_{RX}$ elements; resolution ≈ $2/(N_{TX}N_{RX})$ rad | MIMO radar, λ/2 filled line | [21-10](../../courses/21-rf-and-microwave-engineering/chapters/21-10-antennas-arrays-mmwave.md) |

## Link budgets

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $P_r/P_t = G_tG_r(\lambda/4\pi d)^2$; $\text{FSPL} = 20\log_{10}(4\pi d/\lambda)$ dB; $PL(d) = PL(d_0) + 10n\log_{10}(d/d_0)$ | Friis, far field; log-distance beyond $d_0$ | [21-11](../../courses/21-rf-and-microwave-engineering/chapters/21-11-link-budgets.md) |
| $P_r = P_t - L_t + G_t - PL - L_{ex} + G_r - L_r \ge S + M$ | The ledger, dB | [21-11](../../courses/21-rf-and-microwave-engineering/chapters/21-11-link-budgets.md) |
| $\text{MAPL} = \text{EIRP} + G_r - L_r - S - M - L_{ex}$; $d_{max} = d_0\cdot10^{[\text{MAPL} - PL(d_0)]/(10n)}$ | Range from loss | [21-11](../../courses/21-rf-and-microwave-engineering/chapters/21-11-link-budgets.md) |
| Each dB extends range by $10^{1/(10n)}$ | 12% at $n$ = 2, 7% at 3.5 | [21-11](../../courses/21-rf-and-microwave-engineering/chapters/21-11-link-budgets.md) |
| $S = -174 + 10\log_{10}R_b + (E_b/N_0)_{req} + \text{NF} + \text{IM}$ dBm | Sensitivity in rate form | [21-11](../../courses/21-rf-and-microwave-engineering/chapters/21-11-link-budgets.md) |
| Shannon: $E_b/N_0 \ge (2^\eta - 1)/\eta \to \ln2$ (−1.59 dB) | η in b/s/Hz | [21-11](../../courses/21-rf-and-microwave-engineering/chapters/21-11-link-budgets.md) |
| Repetition $N$: gain $10\log_{10}N$ dB, $N$ × airtime | Ideal combining | [21-11](../../courses/21-rf-and-microwave-engineering/chapters/21-11-link-budgets.md) |
| Lognormal margin $M = \sigma Q^{-1}(p_{out})$; Rayleigh margin $-10\log_{10}[-\ln(1 - p_{out})]$ | Separate margins | [21-11](../../courses/21-rf-and-microwave-engineering/chapters/21-11-link-budgets.md) |
| Combined (Suzuki): $P_{out}(M) = \int[1 - \exp(-10^{-(M + x)/10})]\,\phi_\sigma(x)\,dx$ | Less than the sum of the two | [21-11](../../courses/21-rf-and-microwave-engineering/chapters/21-11-link-budgets.md) |
| Jakes: $U = \tfrac12[1 + \text{erf}(a)] + \tfrac12e^{(1 + 2ab)/b^2}[1 - \text{erf}((1 + ab)/b)]$ | $a = M/(\sigma\sqrt2)$, $b = 10n\log_{10}e/(\sigma\sqrt2)$ | [21-11](../../courses/21-rf-and-microwave-engineering/chapters/21-11-link-budgets.md) |
| Noise rise $10\log_{10}[1/(1 - X)]$ | Load $X$, from $I = X(N + I)$ | [21-11](../../courses/21-rf-and-microwave-engineering/chapters/21-11-link-budgets.md) |
| $C/N_0 = \text{EIRP} - L - L_{other} + G/T + 228.6$ dBHz | Satellite and GNSS | [21-11](../../courses/21-rf-and-microwave-engineering/chapters/21-11-link-budgets.md) |
| Slant range $d = \sqrt{(R_E + h)^2 - R_E^2\cos^2\theta_{el}} - R_E\sin\theta_{el}$ | Elevation $\theta_{el}$ | [21-11](../../courses/21-rf-and-microwave-engineering/chapters/21-11-link-budgets.md) |

## Modems and standards

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $R = 10^{-6}\sum_j v_j Q_{m,j}f_jR_{max}\dfrac{12N_{PRB,j}}{T_s^\mu}(1 - OH_j)$ Mb/s | TS 38.306 peak rate; $T_s^\mu = 10^{-3}/(14\cdot2^\mu)$ s; $R_{max}$ = 948/1024, $f$ = 1 unless stated | [21-12](../../courses/21-rf-and-microwave-engineering/chapters/21-12-modem-baseband-and-standards.md) |
| Layer-2 buffer = (DL + UL peak rate) × RLC round trip | 3GPP sizing | [21-12](../../courses/21-rf-and-microwave-engineering/chapters/21-12-modem-baseband-and-standards.md) |
| Soft buffer per HARQ process = information bits / $R_{LBRM}$ ($R_{LBRM}$ = 2/3) × LLR bits | Up to 16 (or 32) processes | [21-12](../../courses/21-rf-and-microwave-engineering/chapters/21-12-modem-baseband-and-standards.md) |
| FFT: $(N/2)\log_2N$ complex multiplications per symbol | Radix 2 | [21-12](../../courses/21-rf-and-microwave-engineering/chapters/21-12-modem-baseband-and-standards.md) |
| Wi-Fi: $R = N_{SD}\log_2M\,R_c/T_{sym}$, $T_{sym}$ = 12.8 µs + GI | Per stream | [21-12](../../courses/21-rf-and-microwave-engineering/chapters/21-12-modem-baseband-and-standards.md) |
| SS-TWR error $\approx (e_A - e_B)T_{reply}/2$; DS-TWR $\hat\tau = (T_{r1}T_{r2} - T_{d1}T_{d2})/(T_{r1} + T_{r2} + T_{d1} + T_{d2})$ | Clock offsets $e_A$, $e_B$ | [21-12](../../courses/21-rf-and-microwave-engineering/chapters/21-12-modem-baseband-and-standards.md) |
| Phase ranging $d = c\Delta\phi/(4\pi\Delta f)$; unambiguous $c/(2\Delta f)$ | Round-trip phase | [21-12](../../courses/21-rf-and-microwave-engineering/chapters/21-12-modem-baseband-and-standards.md) |
| Ionosphere-free: weights $f_1^2/(f_1^2 - f_2^2)$ and $-f_2^2/(f_1^2 - f_2^2)$ | Delay $\propto 1/f^2$ | [21-12](../../courses/21-rf-and-microwave-engineering/chapters/21-12-modem-baseband-and-standards.md) |
| LEO: $v = \sqrt{GM/(R_E + h)}$; peak Doppler $(f/c)vR_E/(R_E + h)$ | Near the horizon | [21-12](../../courses/21-rf-and-microwave-engineering/chapters/21-12-modem-baseband-and-standards.md) |
