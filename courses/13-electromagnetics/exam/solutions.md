# Course 13 · Final Exam Solutions (Electromagnetics)

Exam: [README.md](README.md). Every number below is recomputed by [verify_13_exam.py](../verify/verify_13_exam.py), which mostly uses different routes from these formulas (where a value is a definition, such as an EIRP sum or a fractional bandwidth, it evaluates the definition). It uses symbolic differentiation and numerical quadrature for the vector calculus, finite-difference Laplace solutions and surface-charge integration for the electrostatics, field-energy integrals for the inductor, and the exact complex propagation constant for the lossy media. It also uses thin-film matrices and root finding for the optics, a discrete-time wave simulation for the line transient, ABCD matrices and a sampled standing-wave pattern for the lines, finite-difference eigenvalues for the guide, and direct summation of array fields.

---

## Solutions

### Solution 1

(a) $\nabla\cdot\vec{A} = \partial(xy)/\partial x + \partial(yz)/\partial y + \partial(zx)/\partial z = y + z + x$ = **6** at (1, 2, 3). The curl is

$$
\nabla\times\vec{A} = \Big(\frac{\partial A_z}{\partial y} - \frac{\partial A_y}{\partial z}\Big)\hat{x} + \Big(\frac{\partial A_x}{\partial z} - \frac{\partial A_z}{\partial x}\Big)\hat{y} + \Big(\frac{\partial A_y}{\partial x} - \frac{\partial A_x}{\partial y}\Big)\hat{z} = -y\,\hat{x} - z\,\hat{y} - x\,\hat{z},
$$

which is (**−2**, **−3**, **−1**) at (1, 2, 3).

(b) $\nabla V = (2xyz,\ x^2z,\ x^2y)$ = (**12**, **3**, **2**) at (1, 2, 3), with magnitude $\sqrt{144 + 9 + 4} = \sqrt{157}$ = **12.53**.

(c) In spherical coordinates $\nabla\cdot\vec{D} = (1/r^2)\,\partial(r^2D_r)/\partial r = (1/r^2)\,\partial(2r^4)/\partial r = 8r$, so $\rho_v$ = **8** nC/m³ at $r$ = 1 m. By the divergence theorem the charge inside $r$ = 2 m is the flux out of that sphere: $D_r \times 4\pi r^2 = 2(4) \times 4\pi(4) = 128\pi$ = **402.1** nC. (Integrating $\rho_v$ directly, $\int_0^2 8r \cdot 4\pi r^2\,dr = 8\pi r^4\big|_0^2 = 128\pi$, agrees.)

(d) $(\nabla\times\vec{F})_z = \partial(x)/\partial x - \partial(-y)/\partial y = 2$, uniform, so by Stokes's theorem the circulation is $2 \times \pi(2)^2 = 8\pi$ = **25.13** m². (Directly: on the circle $\vec{F}\cdot d\vec\ell = 2 \times 2\,d\phi$, so $\oint = 4 \times 2\pi$, the same.)

### Solution 2

(a) The layers are in series because $D$ is continuous across the interface: $C = \varepsilon_0A/(d_1/\varepsilon_{r1} + d_2/\varepsilon_{r2}) = 8.854 \times 10^{-15}/(0.5 \times 10^{-3} + 0.1667 \times 10^{-3})$ = **13.28** pF. Then $Q = CV$ and $D = Q/A$ = **1.328** µC/m², and $E = D/\varepsilon$ gives **75** kV/m in the $\varepsilon_r$ = 2 layer and **25** kV/m in the $\varepsilon_r$ = 6 layer (check: 75 V + 25 V = 100 V). The low-permittivity layer carries three times the field, which is why an air void in insulation is where breakdown starts.

(b) $C' = 2\pi\varepsilon/\ln(b/a) = 2\pi(2.25)(8.854 \times 10^{-12})/\ln(3.333)$ = **104.0** pF/m. The field is $E(\rho) = V/[\rho\ln(b/a)]$, largest at the inner conductor: $1000/(0.45 \times 10^{-3} \times 1.204)$ = **1.846** MV/m, comfortably below polyethylene's breakdown strength (tens of MV/m).

(c) The plane is replaced by an image charge of −1 nC at 1 cm below it, 2 cm from the real charge. The force is attractive (toward the plane): $F = q^2/[4\pi\varepsilon_0(2d)^2] = (10^{-9})^2 \times 8.988 \times 10^9/(0.02)^2$ = **22.47** µN.

### Solution 3

