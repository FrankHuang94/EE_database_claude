<!-- status: verified -->
# 13-10 · Waveguides and Resonators

| | |
|---|---|
| **Course** | [13 · Electromagnetics](../README.md) |
| **University equivalent** | The waveguide and cavity chapter of a junior electromagnetics course with a first look at dielectric guides: TE and TM modes of rectangular waveguide, cutoff, dispersion, wave impedance and attenuation, evanescent (below-cutoff) guides, rectangular cavity resonators and their Q, and step-index optical fibre (Pozar, *Microwave Engineering*, ch. 3 and 6; Ulaby & Ravaioli, *Fundamentals of Applied Electromagnetics*, ch. 8; Saleh & Teich, *Fundamentals of Photonics*, ch. 9) |
| **Prerequisites** | [13-08 Transmission Lines: Sinusoidal Steady State](13-08-transmission-lines-sinusoidal-steady-state.md), [13-06 Reflection and Transmission of Waves](13-06-reflection-and-transmission.md), [13-05 Plane Waves in Lossless and Lossy Media](13-05-plane-waves.md), [13-02 Electrostatics: Boundary-Value Problems](13-02-electrostatics-boundary-value-problems.md) (separation of variables) |
| **Estimated study hours** | 6 |
| **Last verified** | 2026-11-20 |

**Learning objectives.** After this chapter you can:

1. Derive the TE modes of a rectangular waveguide by separation of variables, and compute cutoff frequencies and the single-mode band.
2. Compute the propagation constant, guide wavelength, phase and group velocities and wave impedance of a mode, and its conductor attenuation.
3. Compute the attenuation of a guide below cutoff and use it to size EMI vents and attenuators.
4. Compute the resonant frequencies and conductor-loss Q of a rectangular cavity.
5. Compute a step-index fibre's numerical aperture, V-number, single-mode cutoff wavelength and mode field diameter.

---

## 1. Big picture

A transmission line needs two conductors. A hollow metal pipe has only one, so it cannot carry a TEM wave or DC, but above a certain frequency it guides waves with very low loss and high power handling: the plane wave bounces down the pipe between its walls. Close the pipe at both ends and it becomes a cavity, a resonator with a Q in the thousands. Replace the metal walls with a dielectric step and total internal reflection does the guiding: the optical fibre. These three structures carry radar power, set the frequency of microwave oscillators and filters, and carry nearly all long-distance data.

- **Waveguides** feed radar and satellite antennas and connect millimetre-wave test equipment, where coax becomes too lossy or too small.
- **Cutoff** is a feature as well as a limit: a pipe below cutoff blocks radio, which is how ventilation holes in shielded enclosures and microwave-oven doors work.
- **Cavities** make high-Q filters for base stations and the frequency references of some oscillators.
- **Single-mode fibre** carries every long-haul and most datacenter optical link (Course 24).

## 2. Intuition first

**Bouncing plane waves.** Picture two plane waves crossing at an angle inside a rectangular pipe, reflecting off the side walls. Their sum is zero at the walls (as a conductor requires for tangential E) and travels along the pipe. The criss-crossing slows the pattern's energy along the axis, and the angle depends on frequency: at high frequency the waves go almost straight down the pipe; as the frequency falls, they bounce more steeply, until at **cutoff** they bounce straight across and nothing moves along the guide. Below cutoff the field just decays.

**A pipe as a high-pass filter.** The cutoff frequency is the one at which half a wavelength fits across the guide's width. A WR-90 guide is 22.86 mm wide, so its first mode starts at the frequency whose half wavelength is 22.86 mm: 6.56 GHz.

**An analogy from finance, and its limits.** A waveguide behaves like a market with a minimum lot size: below a threshold (cutoff) no trade can happen at all, just above it trades happen slowly and expensively (low group velocity, high wave impedance), and well above it the market approaches frictionless (the free-space speed). The analogy captures the threshold and the approach to an asymptote but not the physics: the guide is linear and lossless in principle, and its "threshold" is set purely by geometry, with additional thresholds (higher modes) that open new parallel channels rather than replacing the first.

## 3. Theory

