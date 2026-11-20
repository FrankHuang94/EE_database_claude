<!-- status: verified -->
# 13-06 · Reflection and Transmission of Waves

| | |
|---|---|
| **Course** | [13 · Electromagnetics](../README.md) |
| **University equivalent** | The reflection-and-transmission chapter of a junior electromagnetics course: normal incidence on dielectrics and conductors, standing waves, multilayer matching, oblique incidence with Snell's law and the Fresnel coefficients, total internal reflection and the Brewster angle, and shielding (Ulaby & Ravaioli, *Fundamentals of Applied Electromagnetics*, ch. 8; Cheng, *Field and Wave Electromagnetics*, ch. 8; Hecht, *Optics*, ch. 4) |
| **Prerequisites** | [13-05 Plane Waves in Lossless and Lossy Media](13-05-plane-waves.md), [13-02 Electrostatics: Boundary-Value Problems](13-02-electrostatics-boundary-value-problems.md) (boundary conditions), [04-09 Waves and Optics Basics](../../04-physics-for-ee/chapters/04-09-waves-and-optics.md) |
| **Estimated study hours** | 8 |
| **Last verified** | 2026-11-20 |

**Learning objectives.** After this chapter you can:

1. Derive the reflection and transmission coefficients at normal incidence from the boundary conditions, and compute reflected and transmitted power and the standing-wave ratio.
2. Design a quarter-wave matching layer and a half-wave window, and explain them as impedance transformers.
3. Derive Snell's law from phase matching, and compute the Fresnel coefficients for TE and TM polarization.
4. Compute the critical angle, the evanescent field beyond it, and the Brewster angle, and explain where each is used.
5. Estimate the shielding effectiveness of a conducting sheet from absorption and reflection losses, and explain why real enclosures fall short of it.

---

## 1. Big picture

Every boundary between materials reflects part of a wave and transmits the rest. The split is decided by one quantity, the mismatch between the two media's intrinsic impedances, exactly as a load's mismatch to a transmission line decides how much of a signal bounces back (13-07, 13-08). Reflection is what radar measures, what antireflection coatings cancel, what makes metal enclosures shield, and what traps light inside an optical fibre.

- **Matching.** Antireflection coatings on lenses and solar cells, and radomes over radar antennas, are impedance transformers built from dielectric layers.
- **Fibre optics.** Total internal reflection guides light through kilometres of glass with a fraction of a decibel of loss per kilometre (§9).
- **Shielding and EMC.** A metal sheet reflects most of an incoming wave and absorbs the rest within a few skin depths; seams and holes, not the metal, set what leaks.
- **Polarization effects.** The Brewster angle explains why glare off water is polarized and how laser windows are made lossless.

## 2. Intuition first

**The boundary must agree with both sides.** On each side of an interface, a plane wave's $E/H$ ratio is that side's intrinsic impedance. At the boundary itself the tangential fields must be continuous. If the impedances differ, one wave cannot satisfy both requirements; a reflected wave appears to make up the difference. The bigger the mismatch, the bigger the reflection. A perfect conductor ($\eta$ = 0) forces the total $E$ to zero at its surface: the reflection is total and inverted.

**Bending at an angle.** When a wave hits a boundary obliquely, the wavefronts on both sides must line up along the boundary, or the fields could not match at every point. In the slower medium the wavelength is shorter, so the transmitted wave must tilt toward the normal to keep the same spacing along the boundary. That is Snell's law; it comes from geometry alone, before any impedances enter.

**An analogy from finance, and its limits.** Reflection at a mismatch resembles a price shock at a boundary between two markets with different liquidity: part of an order flow passes through and part "bounces" as a correction. The analogy captures the idea that the split depends on the mismatch of a single property on either side. It breaks down quickly: wave reflection is linear and exactly predictable, it conserves energy perfectly at a lossless boundary, and it depends on angle and polarization in ways no market analogy captures.

## 3. Theory

> **Conventions.** A plane wave travels in medium 1 ($\eta_1$, $\varepsilon_1$, $\mu_1$) toward the plane $z$ = 0, beyond which is medium 2 ($\eta_2$, …). The refractive index is $n = \sqrt{\mu_r\varepsilon_r}$ ($\sqrt{\varepsilon_r}$ for nonmagnetic media) and $\eta = \eta_0\sqrt{\mu_r/\varepsilon_r}$. Angles are measured from the normal. Reflection and transmission coefficients Γ and τ refer to the **electric field**.

### 3.1 Normal incidence

Let the incident wave be $\tilde{\vec{E}}^i = E_0e^{-jk_1z}\hat{x}$ with $\tilde{\vec{H}}^i = (E_0/\eta_1)e^{-jk_1z}\hat{y}$. The reflected wave travels in $-z$, so its $\vec{H}$ flips relative to $\vec{E}$: $\tilde{\vec{E}}^r = \Gamma E_0e^{+jk_1z}\hat{x}$ and $\tilde{\vec{H}}^r = -(\Gamma E_0/\eta_1)e^{+jk_1z}\hat{y}$. The transmitted wave is $\tilde{\vec{E}}^t = \tau E_0e^{-jk_2z}\hat{x}$, $\tilde{\vec{H}}^t = (\tau E_0/\eta_2)e^{-jk_2z}\hat{y}$. Both fields are tangential, so both are continuous at $z$ = 0:

