# Solutions 04-04 · Electric Potential, Capacitance and Dielectrics

Problems: [04-04 problems](../problems/04-04-problems.md) · Chapter: [04-04](../chapters/04-04-potential-capacitance-and-dielectrics.md). Every number below is recomputed by [verify_04_04.py](../verify/verify_04_04.py).

---

## Solutions

### Solution 04-04.1

(a) $V = k_eq/r$: at 10 cm, \$8.988\times10^9\times5\times10^{-9}/0.1 = \$ **449.4 V**; at 30 cm, **149.8 V**.

(b) You must raise the 1 nC charge's potential energy by $q\Delta V = 10^{-9}\times(449.4 - 149.8) = $ **2.996×10⁻⁷ J**, pushing it toward the like charge against the repulsion.

### Solution 04-04.2

(a) $1\ \text{keV} = 1000\times1.602\times10^{-19} = $ **1.602×10⁻¹⁶ J**.

(b) $\Delta U = q\Delta V = (-1.602\times10^{-19})(+5) = $ **−8.011×10⁻¹⁹ J**: the electron's potential energy falls as it moves to higher potential.

(c) Energy is conserved, so it gains **5 eV** of kinetic energy.

### Solution 04-04.3

\$V(4\ \text{cm}, 0) - V(0, 0) = -\int_0^{0.04}E\,dx = -500\times0.04 = \$ **−20 V**: the potential falls along the field. Moving along $y$, perpendicular to the field, does no work: **0 V**. The equipotentials are planes of constant $x$, perpendicular to the field.

### Solution 04-04.4

(a) $V(z) = \dfrac{\sigma}{2\varepsilon_0}\big(\sqrt{z^2 + R^2} - z\big)$ with $\sigma/(2\varepsilon_0) = 5.647\times10^4$ V/m. At $z$ = 1 mm: \$5.647\times10^4\times(0.010050 - 0.001) = \$ **511.1 V**. At the center: \$5.647\times10^4\times0.01 = \$ **564.7 V**.

(b) $E_z = -\dfrac{dV}{dz} = \dfrac{\sigma}{2\varepsilon_0}\Big(1 - \dfrac{z}{\sqrt{z^2 + R^2}}\Big) = $ **5.085×10⁴ V/m**, the same as the disk field integrated in Example 04-02.5.

### Solution 04-04.5

(a) $V = k_ep\cos\theta/r^2 = 8.988\times10^9\times10^{-12}\times0.5/0.01 = $ **0.4494 V**.

(b) $E_r = -\partial V/\partial r = 2k_ep\cos\theta/r^3 = $ **8.988 V/m**; $E_\theta = -(1/r)\,\partial V/\partial\theta = k_ep\sin\theta/r^3 = $ **7.783 V/m**. The magnitude is $\sqrt{E_r^2 + E_\theta^2} = $ **11.89 V/m**.

**Sanity check.** At θ = 0 these give $E = 2k_ep/r^3$ on the axis, and at θ = 90° $E = k_ep/r^3$ broadside, matching 04-02 §3.5 ✓.

### Solution 04-04.6

(a) Far apart, each sphere's potential is $k_eQ_i/R_i$, and the wire makes them equal, so $Q_i\propto R_i$: \$Q_1 = 22\times1/11 = \$ **2 nC**, \$Q_2 = \$ **20 nC**.

(b) $V = k_eQ_1/R_1 = 8.988\times10^9\times2\times10^{-9}/0.01 = $ **1798 V**.

(c) $E = V/R$: **1.798×10⁵ V/m** on the small sphere and **1.798×10⁴ V/m** on the large one.

(d) $\sigma = Q/(4\pi R^2)$: **1.592×10⁻⁶ C/m²** and **1.592×10⁻⁷ C/m²**, a tenfold ratio, the inverse of the radii.

### Solution 04-04.7

(a) The series pair: $1/(1/2 + 1/3) = 1.2$ µF. In parallel with 4 µF: **5.2 µF**.

(b) The pair sees the full 10 V: $Q = 1.2\times10 = $ **12 µC**, the same on both.

(c) $V_1 = 12/2 = $ **6 V** and $V_2 = 12/3 = $ **4 V**: the smaller capacitor takes the larger voltage. They add to 10 V ✓.

(d) $U = \tfrac12(5.2\times10^{-6})(10^2) = $ **260 µJ**.

### Solution 04-04.8

(a) Air (1 mm) and dielectric (1 mm) are in series:

$$
C = \frac{\varepsilon_0A}{d_{\text{air}} + d_{\text{slab}}/\varepsilon_r} = \frac{8.854\times10^{-12}\times0.01}{10^{-3} + 0.25\times10^{-3}} ,
$$

which is **70.83 pF**. With 100 V, $D = CV/A = 7.083\times10^{-7}$ C/m². In the air, \$E = D/\varepsilon_0 = \$ **8×10⁴ V/m** (80 V across 1 mm); in the slab, \$E = D/(4\varepsilon_0) = \$ **2×10⁴ V/m** (20 V across 1 mm).

