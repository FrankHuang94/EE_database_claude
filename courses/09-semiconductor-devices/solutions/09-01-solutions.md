# Solutions 09-01 · Crystals, Energy Bands and the Semiconductor

Problems: [09-01 problems](../problems/09-01-problems.md) · Chapter: [09-01](../chapters/09-01-crystals-and-energy-bands.md). Every number below is recomputed by [verify_09_01.py](../verify/verify_09_01.py): lattice quantities by generating the crystal and counting atoms, planes and angles from vectors, Kronig–Penney bands from the transfer matrix of one period, effective masses from mass tensors and by fitting computed bands, and alloy gaps by root finding.

---

## Solutions

### Solution 09-01.1

(a) Eight atoms per cube: $N = 8/a^3 = 8/(5.658\times10^{-8}\ \text{cm})^3$ = **4.417 × 10²²** cm⁻³.

(b) $r_{nn} = \sqrt3\,a/4 = 1.7321 \times 5.658/4$ = **2.450** Å.

(c) The nearest FCC lattice points to the origin are at $(a/2)(1,1,0)$ and its equivalents, a distance $a/\sqrt2$ = **4.001** Å.

(d) Mass per volume is (atoms per volume) × (mass per atom), so $\rho = NM/N_A$ and

$$
M = \frac{\rho N_A}{N} = \frac{5.3234\ \text{g/cm}^3 \times 6.022141\times10^{23}\ \text{mol}^{-1}}{4.417\times10^{22}\ \text{cm}^{-3}} = 72.58\ \text{g/mol} .
$$

**Units check.** (g/cm³)(mol⁻¹)/(cm⁻³) = g/mol. **Sanity check.** Germanium's atoms are **4.2**% farther apart than silicon's (2.450 against 2.352 Å) and **2.6** times heavier (72.58 against 28.09 g/mol), so germanium is **2.3** times denser (5.3234 against 2.329 g/cm³).

### Solution 09-01.2

Take reciprocals of the intercepts in units of $a$, then clear fractions.

(a) 1, 1, 1 → 1, 1, 1: **(111)**.

(b) ½, ∞, 1 → 2, 0, 1: **(201)**.

(c) −1, 1, ∞ → −1, 1, 0: **(1̄10)**.

(d) 3, 2, 6 → ⅓, ½, ⅙ → multiply by 6: **(231)**.

(e) $d_{231} = a/\sqrt{2^2 + 3^2 + 1^2} = 5.431/\sqrt{14}$ = **1.451** Å.

### Solution 09-01.3

In a cubic crystal the normal to $(hkl)$ is $[hkl]$, so angles between planes are angles between index vectors.

(a) $\cos\theta = (1 + 1 + 0)/(\sqrt2\sqrt3) = 2/\sqrt6 = 0.8165$, so $\theta$ = **35.26°**.

(b) $\cos\theta = (-1 + 1 + 1)/(\sqrt3\sqrt3) = 1/3$, so $\theta$ = **70.53°**.

(c) $[1\bar10]\cdot[111] = 1 - 1 + 0 = 0$: the direction is perpendicular to the plane's normal, so **yes**, it lies in (111).

(d) $\cos\theta = (1 - 1 - 1)/3 = -1/3$, so the bond angle is **109.47°**, the tetrahedral angle.

### Solution 09-01.4

(a) Zinc blende has the same 8 atoms per cube as diamond (4 Ga, 4 As): $N = 8/(5.65325\times10^{-8})^3$ = **4.428 × 10²²** cm⁻³.

(b) The Ga atoms occupy an FCC lattice (cube corners and face centers); the As atoms occupy the same lattice shifted by $(a/4)(1,1,1)$. The Ga atoms therefore have $z$ coordinates 0 and $a/2$, and the As atoms $a/4$ and $3a/4$: the (100) atomic planes, spaced $a/4$ apart, alternate between all-Ga and all-As. Each holds 2 atoms per $a^2$ (4 corners shared by 4 cells plus 1 face center): $\sigma = 2/a^2$ = **6.258 × 10¹⁴** cm⁻².

(c) A (111) plane through the cube cuts an equilateral triangle of side $\sqrt2a$ and area $\sqrt3a^2/2$ containing 2 atoms of one sublattice (3 corners × ⅙ + 3 edge midpoints × ½). So $\sigma = 4/(\sqrt3a^2)$ = **7.226 × 10¹⁴** cm⁻². Because the two sublattices are offset along [111], each (111) atomic plane holds one element only, which makes the two (111) faces of a GaAs crystal chemically different (one Ga-terminated, one As-terminated).

