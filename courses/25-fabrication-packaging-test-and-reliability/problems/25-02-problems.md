# Problems 25-02 · Lithography: DUV, Multipatterning, EUV and High-NA

Chapter: [25-02](../chapters/25-02-lithography.md) · Worked solutions: [25-02 solutions](../solutions/25-02-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.**

- Wavelengths are vacuum values: 248 nm (KrF), 193 nm (ArF), 13.5 nm (EUV); $hc$ = 1239.84 eV·nm and 1 eV = 1.6022 × 10⁻¹⁹ J.
- Pupil coordinates $s = n\sin\theta$; orders sit at $s_0 + m\lambda/p$ and pass if $|s| \le \text{NA}$.
- Depth of focus is twice the quarter-wave defocus limit of §3.3.
- Cost per pass is depreciation only, five years straight-line at 80% availability, as in Example 25-02.7.
- "Assumed" values are illustrative.
- Problems marked *(lab)* can be checked with `labs/25-02-lab/litho.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 25-02.1 [A]

**A KrF scanner.** A dry 248 nm scanner has NA = 0.80 (assumed). Find its minimum pitch with (a) on-axis and (b) ideal off-axis illumination, and (c) the half-pitch in (b).

### Problem 25-02.2 [A]

**A higher-index fluid.** A hypothetical immersion fluid has $n$ = 1.65 at 193 nm (assumed). With the same steepest angle in the fluid as Example 25-02.3 ($\sin\theta$ = 0.94, and a lens glass of higher index), find (a) the NA and (b) the half-pitch at $k_1$ = 0.25.

### Problem 25-02.3 [B]

**An EUV grating.** *(lab)* A 0.33-NA EUV scanner prints a 24 nm pitch with dipole illumination. (a) Where must the dipole sit for symmetric two-beam imaging, and does it fit? (b) What is the minimum pitch with ideal off-axis illumination, and (c) with on-axis illumination?

### Problem 25-02.4 [B]

**Immersion's hidden benefit.** Compare the depth of focus of a dry lens and a water-immersion lens ($n$ = 1.44) at the same NA of 0.93. Find (a) the dry DOF, (b) the water DOF and (c) their ratio.

### Problem 25-02.5 [C]

**Two-beam image contrast.** (a) A mask of lines and spaces transmits 1 over a fraction $f$ of each period and 0 elsewhere. Show that its zeroth and first Fourier amplitudes are $a_0 = f$ and $a_1 = \sin(\pi f)/\pi$. (b) Show that the two-beam image of §3.2 has contrast $(I_{max} - I_{min})/(I_{max} + I_{min}) = 2a_0a_1/(a_0^2 + a_1^2)$, whatever the illumination tilt. (c) Evaluate the contrast for $f$ = 0.5 and $f$ = 0.25.

### Problem 25-02.6 [B]

**A 21 nm pitch.** (a) What pitch does SAQP reach from ArF immersion's 76 nm single-exposure pitch? (b) Find the $k_1$ a 21 nm pitch demands of a 0.33-NA EUV exposure and (c) of a 0.55-NA one. Which are plausible single exposures?

### Problem 25-02.7 [B]

**An overlay budget.** LELE prints a 48 nm pitch with 24 nm lines and spaces (assumed). (a) With 2.5 nm of overlay error, what are the alternating spaces and the fractional error? (b) What overlay keeps spaces within ±8%?

### Problem 25-02.8 [B]

**High-NA photons.** *(lab)* High-NA is specified at 50 mJ/cm² [R-561]. Find (a) the EUV photons per nm², (b) the photons on an 8 nm × 8 nm feature, (c) the number absorbed at 20% absorption (assumed) and (d) their relative fluctuation.

### Problem 25-02.9 [C]

**Dose for a noise target.** For the 8 nm × 8 nm feature of Problem 25-02.8 and a resist absorbing 25% (assumed), what dose keeps the absorbed-photon fluctuation at or below 3%?

### Problem 25-02.10 [B]

**Dose costs throughput.** *(lab)* A scanner gives 220 wph at 30 mJ/cm² with 6.0 s of overhead per wafer (assumed); exposure time is proportional to dose. Find (a) the exposure time at 30 mJ/cm², and the throughput at (b) 50 mJ/cm² and (c) 102 mJ/cm² (Problem 25-02.9's dose, rounded).

### Problem 25-02.11 [B]

**Acceptance throughput.** Repeat Example 25-02.7's High-NA cost per pass at the 135 wph reported in acceptance testing [R-565]. How much more is that than at specification?

### Problem 25-02.12 [A]

**A large die.** A 700 mm² die (assumed). (a) Does it fit a Low-NA field, and what fraction of the field does it use? (b) Does it fit a High-NA field?

### Problem 25-02.13 [B]

**Source power and throughput.** (a) Using Problem 25-02.10's model, suppose the scanner's 220 wph is achieved with a 600 W source. What throughput does a 1,000 W source give at the same dose, and by what percentage does it rise? (b) As an illustration, suppose the projected rise from today's 220 wph specification to about 330 wph [R-560], [R-567] came only from the same 67% power increase. What overhead and exposure time would that imply?

### Problem 25-02.14 [B]

**Pitch walk.** SADP uses a 64 nm mandrel pitch, 16 nm spacers and a 16 nm target mandrel width, giving 16 nm lines at 32 nm pitch. (a) If the mandrels print 18 nm wide, what are the two alternating spaces? (b) How does the space difference relate to the mandrel width error? (c) What mandrel width tolerance keeps the space difference within 2 nm?

### Problem 25-02.15 [B]

**Dose and CD.** Near each edge of a clear space the aerial image falls linearly, $I(x) = I_e(1 - x/\ell)$ with $x$ measured outward from the nominal edge, and the resist clears where the dose times $I$ exceeds a threshold $D_0$; at nominal dose $D I_e = D_0$. (a) Show that a fractional dose change $\delta$ moves each edge outward by about $\ell\delta$, where $\ell = I/\lvert dI/dx\rvert$ is the inverse image log slope. (b) For $\ell$ = 10 nm, by how much does a 5% dose increase widen the space, exactly and to first order? (c) What dose latitude (±%) keeps the space within ±1.5 nm to first order?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Diffraction orders and the $k_1$ limit | 1, 2, 3, 5 |
| 2. Depth of focus and immersion | 2, 4, 15 |
| 3. Multipatterning, overlay and pitch walk | 6, 7, 14 |
| 4. Photon shot noise | 8, 9 |
| 5. Throughput, cost per pass and stitching | 10, 11, 12, 13 |
| 6. Reading EUV and High-NA claims | 11, 13 |
