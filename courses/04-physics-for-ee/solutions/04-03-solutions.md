# Solutions 04-03 · Gauss's Law

Problems: [04-03 problems](../problems/04-03-problems.md) · Chapter: [04-03](../chapters/04-03-gauss-law.md). Every number below is recomputed by [verify_04_03.py](../verify/verify_04_03.py).

---

## Solutions

### Solution 04-03.1

(a) The roof's normal is vertical, parallel to the field: $|\Phi| = EA = 500\times6 = $ **3000 V·m**.

(b) Tilting the roof by 40° tilts its normal by 40° from the field: $|\Phi| = EA\cos40° = 3000\times0.7660 = $ **2298 V·m**. Equivalently, the field sees the roof's horizontal projection, $6\cos40°$ m².

(c) **Zero.** The shed encloses no charge; every field line that enters through the roof leaves through the floor.

**Units check.** (V/m)(m²) = V·m ✓.

### Solution 04-03.2

(a) $Q_{\text{enc}} = \varepsilon_0\Phi = 8.854\times10^{-12}\times(-5000) = $ **−4.427×10⁻⁸ C**, that is −44.27 nC.

(b) No. Gauss's law gives only the net enclosed charge. The same flux results whether the charge is concentrated or spread out, near the surface or deep inside, and any charges outside contribute nothing to the net flux. Locating the charge needs the field itself, point by point.

### Solution 04-03.3

(a) A point charge $q_1$ has no preferred direction, so its field is radial with magnitude depending only on $r$. On a concentric sphere, Gauss's law gives $E\cdot4\pi r^2 = q_1/\varepsilon_0$, so $E = q_1/(4\pi\varepsilon_0r^2)$. A second charge $q_2$ placed there feels $F = q_2E = q_1q_2/(4\pi\varepsilon_0r^2)$: Coulomb's law.

(b) $E = k_eq/r^2 = 8.988\times10^9\times5\times10^{-9}/0.1^2 = $ **4494 V/m**.

(c) Both surfaces enclose the charge, so both carry $q/\varepsilon_0 = 5\times10^{-9}/8.854\times10^{-12} = $ **564.7 V·m**. Shape and size do not matter.

### Solution 04-03.4

(a) Eight cubes of side 10 cm meeting at the charge's corner would together form a 20 cm cube with the charge at its center, carrying total flux $q/\varepsilon_0$. By symmetry each small cube gets an eighth: $\Phi = q/(8\varepsilon_0) = 8\times10^{-9}/(8\times8.854\times10^{-12}) = $ **112.9 V·m**.

(b) The three faces that meet at the charge's corner contain the charge's position in their planes, so the field there lies in the face (radial from a point in the plane) and carries **no flux**. The other three faces share the 112.9 V·m equally by symmetry: **37.65 V·m** each.

### Solution 04-03.5

At 5 cm, a concentric Gaussian sphere encloses only the −5 nC: $E = k_e(5\times10^{-9})/0.05^2 = $ **1.798×10⁴ V/m**, pointing **inward** (toward the negative charge). The shell's charge contributes nothing inside.

At 15 cm the sphere encloses $+20 - 5 = +15$ nC: $E = k_e(15\times10^{-9})/0.15^2 = $ **5992 V/m**, pointing **outward**.

### Solution 04-03.6

(a) Use a coaxial Gaussian cylinder of radius $r$ and length $\ell$. Inside ($r < a$) it encloses $\rho\pi r^2\ell$, so $E\cdot2\pi r\ell = \rho\pi r^2\ell/\varepsilon_0$ and

$$
E = \frac{\rho r}{2\varepsilon_0}\quad(r < a), \qquad E = \frac{\rho a^2}{2\varepsilon_0r}\quad(r > a) ,
$$

the second because the enclosed charge stops growing at $r = a$, giving $\lambda = \rho\pi a^2$.

(b) At 0.5 mm: $0.01\times5\times10^{-4}/(2\times8.854\times10^{-12}) = $ **2.824×10⁵ V/m**. At 1 mm (the surface): **5.647×10⁵ V/m**, where both formulas agree. At 5 mm: $5.647\times10^5\times(1/5) = $ **1.129×10⁵ V/m**.

### Solution 04-03.7

At 0.5 cm a coaxial cylinder encloses nothing: **0**. At 2 cm it encloses +3 nC/m: $E = \lambda/(2\pi\varepsilon_0r) = 3\times10^{-9}/(2\pi\times8.854\times10^{-12}\times0.02) = $ **2696 V/m**, outward. At 4 cm it encloses +2 nC/m: **898.8 V/m**, outward.