### Solution 09-01.5

(a) The sidewall is vertical (it contains [001]) and runs along the fin (it contains [110]), so its normal is perpendicular to both:

$$
[001] \times [110] = (0\cdot0 - 1\cdot1,\ 1\cdot1 - 0\cdot0,\ 0\cdot1 - 0\cdot1) = (-1, 1, 0) .
$$

The sidewalls are **(1̄10)** planes, members of the {110} family, the orientation that favors holes (chapter §3.2).

(b) $[001] \times [100] = (0, 1, 0)$: **(010)** sidewalls, a {100} plane.

(c) The sidewall angle is the angle between (001) and a {111} plane: $\cos\theta = 1/\sqrt3$, $\theta$ = **54.74°**. Each sidewall meets the surface at the rim and slopes down to the apex at the center, a horizontal run of $W/2$ = 5.00 µm. Depth: $(W/2)\tan\theta = 5.00 \times \sqrt2$ = **7.071** µm (since $\tan\theta = \sqrt2$ exactly when $\cos\theta = 1/\sqrt3$). Sidewall length: $(W/2)/\cos\theta = 5.00 \times \sqrt3$ = **8.660** µm.

**Sanity check.** $7.071^2 + 5.000^2 = 75.0 = 8.660^2$. Because the etch stops on {111} planes, the pit depth is set by the mask opening, not by etch time: a self-limiting process that MEMS makers use to form precise grooves and membranes.

### Solution 09-01.6

(a) $E_d = \hbar^2/(2m_0d^2) = (1.054572\times10^{-34})^2/(2 \times 9.109384\times10^{-31} \times (0.4\times10^{-9})^2)$ J = **3.815 × 10⁻²⁰** J = **0.2381** eV.

(b) Solve $F(x) = 1.5\sin x/x + \cos x = 1$ on $0 < x < \pi$ (Newton or bisection): $x_b$ = **1.5427**. Bottom: $0.2381 \times 1.5427^2$ = **0.5667** eV. Top ($x = \pi$, where $F = -1$ for any $P$): $0.2381\pi^2$ = **2.350** eV. Width: **1.783** eV.

(c) Above $x = \pi$, $F < -1$ until $x_2$ = **3.8795**: band 2 starts at $0.2381 \times 3.8795^2$ = **3.584** eV, and the gap is $3.584 - 2.350$ = **1.234** eV wide.

(d) $F'(x) = P(x\cos x - \sin x)/x^2 - \sin x$ gives $F'(x_b)$ = **−1.6023**, so $m^*/m_0 = -F'(x_b)/x_b = 1.6023/1.5427$ = **1.039**.

(e) Compare in units of $E_d$, since the two lattices have different periods. Band 1 spans $\pi^2 - x_b^2$ = **7.490** $E_d$ here against **5.963** $E_d$ for $P$ = 3; the first gap spans $x_2^2 - \pi^2$ = **5.181** $E_d$ against **9.046** $E_d$; the band-bottom mass is 1.039 $m_0$ against 1.125 $m_0$. Weaker barriers reflect less, so the wave is closer to a free electron: wider bands, narrower gaps and a mass closer to $m_0$.

### Solution 09-01.7

(a) For large $P$ the band bottom approaches $\pi$. Write $x = \pi - \epsilon$. Then $\sin x = \sin\epsilon \approx \epsilon$ and $\cos x \approx -1$, so

$$
F \approx \frac{P\epsilon}{\pi} - 1 = 1 \quad\Longrightarrow\quad \epsilon \approx \frac{2\pi}{P}, \qquad x_b \approx \pi\left(1 - \frac{2}{P}\right).
$$

The band runs from $x_b$ to $\pi$, so its width is

$$
E_d\left(\pi^2 - x_b^2\right) = E_d\,\epsilon\,(2\pi - \epsilon) \approx E_d \cdot \frac{2\pi}{P} \cdot 2\pi = \frac{4\pi^2E_d}{P},
$$

dropping the $\epsilon^2$ term.

(b) Numerically, for $P$ = 20: $x_b$ = **2.8577** (approximation 2.8274), width **1.7029** $E_d$ against the approximation $4\pi^2/20$ = **1.9739** $E_d$, an error of **15.9**%. For $P$ = 50: $x_b$ = **3.0209** (approximation 3.0159), width **0.7437** $E_d$ against **0.7896** $E_d$, an error of **6.2**%. The error falls roughly as $1/P$, because the neglected terms are a factor $\epsilon \propto 1/P$ smaller than the kept ones.

