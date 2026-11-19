# Lab 09-13 · Compound and Wide-Bandgap Semiconductors

**Chapter:** [09-13](../../chapters/09-13-compound-and-wide-bandgap-semiconductors.md) · **Notebook:** [09-13-wide-bandgap.ipynb](09-13-wide-bandgap.ipynb) · **Time:** about 2 hours

## Objective

1. Compute avalanche breakdown against doping for silicon and 4H-SiC from the ionization integral, and design drift layers for 600 V to 3300 V.
2. Plot Baliga's on-resistance limit against blocking voltage and see how the SiC advantage changes with voltage.
3. Compute the AlGaN/GaN polarization charge against aluminum content.
4. Compare the sheet resistance of a 2DEG with that of a doped layer.
5. Count dies on 150, 200 and 300 mm wafers and compare with the edge-loss estimate.

## Background

Chapter sections 3.1–3.6 and Examples 09-13.1 to 09-13.7. Silicon ionization uses the handbook fits of 09-06; 4H-SiC uses Hatakeyama's c-axis fits as tabulated by Burin et al., with $\varepsilon_r$ = 9.96 and $\mu_n$ = 1000 cm²/V·s. The breakdown condition is the ionization integral $\int_0^W\alpha_n\exp[-\int_0^x(\alpha_n - \alpha_p)dx']dx = 1$ over a triangular field. The GaN and AlN constants are Vurgaftman's Table X values. There is no ngspice file: compact models for SiC and GaN power devices come from their manufacturers. You need Python with NumPy, SciPy and Matplotlib (see [SETUP.md](../../../../SETUP.md)).

## Files

| File | What it does | Checks against |
|---|---|---|
| [09-13-wide-bandgap.ipynb](09-13-wide-bandgap.ipynb) | The guided notebook (Parts 1 to 5) | Its own `assert`s, which compare with the chapter's examples and the answer key below |

## Procedure

1. **Breakdown against doping (Part 1).** *Predict first:* at equal doping, how many times higher is SiC's breakdown voltage? Then sweep doping from 10¹⁴ to 10¹⁷ cm⁻³.
2. **Baliga's limit (Part 2, the chapter's guided exercise).** *Predict first:* at 600 V and at 3300 V, does SiC's on-resistance advantage grow, shrink or stay the same? Then design both and compute the ratios.
3. **Polarization (Part 3).** *Predict first:* is the sheet density linear in aluminum content? Then compute it from 0 to 0.4.
4. **Modulation doping (Part 4).** Compare 2DEG and doped-silicon sheet resistance for densities from 10¹² to 10¹⁴ cm⁻².
5. **Wafers (Part 5).** Count whole dies on a grid inside each wafer and compare with the edge-loss formula.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Breakdown at 10¹⁶ cm⁻³ | 55.6 V (Si), 1996 V (SiC) (Example 09-13.2) |
| 2 | On-resistance ratio at 1200 V | 1386 (Example 09-13.3) |
| 2 | Ratios at 600 V and 3300 V; SiC critical field at 3300 V | see the answer key |
| 3 | Sheet density at $x$ = 0.25 and 0.35 | 1.39 × 10¹³ cm⁻² (Example 09-13.4); see the answer key |
| 5 | Counted dies against the formula | within a few percent |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 09-13.a | Si/SiC on-resistance ratio at 600 V | 1242 | — |
| Lab 09-13.b | Si/SiC on-resistance ratio at 3300 V | 1585 | — |
| Lab 09-13.c | SiC critical field at 3300 V | 2.56e6 | V/cm |
| Lab 09-13.d | sheet density at x = 0.35 | 1.99e13 | cm⁻² |

## Discussion questions

1. Why does SiC's advantage grow with blocking voltage?
2. Why is the polarization sheet density not exactly linear in aluminum content?
3. Why does the edge-loss formula overestimate or underestimate the count, depending on die size?
4. Which of the chapter's parameters are least certain, and how would that uncertainty change the conclusions?

<details><summary>Answers to the discussion questions</summary>

1. The on-resistance ratio rises from **1242** at 600 V to **1586** at 3300 V because both critical fields fall as doping falls, and silicon's falls faster in proportion. At 3300 V SiC still holds **2.56 × 10⁶** V/cm. Since $R_{on,sp} \propto 1/\mathcal E_c^3$, the gap widens.
2. The spontaneous part is linear in $x$ by assumption, but the piezoelectric part is a product of the strain (which grows with $x$) and interpolated coefficients (which also vary with $x$), so the total bends upward slightly: **1.99 × 10¹³** cm⁻² at $x$ = 0.35 against 1.39 × 10¹³ at 0.25.
3. The formula subtracts one die per die diagonal of circumference, a smooth average. The actual count depends on how the grid aligns with the edge, which matters more for large dies; the best grid offset usually beats the formula slightly for small dies.
4. The SiC ionization coefficients (fits differ noticeably), the SiC mobility (doping- and direction-dependent) and GaN's spontaneous polarization (calculations differ by more than a factor of two) are the least certain. They change the numbers by tens of percent, not the conclusions: the on-resistance advantage stays in the hundreds to thousands, and the 2DEG density stays near 10¹³ cm⁻².

</details>

## Optional extension

Add a punch-through drift layer: fix the thickness below the triangular value and solve for the doping that still blocks the target voltage. Find the thickness that minimizes $R_{on,sp}$ for SiC at 1200 V, and compare with the triangular design.