> **Conventions.** A rectangular guide has inner width $a$ (along $x$) and height $b$ (along $y$), with $a \ge b$, filled with a medium of $\varepsilon$, μ; the wave travels along $z$ as $e^{-j\beta z}$. $k = \omega\sqrt{\mu\varepsilon}$ is the medium's wavenumber and η its intrinsic impedance. Mode indices $m$, $n$ count half-wave variations across $a$ and $b$.

### 3.1 TE modes of a rectangular guide

With no axial electric field ($E_z$ = 0, TE), all transverse fields follow from $H_z$, which satisfies the Helmholtz equation of 13-04 in the cross-section:

$$
\Big(\frac{\partial^2}{\partial x^2} + \frac{\partial^2}{\partial y^2} + k_c^2\Big)H_z = 0, \qquad k_c^2 = k^2 - \beta^2 .
$$

Separation of variables (13-02) with the boundary condition that tangential E vanishes on the walls (which requires $\partial H_z/\partial n$ = 0 there) gives

$$
H_z = H_0\cos\frac{m\pi x}{a}\cos\frac{n\pi y}{b}\,e^{-j\beta z}, \qquad k_c^2 = \Big(\frac{m\pi}{a}\Big)^2 + \Big(\frac{n\pi}{b}\Big)^2 .
$$

Each pair $(m, n)$, not both zero, is a mode TE$_{mn}$. TM modes ($H_z$ = 0) have $E_z \propto \sin(m\pi x/a)\sin(n\pi y/b)$ with the same $k_c$, but need both $m, n \ge 1$.

**Cutoff.** The propagation constant is $\beta = \sqrt{k^2 - k_c^2}$, real only when $k > k_c$. The **cutoff frequency** is

$$
f_{c,mn} = \frac{1}{2\pi\sqrt{\mu\varepsilon}}\sqrt{\Big(\frac{m\pi}{a}\Big)^2 + \Big(\frac{n\pi}{b}\Big)^2} = \frac{c}{2\sqrt{\mu_r\varepsilon_r}}\sqrt{\Big(\frac{m}{a}\Big)^2 + \Big(\frac{n}{b}\Big)^2} .
$$

The lowest is TE$_{10}$, at $f_c = c/(2a)$ for an air-filled guide: the **dominant mode**. Its fields are $E_y \propto \sin(\pi x/a)$ (maximum at the centre, zero at the side walls) and $H$ in the $x$–$z$ plane. Between the TE$_{10}$ cutoff and the next one (TE$_{20}$ at $c/a$ when $a \ge 2b$) only the dominant mode propagates; standard guides are used over roughly the middle of this range (§9).

### 3.2 Propagation above cutoff

Writing $\beta = k\sqrt{1 - (f_c/f)^2}$:

- **Guide wavelength:** $\lambda_g = 2\pi/\beta = \lambda/\sqrt{1 - (f_c/f)^2}$, longer than in free space.
- **Phase velocity:** $v_p = \omega/\beta = c/\sqrt{1 - (f_c/f)^2}$, *faster* than light (no information travels at it).
- **Group velocity:** $v_g = d\omega/d\beta = c\sqrt{1 - (f_c/f)^2}$, slower than light, with $v_pv_g = c^2$. Energy and signals travel at $v_g$, which goes to zero at cutoff. The guide is dispersive: different frequencies arrive at different times, which limits the bandwidth of pulses sent through long runs.
- **Wave impedance:** the ratio of transverse E to transverse H, $Z_{TE} = k\eta/\beta = \eta/\sqrt{1 - (f_c/f)^2}$, larger than η and infinite at cutoff. (TM modes have $Z_{TM} = \eta\sqrt{1 - (f_c/f)^2}$.)

In the bouncing-plane-wave picture, the two plane waves travel at angle θ to the axis with $\cos\theta = \sqrt{1 - (f_c/f)^2}$: the axial component of their velocity is $v_g$, and the speed at which their crossing pattern moves along the wall is $v_p$.