(c) The band narrows in proportion to $1/P$, the barriers' transparency: it is the broadening of the isolated-well level $x = \pi$ by tunneling between neighboring wells, the tight-binding picture of 04-11. A narrower band means a flatter $E(k)$ and a heavier effective mass, which grows roughly in proportion to $P$: in the limit, carriers are localized in their wells.

### Solution 09-01.8

(a) $E$ runs from $E_0 - 2t$ (at $k = 0$) to $E_0 + 2t$ (at $k = \pm\pi/d$): width $4t$ = **2.0** eV.

(b) $d^2E/dk^2 = 2td^2\cos kd$. At $k = 0$:

$$
m^* = \frac{\hbar^2}{2td^2} = \frac{(1.054572\times10^{-34})^2}{2 \times 0.5 \times 1.602177\times10^{-19} \times (0.3\times10^{-9})^2}\ \text{kg} = 0.8467\,m_0 .
$$

At $k = \pi/d$, $\cos kd = -1$, so $m^*$ = **−0.8467** $m_0$: the band top has negative mass, which is the reason holes are introduced.

(c) $v_g = (1/\hbar)\,dE/dk = 2td\sin(kd)/\hbar$, largest at $kd = \pi/2$, i.e. $k$ = **5.236 × 10⁹** m⁻¹:

$$
v_{g,\max} = \frac{2td}{\hbar} = \frac{2 \times 0.5 \times 1.602177\times10^{-19} \times 0.3\times10^{-9}}{1.054572\times10^{-34}} = 4.558\times10^5\ \text{m/s} .
$$

**Sanity check.** A Bloch electron cannot be accelerated indefinitely: its velocity rises, peaks mid-band and falls to zero at the zone edge, where Bragg reflection turns it into a standing wave.

### Solution 09-01.9

(a) With four valleys along the cube diagonals, a field along $x$ makes the same angle with every valley axis, so by symmetry each valley responds identically and the cubic average gives the same formula as for silicon (the trace of the inverse-mass tensor divided by 3):

$$
\frac{1}{m_c} = \frac13\left(\frac{1}{1.6} + \frac{2}{0.08}\right) = \frac{25.625}{3} \quad\Longrightarrow\quad m_c = 0.1171\,m_0 .
$$

(b) One valley: $(m_lm_t^2)^{1/3} = (1.6 \times 0.08^2)^{1/3}$ = **0.2172** $m_0$. Four valleys: $m_{dn} = 4^{2/3} \times 0.2172$ = **0.5472** $m_0$.

(c) $N_C = 2.509\times10^{19} \times 0.5472^{1.5}$ = **1.016 × 10¹⁹** cm⁻³, **2.3**% below Hu's value.

(d) $m_{dp} = (0.33^{1.5} + 0.043^{1.5})^{2/3}$ = **0.3403** $m_0$ and $N_V = 2.509\times10^{19} \times 0.3403^{1.5}$ = **4.981 × 10¹⁸** cm⁻³, **17.0**% below Hu's.

(e) The parabolic-band formula uses band-edge masses. Germanium's valence bands are strongly non-parabolic (and the split-off band is close), so at room temperature, where holes spread over a few $kT$, the effective counting mass is larger than the band-edge masses imply, exactly as for silicon's holes in Example 09-01.4. Tables built from room-temperature masses give the larger $N_V$.

### Solution 09-01.10

(a) $\Phi_s = \chi + (E_C - E_F) = 4.05 + 0.25$ = **4.30** eV. The metal's Fermi level lies $4.50 - 4.30$ = **0.20** eV lower (farther below the vacuum level). Electrons flow from the semiconductor, where they sit higher, into the metal until the Fermi levels align, leaving the semiconductor's surface depleted: the start of a Schottky barrier ([09-06](../chapters/09-06-pn-junction-iv-and-capacitance.md)).

(b) $|\mathcal E| = (1/q)\,|dE_C/dx| = 0.30\ \text{V}/50\times10^{-7}\ \text{cm}$ = **6.0 × 10⁴** V/cm. The field points toward rising band energy: from right to left, along $-x$. Electrons drift downhill, to the **right** (against the field); holes float up the $E_V$ slope, to the **left** (with the field).

