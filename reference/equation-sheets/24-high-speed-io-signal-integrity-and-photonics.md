# Equation Sheet · 24 High-Speed I/O, Signal Integrity and Photonics

The relations to know cold from Course 24, each with its conditions and the chapter that derives it.

Conventions:

- bandwidths are decimal (1 GB/s = 10⁹ bytes/s); "both directions" adds the two directions; energy per bit is power divided by bit rate;
- electrical dB is $20\log_{10}$ of a voltage ratio; optical dB is $10\log_{10}$ of an optical power ratio, and a photocurrent is proportional to optical power;
- $Q(x)$ is the Gaussian tail probability, $Q(x) \approx e^{-x^2/2}/(x\sqrt{2\pi})$ for $x \gtrsim 3$; $Q^{-1}(10^{-12})$ = 7.03, $Q^{-1}(2.4 \times 10^{-4})$ = 3.49 (the KP4 FEC threshold);
- $\lambda$ is a wavelength or (in reliability) a failure rate, by context; $\alpha$ is a loss per length (24-01), a channel tap (24-04) or a conductor-loss fraction (24-03); $D$ is fiber dispersion (24-07) or the delay operator (24-04); $Q$ is a BER margin, a resonator quality factor or a charge, by context; $w$ is a trace width (24-01) or a mode radius (24-08).

## Signal integrity (24-01)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $f_N = f_{sym}/2$; $UI = 1/f_{sym}$ | PAM4 halves the symbol rate for a given bit rate | [24-01](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-01-signal-integrity-fundamentals.md) |
| $\alpha \approx R'/(2Z_0) + G'Z_0/2$ Np/m; 1 Np = 8.686 dB | Low-loss line | [24-01](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-01-signal-integrity-fundamentals.md) |
| $\delta = 1/\sqrt{\pi f\mu_0\sigma}$; $\alpha_c \approx 36\sqrt{f_{GHz}}/(w_{mil}Z_0)$ dB/in | Smooth copper; grows as $\sqrt f$ | [24-01](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-01-signal-integrity-fundamentals.md) |
| $K_r = 1 + (2/\pi)\arctan[1.4(\Delta_{rms}/\delta)^2]$ | Hammerstad roughness factor on $\alpha_c$ | [24-01](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-01-signal-integrity-fundamentals.md) |
| $\alpha_d = \pi f\sqrt{\varepsilon_r}\tan\delta/c$ Np/m $= 2.3f_{GHz}\tan\delta\sqrt{\varepsilon_r}$ dB/in | Grows as $f$; dominates at high frequency | [24-01](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-01-signal-integrity-fundamentals.md) |
| $\Gamma = (Z - Z_0)/(Z + Z_0)$; RL $= -20\log_{10}\lvert\Gamma\rvert$ | Impedance discontinuity | [24-01](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-01-signal-integrity-fundamentals.md) |
| $f_{stub} = c/(4\ell_{stub}\sqrt{\varepsilon_r})$ | Quarter-wave via-stub notch | [24-01](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-01-signal-integrity-fundamentals.md) |
| $K_b = \tfrac14(C_m/C + L_m/L)$; $\ell_{sat} = vt_r/2$ | NEXT plateau, saturating with length | [24-01](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-01-signal-integrity-fundamentals.md) |
| $V_{FEXT} = (\ell/2v)(C_m/C - L_m/L)\,dV_a/dt$ | Zero in homogeneous stripline | [24-01](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-01-signal-integrity-fundamentals.md) |
| $V_{bounce} \approx L_{ret}N\Delta I/t_r$; $Z_{target} = \Delta V/\Delta I$ | Simultaneous switching; PDN target | [24-01](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-01-signal-integrity-fundamentals.md) |

## Eyes, jitter and BER (24-02)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $y_n = h_0a_n + \sum_{k\ne0}h_ka_{n-k}$ | Pulse-response cursors | [24-02](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-02-eye-diagrams-jitter-ber.md) |
| $E_{NRZ} = h_0 - \sum\lvert h_k\rvert$; $E_{PAM\text{-}M} = h_0/(M - 1) - \sum\lvert h_k\rvert$ | Peak-distortion eye | [24-02](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-02-eye-diagrams-jitter-ber.md) |
| BER $= Q(V_{eye}/2\sigma)$; PAM4: $\tfrac34Q(V_{eye}/2\sigma)$ | Gaussian noise, Gray coding | [24-02](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-02-eye-diagrams-jitter-ber.md) |
| $TJ = 2Q^{-1}(\text{BER})\,RJ + DJ(\delta\delta)$; $2Q^{-1}(10^{-12})$ = 14.07 | Dual-Dirac model; eye width $UI - TJ$ | [24-02](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-02-eye-diagrams-jitter-ber.md) |
| $H(f) = 1/(1 + jf/f_c)$; $A_{tol} = M\sqrt{1 + (f_c/f)^2}$ | First-order CDR transfer and tolerance | [24-02](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-02-eye-diagrams-jitter-ber.md) |
| COM $= 20\log_{10}(A_s/A_{ni})$ dB | Channel operating margin | [24-02](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-02-eye-diagrams-jitter-ber.md) |

