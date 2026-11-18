# Solutions 04-02 · Charge, Coulomb's Law and Electric Fields

Problems: [04-02 problems](../problems/04-02-problems.md) · Chapter: [04-02](../chapters/04-02-charge-coulomb-and-electric-fields.md). Every number below is recomputed by [verify_04_02.py](../verify/verify_04_02.py).

---

## Solutions

### Solution 04-02.1

(a) $10^{-6}/1.602176634\times10^{-19} = $ **6.242×10¹²** electrons.

(b) 1 mA for 1 s is 1 mC: **6.242×10¹⁵** electrons.

(c) $e/m_p = $ **9.579×10⁷ C/kg**; $e/m_e = $ **1.759×10¹¹ C/kg**. The electron responds to a field 1836 times more strongly.

### Solution 04-02.2

(a) $F = k_eq^2/r^2 = 8.988\times10^9\times(5\times10^{-9})^2/0.02^2 = $ **5.617×10⁻⁴ N**, repulsive (like charges).

(b) $r = \sqrt{k_eq^2/F} = \sqrt{8.988\times10^9\times25\times10^{-18}/10^{-6}} = $ **0.4740 m**.

### Solution 04-02.3

(a) $E = k_eq/r^2 = 8.988\times10^9\times4\times10^{-9}/0.03^2 = $ **3.994×10⁴ V/m**, pointing away from the charge.

(b) $F = eE = $ **6.400×10⁻¹⁵ N**; $a = F/m_e = $ **7.026×10¹⁵ m/s²**.

(c) Toward the positive charge, opposite to $\vec E$.

### Solution 04-02.4

Between the charges both fields point the same way (away from +2 nC, toward −8 nC, both in +$x$), so they cannot cancel. Outside, the null must lie closer to the smaller charge, to the left of +2 nC at $x = -s$: $2/s^2 = 8/(s + 6)^2$ gives $s + 6 = 2s$, so $s = 6$ cm. The null is at **x = −6 cm**.

### Solution 04-02.5

(a) **Zero**: the four equal charges are equidistant from the center, and their fields cancel in opposite pairs.

(b) Each adjacent charge pushes with $k_eq^2/a^2 = 8.988\times10^9\times10^{-18}/0.02^2 = 2.247\times10^{-5}$ N, the two at right angles, combining to $\sqrt2\times2.247\times10^{-5} = 3.178\times10^{-5}$ N along the diagonal. The diagonal charge, at $a\sqrt2$, pushes with $k_eq^2/(2a^2) = 1.123\times10^{-5}$ N along the same diagonal. Total: **4.301×10⁻⁵ N**, outward along the diagonal.

### Solution 04-02.6

(a) $E_z = k_eQz/(z^2 + R^2)^{3/2} = 8.988\times10^9\times10^{-8}\times0.05/(0.005)^{3/2} = $ **1.271×10⁴ V/m**.

(b) Differentiate: $\frac{d}{dz}\frac{z}{(z^2 + R^2)^{3/2}} = \frac{(z^2 + R^2) - 3z^2}{(z^2 + R^2)^{5/2}} = 0$ gives $z = R/\sqrt2 = $ **3.536 cm**, where $E_{\max} = 2k_eQ/(3\sqrt3R^2) = $ **1.384×10⁴ V/m**.

(c) Zero: at the center every piece of the ring is balanced by the piece opposite it.

### Solution 04-02.7

(a) Close to the middle of a large plate, use the sheet: $\sigma/(2\varepsilon_0) = 50\times10^{-9}/(2\times8.854\times10^{-12}) = $ **2824 V/m**.

(b) At 1 mm the plate (5 cm from center to edge) looks infinite. Treating it as a disk of equal area ($R = 10/\sqrt\pi = $ **5.642 cm**), the disk formula gives **2773 V/m** at 1 mm, only 1.8% below the sheet value, and falls 10% below it at $z = $ **5.670 mm**. Beyond a centimeter or so the plate's finite size matters, and far away it looks like a 0.5 nC point charge.

### Solution 04-02.8

(a) $\sigma = \varepsilon_0E = 8.854\times10^{-12}\times10^6 = $ **8.854×10⁻⁶ C/m²**.

(b) $\sigma\times10^{-4}$ m² = **0.8854 nC**.

### Solution 04-02.9

(a) $\tau_{\max} = pE = $ **3×10⁻²³ N·m**; the energy difference is $2pE = $ **6×10⁻²³ J**.

(b) $kT = 1.380649\times10^{-23}\times300 = $ **4.142×10⁻²¹ J**; $pE/kT = $ **0.007243**.

(c) Thermal agitation is over a hundred times stronger than the aligning energy, so the molecules align only slightly: the average alignment is of order $pE/(3kT)$, under a percent. This weak, temperature-dependent orientation is the origin of the permittivity of polar liquids ([04-04](../chapters/04-04-potential-capacitance-and-dielectrics.md)).

### Solution 04-02.10

