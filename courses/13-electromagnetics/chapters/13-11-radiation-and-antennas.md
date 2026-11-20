<!-- status: reviewed -->
# 13-11 · Radiation and Antenna Fundamentals

| | |
|---|---|
| **Course** | [13 · Electromagnetics](../README.md) |
| **University equivalent** | The radiation and antennas chapter of a junior electromagnetics course: retarded potentials, the Hertzian dipole and its near and far fields, radiation resistance, patterns, directivity, gain and efficiency, the half-wave dipole, effective aperture, the Friis transmission equation and an introduction to arrays (Ulaby & Ravaioli, *Fundamentals of Applied Electromagnetics*, ch. 9–10; Balanis, *Antenna Theory*, ch. 2, 4 and 6) |
| **Prerequisites** | [13-04 Maxwell's Equations and Time-Varying Fields](13-04-maxwells-equations.md), [13-05 Plane Waves in Lossless and Lossy Media](13-05-plane-waves.md), [13-09 The Smith Chart and Impedance Matching](13-09-smith-chart-and-matching.md), [13-03 Magnetostatics and Inductance](13-03-magnetostatics-and-inductance.md) (vector potential) |
| **Estimated study hours** | 8 |
| **Last verified** | 2026-11-20 |

**Learning objectives.** After this chapter you can:

1. Derive the far fields of a Hertzian dipole from the retarded vector potential, and distinguish its near and far fields.
2. Compute radiation resistance, radiation efficiency, directivity, gain and half-power beamwidth from a radiation pattern.
3. Compute the half-wave dipole's radiation resistance and directivity by integrating its pattern.
4. Use effective aperture and the Friis equation to build a free-space link budget, including the effect of frequency.
5. Compute an array factor, steer its beam with a progressive phase, and identify grating lobes.

---

## 1. Big picture

Every wireless product ends at an antenna, the structure that lets guided energy go free as a wave and catches a tiny fraction of it at the other end. The physics is Maxwell's equations once more: accelerating charges radiate, and the radiated fields fall off as $1/r$, so power density falls as $1/r^2$ while the total power through any sphere stays constant. Two numbers dominate engineering: how the antenna distributes its power over angle (its gain), and how much of the power that reaches it actually radiates (its efficiency). The Friis equation then turns them into a link budget.

- **Link budgets** for phones, Wi-Fi, satellite and radar all start from the Friis equation.
- **Small antennas** in wearables and IoT devices are inefficient for fundamental reasons: their radiation resistance is tiny compared with their loss.
- **Arrays and beamforming** are how 5G millimetre-wave, Wi-Fi access points and radars overcome high path loss and steer beams electronically.
- **Exposure and regulation** are written in EIRP and power density (13-04): regulators cap the product of transmitter power and antenna gain.

## 2. Intuition first

**Why things radiate.** A static charge has a field that falls as $1/r^2$; a steady current a magnetic field that falls as $1/r^2$. When a charge accelerates, the change in its field travels outward at the speed of light, and that travelling "kink" falls only as $1/r$. Since power goes as field squared, $1/r$ fields carry the same total power through every sphere: energy escapes for good. An antenna is a structure designed to make charges accelerate coherently (an oscillating current) in a way that couples efficiently to free space.

**An opened transmission line.** A twin-wire line carries power with little radiation because the currents in its two wires are opposite and close together; their fields cancel at a distance. Bend the last quarter wavelength of each wire outward, in line, and the currents in the two arms now point the same way: their fields add, and the line radiates. That is the half-wave dipole.

**An analogy from finance, and its limits.** Gain is like a portfolio's concentration: an antenna cannot create power, only redistribute it, so higher gain in one direction must come with less elsewhere, as concentrating a fixed budget in one asset reduces exposure to the others. The analogy breaks at reciprocity: a receiving antenna has exactly the same pattern as when transmitting, with no counterpart in finance, and the "budget" here is conserved exactly by Maxwell's equations.

## 3. Theory

> **Conventions.** Spherical coordinates $(r, \theta, \phi)$ with the antenna along $z$. Phasors use $e^{j\omega t}$; $k = 2\pi/\lambda$; $\eta_0$ = 376.7 Ω. Radiation intensity $U(\theta, \phi) = r^2S$ (W/sr) is power per unit solid angle. Gains in dBi are relative to an isotropic radiator. Powers in dBm are relative to 1 mW.

### 3.1 Retarded potentials

13-03 found the static vector potential $\vec{A} = (\mu/4\pi)\int\vec{J}/R\,dv'$. When currents vary, the potential at distance $R$ responds to what the current was a time $R/c$ earlier. For phasors this delay is a phase factor:

$$
\tilde{\vec{A}}(\vec{r}) = \frac{\mu}{4\pi}\int\frac{\tilde{\vec{J}}(\vec{r}\,')\,e^{-jkR}}{R}\,dv' .
$$

With $\tilde{\vec{H}} = \nabla\times\tilde{\vec{A}}/\mu$ and, away from sources, $\tilde{\vec{E}} = \nabla\times\tilde{\vec{H}}/(j\omega\varepsilon)$, this gives the fields of any current distribution.

### 3.2 The Hertzian dipole

Take a short current element: current $I_0$ (peak phasor) along $z$ over a length $\ell \ll \lambda$. Then $\tilde{\vec{A}} = \hat{z}\,\mu I_0\ell e^{-jkr}/(4\pi r)$. Write it in spherical components, using $\hat{z} = \hat{r}\cos\theta - \hat\theta\sin\theta$: $A_r = A_z\cos\theta$, $A_\theta = -A_z\sin\theta$, $A_\phi = 0$, with $A_z = \mu I_0\ell e^{-jkr}/(4\pi r)$ independent of θ and φ. Nothing depends on φ, so the spherical curl (13-01) has only a φ-component:

$$
\mu\tilde H_\phi = (\nabla\times\tilde{\vec{A}})_\phi = \frac1r\Big[\frac{\partial(rA_\theta)}{\partial r} - \frac{\partial A_r}{\partial\theta}\Big] = \frac1r\Big[-\sin\theta\,\frac{\partial(rA_z)}{\partial r} + A_z\sin\theta\Big] .
$$

Since $rA_z \propto e^{-jkr}$, $\partial(rA_z)/\partial r = -jk\,rA_z$, so $\mu\tilde H_\phi = \sin\theta\,A_z(jk + 1/r)$, which is the first line below. The electric field follows from Ampère's law in the source-free region, $\tilde{\vec{E}} = \nabla\times\tilde{\vec{H}}/(j\omega\varepsilon)$, whose θ-component is $-(1/r)\,\partial(rH_\phi)/\partial r$ divided by $j\omega\varepsilon$. Differentiating $rH_\phi \propto (jk + 1/r)e^{-jkr}$ once more and using $\omega\varepsilon = k/\eta$:

$$
\begin{aligned}
\tilde H_\phi &= \frac{jkI_0\ell\sin\theta}{4\pi r}\Big[1 + \frac{1}{jkr}\Big]e^{-jkr}, \\
\tilde E_\theta &= \frac{j\eta kI_0\ell\sin\theta}{4\pi r}\Big[1 + \frac{1}{jkr} - \frac{1}{(kr)^2}\Big]e^{-jkr},
\end{aligned}
$$

plus a radial $\tilde E_r$ that falls as $1/r^2$ and faster. Three regimes appear. Close in ($kr \ll 1$) the $1/r^3$ term dominates $E$: it is the quasi-static field of an oscillating electric dipole, storing energy reactively. Far out ($kr \gg 1$) only the $1/r$ terms remain:

$$
\tilde E_\theta = \frac{j\eta kI_0\ell}{4\pi r}\sin\theta\,e^{-jkr}, \qquad \tilde H_\phi = \frac{\tilde E_\theta}{\eta} ,
$$

a spherical wave that locally looks like 13-05's plane wave: transverse, in phase, with $E/H = \eta$. The terms are equal at $kr$ = 1, that is $r = \lambda/2\pi$, the conventional boundary of the reactive near field.

**Radiated power and radiation resistance.** The far-field power density is $S = \lvert E_\theta\rvert^2/(2\eta)$; integrating over a sphere:

$$
P_{rad} = \int_0^{2\pi}\!\!\int_0^\pi\frac{\eta}{2}\Big(\frac{kI_0\ell}{4\pi}\Big)^2\sin^2\theta\,\sin\theta\,d\theta\,d\phi = \frac{\eta\pi}{3}\Big(\frac{I_0\ell}{\lambda}\Big)^2 .
$$

Writing $P_{rad} = \tfrac12I_0^2R_{rad}$ defines the **radiation resistance**,

$$
R_{rad} = \frac{2\pi\eta}{3}\Big(\frac{\ell}{\lambda}\Big)^2 \approx 789\Big(\frac{\ell}{\lambda}\Big)^2\ \Omega .
$$

For an antenna a fiftieth of a wavelength long it is only 0.3 Ω (Example 13-11.1). This formula assumes the current is uniform along the element. A real centre-fed short dipole has a current that falls roughly linearly to zero at its tips, so its average current is half the feed current and its radiation resistance a quarter of this: about 0.079 Ω at λ/50. Either way the conclusion stands. Any loss resistance in the conductors or matching network competes directly with it, so the **radiation efficiency** $e_r = R_{rad}/(R_{rad} + R_{loss})$ of small antennas is low. This is the fundamental difficulty of antennas in wearables and in low-frequency IoT devices.

### 3.3 Patterns, directivity and gain

The **radiation pattern** is $U(\theta, \phi)$ normalized to its maximum. The Hertzian dipole's is $\sin^2\theta$: a doughnut with nulls along the axis, maximum broadside, and a **half-power beamwidth** (between the angles where $U$ falls to half) of 90°.

**Directivity** compares the maximum to the average:

$$
D = \frac{4\pi U_{max}}{P_{rad}} = \frac{4\pi U_{max}}{\oint U\,d\Omega} .
$$

For $\sin^2\theta$: $\oint\sin^2\theta\,d\Omega = 8\pi/3$, so $D$ = 1.5, or 1.761 dBi. **Gain** includes efficiency: $G = e_rD$. The **EIRP** in the direction of maximum gain is $P_tG_t$, the power an isotropic radiator would need to produce the same peak power density, and it is what regulators limit (§9).

### 3.4 The half-wave dipole

A dipole of total length λ/2 fed at its centre carries an approximately sinusoidal current, zero at the tips: $I(z) = I_0\cos(kz)$ for $\lvert z\rvert \le \lambda/4$. Treat each piece $dz$ as a Hertzian dipole. In the far field its distance to the observer is $r - z\cos\theta$, which matters only in the phase, so the element contributes $d\tilde E_\theta = (j\eta kI(z)\,dz\sin\theta/4\pi r)\,e^{-jkr}e^{jkz\cos\theta}$. Summing,

$$
\tilde E_\theta = \frac{j\eta kI_0\sin\theta}{4\pi r}e^{-jkr}\int_{-\lambda/4}^{\lambda/4}\cos(kz)\,e^{jkz\cos\theta}\,dz .
$$

With $u = kz$ the integral is $(1/k)\int_{-\pi/2}^{\pi/2}\cos u\,\cos(u\cos\theta)\,du$ (the sine part is odd and vanishes), and the product-to-sum identity gives $(2/k)\cos(\tfrac\pi2\cos\theta)/\sin^2\theta$. So the far field is

$$
\tilde E_\theta = \frac{j\eta I_0}{2\pi r}\,\frac{\cos(\tfrac{\pi}{2}\cos\theta)}{\sin\theta}\,e^{-jkr} .
$$

Its pattern is slightly narrower than the Hertzian dipole's (half-power beamwidth 78.08°). Integrating the pattern numerically (there is no elementary closed form) gives a radiation resistance of **73.08** Ω and a directivity of **1.641** (2.151 dBi): an antenna that matches well to common 50 to 75 Ω lines, which is one reason it is the reference antenna of radio engineering ("dBd" means dB relative to a half-wave dipole). Its input reactance is zero at a length slightly shorter than λ/2, the usual practical resonant length.

![Left: polar power patterns of a Hertzian dipole and a half-wave dipole with the dipole axis vertical, both doughnut-shaped with nulls along the axis, the half-wave pattern slightly narrower. Right: the array factor in dB of eight isotropic elements spaced half a wavelength apart, with a main beam at broadside and, when steered, at 30 degrees, each with sidelobes about 13 dB down](../../../assets/figures/13-11/patterns.svg)

*Figure 1. Left: the Hertzian and half-wave dipole patterns (half-power beamwidths 90° and 78°). Right: an 8-element λ/2 array at broadside and steered to 30° by a progressive phase of −90° per element; steering widens the beam and shifts the sidelobes.*

### 3.5 Effective aperture and the Friis equation

A receiving antenna in a field of power density $S$ delivers (when matched) a power $P_r = SA_e$, where the **effective aperture** $A_e$ is an area. For the Hertzian dipole it can be computed directly. A field $E$ (peak) parallel to the dipole induces an open-circuit voltage $V_{oc} = E\ell$; a conjugate-matched load takes $\lvert V_{oc}\rvert^2/(8R_{rad})$ from a source of internal resistance $R_{rad}$ (07-06); and the incident power density is $S = E^2/(2\eta)$. So

$$
A_e = \frac{E^2\ell^2/(8R_{rad})}{E^2/(2\eta)} = \frac{\eta\ell^2}{4R_{rad}} = \frac{\eta\ell^2}{4}\cdot\frac{3\lambda^2}{2\pi\eta\ell^2} = \frac{3\lambda^2}{8\pi} = \frac{1.5\,\lambda^2}{4\pi} ,
$$

which is $D\lambda^2/(4\pi)$ with $D$ = 1.5. Reciprocity (an antenna's receiving and transmitting patterns are the same) and a thermodynamic argument (an antenna in a black-body enclosure must absorb as much as it radiates) show that the same ratio holds for every antenna:

$$
A_e = \frac{G\lambda^2}{4\pi} .
$$

A transmitter of power $P_t$ and gain $G_t$ produces $S = P_tG_t/(4\pi R^2)$ at distance $R$ in its far field. Multiplying by the receiver's $A_e$ gives the **Friis transmission equation**:

$$
\frac{P_r}{P_t} = G_tG_r\Big(\frac{\lambda}{4\pi R}\Big)^2, \qquad
P_r\,[\text{dBm}] = P_t\,[\text{dBm}] + G_t\,[\text{dBi}] + G_r\,[\text{dBi}] - 20\log_{10}\frac{4\pi R}{\lambda} .
$$

The last term is the **free-space path loss** (FSPL). It grows as $f^2$, which leads to the common statement that higher frequencies "travel less far". That is true only for antennas of fixed gain. For antennas of fixed physical **area**, $G = 4\pi A_e/\lambda^2$ grows as $f^2$ at each end, and the link improves as $f^2$ (Example 13-11.5). Millimetre-wave systems exploit this with arrays: many small elements make a large aperture that must then be pointed, which is what beamforming does.

The Friis equation assumes the far field (§3.6), free space, matched impedances and polarizations (13-05), and no obstacles; real links add mismatch, polarization, cable and fading margins.

### 3.6 Near field, far field and arrays

**Far-field distance.** For an antenna of largest dimension $D_a$ (written with a subscript to keep it apart from the directivity $D$), the phase difference between rays from its centre and edge to a distant point falls below π/8 when $r > 2D_a^2/\lambda$; beyond that distance (and $r \gg \lambda$) the pattern no longer changes with distance. A 1 m dish at 12 GHz has a far field beyond 80 m (Problem 13-11.4).

**Arrays.** $N$ identical elements spaced $d$ apart along a line, each fed with a progressive phase β, have a combined pattern equal to the element pattern times the **array factor**

$$
\text{AF}(\theta) = \frac{\sin(N\psi/2)}{N\sin(\psi/2)}, \qquad \psi = kd\sin\theta + \beta ,
$$

with θ measured from broadside. The main beam points where ψ = 0, so the phase $\beta = -kd\sin\theta_0$ steers it to $\theta_0$ with no moving parts: a **phased array**. Key properties:

- The peak gain is about $N$ times the element gain (+10 log₁₀ N dB) when the elements are about λ/2 apart.
- The broadside half-power beamwidth is about $0.886\lambda/(Nd)$ radians, widening by $1/\cos\theta_0$ when steered.
- Additional main beams, **grating lobes**, appear when ψ reaches ±2π within visible angles; avoiding them up to a scan angle $\theta_{max}$ requires $d < \lambda/(1 + \lvert\sin\theta_{max}\rvert)$, hence the usual λ/2 spacing.

Arrays are developed in Course 21 and their signal processing (beamforming) in Course 17.

## 4. Worked examples

### Example 13-11.1 · A short antenna (tier A)

**Setup.** An antenna is λ/50 long and carries a uniform 1 A peak current. Find its radiation resistance, its radiation efficiency if its conductors and matching network add 1 Ω of loss, and the peak electric field broadside at 1 km.

**Solution.** $R_{rad} = (2\pi\eta_0/3)(1/50)^2$ = **0.3156** Ω. Efficiency $0.3156/1.3156$ = **23.99**%. The field is $\eta_0kI_0\ell/(4\pi r) = \eta_0I_0(\ell/\lambda)/(2r)$ = **3.767** mV/m.

**Sanity check.** Three quarters of the power accepted by this antenna heats its conductors. Making the antenna a little longer helps a lot: $R_{rad}$ grows as the square of length.

### Example 13-11.2 · The Hertzian dipole's directivity (tier A)

**Setup.** Find the directivity of a Hertzian dipole in linear terms and dBi, and its half-power beamwidth.

**Solution.** $D = 4\pi U_{max}/\oint U\,d\Omega = 4\pi/(8\pi/3)$ = **1.5**, or **1.761** dBi. $\sin^2\theta = 1/2$ at θ = 45° and 135°, a half-power beamwidth of **90**°.

**Sanity check.** Even the simplest antenna has gain over isotropic, because it sends nothing along its axis; all real antennas have $D > 1$.

### Example 13-11.3 · The half-wave dipole by numerical integration (tier B)

**Setup.** Integrate the half-wave dipole's pattern to find its radiation resistance, directivity and half-power beamwidth.

**Solution.** With $U \propto [\cos(\tfrac{\pi}{2}\cos\theta)/\sin\theta]^2$, numerical integration gives $\int_0^\pi U\sin\theta\,d\theta$ = 1.219 (for unit maximum). Then $D = 2/1.219$ = **1.641** (**2.151** dBi), and $R_{rad} = (\eta_0/2\pi)\times 1.219$ = **73.08** Ω. The half-power points are at 50.96° and 129.04°, a beamwidth of **78.08**°.

**Sanity check.** The half-wave dipole is only slightly more directive than the Hertzian dipole (2.15 against 1.76 dBi), but its radiation resistance (73 Ω) is over two hundred times that of Example 13-11.1's λ/50 dipole (0.32 Ω): length buys efficiency far more than it buys gain.

### Example 13-11.4 · A Wi-Fi link budget (tier B)

**Setup.** Two half-wave dipoles 100 m apart in free space link at 2.4 GHz with 20 dBm transmitted. Find the free-space path loss, the received power, and the effective aperture of each dipole.

**Solution.** λ = 12.49 cm, so FSPL = $20\log_{10}(4\pi \times 100/0.1249)$ = **80.05** dB. $P_r$ = 20 + 2.15 + 2.15 − 80.05 = **−55.75** dBm. $A_e = 1.641\lambda^2/(4\pi)$ = **20.4** cm².

**Sanity check.** −56 dBm is a strong Wi-Fi signal; indoors, walls and multipath typically cost tens of dB more, which is why real coverage is far shorter than free-space arithmetic suggests.

### Example 13-11.5 · Is higher frequency really worse? (tier B)

**Setup.** Two antennas each with an effective aperture of 100 cm² (a 10 cm square) face each other 100 m apart. Find $P_r/P_t$ in dB at 2.4 GHz and at 28 GHz.

**Solution.** With fixed apertures, Friis becomes $P_r/P_t = A_{e,t}A_{e,r}/(\lambda R)^2$. At 2.4 GHz: **−61.93** dB. At 28 GHz: **−40.59** dB, over 21 dB better.

**Sanity check.** The ratio is $(28/2.4)^2$, **21.3** dB. The catch: at 28 GHz a 100 cm² aperture has a gain of $4\pi A_e/\lambda^2$ = **30.4** dBi (against **9.06** dBi at 2.4 GHz) and a correspondingly narrow beam, so it must be pointed, which is the job of a phased array. The argument needs apertures large against $\lambda^2/4\pi$ (12.4 cm² at 2.4 GHz): since directivity is at least 1, no lossless antenna has a smaller effective aperture, and the link is in the far field ($2D_a^2/\lambda$ is 3.7 m at 28 GHz for this aperture).

### Example 13-11.6 · An 8-element array at 28 GHz (tier C)

**Setup.** Eight isotropic elements are spaced λ/2 apart in a line. Find the array gain in dB, the half-power beamwidth at broadside, the progressive phase that steers the beam to 30°, and the beamwidth there.

**Solution.** The array gain is $10\log_{10}8$ = **9.031** dB. Computing $\lvert\text{AF}\rvert^2$ numerically, the broadside half-power beamwidth is **12.80**°. Steering to 30° needs $\beta = -kd\sin 30^\circ$ = **−90**° per element, and the beamwidth widens to **14.84**°.

**Sanity check.** The estimate $0.886\lambda/(Nd)$ = 0.2215 rad = 12.69° is close to 12.80°; dividing by cos 30° gives 14.65°, close to the computed 14.84°. At λ/2 spacing, no grating lobe appears for any steering angle short of endfire.

### Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| T 13-11.a | reactive near-field boundary in wavelengths | 0.159 | λ |
| T 13-11.b | Hertzian radiation-resistance coefficient | 789.0 | Ω |
| Ex 13-11.1a | radiation resistance | 0.3156 | Ω |
| Ex 13-11.1b | radiation efficiency | 23.99 | % |
| Ex 13-11.1c | peak field at 1 km | 3.767 | mV/m |
| Ex 13-11.2a | directivity | 1.5 | — |
| Ex 13-11.2b | directivity | 1.761 | dBi |
| Ex 13-11.2c | half-power beamwidth | 90 | ° |
| Ex 13-11.3a | pattern integral | 1.219 | — |
| Ex 13-11.3b | directivity | 1.641 | — |
| Ex 13-11.3c | directivity | 2.151 | dBi |
| Ex 13-11.3d | radiation resistance | 73.08 | Ω |
| Ex 13-11.3e | lower half-power angle | 50.96 | ° |
| Ex 13-11.3f | half-power beamwidth | 78.08 | ° |
| Ex 13-11.4a | free-space path loss | 80.05 | dB |
| Ex 13-11.4b | received power | −55.75 | dBm |
| Ex 13-11.4c | effective aperture | 20.4 | cm² |
| Ex 13-11.5a | path ratio at 2.4 GHz | −61.93 | dB |
| Ex 13-11.5b | path ratio at 28 GHz | −40.59 | dB |
| Ex 13-11.5c | improvement | 21.3 | dB |
| Ex 13-11.5d | gain of a 100 cm² aperture at 28 GHz | 30.4 | dBi |
| Ex 13-11.5e | gain of a 100 cm² aperture at 2.4 GHz | 9.06 | dBi |
| Ex 13-11.6a | array gain | 9.031 | dB |
| Ex 13-11.6b | broadside beamwidth | 12.80 | ° |
| Ex 13-11.6c | progressive phase for 30° | −90 | ° |
| Ex 13-11.6d | beamwidth at 30° | 14.84 | ° |
| Ex 13-11.6e | estimated broadside beamwidth | 12.69 | ° |
| Ex 13-11.6f | estimated beamwidth at 30° | 14.65 | ° |
| Prac 13-11.a | half-wavelength at 28 GHz | 5.353 | mm |
| Prac 13-11.b | side of an 8 × 8 array at λ/2 | 4.283 | cm |
| Prac 13-11.c | 6 GHz indoor PSD-limited EIRP, 160 MHz | 27.04 | dBm |
| Sim 13-11.a | simulated share of available power radiated | 24.0 | % |

*Every value is recomputed by [verify_13_11.py](../verify/verify_13_11.py): the dipole fields by numerically differentiating the retarded potential (curls by finite differences), radiated power and directivity by numerical integration over the sphere, the half-wave dipole by summing Hertzian elements along its sinusoidal current, and array patterns by direct summation of element phasors. The small antenna's efficiency is also simulated in ngspice with its matching network.*

## 5. Simulate it

The lab, [labs/13-11-lab](../labs/13-11-lab/README.md), has a notebook and an ngspice netlist:

1. Computes the field of a Hertzian dipole from its retarded potential and plots the $1/r$, $1/r^2$ and $1/r^3$ terms against distance, crossing at $r = \lambda/2\pi$.
2. Builds the pattern of dipoles of length λ/2, λ and 1.5λ by summing elements, and computes their directivity.
3. Runs a Friis link budget across frequency for fixed-gain and fixed-area antennas.
4. Plots array factors for 4, 8 and 16 elements, steers them, and shows grating lobes appearing at wide spacing.

The netlist [small_antenna.cir](../labs/13-11-lab/small_antenna.cir) matches Example 13-11.1's λ/50 antenna (0.3156 Ω radiation resistance plus 1 Ω loss) to 50 Ω at 100 MHz with an L-network and measures how much of the available power is radiated.

**Guided exercise (predict, then run).** **Before running the netlist**, predict the fraction of the source's available power that reaches the radiation resistance with a perfect match. Then run it. (**24.0**%: matching delivers all the power to the antenna, but the antenna's own loss still takes three quarters.)

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Larger antenna (in wavelengths) | Radiation resistance, efficiency, bandwidth | Size, industrial design | Antenna engineer, product designer |
| Higher gain | Range in the beam direction | Narrower coverage, pointing needed | System architect |
| More array elements | Gain, beam agility | Cost, power, calibration, heat | RF and system architects |
| Higher frequency | Bandwidth, smaller elements, more gain per area | Path loss for fixed gain, blockage, circuit efficiency | System architect, spectrum strategy |
| Matching network complexity | Bandwidth of a small antenna | Loss in the network itself | RF designer |

## 7. Numbers to know

| Quantity | Value | Note |
|---|---|---|
| Hertzian dipole | D = 1.5 (1.76 dBi); $R_{rad} \approx 789(\ell/\lambda)^2$ Ω | Doughnut pattern, HPBW 90° |
| Half-wave dipole | D = 1.64 (2.15 dBi); $R_{rad}$ ≈ 73 Ω | HPBW 78° |
| Effective aperture | $G\lambda^2/4\pi$ | 20 cm² for a dipole at 2.4 GHz |
| Free-space path loss | $20\log_{10}(4\pi R/\lambda)$ | 80 dB for 100 m at 2.4 GHz |
| Array gain | +3 dB per doubling of elements | At about λ/2 spacing |
| Far-field distance | $2D_a^2/\lambda$ | 80 m for a 1 m dish at 12 GHz |
| 6 GHz indoor Wi-Fi limit (US) | 30 dBm EIRP, 5 dBm/MHz | As of Nov 2026 [2] |

## 8. Common mistakes

- **Using Friis in the near field.** Below about $2D_a^2/\lambda$ (or a few wavelengths for small antennas) the pattern and the $1/r^2$ law do not hold.
- **Confusing gain and directivity.** Gain includes efficiency; a small antenna can have a respectable directivity and a poor gain.
- **Saying "higher frequencies travel less far" without a qualifier.** True for fixed gain; false for fixed aperture area.
- **Forgetting that matching does not create efficiency.** A perfect match delivers all the power to the antenna; how much it radiates depends on $R_{rad}$ against $R_{loss}$.
- **Spacing array elements too far apart.** Grating lobes appear when $d > \lambda/(1 + \lvert\sin\theta_{max}\rvert)$.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **5G millimetre-wave bands drive arrays.** 3GPP's frequency range FR2-1 spans 24.25 to 52.6 GHz, with TDD bands such as n257 (26.5–29.5 GHz) and n261 (27.5–28.35 GHz) [1] **[Established]**. At 28 GHz half a wavelength is **5.353** mm, so an 8 × 8 array at λ/2 spacing is only **4.283** cm on a side (our arithmetic): large arrays fit in base stations and small ones in phones.
- **Regulators cap EIRP and its density.** In the US 6 GHz band (5.925–7.125 GHz), an indoor access point is limited to 5 dBm/MHz EIRP and 30 dBm total EIRP; standard-power access points are allowed 23 dBm/MHz and 36 dBm in parts of the band [2] **[Established]**. The density limit means a 160 MHz channel can reach only **27.04** dBm EIRP (our arithmetic), and only a 320 MHz channel reaches the 30 dBm cap.
- **Small-antenna limits are fundamental.** The bandwidth and efficiency of electrically small antennas are bounded by their size in wavelengths (the Chu–Wheeler limit), so wearables and compact IoT devices trade size against efficiency and bandwidth **[Established]** (antenna theory; Course 21).

### Why it matters commercially

- **Coverage and battery life.** Every decibel of antenna efficiency in a phone or wearable translates into range or into transmit power and battery drain.
- **Millimetre-wave economics.** Phased-array modules (many transceiver channels, calibration, thermal design) are a large part of the cost of millimetre-wave radios **[Industry estimate]** (not quantified here); the array gain is what makes the link budget close.
- **Automotive radar** (in the 77 GHz region) and Wi-Fi sensing use arrays for angular resolution, set by aperture in wavelengths **[Industry estimate]** (band edges not cited here).

### Marketing vs Reality

- **"High-gain antenna for better coverage."** *Reality:* gain concentrates power; it improves range in the beam and worsens it elsewhere. *Sanity check:* ask for the pattern, not just the peak dBi.
- **"Our tiny antenna is 90% efficient across the band."** *Reality:* for an antenna much smaller than λ/2π, the Chu–Wheeler limit makes wide bandwidth and high efficiency incompatible. *Sanity check:* ask for measured radiated efficiency (in a chamber) across the band, not return loss.

### Questions for engineering leaders

1. **"What is your antenna's radiated efficiency in the product, with the user present?"**
   *Strong:* chamber measurements in free space and with phantom hand or head, per band. *Evasive:* "the antenna vendor quotes 2 dBi."
2. **"How did you size your array?"**
   *Strong:* a link budget with path loss, required SNR and EIRP limits leading to element count and spacing. *Evasive:* "64 elements is standard."
3. **"Where is your EIRP limited: by the power amplifier, by thermal design, or by regulation?"**
   *Strong:* a clear identification of the binding constraint in each band. *Evasive:* "we transmit at maximum power."

## 10. Concept check

**Q1.** Why do radiated fields fall as $1/r$ while static fields fall as $1/r^2$?

<details><summary>Answer</summary>

Radiated energy must cross every enclosing sphere undiminished, so power density must fall as $1/r^2$ and fields as $1/r$. Static fields carry no net power outward and fall faster; the $1/r$ terms appear only from time variation (retardation).

</details>

**Q2.** Why are small antennas inefficient?

<details><summary>Answer</summary>

Radiation resistance scales as $(\ell/\lambda)^2$, so a small antenna's $R_{rad}$ is tiny and comparable to or smaller than its conductor and matching losses, which then absorb most of the power.

</details>

**Q3.** What is the difference between directivity and gain?

<details><summary>Answer</summary>

Directivity describes how the radiated power is distributed over angle; gain multiplies it by the radiation efficiency, so it describes how the power accepted at the terminals is distributed.

</details>

**Q4.** Why does a link between fixed-area antennas improve with frequency?

<details><summary>Answer</summary>

Each antenna's gain is $4\pi A_e/\lambda^2$, growing as $f^2$, while free-space loss grows as $f^2$ only once: the net is $A_{e,t}A_{e,r}/(\lambda R)^2$, which improves as $f^2$. The price is narrower beams that must be pointed.

</details>

**Q5.** How does a phased array steer without moving?

<details><summary>Answer</summary>

A progressive phase β between elements makes their fields add in phase in the direction where $kd\sin\theta = -\beta$; changing β electronically moves that direction.

</details>

**Q6.** What causes grating lobes, and how are they avoided?

<details><summary>Answer</summary>

When the elements are more than about half a wavelength apart, there are other directions where the path differences are whole wavelengths, so the fields add in phase there too. Spacing $d < \lambda/(1 + \lvert\sin\theta_{max}\rvert)$ keeps them out of visible space for scans up to $\theta_{max}$.

</details>

Next: the [13-11 problem set](../problems/13-11-problems.md).

## 11. Key terms

[Antenna](../../../reference/glossary.md#antenna) · [Hertzian dipole](../../../reference/glossary.md#hertzian-dipole) · [Radiation resistance](../../../reference/glossary.md#radiation-resistance) · [Radiation efficiency](../../../reference/glossary.md#radiation-efficiency) · [Radiation pattern](../../../reference/glossary.md#radiation-pattern) · [Directivity](../../../reference/glossary.md#directivity) · [Antenna gain](../../../reference/glossary.md#antenna-gain) · [EIRP](../../../reference/glossary.md#eirp) · [Effective aperture](../../../reference/glossary.md#effective-aperture) · [Friis transmission equation](../../../reference/glossary.md#friis-transmission-equation) · [Far field](../../../reference/glossary.md#far-field) · [Array factor](../../../reference/glossary.md#array-factor) · [Phased array](../../../reference/glossary.md#phased-array)

## 12. Connections

- **Builds on:** the vector potential ([13-03](13-03-magnetostatics-and-inductance.md)); Maxwell's equations and the Poynting vector ([13-04](13-04-maxwells-equations.md)); plane waves and polarization ([13-05](13-05-plane-waves.md)); matching ([13-09](13-09-smith-chart-and-matching.md)).
- **Next:** the Course 13 exam and the [course README](../README.md); then Course 14.
- **Used later:** link budgets and modulation in Course 17; RF front ends, arrays and small antennas in Course 21; wireless products in the practitioner layer.

## 13. Further study

- F. T. Ulaby and U. Ravaioli, *Fundamentals of Applied Electromagnetics*, ch. 9 (radiation, antennas and arrays).
- MIT OpenCourseWare 6.013, *Electromagnetics and Applications*: the lecture notes and videos on radiation, antennas and arrays.
- C. A. Balanis, *Antenna Theory: Analysis and Design*, ch. 2 (parameters), 4 (wire antennas) and 6 (arrays).
- J. D. Kraus and R. J. Marhefka, *Antennas*, ch. 2–5.

## 14. Sources

1. ETSI TS 138 104 V19.6.0 (3GPP TS 38.104 Release 19), Tables 5.1-1 and 5.2-2. [R-083](../../../reference/research-log.md#r-083--board-dielectrics-propagation-5g-bands-and-rf-exposure).
2. US Code of Federal Regulations, 47 CFR § 15.407(a)(4)–(5). [R-200](../../../reference/research-log.md#r-200--fcc-6-ghz-unlicensed-u-nii-eirp-limits).

The physics (radiation, dipoles, Friis, arrays) is textbook material (Further study).
