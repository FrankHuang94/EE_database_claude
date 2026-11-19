# Solutions 09-05 · PN Junction Electrostatics

Problems: [09-05 problems](../problems/09-05-problems.md) · Chapter: [09-05](../chapters/09-05-pn-junction-electrostatics.md). Every number below is recomputed by [verify_09_05.py](../verify/verify_09_05.py): built-in potentials from flat-Fermi-level band positions, depletion quantities by integrating the charge numerically and root-finding the edges, capacitances by differentiating the depleted charge, and design questions by root finding.

---

## Solutions

### Solution 09-05.1

$V_{bi} = (kT/q)\ln(N_AN_D/n_i^2)$.

(a) $0.025852\ln(10^{33}/10^{20})$ = **0.7738** V.

(b) $0.025852\ln(10^{32}/10^{20})$ = **0.7143** V.

(c) $0.025852\ln(10^{34}/4.41\times10^{12})$ = **1.271** V.

(d) GaAs's wider gap gives it a far smaller $n_i$, so its Fermi levels sit much closer to the band edges for the same doping, and their difference is larger. The built-in potential still stays below the gap (1.42 eV).

### Solution 09-05.2

$W = \sqrt{2\varepsilon_sV_{bi}(2/10^{16})/q}$ = **0.4298** µm, split equally: $x_n$ = **0.2149** µm. Peak field $2V_{bi}/W$ = **3.324 × 10⁴** V/cm.

### Solution 09-05.3

$V_{bi} = 0.025852\ln(10^{34}/10^{20})$ = 0.8334 V. Full formula and one-sided approximation:

| $V_A$ | $W$ (full) | $W$ (one-sided) |
|---|---|---|
| 0 V | **1.0382** µm | **1.0381** µm |
| −1 V | **1.5398** µm | **1.5398** µm |
| −10 V | **3.743** µm | **3.743** µm |
| −100 V | **11.420** µm | **11.419** µm |

The one-sided formula is essentially exact (the p side holds 0.01% of the width). From −10 to −100 V, $W$ grows by $\sqrt{100.83/10.83}$ = **3.05**.

### Solution 09-05.4

(a) $V = \tfrac12|\mathcal E_{\max}|W$, so $|\mathcal E_{\max}| = 2 \times 1.2/0.5\times10^{-4}$ = **4.8 × 10⁴** V/cm.

(b) $x_n/x_p = N_A/N_D = 10$, so $x_n = W \times 10/11$ = **0.4545** µm and $x_p$ = **0.04545** µm.

(c) The field is a triangle: zero at $-x_p$, falling steeply (slope $qN_A/\varepsilon_s$) to $-4.8\times10^4$ V/cm at $x = 0$, then rising gently back to zero at $x_n$. The potential rises from the p side as two parabolic arcs joined at $x = 0$, with 1.091 V of the 1.2 V on the n side.

### Solution 09-05.5

The width condition is $\sqrt{2\varepsilon_s(V_{bi}(N_D) + 5)/(qN_D)} = 2$ µm with $V_{bi} = (kT/q)\ln(10^{19}N_D/n_i^2)$. Root finding gives $N_D$ = **1.892 × 10¹⁵** cm⁻³ (with $V_{bi}$ = **0.8498** V). A first guess ignoring $V_{bi}$, $2\varepsilon_s \times 5/(qW^2)$ = 1.62 × 10¹⁵ cm⁻³, would be **15**% low.

### Solution 09-05.6

$x_n$ = 0.3016 µm and $x_p$ = 30.16 nm (Example 09-05.2).

(a) On the n side the potential approaches its neutral value as a parabola: $V(x_n) - V(x) = qN_D(x_n - x)^2/2\varepsilon_s$. At $x = x_n/2$: **0.1759** V below the n-side neutral potential, a quarter of the n-side drop (0.7035 V), as a parabola requires.