(a) Exactly, $k_eq[1/0.0045^2 - 1/0.0055^2] = $ **1.467×10⁵ V/m**; $2k_ep/r^3 = $ **1.438×10⁵ V/m**; the approximation is **1.990%** low.

(b) Exactly, $k_ep/(r^2 + d^2/4)^{3/2} = $ **7.084×10⁴ V/m**; $k_ep/r^3 = $ **7.190×10⁴ V/m**, **1.504%** high.

(c) Both errors are of order $(d/r)^2$ = 4%. On the axis the exact field is the approximation times $1/(1 - d^2/4r^2)^2 \approx 1 + d^2/(2r^2)$ (a 2% correction); broadside it is the approximation times $(1 + d^2/4r^2)^{-3/2} \approx 1 - 3d^2/(8r^2)$ (1.5%). The broadside approximation is slightly better because its correction coefficient is smaller.

### Solution 04-02.11

(a) $v = \sqrt{2eV_a/m_e} = \sqrt{2\times1.602\times10^{-19}\times2000/9.109\times10^{-31}} = $ **2.652×10⁷ m/s**, so $v/c$ = **0.08847**. Relativity lowers the speed by about $\tfrac38(v/c)^2$ = 0.3% here, which we neglect.

(b) Field $E = 50/0.005 = 10^4$ V/m and $a = eE/m_e = 1.759\times10^{15}$ m/s². Time in the plates $t = 0.02/v = $ **0.7540 ns**. Deflection $\tfrac12at^2 = $ **0.5000 mm**. The exit angle has $\tan\theta = at/v = $ **0.05000**.

(c) $\tan\theta = \frac{(eV_d/(md))(L/v)}{v} = \frac{eV_dL}{mdv^2}$, and $mv^2 = 2eV_a$, so $\tan\theta = V_dL/(2V_ad) = 50\times0.02/(2\times2000\times0.005) = 0.05$ ✓. Charge and mass cancel: any particle accelerated through $V_a$ follows the same path, which is why ion and electron optics are designed in volts.

### Solution 04-02.12

(a) $K = eV = $ **10 keV** = **1.602×10⁻¹⁵ J**.

(b) $v = \sqrt{2K/m} = \sqrt{2\times1.602\times10^{-15}/(11\times1.6605\times10^{-27})} = $ **4.188×10⁵ m/s**.

(c) A doubly charged ion gains twice the energy from the same voltage ($K = qV$). The implant depth depends on the ion's energy, so tools specify energy, and choosing doubly charged ions doubles the reachable energy without a higher accelerating voltage.

### Solution 04-02.13

(a) With $L/2$ = 5 cm and $E(y) = \frac{\lambda}{2\pi\varepsilon_0y}\cdot\frac{L/2}{\sqrt{y^2 + (L/2)^2}}$:

| $y$ | exact | infinite line | point charge |
|---|---|---|---|
| 1 mm | **3.594×10⁴ V/m** | 3.595×10⁴ V/m | 1.798×10⁶ V/m |
| 5 cm | **508.4 V/m** | 719.0 V/m | 719.0 V/m |
| 1 m | **1.795 V/m** | 35.95 V/m | 1.798 V/m |

Close in, the infinite line is right; far out, the point charge is right; at $y = L/2$ both approximations give the same wrong answer, $\sqrt2$ times too high.

(b) The infinite-line formula is 10% high when $\sqrt{y^2 + (L/2)^2}/(L/2) = 1.1$, so $y = (L/2)\sqrt{1.21 - 1} = $ **2.291 cm**.

### Solution 04-02.14

(a) For $z \gg R$, $z/\sqrt{z^2 + R^2} = (1 + R^2/z^2)^{-1/2} \approx 1 - R^2/(2z^2)$, so $E \approx \frac{\sigma}{2\varepsilon_0}\cdot\frac{R^2}{2z^2} = \frac{\sigma\pi R^2}{4\pi\varepsilon_0z^2} = k_eQ/z^2$ ✓.

(b) $1 - z/\sqrt{z^2 + R^2} = 0.99$ gives $z/\sqrt{z^2 + R^2} = 0.01$, so $z/R = 0.01/\sqrt{1 - 0.0001} = $ **0.01000**: within a hundredth of its radius, a disk is 99% of an infinite sheet.

### Solution 04-02.15

(a) $E = V/t = 1.0/1.2\times10^{-9} = 8.333\times10^8$ V/m = **8.333 MV/cm**, already 83% of the breakdown field.

(b) **1.2 V**. In practice oxides run well below breakdown, because they wear out over years at fields far below the instantaneous limit.

(c) $\sigma = 3.9\times8.854\times10^{-12}\times8.333\times10^8 = $ **0.02878 C/m²**, or $0.02878/1.602\times10^{-19} = 1.796\times10^{17}$ per m² = **0.1796 electrons per nm²**: one electron per **5.568 nm²**. A gate a few tens of nanometers on a side carries only a few hundred electrons, so random fluctuations in their number and position are a real source of device variability.

### Solution 04-02.16

