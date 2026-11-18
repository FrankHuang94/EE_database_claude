# Lab 04-09 · Waves and Optics Basics

**Chapter:** [04-09](../../chapters/04-09-waves-and-optics.md) · **Notebook:** [04-09-waves.ipynb](04-09-waves.ipynb) · **Netlist:** [quarter_wave_stub.cir](quarter_wave_stub.cir) · **Time:** about 60 minutes

## Objective

1. Build beats and standing waves from travelling waves.
2. Compute a phased array's beam, steer it, and see grating lobes appear.
3. Reproduce the diffraction zeros of a slit and a circular aperture by summing Huygens wavelets.
4. Compute a thin-film coating's reflectance spectrum with characteristic matrices.
5. Estimate dispersion-limited bit rates in fiber.
6. Simulate a quarter-wave transmission-line stub in ngspice.

## Background

Chapter sections 3.1 to 3.5 and Examples 04-09.2 to 04-09.4 and 04-09.7; Problems 04-09.5, 04-09.12 and 04-09.14. The notebook has no random elements.

## Procedure

1. Run all notebook cells in order, writing a prediction before each **🔮 Predict** cell.
2. **Part 1:** predict where the nodes of a standing wave sit and whether they move.
3. **Part 2:** predict an 8-element λ/2 array's beamwidth at broadside and at 30°, and what a full-wavelength spacing does.
4. **Part 3:** predict the first diffraction zeros of a slit and a circular aperture.
5. **Part 4:** predict where the MgF₂ coating's reflectance is lowest.
6. **Part 5:** predict the dispersion spreading over 10 km and 100 km.
7. From the repository root, run `python tools/run_spice.py 04-09` to simulate the stub.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | standing wave | nodes fixed at 0.25, 0.75, … wavelengths |
| 2 | 8 elements, λ/2 | −3 dB beamwidth 12.80° at broadside, 14.84° steered to 30°; grating lobes at ±90° with λ spacing |
| 3 | diffraction zeros | slit at sin θ = 1.0000 λ/a; circle at 1.2197 λ/D |
| 4 | MgF₂ coating | minimum 1.411% at 550 nm; 1.721% at 450 nm and 1.563% at 650 nm |
| 5 | dispersion, 0.1 nm source | 17 ps over 10 km (29.4 Gb/s limit); 170 ps over 100 km |
| netlist | quarter-wave stub | input-impedance minimum at 1.000 GHz |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 04-09.a | array beamwidth at broadside | 12.80 | ° |
| Lab 04-09.b | array beamwidth steered to 30° | 14.84 | ° |
| Lab 04-09.c | slit first zero | 1.0000 | λ/a |
| Lab 04-09.d | circular-aperture first zero | 1.2197 | λ/D |
| Lab 04-09.e | wavelength of minimum reflectance | 550.0 | nm |
| Lab 04-09.f | dispersion-limited bit rate over 10 km | 29.41 | Gb/s |

## Discussion questions

1. Part 2 shows the beam widening when steered. A base-station array must cover ±60°. What does the widening imply for its gain at the edges of its coverage, and how might designers compensate?
2. Part 3 reproduces the 1.22 factor by brute force. A lithography lens's NA plays the role of D. Why does a scanner illuminate the mask with carefully shaped off-axis light rather than a simple cone?
3. Part 4's single-layer coating has 1.4–1.7% reflectance across the visible. Why do camera lenses with a dozen elements need much better coatings than a single window?
4. The netlist shows a quarter-wave open stub acting as a short at 1 GHz. At 2 GHz it is open again. How could you use such a stub as a filter in a radio front end?

<details><summary>Answers to the discussion questions</summary>

1. A steered array's effective aperture shrinks by about cos θ, so the beam widens and the peak gain falls (by roughly cos θ, about 3 dB at 60°), and element patterns usually fall off at wide angles too. Designers add elements, split coverage among several panels facing different directions, or accept lower margin at the edges.
2. Diffraction orders from a fine mask pattern leave at angles too large for the lens to capture with on-axis light; tilting the illumination lets two orders (for example 0 and +1) pass through the pupil, which is all the image needs, effectively lowering $k_1$. Shaping the illumination to the pattern (and the mask to the illumination) is how lithographers approach $k_1$ = 0.25.
3. Reflections add up: with 24 surfaces at 1.5% each, about 30% of the light would be lost and, worse, scattered into flare and ghost images. Multilayer coatings below 0.5% per surface keep total loss and stray light acceptable.
4. Connected across a signal line, the stub shorts out 1 GHz (a notch that removes an interfering signal) while passing frequencies where it looks open; connected in other arrangements it can pass a band instead. Such stubs and resonators make filters and impedance-matching networks in RF and microwave circuits (Course 21).

</details>

## Optional hardware version

With a laser pointer, a piece of foil with two pin scratches close together (or a hair stretched across a frame), and a wall a few meters away, measure the fringe spacing and compute the slit separation (or hair thickness) from $\Delta y = \lambda L/d$. Two polarizing sunglasses lenses and a phone screen demonstrate Malus's law: rotate one lens and watch the screen dim.