(b) On the p side $|\mathcal E| = qN_A(x + x_p)/\varepsilon_s$; at $x = -x_p/2$: **2.332 × 10⁴** V/cm, half the peak.

### Solution 09-05.7

(a) $Q = qN_Dx_n$: **4.832 × 10⁻⁸** C/cm² at 0 V and **1.320 × 10⁻⁷** C/cm² at −5 V.

(b) $\varepsilon_s/W(-5\ \text{V})$ = **11.43** nF/cm²; a central difference of $Q$ over ±0.1 mV gives **11.43** nF/cm². They agree because the depleted charge changes only at the edges, which act like parallel plates $W$ apart. (At 0 V, $\varepsilon_s/W$ = **31.22** nF/cm².)

### Solution 09-05.8

| $N_D$ (cm⁻³) | $L_D$ | $W$ (zero bias) | $W/L_D$ |
|---|---|---|---|
| 10¹⁴ | **408.8** nm | **3.163** µm | **7.74** |
| 10¹⁶ | **40.88** nm | **0.3400** µm | **8.32** |
| 10¹⁸ | **4.088** nm | **0.03794** µm | **9.28** |

The ratio barely changes, because both $W$ and $L_D$ scale as $N^{-1/2}$; for a one-sided junction it grows only through the logarithmic $V_{bi}$ ($W/L_D = \sqrt{2qV_{bi}/kT}$), and at 10¹⁸ cm⁻³ the p side (only ten times more heavily doped) adds a little more width. The depletion approximation is equally good (a few percent, Example 09-05.5) at all doping levels at zero bias, and better under reverse bias.

### Solution 09-05.9

Solving $(2kT/q)\ln(aW/2n_i) = qaW^3/12\varepsilon_s$: $W$ = **0.1860** µm, $V_{bi}$ = **0.8296** V, edge doping $aW/2$ = **9.30 × 10¹⁶** cm⁻³, peak field $qaW^2/8\varepsilon_s$ = **6.690 × 10⁴** V/cm.

### Solution 09-05.10

(a) $1/C^2$ is **1.1538 × 10²³** F⁻² at −1 V and **2.9633 × 10²³** F⁻² at −4 V, so the slope is $(2.9633 - 1.1538)\times10^{23}/(-4 + 1)$ = **−6.032 × 10²²** F⁻² V⁻¹, and $N = -2/(q\varepsilon_sA^2\,\text{slope})$ = **2.00 × 10¹⁶** cm⁻³.

(b) Extrapolating to $1/C^2 = 0$: $V_A = -1 + 1.1538\times10^{23}/6.032\times10^{22}$ = **0.913** V, the built-in potential (the true value for a 10¹⁹/2 × 10¹⁶ cm⁻³ junction is 0.911 V; the difference comes from the four-digit data).

### Solution 09-05.11

(a) $N_D \le \varepsilon_s\mathcal E_c^2/(2qV_{br}) = 1.036\times10^{-12} \times 9\times10^{10}/(2 \times 1.602\times10^{-19} \times 200)$ = **1.45 × 10¹⁵** cm⁻³.

(b) $W = 2V_{br}/\mathcal E_c$ = **13.33** µm.

(c) $\mu_n$ = **1339** cm²/V·s at that doping, so $W/(q\mu N_D)$ = **4.27** mΩ·cm².

### Solution 09-05.12

(a) $V_{bi} = 0.025852\ln(10^{38}/10^{20})$ = **1.0715** V.

(b) $|\mathcal E| \approx (V_{bi} + 10)/2\ \mu\text{m}$ = **5.54 × 10⁴** V/cm, uniform; $C = \varepsilon_s/W_i$ = **5.18** nF/cm², independent of bias once the i-region is depleted.

(c) The P⁺N junction with 10¹⁵ cm⁻³ at −10 V has $W$ = 3.743 µm and **2.77** nF/cm²: smaller here, but its width and capacitance change with bias, and its field is concentrated at the junction. A PIN diode's wide, uniform-field region collects photocarriers by fast drift over its whole thickness and has a small, bias-independent capacitance: both make it fast.