### Solution 04-03.8

(a) By symmetry the field at the midplane is **0**. A pillbox from the midplane to distance $x$ gives $EA = \rho xA/\varepsilon_0$, so $E = \rho x/\varepsilon_0$ inside. At 0.5 mm: $10^{-4}\times5\times10^{-4}/8.854\times10^{-12} = $ **5647 V/m**. At the surface (1 mm): **1.129×10⁴ V/m**. Outside, the pillbox encloses the full half-thickness, $\rho t/2$, at any distance, so 1 cm outside the field is still **1.129×10⁴ V/m**.

(b) $E(x)$ is an odd function: a straight line through zero across the slab, pointing away from the midplane on both sides, then flat outside.

### Solution 04-03.9

(a) $E = \sigma/\varepsilon_0$ just outside a conductor, so $\sigma_{\max} = \varepsilon_0E_{\text{bd}} = 8.854\times10^{-12}\times3\times10^6 = $ **2.656×10⁻⁵ C/m²**.

(b) $2.656\times10^{-5}/1.602\times10^{-19} = 1.658\times10^{14}$ per m², which is **1.658×10¹⁰ electrons per cm²**.

(c) Atoms 0.3 nm apart give $1/(0.3\times10^{-7}\ \text{cm})^2 = $ **1.111×10¹⁵ atoms per cm²**. The fraction is $1.658\times10^{10}/1.111\times10^{15} = $ **1.492×10⁻⁵**: about one surface atom in 67,000. Even a conductor charged to the point of sparking is overwhelmingly neutral, which is why its surface charge can rearrange so easily.

### Solution 04-03.10

(a) A Gaussian surface in the metal around the cavity has zero field and must enclose zero charge, so the cavity wall carries **−2 nC**. The conductor's net charge is +3 nC = (cavity wall) + (outer surface), so the outer surface carries $3 - (-2) = $ **+5 nC**.

(b) **Yes, uniform.** The cavity wall's −2 nC arranges itself so that, together with the +2 nC, it produces zero field throughout the metal; the uniqueness theorem of [13-02](../../13-electromagnetics/chapters/13-02-electrostatics-boundary-value-problems.md) shows the pair then produces zero field everywhere outside the cavity as well. The outer +5 nC therefore feels nothing from inside and arranges itself as on an isolated sphere, which by symmetry means uniformly, wherever the inner charge sits.

(c) $\sigma = 5\times10^{-9}/(4\pi\times0.05^2) = $ **1.592×10⁻⁷ C/m²**. At 10 cm the field is that of +5 nC at the center: $8.988\times10^9\times5\times10^{-9}/0.01 = $ **4494 V/m**.

### Solution 04-03.11

Label the four surfaces 1 to 4 from left to right (1 and 2 on plate A, 3 and 4 on plate B), with charge densities $\sigma_1, \dots, \sigma_4$. Each surface is a large sheet with field $\sigma/(2\varepsilon_0)$ pointing away from it on both sides.

**Inside plate A's metal** (to the right of sheet 1, left of sheets 2–4) the field must vanish:

$$
\frac{\sigma_1 - \sigma_2 - \sigma_3 - \sigma_4}{2\varepsilon_0} = 0 .
$$

**Inside plate B's metal** (right of sheets 1–3, left of sheet 4):

$$
\frac{\sigma_1 + \sigma_2 + \sigma_3 - \sigma_4}{2\varepsilon_0} = 0 .
$$

Adding the two gives $\sigma_1 = \sigma_4$; subtracting gives $\sigma_2 = -\sigma_3$. With the plate charges $(\sigma_1 + \sigma_2)A = 4$ nC and $(\sigma_3 + \sigma_4)A = -1$ nC, adding gives $(\sigma_1 + \sigma_4)A = 3$ nC.

(a) The outer surfaces each carry **1.5 nC** (half the total), the inner face of A carries **+2.5 nC** and the inner face of B **−2.5 nC**.

(b) Between the plates, all four fields add to $\sigma_2/\varepsilon_0 = 2.5\times10^{-9}/(0.01\times8.854\times10^{-12}) = $ **2.824×10⁴ V/m**, from A toward B. Outside, $(\sigma_1 + \sigma_2 + \sigma_3 + \sigma_4)/(2\varepsilon_0) = 3\times10^{-9}/(2\times0.01\times8.854\times10^{-12}) = $ **1.694×10⁴ V/m**, pointing away from the pair on both sides.

**Sanity check.** If the plates carried equal and opposite charges, the outer surfaces would be bare and the field outside zero: the ideal capacitor of 04-04. Any net charge spreads equally over the two outer faces.

