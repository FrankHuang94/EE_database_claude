# Equation Sheet · 15 Control Systems

The relations to know cold from Course 15, each with its conditions and the chapter that derives it.

Conventions:

- unity negative feedback unless stated: loop gain $L = CP$, $T = L/(1 + L)$, $S = 1/(1 + L)$, $S + T = 1$;
- second-order poles $s = -\zeta\omega_n \pm j\omega_n\sqrt{1 - \zeta^2}$, with $\sigma = \zeta\omega_n$ and $\omega_d = \omega_n\sqrt{1 - \zeta^2}$;
- settling times to the 2% band; phase margins in degrees;
- symbol reuse, as in the chapters: $T$ is the complementary sensitivity, but a sample period in the digital rows and a time constant in the lead row; a pure delay is written $\theta$; $K_v$ is the velocity constant, and $K_v$ in the PLL rows is the VCO gain; $K_p$ is the position constant, and in the PID rows the proportional gain; $N$ is the derivative-filter ratio, the PLL divider, the reference gain or the Nyquist encirclement count, as each row says.

## Modeling

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Thermal node: $C_{th}\dot T = P - (T - T_A)/R_{th}$; $\tau = R_{th}C_{th}$; $T_\infty = T_A + PR_{th}$ | One lumped node; heat flow ↔ current, temperature ↔ voltage | [15-01](../../courses/15-control-systems/chapters/15-01-modeling-dynamic-systems.md) |
| Leakage loop gain $G = R\,dP_L/dT$; deviations decay with $\tau/(1 - G)$; runaway when $G \ge 1$ | Linearized about an operating point | [15-01](../../courses/15-control-systems/chapters/15-01-modeling-dynamic-systems.md) |
| DC motor: $K_t$ (N·m/A) $= K_e$ (V·s/rad) in SI; $\Omega/V = K_t/[(Js + b)(L_as + R_a) + K_tK_e]$ | Armature-controlled | [15-01](../../courses/15-control-systems/chapters/15-01-modeling-dynamic-systems.md) |
| Linearization: $\delta\dot x = (\partial f/\partial x)\,\delta x + (\partial f/\partial u)\,\delta u$ | Small deviations about an equilibrium | [15-01](../../courses/15-control-systems/chapters/15-01-modeling-dynamic-systems.md) |

## Transfer functions and loops

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $G(s) = C(sI - A)^{-1}B + D$; poles are eigenvalues of $A$ unless cancelled | Zero initial conditions | [15-02](../../courses/15-control-systems/chapters/15-02-transfer-functions-and-block-diagrams.md) |
| Feedback: $Y/R = G/(1 + GH)$ | Negative feedback through $H$ | [15-02](../../courses/15-control-systems/chapters/15-02-transfer-functions-and-block-diagrams.md) |
| Output disturbance: $Y/D_o = S$; input disturbance: $Y/D_i = PS$; noise: $Y/N = -T$ | Standard loop | [15-02](../../courses/15-control-systems/chapters/15-02-transfer-functions-and-block-diagrams.md) |
| Mason: $T = \sum_k P_k\Delta_k/\Delta$, $\Delta = 1 - \sum L_i + \sum L_iL_j - \cdots$ (non-touching products); $\Delta_k$ is $\Delta$ with only the loops that do not touch path $k$ | Signal-flow graphs | [15-02](../../courses/15-control-systems/chapters/15-02-transfer-functions-and-block-diagrams.md) |

## Time response

