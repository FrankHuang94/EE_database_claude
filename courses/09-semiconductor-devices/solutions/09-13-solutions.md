# Solutions 09-13 · Compound and Wide-Bandgap Semiconductors

Problems: [09-13 problems](../problems/09-13-problems.md) · Chapter: [09-13](../chapters/09-13-compound-and-wide-bandgap-semiconductors.md). Every number below is recomputed by [verify_09_13.py](../verify/verify_09_13.py), by these routes:

- breakdown designs by integrating the carrier-continuity equations with avalanche generation;
- polarization from the elastic and piezoelectric tensors;
- die counts by the formula, cross-checked by counting;
- everything else by direct evaluation or root finding.

---

## Solutions

### Solution 09-13.1

$e^{-(3.435 - 1.12)/(2 \times 0.025852)}$ = **3.59 × 10⁻²⁰**. GaN, like SiC, has essentially no thermally generated carriers at room temperature.

### Solution 09-13.2

$E_g(T) = 3.507 - 0.909\times10^{-3}\,T^2/(T + 830)$:

- **3.389** eV at 400 K;
- **3.501** eV at 77 K.

From 300 K to 400 K the gap shrinks by **45.8** meV.

### Solution 09-13.3

$N_D = \varepsilon_s\mathcal E_c^2/2qV_B$ = **5.21 × 10¹⁵** cm⁻³ and $W = 2V_B/\mathcal E_c$ = **26.4** µm, so $R_{on,sp} = W/q\mu N_D$ = **3.16** mΩ·cm². Baliga's formula $4V_B^2/\varepsilon_s\mu\mathcal E_c^3$ gives the same **3.16** mΩ·cm², as it must, since it is the same algebra.

### Solution 09-13.4

| | $N_D$ (cm⁻³) | $\mathcal E_c$ (V/cm) | $W$ (µm) | $\mu_n$ | $R_{on,sp}$ (mΩ·cm²) |
|---|---|---|---|---|---|
| Si | **2.89 × 10¹⁴** | **2.41 × 10⁵** | **53.9** | **1355** | **86.0** |
| 4H-SiC | **3.91 × 10¹⁶** | **3.04 × 10⁶** | **4.28** | 1000 | **0.0683** |

The ratio is **1259**, slightly less than at 1200 V.

### Solution 09-13.5

$n = \ln(R_{1200}/R_{650})/\ln(1200/650)$: **2.33** for SiC and **2.49** for Si. At a fixed critical field, $R_{on,sp} \propto V_B^2$. But the critical field falls as the doping falls (thicker, lighter drift layers break down at lower peak fields, because the ionization integral runs over a longer distance), and $R_{on,sp} \propto 1/\mathcal E_c^3$ amplifies that decline. This is why the silicon disadvantage grows with voltage.

### Solution 09-13.6

For $x$ = 0.15, with the same interpolation as Example 09-13.4, the bound charge is **0.0132** C/m², a sheet density of **8.21 × 10¹²** cm⁻²: about 60% of the $x$ = 0.25 value. Both polarizations grow with aluminum content.

### Solution 09-13.7

$I/W = qn_sv$ = 1.602 × 10⁻¹⁹ × 10¹³ × 10⁷ = **16.0** A/cm = **1.60** A/mm. A real HEMT delivers less, because the density under the gate falls at high current and the velocity is not uniform.

### Solution 09-13.8

$\Delta E_g = kT\ln 100$ = **0.119** eV at 300 K and **0.159** eV at 400 K. The gain advantage of a fixed heterojunction shrinks as the device heats.

### Solution 09-13.9

$e^{-3.26/(2kT_{600})}/e^{-1.12/(2kT_{300})}$ = **5.20 × 10⁻⁵**: even at 600 K, 4H-SiC has fewer intrinsic carriers than silicon at room temperature (ignoring the prefactors).

### Solution 09-13.10

| Die area | 200 mm | 300 mm | ratio |
|---|---|---|---|
| 25 mm² | **1168** | **2694** | **2.31** |
| 100 mm² | **270** | **640** | **2.37** |