$$
1 + \Gamma = \tau, \qquad \frac{1 - \Gamma}{\eta_1} = \frac{\tau}{\eta_2} .
$$

Solving,

$$
\Gamma = \frac{\eta_2 - \eta_1}{\eta_2 + \eta_1}, \qquad \tau = 1 + \Gamma = \frac{2\eta_2}{\eta_2 + \eta_1} .
$$

This is the same formula as a load's reflection coefficient on a transmission line, $(Z_L - Z_0)/(Z_L + Z_0)$ (13-07): the second medium acts as a load of impedance $\eta_2$ on the first.

**Power.** The incident, reflected and transmitted power densities are $\lvert E_0\rvert^2/2\eta_1$, $\lvert\Gamma\rvert^2$ times that, and $\lvert\tau\rvert^2\lvert E_0\rvert^2/2\eta_2$. So the fractions are

$$
R = \lvert\Gamma\rvert^2, \qquad T = \frac{\eta_1}{\eta_2}\lvert\tau\rvert^2 = 1 - \lvert\Gamma\rvert^2 \quad\text{(lossless media)}.
$$

If medium 2 is lossy, its impedance $\eta_2$ is complex and the transmitted power density is $\tfrac12\operatorname{Re}\{\tilde E^t\tilde H^{t*}\} = \tfrac12\lvert\tau E_0\rvert^2\operatorname{Re}\{1/\eta_2^*\}$, so in general $T = \lvert\tau\rvert^2\eta_1\operatorname{Re}\{1/\eta_2^*\}$ (with medium 1 lossless), which reduces to the formula above for real $\eta_2$. Here $R$ and $T$ are power fractions; §3.7 uses $R$ and $A$ differently, for the reflection and absorption losses in decibels (Schelkunoff's notation).

Note that τ can exceed 1 (going into a higher-impedance medium) without violating energy conservation; it is the power fraction that is bounded.

**Standing waves.** In medium 1 the total field is $E_0(e^{-jk_1z} + \Gamma e^{jk_1z})$. Its magnitude oscillates between $E_0(1 + \lvert\Gamma\rvert)$ and $E_0(1 - \lvert\Gamma\rvert)$, maxima and minima a quarter wavelength apart, and the **standing-wave ratio** is

$$
\text{SWR} = \frac{1 + \lvert\Gamma\rvert}{1 - \lvert\Gamma\rvert} .
$$

For a perfect conductor, Γ = −1: the field in front of it is $-2jE_0\sin(k_1z)\hat{x}$, a pure standing wave with zeros at the surface and every half wavelength in front of it, maxima of $2E_0$ midway, and no net power flow. The magnetic field has its maxima of $2E_0/\eta_1$ at the conductor, where it equals the surface current.

### 3.2 Layers: matching and windows

With a layer between two media, waves bounce back and forth inside it. Rather than summing the bounces, track the ratio of $E$ to $H$, the **wave impedance**, which is continuous across each boundary because both tangential fields are. Put the layer (impedance $\eta_2$, wavenumber $k_2$) between $z = 0$ and $z = d$, with medium 3 behind it. Inside the layer there is a forward and a backward wave:

$$
\tilde E_x = A\big[e^{-jk_2(z - d)} + \Gamma_3e^{jk_2(z - d)}\big], \qquad \tilde H_y = \frac{A}{\eta_2}\big[e^{-jk_2(z - d)} - \Gamma_3e^{jk_2(z - d)}\big] .
$$

At the back face only a transmitted wave leaves, so $\tilde E_x/\tilde H_y = \eta_3$ there; at $z = d$ this gives $\eta_2(1 + \Gamma_3)/(1 - \Gamma_3) = \eta_3$, so $\Gamma_3 = (\eta_3 - \eta_2)/(\eta_3 + \eta_2)$, the normal-incidence formula again. At the front face, $z = 0$,

$$
\eta_{in} = \frac{\tilde E_x}{\tilde H_y}\Big|_{z=0} = \eta_2\frac{e^{jk_2d} + \Gamma_3e^{-jk_2d}}{e^{jk_2d} - \Gamma_3e^{-jk_2d}} = \eta_2\,\frac{\eta_3\cos(k_2d) + j\eta_2\sin(k_2d)}{\eta_2\cos(k_2d) + j\eta_3\sin(k_2d)} ,
$$

where the last step substitutes $\Gamma_3$, multiplies through by $\eta_3 + \eta_2$ and uses $e^{\pm jx} = \cos x \pm j\sin x$. Dividing top and bottom by $\cos(k_2d)$ gives the form 13-08 will use for transmission lines,

$$
\eta_{in} = \eta_2\,\frac{\eta_3 + j\eta_2\tan(k_2d)}{\eta_2 + j\eta_3\tan(k_2d)} ,
$$

and the reflection seen from medium 1 is $(\eta_{in} - \eta_1)/(\eta_{in} + \eta_1)$. Two thicknesses are special.

- **Quarter-wave layer** ($k_2d = \pi/2$, so $d = \lambda_2/4$): with $\cos(k_2d) = 0$ and $\sin(k_2d) = 1$ in the cosine form, $\eta_{in} = \eta_2^2/\eta_3$. Choosing $\eta_2 = \sqrt{\eta_1\eta_3}$ makes $\eta_{in} = \eta_1$ and the reflection vanishes at the design wavelength. For optics this means $n_2 = \sqrt{n_1n_3}$: an antireflection coating. With a real material whose index is not exactly the geometric mean, the reflection is reduced, not eliminated (Example 13-06.3).
- **Half-wave layer** ($d = \lambda_2/2$): $\eta_{in} = \eta_3$, as if the layer were absent. A radome of half-wave thickness is transparent at its design frequency whatever its permittivity, though the transparency narrows with frequency (Problem 13-06.7).

### 3.3 Oblique incidence: Snell's law

Now let the wave arrive at angle $\theta_i$ from the normal, with the **plane of incidence** containing the normal and the direction of travel. Every field on either side varies along the boundary as $e^{-jk\sin\theta\,x}$; for the boundary conditions to hold at every $x$, these variations must match:

$$
k_1\sin\theta_i = k_1\sin\theta_r = k_2\sin\theta_t .
$$

So the angle of reflection equals the angle of incidence, and

$$
n_1\sin\theta_i = n_2\sin\theta_t \qquad\text{(Snell's law)}.
$$

Going into a denser medium ($n_2 > n_1$), the wave bends toward the normal; going out, away from it.

### 3.4 The Fresnel coefficients

The reflection now depends on the polarization. Any incident wave splits into two independent parts.

- **TE** (perpendicular, or *s*): $\vec{E}$ perpendicular to the plane of incidence, so it is entirely tangential to the boundary.
- **TM** (parallel, or *p*): $\vec{H}$ perpendicular to the plane of incidence, $\vec{E}$ in it.

Put the boundary at $z = 0$ with the plane of incidence the $xz$-plane; every field varies as $e^{-jk_1(x\sin\theta_i \pm z\cos\theta_i)}$ in medium 1 and $e^{-jk_2(x\sin\theta_t + z\cos\theta_t)}$ in medium 2, and at $z = 0$ the common factor $e^{-jk_1x\sin\theta_i}$ (equal to medium 2's by Snell's law) cancels.

**TE.** $\tilde{\vec{E}}$ is along $\hat{y}$ for all three waves, with amplitudes $E_0$, $\Gamma_\perp E_0$ and $\tau_\perp E_0$. Each $\tilde{\vec{H}} = \hat{k}\times\tilde{\vec{E}}/\eta$; with $\hat{k}_i = (\sin\theta_i, 0, \cos\theta_i)$, $\hat{k}_r = (\sin\theta_i, 0, -\cos\theta_i)$ and $\hat{k}_t = (\sin\theta_t, 0, \cos\theta_t)$, the tangential ($x$) components of $\tilde{\vec{H}}$ are $-E_0\cos\theta_i/\eta_1$, $+\Gamma_\perp E_0\cos\theta_i/\eta_1$ and $-\tau_\perp E_0\cos\theta_t/\eta_2$. Continuity of $E_y$ and $H_x$:

$$
1 + \Gamma_\perp = \tau_\perp, \qquad \frac{(1 - \Gamma_\perp)\cos\theta_i}{\eta_1} = \frac{\tau_\perp\cos\theta_t}{\eta_2} .
$$

These are the normal-incidence equations with $\eta_1/\cos\theta_i$ and $\eta_2/\cos\theta_t$ in place of $\eta_1$ and $\eta_2$, so the solution is the normal-incidence formula with those substitutions.

**TM.** Now $\tilde{\vec{H}}$ is along $\pm\hat{y}$ and $\tilde{\vec{E}}$ lies in the plane of incidence. The reference directions (the arrows that define a positive Γ∥ and τ∥, following Ulaby) are

$$
\begin{aligned}
\tilde{\vec{E}}^i &= E_0(\hat{x}\cos\theta_i - \hat{z}\sin\theta_i), & \tilde{\vec{H}}^i &= (E_0/\eta_1)\,\hat{y},\\
\tilde{\vec{E}}^r &= \Gamma_\parallel E_0(\hat{x}\cos\theta_i + \hat{z}\sin\theta_i), & \tilde{\vec{H}}^r &= -(\Gamma_\parallel E_0/\eta_1)\,\hat{y},\\
\tilde{\vec{E}}^t &= \tau_\parallel E_0(\hat{x}\cos\theta_t - \hat{z}\sin\theta_t), & \tilde{\vec{H}}^t &= (\tau_\parallel E_0/\eta_2)\,\hat{y},
\end{aligned}
$$

each with $\tilde{\vec{E}}\times\tilde{\vec{H}}$ along its own direction of travel (check: $(\hat{x}\cos\theta_i - \hat{z}\sin\theta_i)\times\hat{y} = \hat{k}_i$). Continuity of $E_x$ and $H_y$:

$$
(1 + \Gamma_\parallel)\cos\theta_i = \tau_\parallel\cos\theta_t, \qquad \frac{1 - \Gamma_\parallel}{\eta_1} = \frac{\tau_\parallel}{\eta_2} .
$$

Eliminating $\tau_\parallel = (\eta_2/\eta_1)(1 - \Gamma_\parallel)$ gives $\eta_1\cos\theta_i(1 + \Gamma_\parallel) = \eta_2\cos\theta_t(1 - \Gamma_\parallel)$. Solving the TE and TM pairs:

$$
\Gamma_\perp = \frac{\eta_2\cos\theta_i - \eta_1\cos\theta_t}{\eta_2\cos\theta_i + \eta_1\cos\theta_t}, \qquad
\Gamma_\parallel = \frac{\eta_2\cos\theta_t - \eta_1\cos\theta_i}{\eta_2\cos\theta_t + \eta_1\cos\theta_i},
$$

with $\tau_\perp = 1 + \Gamma_\perp$ and $\tau_\parallel = (1 + \Gamma_\parallel)\cos\theta_i/\cos\theta_t$. (Sign conventions for $\Gamma_\parallel$ differ between textbooks; this is Ulaby's, for which $\Gamma_\parallel = \Gamma_\perp$ at normal incidence.) The reflected power fractions are $\lvert\Gamma\rvert^2$ for each polarization; the transmitted fractions carry the extra factor $(\eta_1\cos\theta_t)/(\eta_2\cos\theta_i)$ for the change in beam cross-section and impedance (Problem 13-06.13).

> **Going deeper — impedances seen along the normal.** Each Fresnel formula is the normal-incidence formula with "effective" impedances: $\eta\cos\theta$ for TM and $\eta/\cos\theta$ for TE. Those are the ratios of the tangential $E$ to tangential $H$ in each polarization, which is exactly what a transmission line along $z$ sees. The multilayer formula of §3.2 works at oblique incidence with those impedances and $k_2\cos\theta_2$ in place of $k_2$.

### 3.5 Total internal reflection

Going from a denser to a less dense medium, Snell's law gives $\sin\theta_t = (n_1/n_2)\sin\theta_i$, which reaches 1 at the **critical angle**

$$
\theta_c = \arcsin\frac{n_2}{n_1} .
$$

Beyond it there is no real transmitted angle. The transmitted field still exists, but its component of $k$ normal to the boundary becomes imaginary:

$$
k_{2z} = -j\alpha, \qquad \alpha = k_0\sqrt{n_1^2\sin^2\theta_i - n_2^2} ,
$$

so the field decays as $e^{-\alpha z}$ away from the boundary: an **evanescent wave**. In the Fresnel formulas $\cos\theta_t = k_{2z}/k_2 = -jb$ with $b = \alpha/k_2$ real and positive (the sign that makes the field decay rather than grow). Then, for TE,

$$
\Gamma_\perp = \frac{\eta_2\cos\theta_i + j\eta_1b}{\eta_2\cos\theta_i - j\eta_1b} ,
$$

a complex number divided by its own conjugate, so $\lvert\Gamma_\perp\rvert = 1$ exactly; the same holds for $\Gamma_\parallel$. The reflection is total, with only a polarization-dependent phase shift (the basis of the Fresnel rhomb, which turns linear into circular polarization). The evanescent wave carries no average power across the boundary: **total internal reflection**. The evanescent field reaches a fraction of a wavelength into the second medium (Problem 13-06.12), which is how a nearby surface can "frustrate" the reflection and couple light out, the basis of fibre couplers and of the cladding's role in a fibre.

**Optical fibre.** A fibre's core ($n_1$) is surrounded by cladding of slightly lower index ($n_2$). Rays striking the core–cladding boundary beyond $\theta_c$ are trapped. Tracing back through the fibre's end face, a ray from air is trapped if its angle to the axis is less than $\arcsin(\text{NA})$, where the **numerical aperture** is $\text{NA} = \sqrt{n_1^2 - n_2^2}$ (Example 13-06.4). Single-mode fibres have cores so small that ray optics fails and the mode must be treated as a field (13-10).

### 3.6 The Brewster angle

For TM polarization between nonmagnetic dielectrics, $\Gamma_\parallel$ = 0 when $\eta_2\cos\theta_t = \eta_1\cos\theta_i$, that is (with $\eta = \eta_0/n$) $n_1\cos\theta_t = n_2\cos\theta_i$. Square it, write $\cos^2\theta_t = 1 - \sin^2\theta_t = 1 - (n_1^2/n_2^2)\sin^2\theta_i$ by Snell's law, and solve for $s = \sin^2\theta_i$: $n_1^2 - (n_1^4/n_2^2)s = n_2^2(1 - s)$, so $s(n_2^4 - n_1^4)/n_2^2 = n_2^2 - n_1^2$ and $\sin^2\theta_i = n_2^2/(n_1^2 + n_2^2)$. Then $\cos^2\theta_i = n_1^2/(n_1^2 + n_2^2)$, and the ratio gives

$$
\tan\theta_B = \frac{n_2}{n_1} ,
$$

the **Brewster angle**, at which the reflected and transmitted directions are perpendicular. For TE the same steps with $n_1\cos\theta_i = n_2\cos\theta_t$ lead to $n_1 = n_2$: between different nonmagnetic dielectrics there is no TE Brewster angle, so TE waves always reflect somewhat, so light reflected near $\theta_B$ is mostly TE polarized: glare off water and roads is horizontally polarized, which polarizing sunglasses block. Laser tubes use windows tilted at $\theta_B$ so that the TM-polarized beam passes with no reflection loss.

![Two panels of reflected power fraction against angle of incidence. Air into glass: TE reflectance rises steadily from 4% to 100% at grazing incidence, while TM falls to zero at the Brewster angle of 56.3 degrees before rising. Glass into air: TM falls to zero at 33.7 degrees, and both polarizations jump to total reflection at the critical angle of 41.8 degrees](../../../assets/figures/13-06/fresnel.svg)

*Figure 1. Fresnel power reflectances for glass ($n$ = 1.5). Both polarizations reflect 4% at normal incidence. TM reflection vanishes at the Brewster angle; going from glass into air, everything is reflected beyond the critical angle.*

### 3.7 Shielding by a conducting sheet

A conducting sheet of thickness $t$ attenuates a wave in two ways. **Reflection:** at the first face, the mismatch between $\eta_0$ and the conductor's tiny $\eta_c$ reflects almost everything; the field that enters is $\approx 2\eta_c/\eta_0$ of the incident, and at the exit face the field roughly doubles again, so the two faces together transmit about $4\lvert\eta_c\rvert/\eta_0$ of the field. **Absorption:** inside, the field decays by $e^{-t/\delta}$. In decibels, the **shielding effectiveness** for a plane wave is approximately

$$
\text{SE} \approx \underbrace{8.686\,\frac{t}{\delta}}_{A} + \underbrace{20\log_{10}\frac{\eta_0}{4\lvert\eta_c\rvert}}_{R} ,
$$

valid when $t$ is several skin depths (thinner sheets need a correction for the multiple internal reflections, which the lab computes exactly). The numbers are enormous (Example 13-06.6): a solid metal sheet is not where shields fail. Real enclosures leak through seams, ventilation holes, cable penetrations and display windows; a slot behaves as an antenna, and leaks badly once its length approaches half a wavelength. Near-field magnetic sources at low frequency are the other hard case: their wave impedance is far below 377 Ω, so the reflection term shrinks, and thin shields barely help (magnetic materials are used instead).

## 4. Worked examples

### Example 13-06.1 · Air to glass, straight on (tier A)

**Setup.** A plane wave in air meets glass ($\varepsilon_r$ = 2.25) at normal incidence. Find $\eta_2$, Γ, τ, the reflected and transmitted power fractions, and the standing-wave ratio in the air.

**Solution.** $\eta_2 = \eta_0/1.5$ = **251.2** Ω. $\Gamma = (251.2 - 376.7)/(251.2 + 376.7)$ = **−0.2** and τ = 1 + Γ = **0.8**. Reflected power: $\lvert\Gamma\rvert^2$ = **4**%. Transmitted: $(\eta_1/\eta_2)\tau^2 = 1.5 \times 0.64$ = **96**%. SWR = 1.2/0.8 = **1.5**.

**Sanity check.** 4% reflection per surface is the familiar figure for uncoated glass: a window has two surfaces and loses about twice that. In terms of index, $\Gamma = (n_1 - n_2)/(n_1 + n_2) = (1 - 1.5)/2.5$, the optics form.

### Example 13-06.2 · A wave against a metal wall (tier A)

**Setup.** A 2.4 GHz plane wave of 1 V/m peak strikes a perfectly conducting wall at normal incidence. Where in front of the wall is the total electric field largest, and what is it? Where is it zero? What is the magnetic field at the wall?

**Solution.** With Γ = −1 the field is $2E_0\lvert\sin k_1z\rvert$ in magnitude, $z$ measured from the wall. It is zero at the wall and every half wavelength, **6.246** cm, in front of it. Its maxima, **2** V/m, are at odd quarter-wavelengths: **3.123** cm and **9.369** cm from the wall. The magnetic field at the wall is $2E_0/\eta_0$ = **5.309** mA/m.

**Sanity check.** A small antenna or a sensor placed flat against a metal surface sees almost no electric field; moving it a quarter wavelength out doubles the field. This is why antennas over ground planes are spaced about λ/4 above them, and why microwave ovens heat unevenly.

### Example 13-06.3 · An antireflection coating (tier B)

**Setup.** Glass ($n$ = 1.5) in air reflects 4%. Find the ideal quarter-wave coating index, and the thickness of a magnesium fluoride coating ($n$ = 1.38) designed for 550 nm (green light). What is the reflectance at 550 nm with MgF₂?

**Solution.** The ideal index is $\sqrt{1 \times 1.5}$ = **1.225**, lower than any durable coating material. A quarter wave in MgF₂ at 550 nm is $550/(4 \times 1.38)$ = **99.64** nm. At the design wavelength the coating presents $\eta_{in} = \eta_2^2/\eta_3$, equivalent in index terms to $\Gamma = (n_1n_3 - n_2^2)/(n_1n_3 + n_2^2) = (1.5 - 1.9044)/(1.5 + 1.9044)$, so the reflectance is $\Gamma^2$ = **1.411**%, down from **4**%.

**Sanity check.** The coating cannot reach zero because 1.38 is not 1.225, but it cuts the reflection by almost two thirds. Multilayer coatings, with several indices, get below 0.5% across the visible band.

### Example 13-06.4 · Light trapped in glass (tier B)

**Setup.** (a) Find the critical angle from glass ($n$ = 1.5) into air. (b) An optical fibre has an illustrative core index of 1.468 and cladding index of 1.463. Find the critical angle at the core–cladding boundary, the numerical aperture, and the largest angle to the axis at which light from air is trapped.

**Solution.** (a) $\arcsin(1/1.5)$ = **41.81**°. (b) $\theta_c = \arcsin(1.463/1.468)$ = **85.27**°: rays must graze the boundary, within **4.73**° of parallel to the axis. $\text{NA} = \sqrt{1.468^2 - 1.463^2}$ = **0.1211**, and the acceptance half-angle in air is $\arcsin(0.1211)$ = **6.953**°.

**Sanity check.** A tiny index step (0.3%) makes a narrow acceptance cone. That is deliberate: a small step keeps the fibre single-mode for a usable core size and limits the spread of ray path lengths (dispersion).

### Example 13-06.5 · Fresnel and Brewster (tier B)

**Setup.** A wave in air strikes glass ($n$ = 1.5) at 45°. Find the transmission angle, $\Gamma_\perp$ and $\Gamma_\parallel$, and the reflected power fractions for each polarization. At what angle does TM reflection vanish?

**Solution.** Snell: $\sin\theta_t = \sin 45^\circ/1.5$, so $\theta_t$ = **28.13**°. With $\eta_2 = \eta_0/1.5$:

$$
\Gamma_\perp = \frac{\eta_2\cos 45^\circ - \eta_0\cos 28.13^\circ}{\eta_2\cos 45^\circ + \eta_0\cos 28.13^\circ} = \mathbf{-0.3033}, \qquad
\Gamma_\parallel = \mathbf{-0.09201} .
$$

So TE reflects **9.201**% of its power and TM **0.8466**%. TM reflection vanishes at the Brewster angle $\arctan 1.5$ = **56.31**°.

**Sanity check.** TM reflects far less than TE at every angle between 0 and grazing, and is zero at Brewster; at normal incidence both give 4%. (A curiosity of the Fresnel formulas: at 45°, $\Gamma_\parallel = -\Gamma_\perp^2$ exactly in this sign convention, which these numbers obey.)

### Example 13-06.6 · Shielding with copper foil (tier C)

**Setup.** Estimate the plane-wave shielding effectiveness of a 35 µm copper foil at 1 GHz.

**Solution.** δ = 2.090 µm, so $t/\delta$ = **16.75** and the absorption loss is $A = 8.686 \times 16.75$ = **145.5** dB. The conductor's impedance magnitude is $\lvert(1 + j)R_s\rvert$ = **11.67** mΩ, so the reflection loss is $R = 20\log_{10}(376.7/(4 \times 0.01167))$ = **78.14** dB. Total: **223.6** dB.

**Sanity check.** No measurement could see such a reduction: the number says that the foil itself is effectively perfect, and the shield's performance will be set entirely by its openings. A slot in the same enclosure might give only tens of decibels.

### Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 13-06.1a | glass intrinsic impedance | 251.2 | Ω |
| Ex 13-06.1b | reflection coefficient | −0.2 | — |
| Ex 13-06.1c | transmission coefficient | 0.8 | — |
| Ex 13-06.1d | reflected power | 4 | % |
| Ex 13-06.1e | transmitted power | 96 | % |
| Ex 13-06.1f | standing-wave ratio | 1.5 | — |
| Ex 13-06.2a | spacing of the zeros | 6.246 | cm |
| Ex 13-06.2b | maximum field | 2 | V/m |
| Ex 13-06.2c | first maximum | 3.123 | cm |
| Ex 13-06.2d | second maximum | 9.369 | cm |
| Ex 13-06.2e | magnetic field at the wall | 5.309 | mA/m |
| Ex 13-06.3a | ideal coating index | 1.225 | — |
| Ex 13-06.3b | MgF₂ thickness | 99.64 | nm |
| Ex 13-06.3c | coated reflectance | 1.411 | % |
| Ex 13-06.3d | uncoated reflectance | 4 | % |
| Ex 13-06.4a | glass-to-air critical angle | 41.81 | ° |
| Ex 13-06.4b | core–cladding critical angle | 85.27 | ° |
| Ex 13-06.4c | numerical aperture | 0.1211 | — |
| Ex 13-06.4d | acceptance half-angle | 6.953 | ° |
| Ex 13-06.4e | largest ray angle to the axis inside the core | 4.73 | ° |
| Ex 13-06.5a | transmission angle | 28.13 | ° |
| Ex 13-06.5b | TE reflection coefficient | −0.3033 | — |
| Ex 13-06.5c | TM reflection coefficient | −0.09201 | — |
| Ex 13-06.5d | TE reflected power | 9.201 | % |
| Ex 13-06.5e | TM reflected power | 0.8466 | % |
| Ex 13-06.5f | Brewster angle | 56.31 | ° |
| Ex 13-06.6a | thickness in skin depths | 16.75 | — |
| Ex 13-06.6b | absorption loss | 145.5 | dB |
| Ex 13-06.6c | conductor impedance magnitude | 11.67 | mΩ |
| Ex 13-06.6d | reflection loss | 78.14 | dB |
| Ex 13-06.6e | shielding effectiveness | 223.6 | dB |
| Prac 13-06.a | coax loss at 1 GHz over fibre loss, per unit length | 1067 | — |
| Sim 13-06.a | simulated transmitted step (1 V incident) | 0.8 | V |
| Sim 13-06.b | simulated reflected step | −0.2 | V |

*Every value is recomputed by [verify_13_06.py](../verify/verify_13_06.py): reflection coefficients by solving the boundary conditions as linear systems, layered structures by the transfer-matrix method, Snell's law by phase matching with root finding, standing-wave positions from the computed field, and the shield by an exact transfer matrix through the lossy sheet (checked against the A + R estimate). The normal-incidence case is also simulated in ngspice as a junction of two transmission lines.*

## 5. Simulate it

The lab, [labs/13-06-lab](../labs/13-06-lab/README.md), has a notebook and an ngspice netlist:

1. Plots the standing-wave envelope in front of a dielectric and a conductor, and reads off $S$ and the positions of the maxima.
2. Plots the Fresnel reflectances for TE and TM against angle, from air into glass and from glass into air, showing the Brewster angle and total internal reflection.
3. Computes the reflectance of a quarter-wave coating and a half-wave radome against frequency by the transfer-matrix method.
4. Computes the exact shielding effectiveness of a copper foil against frequency, with the A + R estimate.

The netlist [interface_line.cir](../labs/13-06-lab/interface_line.cir) models Example 13-06.1's air–glass boundary as a 376.7 Ω transmission line joined to a 251.2 Ω line, and launches a 1 V step.

**Guided exercise (predict, then run).** **Before running the netlist**, predict the voltage step that continues into the second line and the step that reflects back. Then run it. (**0.8** V transmitted and **−0.2** V reflected: the wave impedances of the two media act exactly like the characteristic impedances of two lines.)

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Quarter-wave coatings (single or multilayer) | Lower reflection at the design band | Bandwidth (single layer), cost and process steps (multilayer) | Optical or RF engineer |
| Half-wave radome thickness | Transparency at the design frequency | Narrow band; weight and strength trade against thickness | Antenna and mechanical engineers |
| Smaller core–cladding index step in fibre | Single-mode operation, low dispersion | Tighter bend tolerance, smaller acceptance angle | Fibre designer |
| Fewer, smaller apertures in an enclosure | Shielding effectiveness | Airflow, access, cost of gaskets | EMC and mechanical engineers |
| Operating near the Brewster angle | Loss-free TM transmission | Reflection of the TE component | Optical designer |

## 7. Numbers to know

| Quantity | Value | Note |
|---|---|---|
| Uncoated glass reflection | 4% per surface | $n$ = 1.5 |
| Glass-to-air critical angle | 41.8° | $\arcsin(1/1.5)$ |
| Air-to-glass Brewster angle | 56.3° | $\arctan 1.5$ |
| Perfect conductor | Γ = −1 | Field zero at the surface; maxima at λ/4 |
| Single-mode fibre attenuation (G.652.D cable, 1530–1565 nm) | ≤ 0.30 dB/km | As of Nov 2026 [1] |
| Solid copper foil at 1 GHz | > 200 dB shielding | Openings dominate in practice |

## 8. Common mistakes

- **Taking $\lvert\tau\rvert^2$ as the transmitted power.** It is $(\eta_1/\eta_2)\lvert\tau\rvert^2$ (times $\cos\theta_t/\cos\theta_i$ at oblique incidence); τ can exceed 1.
- **Mixing up TE and TM**, or using one textbook's $\Gamma_\parallel$ sign with another's formulas. State the convention.
- **Applying Snell's law beyond the critical angle** and computing a sine greater than 1: the transmitted wave is evanescent.
- **Expecting a half-wave window to work at all frequencies.** It is transparent only near its design frequency.
- **Judging a shield by its material.** Seams and apertures set real shielding effectiveness.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **Fibre loss is three orders of magnitude below coax.** ITU-T G.652.D specifies cabled single-mode fibre with attenuation of at most 0.30 dB/km at 1530–1565 nm and 0.40 dB/km from 1310 to 1625 nm, with a 125 µm cladding [1] **[Established]**. The 1 GHz coax of Problem 13-05.13 loses 0.32 dB per *metre* (conductor and dielectric together), **1067** times more per unit length (our arithmetic). Total internal reflection, with an evanescent tail confined to the cladding, is why light can be guided so efficiently.
- **Matching layers are everywhere.** Antireflection coatings on camera lenses and solar cells, matching layers on ultrasound and radar sensors, and radomes over antennas are all §3.2's quarter- and half-wave layers **[Established]** (textbook practice).
- **Enclosure shielding is limited by openings.** Solid metal provides far more attenuation than any requirement; EMC design focuses on seams, apertures and cable entries **[Established]** (standard EMC practice).

### Why it matters commercially

- **Optical interconnect** in datacenters and long-haul networks rests on total internal reflection in glass; its low loss is why links longer than a few metres at the highest data rates are optical **[Established]** (Course 24).
- **Automotive radar and 5G millimetre-wave** antennas sit behind bumpers, radomes and glass; reflections from these covers cost range and create blind spots, so cover thickness and material are tuned like §3.2's windows **[Established]**.
- **EMC compliance** is a launch gate for every electronic product; shielding cost is driven by apertures, gaskets and cable treatment, not sheet metal **[Industry estimate]**.

> **Deeper:** see companion repo *Datacenter Networking* for optical links in datacenters.

### Marketing vs Reality

- **"Our enclosure provides 100 dB of shielding."** *Reality:* at what frequency, for which field (electric or magnetic, near or far), and with the vents and connectors installed? *Sanity check:* ask for a measured shielding-effectiveness curve of the finished enclosure, not the material's data sheet value.
- **"Radar-transparent cover."** *Reality:* a cover is transparent only near its design frequency and angle. *Sanity check:* ask for the two-way loss and the reflection across the radar's full band and scan angles.

### Questions for engineering leaders

1. **"What sets the shielding effectiveness of your product: material, seams, or apertures?"**
   *Strong:* the dominant leakage path, with a measured or simulated number. *Evasive:* "we use a metal enclosure."
2. **"How did you design the radome or cover in front of your antenna?"**
   *Strong:* thickness chosen for the band (often half-wave in the material), with simulated loss versus angle. *Evasive:* "the industrial designer chose it."
3. **"Where does optical fibre replace copper in your system, and why there?"**
   *Strong:* a reach-versus-data-rate argument with the electrical loss budget. *Evasive:* "optics is the future."

## 10. Concept check

**Q1.** Why does a wave reflect at an interface between two lossless dielectrics?

<details><summary>Answer</summary>

The tangential $E$ and $H$ must be continuous, but each medium imposes its own ratio $E/H = \eta$. With $\eta_1 \neq \eta_2$, a single transmitted wave cannot satisfy both conditions; a reflected wave makes up the difference, with $\Gamma = (\eta_2 - \eta_1)/(\eta_2 + \eta_1)$.

</details>

**Q2.** How can τ be greater than 1 without creating energy?

<details><summary>Answer</summary>

τ is a ratio of electric fields. Power depends on $E^2/\eta$; going into a higher-impedance medium, a larger $E$ carries less power per unit $E^2$, and the power fractions always add to 1.

</details>

**Q3.** Where does Snell's law come from?

<details><summary>Answer</summary>

Phase matching: the incident, reflected and transmitted fields must vary identically along the boundary for the boundary conditions to hold everywhere on it, so $k_1\sin\theta_i = k_2\sin\theta_t$. It needs no impedances.

</details>

**Q4.** Why is glare off water polarized?

<details><summary>Answer</summary>

Near the Brewster angle the TM component (in the plane of incidence) is hardly reflected, so the reflected light is mostly TE, which for a horizontal surface means horizontally polarized.

</details>

**Q5.** Does any field exist beyond a totally reflecting boundary?

<details><summary>Answer</summary>

Yes, an evanescent field that decays exponentially away from the boundary over a fraction of a wavelength. It carries no average power across, but a second surface brought within its reach can couple power out (frustrated total internal reflection).

</details>

**Q6.** Why is a quarter-wave layer of index $\sqrt{n_1n_3}$ reflection-free at its design wavelength?

<details><summary>Answer</summary>

The reflections from its two faces are equal in magnitude (the impedance steps are equal in ratio) and, after the half-wavelength round trip through the layer, opposite in phase, so they cancel. Equivalently, a quarter-wave section transforms $\eta_3$ into $\eta_2^2/\eta_3 = \eta_1$.

</details>

Next: the [13-06 problem set](../problems/13-06-problems.md).

## 11. Key terms

[Reflection coefficient](../../../reference/glossary.md#reflection-coefficient) · [Transmission coefficient](../../../reference/glossary.md#transmission-coefficient) · [Standing wave](../../../reference/glossary.md#standing-wave) · [Voltage standing-wave ratio](../../../reference/glossary.md#voltage-standing-wave-ratio-vswr) · [Quarter-wave transformer](../../../reference/glossary.md#quarter-wave-transformer) · [Snell's law](../../../reference/glossary.md#snells-law) · [Fresnel equations](../../../reference/glossary.md#fresnel-equations) · [Critical angle](../../../reference/glossary.md#critical-angle) · [Total internal reflection](../../../reference/glossary.md#total-internal-reflection) · [Evanescent wave](../../../reference/glossary.md#evanescent-wave) · [Numerical aperture](../../../reference/glossary.md#numerical-aperture) · [Brewster angle](../../../reference/glossary.md#brewster-angle) · [Shielding effectiveness](../../../reference/glossary.md#shielding-effectiveness)

## 12. Connections

- **Builds on:** plane waves, η and skin depth from [13-05](13-05-plane-waves.md); boundary conditions from [13-02](13-02-electrostatics-boundary-value-problems.md) and [13-03](13-03-magnetostatics-and-inductance.md); Snell's law in [04-09](../../04-physics-for-ee/chapters/04-09-waves-and-optics.md).
- **Next:** [13-07 Transmission Lines: Time Domain](13-07-transmission-lines-time-domain.md) applies the same reflection coefficient to voltage and current waves on lines.
- **Used later:** input impedance and quarter-wave transformers on lines ([13-08](13-08-transmission-lines-sinusoidal-steady-state.md)), matching ([13-09](13-09-smith-chart-and-matching.md)), dielectric waveguides and fibre modes ([13-10](13-10-waveguides-and-resonators.md)).

## 13. Further study

- F. T. Ulaby and U. Ravaioli, *Fundamentals of Applied Electromagnetics*, ch. 8 (wave reflection and transmission).
- D. K. Cheng, *Field and Wave Electromagnetics*, ch. 8 (normal and oblique incidence).
- E. Hecht, *Optics*, ch. 4 (Fresnel equations, total internal reflection).
- H. W. Ott, *Electromagnetic Compatibility Engineering*, ch. 6 (shielding and apertures).

## 14. Sources

1. ITU-T Recommendation G.652 (08/2024), Table 2. [R-197](../../../reference/research-log.md#r-197--itu-t-g652-single-mode-fibre-attributes).

The physics (Fresnel equations, total internal reflection, shielding theory) is textbook material (Further study).