![Dispersion diagram for air-filled WR-90: frequency against phase constant for TE10 (cutoff 6.56 GHz), TE20 (13.11 GHz), TE01 (14.75 GHz) and TE11/TM11 (16.15 GHz), each a hyperbola approaching the dashed light line at high frequency, with the recommended band from 8.2 to 12.4 GHz shaded where only TE10 propagates](../../../assets/figures/13-10/dispersion.svg)

*Figure 1. Dispersion diagram of WR-90. Each mode starts at its cutoff with β = 0 and approaches the light line from above; the slope $d\omega/d\beta$ is the group velocity, zero at cutoff. The recommended band (shaded) sits where only TE₁₀ propagates and its curve has straightened.*

**Attenuation.** Wall currents flow in the metal's skin depth, dissipating $\tfrac12R_s\lvert H_t\rvert^2$ per unit area (13-05). Integrating over the walls for TE$_{10}$ gives (Pozar)

$$
\alpha_c = \frac{R_s}{a^3b\beta k\eta}\,\big(2b\pi^2 + a^3k^2\big)\quad\text{Np/m} .
$$

It is large near cutoff (β → 0) and has a broad minimum in the recommended band. For copper WR-90 at 10 GHz it is about 0.11 dB/m (Example 13-10.3), far below the loss of coax at the same frequency.

### 3.3 Below cutoff: evanescent guides

Below cutoff, β becomes imaginary: $\gamma = \alpha = \sqrt{k_c^2 - k^2}$. The field decays without propagating, by $e^{-\alpha z}$, carrying no power (as the evanescent wave of 13-06 did). Far below cutoff $\alpha \approx k_c = \pi/a$, independent of frequency: about 27 dB of attenuation per guide width. A tube whose length is several times its width is an excellent filter for everything below its cutoff. This is how a microwave oven's door mesh (holes far smaller than the 12 cm wavelength) keeps the energy in while letting light through, and how honeycomb vents on shielded rooms pass air but not radio (Example 13-10.4). Below-cutoff attenuators also make precise, frequency-independent RF attenuators.

### 3.4 Cavity resonators

Short both ends of a guide of length $d$. The standing waves must have a whole number of half-waves along $z$ too, so $\beta = \ell\pi/d$ and the resonant frequencies are

$$
f_{mn\ell} = \frac{c}{2\sqrt{\mu_r\varepsilon_r}}\sqrt{\Big(\frac{m}{a}\Big)^2 + \Big(\frac{n}{b}\Big)^2 + \Big(\frac{\ell}{d}\Big)^2} .
$$

For $b < a < d$ the lowest is TE$_{101}$. The **quality factor** compares stored energy to the energy lost per radian of oscillation, $Q = \omega_0W/P_{loss}$. For TE$_{10\ell}$ with wall loss only (Pozar),

$$
Q_c = \frac{(kad)^3b\eta}{2\pi^2R_s}\,\frac{1}{2\ell^2a^3b + 2bd^3 + \ell^2a^3d + ad^3} ,
$$

which gives several thousand for copper at X band (Example 13-10.5). The Q is roughly (volume)/(surface × skin depth): big cavities with smooth, highly conducting walls store much and lose little. Dielectric resonators (ceramic pucks with $\varepsilon_r$ of 30 to 80) shrink the cavity by $\sqrt{\varepsilon_r}$ and are used in base-station filters and low-noise oscillators. Near one resonance, a cavity behaves like a parallel RLC circuit with the same $f_0$ and Q; the lab's netlist uses that model.

### 3.5 Dielectric guides and optical fibre

A dielectric slab or rod of higher index $n_1$ surrounded by lower index $n_2$ guides light by total internal reflection (13-06). The field is a standing wave inside the core and an evanescent tail in the cladding. For a step-index fibre of core radius $a$, the modes are characterized by the **V-number**

$$
V = \frac{2\pi a}{\lambda}\,\text{NA}, \qquad \text{NA} = \sqrt{n_1^2 - n_2^2} .
$$