(c) It falls 0.30 eV in potential energy, so without scattering it gains **0.30** eV of kinetic energy.

### Solution 09-01.11

(a) $E_g(T) = 1.519 - 5.405\times10^{-4}T^2/(T + 204)$: **1.5076** eV at 77 K, **1.4225** eV at 300 K, **1.3758** eV at 400 K.

(b) Differentiating, $dE_g/dT = -\alpha_VT(T + 2\beta_V)/(T + \beta_V)^2 = -5.405\times10^{-4} \times 300 \times 708/504^2$ eV/K = **−0.452** meV/K.

(c) $\lambda = hc/E_g = 1239.84/1.4225$ = **871.6** nm. Since $\lambda = (hc/q)/E_g$, $d\lambda/dT = -(1239.84/E_g^2)\,dE_g/dT = (1239.84/1.4225^2) \times 4.519\times10^{-4}$ = **0.277** nm/K: the wavelength lengthens as the device warms.

(d) $E_g(350\ \text{K}) = 1.519 - 5.405\times10^{-4} \times 350^2/554 = 1.3995$ eV, so $\lambda$ = **885.9** nm, a shift of **14.3** nm. (The linear estimate, $0.277 \times 50$ = 13.8 nm, slightly underestimates it because $dE_g/dT$ steepens with temperature.)

(e) Wavelength-division multiplexing packs channels a fraction of a nanometer apart, so a few kelvin of drift moves a laser into its neighbor's channel; thermoelectric coolers hold the laser temperature constant.

### Solution 09-01.12

(a) $a = 0.75 \times 5.431 + 0.25 \times 5.658$ = **5.48775** Å. Mismatch: $(5.48775 - 5.431)/5.431$ = **1.045**%. A coherent layer must shrink in-plane to silicon's spacing: strain $(5.431 - 5.48775)/5.48775$ = **−1.034**%, **compressive**. (The layer stretches out of plane in response, a tetragonal distortion.)

(b) $a = 0.40 \times 5.65325 + 0.60 \times 6.0583$ = **5.8963** Å; mismatch to InP $(5.8963 - 5.8697)/5.8697$ = **0.453**%, also compressive when grown on InP.

### Solution 09-01.13

(a) $E_g = 1239.84/2000$ = **0.6199** eV.

(b) With $E_{GaAs}$ = 1.4225 eV and $E_{InAs}$ = 0.3538 eV at 300 K:

$$
E_g(y) = (1 - y)(1.4225) + y(0.3538) - 0.477\,y(1 - y) = 1.4225 - 1.5457\,y + 0.477\,y^2 .
$$

Setting this equal to 0.6199 eV gives $0.477y^2 - 1.5457y + 0.8026 = 0$, whose root in [0, 1] is $y = \left[1.5457 - \sqrt{1.5457^2 - 4 \times 0.477 \times 0.8026}\right]/(2 \times 0.477)$ = **0.6493**.

(c) $a = 5.65325 + 0.6493 \times (6.0583 - 5.65325)$ = **5.9163** Å; mismatch to InP **0.793**%.

(d) $1239.84/0.3538$ = **3504** nm. Pure InAs absorbs out to 3.5 µm but is 3.2% mismatched to InP; the 2 µm alloy sits between. At 0.79% mismatch a thick absorber cannot stay coherent on InP: it relaxes through misfit dislocations, which raise dark current. Extended-wavelength detectors therefore grow graded buffer layers that relax the lattice step by step before the absorber, accepting higher dark current than lattice-matched 1.7 µm devices.

### Solution 09-01.14

(a) Put the in-plane valleys at energy 0 and the two lowered valleys at $-\Delta E$. With equal densities of states, populations are proportional to the Boltzmann factors, so

$$
f = \frac{2e^{\Delta E/kT}}{2e^{\Delta E/kT} + 4} = \frac{1}{1 + 2e^{-\Delta E/kT}} .
$$

At $\Delta E = 0$, $f$ = **1/3**: two of six equal valleys.

(b) $f = 0.8$ requires $2e^{-\Delta E/kT} = 0.25$, so $\Delta E = kT\ln8 = 0.02585 \times 2.0794$ = **53.8** meV.

(c) $f = 1/(1 + 2e^{-0.10/0.02585})$ = **0.960**.

### Solution 09-01.15