(a) The reluctances are $\mathcal{R}_c = \ell_c/(\mu_r\mu_0A) = 0.1/(1200 \times 4\pi \times 10^{-7} \times 10^{-5}) = 6.63 \times 10^6$ A/Wb and $\mathcal{R}_g = g/(\mu_0A) = 10^{-3}/(4\pi \times 10^{-7} \times 10^{-5}) = 7.96 \times 10^7$ A/Wb, so the gap holds $\mathcal{R}_g/(\mathcal{R}_c + \mathcal{R}_g) = 12/13$ = **92.31**% of the total (the gap is 1 mm of air against the core's 100 mm/1200 = 0.083 mm of "equivalent air"). $L = N^2/(\mathcal{R}_c + \mathcal{R}_g) = 62\,500/(8.62 \times 10^7)$ = **725.0** µH, and $B = NI/[(\mathcal{R}_c + \mathcal{R}_g)A]$ = **0.5800** T at 2 A, well below the saturation of the laminated silicon steel (about 1.5 T). A ferrite core of the same permeability would saturate near 0.4 to 0.5 T, so this design would need fewer ampere-turns per gap or a larger cross-section with ferrite.

(b) $W = \tfrac12LI^2$ = **1.450** mJ. The same flux passes the core and the gap, so the energy $\tfrac12\Phi^2\mathcal{R}$ divides as the reluctance does: **92.31**% of it sits in the 1 mm gap. A gap lets a small, lightly-magnetized core store a lot of energy without saturating, and it makes $L$ depend on a mechanical dimension rather than on the core's temperature-sensitive permeability.

(c) By Biot–Savart every element of the loop is at distance $a$ and perpendicular to the radius, so $B = \mu_0I/(2a) = 4\pi \times 10^{-7}/(0.02)$ = **62.83** µT, about the size of the Earth's field.

### Solution 4

(a) The phase velocity is $\omega/\beta = 2\pi \times 10^9/30 = 2.094 \times 10^8$ m/s, so $n = c/v_p$ = 1.431 and $\varepsilon_r = n^2$ = **2.049**. $\eta = \eta_0/n$ = **263.2** Ω. $\vec{H}$ is in phase with $\vec{E}$ with amplitude $100/263.2$ = **0.380** A/m, along $+\hat{y}$ so that $\vec{E}\times\vec{H}$ points along $+\hat{z}$. The time-average power density is $E_0^2/(2\eta)$ = **19.00** W/m² along $+\hat{z}$, and $\lambda = 2\pi/\beta$ = **20.94** cm.

(b) The ratio of conduction to displacement current is $\sigma/(\omega\varepsilon) = 2 \times 10^{-3}/(2\pi f \times 4 \times 8.854 \times 10^{-12})$: **8.988** at 1 MHz and **0.008988** at 1 GHz. At 1 MHz conduction dominates but not overwhelmingly: the soil is a lossy, "quasi-conducting" medium and the exact formulas for γ are needed. At 1 GHz it is a low-loss dielectric (loss tangent 0.009). In that regime α levels off and the wave propagates with little dispersion, so echoes keep their shape and timing, and shorter wavelengths give finer resolution: that is why ground-penetrating radar works at hundreds of MHz. At 1 MHz the field diffuses rather than propagates, so there are no sharp echoes to time, even though the soil attenuates less there.

(c) $\tau = \varepsilon/\sigma = 4 \times 8.854 \times 10^{-12}/(2 \times 10^{-3})$ = **17.71** ns. A free charge placed inside the soil decays with this time constant; the ratio in (b) equals $1/(\omega\tau)$, so the soil behaves as a conductor for periods much longer than τ and as a dielectric for periods much shorter.

### Solution 5

(a) $\delta = 1/\sqrt{\pi f\mu_0\sigma} = 1/\sqrt{\pi(3 \times 10^8)(4\pi \times 10^{-7})(3.5 \times 10^7)}$ = **4.912** µm and $R_s = 1/(\sigma\delta)$ = **5.817** mΩ. With the current in a skin of depth δ around the circumference $\pi d$, $R_{ac} = R_s\ell/(\pi d) = 5.817 \times 10^{-3}/(\pi \times 10^{-3})$ = **1.852** Ω, while $R_{dc} = \ell/(\sigma\pi d^2/4)$ = **36.38** mΩ. The ratio is $a/(2\delta)$ = **50.90**: at 300 MHz only the outer 5 µm of the 1 mm wire carries current. (The exact Bessel-function solution for a round wire is **0.5**% higher: the skin sits on a curved surface, and the correction is about $\delta/(2a)$, small because $a/\delta \approx 100$.)

(b) \$\sigma/(\omega\varepsilon) = 4/(2\pi \times 4 \times 10^4 \times 81 \times 8.854 \times 10^{-12}) = \$ **2.219 × 10⁴** ≫ 1, a good conductor. $\delta = 1/\sqrt{\pi f\mu_0\sigma}$ = **1.258** m, the attenuation is $8.686/\delta$ = **6.903** dB/m, the wavelength in the water is $2\pi\delta$ = **7.906** m (against 7.5 km in air), and an 80 dB loss takes $80/6.903$ = **11.59** m. Submarine communication therefore uses very low frequencies (and still only reaches shallow depths).

### Solution 6

(a) $\eta_2 = \eta_0/3$, so $\Gamma = (\eta_2 - \eta_1)/(\eta_2 + \eta_1) = (1 - 3)/(1 + 3)$ = **−0.5** and $\tau = 1 + \Gamma = 2\eta_2/(\eta_1 + \eta_2)$ = **0.5**. Reflected power $\lvert\Gamma\rvert^2$ = **25**%; transmitted $\lvert\tau\rvert^2\eta_1/\eta_2$ = 0.25 × 3 = **75**%, which together make 100%. (τ is only 0.5, yet three-quarters of the power is transmitted, because the lower-impedance medium carries more power per unit field squared.)

(b) The quarter-wave coating cancels the two reflections when its index is the geometric mean, $\sqrt{1 \times 1.8}$ = **1.342**, and its thickness is $\lambda_0/(4n_1) = 550/(4 \times 1.342)$ = **102.5** nm. A quarter-wave layer of MgF₂ (99.6 nm thick at 550 nm) transforms the glass's normalized impedance $1/n_s$ to $n_1^2/n_s$ (13-06 §3.2), so $\Gamma = (n_s - n_1^2)/(n_s + n_1^2) = (1.8 - 1.904)/(1.8 + 1.904)$, a reflectance of **0.0794**%, against $[(1.8 - 1)/(1.8 + 1)]^2$ = **8.163**% for bare glass. Because $1.38^2$ = 1.904 is close to 1.8, MgF₂ is nearly ideal on high-index glass (on ordinary glass of index 1.5 it leaves about 1.4%), one reason high-index lens elements are coated with it.

(c) Brewster: $\tan\theta_B = n_2/n_1 = 1.45$, so $\theta_B$ = **55.41**° (parallel polarization only). Critical angle from silica into air: $\sin\theta_c = 1/1.45$, $\theta_c$ = **43.60**°; beyond it the silica totally reflects, which is how a fibre or a prism guides light.

### Solution 7

(a) The source sees the line as $Z_0$ at first, so $v^+ = 2 \times 50/(25 + 50)$ = **1.333** V. $\Gamma_S = (25 - 50)/(25 + 50)$ = **−0.3333** and $\Gamma_L = (200 - 50)/(200 + 50)$ = **0.6**. Each round trip multiplies the wave by $\Gamma_L\Gamma_S$ = −0.2, and each arrival adds $(1 + \Gamma_L)$ times the incident wave to the load voltage:

- $t = T$: $1.333 \times 1.6$ = **2.133** V;
- $t = 3T$: $2.133 + 1.333(-0.2)(1.6)$ = **1.707** V;
- $t = 5T$: $1.707 + 1.333(0.04)(1.6)$ = **1.792** V;

converging (with ringing, because $\Gamma_L\Gamma_S < 0$) to the DC divider $2 \times 200/225$ = **1.778** V. The geometric series of arrivals, $1.333 \times 1.6/(1 + 0.2)$, gives the same answer.

(b) At the load the line looks like a Thévenin source of $2v^+$ behind $Z_0$, so the capacitor charges with $\tau = Z_0C$ = **100** ps, and $v_L = 2v^+(1 - e^{-t/\tau})$. Its 10–90% rise time is $\tau\ln 9$ = **219.7** ps: even an ideal edge arrives at the receiver slowed by about 220 ps. Transmitter equalization can partly pre-compensate, and a shunt termination at the receiver halves τ to $Z_0C/2$, but the receiver's capacitance always costs bandwidth.

### Solution 8

(a) $Z_0 = \sqrt{L'/C'} = \sqrt{2500}$ = **50** Ω, $v = 1/\sqrt{L'C'}$ = **1.667 × 10⁸** m/s, and $\varepsilon_{eff} = (c/v)^2$ = **3.236**, typical of a microstrip on a laminate of $\varepsilon_r$ ≈ 4.

(b) β = $2\pi \times 10^9/(1.667 \times 10^8)$ = 37.70 rad/m, so βℓ = 0.3770 rad. An open line has $Z_{in} = -jZ_0\cot\beta\ell$ = **−j126.3** Ω, a capacitor of $1/(\omega\lvert X\rvert)$ = **1.260** pF. The lumped estimate is $C'\ell$ = **1.2** pF; the exact value is **5.02**% larger because the stub is already 6% of a wavelength long, and $\cot x \approx 1/x$ only for small $x$.

(c) $Z_1 = \sqrt{50 \times 100}$ = **70.71** Ω, and the length is $v/(4f) = 1.667 \times 10^8/(4 \times 2.5 \times 10^9)$ = **1.667** cm. The match is exact only at 2.5 GHz, where the section is a quarter-wavelength.

### Solution 9

(a) A quarter-wave line inverts the load about $Z_0$: $Z_{in} = Z_0^2/Z_L = 2500/(20 - j10) = 2500(20 + j10)/500$ = **100 + j50** Ω. The capacitive load becomes inductive.

(b) $\Gamma_L = (Z_L - Z_0)/(Z_L + Z_0) = (-30 - j10)/(70 - j10)$, of magnitude $\sqrt{1000}/\sqrt{5000}$ = **0.4472** (the same anywhere on a lossless line, including at the 100 + j50 Ω input). VSWR $= (1 + 0.4472)/(1 - 0.4472)$ = **2.618**; return loss $-20\log_{10}0.4472$ = **6.990** dB; mismatch loss $-10\log_{10}(1 - 0.2)$ = **0.9691** dB.

(c) The angle of $\Gamma_L$ is −153.43°. Moving a distance $d$ toward the source multiplies Γ by $e^{-j2\beta d}$, a clockwise rotation of 720° per wavelength. The voltage is a minimum where Γ's angle reaches −180°: $d_{min} = (180 - 153.43)/720$ = **0.0369**λ. It is a maximum where the angle reaches −360°, a quarter-wavelength further: $d_{max}$ = **0.2869**λ. The first extremum is a minimum because Γ starts with a negative angle (the load is capacitive), and it comes early because −153° is already close to −180°.

(d) In admittance terms, move until the conductance is $1/Z_0$, then cancel the susceptance with the stub. With $R_L$ = 20 Ω and $X_L$ = −10 Ω, the quadratic of 13-09 §3.4 gives $t = \tan\beta d = [X_L \pm \sqrt{R_L((Z_0 - R_L)^2 + X_L^2)/Z_0}]/(R_L - Z_0) = (-10 \pm 20)/(-30)$, so $t$ = −1/3 or 1. For $t$ = 1, $d$ = **0.125**λ, where the normalized admittance is $1 - j1$; a shorted stub ($y = -j\cot\beta\ell$) must add $+j1$, so $\cot\beta\ell = -1$ and ℓ = **0.375**λ. For $t$ = −1/3, $d = (\arctan(-1/3) + \pi)/2\pi$ = **0.4488**λ, where $y = 1 + j1$; the stub must add $-j1$, so $\cot\beta\ell = 1$ and ℓ = **0.125**λ. On the chart, both are the two crossings of the |Γ| = 0.4472 circle with the $g$ = 1 circle. The first solution needs the shorter line to the stub; the second the shorter stub.

### Solution 10

(a) $Q = \sqrt{R_{high}/R_{low} - 1} = \sqrt{50/12.5 - 1}$ = **1.732**. The series reactance is $QR_{low}$ = 21.65 Ω, an inductor of $21.65/(2\pi \times 9 \times 10^8)$ = **3.829** nH; the shunt susceptance is $Q/R_{high}$ = 34.64 mS, a capacitor of $0.03464/\omega$ = **6.126** pF. (Check: 12.5 + j21.65 Ω has admittance 20 − j34.64 mS, and the capacitor cancels the imaginary part, leaving 1/50 S.)

(b) At 800 MHz the series branch is $12.5 + j\omega L$ = 12.5 + j19.25 Ω, admittance **23.74 − j36.54** mS; the capacitor adds j**30.79** mS, leaving **23.74 − j5.752** mS, so $Z$ = **39.79 + j9.64** Ω. Then $\lvert\Gamma\rvert = \lvert Z - 50\rvert/\lvert Z + 50\rvert$ = **0.1555** and the mismatch loss is $-10\log_{10}(1 - \lvert\Gamma\rvert^2)$ = **0.1063** dB. A 4:1 step with Q = 1.7 stays usefully matched over ±100 MHz; a larger ratio would need a higher Q and would narrow the band.

### Solution 11

(a) $f_{c,mn} = (c/2)\sqrt{(m/a)^2 + (n/b)^2}$: TE₁₀ at $c/(2a)$ = **7.869** GHz; TE₂₀ at $c/a$ = **15.74** GHz; TE₀₁ at $c/(2b)$ = **15.74** GHz (because $b = a/2$ exactly). Only TE₁₀ propagates from **7.869** to **15.74** GHz (the guide's recommended range, about 10 to 15 GHz, stays inside that band with margin at both ends).

(b) $f_c/f$ = 0.6053, so $\sqrt{1 - (f_c/f)^2}$ = 0.7960. With $k = 2\pi f/c$ = 272.5 rad/m: $\beta$ = **216.9** rad/m, $\lambda_g = 2\pi/\beta$ = **2.897** cm (longer than the free-space 2.306 cm), $Z_{TE} = \eta_0/0.7960$ = **473** Ω, $v_g$ = **0.7960** $c$, and the delay through 1 m is $1/v_g$ = **4.190** ns.

(c) $f_{101} = (c/2)\sqrt{(1/a)^2 + (1/d)^2} = 1.499 \times 10^8\sqrt{(1/0.01905)^2 + (1/0.02)^2}$ = **10.87** GHz: the TE₁₀ mode bouncing between the end walls with one half-wavelength along the 2 cm length.

### Solution 12

(a) EIRP = 20 + 9 = **29** dBm. λ = 5.169 cm, so FSPL = $20\log_{10}(4\pi \times 2000/0.05169)$ = **113.7** dB, and $P_r$ = 29 + 9 − 113.74 = **−75.74** dBm.

(b) $A_e = G\lambda^2/(4\pi) = 7.943 \times 0.05169^2/(4\pi)$ = **16.89** cm².

(c) The margin is −75.74 − (−90) = **14.26** dB. Free-space loss grows by 20 dB per decade of distance, so the range stretches by $10^{14.26/20}$ to **10.33** km. A real link must also budget for fading, rain (small at 5.8 GHz) and obstacles near the path, so a working design keeps 10 dB or more of margin and does not use it as range.

### Solution 13

(a) In a source-free, lossless, linear, homogeneous and isotropic medium (so that μ and ε are constants that can be taken outside the derivatives), $\nabla\times\vec{E} = -\mu\,\partial\vec{H}/\partial t$, $\nabla\times\vec{H} = \varepsilon\,\partial\vec{E}/\partial t$, and $\nabla\cdot\vec{E} = 0$. Take the curl of the first and substitute the second:

$$
\nabla\times\nabla\times\vec{E} = -\mu\frac{\partial}{\partial t}(\nabla\times\vec{H}) = -\mu\varepsilon\frac{\partial^2\vec{E}}{\partial t^2} .
$$

With the identity $\nabla\times\nabla\times\vec{E} = \nabla(\nabla\cdot\vec{E}) - \nabla^2\vec{E}$ and $\nabla\cdot\vec{E} = 0$, this is the wave equation $\nabla^2\vec{E} = \mu\varepsilon\,\partial^2\vec{E}/\partial t^2$. A uniform plane wave $E_x = f(z - vt)$ satisfies it when $f''v^2 = f''/(\mu\varepsilon)$, that is $v = 1/\sqrt{\mu\varepsilon}$, for any shape $f$. Faraday's law has only a $y$-component for this field: $\partial H_y/\partial t = -(1/\mu)\,\partial E_x/\partial z = -(1/\mu)f'$. Since $\partial f/\partial t = -vf'$, this integrates (dropping a static constant) to $H_y = f/(\mu v) = \sqrt{\varepsilon/\mu}\,E_x$, so $E_x/H_y = \sqrt{\mu/\varepsilon} = \eta$. ∎

(b) On the line, with $z$ measured toward the load and the load at $z = 0$, $V(z) = V^+(e^{-j\beta z} + \Gamma_Le^{j\beta z})$ and $I(z) = (V^+/Z_0)(e^{-j\beta z} - \Gamma_Le^{j\beta z})$, where $\Gamma_L = (Z_L - Z_0)/(Z_L + Z_0)$ makes $V(0)/I(0) = Z_L$. At $z = -\ell$,

$$
Z_{in} = Z_0\frac{e^{j\beta\ell} + \Gamma_Le^{-j\beta\ell}}{e^{j\beta\ell} - \Gamma_Le^{-j\beta\ell}} .
$$

Substituting $\Gamma_L$ and multiplying through by $Z_L + Z_0$, the numerator is $(Z_L + Z_0)e^{j\beta\ell} + (Z_L - Z_0)e^{-j\beta\ell} = 2(Z_L\cos\beta\ell + jZ_0\sin\beta\ell)$ and the denominator $2(Z_0\cos\beta\ell + jZ_L\sin\beta\ell)$, so $Z_{in} = Z_0(Z_L\cos\beta\ell + jZ_0\sin\beta\ell)/(Z_0\cos\beta\ell + jZ_L\sin\beta\ell)$. Dividing both by $\cos\beta\ell$ (where it is not zero):

$$
Z_{in} = Z_0\frac{Z_L + jZ_0\tan\beta\ell}{Z_0 + jZ_L\tan\beta\ell} .
$$

At ℓ = λ/4, βℓ = π/2, so in the undivided form $\cos\beta\ell$ = 0 and $\sin\beta\ell$ = 1: $Z_{in} = Z_0(jZ_0)/(jZ_L) = Z_0^2/Z_L$. ∎

(c) The far field is a local plane wave, so the power density is $S = \lvert E_\theta\rvert^2/(2\eta_0) = \eta_0k^2I^2\ell^2\sin^2\theta/(32\pi^2r^2)$. Integrating over a sphere, with $dA = r^2\sin\theta\,d\theta\,d\phi$ and $\int_0^\pi\sin^3\theta\,d\theta = 4/3$:

$$
P_{rad} = \frac{\eta_0k^2I^2\ell^2}{32\pi^2}\cdot2\pi\cdot\frac43 = \frac{\eta_0k^2I^2\ell^2}{12\pi} = \frac{\pi\eta_0}{3}I^2\Big(\frac{\ell}{\lambda}\Big)^2 .
$$

Setting $P_{rad} = \tfrac12I^2R_{rad}$ gives $R_{rad} = (2\pi\eta_0/3)(\ell/\lambda)^2$ ≈ 789(ℓ/λ)² Ω. For ℓ = λ/25 it is 789/625 = **1.262** Ω. With 1 Ω of loss in series, the radiation efficiency is $1.262/(1.262 + 1)$ = **55.80**%: a short antenna's resistance falls as the square of its length, so its losses soon dominate. ∎

### Solution 14

(a) The 16 coherent elements give an EIRP of $P_{el} + 20\log_{10}N + G_{el}$ = 10 + 24.08 + 5 = **39.08** dBm at broadside: $10\log_{10}16$ of array gain and the same again from 16 times the transmitted power (13-11). At 60° each element's gain is down by $10\log_{10}\cos60^\circ$ = 3.01 dB, so the EIRP is **36.07** dBm. "39 dBm across ±60°" holds only at broadside: at the scan edge the module is 3 dB short, the same as halving its transmitted power. The 16 PAs deliver 160 mW, which at 15% efficiency draws **1.067** W of DC, before the beamformer, LO distribution and control; about 0.9 W of it becomes heat in a few square centimetres.

(b) Grating lobes stay out of visible space while $d < \lambda/(1 + \sin\theta_{max})$, so for 5 mm and 60° the frequency must stay below $c/[d(1 + \sin60^\circ)] = 2.998 \times 10^8/(0.005 \times 1.866)$ = **32.13** GHz. At 40 GHz (λ = 7.495 mm) the spacing must be under **0.5359**λ = **4.02** mm. The band 24–40 GHz is a **50**% fractional bandwidth (16 GHz about a 32 GHz centre), several times what a single patch element usually covers well. As stated, the claim fails above 32 GHz: scanned to 60° at 40 GHz, a grating lobe enters visible space and radiates power in an unintended direction.

(c) Rubric (4 points for any three of these or equivalent questions, about 4/3 points each: half for a sharp question, half for a clear contrast between a strong and an evasive answer):

- **"Is 39 dBm EIRP measured at the scan edge and at the band edges, and at what linearity (EVM or ACLR) and compression?"** A strong answer gives a measured EIRP-against-angle-and-frequency plot at the standard's modulation and EVM limit. An evasive answer gives "peak" or "saturated" EIRP at broadside.
- **"How do you avoid grating lobes at 40 GHz with 5 mm spacing?"** At 40 GHz, 5 mm spacing is grating-lobe-free only for scans up to $\arcsin(\lambda/d - 1)$ = **29.93**°, so a strong answer concedes a reduced scan range at the top of the band, or a smaller spacing, or band-specific sub-arrays, and shows measured patterns. An evasive answer says "proprietary element" or quotes a simulation only.
- **"What element gain do you get at 24 GHz?"** A 5 mm × 5 mm cell has an aperture of 25 mm², so even a perfectly efficient element is limited to $4\pi A/\lambda^2$ = **3.04** dBi at 24 GHz (**4.38** dBi at 28 GHz): the 5 dBi assumption cannot hold at the bottom of the band. A strong answer gives measured element gain and active return loss across 24–40 GHz; an evasive one quotes a single-frequency value.
- **"What are the DC power and junction temperature at full EIRP, and how is the module cooled?"** A strong answer gives watts, thermal resistance and derating. An evasive answer quotes only RF output power or "typical" consumption at low duty cycle.
- **"How does the EIRP compare with the regulatory limit and the standard's power class for the target device, and what is the link margin at the intended range?"** A strong answer gives a link budget with path loss, body or hand blockage and margins. An evasive answer gives free-space range in a lab.
- **"What does calibration cost per module, and how do patterns hold over temperature and part-to-part spread?"** A strong answer gives calibration time, tables and production yield. An evasive answer says it is "self-calibrating" without data.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| X13.1a | divergence at (1, 2, 3) | 6 | — |
| X13.1b | curl x-component | −2 | — |
| X13.1c | curl y-component | −3 | — |
| X13.1d | curl z-component | −1 | — |
| X13.1e | gradient x-component | 12 | — |
| X13.1f | gradient y-component | 3 | — |
| X13.1g | gradient z-component | 2 | — |
| X13.1h | gradient magnitude | 12.53 | — |
| X13.1i | charge density at 1 m | 8 | nC/m³ |
| X13.1j | charge inside 2 m | 402.1 | nC |
| X13.1k | circulation | 25.13 | m² |
| X13.2a | two-layer capacitance | 13.28 | pF |
| X13.2b | flux density | 1.328 | µC/m² |
| X13.2c | field in εr = 2 layer | 75 | kV/m |
| X13.2d | field in εr = 6 layer | 25 | kV/m |
| X13.2e | coax capacitance | 104.0 | pF/m |
| X13.2f | largest coax field | 1.846 | MV/m |
| X13.2g | force on charge near plane | 22.47 | µN |
| X13.3a | gap fraction of reluctance | 92.31 | % |
| X13.3b | inductance | 725.0 | µH |
| X13.3c | flux density at 2 A | 0.5800 | T |
| X13.3d | stored energy | 1.450 | mJ |
| X13.3e | energy fraction in gap | 92.31 | % |
| X13.3f | loop centre field | 62.83 | µT |
| X13.4a | relative permittivity | 2.049 | — |
| X13.4b | intrinsic impedance | 263.2 | Ω |
| X13.4c | H amplitude | 0.380 | A/m |
| X13.4d | power density | 19.00 | W/m² |
| X13.4e | wavelength | 20.94 | cm |
| X13.4f | conduction/displacement at 1 MHz | 8.988 | — |
| X13.4g | conduction/displacement at 1 GHz | 0.008988 | — |
| X13.4h | relaxation time | 17.71 | ns |
| X13.5a | aluminium skin depth | 4.912 | µm |
| X13.5b | aluminium surface resistance | 5.817 | mΩ |
| X13.5c | wire resistance at 300 MHz | 1.852 | Ω |
| X13.5d | wire resistance at DC | 36.38 | mΩ |
| X13.5e | AC/DC ratio | 50.90 | — |
| X13.5f | seawater σ/ωε | 2.219 × 10⁴ | — |
| X13.5g | seawater skin depth | 1.258 | m |
| X13.5h | seawater attenuation | 6.903 | dB/m |
| X13.5i | wavelength in seawater | 7.906 | m |
| X13.5j | depth for 80 dB | 11.59 | m |
| X13.5k | exact round-wire excess | 0.5 | % |
| X13.6a | reflection coefficient | −0.5 | — |
| X13.6b | transmission coefficient | 0.5 | — |
| X13.6c | reflected power | 25 | % |
| X13.6d | transmitted power | 75 | % |
| X13.6e | ideal coating index | 1.342 | — |
| X13.6f | ideal coating thickness | 102.5 | nm |
| X13.6g | MgF2-coated reflectance | 0.0794 | % |
| X13.6h | bare glass reflectance | 8.163 | % |
| X13.6i | Brewster angle | 55.41 | ° |
| X13.6j | critical angle | 43.60 | ° |
| X13.7a | launched voltage | 1.333 | V |
| X13.7b | source reflection coefficient | −0.3333 | — |
| X13.7c | load reflection coefficient | 0.6 | — |
| X13.7d | load voltage after T | 2.133 | V |
| X13.7e | load voltage after 3T | 1.707 | V |
| X13.7f | load voltage after 5T | 1.792 | V |
| X13.7g | final load voltage | 1.778 | V |
| X13.7h | capacitive-load time constant | 100 | ps |
| X13.7i | 10–90% rise time | 219.7 | ps |
| X13.8a | characteristic impedance | 50 | Ω |
| X13.8b | phase velocity | 1.667 × 10⁸ | m/s |
| X13.8c | effective permittivity | 3.236 | — |
| X13.8d | open-stub reactance | −126.3 | Ω |
| X13.8e | equivalent capacitance | 1.260 | pF |
| X13.8f | lumped capacitance | 1.2 | pF |
| X13.8g | excess over lumped | 5.02 | % |
| X13.8h | transformer impedance | 70.71 | Ω |
| X13.8i | transformer length | 1.667 | cm |
| X13.9a | input resistance at λ/4 | 100 | Ω |
| X13.9b | input reactance at λ/4 | 50 | Ω |
| X13.9c | reflection magnitude | 0.4472 | — |
| X13.9d | VSWR | 2.618 | — |
| X13.9e | return loss | 6.990 | dB |
| X13.9f | mismatch loss | 0.9691 | dB |
| X13.9g | first voltage minimum | 0.0369 | λ |
| X13.9h | first voltage maximum | 0.2869 | λ |
| X13.9i | stub position, first solution | 0.125 | λ |
| X13.9j | stub length, first solution | 0.375 | λ |
| X13.9k | stub position, second solution | 0.4488 | λ |
| X13.9l | stub length, second solution | 0.125 | λ |
| X13.10a | L-network Q | 1.732 | — |
| X13.10b | series inductor | 3.829 | nH |
| X13.10c | shunt capacitor | 6.126 | pF |
| X13.10i | series-branch conductance at 800 MHz | 23.74 | mS |
| X13.10j | series-branch susceptance at 800 MHz | −36.54 | mS |
| X13.10k | capacitor susceptance at 800 MHz | 30.79 | mS |
| X13.10l | total susceptance at 800 MHz | −5.752 | mS |
| X13.10d | resistance at 800 MHz | 39.79 | Ω |
| X13.10e | reactance at 800 MHz | 9.64 | Ω |
| X13.10f | reflection at 800 MHz | 0.1555 | — |
| X13.10g | mismatch loss at 800 MHz | 0.1063 | dB |
| X13.11a | TE10 cutoff | 7.869 | GHz |
| X13.11b | TE20 cutoff | 15.74 | GHz |
| X13.11c | TE01 cutoff | 15.74 | GHz |
| X13.11d | phase constant at 13 GHz | 216.9 | rad/m |
| X13.11e | guide wavelength | 2.897 | cm |
| X13.11f | wave impedance | 473 | Ω |
| X13.11g | group velocity | 0.7960 | c |
| X13.11h | delay through 1 m | 4.190 | ns |
| X13.11i | TE101 resonance | 10.87 | GHz |
| X13.12a | EIRP | 29 | dBm |
| X13.12b | free-space path loss | 113.7 | dB |
| X13.12c | received power | −75.74 | dBm |
| X13.12d | effective aperture | 16.89 | cm² |
| X13.12e | link margin | 14.26 | dB |
| X13.12f | range at zero margin | 10.33 | km |
| X13.13a | radiation resistance at λ/25 | 1.262 | Ω |
| X13.13b | radiation efficiency | 55.80 | % |
| X13.14a | broadside EIRP | 39.08 | dBm |
| X13.14b | EIRP at 60° | 36.07 | dBm |
| X13.14c | PA DC power | 1.067 | W |
| X13.14d | highest grating-lobe-free frequency | 32.13 | GHz |
| X13.14e | spacing limit in wavelengths | 0.5359 | λ |
| X13.14f | spacing limit at 40 GHz | 4.02 | mm |
| X13.14g | fractional bandwidth | 50 | % |
| X13.14h | grating-lobe-free scan at 40 GHz | 29.93 | ° |
| X13.14i | element gain limit at 24 GHz | 3.04 | dBi |
| X13.14j | element gain limit at 28 GHz | 4.38 | dBi |