Only the fundamental mode (LP$_{01}$) is guided when $V$ < 2.405, the first zero of the Bessel function $J_0$. This sets the **cutoff wavelength** $\lambda_c = 2\pi a\,\text{NA}/2.405$: a fibre is single-mode at wavelengths longer than $\lambda_c$. In the weakly guiding approximation ($n_1 \approx n_2$), the LP$_{01}$ field is $J_0(u\rho/a)$ in the core and $K_0(w\rho/a)$ in the cladding, with $u^2 + w^2 = V^2$ and the matching condition

$$
\frac{uJ_1(u)}{J_0(u)} = \frac{wK_1(w)}{K_0(w)} ,
$$

which the lab solves numerically. The field is close to Gaussian; the diameter of the best-fitting Gaussian is the **mode field diameter** (MFD), somewhat larger than the core because of the evanescent tail. The MFD sets how tolerant splices and connectors are to misalignment and how efficiently light couples from a laser or a silicon-photonics chip.

> **Deeper:** see companion repo *Datacenter Networking* for optical transceivers and fibre plant in datacenters.

## 4. Worked examples

### Example 13-10.1 · The modes of WR-90 (tier A)

**Setup.** WR-90 has inside dimensions 22.86 mm × 10.16 mm [1]. Find the cutoff frequencies of TE$_{10}$, TE$_{20}$, TE$_{01}$ and TE$_{11}$/TM$_{11}$ when air-filled, and the single-mode band.

**Solution.** $f_c = (c/2)\sqrt{(m/a)^2 + (n/b)^2}$: TE$_{10}$ **6.557** GHz, TE$_{20}$ **13.11** GHz, TE$_{01}$ **14.75** GHz, TE$_{11}$ and TM$_{11}$ **16.15** GHz. Only TE$_{10}$ propagates between 6.557 and 13.11 GHz.

**Sanity check.** TE$_{20}$ is exactly twice TE$_{10}$, and TE$_{01}$ comes later because $b < a/2$: guides are made about half as tall as wide precisely to push TE$_{01}$ above TE$_{20}$.

### Example 13-10.2 · TE₁₀ at 10 GHz (tier B)

**Setup.** For WR-90 at 10 GHz, find β, the guide wavelength, the phase and group velocities, and the wave impedance.

**Solution.** $k$ = 209.6 rad/m and $k_c = \pi/a$ = 137.4 rad/m, so β = **158.2** rad/m and $\lambda_g$ = **3.971** cm (against 3.0 cm in free space). $v_p = \omega/\beta$ = **3.971 × 10⁸** m/s and $v_g = c^2/v_p$ = **2.263 × 10⁸** m/s. $Z_{TE} = \eta_0/\sqrt{1 - (6.557/10)^2}$ = **499.0** Ω.

**Sanity check.** $v_pv_g = c^2$ (3.971 × 2.263 = 8.99 × 10¹⁶ m²/s²), and the impedance exceeds 377 Ω, rising toward infinity as the frequency approaches cutoff.

### Example 13-10.3 · Loss in copper WR-90 (tier B)

**Setup.** Find the conductor attenuation of copper WR-90 (σ = 5.8 × 10⁷ S/m) at 10 GHz.

**Solution.** $R_s = \sqrt{\pi f\mu_0/\sigma}$ = **26.09** mΩ. The TE$_{10}$ formula gives $\alpha_c$ = **0.01248** Np/m = **0.1084** dB/m.

**Sanity check.** The coax of Problem 13-05.13 lost 0.29 dB/m at only 1 GHz, and coax loss grows as $\sqrt f$ and faster: at 10 GHz a guide is about ten times better than a comparable coax, and it can carry far more power because there is no small centre conductor to concentrate the field.

### Example 13-10.4 · A honeycomb vent (tier B)

**Setup.** A shielded enclosure has a vent made of square tubes 5 mm on a side and 15 mm deep. Find the attenuation of a 2.4 GHz signal through one tube, treating it as a waveguide below cutoff.

**Solution.** The tube's TE$_{10}$ cutoff is $c/(2 \times 5\ \text{mm})$ = 30 GHz, far above 2.4 GHz. $\alpha = \sqrt{(\pi/0.005)^2 - k^2}$ = **626.3** Np/m, or **5440** dB/m, so 15 mm gives **81.60** dB.

