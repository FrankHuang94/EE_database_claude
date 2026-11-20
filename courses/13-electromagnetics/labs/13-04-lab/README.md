# Lab 13-04 · Maxwell's Equations and Time-Varying Fields

Chapter: [13-04 Maxwell's Equations and Time-Varying Fields](../../chapters/13-04-maxwells-equations.md)

## Objective

Solve Maxwell's two curl equations directly on a grid and watch electromagnetic waves emerge at the speed of light; measure the grid's numerical dispersion; see a pulse reflect from a conductor; check the Poynting theorem for a resistive wire; and map which materials conduct and which insulate at each frequency. Then confirm in ngspice that a capacitor's lead current is its displacement current.

## Background

Faraday's law and the displacement current (§3.1–3.2), conductors against dielectrics (§3.4), the wave equation (§3.5) and the Poynting theorem (§3.6).

## Files

- [13-04-maxwell.ipynb](13-04-maxwell.ipynb): the notebook (Parts 1–4).
- [displacement.cir](displacement.cir): Example 13-04.2's 35.42 pF capacitor driven with 1 V at 1 GHz (AC analysis). Run with `ngspice -b displacement.cir`, or `python tools/run_spice.py 13-04` from the repository root.

## Procedure

1. **FDTD (Part 1).** Start a Gaussian pulse of $E_z$ at rest and run 600 steps at a Courant number of 0.5. *Predict first:* where are the pulses, and how tall?
2. **Numerical dispersion (Part 2).** Drive a sinusoid at 10, 20 and 40 cells per wavelength, at Courant numbers 0.5 and 1, and measure the phase velocity from the phase advance across 500 cells. Compare with the Yee dispersion relation.
3. **A conducting slab (Part 3).** Launch a one-way pulse into a weak and a strong conductor and record the reflected and transmitted peaks.
4. **Poynting and σ/ωε (Part 4).** Integrate the Poynting vector over the surface of Example 13-04.5's wire, then plot $\sigma/\omega\varepsilon$ against frequency for copper, seawater, doped and intrinsic silicon and a lossy laminate.
5. **ngspice (the chapter's guided exercise).** Predict the capacitor current's amplitude and phase, then run `displacement.cir`.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Pulses | Two half-height pulses moving apart at one cell per two steps: the speed of light |
| 2 | Phase velocity | Slightly below $c$ at $S$ = 0.5, more so with fewer cells per wavelength; exactly $c$ at $S$ = 1 |
| 3 | Conductor | Weak: small inverted reflection and an attenuated transmitted pulse. Strong: most of the pulse reflected, inverted, nothing through |
| 4 | Poynting | The surface inflow equals $I^2R$; each material's ratio crosses 1 at $1/(2\pi\tau_r)$ |
| ngspice | Capacitor current | 0.2225 A, leading the voltage by 90° |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 13-04.a | FDTD phase velocity, 20 cells per wavelength, S = 0.5 | 0.9969 | c |
| Lab 13-04.b | FDTD phase velocity, 10 cells per wavelength, S = 0.5 | 0.9876 | c |
| Lab 13-04.c | FDTD phase velocity at S = 1 | 1.0000 | c |

*These are recomputed by [verify_13_04.py](../../verify/verify_13_04.py) from the Yee dispersion relation and confirmed by running its own one-dimensional FDTD grid.*

## Discussion questions

1. The code updates $H$ from the spatial difference of $E$ and then $E$ from that of $H$. Which of Maxwell's equations is each update, and why does a wave result?
2. Why is the one-dimensional grid exact at a Courant number of 1, and why can it not run faster than that?
3. Why does the strong conductor reflect the pulse with its electric field inverted?

### Answers

1. The $H$ update is Faraday's law ($\mu_0\partial H_y/\partial t = \partial E_z/\partial x$) and the $E$ update is the Ampère–Maxwell law with only displacement current ($\varepsilon_0\partial E_z/\partial t = \partial H_y/\partial x$). Each field's change is driven by the other's spatial variation, the mutual regeneration of §2; eliminating one field gives the wave equation, so the scheme propagates waves at $1/\sqrt{\mu_0\varepsilon_0}$ without being told to.
2. At $S$ = 1 the central differences in time and space have exactly matching errors, so $\sin(\omega\Delta t/2) = \sin(k\Delta x/2)$ gives $\omega = ck$ for every wavelength: the update simply shifts the wave one cell per step. Beyond $S$ = 1 the information would have to travel more than one cell per step, faster than the scheme's stencil can carry it, and the update becomes unstable (the Courant–Friedrichs–Lewy condition).
3. Inside a good conductor the electric field must be nearly zero (charge relaxes almost instantly), so at its surface the incident and reflected electric fields must nearly cancel: the reflection coefficient for $E$ approaches −1, like a short circuit at the end of a line. The magnetic field, by contrast, doubles there (13-06).

## Optional hardware extension

Make a small loop probe (a few turns of wire, about 1 cm across) and connect it to an oscilloscope. Hold it near a switching power supply's inductor and see the induced voltage from $d\Phi/dt$; rotate the loop to change the flux through it and watch the reading follow $\cos\theta$. Then shorten an ordinary probe's ground lead to a spring tip and compare the ringing on a fast logic edge.