Both ratios exceed the area ratio of 2.25, and the larger die gains more, because edge loss scales with the circumference divided by the die diagonal, and a large die loses relatively more at the edge of a small wafer.

### Solution 09-13.11

$C_b = \varepsilon/d$ = 9 × 8.854 × 10⁻¹⁴/(20 × 10⁻⁷) = **3.98 × 10⁻⁷** F/cm², so $\Delta n_s/\Delta V = C_b/q$ = **2.49 × 10¹²** cm⁻² per volt. Emptying 1.39 × 10¹³ cm⁻² takes about **5.59** V, so the threshold is near −5.6 V: the device is normally on, and must be held at a negative gate voltage to turn it off.

### Solution 09-13.12

Cost per die scales as wafer cost over dies per wafer: (1.4/1168)/(1.0/640) = **0.768**, a 23% saving at equal yield. With yields of 70% and 85%: (1.4/(1168 × 0.70))/(1.0/(640 × 0.85)) = **0.932**: most of the saving disappears. The break-even 200 mm yield is 1.4 × 640 × 0.85/1168 = **65.2**%. Wafer-size transitions pay only once yields mature, which is why they take years.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 09-13.1a | n_i ratio GaN/Si | 3.59e-20 | — |
| 09-13.2a | GaN gap at 400 K | 3.389 | eV |
| 09-13.2b | GaN gap at 77 K | 3.501 | eV |
| 09-13.2c | shift 300 to 400 K | 45.8 | meV |
| 09-13.3a | drift doping | 5.21e15 | cm⁻³ |
| 09-13.3b | drift thickness | 26.4 | µm |
| 09-13.3c | R_on,sp | 3.16 | mΩ·cm² |
| 09-13.4a | Si doping | 2.89e14 | cm⁻³ |
| 09-13.4b | Si critical field | 2.41e5 | V/cm |
| 09-13.4c | Si thickness | 53.9 | µm |
| 09-13.4d | Si mobility | 1355 | cm²/V·s |
| 09-13.4e | Si R_on,sp | 86.0 | mΩ·cm² |
| 09-13.4f | SiC doping | 3.91e16 | cm⁻³ |
| 09-13.4g | SiC critical field | 3.04e6 | V/cm |
| 09-13.4h | SiC thickness | 4.28 | µm |
| 09-13.4i | SiC R_on,sp | 0.0683 | mΩ·cm² |
| 09-13.4j | ratio | 1259 | — |
| 09-13.5a | exponent, SiC | 2.33 | — |
| 09-13.5b | exponent, Si | 2.49 | — |
| 09-13.6a | bound charge, x = 0.15 | 0.0132 | C/m² |
| 09-13.6b | sheet density, x = 0.15 | 8.21e12 | cm⁻² |
| 09-13.7a | current per cm | 16.0 | A/cm |
| 09-13.7b | current per mm | 1.60 | A/mm |
| 09-13.8a | gap difference, 300 K | 0.119 | eV |
| 09-13.8b | gap difference, 400 K | 0.159 | eV |
| 09-13.9a | n_i ratio, SiC 600 K to Si 300 K | 5.20e-5 | — |
| 09-13.10a | dies, 200 mm, 25 mm² | 1168 | — |
| 09-13.10b | dies, 300 mm, 25 mm² | 2694 | — |
| 09-13.10c | ratio, 25 mm² | 2.31 | — |
| 09-13.10d | dies, 200 mm, 100 mm² | 270 | — |
| 09-13.10e | dies, 300 mm, 100 mm² | 640 | — |
| 09-13.10f | ratio, 100 mm² | 2.37 | — |
| 09-13.11a | barrier capacitance | 3.98e-7 | F/cm² |
| 09-13.11b | density change per volt | 2.49e12 | cm⁻² |
| 09-13.11c | voltage to empty the channel | 5.59 | V |
| 09-13.12a | cost-per-die ratio, equal yield | 0.768 | — |
| 09-13.12b | cost per good die ratio | 0.932 | — |
| 09-13.12c | break-even yield | 65.2 | % |