| Relation | Conditions / notes | Chapter |
|---|---|---|
| First order: $t_r = 2.20\tau$, $t_s = 3.91\tau$ (2%); $t_r \times f_{-3dB} \approx 0.35$ | Single pole | [15-03](../../courses/15-control-systems/chapters/15-03-time-response.md) |
| Standard form $\omega_n^2/(s^2 + 2\zeta\omega_ns + \omega_n^2)$; poles at angle $\theta$ from the negative real axis with $\zeta = \cos\theta$ | Underdamped pair | [15-03](../../courses/15-control-systems/chapters/15-03-time-response.md) |
| $M_p = e^{-\pi\zeta/\sqrt{1 - \zeta^2}}$; $t_p = \pi/\omega_d$; $t_s \approx 4/\sigma$; $t_r \approx 1.8/\omega_n$ | Two poles, no zero; $t_r$ rule within about 25% for $0.4 \le \zeta \le 0.7$; $4/\sigma$ bounds the envelope only | [15-03](../../courses/15-control-systems/chapters/15-03-time-response.md) |
| $\zeta = -\ln M_p/\sqrt{\pi^2 + \ln^2M_p}$ | Inverse of the overshoot formula | [15-03](../../courses/15-control-systems/chapters/15-03-time-response.md) |
| A zero at $-z$ adds $(1/z)\,dy/dt$: slow zeros raise overshoot; RHP zeros cause undershoot | Same poles | [15-03](../../courses/15-control-systems/chapters/15-03-time-response.md) |

## Steady-state error and sensitivity

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $S_P^T = S = 1/(1 + L)$; $S_H^T \approx -1$ for large $L$ | Relative sensitivities | [15-04](../../courses/15-control-systems/chapters/15-04-feedback-and-steady-state-error.md) |
| $K_p = \lim L$, $K_v = \lim sL$, $K_a = \lim s^2L$ ($s \to 0$) | Stable closed loop | [15-04](../../courses/15-control-systems/chapters/15-04-feedback-and-steady-state-error.md) |
| Errors: step $1/(1 + K_p)$, ramp $1/K_v$, parabola $1/K_a$ | Type 0, 1, 2 respectively give the finite entries | [15-04](../../courses/15-control-systems/chapters/15-04-feedback-and-steady-state-error.md) |
| Input-disturbance offset $= d/C(0)$ | Plant with one integrator, controller without one ($C(0)$ finite); only integrators upstream of the disturbance reject it | [15-04](../../courses/15-control-systems/chapters/15-04-feedback-and-steady-state-error.md) |

## Stability

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Routh: number of RHP roots = sign changes in the first column | Zero-row and zero-first-element special cases in 15-05 | [15-05](../../courses/15-control-systems/chapters/15-05-stability-routh-hurwitz.md) |
| Cubic $a_3s^3 + a_2s^2 + a_1s + a_0$: all $a_i > 0$ and $a_2a_1 > a_3a_0$ | | [15-05](../../courses/15-control-systems/chapters/15-05-stability-routh-hurwitz.md) |
| Boundary oscillation from the auxiliary polynomial (row above the zero row) | | [15-05](../../courses/15-control-systems/chapters/15-05-stability-routh-hurwitz.md) |
| Relative stability: substitute $s = \hat s - \sigma_0$ | Poles left of $-\sigma_0$ | [15-05](../../courses/15-control-systems/chapters/15-05-stability-routh-hurwitz.md) |

## Root locus

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Angle: $\angle L = 180°(2k + 1)$; magnitude: $K = 1/\lvert G(s)\rvert$ | $L = KG$, $K > 0$ | [15-06](../../courses/15-control-systems/chapters/15-06-root-locus.md) |
| Asymptotes: centroid $(\sum p - \sum z)/(n - m)$, angles $180°(2k + 1)/(n - m)$ | $n$ poles, $m$ zeros | [15-06](../../courses/15-control-systems/chapters/15-06-root-locus.md) |
| Breakaway: $dK/ds = 0$, equivalently $ND' - N'D = 0$ | Check the point lies on the locus | [15-06](../../courses/15-control-systems/chapters/15-06-root-locus.md) |
| Departure angle at a pole: $180° + \sum\angle(\text{zeros}) - \sum\angle(\text{other poles})$ | Complex poles | [15-06](../../courses/15-control-systems/chapters/15-06-root-locus.md) |

## Frequency response

