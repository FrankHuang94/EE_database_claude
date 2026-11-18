# Lab 04-10 · Introduction to Quantum Mechanics

**Chapter:** [04-10](../../chapters/04-10-intro-quantum-mechanics.md) · **Notebook:** [04-10-quantum.ipynb](04-10-quantum.ipynb) · **Time:** about 75 minutes

## Objective

1. Solve the Schrödinger equation numerically as a matrix eigenvalue problem for infinite and finite wells.
2. Compute tunneling through rectangular and field-tilted barriers by matching boundary conditions.
3. Watch a wavepacket split at a barrier, with total probability conserved.
4. Recover Planck's constant from photoelectric stopping voltages.
5. See measurement statistics of a qubit emerge from sampling.

## Background

Chapter sections 3.1 to 3.5 and Examples 04-10.5 and 04-10.7; Problems 04-10.3 and 04-10.13. Part 5 uses random numbers with seed 2026, so its results reproduce exactly. There is no ngspice netlist for this chapter (it has no circuit results).

## Procedure

1. Run all notebook cells in order, writing a prediction before each **🔮 Predict** cell.
2. **Part 1:** predict the number of bound states in a 1 eV-deep, 2 nm-wide well.
3. **Part 2:** predict whether the step-matrix method matches the exact formula, and how a tilted barrier's transmission depends on field.
4. **Part 3:** predict the fraction of a 0.5 eV packet that tunnels through a 1 eV, 0.5 nm barrier.
5. **Part 4:** predict how close a two-point fit gets to $h$.
6. **Part 5:** predict the spread in the count of 1s in 1000 shots.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | infinite well, 1 nm | 0.3757, 1.503, 3.381, 6.011 eV against the formula's 0.3760, 1.504, 3.384, 6.016 eV |
| 1 | finite well, 1 eV deep, 2 nm wide | 4 bound states; ground state 0.06554 eV (exact 0.06557 eV) |
| 2 | rectangular barrier, 1 eV electron, 3.1 eV | 1.245×10⁻⁶ at 1.0 nm and 6.388×10⁻⁸ at 1.2 nm, matching the exact formula |
| 2 | tilted barrier, 0.5 m₀ | about 4×10⁻¹⁶ at 7 MV/cm and 8×10⁻¹² at 10 MV/cm |
| 3 | wavepacket | about 10% transmitted, close to the plane-wave 0.1014; total probability 1.000000 |
| 4 | photoelectric fit | h = 6.630×10⁻³⁴ J·s |
| 5 | 1000 shots at P(1) = 0.75 | mean 749.7, standard deviation 13.9 over 2000 repeats (theory 750 and 13.69) |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 04-10.a | bound states in the finite well | 4 | — |
| Lab 04-10.b | finite-well ground state | 65.57 | meV |
| Lab 04-10.c | transmission through 1.0 nm | 1.245×10^-6 | — |
| Lab 04-10.d | plane-wave transmission at 0.5 eV through 1 eV, 0.5 nm | 0.1014 | — |
| Lab 04-10.e | Planck's constant from the fit | 6.630×10^-34 | J·s |

## Discussion questions

1. Part 1's finite-well levels lie below the infinite-well ones. Why, and what does this imply for quantum-well lasers designed with the simple infinite-well formula?
2. Part 2's tilted-barrier transmission rises by about four orders of magnitude between 7 and 10 MV/cm. Why is that steepness both useful and dangerous for flash memory?
3. Part 3 conserves total probability exactly. Physically, what does it mean that the packet is "partly transmitted and partly reflected" before any detector clicks?
4. Part 5's counts scatter by about ±14 around 750. A quantum algorithm needs to distinguish two outcomes with probabilities 0.50 and 0.52. Roughly how many shots does it need?

<details><summary>Answers to the discussion questions</summary>

1. The wavefunction leaks into the finite walls, so the effective width is larger than the well and every level drops; the effect is strongest for the higher levels, closest to the top of the well. An infinite-well estimate overestimates transition energies, so real designs solve the finite (or full band-structure) problem, then calibrate against measured emission.
2. Useful: a modest program voltage moves charge quickly (a large current at high field) while the same oxide holds charge for years at low field (a tiny current), giving both fast writes and long retention. Dangerous: small variations in oxide thickness or trapped charge change the local field and the current enormously, so cell-to-cell variation is large; repeated stress creates traps that let charge leak at low fields, limiting endurance.
3. The electron is in a superposition of a transmitted and a reflected wavepacket. Neither is "where the electron really is"; a detector on one side finds it there with probability equal to that packet's share of $|\psi|^2$, and finds it only once. This is exactly how a beam of many electrons gives the transmitted current fraction $T$.
4. The difference of 0.02 must exceed a few standard deviations of the estimate, $\sqrt{p(1-p)/N} \approx 0.5/\sqrt N$. For 3σ, $0.02 \gtrsim 3\times0.5/\sqrt N$, so $N \gtrsim 5600$ shots. Sampling cost grows as the inverse square of the effect size, a real overhead for quantum algorithms.

</details>

## Optional hardware version

A simple photoelectric-style experiment uses LEDs: an LED starts to conduct (and glow) at a forward voltage close to its photon energy divided by $e$. Measure the turn-on voltage of red, green and blue LEDs (with a series resistor and a variable supply) and plot it against $1/\lambda$ from the datasheets; the slope estimates $hc/e$. (LED turn-on voltages include other drops, so expect agreement within 10–20%.)
