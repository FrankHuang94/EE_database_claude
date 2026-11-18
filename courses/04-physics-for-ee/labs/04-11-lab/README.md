# Lab 04-11 · Introduction to Solid-State Physics

**Chapter:** [04-11](../../chapters/04-11-intro-solid-state-physics.md) · **Notebook:** [04-11-solid-state.ipynb](04-11-solid-state.ipynb) · **Time:** about 75 minutes

## Objective

1. Derive the Fermi energy by counting states and see the formula emerge as the electron number grows.
2. Confirm Sommerfeld's electronic heat capacity by direct numerical integration.
3. Watch atomic levels grow into a band and extract an effective mass from its curvature.
4. Compute band structure for a periodic potential and compare the gap with the first-order estimate $2|U|$.
5. Compare intrinsic carrier concentrations across silicon, GaAs, GaN and 4H-SiC.

## Background

Chapter sections 3.2 to 3.6 and Examples 04-11.2 to 04-11.6; Problems 04-11.5 and 04-11.9. The notebook uses no random numbers. There is no ngspice netlist for this chapter (it has no circuit results).

## Procedure

1. Run all notebook cells in order, writing a prediction before each **🔮 Predict** cell.
2. **Part 1:** predict how many electrons a box needs before the counted Fermi level is within 1% of the formula.
3. **Part 2:** predict the heat capacity per electron at $T/T_F$ = 0.01.
4. **Part 3:** predict whether a 100-atom chain's band is narrower or wider than $4t$.
5. **Part 4:** predict whether the exact gap at $U$ = 0.5 eV is above or below $2U$.
6. **Part 5:** predict the temperature at which 4H-SiC's intrinsic concentration reaches $10^{14}$ cm⁻³.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | counted / formula Fermi level | 0.889, 0.957, 1.031, 1.004, 0.9994 for 10 to 100,000 electrons |
| 2 | heat capacity per electron at $T/T_F$ = 0.01 | 0.04933 k numerically, 0.04935 k from Sommerfeld; μ = 0.999918 $E_F$ |
| 3 | 100-atom chain, $t$ = 1 eV | width 3.998 eV; fitted $m^*$ = 0.6096 $m_0$ for $a$ = 0.25 nm |
| 4 | gap at π/a, $a$ = 0.5 nm | 0.1000, 0.3999, 0.9983, 1.986 eV for $U$ = 0.05, 0.2, 0.5, 1.0 eV |
| 5 | temperature for $n_i = 10^{14}$ cm⁻³ | 469.8 K for Si (fit); about 1,320 K for 4H-SiC (exponential model) |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 04-11.a | counted over formula Fermi level, 100,000 electrons | 0.9994 | — |
| Lab 04-11.b | numerical heat capacity per electron at T/T_F = 0.01 | 0.04933 | k |
| Lab 04-11.c | band width of a 100-atom chain | 3.998 | eV |
| Lab 04-11.d | exact gap at U = 0.5 eV | 0.9983 | eV |
| Lab 04-11.e | 4H-SiC temperature for n_i = 10^14 cm⁻³ (model) | 1324 | K |

## Discussion questions

1. Part 1's counted Fermi level jumps in steps instead of rising smoothly. What causes the steps, and why do they not matter for a real metal?
2. Part 2's numerical heat capacity falls slightly below the Sommerfeld formula at $T/T_F$ = 0.05. Why does the formula become less accurate as temperature rises, and should a copper engineer worry?
3. Part 3's band is slightly narrower than $4t$ for a finite chain. What does this suggest about the electronic structure of a nanoparticle a few nanometers across?
4. Part 5 gives every material the same prefactor. Why is that acceptable for comparing SiC with silicon, and when would it mislead you?

<details><summary>Answers to the discussion questions</summary>

1. Many wavevectors share the same $|\vec n|^2$ (for example all permutations and sign changes of (1, 2, 2)), so states come in degenerate shells, and the top filled level stays put until a whole shell fills. In a real metal there are $\sim10^{22}$ electrons and the shells are spaced by about $E_F/N^{2/3}$, far below $kT$, so the steps are invisible.
2. The Sommerfeld formula is the first term of an expansion in $T/T_F$; the next correction is of relative order $(T/T_F)^2$ times a coefficient, and a numerical derivative also picks it up. For copper at 300 K, $T/T_F \approx 0.004$, so the formula is accurate to better than 0.1%; the correction matters only for low-density electron systems such as doped semiconductors.
3. Its levels are discrete and its band edges pulled in, so its optical and electronic properties depend on size: quantum confinement (04-10) appearing in a band picture. This is why quantum dots of the same material emit different colors.
4. The prefactors differ by factors of a few, while the exponential differs by tens of orders of magnitude, so the comparison of which material reaches a given $n_i$ at what temperature is dominated by the gap. It would mislead when comparing materials with similar gaps (silicon against GaAs), where prefactor differences, the gap's temperature dependence and defect-assisted generation decide the outcome.

</details>

## Optional hardware version

Measure the leakage of a silicon diode's reverse current against temperature: reverse-bias a small-signal diode (for example 5 V through a 1 MΩ resistor), read the current with a picoammeter or by the voltage across the resistor, and warm the diode with a hair dryer while a thermocouple records its temperature. Plot $\ln I$ against $1/T$: the slope gives an activation energy, near $E_g$ if diffusion dominates or near $E_g/2$ if generation in the depletion region does. Stay below about 100 °C and keep the diode away from the dryer's element.