| | HBM (100 pF, 1.5 kΩ) | IEC 61000-4-2 (150 pF, 330 Ω) |
|---|---|---|
| Charge | **0.8 µC** | **1.2 µC** |
| Energy $\tfrac12CV^2$ | **3.2 mJ** | **4.8 mJ** |
| Peak current $V/R$ | **5.333 A** | **24.24 A** |
| Time constant $RC$ | **150 ns** | **49.5 ns** |

The system-level pulse delivers 4.5 times the current, half again the energy, and three times faster. On-chip protection sized for HBM cannot absorb it, which is why products add external protection (transient-voltage suppressors) at connectors, where users touch.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 04-02.1a | electrons in 1 µC | 6.242×10^12 | — |
| 04-02.1b | electrons in 1 mC | 6.242×10^15 | — |
| 04-02.1c | proton e/m | 9.579×10^7 | C/kg |
| 04-02.1d | electron e/m | 1.759×10^11 | C/kg |
| 04-02.2a | force between 5 nC charges | 5.617×10^-4 | N |
| 04-02.2b | separation for 1 µN | 0.4740 | m |
| 04-02.3a | field 3 cm from 4 nC | 3.994×10^4 | V/m |
| 04-02.3b | force on an electron | 6.400×10^-15 | N |
| 04-02.3c | electron acceleration | 7.026×10^15 | m/s² |
| 04-02.4a | null position | −6 | cm |
| 04-02.5a | field at the center | 0 | V/m |
| 04-02.5b | net force on a corner charge | 4.301×10^-5 | N |
| 04-02.6a | ring field at 5 cm | 1.271×10^4 | V/m |
| 04-02.6b | position of the maximum | 3.536 | cm |
| 04-02.6c | maximum field | 1.384×10^4 | V/m |
| 04-02.7a | sheet field | 2824 | V/m |
| 04-02.7b | equal-area disk radius | 5.642 | cm |
| 04-02.7c | disk field at 1 mm | 2773 | V/m |
| 04-02.7d | 10%-low distance | 5.670 | mm |
| 04-02.8a | surface charge for 1 MV/m | 8.854×10^-6 | C/m² |
| 04-02.8b | charge on 1 cm² | 0.8854 | nC |
| 04-02.9a | maximum torque | 3×10^-23 | N·m |
| 04-02.9b | energy difference | 6×10^-23 | J |
| 04-02.9c | kT at 300 K | 4.142×10^-21 | J |
| 04-02.9d | pE over kT | 0.007243 | — |
| 04-02.10a | exact axial field | 1.467×10^5 | V/m |
| 04-02.10b | approximate axial field | 1.438×10^5 | V/m |
| 04-02.10c | axial error | 1.990 | % |
| 04-02.10d | exact broadside field | 7.084×10^4 | V/m |
| 04-02.10e | approximate broadside field | 7.190×10^4 | V/m |
| 04-02.10f | broadside error | 1.504 | % |
| 04-02.11a | electron speed after 2 kV | 2.652×10^7 | m/s |
| 04-02.11b | v over c | 0.08847 | — |
| 04-02.11c | time in plates | 0.7540 | ns |
| 04-02.11d | deflection at exit | 0.5000 | mm |
| 04-02.11e | tangent of exit angle | 0.05000 | — |
| 04-02.11f | relativistic speed correction at 2 kV | 0.3 | % |
| 04-02.12a | ion energy | 1.602×10^-15 | J |
| 04-02.12b | ion speed | 4.188×10^5 | m/s |
| 04-02.13a | rod field at 1 mm | 3.594×10^4 | V/m |
| 04-02.13b | infinite-line field at 1 mm | 3.595×10^4 | V/m |
| 04-02.13c | rod field at 5 cm | 508.4 | V/m |
| 04-02.13d | approximations at 5 cm | 719.0 | V/m |
| 04-02.13e | rod field at 1 m | 1.795 | V/m |
| 04-02.13f | point-charge field at 1 m | 1.798 | V/m |
| 04-02.13g | infinite-line field at 1 m | 35.95 | V/m |
| 04-02.13h | point-charge field at 1 mm | 1.798×10^6 | V/m |
| 04-02.13i | 10%-high distance | 2.291 | cm |
| 04-02.14a | z/R for 1% below the sheet | 0.01000 | — |
| 04-02.15a | oxide field | 8.333 | MV/cm |
| 04-02.15b | voltage for 10 MV/cm | 1.2 | V |
| 04-02.15c | gate charge density | 0.02878 | C/m² |
| 04-02.15d | electrons per nm² | 0.1796 | — |
| 04-02.15e | area per electron | 5.568 | nm² |
| 04-02.16a | HBM charge | 0.8 | µC |
| 04-02.16b | IEC charge | 1.2 | µC |
| 04-02.16c | HBM energy | 3.2 | mJ |
| 04-02.16d | IEC energy | 4.8 | mJ |
| 04-02.16e | HBM peak current | 5.333 | A |
| 04-02.16f | IEC peak current | 24.24 | A |
| 04-02.16g | HBM time constant | 150 | ns |
| 04-02.16h | IEC time constant | 49.5 | ns |