| Relation | Conditions / notes | Chapter |
|---|---|---|
| PM $= 180° + \angle L(j\omega_c)$ at $\lvert L\rvert = 1$; GM $= 1/\lvert L(j\omega_{180})\rvert$ | No open-loop right-half-plane poles (poles at $s = 0$ allowed), single crossovers | [15-07](../../courses/15-control-systems/chapters/15-07-frequency-domain-design.md) |
| Nyquist: $Z = N + P$ (clockwise encirclements of −1, open-loop RHP poles) | Contour indented around $j\omega$-axis poles | [15-07](../../courses/15-control-systems/chapters/15-07-frequency-domain-design.md) |
| Delay margin $= \text{PM (rad)}/\omega_c$; a delay $\theta$ adds $-\omega\theta$ of phase | | [15-07](../../courses/15-control-systems/chapters/15-07-frequency-domain-design.md) |
| $\text{PM} \approx 100\zeta$ degrees (to $\zeta \approx 0.7$); exact for $\omega_n^2/[s(s + 2\zeta\omega_n)]$: $\text{PM} = \arctan\bigl(2\zeta/\sqrt{\sqrt{1 + 4\zeta^4} - 2\zeta^2}\bigr)$ | Standard second-order loop | [15-07](../../courses/15-control-systems/chapters/15-07-frequency-domain-design.md) |
| Bode: $\int_0^\infty\ln\lvert S(j\omega)\rvert\,d\omega = \pi\sum\mathrm{Re}\,p_k$ over the open-loop right-half-plane poles $p_k$ (0 if there are none) | Stable closed loop, loop relative degree ≥ 2 | [15-07](../../courses/15-control-systems/chapters/15-07-frequency-domain-design.md) |

## PID, lead and lag

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $C = K_p + K_i/s + K_ds = K_p(1 + 1/(T_is) + T_ds)$; filtered derivative $K_ds/(1 + T_ds/N)$ | Parallel and standard forms | [15-08](../../courses/15-control-systems/chapters/15-08-pid-control.md) |
| Ziegler–Nichols PID: $K_p = 0.6K_u$, $T_i = P_u/2$, $T_d = P_u/8$; Tyreus–Luyben: $K_u/2.2$, $2.2P_u$, $P_u/6.3$ | From the ultimate gain and period | [15-08](../../courses/15-control-systems/chapters/15-08-pid-control.md) |
| SIMC PI: $K_p = \tau/[K(\tau_c + \theta)]$, $T_i = \min[\tau, 4(\tau_c + \theta)]$ | First-order plus delay | [15-08](../../courses/15-control-systems/chapters/15-08-pid-control.md) |
| Anti-windup: clamping, or back-calculation with tracking time $T_t$ | Saturating actuator | [15-08](../../courses/15-control-systems/chapters/15-08-pid-control.md) |
| Lead $(1 + \alpha Ts)/(1 + Ts)$: $\sin\phi_{max} = (\alpha - 1)/(\alpha + 1)$ at $\omega_m = 1/(T\sqrt\alpha)$, gain $\sqrt\alpha$ there | $\alpha > 1$ | [15-09](../../courses/15-control-systems/chapters/15-09-lead-lag-compensation.md) |
| Lag: DC gain boost $\beta$ with its zero about a decade below crossover (costs about 5°) | | [15-09](../../courses/15-control-systems/chapters/15-09-lead-lag-compensation.md) |

## State space

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\mathbf{x}(t) = e^{At}\mathbf{x}(0) + \int_0^te^{A(t - \tau)}B\mathbf{u}(\tau)\,d\tau$ | Linear time-invariant | [15-10](../../courses/15-control-systems/chapters/15-10-state-space-introduction.md) |
| Controllable iff rank$[B\ AB\ \cdots\ A^{n-1}B] = n$; observable iff rank$[C;\ CA;\ \ldots;\ CA^{n-1}] = n$ | | [15-10](../../courses/15-control-systems/chapters/15-10-state-space-introduction.md) |
| Ackermann: $K = [0\ \cdots\ 0\ 1]\,\mathcal{C}^{-1}\alpha_c(A)$; reference gain $N = -1/[C(A - BK)^{-1}B]$ | Single input | [15-10](../../courses/15-control-systems/chapters/15-10-state-space-introduction.md) |
| Observer $\dot{\hat{\mathbf{x}}} = A\hat{\mathbf{x}} + B\mathbf{u} + L(\mathbf{y} - C\hat{\mathbf{x}})$; closed-loop poles = eig$(A - BK)$ ∪ eig$(A - LC)$ | Separation principle | [15-10](../../courses/15-control-systems/chapters/15-10-state-space-introduction.md) |