### Solution 04-03.12

Convert: $N_A = 10^{24}$ m⁻³, $N_D = 10^{21}$ m⁻³, $\varepsilon_s = 11.7\varepsilon_0 = 1.036\times10^{-10}$ F/m.

(a) $x_p = x_nN_D/N_A = 1.0\ \text{µm}\times10^{-3} = $ **1 nm**. The depletion region lies almost entirely in the lightly doped n side: a **one-sided** junction.

(b) $E_{\max} = qN_Dx_n/\varepsilon_s = 1.602\times10^{-19}\times10^{21}\times10^{-6}/1.036\times10^{-10} = $ **1.547×10⁶ V/m**, which is **15.47 kV/cm**.

(c) $\tfrac12E_{\max}(x_n + x_p) = 0.5\times1.547\times10^6\times1.001\times10^{-6} = $ **0.7741 V**.

**Interpretation.** For the same 0.77 V, the lightly doped junction has a three-times-wider depletion region and a three-times-smaller peak field than Example 04-03.6: lighter doping buys breakdown voltage at the cost of width.

### Solution 04-03.13

(a) Take a flat pillbox of face area $A$ with one face in the oxide and one in the silicon, and let its thickness shrink to zero. The side walls then carry no flux, and the pillbox encloses no free charge. Gauss's law for free charge gives $\varepsilon_{\text{Si}}E_{\text{Si}}A - \varepsilon_{\text{ox}}E_{\text{ox}}A = 0$ (normal components, both measured along the same direction), so $\varepsilon_{\text{ox}}E_{\text{ox}} = \varepsilon_{\text{Si}}E_{\text{Si}}$.

(b) $E_{\text{Si}} = E_{\text{ox}}\varepsilon_{\text{ox}}/\varepsilon_{\text{Si}} = 5\times3.9/11.7 = $ **1.667 MV/cm**: three times weaker than in the oxide.

(c) The gate charge per area equals $\varepsilon_{\text{ox}}E_{\text{ox}}$ (a pillbox with one face in the gate metal): $3.9\times8.854\times10^{-12}\times5\times10^8 = $ **1.727×10⁻² C/m²**. In electrons: $1.727\times10^{-2}/1.602\times10^{-19} = 1.078\times10^{17}$ m⁻², which is **1.078×10¹³ cm⁻²**: about one electron per 9 nm², or roughly a hundred under a 30 nm × 30 nm gate.

### Solution 04-03.14

(a) Inside a uniform sphere of density ρ, the field at position $\vec r$ from its center is radial with magnitude $\rho r/(3\varepsilon_0)$ (from $E\cdot4\pi r^2 = \rho\tfrac43\pi r^3/\varepsilon_0$), so in vector form $\vec E = \rho\vec r/(3\varepsilon_0)$. The holed sphere equals the full sphere (density ρ, center O) plus a small sphere of density −ρ filling the cavity (center C, at $\vec d$ from O). At a point $\vec r$ in the cavity, measured from O, the two fields are $\rho\vec r/(3\varepsilon_0)$ and $-\rho(\vec r - \vec d)/(3\varepsilon_0)$. Their sum is

$$
\vec E = \frac{\rho}{3\varepsilon_0}\big[\vec r - (\vec r - \vec d)\big] = \frac{\rho\vec d}{3\varepsilon_0} ,
$$

independent of position: uniform throughout the cavity, pointing from O toward C.

(b) $E = 10^{-6}\times0.02/(3\times8.854\times10^{-12}) = $ **752.9 V/m**.

### Solution 04-03.15

The button area is $A = \pi(5\times10^{-3})^2 = 7.854\times10^{-5}$ m², and $C_F = \varepsilon_r\varepsilon_0A/d$.

(a) Glass: $C_F = 7\times8.854\times10^{-12}\times7.854\times10^{-5}/1.5\times10^{-3} = $ **3.245 pF**, raising the total by $3.245/20 = $ **16.23%**.

(b) Acrylic: $C_F = 2.6\times8.854\times10^{-12}\times7.854\times10^{-5}/3\times10^{-3} = $ **0.6027 pF**, a change of **3.013%**.

The glass overlay gives **5.385** times the signal: $7/2.6$ for permittivity times 2 for thickness.