(a) A field along $x$ accelerates an electron in each valley by $q\mathcal E/m_{xx}$, where $m_{xx}$ is that valley's mass along $x$. The two $z$ valleys have their long axis along $z$, so $m_{xx} = m_t$. Of the four in-plane valleys, the two along $x$ have $m_{xx} = m_l$ and the two along $y$ have $m_{xx} = m_t$. Averaging accelerations over the electron population:

$$
\frac{1}{m_c} = f\,\frac{1}{m_t} + (1 - f)\cdot\frac12\left(\frac{1}{m_l} + \frac{1}{m_t}\right) .
$$

At $f = 1/3$: $\frac{1}{3m_t} + \frac13\left(\frac{1}{m_l} + \frac{1}{m_t}\right) = \frac13\left(\frac{1}{m_l} + \frac{2}{m_t}\right)$, the chapter's result.

(b) Unstrained, $m_c$ = 0.2598 $m_0$. At $f$ = 0.8: $1/m_c = 0.8/0.19 + 0.1 \times (1/0.98 + 1/0.19) = 4.8389$, so $m_c$ = **0.2067** $m_0$ and $\mu(f)/\mu(1/3) = 0.2598/0.2067$ = **1.257**. At $f$ = 1: $m_c = m_t$ = 0.19 $m_0$ and the ratio is $0.2598/0.19$ = **1.367**.