### Solution 09-05.13

(a) $N = \varepsilon_s\mathcal E_c^2/(2qV_{br})$ and $W = 2V_{br}/\mathcal E_c$, so $R = W/(q\mu N) = (2V_{br}/\mathcal E_c) \cdot 2qV_{br}/(q\mu\varepsilon_s\mathcal E_c^2) = 4V_{br}^2/(\varepsilon_s\mu\mathcal E_c^3)$.

(b) $N$ = **4.85 × 10¹⁴** cm⁻³, $W$ = **40.0** µm, $\mu_n$ = **1352** cm²/V·s, $R$ = **38.07** mΩ·cm².

(c) $R \propto \mathcal E_c^{-3}$: a thousandfold reduction, to **0.0381** mΩ·cm² at the same voltage (before the different permittivity and mobility of a real wide-gap material are included).

### Solution 09-05.14

$V_{bi}$ = **0.8334** V, $W$ = **1.0381** µm (one-sided), and the corrected width is $W\sqrt{(V_{bi} - 2kT/q)/V_{bi}}$ = **1.0054** µm, a factor **0.968**. A 3% change matters for precise capacitance modeling but not for most design estimates.

### Solution 09-05.15

$\varepsilon_s = 12.9\varepsilon_0$, $V_{bi}$ = 1.271 V, so $W = \sqrt{2\varepsilon_sV_{bi}(2/10^{17})/q}$ = **0.1904** µm and $|\mathcal E_{\max}| = 2V_{bi}/W$ = **1.335 × 10⁵** V/cm. Silicon with the same doping has $V_{bi}$ = **0.8334** V and $W$ = **0.1468** µm: silicon's zero-bias peak field is $2 \times 0.8334/0.1468\times10^{-4}$ = **1.135 × 10⁵** V/cm. GaAs's larger built-in potential widens the region (its larger permittivity widens it slightly more) and raises the zero-bias field by a factor of only **1.18**: the field grows as $\sqrt{V_{bi}/\varepsilon_s}$, not in proportion to $V_{bi}$.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 09-05.1a | V_bi, 1e18/1e15 | 0.7738 | V |
| 09-05.1b | V_bi, 1e16/1e16 | 0.7143 | V |
| 09-05.1c | V_bi, GaAs 1e17/1e17 | 1.271 | V |
| 09-05.2a | W, symmetric 1e16 | 0.4298 | µm |
| 09-05.2b | x_n | 0.2149 | µm |
| 09-05.2c | peak field | 3.324e4 | V/cm |
| 09-05.3a | V_bi, 1e19/1e15 | 0.8334 | V |
| 09-05.3b | W at 0 V | 1.0382 | µm |
| 09-05.3c | one-sided W at 0 V | 1.0381 | µm |
| 09-05.3d | W at −1 V | 1.5398 | µm |
| 09-05.3e | one-sided W at −1 V | 1.5398 | µm |
| 09-05.3f | W at −10 V | 3.743 | µm |
| 09-05.3g | one-sided W at −10 V | 3.743 | µm |
| 09-05.3h | W at −100 V | 11.420 | µm |
| 09-05.3i | one-sided W at −100 V | 11.419 | µm |
| 09-05.3j | growth from −10 to −100 V | 3.05 | — |
| 09-05.4a | peak field | 4.8e4 | V/cm |
| 09-05.4b | x_n | 0.4545 | µm |
| 09-05.4c | x_p | 0.04545 | µm |
| 09-05.4d | potential on the n side | 1.091 | V |
| 09-05.5a | n-side doping | 1.892e15 | cm⁻³ |
| 09-05.5b | V_bi at that doping | 0.8498 | V |
| 09-05.5c | first guess ignoring V_bi | 1.62e15 | cm⁻³ |
| 09-05.5d | error of the first guess | 15 | % |
| 09-05.6a | potential at x_n/2 below the n side | 0.1759 | V |
| 09-05.6b | field at −x_p/2 | 2.332e4 | V/cm |
| 09-05.7a | charge per area at 0 V | 4.832e-8 | C/cm² |
| 09-05.7b | charge per area at −5 V | 1.320e-7 | C/cm² |
| 09-05.7c | ε/W at −5 V | 11.43 | nF/cm² |
| 09-05.7d | dQ/dV at −5 V | 11.43 | nF/cm² |
| 09-05.7e | ε/W at 0 V | 31.22 | nF/cm² |
| 09-05.8a | L_D at 1e14 | 408.8 | nm |
| 09-05.8b | W at 1e14 | 3.163 | µm |
| 09-05.8c | ratio at 1e14 | 7.74 | — |
| 09-05.8d | L_D at 1e16 | 40.88 | nm |
| 09-05.8e | W at 1e16 | 0.3400 | µm |
| 09-05.8f | ratio at 1e16 | 8.32 | — |
| 09-05.8g | L_D at 1e18 | 4.088 | nm |
| 09-05.8h | W at 1e18 | 0.03794 | µm |
| 09-05.8i | ratio at 1e18 | 9.28 | — |
| 09-05.9a | graded W | 0.1860 | µm |
| 09-05.9b | graded V_bi | 0.8296 | V |
| 09-05.9c | edge doping | 9.30e16 | cm⁻³ |
| 09-05.9d | peak field | 6.690e4 | V/cm |
| 09-05.10a | 1/C² at −1 V | 1.1538e23 | F⁻² |
| 09-05.10b | 1/C² at −4 V | 2.9633e23 | F⁻² |
| 09-05.10c | slope | -6.032e22 | F⁻² V⁻¹ |
| 09-05.10d | extracted doping | 2.00e16 | cm⁻³ |
| 09-05.10e | intercept (V_bi) | 0.913 | V |
| 09-05.10h | true V_bi of the test diode | 0.911 | V |
| 09-05.10f | C at −1 V | 2.944 | pF |
| 09-05.10g | C at −4 V | 1.837 | pF |
| 09-05.11a | maximum doping for 200 V | 1.45e15 | cm⁻³ |
| 09-05.11b | width at breakdown | 13.33 | µm |
| 09-05.11c | mobility | 1339 | cm²/V·s |
| 09-05.11d | resistance per area | 4.27 | mΩ·cm² |
| 09-05.12a | PIN V_bi | 1.0715 | V |
| 09-05.12b | field at −10 V | 5.54e4 | V/cm |
| 09-05.12c | PIN capacitance per area | 5.18 | nF/cm² |
| 09-05.12d | P+N capacitance at −10 V | 2.77 | nF/cm² |
| 09-05.13a | 600 V doping | 4.85e14 | cm⁻³ |
| 09-05.13b | 600 V width | 40.0 | µm |
| 09-05.13c | mobility | 1352 | cm²/V·s |
| 09-05.13d | resistance per area | 38.07 | mΩ·cm² |
| 09-05.13e | with tenfold critical field | 0.0381 | mΩ·cm² |
| 09-05.14a | V_bi | 0.8334 | V |
| 09-05.14b | W | 1.0381 | µm |
| 09-05.14c | corrected W | 1.0054 | µm |
| 09-05.14d | correction factor | 0.968 | — |
| 09-05.15a | GaAs W | 0.1904 | µm |
| 09-05.15b | GaAs peak field | 1.335e5 | V/cm |
| 09-05.15c | Si V_bi at 1e17/1e17 | 0.8334 | V |
| 09-05.15d | Si W at 1e17/1e17 | 0.1468 | µm |
| 09-05.15e | Si peak field at 1e17/1e17 | 1.135e5 | V/cm |
| 09-05.15f | GaAs to Si peak-field ratio | 1.18 | — |