## Digital control

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $z = e^{sT}$; stable iff all poles inside the unit circle | | [15-11](../../courses/15-control-systems/chapters/15-11-digital-control.md) |
| ZOH equivalent $G(z) = (1 - z^{-1})\mathcal{Z}\{P(s)/s\}$; for $a/(s + a)$: $(1 - e^{-aT})/(z - e^{-aT})$ | Exact at the samples | [15-11](../../courses/15-control-systems/chapters/15-11-digital-control.md) |
| Tustin $s \leftarrow (2/T)(z - 1)/(z + 1)$; prewarped $s \leftarrow [\omega_p/\tan(\omega_pT/2)](z - 1)/(z + 1)$; warping: an analog frequency $\omega_a$ appears at the discrete frequency $\omega$ with $\omega_a = (2/T)\tan(\omega T/2)$ | | [15-11](../../courses/15-control-systems/chapters/15-11-digital-control.md) |
| Tustin PI: $u_k = u_{k-1} + (K_p + K_iT/2)e_k + (-K_p + K_iT/2)e_{k-1}$ | Velocity form | [15-11](../../courses/15-control-systems/chapters/15-11-digital-control.md) |
| Jury, $z^2 + a_1z + a_0$: $\lvert a_0\rvert < 1$ and $1 \pm a_1 + a_0 > 0$ | Second order | [15-11](../../courses/15-control-systems/chapters/15-11-digital-control.md) |
| Hold phase $-\omega T/2$; sample at 10–30× the bandwidth (about 18° to 6°) | Below the Nyquist frequency | [15-11](../../courses/15-control-systems/chapters/15-11-digital-control.md) |

## Applications

| Relation | Conditions / notes | Chapter |
|---|---|---|
| PLL: $L = K(1 + s\tau_z)/[s^2(1 + s\tau_p)]$, $K = I_{cp}K_v/[2\pi N(C + C_2)]$, $\tau_z = RC$, $\tau_p = RCC_2/(C + C_2)$ | Charge pump, $R$–$C$ with $C_2$ across | [15-12](../../courses/15-control-systems/chapters/15-12-control-applications-pll-regulators-thermal.md) |
| Maximum-margin design: $\sqrt b = \tan\text{PM} + \sec\text{PM}$, $\tau_z = \sqrt b/\omega_c$, $\tau_p = 1/(\sqrt b\,\omega_c)$, $K = \omega_c^2/\sqrt b$, $C_2 = (C + C_2)/b$ | Crossover at the phase peak | [15-12](../../courses/15-control-systems/chapters/15-12-control-applications-pll-regulators-thermal.md) |
| Its closed-loop poles: $-\omega_c$ and a pair with $\omega_n = \omega_c$, $\zeta = (\sqrt b - 1)/2$ | | [15-12](../../courses/15-control-systems/chapters/15-12-control-applications-pll-regulators-thermal.md) |
| PFD sampling cost $\approx \pi f_c/f_{ref}$ rad; keep $f_c \lesssim f_{ref}/10$ | | [15-12](../../courses/15-control-systems/chapters/15-12-control-applications-pll-regulators-thermal.md) |
| $\phi_{rms} = \sqrt{2\int10^{\mathcal{L}(f)/10}df}$; jitter $= \phi_{rms}/(2\pi f_{out})$ | Single-sideband $\mathcal{L}$ in dBc/Hz | [15-12](../../courses/15-control-systems/chapters/15-12-control-applications-pll-regulators-thermal.md) |
| Droop with $\omega_0 = g/C$: load line $\Delta I/(\omega_0C)$ (crossover $\omega_0$); critically damped PI ($\omega_z = \omega_0/4$) $(2/e)\Delta I/(\omega_0C)$ at $t = 2/\omega_0$ (crossover $1.029\,\omega_0$) | Transconductance regulator model | [15-12](../../courses/15-control-systems/chapters/15-12-control-applications-pll-regulators-thermal.md) |
| Throttling: $P_{sus} = (T_{lim} - T_A)/R_{total}$; permitted power decays with $C_H(R_{JC} \parallel R_{CA})$ | Two-node model, junction held at the limit | [15-12](../../courses/15-control-systems/chapters/15-12-control-applications-pll-regulators-thermal.md) |
