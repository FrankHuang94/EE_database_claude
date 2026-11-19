# Lab 09-03 · Carrier Transport: Drift and Diffusion

**Chapter:** [09-03](../../chapters/09-03-drift-and-diffusion.md) · **Notebook:** [09-03-transport.ipynb](09-03-transport.ipynb) · **Time:** about 2 hours

## Objective

1. Recover $\mu = q\tau/m^*$ from a simulated ensemble of electrons with random collisions.
2. Recover Fick's law and the diffusion coefficient from a simulated random walk, and see the Einstein ratio survive a change in scattering time.
3. Compute the sheet resistance of an implanted (non-uniform) layer by integrating slice conductances.
4. Compute transit times across channels of different lengths from the velocity–field fits.
5. Confirm that a graded doping profile in equilibrium builds a field that cancels diffusion point by point.

## Background

Chapter sections 3.1–3.8 and Examples 09-03.1 to 09-03.7. The ensemble in Part 1 uses free-flight times drawn from an exponential distribution with mean $\tau$ (a Poisson collision process, 03-02); averaging the velocity over time weights each flight by its duration. You need Python with NumPy, SciPy and Matplotlib (see [SETUP.md](../../../../SETUP.md)).

## Files

| File | What it does | Checks against |
|---|---|---|
| [09-03-transport.ipynb](09-03-transport.ipynb) | The guided notebook (Parts 1 to 5) | Its own `assert`s and the answer key below |

## Procedure

1. **Drift from collisions (Part 1, the chapter's guided exercise).** *Predict first:* halving $\tau$ does what to the drift velocity, the mobility and the diffusion coefficient? Then run the ensemble for $\tau$ and $\tau/2$.
2. **Diffusion from a random walk (Part 2).** *Predict first:* if the free time halves at the same thermal speed (so $\lambda$ halves too), by what factor does $D = \lambda^2/2\tau$ change? Then simulate.
3. **An implanted layer (Part 3).** *Predict first:* a dose of 10¹⁴ cm⁻² spread with $\sigma$ = 50 nm or 100 nm: which has the lower sheet resistance, and by roughly how much? Then integrate.
4. **Transit times (Part 4).** *Predict first:* the transit time for 1 V across 30 nm, for electrons and holes. Then compute.
5. **Built-in field (Part 5).** *Predict first:* the field of an exponential profile with a 0.5 µm decay length. Then check that drift and diffusion cancel.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | mobility from the ensemble | about 1345 cm²/V·s for $\tau$ = 0.199 ps; half that for $\tau/2$ |
| 2 | random walk | $D = \lambda^2/2\tau$ to within the sampling error; halves with $\tau$ at fixed speed |
| 3 | implanted layer | see the answer key |
| 4 | transit at 10⁵ V/cm | electrons at 95.5% of $v_s$ |
| 5 | graded profile | field $(kT/q)/L$ = 517 V/cm; drift and diffusion cancel everywhere |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 09-03.a | peak doping, σ = 50 nm | 1.596e19 | cm⁻³ |
| Lab 09-03.b | sheet resistance, σ = 50 nm | 498.7 | Ω/□ |
| Lab 09-03.c | peak doping, σ = 100 nm | 7.98e18 | cm⁻³ |
| Lab 09-03.d | sheet resistance, σ = 100 nm | 416.1 | Ω/□ |
| Lab 09-03.e | ratio | 1.199 | — |
| Lab 09-03.f | electron fraction of v_s at 1e5 V/cm | 95.5 | % |
| Lab 09-03.g | built-in field, L = 0.5 µm | 517 | V/cm |

## Discussion questions

1. In Part 1, why must the velocity be averaged over time (weighting each flight by its duration) rather than over flights?
2. Why does halving $\tau$ at fixed thermal speed halve both $\mu$ and $D$, and what does that say about the Einstein relation?
3. In Part 3, why does a deeper, lower-peak implant of the same dose have a lower sheet resistance? Would the conclusion hold if all carriers had the same mobility?
4. In Part 4, why do short channels shrink the electron–hole speed difference?
5. In Part 5, both the drift and the diffusion currents are large. Why is the measured current zero, and what would make it non-zero?

<details><summary>Answers to the discussion questions</summary>

1. The drift velocity is the average velocity of the population at a random instant. A random instant is more likely to fall inside a long flight than a short one, in proportion to its length, so each flight's average velocity must be weighted by its duration. An unweighted average over flights underestimates $v_d$ by a factor of two for exponential flights.
2. $\mu = q\tau/m^*$ is proportional to $\tau$, and $D = v_{th}^2\tau/3$ (or $\lambda^2/2\tau$ with $\lambda = v_{th}\tau$) is also proportional to $\tau$, so their ratio does not depend on scattering at all: $D/\mu = m^*v_{th}^2/(3q) = kT/q$, set only by temperature. That is the content of the Einstein relation.
3. Sheet conductance is $q\int\mu N\,dx$, and the dose $\int N\,dx$ is fixed, so only the dose-weighted average mobility matters. Spreading the dose lowers the doping everywhere and raises the mobility (less impurity scattering): the 100 nm layer's resistance is lower by a factor of **1.199**. With a constant mobility the two would be identical.
4. At high fields both carriers approach their saturation velocities, which differ by only about 30% (1.07 × 10⁷ against 8.3 × 10⁶ cm/s), while their low-field mobilities differ about threefold. Short channels push both carriers into saturation.
5. In equilibrium the built-in field exists *because* of the gradient, and the drift it drives is exactly equal and opposite to the diffusion: the Fermi level is flat. A current flows only if something tilts the Fermi level: an applied voltage, light that creates extra carriers, or a temperature gradient.

</details>

## Optional extension

Replace the constant field of Part 1 with a field that switches on at $t = 0$, and plot the ensemble's average velocity against time. Confirm that the drift velocity approaches its steady value with time constant $\tau$, and estimate the frequency up to which mobility is a constant (about $1/(2\pi\tau)$).