(b) Side by side, the two halves share the voltage and are in parallel: $C = \varepsilon_0(A/2)/d + 4\varepsilon_0(A/2)/d = 2.5\,\varepsilon_0A/d = $ **110.7 pF**.

### Solution 04-04.9

$C/\ell = 2\pi\varepsilon_r\varepsilon_0/\ln(b/a)$ with $b/a = 2.95/0.9 = 3.278$ (diameters give the same ratio as radii): \$2\pi\times2.25\times8.854\times10^{-12}/1.1872 = \$ **105.4 pF/m**. A 1.5 m length is **158.2 pF**.

### Solution 04-04.10

(a) $u = \tfrac12\varepsilon_0E^2 = 0.5\times8.854\times10^{-12}\times(3\times10^6)^2 = $ **39.84 J/m³**.

(b) $C = 4\pi\varepsilon_0R = 11.13$ pF, so \$U = \tfrac12CV^2 = 0.5\times11.13\times10^{-12}\times10^{10} = \$ **0.05563 J**. By field energy: outside, $E = VR/r^2$, and a shell of radius $r$ and thickness $dr$ has volume $4\pi r^2dr$:

$$
U = \int_R^\infty\frac12\varepsilon_0\frac{V^2R^2}{r^4}4\pi r^2\,dr = 2\pi\varepsilon_0V^2R^2\int_R^\infty\frac{dr}{r^2} = 2\pi\varepsilon_0V^2R ,
$$

which is $\tfrac12(4\pi\varepsilon_0R)V^2$ ✓.

### Solution 04-04.11

(a) The field peaks at the inner conductor: $E(a) = V/[a\ln(b/a)]$. Setting $E(a) = E_{\text{bd}}$ gives $V_{\max}(a) = E_{\text{bd}}\,a\ln(b/a)$. Differentiating, $dV_{\max}/da = E_{\text{bd}}[\ln(b/a) - 1]$, which is zero at $\ln(b/a) = 1$, i.e. $b/a = e$; the second derivative, $-E_{\text{bd}}/a$, is negative, so this is a maximum.

(b) $a = 5/e = $ **1.839 mm** and $V_{\max} = E_{\text{bd}}b/e = 3\times10^6\times5\times10^{-3}/e = $ **5.518 kV**.

(c) $V_{\max} = 3\times10^6\times5\times10^{-4}\times\ln10 = $ **3.454 kV**, 37% lower.

### Solution 04-04.12

The capacitor supplies $\Delta Q = I\Delta t = 2\times0.5\times10^{-6} = 1$ µC, so $\Delta V = \Delta Q/C$: (a) **10 mV**, (b) **11.11 mV**, (c) **16.67 mV**. The real droop is 11% (X5R) and 67% (Y5V) larger than the nominal estimate at this mild bias; at biases near the rating, class 2 losses can be much larger.

### Solution 04-04.13

(a) $\text{EOT} = t_{\text{SiO}_2} + t_{\text{HfO}_2}\times3.9/25$, so \$t_{\text{HfO}_2} = (0.9 - 0.4)\times25/3.9 = \$ **3.205 nm**.

(b) $0.4 + 3.205 = $ **3.605 nm**, four times the EOT.

(c) $C/A = 3.9\varepsilon_0/\text{EOT} = 3.9\times8.854\times10^{-12}/0.9\times10^{-9} = 3.837\times10^{-2}$ F/m² = **3.837 µF/cm²**.

### Solution 04-04.14

(a) $\Delta V = (V_{\text{cell}} - V_{\text{BL}})\,C_s/(C_s + C_{\text{BL}}) = 0.55\times8/88 = $ **50 mV**.

(b) Need $(V_{\text{cell}} - 0.55)\times8/88 \ge 0.040$, so \$V_{\text{cell}} \ge 0.55 + 0.44 = \$ **0.99 V**.

(c) The cell may lose **0.11 V**, which is $Q = C_s\Delta V = 8\ \text{fF}\times0.11 = $ **0.88 fC**, or $0.88\times10^{-15}/1.602\times10^{-19} = $ **5493 electrons**. Spread over a refresh interval of tens of milliseconds ([23](../../23-memory-and-storage-technology/README.md)), that budget allows an average leakage of only about ten femtoamperes (0.88 fC over 64 ms is 14 fA).

### Solution 04-04.15

$S = \pi(0.1)^2 = 0.03142$ m² and $l/\varepsilon_r = 0.54/8.8 = 61.36$ µm. $F = \varepsilon_0SV^2/[2(g + 61.36\ \text{µm})^2]$:

(a) $g$ = 0: **36.94 N**. (b) $g$ = 1 µm: **35.76 N**. (c) $g$ = 10 µm: **27.31 N**.

(d) The force depends on the total effective gap $g + l/\varepsilon_r$, squared. A particle or bow of a few micrometers is a sizable fraction of 61 µm, so it weakens the clamp locally and degrades heat transfer to the chuck, which is what the clamp is often for. Thin, high-permittivity dielectrics make the effective gap small, and therefore make the chuck more sensitive.

### Solution 04-04.16

