# Problems 04-09 · Waves and Optics Basics

Chapter: [04-09](../chapters/04-09-waves-and-optics.md) · Worked solutions: [04-09 solutions](../solutions/04-09-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** $c = 299\,792\,458$ m/s. Indices are given where needed. Angles are measured from the normal unless stated. Answers to 4 significant figures unless exact.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 04-09.1 [A]

**Wi-Fi.** For a 2.4 GHz wave in air, find the wavelength, the period and the wavenumber.

### Problem 04-09.2 [A]

**Tuning a string.** A string of mass 2 g/m and length 0.5 m (fixed at both ends) is under 100 N tension. (a) Find the wave speed and fundamental frequency. (b) What tension gives a fundamental of 440 Hz?

### Problem 04-09.3 [A]

**Beats.** Two tones of 440 Hz and 443 Hz sound together. What do you hear, and at what rate does the loudness pulse?

### Problem 04-09.4 [B]

**Green fringes.** Light at 532 nm passes through two slits 0.5 mm apart. Find the fringe spacing on a screen 2 m away.

### Problem 04-09.5 [B]

**Grating lobes.** A linear antenna array is steered to 30° from broadside. (a) With element spacing 0.75λ, the array also radiates strongly where $\sin\theta = \sin30° - \lambda/d$. Find that grating-lobe direction. (b) Find the largest spacing (in wavelengths) that avoids any grating lobe when steering to 30°, using the condition $d/\lambda < 1/(1 + |\sin\theta_0|)$.

### Problem 04-09.6 [B]

**A single slit.** Light at 633 nm passes through a slit 10 µm wide. Find the angle of the first minimum and the width of the central bright band on a screen 1 m away.

### Problem 04-09.7 [B]

**A camera's limit.** A lens with a 5 mm aperture images green light (550 nm). Find its Rayleigh angular resolution and the smallest separation it can resolve 100 m away.

### Problem 04-09.8 [C]

**Coating a silicon-photonics facet.** A silicon facet ($n$ = 3.48) at 1550 nm reflects 30.6% (Example 04-09.6). (a) Find the ideal single-layer coating index. (b) Using silicon nitride ($n$ = 1.9), find the quarter-wave thickness and the residual reflectance with the formula of Example 04-09.3.

### Problem 04-09.9 [B]

**Refraction and critical angles.** (a) Light hits glass ($n$ = 1.5) from air at 30°. Find the refraction angle. (b) Find the critical angle for glass to air. (c) Find the critical angle for silicon ($n$ = 3.48) to silicon dioxide ($n$ = 1.444), and explain why silicon waveguides confine light so tightly.

### Problem 04-09.10 [B]

**Multimode fiber.** A fiber has core index 1.48 and cladding index 1.46. Find its NA and acceptance half-angle in air.

### Problem 04-09.11 [C]

**A short-reach link budget.** (a) Derive the fiber NA formula $\sqrt{n_1^2 - n_2^2}$ by applying Snell's law at the end face and the critical-angle condition at the core–cladding boundary. (b) A 2 km O-band link has 0.5 dB/km of fiber loss and two connectors of 0.4 dB each. Find the total loss and the received power for a 0 dBm transmitter.

### Problem 04-09.12 [C]

**Dispersion-limited bit rate.** A 40 km C-band link uses a source with 0.08 nm spectral width in fiber with 17 ps/(nm·km) of dispersion. (a) Find the pulse spreading. (b) If spreading must stay below half a bit period, find the highest bit rate.

### Problem 04-09.13 [A]

**Polarizer stack.** Unpolarized light passes through polarizers at 0°, 30° and 90°. What fraction of the intensity emerges after the second and after the third?

### Problem 04-09.14 [C]

**A coating across the spectrum.** For a single layer of thickness $d$ and index $n_c$ between media $n_0$ and $n_s$, the reflectance is
$R = \dfrac{r_1^2 + r_2^2 + 2r_1r_2\cos2\delta}{1 + r_1^2r_2^2 + 2r_1r_2\cos2\delta}$, with $r_1 = \frac{n_0 - n_c}{n_0 + n_c}$, $r_2 = \frac{n_c - n_s}{n_c + n_s}$ and $\delta = 2\pi n_cd/\lambda$.
(a) Show that at the quarter-wave condition this reduces to the formula of Example 04-09.3. (b) For the MgF₂ coating of Example 04-09.3 (designed for 550 nm), find $R$ at 450 nm and 650 nm.

---

## Objective coverage

| Learning objective (chapter 04-09) | Problems |
|---|---|
| 1. Wave equation and wave parameters | 1, 2 |
| 2. Interference, arrays, thin films, beats, standing waves | 2, 3, 4, 5, 8, 14 |
| 3. Diffraction and resolution | 6, 7 |
| 4. Reflection, refraction, fibers, dispersion | 9, 10, 11, 12 |
| 5. Polarization and the spectrum | 13 |
