# Equation Sheet · 09 Semiconductor Devices

The relations to know cold from Course 09, each with its conditions and the chapter that derives it.

Conventions and course values (silicon, 300 K unless stated):

- $V_T = kT/q$ = 25.852 mV; $q$ = 1.602 × 10⁻¹⁹ C; $\varepsilon_s$ = 11.7ε₀ = 1.036 × 10⁻¹² F/cm; $\varepsilon_{ox}$ = 3.9ε₀ = 3.453 × 10⁻¹³ F/cm;
- $E_g$ = 1.12 eV, $n_i$ = 1.0 × 10¹⁰ cm⁻³, $N_C$ = 3.2 × 10¹⁹ and $N_V$ = 1.8 × 10¹⁹ cm⁻³; $\chi_{\text{Si}}$ = 4.05 eV;
- mobility (cm²/V·s): $\mu_n = 92 + 1268/[1 + (N/1.3\times10^{17})^{0.91}]$, $\mu_p = 48 + 402/[1 + (N/6.3\times10^{16})^{0.76}]$, $N$ the total doping;
- $hc$ = 1.2398 eV·µm; $c$ = 2.998 × 10⁸ m/s;
- the passive sign convention for currents; $\phi_B = V_T\ln(N_A/n_i)$ for a p-type body.

## Crystals, bands and carriers

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Si: diamond lattice, $a$ = 5.431 Å, 8 atoms per cubic cell (5.0 × 10²² cm⁻³) | Six conduction valleys along ⟨100⟩, $m_l$ = 0.98, $m_t$ = 0.19 $m_0$ | [09-01](../../courses/09-semiconductor-devices/chapters/09-01-crystals-and-energy-bands.md) |
| Conductivity mass $1/m_c = \tfrac13(1/m_l + 2/m_t)$; DOS mass $m_{dn} = 6^{2/3}(m_lm_t^2)^{1/3}$ | Electrons; holes combine heavy and light bands | [09-01](../../courses/09-semiconductor-devices/chapters/09-01-crystals-and-energy-bands.md) |
| Photon cutoff $\lambda_c = 1.24/E_g$ (µm, eV) | Direct gaps absorb and emit efficiently; indirect need phonons | [09-01](../../courses/09-semiconductor-devices/chapters/09-01-crystals-and-energy-bands.md), [09-14](../../courses/09-semiconductor-devices/chapters/09-14-optoelectronic-devices.md) |
| $n = N_Ce^{-(E_C - E_F)/kT}$, $p = N_Ve^{-(E_F - E_V)/kT}$, $np = n_i^2 = N_CN_Ve^{-E_g/kT}$ | Nondegenerate (Boltzmann) | [09-02](../../courses/09-semiconductor-devices/chapters/09-02-carriers-doping-fermi-level.md) |
| $n = n_ie^{(E_F - E_i)/kT}$; n-type $n_0 \approx N_D - N_A$, $p_0 = n_i^2/n_0$ | Full ionization, $N_D - N_A \gg n_i$ | [09-02](../../courses/09-semiconductor-devices/chapters/09-02-carriers-doping-fermi-level.md) |
| Dopant count in volume $V$: Poisson, mean $NV$, σ = $\sqrt{NV}$ | Random placement; drives random dopant fluctuation | [09-02](../../courses/09-semiconductor-devices/chapters/09-02-carriers-doping-fermi-level.md), [09-10](../../courses/09-semiconductor-devices/chapters/09-10-short-channel-effects-and-leakage.md) |

## Transport, recombination and continuity

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $J = q(n\mu_n + p\mu_p)\mathcal E + q(D_n\nabla n - D_p\nabla p)$; $\rho = 1/q(n\mu_n + p\mu_p)$; $R_{sh} = \rho/t$ | Drift plus diffusion | [09-03](../../courses/09-semiconductor-devices/chapters/09-03-drift-and-diffusion.md) |
| Einstein relation $D = \mu V_T$ | Nondegenerate, equilibrium-like | [09-03](../../courses/09-semiconductor-devices/chapters/09-03-drift-and-diffusion.md) |
| $v = \mu\mathcal E/(1 + \mathcal E/\mathcal E_{sat})$; $v_{sat}$ ≈ 10⁷ cm/s (bulk), 8 × 10⁶ cm/s (electrons, inversion layer) | High-field limit | [09-03](../../courses/09-semiconductor-devices/chapters/09-03-drift-and-diffusion.md), [09-10](../../courses/09-semiconductor-devices/chapters/09-10-short-channel-effects-and-leakage.md) |
| SRH: $\tau = 1/(\sigma v_{th}N_t)$; radiative $\tau = 1/Bn_0$; Auger $\tau = 1/C_nn_0^2$; rates add, $1/\tau = \sum 1/\tau_i$ | Low-level injection, minority carriers | [09-04](../../courses/09-semiconductor-devices/chapters/09-04-generation-recombination-continuity.md) |
| Continuity: $\partial p'/\partial t = D_p\nabla^2p' - p'/\tau_p + G$; $L_p = \sqrt{D_p\tau_p}$ | Uniform generation: $p' = G\tau_p$ | [09-04](../../courses/09-semiconductor-devices/chapters/09-04-generation-recombination-continuity.md) |
| Quasi-Fermi levels: $np = n_i^2e^{(E_{Fn} - E_{Fp})/kT}$ | Out of equilibrium | [09-04](../../courses/09-semiconductor-devices/chapters/09-04-generation-recombination-continuity.md) |