## SerDes architecture (24-03)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $f_{clk} = f_{baud}/N$; phase spacing $360°/N$ = 1 UI | $N$-way interleaving | [24-03](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-03-serdes-architecture.md) |
| $P_{CML} = V_{DD}V_{pp,diff}/50\ \Omega$; $P_{SST} = V_{reg}^2/200\ \Omega$ | Double-terminated 50 Ω per side | [24-03](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-03-serdes-architecture.md) |
| $g_k = \sum_jc_jh_{k-j}$; $\sum\lvert c_j\rvert = 1$ | Transmit FFE under a peak-swing limit | [24-03](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-03-serdes-architecture.md) |
| $H(s) = -g_mR_D(1 + sR_SC_S)/(1 + g_mR_S/2 + sR_SC_S)$; peaking $1 + g_mR_S/2$ | Source-degenerated CTLE | [24-03](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-03-serdes-architecture.md) |
| $z_n = y_n - \sum b_k\hat a_{n-k}$, $b_k = h_k$; $t_{clk\text{-}q} + t_{settle} + t_{setup} < 1$ UI | DFE and its first-tap timing | [24-03](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-03-serdes-architecture.md) |
| $P(e_n\mid e_{n-1}) = \tfrac12Q((h_0 - 2h_1)/\sigma) + \tfrac12Q((h_0 + 2h_1)/\sigma)$ | DFE error propagation | [24-03](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-03-serdes-architecture.md) |
| $\varphi_d - \varphi_c = \Delta f_{baud}/(2\pi f_c)$ UI | First-order CDR under frequency offset $\Delta$ | [24-03](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-03-serdes-architecture.md) |
| PAM4 wins if $L > 9.54\ \text{dB}/[\alpha(\sqrt2 - 1) + 1 - \alpha]$ | $L$ at PAM4 Nyquist, conductor fraction $\alpha$ | [24-03](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-03-serdes-architecture.md) |

## DSP SerDes and FEC (24-04)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| SNR$_{jitter} = -20\log_{10}(2\pi f\sigma_t)$; ENOB $= (\text{SNR} - 1.76)/6.02$ | Sampling-clock jitter | [24-04](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-04-dsp-serdes-and-fec.md) |
| $z_n = \sum_{j=-P}^{F}c_jx_{n-j}$ | Digital FFE | [24-04](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-04-dsp-serdes-and-fec.md) |
| $G_{MLSD} = 10\log_{10}(1 + \alpha^2)$ dB | Channel $1 + \alpha D$, single-error event | [24-04](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-04-dsp-serdes-and-fec.md) |
| NCG $= 20\log_{10}[Q^{-1}(p_{out})/Q^{-1}(p_{in})] + 10\log_{10}R$ dB | BPSK-equivalent convention | [24-04](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-04-dsp-serdes-and-fec.md) |

## Interconnect standards (24-05)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $B = NR\eta/8$ bytes/s | $N$ lanes at $R$ with encoding efficiency $\eta$ | [24-05](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-05-pcie-cxl-ethernet.md) |
| $\eta_{TLP} = P/(P + H)$ | Payload $P$, per-packet overhead $H$ | [24-05](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-05-pcie-cxl-ethernet.md) |
| buffer $\ge B \times t_{RTT}$ | Credits and retry buffers | [24-05](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-05-pcie-cxl-ethernet.md) |
| $R_{lane} = R_{MAC,lane} \times (257/256) \times (544/514)$ | Ethernet transcoding and RS(544,514) | [24-05](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-05-pcie-cxl-ethernet.md) |
| $N_{2\text{-tier}} = k^2/2$ | Non-blocking leaf-spine of radix-$k$ switches | [24-05](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-05-pcie-cxl-ethernet.md) |

## Die-to-die links (24-06)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $E_{bit} = CV^2/4$ | Unterminated short wire, random data | [24-06](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-06-d2d-memory-phys-scale-up.md) |
| $E_{bit} = V^2/(4Rf_b)$ | Terminated link | [24-06](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-06-d2d-memory-phys-scale-up.md) |
| $D_{area} = \phi r/(8p^2)$ | Square bump grid of pitch $p$, data fraction $\phi$, rate $r$ | [24-06](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-06-d2d-memory-phys-scale-up.md) |
| Elmore delay $\approx R_{on}C_{tot} + R_w(C_w/2 + C_L)$; $t_{10\text{–}90} \approx 2.2 \times$ Elmore | RC wire | [24-06](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-06-d2d-memory-phys-scale-up.md) |