**Sanity check.** α is almost exactly $\pi/a$ = 628.3 Np/m: far below cutoff the attenuation is set by the geometry alone, about 27 dB per width of depth. A thin sheet with 5 mm holes (depth ≈ 0) would give almost nothing; the depth is what works.

### Example 13-10.5 · An X-band cavity (tier B)

**Setup.** Close a length of WR-90 with copper walls to make a cavity 22.86 mm × 10.16 mm × 22.86 mm. Find the TE$_{101}$ resonant frequency, the conductor Q, and the 3 dB bandwidth.

**Solution.** $f_{101} = (c/2)\sqrt{(1/a)^2 + (1/d)^2}$ = **9.273** GHz. At that frequency $R_s$ = 25.12 mΩ, and the Q formula gives $Q_c$ = **7838**. The bandwidth is $f_0/Q$ = **1.183** MHz.

**Sanity check.** A lumped LC resonator at 9 GHz would struggle to reach a Q of 100; the cavity's volume-to-surface ratio, measured in skin depths, gives it nearly a hundred times more. Silver plating, or cooling, raises Q further.

### Example 13-10.6 · A single-mode fibre (tier C)

**Setup.** A step-index fibre has a core radius of 4.1 µm, core index 1.4504 and cladding index 1.4457 (illustrative values). Find the NA, the relative index step, the single-mode cutoff wavelength, and at 1310 nm the V-number, the normalized propagation constant $b = 1 - u^2/V^2$, the effective index, and the mode field diameter. Repeat V and MFD at 1550 nm.