## PN junctions and diodes

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $V_{bi} = V_T\ln(N_AN_D/n_i^2)$ | Step junction | [09-05](../../courses/09-semiconductor-devices/chapters/09-05-pn-junction-electrostatics.md) |
| $W = \sqrt{\dfrac{2\varepsilon_s(V_{bi} - V)}{q}\Big(\dfrac1{N_A} + \dfrac1{N_D}\Big)}$; $N_Ax_p = N_Dx_n$; $\mathcal E_{\max} = 2(V_{bi} - V)/W$; $C_j = \varepsilon_s/W$ per area | Depletion approximation | [09-05](../../courses/09-semiconductor-devices/chapters/09-05-pn-junction-electrostatics.md) |
| Law of the junction $p_n(0) = p_{n0}e^{V/V_T}$ | Low-level injection | [09-06](../../courses/09-semiconductor-devices/chapters/09-06-pn-junction-iv-and-capacitance.md) |
| $I = I_0(e^{V/V_T} - 1)$, $I_0 = qAn_i^2\Big(\dfrac{D_p}{N_DL_p} + \dfrac{D_n}{N_AL_n}\Big)$; short side: $L \to W$ | Ideal diode | [09-06](../../courses/09-semiconductor-devices/chapters/09-06-pn-junction-iv-and-capacitance.md) |
| $g_d = I/V_T$; $C_d = (\tau_p/2)g_d$ (long), $(2/3)\tau_tg_d$ (short) | Small signal | [09-06](../../courses/09-semiconductor-devices/chapters/09-06-pn-junction-iv-and-capacitance.md) |
| Avalanche when $\int_0^W\alpha_ne^{-\int_0^x(\alpha_n - \alpha_p)dx'}dx = 1$; Hu's rule $V_B \approx 15\text{ V}(10^{17}/N)^{0.6}$ | One-sided junction; tunneling dominates below a few volts | [09-06](../../courses/09-semiconductor-devices/chapters/09-06-pn-junction-iv-and-capacitance.md) |
| Schottky: $J = A^*T^2e^{-\phi_B/V_T}(e^{V/V_T} - 1)$ | Thermionic emission | [09-06](../../courses/09-semiconductor-devices/chapters/09-06-pn-junction-iv-and-capacitance.md) |

## Bipolar transistors

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $I_C = I_Se^{V_{BE}/V_T}$, $I_S = qA_En_i^2D_n/G_B$, Gummel number $G_B = \int N_B\,dx$ | Short base, low-level injection | [09-07](../../courses/09-semiconductor-devices/chapters/09-07-bipolar-junction-transistor.md) |
| $\beta = (D_nN_EW_E)/(D_pN_BW_B)$ (emitter-injection limit); HBT: $\times e^{\Delta E_g/kT}$ | Band-gap narrowing lowers it in heavily doped emitters | [09-07](../../courses/09-semiconductor-devices/chapters/09-07-bipolar-junction-transistor.md), [09-13](../../courses/09-semiconductor-devices/chapters/09-13-compound-and-wide-bandgap-semiconductors.md) |
| $\tau_B = W_B^2/2D_n$; $f_T = 1/2\pi\tau_F$; $g_m = I_C/V_T$; $r_o = V_A/I_C$ | $\tau_F$ includes base, emitter and collector delays | [09-07](../../courses/09-semiconductor-devices/chapters/09-07-bipolar-junction-transistor.md) |

## MOS capacitor and MOSFET

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $C_{ox} = \varepsilon_{ox}/T_{ox}$; $V_{FB} = \psi_g - \psi_s - Q_{ox}/C_{ox}$; n⁺ poly on p-Si: $V_{FB} = -(E_C - E_F)/q$ | $\psi$ are work functions | [09-08](../../courses/09-semiconductor-devices/chapters/09-08-mos-capacitor.md) |
| $V_{TH} = V_{FB} + 2\phi_B + \sqrt{2qN_A\varepsilon_s(2\phi_B)}/C_{ox}$; $W_{d\max} = \sqrt{2\varepsilon_s(2\phi_B)/qN_A}$ | p-type body, n-channel | [09-08](../../courses/09-semiconductor-devices/chapters/09-08-mos-capacitor.md) |
| $C_{\min} = (1/C_{ox} + W_{d\max}/\varepsilon_s)^{-1}$; EOT $= T_{hk}\times 3.9/k$ | High-frequency C–V | [09-08](../../courses/09-semiconductor-devices/chapters/09-08-mos-capacitor.md) |
| Body effect $V_{TH} = V_{TH0} + \gamma(\sqrt{2\phi_B + V_{SB}} - \sqrt{2\phi_B})$, $\gamma = \sqrt{2qN_A\varepsilon_s}/C_{ox}$ | | [09-09](../../courses/09-semiconductor-devices/chapters/09-09-long-channel-mosfet.md) |
| $I_D = \dfrac WL\mu C_{ox}\Big(V_{ov} - \dfrac m2V_{DS}\Big)V_{DS}$; $V_{Dsat} = V_{ov}/m$; $I_{Dsat} = \dfrac{W}{2mL}\mu C_{ox}V_{ov}^2$; $m = 1 + 3T_{ox}/W_{d\max}$ | Long channel | [09-09](../../courses/09-semiconductor-devices/chapters/09-09-long-channel-mosfet.md) |
| $g_m = 2I_D/V_{ov}$ (strong), $1/mV_T$ (weak); $f_T = g_m/2\pi C_{gs}$, $C_{gs} = \tfrac23WLC_{ox}$ | Saturation | [09-09](../../courses/09-semiconductor-devices/chapters/09-09-long-channel-mosfet.md) |
| $S = mV_T\ln 10 \ge$ 59.5 mV/decade; $I_{off} = I_t10^{-V_{TH}/S}$, $I_t$ = 100 nA × W/L (Hu) | Subthreshold | [09-09](../../courses/09-semiconductor-devices/chapters/09-09-long-channel-mosfet.md) |
| $1/V_{Dsat} = m/V_{ov} + 1/\mathcal E_{sat}L$, $\mathcal E_{sat} = 2v_{sat}/\mu$; $I_{Dsat} = WC_{ox}v_{sat}(V_{ov} - mV_{Dsat})$ | Velocity saturation | [09-10](../../courses/09-semiconductor-devices/chapters/09-10-short-channel-effects-and-leakage.md) |
| Injection limit $I_{Dsat} = WBv_{thx}C_{ox}V_{ov}$; series $R_S$: $I_{Dsat0}/(1 + R_SI_{Dsat0}/V_{ov})$ | Very short channels | [09-10](../../courses/09-semiconductor-devices/chapters/09-10-short-channel-effects-and-leakage.md) |
| Roll-off/DIBL: $\Delta V_{TH} = (V_{DS} + 0.4)e^{-L/l_d}$, $l_d \propto (T_{oxe}W_{dep}X_j)^{1/3}$ | Hu's semi-quantitative model | [09-10](../../courses/09-semiconductor-devices/chapters/09-10-short-channel-effects-and-leakage.md) |
| Random dopants: $\sigma_{V_{TH}} = (q/C_{ox})\sqrt{N_AW_{dep}/3WL}$ | Depth-weighted, uniform doping | [09-10](../../courses/09-semiconductor-devices/chapters/09-10-short-channel-effects-and-leakage.md) |

## CMOS, scaling and advanced devices

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $V_M = (V_{TN}\sqrt r + V_{DD} - \lvert V_{TP}\rvert)/(1 + \sqrt r)$, $r = k_n/k_p$ | Square-law inverter | [09-11](../../courses/09-semiconductor-devices/chapters/09-11-cmos-and-scaling.md) |
| $\tau_d = (CV_{DD}/4)(1/I_{onN} + 1/I_{onP})$; ring period $2N\tau_d$ | | [09-11](../../courses/09-semiconductor-devices/chapters/09-11-cmos-and-scaling.md) |
| $P_{dyn} = \alpha CV_{DD}^2f$; $P_{static} = V_{DD}I_{off}$ | | [09-11](../../courses/09-semiconductor-devices/chapters/09-11-cmos-and-scaling.md) |
| Constant-field scaling by κ: delay 1/κ, power per circuit 1/κ², density κ², power density 1; constant voltage: power density κ² (at $f \propto \kappa$) | | [09-11](../../courses/09-semiconductor-devices/chapters/09-11-cmos-and-scaling.md) |
| Double-gate scale length $\lambda^2 = (\varepsilon_s/2\varepsilon_{ox})t_{si}t_{ox} + t_{si}^2/8$; single gate $(\varepsilon_s/\varepsilon_{ox})t_{si}t_{ox} + t_{si}^2/2$ | Parabolic potential | [09-12](../../courses/09-semiconductor-devices/chapters/09-12-finfet-gaa-cfet-backside-power.md) |
| Barrier lowering $u_{\min} \approx 2\sqrt{ab}\,e^{-L/2\lambda}$, $a$ ≈ 0.2 V, $b = a + V_{DS}$ | $L \gg \lambda$ | [09-12](../../courses/09-semiconductor-devices/chapters/09-12-finfet-gaa-cfet-backside-power.md) |
| Fin $W_{\text{eff}} = 2H + W_{fin}$; nanosheets $N \times 2(W + t)$; rail IR drop $IR/2$ (one end), $IR/8$ (both ends) | | [09-12](../../courses/09-semiconductor-devices/chapters/09-12-finfet-gaa-cfet-backside-power.md) |

## Wide-bandgap and optoelectronic devices

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Triangular drift layer: $N_D = \varepsilon\mathcal E_c^2/2qV_B$, $W = 2V_B/\mathcal E_c$, $R_{on,sp} = 4V_B^2/\varepsilon\mu\mathcal E_c^3$ | Baliga's unipolar limit | [09-13](../../courses/09-semiconductor-devices/chapters/09-13-compound-and-wide-bandgap-semiconductors.md) |
| Polarization sheet charge $\sigma = P_{\text{GaN}} - P_{\text{AlGaN}}$, $P_{pz} = 2\epsilon(e_{31} - e_{33}c_{13}/c_{33})$ | Coherently strained AlGaN on Ga-face GaN | [09-13](../../courses/09-semiconductor-devices/chapters/09-13-compound-and-wide-bandgap-semiconductors.md) |
| $R_{sh} = 1/qn_s\mu$ | 2DEG or any sheet | [09-13](../../courses/09-semiconductor-devices/chapters/09-13-compound-and-wide-bandgap-semiconductors.md) |
| $\mathcal R = \eta\lambda(\text{µm})/1.24$ A/W; shot noise $\overline{i_n^2} = 2qIB$ | Photodiodes | [09-14](../../courses/09-semiconductor-devices/chapters/09-14-optoelectronic-devices.md) |
| $d = ct/2$, $\Delta d = c\Delta t/2$; $P_{det} = 1 - e^{-\text{PDE}\,\bar n}$ | Time of flight | [09-14](../../courses/09-semiconductor-devices/chapters/09-14-optoelectronic-devices.md) |
| Pixel: conversion gain $q/C_{FD}$; SNR$_{\max} = \sqrt{N_{FW}}$; DR $= 20\log_{10}(N_{FW}/\sigma_r)$ | Shot-noise-limited | [09-14](../../courses/09-semiconductor-devices/chapters/09-14-optoelectronic-devices.md) |
| Escape cone $(1 - \cos\theta_c)/2$, $\theta_c = \arcsin(1/n)$; Fresnel $R = [(n-1)/(n+1)]^2$ | One face, normal incidence | [09-14](../../courses/09-semiconductor-devices/chapters/09-14-optoelectronic-devices.md) |
| Laser threshold $g_{th} = \alpha_i + (1/2L)\ln(1/R_1R_2)$; inversion needs $E_{Fn} - E_{Fp} > E_g$ | | [09-14](../../courses/09-semiconductor-devices/chapters/09-14-optoelectronic-devices.md) |
| Solar cell: $I = I_0(e^{V/V_T} - 1) - I_{sc}$; $V_{oc} = V_T\ln(I_{sc}/I_0 + 1)$; MPP: $V = V_{oc} - V_T\ln(1 + V/V_T)$; $FF = V_{mp}I_{mp}/V_{oc}I_{sc}$ | Ideal diode, no series resistance | [09-14](../../courses/09-semiconductor-devices/chapters/09-14-optoelectronic-devices.md) |