## Photonics fundamentals (24-07)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\mathcal R = \eta q\lambda/(hc)$ | Responsivity; 1.06 A/W ideal at 1310 nm | [24-07](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-07-photonics-fundamentals.md) |
| $\tau = n_gL/c$ (4.9 µs/km) | Fiber latency | [24-07](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-07-photonics-fundamentals.md) |
| $\Delta\lambda = \lambda^2\Delta f/c$; $\Delta\tau = DL\Delta\lambda$ | Dispersion spread; grows as rate² in UI | [24-07](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-07-photonics-fundamentals.md) |
| $\beta_2 = -D\lambda^2/(2\pi c)$; broadening $\sqrt{1 + (L/L_D)^2}$, $L_D = T_0^2/\lvert\beta_2\rvert$ | Gaussian pulse | [24-07](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-07-photonics-fundamentals.md) |
| $P_{out} = P_{in}\cos^2(\Delta\phi/2)$, $\Delta\phi = \pi V/V_\pi$; $L = V_\pi L/V_\pi$ | Mach–Zehnder modulator | [24-07](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-07-photonics-fundamentals.md) |
| $\Delta\lambda_{res} = \lambda\Delta n/n_g$; linewidth $\lambda/Q$ | Ring modulator thermal shift | [24-07](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-07-photonics-fundamentals.md) |
| $P_{sens} = Q\sigma/\mathcal R$; PAM4 $+10\log_{10}3$; ER $+10\log_{10}[(ER + 1)/(ER - 1)]$ | Optical dB | [24-07](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-07-photonics-fundamentals.md) |
| $Z_T = R_FA/(1 + A)$; $f_{3dB} = (1 + A)/(2\pi R_FC_{in})$; $i_n = \sqrt{4kT/R_F}$ | Shunt-feedback TIA | [24-07](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-07-photonics-fundamentals.md) |
| $\Delta f = c\Delta\lambda/\lambda^2$ | WDM grid conversion | [24-07](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-07-photonics-fundamentals.md) |

## Silicon photonics (24-08)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\lambda_c = 1239.84\ \text{nm·eV}/E_g$ | Cutoff: Si 1107 nm, Ge (direct) ≈ 1550 nm | [24-08](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-08-silicon-photonics.md) |
| $\theta_c = \arcsin(n_2/n_1)$; single-mode slab $d < \lambda/(2\sqrt{n_1^2 - n_2^2})$ | Fiber: $V = (\pi d/\lambda)\,\text{NA} < 2.405$ | [24-08](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-08-silicon-photonics.md) |
| $\eta = [2w_1w_2/(w_1^2 + w_2^2)]^2\exp[-2d^2/(w_1^2 + w_2^2)]$ | Gaussian mode coupling with offset $d$ | [24-08](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-08-silicon-photonics.md) |
| $\eta_\alpha = \exp[-(\alpha/\theta_{div})^2]$, $\theta_{div} = \lambda/(\pi w)$ | Tilt loss | [24-08](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-08-silicon-photonics.md) |
| $\Lambda = \lambda/(n_{eff} - \sin\theta)$; $d\theta/d\lambda = -1/(\Lambda\cos\theta)$ | Grating coupler | [24-08](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-08-silicon-photonics.md) |
| $\omega_0 = 1/\sqrt{LC}$, $\zeta = (R/2)\sqrt{C/L}$; peak $1/(2\zeta\sqrt{1 - \zeta^2})$; $f_{3dB} = f_0\sqrt{1 - 2\zeta^2 + \sqrt{(1 - 2\zeta^2)^2 + 1}}$ | Driver–bond–modulator RLC | [24-08](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-08-silicon-photonics.md) |
| $P_{laser} = P_{rx,req} + M + \sum L_i$; quadrature costs 3.01 dB | Transmitter budget | [24-08](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-08-silicon-photonics.md) |
| Linear: $1/Q^2 = \sum 1/Q_i^2$; retimed: BER $\approx \sum Q(Q_i)$ | Error accumulation | [24-08](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-08-silicon-photonics.md) |
| $Y = y^n$; cost per good module $(c_P + c_A)/Y$ untested, $c_P/Y + c_A$ tested | Compound yield and wafer test | [24-08](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-08-silicon-photonics.md) |

## Linear-drive and co-packaged optics (24-09)

| Relation | Conditions / notes | Chapter |
|---|---|---|
| pJ/bit $=$ W $/$ (Gb/s) $\times 1000$ | State the port speed | [24-09](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-09-lpo-and-cpo.md) |
| Lanes per laser $\le 10^{(P_{src} - L_{path} - L_{excess} - P_{lane})/10}$ | External laser sharing | [24-09](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-09-lpo-and-cpo.md) |
| $\lambda_U = -\ln(0.05)/T \approx 3/T$; with $r$ failures $\chi^2_{0.95,2r+2}/(2T)$ | 95% upper bound; FIT = failures per 10⁹ h | [24-09](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-09-lpo-and-cpo.md) |
| $U = \lambda \times 8766\ \text{h} \times (\text{ports lost} \times \text{MTTR})/(\text{ports per unit})$ | Port-hours lost per port per year | [24-09](../../courses/24-high-speed-io-signal-integrity-and-photonics/chapters/24-09-lpo-and-cpo.md) |