(c) Mobility is $q\tau/m_c$, so the gain is (mass factor) × (scattering-time factor). Even the full mass factor, 1.367, leaves $1.5/1.367$ = **1.10** to reach the low end and $2.0/1.367$ = **1.46** for the high end. The extra comes from a longer scattering time: once the two valleys sit tens of meV below the other four, phonon scattering of electrons into the four upper valleys (intervalley scattering) needs extra energy and becomes rarer.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 09-01.1a | Ge atomic density | 4.417e22 | cm⁻³ |
| 09-01.1b | Ge nearest-neighbor distance | 2.450 | Å |
| 09-01.1c | Ge second-neighbor distance | 4.001 | Å |
| 09-01.1d | Ge molar mass from density | 72.58 | g/mol |
| 09-01.1e | Ge–Si bond-length difference | 4.2 | % |
| 09-01.1f | Ge to Si atomic mass ratio | 2.6 | — |
| 09-01.1g | Ge to Si density ratio | 2.3 | — |
| 09-01.1h | Si molar mass (rounded) | 28.09 | g/mol |
| 09-01.2a | (231) spacing in Si | 1.451 | Å |
| 09-01.3a | angle (110)–(111) | 35.26 | ° |
| 09-01.3b | angle (111)–(1̄11) | 70.53 | ° |
| 09-01.3c | tetrahedral bond angle | 109.47 | ° |
| 09-01.4a | GaAs atomic density | 4.428e22 | cm⁻³ |
| 09-01.4b | GaAs (100) single-element plane density | 6.258e14 | cm⁻² |
| 09-01.4c | GaAs (111) single-element plane density | 7.226e14 | cm⁻² |
| 09-01.5a | {111} sidewall angle | 54.74 | ° |
| 09-01.5b | pit depth | 7.071 | µm |
| 09-01.5c | sidewall length | 8.660 | µm |
| 09-01.6a | E_d at d = 0.4 nm | 0.2381 | eV |
| 09-01.6o | E_d in joules | 3.815e-20 | J |
| 09-01.6b | band 1 bottom, x | 1.5427 | — |
| 09-01.6c | band 1 bottom | 0.5667 | eV |
| 09-01.6d | band 1 top | 2.350 | eV |
| 09-01.6e | band 1 width | 1.783 | eV |
| 09-01.6f | band 2 bottom, x | 3.8795 | — |
| 09-01.6g | band 2 bottom | 3.584 | eV |
| 09-01.6h | first gap width | 1.234 | eV |
| 09-01.6i | F' at band 1 bottom | -1.6023 | — |
| 09-01.6j | band-bottom effective mass | 1.039 | m0 |
| 09-01.6k | band 1 width in E_d, P = 1.5 | 7.490 | — |
| 09-01.6l | band 1 width in E_d, P = 3 | 5.963 | — |
| 09-01.6m | gap width in E_d, P = 1.5 | 5.181 | — |
| 09-01.6n | gap width in E_d, P = 3 | 9.046 | — |
| 09-01.7a | x_b exact, P = 20 | 2.8577 | — |
| 09-01.7b | x_b approximate, P = 20 | 2.8274 | — |
| 09-01.7c | band width exact, P = 20 | 1.7029 | E_d |
| 09-01.7d | band width approximate, P = 20 | 1.9739 | E_d |
| 09-01.7e | relative error, P = 20 | 15.9 | % |
| 09-01.7f | x_b exact, P = 50 | 3.0209 | — |
| 09-01.7g | x_b approximate, P = 50 | 3.0159 | — |
| 09-01.7h | band width exact, P = 50 | 0.7437 | E_d |
| 09-01.7i | band width approximate, P = 50 | 0.7896 | E_d |
| 09-01.7j | relative error, P = 50 | 6.2 | % |
| 09-01.8a | tight-binding band width | 2.0 | eV |
| 09-01.8b | effective mass at band bottom | 0.8467 | m0 |
| 09-01.8c | effective mass at band top | -0.8467 | m0 |
| 09-01.8d | k of maximum group velocity | 5.236e9 | m⁻¹ |
| 09-01.8e | maximum group velocity | 4.558e5 | m/s |
| 09-01.9a | Ge conductivity mass | 0.1171 | m0 |
| 09-01.9i | sum 1/m_l + 2/m_t for Ge | 25.625 | 1/m0 |
| 09-01.9b | Ge single-valley DOS mass | 0.2172 | m0 |
| 09-01.9c | Ge electron DOS mass | 0.5472 | m0 |
| 09-01.9d | Ge N_C | 1.016e19 | cm⁻³ |
| 09-01.9e | Ge N_C below Hu | 2.3 | % |
| 09-01.9f | Ge hole DOS mass | 0.3403 | m0 |
| 09-01.9g | Ge N_V | 4.981e18 | cm⁻³ |
| 09-01.9h | Ge N_V below Hu | 17.0 | % |
| 09-01.10a | Si work function | 4.30 | eV |
| 09-01.10b | Fermi-level difference to metal | 0.20 | eV |
| 09-01.10c | electric field | 6.0e4 | V/cm |
| 09-01.10d | kinetic energy gained | 0.30 | eV |
| 09-01.11a | GaAs gap at 77 K | 1.5076 | eV |
| 09-01.11b | GaAs gap at 300 K | 1.4225 | eV |
| 09-01.11c | GaAs gap at 400 K | 1.3758 | eV |
| 09-01.11d | GaAs dEg/dT at 300 K | -0.452 | meV/K |
| 09-01.11e | emission wavelength at 300 K | 871.6 | nm |
| 09-01.11f | dλ/dT at 300 K | 0.277 | nm/K |
| 09-01.11g | GaAs gap at 350 K | 1.3995 | eV |
| 09-01.11h | wavelength at 350 K | 885.9 | nm |
| 09-01.11i | wavelength shift 300 to 350 K | 14.3 | nm |
| 09-01.11j | linear estimate of the shift | 13.8 | nm |
| 09-01.12a | Si0.75Ge0.25 lattice constant | 5.48775 | Å |
| 09-01.12b | SiGe mismatch to Si | 1.045 | % |
| 09-01.12c | coherent in-plane strain | -1.034 | % |
| 09-01.12d | Ga0.40In0.60As lattice constant | 5.8963 | Å |
| 09-01.12e | Ga0.40In0.60As mismatch to InP | 0.453 | % |
| 09-01.13a | gap for 2.00 µm cutoff | 0.6199 | eV |
| 09-01.13b | In fraction | 0.6493 | — |
| 09-01.13c | alloy lattice constant | 5.9163 | Å |
| 09-01.13d | mismatch to InP | 0.793 | % |
| 09-01.13e | InAs cutoff wavelength | 3504 | nm |
| 09-01.13f | InAs mismatch to InP | 3.2 | % |
| 09-01.13g | linear coefficient of the gap polynomial | -1.5457 | eV |
| 09-01.13h | constant term of the quadratic | 0.8026 | eV |
| 09-01.14a | lowered-valley fraction, no strain | 0.3333 | — |
| 09-01.14b | splitting for 80% | 53.8 | meV |
| 09-01.14c | fraction at 0.10 eV splitting | 0.960 | — |
| 09-01.15a | m_c at f = 0.8 | 0.2067 | m0 |
| 09-01.15b | mobility ratio at f = 0.8 | 1.257 | — |
| 09-01.15c | mobility ratio at f = 1 | 1.367 | — |
| 09-01.15d | scattering factor for 1.5× | 1.10 | — |
| 09-01.15e | scattering factor for 2.0× | 1.46 | — |
| 09-01.15f | 1/m_c at f = 0.8 | 4.8389 | 1/m0 |