(c) The model assumes a flat conducting finger fully covering the pad, with all field lines running straight across. A real fingertip is curved and partly covers the pad, and fringing field lines from the pad end on nearby ground copper instead of the finger, so the real $C_F$ is smaller. Datasheet benchmarks (0.1 pF on a 33 pF pad, [R-078](../../../reference/research-log.md#r-078--gauss-law-applications-silicon-permittivity-capacitive-sensing-and-coulombs-law-tests)) show by how much.

### Solution 04-03.16

(a) On a concentric sphere the field is radial and constant: $\Phi = \dfrac{k_eq}{r^{2+\delta}}\cdot4\pi r^2 = 4\pi k_eq\,r^{-\delta} = \dfrac{q}{\varepsilon_0}r^{-\delta}$.

(b) $\Phi(2)/\Phi(1) = 2^{-0.01} = $ **0.9931**: 0.7% of the flux "disappears" between the spheres, so Gauss's law fails.

(c) With δ = 0 the field inside a charged closed conductor is exactly zero, so any measured field is a direct signal of δ ≠ 0, with nothing to subtract. Experiments charge a shell to a high voltage and look for any interior field with a sensitive detector; a null measurement bounds δ at the level of the detector's sensitivity divided by the applied field, which is how δ has been bounded to parts in 10¹⁶.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 04-03.1a | flux through the flat roof | 3000 | V·m |
| 04-03.1b | flux through the tilted roof | 2298 | V·m |
| 04-03.1c | net flux out of the shed | 0 | V·m |
| 04-03.2a | enclosed charge | −4.427×10^-8 | C |
| 04-03.3a | field 10 cm from 5 nC | 4494 | V/m |
| 04-03.3b | flux of 5 nC | 564.7 | V·m |
| 04-03.4a | flux through the cube, charge at a corner | 112.9 | V·m |
| 04-03.4b | flux through each far face | 37.65 | V·m |
| 04-03.5a | field at 5 cm (inward) | 1.798×10^4 | V/m |
| 04-03.5b | field at 15 cm (outward) | 5992 | V/m |
| 04-03.6a | rod field at 0.5 mm | 2.824×10^5 | V/m |
| 04-03.6b | rod field at 1 mm | 5.647×10^5 | V/m |
| 04-03.6c | rod field at 5 mm | 1.129×10^5 | V/m |
| 04-03.7a | field at 0.5 cm | 0 | V/m |
| 04-03.7b | field at 2 cm | 2696 | V/m |
| 04-03.7c | field at 4 cm | 898.8 | V/m |
| 04-03.8a | slab field at the midplane | 0 | V/m |
| 04-03.8b | slab field 0.5 mm from the midplane | 5647 | V/m |
| 04-03.8c | slab field at the surface | 1.129×10^4 | V/m |
| 04-03.8d | slab field 1 cm outside | 1.129×10^4 | V/m |
| 04-03.9a | maximum surface charge density | 2.656×10^-5 | C/m² |
| 04-03.9b | electrons per cm² | 1.658×10^10 | cm⁻² |
| 04-03.9c | surface atoms per cm² | 1.111×10^15 | cm⁻² |
| 04-03.9d | fraction of surface atoms charged | 1.492×10^-5 | — |
| 04-03.10a | charge on the cavity wall | −2 | nC |
| 04-03.10b | charge on the outer surface | 5 | nC |
| 04-03.10c | outer surface charge density | 1.592×10^-7 | C/m² |
| 04-03.10d | field at 10 cm | 4494 | V/m |
| 04-03.11a | charge on each outer surface | 1.5 | nC |
| 04-03.11b | charge on plate A's inner face | 2.5 | nC |
| 04-03.11c | charge on plate B's inner face | −2.5 | nC |
| 04-03.11d | field between the plates | 2.824×10^4 | V/m |
| 04-03.11e | field outside the plates | 1.694×10^4 | V/m |
| 04-03.12a | p-side width | 1 | nm |
| 04-03.12b | peak field | 1.547×10^6 | V/m |
| 04-03.12c | peak field | 15.47 | kV/cm |
| 04-03.12d | area under the field | 0.7741 | V |
| 04-03.13a | field in the silicon | 1.667 | MV/cm |
| 04-03.13b | gate charge per area | 1.727×10^-2 | C/m² |
| 04-03.13c | gate electrons per cm² | 1.078×10^13 | cm⁻² |
| 04-03.14a | field in the cavity | 752.9 | V/m |
| 04-03.15a | finger capacitance, glass | 3.245 | pF |
| 04-03.15b | change in capacitance, glass | 16.23 | % |
| 04-03.15c | finger capacitance, acrylic | 0.6027 | pF |
| 04-03.15d | change in capacitance, acrylic | 3.013 | % |
| 04-03.15e | glass over acrylic signal | 5.385 | — |
| 04-03.16a | flux ratio, 2 m over 1 m, δ = 0.01 | 0.9931 | — |
