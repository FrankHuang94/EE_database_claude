<!-- status: reviewed -->
# 04-09 · Waves and Optics Basics

| | |
|---|---|
| **Course** | [04 · Physics for EE](../README.md) |
| **University equivalent** | Waves and optics in University Physics I–III (Halliday, Resnick & Walker, the chapters on waves, interference, diffraction, and images and refraction; MIT 8.03, Vibrations and Waves) |
| **Prerequisites** | [04-08 Energy in Fields and Maxwell's Equations](04-08-maxwell-preview.md), [04-01](04-01-mechanics-essentials.md) (oscillators), [02-01](../../02-complex-numbers-des-and-linear-algebra/chapters/02-01-complex-numbers-euler-and-phasors.md) (phasors), [01-08](../../01-calculus-for-engineers/chapters/01-08-sequences-series-and-taylor.md) (small-angle approximations) |
| **Estimated study hours** | 10 |
| **Last verified** | 2026-11-18 |

**Learning objectives.** After this chapter you can:

1. Describe travelling waves with the wave equation and relate speed, wavelength, frequency and wavenumber for strings, sound and light.
2. Superpose waves to analyze interference (two sources, phased arrays, thin films), beats and standing waves.
3. Compute diffraction spreading and the Rayleigh resolution limit, and apply $CD = k_1\lambda/\text{NA}$ to lithography.
4. Apply the laws of reflection and refraction (Snell's law, Fresnel reflection, total internal reflection) to lenses, coatings and optical fibers, including numerical aperture and dispersion.
5. Use polarization (Malus's law, Brewster's angle) and relate the electromagnetic spectrum to optical interconnects.

## 1. Big picture

[04-08](04-08-maxwell-preview.md) showed that electric and magnetic fields propagate as waves. Waves of every kind (on strings, in air, in fiber, on circuit boards) obey the same few rules: they travel at a speed set by the medium, they add by superposition so that they can reinforce or cancel, they bend around obstacles by about a wavelength, and they reflect and refract at boundaries. These rules decide the smallest feature a lithography scanner can print, how far light travels in a fiber, why an antenna array can steer its beam electronically, and why a camera lens is coated. This chapter covers them at the level a BSEE graduate uses daily; [Course 13](../../13-electromagnetics/README.md) and [24-07](../../24-high-speed-io-signal-integrity-and-photonics/chapters/24-07-photonics-fundamentals.md) go deeper.

- **Lithography:** diffraction limits printed feature size, hence the move from 193 nm to 13.5 nm light and to higher numerical aperture ([25-02](../../25-fabrication-packaging-test-and-reliability/chapters/25-02-lithography.md)).
- **Optical interconnect:** fiber guides light by total internal reflection; loss and dispersion set reach, and datacenter optics are standardized by wavelength and reach ([24-07](../../24-high-speed-io-signal-integrity-and-photonics/chapters/24-07-photonics-fundamentals.md)).
- **Wireless:** antenna arrays steer beams by interference (5G millimeter wave, radar) ([21](../../21-rf-and-microwave-engineering/README.md)).
- **Resonators:** standing waves underlie lasers, crystal and MEMS resonators, and transmission-line stubs.
- **Displays and sensors:** polarization drives LCDs; thin-film interference makes anti-reflection coatings and optical filters.

## 2. Intuition first

**A wave moves a pattern, not the medium.** Shake one end of a rope and a bump travels along it; each bit of rope only moves up and down. The pattern carries energy and information from place to place. The speed depends on the medium (tension and mass for a rope, stiffness and density for sound, permittivity for light), not on how hard you shake.

**Waves add.** Where two waves meet, displacements simply add. Crest on crest makes a bigger crest; crest on trough cancels. This **superposition** is why two speakers can make a quiet spot, why soap films show colors and why an antenna array can point its beam without moving.

**Waves spread around edges.** Pass a wave through a gap and it fans out. The narrower the gap compared with the wavelength, the more it spreads: sound (wavelength a meter) bends around doorways; light (half a micrometer) mostly does not. To make a small spot, or to print a small feature, you need a short wavelength or a wide cone of light.

**Waves bend at boundaries.** Light slows in glass. A wavefront hitting glass at an angle has one edge slowed first, so it turns, like a column of marchers wheeling as one end steps onto mud. That is refraction; trapped at a shallow enough angle, light cannot get out at all, which is how fiber works.

**A finance analogy, and its limits.** Interference is like combining two strategies with correlated returns: in phase they amplify each other, out of phase they hedge to zero. *Where it breaks:* returns are random and correlations drift; wave interference is deterministic, set exactly by path lengths and wavelengths, and energy is never destroyed, only redistributed (dark fringes here mean brighter fringes there).

![Left: Young's two-slit interference pattern on a screen 1 m away at 633 nm, with bright fringes 3.165 mm apart under a single-slit envelope. Right: snapshots of the third standing-wave mode on a string, with fixed nodes at a third and two thirds of the length.](../../../assets/figures/04-09/interference-and-standing-waves.svg)

*Figure 1. Superposition at work: travelling waves from two slits interfere; counter-propagating waves on a string form a standing wave.*

## 3. Theory

> **Notation for this chapter.** $\lambda$ wavelength, $f$ frequency, $T = 1/f$ period, $k = 2\pi/\lambda$ wavenumber (rad/m), $\omega = 2\pi f$ angular frequency, $v$ wave speed, $n = c/v$ refractive index, NA numerical aperture, $I$ intensity. Angles are measured from the normal to a surface.

### 3.1 The wave equation and travelling waves

A wave on a string, a pressure wave in air and an electromagnetic wave (04-08) all satisfy the one-dimensional **wave equation**

$$
\frac{\partial^2y}{\partial x^2} = \frac{1}{v^2}\frac{\partial^2y}{\partial t^2} .
$$

Any function of $x - vt$ solves it: substitute $y = f(x - vt)$ and both sides equal $f''$. The shape slides along at speed $v$ without changing. Functions of $x + vt$ travel the other way.

**Where $v$ comes from: a string.** Take a short piece of string of length $dx$, mass $\mu\,dx$ (µ is mass per length), under tension $F_T$. If the string makes a small angle with the axis, the vertical components of tension at the two ends are $F_T\,\partial y/\partial x$ evaluated at $x + dx$ and at $x$, and their difference is the net vertical force, $F_T\,\partial^2y/\partial x^2\,dx$. Newton's second law (04-01) gives $\mu\,dx\,\partial^2y/\partial t^2 = F_T\,\partial^2y/\partial x^2\,dx$, which is the wave equation with

$$
v = \sqrt{F_T/\mu} .
$$

Stiffer (higher tension) means faster; heavier means slower. Every wave has an analogous pair: for sound in a gas, $v = \sqrt{\gamma RT/M}$ (about 343 m/s in air at 20 °C); for light, $v = 1/\sqrt{\mu\varepsilon} = c/n$.

**Sinusoidal waves.** The workhorse is $y = A\cos(kx - \omega t + \phi)$. At a fixed place it oscillates at frequency $f$; at a fixed instant it repeats every λ. Substituting into the wave equation gives

$$
v = \frac\omega k = \lambda f .
$$

In phasor form (02-01), $y = \text{Re}[\mathbf Ae^{j(\omega t - kx)}]$: travelling a distance $x$ delays the phase by $kx$. This phase delay is what interference, antenna arrays and transmission lines all exploit. A wave's intensity is proportional to the square of its amplitude, as 04-08 found for light ($E_0^2/2\eta_0$).

### 3.2 Superposition and interference

The wave equation is linear, so any sum of solutions is a solution: waves pass through each other and add. Two equal-frequency waves arriving at a point with a **path difference** Δ have a phase difference $k\Delta = 2\pi\Delta/\lambda$:

- **constructive** interference when $\Delta = m\lambda$ (amplitudes add),
- **destructive** interference when $\Delta = (m + \tfrac12)\lambda$ (they cancel),

for integer $m$. With phasors, the resultant amplitude of two equal waves with phase difference δ is $2A\cos(\delta/2)$, and the intensity $4I_0\cos^2(\delta/2)$: up to four times one wave's intensity at the bright points, zero at the dark ones, with the average unchanged.

**Two slits (Young, 1801).** Light through two narrow slits a distance $d$ apart reaches a screen at angle θ with path difference $d\sin\theta$. Bright fringes fall at $d\sin\theta = m\lambda$; on a screen at distance $L$, for small angles, they are spaced

$$
\Delta y = \frac{\lambda L}{d} .
$$

Measuring fringe spacing measures wavelength; this experiment established that light is a wave.

**Phased arrays.** Reverse the idea: feed a row of antennas spaced $d$ apart with signals whose phases increase by Δφ from one to the next. Their waves add in phase in the direction where the path difference $d\sin\theta$ compensates the phase step:

$$
kd\sin\theta = \Delta\varphi \quad\Longrightarrow\quad \sin\theta = \frac{\Delta\varphi}{kd} .
$$

Changing Δφ electronically steers the beam with no moving parts: 5G millimeter-wave phones and base stations, automotive radar and satellite terminals all do this (Example 04-09.2). Elements spaced too far apart produce unwanted extra beams (**grating lobes**): with spacing $d$, they appear once $d > \lambda/(1 + |\sin\theta_0|)$ when steering to angle $\theta_0$, so a spacing of λ/2 guarantees none at any steering angle, which is why array elements are typically λ/2 apart.

**Thin films.** Light reflecting from the top and bottom surfaces of a thin layer interferes. A layer a quarter-wavelength thick (in the layer's material) sends the second reflection back half a wavelength later, so the two cancel if they have equal strength. (This needs both reflections to undergo the same phase flip, which happens when the indices increase in order, $n_{\text{air}} < n_c < n_{\text{glass}}$, as for a coating on glass.) An **anti-reflection coating** on glass therefore uses a quarter-wave layer with index $n_c = \sqrt{n_{\text{glass}}}$ (Example 04-09.3). The same physics colors soap bubbles and oil films and makes the dielectric mirrors and filters inside lasers and optical transceivers.

**Beats.** Two waves of slightly different frequency $f_1$ and $f_2$ drift in and out of phase, so their sum swells and fades at the **beat frequency** $|f_1 - f_2|$. Musicians tune by eliminating beats; radios and optical coherent receivers deliberately mix signals to shift them to a lower frequency (heterodyning, [17](../../17-communication-systems/README.md)).

### 3.3 Standing waves and resonance

Two equal waves travelling in opposite directions add to

$$
A\cos(kx - \omega t) + A\cos(kx + \omega t) = 2A\cos(kx)\cos(\omega t) ,
$$

a **standing wave**: each point oscillates in place with amplitude $2A|\cos kx|$; the pattern does not travel. Points where $\cos kx = 0$, a half-wavelength apart, never move (**nodes**).

A wave confined between two reflectors becomes a standing wave, but only certain wavelengths fit. A string fixed at both ends (length $L$) must have nodes at both ends, so $L$ must hold a whole number of half-wavelengths:

$$
\lambda_n = \frac{2L}{n}, \qquad f_n = \frac{nv}{2L}, \qquad n = 1, 2, 3, \dots
$$

These are the **resonant modes**. Drive the system at one of them and the reflections reinforce every round trip: resonance, the wave version of the driven oscillator of [02-04](../../02-complex-numbers-des-and-linear-algebra/chapters/02-04-forced-response-and-resonance.md). Examples:

- **Laser cavities.** A semiconductor laser chip is a Fabry–Pérot cavity between its cleaved facets; its allowed modes are spaced $\Delta f = c/(2nL)$ (Example 04-09.4), where strictly $n$ is the *group* index, which for real laser materials exceeds the phase index because the index varies with wavelength. Single-wavelength lasers add gratings to pick one mode.
- **Transmission-line stubs.** A line open at its far end reflects a wave that returns to the input inverted after a round trip of half a wavelength when the line is a quarter-wave long: the input then looks like a short circuit. RF circuits use such stubs as filters and tuning elements; the netlist of Example 04-09.4 shows it.
- **Crystal and MEMS resonators** (04-01) are standing acoustic waves; microwave cavities and on-chip ring resonators are standing electromagnetic waves.

### 3.4 Diffraction and the limit of resolution

**Huygens' principle.** Every point on a wavefront acts as a source of secondary wavelets; the new wavefront is their sum. Behind an opening, the wavelets from different parts of the opening interfere.

**A single slit.** Light through a slit of width $a$ spreads. At angle θ, pair each wavelet in the top half of the slit with the one a distance $a/2$ below it; their path difference is $(a/2)\sin\theta$. When this is half a wavelength, every pair cancels, giving the first dark direction:

$$
a\sin\theta = \lambda .
$$

The central bright lobe spans $\pm\lambda/a$ (Figure 2). A narrower slit spreads light more. For a **circular aperture** of diameter $D$ (a lens, a telescope, a laser beam), the analogous result is $\sin\theta = 1.22\lambda/D$.

**The Rayleigh criterion.** Two point sources can just be resolved when the center of one's diffraction pattern falls on the first dark ring of the other: an angular separation of $1.22\lambda/D$. No lens, however perfect, can do better without changing λ or $D$. Microscopes, cameras and telescopes are all diffraction-limited.

**Lithography.** A scanner projects the image of a chip pattern onto photoresist through a lens of **numerical aperture** $\text{NA} = n\sin\theta_{\max}$, where $\theta_{\max}$ is the half-angle of the cone of light reaching the wafer. Diffraction sets the smallest printable feature, the critical dimension:

$$
CD = k_1\frac{\lambda}{\text{NA}} .
$$

$k_1$ captures everything clever in the process (illumination shapes, phase-shift masks, resist); ASML gives $k_1$ = 0.25 as its physical limit ([R-084](../../../reference/research-log.md#r-084--optical-interconnect-standards-fiber-euv-and-co-packaged-optics)). The industry's history is pushing each term: shorter wavelength (436 → 365 → 248 → 193 → 13.5 nm), higher NA (including immersion in water, which raises $n$), and lower $k_1$. EUV's jump from 193 nm to 13.5 nm light, and High-NA EUV's from NA 0.33 to 0.55, are the latest steps (Example 04-09.5, Figure 2). The price of high NA is depth of focus, which shrinks as $\lambda/\text{NA}^2$: High-NA scanners need flatter wafers and thinner resists.

![Left: diffraction patterns of a slit (first zero at sine theta equals lambda over a) and of a circular aperture (first zero at 1.22 lambda over D). Right: critical dimension against numerical aperture on a log scale for 193 nm and 13.5 nm light at k1 of 0.25 and 0.32, with ASML's EUV points at 13 nm for NA 0.33 and 8 nm for NA 0.55.](../../../assets/figures/04-09/diffraction-and-lithography.svg)

*Figure 2. Diffraction sets resolution. Only a much shorter wavelength could take printed features from tens of nanometers to below 10 nm.*

### 3.5 Reflection and refraction

Light in a material of refractive index $n$ travels at $c/n$ ([04-08](04-08-maxwell-preview.md): $n = \sqrt{\varepsilon_r}$ at optical frequencies). At a boundary, part reflects and part transmits.

**Reflection:** the angle of reflection equals the angle of incidence.

**Refraction: Snell's law.** A wavefront crossing a boundary at an angle must stay continuous along the boundary: its crests must match on both sides. Along the surface, crests are spaced $\lambda_1/\sin\theta_1$ on one side and $\lambda_2/\sin\theta_2$ on the other. Setting them equal with $\lambda = \lambda_0/n$:

$$
n_1\sin\theta_1 = n_2\sin\theta_2 .
$$

Light entering a denser medium bends toward the normal (Figure 3). Lenses use this to focus; prisms use the slight dependence of $n$ on wavelength (**dispersion**) to separate colors.

**How much reflects.** At normal incidence, the field-matching result of 04-08 Problem 6 with wave impedance $\eta\propto1/n$ gives an intensity reflectance

$$
R = \Big(\frac{n_1 - n_2}{n_1 + n_2}\Big)^2 .
$$

Glass ($n$ = 1.5) reflects 4% per surface; silicon (about 3.5 in the infrared) reflects about 31%, a major loss at every silicon-photonics interface unless coated.

**Total internal reflection.** Going from high to low index, the refracted angle exceeds the incident one; at the **critical angle** $\sin\theta_c = n_2/n_1$ it reaches 90°, and beyond it no light transmits at all: 100% reflects. Diamonds sparkle because of it; optical fibers work because of it.

**Optical fiber.** A fiber has a glass **core** of index $n_1$ surrounded by a **cladding** of slightly lower index $n_2$. Light travelling at a shallow angle to the axis meets the core boundary beyond the critical angle and is trapped, bouncing (or, more precisely, guided as a wave) for kilometers. Light enters only within an acceptance cone whose half-angle θ in air satisfies

$$
\text{NA} = \sin\theta_{\text{acc}} = \sqrt{n_1^2 - n_2^2} ,
$$

derived by applying Snell's law at the fiber's end face and the critical-angle condition at the core boundary (Problem 04-09.11). **Multimode** fiber has a large core (tens of micrometers) that carries many paths of different lengths, which smears fast pulses; **single-mode** fiber has a core of about 9 µm that carries one guided mode, for long reach.

**Loss and dispersion in fiber.** Silica fiber is astonishingly transparent near 1310 nm (the O-band) and 1550 nm (the C-band): international standards allow at most 0.40 dB/km in cable from 1310 to 1625 nm and 0.30 dB/km in the C-band ([R-084](../../../reference/research-log.md#r-084--optical-interconnect-standards-fiber-euv-and-co-packaged-optics)). Because $n$ depends on wavelength, a pulse containing a spread of wavelengths spreads in time: **chromatic dispersion** $D$, about 17 ps per nm of spectral width per km at 1550 nm in standard fiber, near zero at 1310 nm. Loss limits how much light arrives; dispersion limits how fast it can be modulated (Example 04-09.7).

![Left: rays refracting from air into glass, bending toward the normal, with weak reflected rays dotted. Right: an optical fiber with a core of higher index than its cladding, a ray zigzagging along the core by total internal reflection, entering within an acceptance cone.](../../../assets/figures/04-09/refraction-and-fiber.svg)

*Figure 3. Refraction at a single surface, and the total internal reflection that guides light in a fiber.*

### 3.6 Polarization

Electromagnetic waves are **transverse**: E oscillates perpendicular to the direction of travel, and the direction it oscillates in is the wave's **polarization**. Light from a lamp is unpolarized (a random mixture); a polarizing filter passes only the component of E along its axis. Since intensity goes as $E^2$, a polarizer at angle θ to linearly polarized light transmits

$$
I = I_0\cos^2\theta \qquad\text{(Malus's law)},
$$

and an ideal polarizer passes half of unpolarized light. Liquid-crystal displays work by rotating polarization between two crossed polarizers; polarization also matters for antennas (a horizontally polarized antenna barely receives a vertical wave) and in fiber optics, where random polarization changes must be handled by coherent receivers.

**Brewster's angle.** At $\tan\theta_B = n_2/n_1$, light polarized in the plane of incidence is not reflected at all; reflected glare is therefore mostly polarized parallel to the surface, which is why polarized sunglasses cut it. Laser windows are tilted at Brewster's angle for lossless transmission.

### 3.7 The spectrum and optical interconnect

All electromagnetic waves are one phenomenon spanning many decades: radio (meters to kilometers), microwaves and millimeter waves (centimeters to millimeters; Wi-Fi, 5G, radar), infrared (micrometers; fiber optics at 0.85, 1.31 and 1.55 µm), visible light (0.4–0.7 µm), ultraviolet (lithography at 193 nm), extreme ultraviolet (13.5 nm) and X-rays. What changes across the spectrum is how waves interact with matter, which depends on photon energy (04-10): at 13.5 nm each photon carries about 92 eV, enough to require all-reflective optics in vacuum.

In datacenters, the reach of copper at hundreds of gigabits per second is a meter or two (04-08's losses), so links of more than a few meters are optical. IEEE 802.3 standards define them by wavelength, fiber and reach: for 400 Gb/s Ethernet, eight 850 nm lanes over 100 m of multimode fiber (400GBASE-SR8), four 1310 nm lanes over 500 m of parallel single-mode fiber (DR4), or four wavelengths from 1271 to 1331 nm on one fiber for 2 km (FR4), with 800 Gb/s and 1.6 Tb/s versions following ([R-084](../../../reference/research-log.md#r-084--optical-interconnect-standards-fiber-euv-and-co-packaged-optics)). The newest step, **co-packaged optics**, moves the optical engines next to the switch chip to shorten the electrical path.

## 4. Worked examples

### Example 04-09.1 — Wavelengths and a vibrating string (tier A)

**Setup.** (a) Find the wavelength of a 1 GHz radio wave in air and of a 1 kHz sound wave in air at 20 °C ($v = \sqrt{\gamma RT/M}$ with γ = 1.4, $R$ = 8.314 J/(mol·K), $M$ = 0.02897 kg/mol). (b) A steel string with µ = 0.5 g/m under 60 N tension is 0.65 m long, fixed at both ends. Find the wave speed and the fundamental and third-mode frequencies.

**Solution.** (a) \$\lambda = c/f = \$ **0.2998 m**. The speed of sound is $\sqrt{1.4\times8.314\times293.15/0.02897} = 343.2$ m/s, so \$\lambda = \$ **0.3432 m**: similar wavelengths, a million times different frequencies.

(b) $v = \sqrt{F_T/\mu} = \sqrt{60/5\times10^{-4}} = $ **346.4 m/s**. $f_1 = v/(2L) = $ **266.5 Hz**; $f_3 = 3f_1 = $ **799.4 Hz**.

**Units check.** $\sqrt{\text{N}/(\text{kg/m})} = \sqrt{\text{kg·m/s}^2\cdot\text{m/kg}}$ = m/s ✓.

### Example 04-09.2 — Fringes and a steerable beam (tier B)

**Setup.** (a) Red light at 633 nm passes through two slits 0.2 mm apart. Find the fringe spacing on a screen 1 m away. (b) A row of antennas spaced half a wavelength apart is fed with a phase step of 45° between neighbors. In which direction does the beam point? (c) What phase step steers it to 30°?

**Solution.** (a) $\Delta y = \lambda L/d = 633\times10^{-9}\times1/0.2\times10^{-3} = $ **3.165 mm** (Figure 1).

(b) With $d = \lambda/2$, $kd = \pi$, so $\sin\theta = \Delta\varphi/\pi = (\pi/4)/\pi = 0.25$, and θ = **14.48°** from broadside.

(c) $\Delta\varphi = \pi\sin30° = \pi/2$, a **90°** phase step.

**Interpretation.** Electronic beam steering is phase control: a 5G array updates its phase shifters in microseconds to track a user, which a mechanical dish could never do.

### Example 04-09.3 — An anti-reflection coating (tier B)

**Setup.** (a) Find the reflectance of bare glass ($n$ = 1.5) at normal incidence. (b) Find the ideal coating index and its quarter-wave thickness at 550 nm. (c) Practical coatings use MgF₂ ($n$ = 1.38). Find its quarter-wave thickness and the reflectance at 550 nm, using the quarter-wave result $R = \big(\frac{n_0n_s - n_c^2}{n_0n_s + n_c^2}\big)^2$.

**Solution.** (a) $((1 - 1.5)/(1 + 1.5))^2 = $ **4%**.

(b) $n_c = \sqrt{1.5} = $ **1.225**, thickness $\lambda/(4n_c) = $ **112.3 nm**.

(c) Thickness $550/(4\times1.38) = $ **99.64 nm**; $R = \big(\frac{1.5 - 1.904}{1.5 + 1.904}\big)^2 = $ **1.411%**.

**Interpretation.** One layer cuts reflection from 4% to 1.4% at the design wavelength (less effectively elsewhere); multilayer stacks reach well under 0.5% across the visible. The quarter-wave formula is the optical twin of the quarter-wave impedance transformer of RF engineering: a quarter-wave section of impedance $\sqrt{Z_1Z_2}$ matches $Z_1$ to $Z_2$ ([13-09](../../13-electromagnetics/chapters/13-09-smith-chart-and-matching.md)).

### Example 04-09.4 — Resonators: a laser cavity and a line stub (tier B)

**Setup.** (a) A semiconductor laser chip 300 µm long with refractive index 3.5 emits near 1310 nm. Find its longitudinal-mode spacing in frequency and in wavelength, and about how many half-wavelengths fit in the cavity. (b) A 50 Ω transmission line with a one-way delay of 0.25 ns is open at its far end. At what frequency does its input look like a short circuit? Confirm in ngspice.

**Solution.** (a) $\Delta f = c/(2nL) = 2.998\times10^8/(2\times3.5\times3\times10^{-4}) = $ **142.8 GHz**; $\Delta\lambda = \lambda^2/(2nL) = $ **0.8172 nm**; $2nL/\lambda = $ **1603** half-wavelengths. (These use the phase index, 3.5; real laser materials have a somewhat larger group index, which narrows the spacing in proportion.)

(b) The input looks shorted when the line is a quarter-wavelength long: the wave travels to the open end and back (half a period) and returns inverted. The delay is a quarter period at $f = 1/(4\times0.25\ \text{ns}) = $ **1.000 GHz**.

**Simulation.** The netlist [labs/04-09-lab/quarter_wave_stub.cir](../labs/04-09-lab/quarter_wave_stub.cir) sweeps the input impedance from 0.5 to 1.5 GHz and finds its minimum at 1.000 GHz.

### Example 04-09.5 — Resolution limits in lithography (tier C)

**Setup.** ASML's EUV systems use 13.5 nm light; its 0.33-NA platform prints 13 nm critical dimensions and its 0.55-NA (High-NA) platform 8 nm ([R-084](../../../reference/research-log.md#r-084--optical-interconnect-standards-fiber-euv-and-co-packaged-optics)). (a) Find the $k_1$ each implies. (b) Find each platform's CD at the $k_1$ = 0.25 limit. (c) What NA would 193 nm light need to print 13 nm at the same $k_1$ as the 0.33-NA EUV system? (d) Find the energy of a 13.5 nm photon, $E = hc/\lambda$ (previewing 04-10).

**Solution.** (a) $k_1 = CD\cdot\text{NA}/\lambda$: \$13\times0.33/13.5 = \$ **0.3178** and \$8\times0.55/13.5 = \$ **0.3259**.

(b) $0.25\times13.5/\text{NA}$: **10.23 nm** and **6.136 nm**.

(c) \$\text{NA} = 193\times0.33/13.5 = \$ **4.718**. Since NA = $n\sin\theta$ cannot exceed the index of the medium touching the wafer (about 1.44 for water at 193 nm), this is impossible: hence multiple patterning at 193 nm and the move to EUV.

(d) $E = hc/\lambda = 6.626\times10^{-34}\times2.998\times10^8/13.5\times10^{-9}$ J = **91.84 eV**.

**Interpretation.** ASML's "1.7× smaller, 2.9× denser" for High-NA is the NA ratio (0.55/0.33 = 1.67, rounded to 1.7) and the square of that rounded figure (1.7² ≈ 2.9; the unrounded square is 2.78). The physics is entirely $\lambda/\text{NA}$.

### Example 04-09.6 — Refraction, reflection and a fiber's acceptance (tier B)

**Setup.** (a) A fiber has core index 1.468 and cladding 1.463 (illustrative values). Find its NA, its acceptance half-angle in air and the critical angle at the core boundary. (b) Find the normal-incidence reflectance from air into glass (1.5) and into silicon (3.48).

**Solution.** (a) $\text{NA} = \sqrt{1.468^2 - 1.463^2} = $ **0.1211**; acceptance half-angle $\arcsin(0.1211) = $ **6.953°**; critical angle $\arcsin(1.463/1.468) = $ **85.27°** from the normal, so only rays within about 5° of the axis are guided.

(b) Glass: **4%**. Silicon: $((3.48 - 1)/(3.48 + 1))^2 = $ **30.64%**.

**Interpretation.** The tiny index difference (0.3%) gives a small NA, which is why coupling light into single-mode fiber needs micrometer alignment, a major cost in optical modules.

### Example 04-09.7 — A fiber-link budget (tier C)

**Setup.** Using ITU-T link-planning values ([R-084](../../../reference/research-log.md#r-084--optical-interconnect-standards-fiber-euv-and-co-packaged-optics)): (a) Find the fiber loss of a 2 km O-band link at 0.5 dB/km and of an 80 km C-band link at 0.275 dB/km. (b) Over the 80 km link, a source with 0.1 nm spectral width sees dispersion of 17 ps/(nm·km). Find the pulse spreading and compare it with the bit period at 25 Gb/s.

**Solution.** (a) **1 dB** for 2 km; **22 dB** for 80 km.

(b) $\Delta t = DL\Delta\lambda = 17\times80\times0.1 = $ **136 ps**, against a bit period of **40 ps**: each bit smears over more than three neighbors.

**Interpretation.** Short datacenter links at 1310 nm are loss- and cost-limited, not dispersion-limited (dispersion is near zero there); long-haul C-band links must compensate dispersion, which modern coherent receivers do digitally.

### Example 04-09.8 — Polarizers and glare (tier A)

**Setup.** (a) Unpolarized light passes through three ideal polarizers at 0°, 45° and 90°. What fraction emerges? (b) Without the middle one? (c) Find Brewster's angle for glass ($n$ = 1.5).

**Solution.** (a) The first passes ½; each subsequent passes $\cos^245° = \tfrac12$: total **0.125**.

(b) Crossed polarizers: $\tfrac12\cos^290° = $ **0**. Inserting a polarizer *between* them lets light through, a striking demonstration that polarizers project rather than merely block.

(c) $\arctan1.5 = $ **56.31°**.

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 04-09.1a | wavelength of 1 GHz in air | 0.2998 | m |
| Ex 04-09.1b | wavelength of 1 kHz sound | 0.3432 | m |
| Ex 04-09.1c | wave speed on the string | 346.4 | m/s |
| Ex 04-09.1d | fundamental frequency | 266.5 | Hz |
| Ex 04-09.1e | third-mode frequency | 799.4 | Hz |
| Ex 04-09.2a | fringe spacing | 3.165 | mm |
| Ex 04-09.2b | beam direction for a 45° step | 14.48 | ° |
| Ex 04-09.2c | phase step for 30° | 90 | ° |
| Ex 04-09.3a | bare-glass reflectance | 4 | % |
| Ex 04-09.3b | ideal coating index | 1.225 | — |
| Ex 04-09.3c | ideal quarter-wave thickness | 112.3 | nm |
| Ex 04-09.3d | MgF₂ quarter-wave thickness | 99.64 | nm |
| Ex 04-09.3e | reflectance with MgF₂ | 1.411 | % |
| Ex 04-09.4a | laser mode spacing | 142.8 | GHz |
| Ex 04-09.4b | laser mode spacing | 0.8172 | nm |
| Ex 04-09.4c | half-wavelengths in the cavity | 1603 | — |
| Ex 04-09.4e | quarter-wave frequency of the stub | 1.000 | GHz |
| Ex 04-09.5a | k₁ at NA 0.33 | 0.3178 | — |
| Ex 04-09.5b | k₁ at NA 0.55 | 0.3259 | — |
| Ex 04-09.5c | CD at k₁ = 0.25, NA 0.33 | 10.23 | nm |
| Ex 04-09.5d | CD at k₁ = 0.25, NA 0.55 | 6.136 | nm |
| Ex 04-09.5e | NA needed at 193 nm | 4.718 | — |
| Ex 04-09.5f | 13.5 nm photon energy | 91.84 | eV |
| Ex 04-09.6a | fiber NA | 0.1211 | — |
| Ex 04-09.6b | acceptance half-angle | 6.953 | ° |
| Ex 04-09.6c | critical angle | 85.27 | ° |
| Ex 04-09.6d | reflectance into glass | 4 | % |
| Ex 04-09.6e | reflectance into silicon | 30.64 | % |
| Ex 04-09.7a | loss of 2 km O-band | 1 | dB |
| Ex 04-09.7b | loss of 80 km C-band | 22 | dB |
| Ex 04-09.7c | dispersion spreading | 136 | ps |
| Ex 04-09.7d | bit period at 25 Gb/s | 40 | ps |
| Ex 04-09.8a | three polarizers | 0.125 | — |
| Ex 04-09.8b | crossed polarizers | 0 | — |
| Ex 04-09.8c | Brewster's angle for glass | 56.31 | ° |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| T 04-09.a | speed of sound in air at 20 °C | 343.2 | m/s |
| T 04-09.b | Airy first-zero factor | 1.220 | — |

## 5. Simulate it

The lab ([labs/04-09-lab/](../labs/04-09-lab/README.md)) is a notebook plus an ngspice netlist:

1. **Superposition:** beats and standing waves built from travelling waves.
2. **Phased arrays:** the array factor of an 8-element antenna, beam steering and grating lobes. *Predict first:* what happens when the elements are spaced a full wavelength apart?
3. **Diffraction by brute force:** sum Huygens wavelets across a slit and a circular aperture and compare with the closed forms.
4. **Thin films:** reflectance against wavelength for a single-layer coating, computed with the characteristic-matrix method.
5. **Fiber:** acceptance angle and dispersion broadening.

The netlist `quarter_wave_stub.cir` simulates the stub of Example 04-09.4.

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Lithography wavelength (193 nm → 13.5 nm) | Resolution | Source power, all-reflective vacuum optics, mask and resist challenges, tool cost | Fab and process-technology leadership |
| Numerical aperture | Resolution ∝ 1/NA | Depth of focus ∝ 1/NA², field size (High-NA halves it), lens cost | Lithography and integration engineers |
| Fiber type (multimode vs single-mode) | Multimode: cheap, easy alignment at 850 nm | Reach (modal dispersion) | Datacenter network architects |
| Optical wavelength (850 / 1310 / 1550 nm) | 1310: low dispersion; 1550: lowest loss | Laser and detector cost and technology | Optical-module designers |
| Antenna-array element spacing | Fewer elements for a given aperture (wider spacing) | Grating lobes beyond λ/2 | RF and antenna engineers |
| Coating layers | Lower reflection over wider bandwidth | Cost, process steps | Optics designers |

## 7. Numbers to know

| Quantity | Value | Note |
|---|---|---|
| Wave speed | $v = \lambda f$; string $\sqrt{F_T/\mu}$; sound in air ≈ 343 m/s; light $c/n$ | |
| Two-slit fringe spacing | λL/d | |
| Diffraction | slit $\lambda/a$; circular aperture $1.22\lambda/D$ | Rayleigh criterion |
| Lithography resolution | $CD = k_1\lambda/\text{NA}$, $k_1 \ge 0.25$ | [R-084](../../../reference/research-log.md#r-084--optical-interconnect-standards-fiber-euv-and-co-packaged-optics) |
| EUV, as of Nov 2026 | 13.5 nm; NA 0.33 → 13 nm CD; NA 0.55 → 8 nm | ASML [R-084](../../../reference/research-log.md#r-084--optical-interconnect-standards-fiber-euv-and-co-packaged-optics) |
| Normal-incidence reflectance | glass 4%; silicon ≈ 31% | $((n_1 - n_2)/(n_1 + n_2))^2$ |
| Fiber NA | $\sqrt{n_1^2 - n_2^2}$, about 0.1 for single-mode | |
| Fiber loss limits (G.652.D cable) | ≤ 0.40 dB/km (1310–1625 nm); ≤ 0.30 dB/km (C-band) | [R-084](../../../reference/research-log.md#r-084--optical-interconnect-standards-fiber-euv-and-co-packaged-optics) |
| Dispersion, standard fiber | ≈ 17 ps/(nm·km) at 1550 nm; near 0 at 1310 nm | |
| 400G Ethernet optics | SR8: 850 nm, 100 m MMF; DR4: 1310 nm, 500 m; FR4: 4 λ, 2 km | IEEE 802.3 |

## 8. Common mistakes

1. **Confusing wave speed with the medium's motion.** The rope moves up and down; the pattern travels.
2. **Forgetting the wavelength changes in a medium.** Frequency stays the same across a boundary; wavelength becomes λ₀/n.
3. **Measuring angles from the surface.** Snell's law and reflection use angles from the normal.
4. **Expecting destructive interference to destroy energy.** It redistributes energy to the bright regions.
5. **Applying the Rayleigh formula with the wrong NA.** NA includes the medium's index; for immersion lithography it exceeds 1.
6. **Ignoring the phase flip on reflection.** Reflection from a higher-index medium inverts the wave, which shifts thin-film fringe conditions.
7. **Spacing array antennas too far apart.** Beyond λ/2 the array forms grating lobes in unwanted directions.
8. **Treating fiber loss and dispersion as the same problem.** Loss weakens the signal; dispersion smears it in time. They have different fixes.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **EUV and High-NA lithography.** ASML's EUV scanners use 13.5 nm light; the 0.33-NA NXE platform (first shipped 2010) prints 13 nm critical dimensions, and the 0.55-NA EXE platform prints 8 nm, which ASML equates to 1.7× smaller features and 2.9× higher density, with an exposure field half the size. ASML lists the EXE:5200B at 8 nm resolution and at least 175 wafers per hour at a 50 mJ/cm² dose; the first High-NA modules shipped to Intel in December 2023 ([R-084](../../../reference/research-log.md#r-084--optical-interconnect-standards-fiber-euv-and-co-packaged-optics)) **[Established for λ, NA and specifications; Industry estimate for the density framing]**.
- **Datacenter optics standards.** IEEE 802.3 defines 400 Gb/s Ethernet optics including SR8 (eight 850 nm lanes, 100 m of OM4 multimode fiber; 802.3cm-2020), DR4 (four 1310 nm lanes, 500 m of parallel single-mode fiber; 802.3bs-2017) and FR4 (four wavelengths at 1271–1331 nm on one fiber, 2 km; 802.3cu-2021). IEEE 802.3df-2024 set 800 Gb/s objectives to 500 m and 2 km over eight single-mode pairs, and the P802.3dj project targets 200 Gb/s lanes for 800 Gb/s and 1.6 Tb/s ([R-084](../../../reference/research-log.md#r-084--optical-interconnect-standards-fiber-euv-and-co-packaged-optics)) **[Established; P802.3dj completion not verified]**.
- **Co-packaged optics.** NVIDIA announced Spectrum-X and Quantum-X Photonics switches with co-packaged optics in March 2025, claiming 3.5× better power efficiency (a later blog cites about 30 W per pluggable interface against as low as 9 W), with availability planned for 2026; general availability had not been confirmed from a primary source when this was checked in Nov 2026. Broadcom announced its 102.4 Tb/s Tomahawk 6 – Davisson CPO switch in October 2025, claiming a 70% cut in optical-interconnect power ([R-084](../../../reference/research-log.md#r-084--optical-interconnect-standards-fiber-euv-and-co-packaged-optics)) **[Industry estimate: vendor claims]**.

### Why it matters commercially

Optics is where two of the industry's largest capital flows meet this chapter's physics. Lithography, the most expensive step in chipmaking, is a diffraction problem whose solution (EUV, High-NA) is supplied by essentially one company. And AI clusters are increasingly limited by interconnect power and reach, pushing optical links ever closer to the chips: transceivers, lasers, silicon photonics and co-packaged optics are among the fastest-moving markets in semiconductors. Understanding $\lambda/\text{NA}$, fiber loss and dispersion lets you test whether a roadmap's claims are physics or marketing.

> **Deeper:** see companion repo *Semiconductor Capital Equipment* for lithography economics, and *Datacenter Networking* for optical-interconnect architecture.

### Marketing vs Reality

- **"63× better signal integrity" (NVIDIA press release) versus "64×" in the same company's later blog.** *Reality:* the headline ratios are not measurements anyone can reproduce; the physical basis is shortening the electrical path between switch chip and optics. Ask for watts per port and link margin.
- **"70% lower power, more than 3.5× lower" (Broadcom).** *Reality:* a 70% cut is a 3.33× reduction; "more than 3.5×" implies at least 71.4%. Small, but a sign to check vendor arithmetic. The same release says the part is "now shipping" and "currently sampling".
- **"High-NA gives 2.9× density."** *Reality:* in the printed layer, at best; chip density also depends on design rules, other layers and cost per wafer, and High-NA halves the exposure field. Ask for cost per wafer and per transistor.
- **"Our transceiver reaches 2 km."** *Reality:* under which standard and fiber, with what margin at end of life and temperature? Ask for the link budget.

### Questions for engineering leaders

1. **"What is your optical link's power per bit, and what share is laser, modulator, DSP and electrical channel?"** *Strong:* pJ/bit by component with measured numbers. *Evasive:* only a ratio versus a competitor.
2. **"Which IEEE 802.3 physical-layer standards do your modules meet, and with what margin?"** *Strong:* standard names, reach and measured margins (TDECQ, receiver sensitivity). *Evasive:* "industry standard".
3. **"How does your lithography plan trade multiple patterning at 0.33 NA against High-NA single exposure?"** *Strong:* cost per layer, overlay, defectivity and throughput comparisons. *Evasive:* "we will adopt High-NA when it's ready".
4. **"How do you handle fiber coupling and alignment in volume?"** *Strong:* coupling loss, tolerance and yield data. *Evasive:* lab demonstration only.

## 10. Concept check

1. A wave travels from air into glass. What happens to its frequency, speed and wavelength?

   <details><summary>Answer</summary>

   Frequency is unchanged (set by the source; the boundary must oscillate in step on both sides). Speed falls to $c/n$, and wavelength to $\lambda_0/n$.

   </details>

2. Two equal waves interfere destructively at a point. Where did the energy go?

   <details><summary>Answer</summary>

   To the points of constructive interference, where intensity reaches four times one wave's; averaged over space the intensity is the sum of the two.

   </details>

3. Why can a 5G phone's antenna array steer its beam without moving?

   <details><summary>Answer</summary>

   By setting the phase of each element: the beam forms in the direction where the path differences compensate the applied phase steps ($\sin\theta = \Delta\varphi/kd$).

   </details>

4. Why did lithography move from 193 nm to 13.5 nm light rather than just increasing NA?

   <details><summary>Answer</summary>

   $CD = k_1\lambda/\text{NA}$ with NA limited by the index of the medium at the wafer (water's is about 1.44 at 193 nm) and $k_1$ limited to 0.25. At 193 nm the floor is tens of nanometers per exposure; only a shorter wavelength (or costly multiple patterning) goes smaller.

   </details>

5. Why does light stay inside an optical fiber?

   <details><summary>Answer</summary>

   The core's index is higher than the cladding's, so rays striking the boundary beyond the critical angle are totally internally reflected; only rays entering within the acceptance cone (set by the NA) are guided.

   </details>

6. A quarter-wave coating cancels reflection at one wavelength. Why is it less effective at others?

   <details><summary>Answer</summary>

   The layer is a quarter-wave only at the design wavelength; at other wavelengths the round-trip phase is not exactly half a cycle, so the two reflections no longer cancel. Multilayer coatings broaden the band.

   </details>

7. Why are short datacenter links often at 1310 nm and long-haul links at 1550 nm?

   <details><summary>Answer</summary>

   Standard fiber has nearly zero chromatic dispersion near 1310 nm, so short, fast links need no dispersion compensation; loss is lowest near 1550 nm, which matters most over tens to thousands of kilometers, where amplifiers and dispersion compensation are used.

   </details>

Problem set: [04-09 problems](../problems/04-09-problems.md) · [solutions](../solutions/04-09-solutions.md).

## 11. Key terms

[Wave equation](../../../reference/glossary.md#wave-equation) ·
[Wavelength](../../../reference/glossary.md#wavelength) ·
[Interference](../../../reference/glossary.md#interference) ·
[Phased array](../../../reference/glossary.md#phased-array) ·
[Standing wave](../../../reference/glossary.md#standing-wave) ·
[Resonance](../../../reference/glossary.md#resonance) ·
[Diffraction](../../../reference/glossary.md#diffraction) ·
[Rayleigh criterion](../../../reference/glossary.md#rayleigh-criterion) ·
[Numerical aperture](../../../reference/glossary.md#numerical-aperture) ·
[Snell's law](../../../reference/glossary.md#snells-law) ·
[Total internal reflection](../../../reference/glossary.md#total-internal-reflection) ·
[Optical fiber](../../../reference/glossary.md#optical-fiber) ·
[Chromatic dispersion](../../../reference/glossary.md#chromatic-dispersion) ·
[Polarization (light)](../../../reference/glossary.md#polarization-light) ·
[Co-packaged optics](../../../reference/glossary.md#co-packaged-optics)

## 12. Connections

- **Previous:** [04-08](04-08-maxwell-preview.md) (electromagnetic waves, impedance and reflection), [04-01](04-01-mechanics-essentials.md) (oscillators and resonance), [02-01](../../02-complex-numbers-des-and-linear-algebra/chapters/02-01-complex-numbers-euler-and-phasors.md) (phasors for adding waves).
- **Next:** [04-10 Introduction to Quantum Mechanics](04-10-intro-quantum-mechanics.md): light also comes in particles (photons), and electrons also behave as waves.
- **Used in:** [13](../../13-electromagnetics/README.md) (waves, reflection, matching, antennas), [21](../../21-rf-and-microwave-engineering/README.md) (antenna arrays), [24-07](../../24-high-speed-io-signal-integrity-and-photonics/chapters/24-07-photonics-fundamentals.md) to [24-09](../../24-high-speed-io-signal-integrity-and-photonics/chapters/24-09-lpo-and-cpo.md) (photonics, silicon photonics, co-packaged optics), [25-02](../../25-fabrication-packaging-test-and-reliability/chapters/25-02-lithography.md) (lithography).

## 13. Further study

- Halliday, D., Resnick, R. and Walker, J., *Fundamentals of Physics*, the chapters on waves, interference, diffraction and refraction.
- Hecht, E., *Optics*, 5th ed., Pearson, 2017, for a complete undergraduate optics course.
- MIT OpenCourseWare 8.03 (Physics III: Vibrations and Waves).
- ASML, "The Rayleigh criterion for resolution" (Technology pages), for lithography resolution in the vendor's own terms.

## 14. Sources

1. Halliday, D., Resnick, R. and Walker, J., *Fundamentals of Physics*, Wiley (any recent edition).
2. Hecht, E., *Optics*, 5th ed., Pearson, 2017.
3. NIST, 2022 CODATA recommended values (exact $h$, $c$, $e$). [R-073]
4. ASML, "5 things you should know about High NA EUV lithography" (25 January 2024); "The Rayleigh criterion for resolution"; TWINSCAN NXE:3800E, EXE:5000 and EXE:5200B product pages (accessed November 2026). [R-084]
5. ITU-T Recommendation G.652 (08/2024), *Characteristics of a single-mode optical fibre and cable*. [R-084]
6. IEEE 802.3 task forces bs, cu, cm, df and dj: baseline and objectives documents (2015–2024). [R-084]
7. NVIDIA press release (18 March 2025) and technical blog (18 August 2025); Broadcom press release (8 October 2025). [R-084]