(a) Outside, $E = k_eQ/r^2$; inside, 0. Then

$$
U = \int_R^\infty\frac12\varepsilon_0\Big(\frac{k_eQ}{r^2}\Big)^24\pi r^2\,dr = \frac{Q^2}{8\pi\varepsilon_0}\int_R^\infty\frac{dr}{r^2} = \frac{k_eQ^2}{2R} ,
$$

which is $8.988\times10^9\times10^{-16}/0.1 = $ **8.988×10⁻⁶ J**.

(b) \$C = Q^2/(2U) = 10^{-16}/(1.798\times10^{-5}) = \$ **5.563 pF**, exactly $4\pi\varepsilon_0R$ ✓.

(c) The integral from $R$ to $2R$ gives $\frac{k_eQ^2}{2}\big(\frac1R - \frac{1}{2R}\big) = \frac12\cdot\frac{k_eQ^2}{2R}$: **half** the energy lies within one radius of the surface, where the field is strongest.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 04-04.1a | potential at 10 cm | 449.4 | V |
| 04-04.1b | potential at 30 cm | 149.8 | V |
| 04-04.1c | work to move 1 nC inward | 2.996×10^-7 | J |
| 04-04.2a | 1 keV in joules | 1.602×10^-16 | J |
| 04-04.2b | electron's potential-energy change | −8.011×10^-19 | J |
| 04-04.2c | kinetic energy gained | 5 | eV |
| 04-04.3a | V(4 cm, 0) − V(0, 0) | −20 | V |
| 04-04.3b | V(0, 4 cm) − V(0, 0) | 0 | V |
| 04-04.4a | disk potential at 1 mm | 511.1 | V |
| 04-04.4b | disk potential at the center | 564.7 | V |
| 04-04.4c | disk field at 1 mm | 5.085×10^4 | V/m |
| 04-04.5a | dipole potential | 0.4494 | V |
| 04-04.5b | radial field | 8.988 | V/m |
| 04-04.5c | angular field | 7.783 | V/m |
| 04-04.5d | field magnitude | 11.89 | V/m |
| 04-04.6a | charge on the 1 cm sphere | 2 | nC |
| 04-04.6b | charge on the 10 cm sphere | 20 | nC |
| 04-04.6c | common potential | 1798 | V |
| 04-04.6d | surface field, 1 cm sphere | 1.798×10^5 | V/m |
| 04-04.6e | surface field, 10 cm sphere | 1.798×10^4 | V/m |
| 04-04.6f | surface charge density, 1 cm sphere | 1.592×10^-6 | C/m² |
| 04-04.6g | surface charge density, 10 cm sphere | 1.592×10^-7 | C/m² |
| 04-04.7a | equivalent capacitance | 5.2 | µF |
| 04-04.7b | charge on the series pair | 12 | µC |
| 04-04.7c | voltage on the 2 µF | 6 | V |
| 04-04.7d | voltage on the 3 µF | 4 | V |
| 04-04.7e | total energy | 260 | µJ |
| 04-04.8a | capacitance, layered | 70.83 | pF |
| 04-04.8b | field in the air | 8×10^4 | V/m |
| 04-04.8c | field in the slab | 2×10^4 | V/m |
| 04-04.8d | voltage across the air | 80 | V |
| 04-04.8e | voltage across the slab | 20 | V |
| 04-04.8f | capacitance, side by side | 110.7 | pF |
| 04-04.9a | cable capacitance per meter | 105.4 | pF/m |
| 04-04.9b | capacitance of 1.5 m | 158.2 | pF |
| 04-04.10a | energy density at 3 MV/m | 39.84 | J/m³ |
| 04-04.10b | sphere energy at 100 kV | 0.05563 | J |
| 04-04.11a | optimal inner radius | 1.839 | mm |
| 04-04.11b | maximum voltage | 5.518 | kV |
| 04-04.11c | maximum voltage with a = 0.5 mm | 3.454 | kV |
| 04-04.12a | droop, 100 µF | 10 | mV |
| 04-04.12b | droop, 90 µF | 11.11 | mV |
| 04-04.12c | droop, 60 µF | 16.67 | mV |
| 04-04.13a | HfO₂ thickness | 3.205 | nm |
| 04-04.13b | total physical thickness | 3.605 | nm |
| 04-04.13c | capacitance per area | 3.837 | µF/cm² |
| 04-04.14a | bit-line signal | 50 | mV |
| 04-04.14b | lowest readable cell voltage | 0.99 | V |
| 04-04.14c | allowed voltage loss | 0.11 | V |
| 04-04.14d | allowed charge loss | 0.88 | fC |
| 04-04.14e | allowed electrons lost | 5493 | — |
| 04-04.15a | force, no gap | 36.94 | N |
| 04-04.15b | force, 1 µm gap | 35.76 | N |
| 04-04.15c | force, 10 µm gap | 27.31 | N |
| 04-04.16a | sphere's field energy | 8.988×10^-6 | J |
| 04-04.16b | capacitance from energy | 5.563 | pF |
| 04-04.16c | fraction of energy within one radius | 0.5 | — |