**Solution.** NA = **0.1167** and Δ = $(n_1 - n_2)/n_1$ = **0.3240**%. $\lambda_c = 2\pi a\,\text{NA}/2.405$ = **1.250** µm, so the fibre is single-mode at both 1310 and 1550 nm. At 1310 nm, $V$ = **2.294**; solving the LP$_{01}$ equation gives $u$ = 1.618, so $b$ = **0.5029** and $n_{eff} = \sqrt{n_2^2 + b(n_1^2 - n_2^2)}$ = **1.4481**. Fitting a Gaussian to the computed field gives an MFD of **9.238** µm (Marcuse's empirical formula gives 9.312 µm). At 1550 nm, $V$ = **1.939** and the MFD grows to **10.63** µm.

**Sanity check.** The mode is much wider than the 8.2 µm core: at lower V more of the light travels in the cladding's evanescent tail, which is why the MFD grows with wavelength and why bending loss rises at long wavelengths.

### Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| T 13-10.a | TE10 cutoff of WR-90 | 6.56 | GHz |
| T 13-10.b | far-below-cutoff attenuation per guide width | 27 | dB |
| Ex 13-10.1a | TE10 cutoff | 6.557 | GHz |
| Ex 13-10.1b | TE20 cutoff | 13.11 | GHz |
| Ex 13-10.1c | TE01 cutoff | 14.75 | GHz |
| Ex 13-10.1d | TE11/TM11 cutoff | 16.15 | GHz |
| Ex 13-10.2a | phase constant | 158.2 | rad/m |
| Ex 13-10.2b | guide wavelength | 3.971 | cm |
| Ex 13-10.2c | phase velocity | 3.971 × 10⁸ | m/s |
| Ex 13-10.2d | group velocity | 2.263 × 10⁸ | m/s |
| Ex 13-10.2e | wave impedance | 499.0 | Ω |
| Ex 13-10.3a | surface resistance at 10 GHz | 26.09 | mΩ |
| Ex 13-10.3b | attenuation | 0.01248 | Np/m |
| Ex 13-10.3c | attenuation | 0.1084 | dB/m |
| Ex 13-10.4a | attenuation constant | 626.3 | Np/m |
| Ex 13-10.4b | attenuation | 5440 | dB/m |
| Ex 13-10.4c | through 15 mm | 81.60 | dB |
| Ex 13-10.5a | TE101 resonance | 9.273 | GHz |
| Ex 13-10.5b | surface resistance at resonance | 25.12 | mΩ |
| Ex 13-10.5c | conductor Q | 7838 | — |
| Ex 13-10.5d | 3 dB bandwidth | 1.183 | MHz |
| Ex 13-10.6a | numerical aperture | 0.1167 | — |
| Ex 13-10.6b | relative index step | 0.3240 | % |
| Ex 13-10.6c | cutoff wavelength | 1.250 | µm |
| Ex 13-10.6d | V at 1310 nm | 2.294 | — |
| Ex 13-10.6e | u at 1310 nm | 1.618 | — |
| Ex 13-10.6f | normalized propagation constant | 0.5029 | — |
| Ex 13-10.6g | effective index | 1.4481 | — |
| Ex 13-10.6h | MFD at 1310 nm (Gaussian fit) | 9.238 | µm |
| Ex 13-10.6i | MFD at 1310 nm (Marcuse formula) | 9.312 | µm |
| Ex 13-10.6j | V at 1550 nm | 1.939 | — |
| Ex 13-10.6k | MFD at 1550 nm | 10.63 | µm |
| Prac 13-10.a | WR-90 band start over TE10 cutoff | 1.251 | — |
| Prac 13-10.b | WR-90 band end over TE20 cutoff | 0.9455 | — |
| Sim 13-10.a | simulated cavity resonance | 9.273 | GHz |
| Sim 13-10.b | simulated cavity Q | 7838 | — |

*Every value is recomputed by [verify_13_10.py](../verify/verify_13_10.py): cutoffs and β by solving the guide's Helmholtz eigenproblem numerically on a finite-difference grid, the attenuation and Q by numerically integrating the wall losses and stored energy of the computed fields, the fibre mode by root finding on the Bessel-function matching condition with the MFD from a numerical Gaussian overlap. The cavity's RLC equivalent is simulated in ngspice.*

## 5. Simulate it

The lab, [labs/13-10-lab](../labs/13-10-lab/README.md), has a notebook and an ngspice netlist:

1. Plots the TE$_{10}$, TE$_{20}$ and TE$_{11}$ field patterns from the separated solutions.
2. Draws the dispersion diagram ($f$ against β) for the first modes of WR-90 and the group delay of a 1 m run against frequency.
3. Solves the guide's eigenproblem numerically on a grid to confirm the cutoffs, and computes below-cutoff attenuation against frequency.
4. Solves the fibre's LP$_{01}$ equation for a range of V, plots $b(V)$, and computes the MFD against wavelength.

The netlist [cavity_rlc.cir](../labs/13-10-lab/cavity_rlc.cir) models Example 13-10.5's cavity near resonance as a parallel RLC with the same $f_0$ and Q, and measures both from an AC sweep.

**Guided exercise (predict, then run).** **Before running the netlist**, predict the resonant frequency and the 3 dB bandwidth. Then run it. (**9.273** GHz and 1.183 MHz, a Q of **7838**.)

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Waveguide instead of coax | Loss and power handling at microwave and millimetre-wave frequencies | Size, rigidity, narrow band, cost of transitions | RF system engineer |
| Larger cavity or silver plating | Q (narrower, lower-loss filters) | Size, weight, cost; temperature drift | Filter designer |
| Dielectric resonators | Size reduced by √εr | Q limited by dielectric loss, cost | Filter and oscillator designer |
| Deeper below-cutoff vents | Shielding effectiveness | Airflow resistance, thickness | EMC and thermal engineers |
| Smaller fibre index step | Single-mode at shorter wavelengths, low dispersion | Bend sensitivity, larger MFD | Fibre designer |

## 7. Numbers to know

| Quantity | Value | Note |
|---|---|---|
| TE₁₀ cutoff | $c/2a$ | 6.557 GHz for WR-90 (a = 22.86 mm) |
| Phase × group velocity | $c^2$ | Phase faster, group slower than light |
| Below cutoff | ≈ 27 dB per guide width | $\alpha \approx \pi/a$ |
| Copper X-band waveguide loss | ≈ 0.1 dB/m | Against ≈ 1 dB/m for small coax |
| Copper X-band cavity Q | several thousand | $Q \sim$ volume/(area × δ) |
| Single-mode condition | V < 2.405 | First zero of $J_0$ |
| Standard single-mode fibre MFD (1310 nm) | 8.6–9.2 µm nominal | G.652.D, as of Nov 2026 [2] |

## 8. Common mistakes

- **Treating phase velocity as signal speed.** $v_p > c$ in a guide; energy and information travel at $v_g < c$.
- **Forgetting TE₀₁ and TE₂₀ when choosing a band.** Single-mode operation needs the frequency below both.
- **Using a thin perforated sheet as a below-cutoff vent.** The attenuation scales with the depth of the holes, not their number.
- **Quoting a cavity's unloaded Q as its filter Q.** Coupling to the outside loads the cavity and lowers Q.
- **Assuming the fibre's light stays in the core.** At V near 2 a large share travels in the cladding; the MFD exceeds the core diameter.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **Standard waveguides are specified by band.** WR-90 (IEC R100) has inside dimensions of 22.86 × 10.16 mm, a TE$_{10}$ cutoff of 6.557 GHz and a recommended band of 8.20 to 12.40 GHz [1] **[Established]**. The band starts at **1.251** times the TE$_{10}$ cutoff and ends at **0.9455** times the TE$_{20}$ cutoff (our arithmetic): it avoids the lossy, dispersive region near cutoff and stays clear of the next mode.
- **Single-mode fibre is standardized by its mode.** ITU-T G.652.D specifies a mode field diameter at 1310 nm with nominal values from 8.6 to 9.2 µm (±0.4 µm), a 125 µm cladding and a cable cut-off wavelength of at most 1260 nm [2] **[Established]**. Example 13-10.6's illustrative fibre (MFD 9.238 µm, cutoff 1.250 µm) falls within these limits.
- **Millimetre-wave and sub-terahertz test** uses waveguide bands whose sizes shrink with frequency; above about 100 GHz, waveguide flanges and their alignment become a significant source of measurement uncertainty **[Industry estimate]** (common metrology experience).

### Why it matters commercially

- **Optical links are fibre waveguides.** Every pluggable transceiver, co-packaged optics engine and silicon-photonics chip couples light into single-mode fibre, and the MFD match between chip and fibre is a large part of the coupling loss budget (Course 24).
- **Base-station and satellite filters** are cavities and dielectric resonators; their size, Q and temperature stability set filter performance and cost.
- **Shielded products** use below-cutoff vents and gaskets; the rules of §3.3 decide how much airflow a shielded enclosure can have.

### Marketing vs Reality

- **"Waveguide-grade shielding with ventilation."** *Reality:* only if the vent holes are small compared with the highest frequency of concern and several widths deep. *Sanity check:* compute $f_c = c/2a$ for the hole and the depth in widths.
- **"Our fibre has a larger core for easier alignment."** *Reality:* a larger MFD eases alignment but raises bend loss and changes dispersion, and it must still be single-mode at the operating wavelength. *Sanity check:* ask for the MFD, cutoff wavelength and bend loss together.

### Questions for engineering leaders

1. **"Why waveguide here instead of coax (or the reverse)?"**
   *Strong:* a loss, power and size comparison at the operating frequency. *Evasive:* "that's what the antenna uses."
2. **"What is your coupling loss into fibre, and what limits it?"**
   *Strong:* mode-field mismatch and alignment tolerances quantified, with the coupler design that addresses them. *Evasive:* "about 1 dB."
3. **"How do your cavity filters behave over temperature?"**
   *Strong:* the materials' thermal expansion and the compensation used, with measured drift. *Evasive:* "they are high-Q."

## 10. Concept check

**Q1.** Why can a hollow metal pipe not carry DC or a TEM wave?

<details><summary>Answer</summary>

A TEM wave needs a transverse static potential difference between two conductors (its fields are those of a 2D electrostatic problem); a single closed conductor has no such difference, so the transverse field would have to be zero. Only TE and TM modes, with a cutoff, are possible.

</details>

**Q2.** How can the phase velocity exceed the speed of light?

<details><summary>Answer</summary>

It is the speed at which the crossing pattern of two obliquely bouncing plane waves moves along the guide, which, like the point where waves strike a beach, can exceed the wave speed. Energy travels at the group velocity, $c\sqrt{1 - (f_c/f)^2}$, always less than $c$.

</details>

**Q3.** Why does a below-cutoff tube attenuate by about 27 dB per width?

<details><summary>Answer</summary>

Far below cutoff $\alpha \approx k_c = \pi/a$, so over a length equal to the width $a$ the field falls by $e^{-\pi}$, which is 27.3 dB.

</details>

**Q4.** What sets a cavity's Q?

<details><summary>Answer</summary>

The ratio of stored energy to energy lost per cycle. Stored energy scales with volume and wall loss with surface area times the skin depth, so $Q \sim$ volume/(area × δ): larger cavities and better conductors give higher Q. Scaling the same cavity to a higher frequency shrinks it in proportion to λ but shrinks δ only as $1/\sqrt f$, so its Q falls as $1/\sqrt f$.

</details>

**Q5.** When is a step-index fibre single-mode?

<details><summary>Answer</summary>

When $V = (2\pi a/\lambda)\text{NA} < 2.405$, the point at which the second mode (LP$_{11}$) would start to be guided; equivalently at wavelengths longer than the cutoff wavelength $2\pi a\,\text{NA}/2.405$.

</details>

**Q6.** Why does the mode field diameter grow with wavelength?

<details><summary>Answer</summary>

V falls as λ grows, the mode is less tightly confined, and more of its power spreads into the cladding's evanescent tail, widening the field.

</details>

Next: the [13-10 problem set](../problems/13-10-problems.md).

## 11. Key terms

[Waveguide](../../../reference/glossary.md#waveguide) · [Waveguide mode](../../../reference/glossary.md#waveguide-mode) · [Dominant mode](../../../reference/glossary.md#dominant-mode) · [Cutoff frequency](../../../reference/glossary.md#cutoff-frequency) · [Guide wavelength](../../../reference/glossary.md#guide-wavelength) · [Group velocity](../../../reference/glossary.md#group-velocity) · [Evanescent wave](../../../reference/glossary.md#evanescent-wave) · [Cavity resonator](../../../reference/glossary.md#cavity-resonator) · [Quality factor](../../../reference/glossary.md#quality-factor) · [Optical fiber](../../../reference/glossary.md#optical-fiber) · [V-number](../../../reference/glossary.md#v-number) · [Mode field diameter](../../../reference/glossary.md#mode-field-diameter)

## 12. Connections

- **Builds on:** separation of variables ([13-02](13-02-electrostatics-boundary-value-problems.md)); plane waves, skin effect and $R_s$ ([13-05](13-05-plane-waves.md)); total internal reflection and evanescent waves ([13-06](13-06-reflection-and-transmission.md)); line concepts ([13-08](13-08-transmission-lines-sinusoidal-steady-state.md)).
- **Next:** [13-11 Radiation and Antenna Fundamentals](13-11-radiation-and-antennas.md) lets the guided waves go free.
- **Used later:** microwave filters and resonators in Course 21; optical interconnect and silicon photonics in Course 24.

## 13. Further study

- D. M. Pozar, *Microwave Engineering*, ch. 3 (waveguides) and ch. 6 (resonators).
- F. T. Ulaby and U. Ravaioli, *Fundamentals of Applied Electromagnetics*, ch. 8 (waveguides and cavities).
- B. E. A. Saleh and M. C. Teich, *Fundamentals of Photonics*, ch. 9 (fibre optics).
- D. Marcuse, "Loss analysis of single-mode fiber splices," *Bell System Technical Journal* 56 (1977) (the Gaussian MFD formula).

## 14. Sources

1. Copper Mountain Technologies waveguide chart (2023) and Microwave Techniques rigid waveguide data (2023). [R-199](../../../reference/research-log.md#r-199--wr-90-rectangular-waveguide-dimensions-and-band).
2. ITU-T Recommendation G.652 (08/2024), Table 2. [R-197](../../../reference/research-log.md#r-197--itu-t-g652-single-mode-fibre-attributes).

The physics (modes, cutoff, cavities, fibre modes) is textbook material (Further study).
