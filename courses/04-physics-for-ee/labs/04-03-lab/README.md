# Lab 04-03 · Gauss's Law

**Chapter:** [04-03](../../chapters/04-03-gauss-law.md) · **Notebook:** [04-03-gauss.ipynb](04-03-gauss.ipynb) · **Time:** about 60 minutes

## Objective

1. Confirm Gauss's law numerically by integrating Coulomb fields over closed surfaces, with charges inside and outside.
2. See that the law depends on the exact inverse-square force.
3. Rebuild the field of a uniformly charged sphere by brute-force superposition.
4. Watch mutually repelling charges in a conductor migrate to its surface.
5. Compute junction fields for arbitrary doping profiles, and explore how a touch sensor's signal scales.

## Background

Chapter sections 3.1 to 3.6 and Examples 04-03.2, 04-03.3, 04-03.6 and 04-03.7; Problem 04-03.16. Parts 3 and 4 use random starting points with seed 2026, so their results reproduce exactly.

## Procedure

1. Run all notebook cells in order, writing a prediction before each **🔮 Predict** cell.
2. **Part 1:** predict the flux through a 1 m cube for 1 nC inside it, and for 1 nC 10 cm outside one face.
3. **Part 2:** predict the flux ratio between 3 m and 1 m spheres if the force fell as $1/r^{2.05}$.
4. **Part 3:** predict where a 20,000-charge sum will scatter most from the Gauss's-law curve.
5. **Part 4:** predict where 60 repelling charges inside a sphere come to rest.
6. **Part 5:** predict the shape of a linearly graded junction's field, and the finger capacitance through 1 mm of plastic.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | flux through the 1 m cube | 112.9 V·m with the charge inside (anywhere); about 10⁻⁵ V·m, zero within grid error, with it outside |
| 2 | flux ratio, 3 m over 1 m, δ = 0.05 | 0.9466 (exactly 1 only for δ = 0) |
| 3 | 20,000 random charges | close to $k_eQ/r^2$ outside (9005 V/m against 8988 V/m at 10 cm); visible scatter about the straight line inside |
| 4 | 60 charges in a conducting sphere | all 60 end on the surface |
| 5 | junction peak fields | abrupt 46.40 kV/cm (Example 04-03.6); graded ($a = 10^{21}$ cm⁻⁴, $W$ = 0.5 µm) 48.33 kV/cm, with a parabolic profile |
| 5 | finger through 1 mm, $\varepsilon_r$ = 3 | 1.690 pF, about 5% of a 33 pF pad |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 04-03.a | flux, charge inside the cube | 112.9 | V·m |
| Lab 04-03.b | flux, charge outside the cube | 0 | V·m |
| Lab 04-03.c | flux ratio for δ = 0.05 | 0.9466 | — |
| Lab 04-03.d | graded-junction peak field | 48.33 | kV/cm |
| Lab 04-03.e | finger capacitance through 1 mm | 1.690 | pF |

## Discussion questions

1. Part 1 integrates over a cube, a surface on which the field is anything but constant, yet gets exactly $q/\varepsilon_0$. Why can you not then divide by the area to find the field?
2. Part 3's brute-force sum is noisy inside the sphere but smooth outside. A real charged object holds about $10^{10}$ or more elementary charges. Why does that make Gauss's law (which assumes a smooth density) accurate, and where might granularity still matter in a chip?
3. Part 4's charges reach the surface of a sphere. In a real metal, what stops the surface charge from leaving the metal entirely, and what happens when the field gets strong enough to overcome that?
4. Part 5 shows a touch signal falling as $1/d$. A product designer wants a 3 mm glass front instead of 1 mm plastic. Using $C_F\propto\varepsilon_r/d$, is the signal better or worse, and by how much?

<details><summary>Answers to the discussion questions</summary>

1. Gauss's law fixes only the surface integral, $\oint\vec E\cdot\hat n\,dA$. On a cube the normal field varies from point to point (strongest at the face centers nearest the charge), so the total flux does not determine the field at any one point. Dividing by the area gives only the average normal field over the surface.
2. The relative fluctuation of a sum of $N$ random contributions falls as $1/\sqrt N$ (Course 03), so with $10^{10}$ charges the granular noise is about $10^{-5}$ of the field, invisible next to the smooth result. Granularity matters where the number of charges is small: the roughly hundred electrons under a nanoscale gate (Problem 04-03.13) or the few dopant atoms in a tiny transistor channel, whose random number and placement cause device-to-device variation (Course 09).
3. Each electron is bound to the metal by its work function, a few electron-volts of energy. If the surface field becomes enormous (of order $10^9$ V/m and above, typically at sharp tips), electrons tunnel out: field emission, the principle of field-emission electron sources. Long before that, in air, the surrounding gas breaks down and the conductor discharges by sparking or corona (§3.4).
4. Slightly worse: $C_F$ scales as $\varepsilon_r/d$, so glass with $\varepsilon_r$ = 7 at 3 mm gives $(7/3)/(3/1) = 0.78$ of the plastic's signal at 1 mm. Only about 22% less signal for a cover three times thicker, which is why glass fronts work well for touch.

</details>

## Optional hardware version

Many microcontroller evaluation boards include capacitive touch buttons and free software that displays the raw sensor count. Place sheets of paper, plastic or glass of known thickness over a button and record the change in count when you touch it; plot the change against $1/d$. Then tape a grounded strip of aluminum foil near the button and see how a nearby ground conductor steals field lines and changes both the baseline and the touch signal.
