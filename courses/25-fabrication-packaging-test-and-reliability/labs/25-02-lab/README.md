# Lab 25-02 · Aerial Images, Focus, Photon Noise and Scanner Economics

**Objective.** Build aerial images of line-space gratings from their diffraction orders; find the resolution cutoff for on-axis and off-axis illumination; see how defocus affects each; simulate photon shot noise; and model scanner throughput against dose.

**Chapter:** [25-02 · Lithography: DUV, Multipatterning, EUV and High-NA](../../chapters/25-02-lithography.md)

## Background

§3.2 showed that an image needs at least two diffraction orders inside the pupil, which gives a minimum pitch of $\lambda/\text{NA}$ on axis and $\lambda/(2\,\text{NA})$ with ideal off-axis illumination. §3.3 derived the defocus phase $2\pi nz\cos\theta/\lambda$ of each order. §3.6 showed that photon counts are Poisson, with relative fluctuation $1/\sqrt N$. §3.8 modelled throughput as overhead plus an exposure time proportional to dose.

## Files

- `litho.py`: Fourier amplitudes of a grating, passing orders, aerial images with poles and defocus, contrast, quarter-wave depth of focus, photon counts and a Monte Carlo of absorbed photons, throughput against dose and power, and cost per pass.
- `25-02-litho-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · Resolution cutoff** (notebook). For a 0.33-NA EUV system with an ideal dipole (orders 0 and −1 at $\pm\lambda/2p$), *predict* the pitch at which the image vanishes, then sweep the pitch. Repeat for an ArF immersion system with on-axis and dipole illumination and plot contrast against pitch.

**Part 2 · Focus** (notebook). For a 160 nm pitch on ArF immersion (NA 1.35, water), *predict* how the contrast of on-axis and dipole images changes 50 nm out of focus, then compute both and plot the images.

**Part 3 · Photon noise** (notebook). For Example 25-02.6's contact (10 nm × 10 nm, 30 mJ/cm², 20% absorption), *predict* the standard deviation of absorbed photons, then simulate 100,000 contacts.

**Part 4 · Dose and throughput** (notebook). For a scanner giving 220 wph at 30 mJ/cm² with 6 s of overhead, *predict* the throughput at 60 mJ/cm², then sweep the dose.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 25-02.a | EUV 0.33-NA cutoff pitch, ideal dipole | 20.5 | nm |
| Lab 25-02.b | on-axis contrast at focus, 160 nm | 1.00 | |
| Lab 25-02.b1 | on-axis contrast at 50 nm defocus | 0.67 | |
| Lab 25-02.b2 | dipole contrast, in and out of focus | 0.906 | |
| Lab 25-02.c | standard deviation of absorbed photons | 20.2 | |
| Lab 25-02.d | throughput at 60 mJ/cm² | 135 | wph |

The simulated standard deviation is within 1% of $\sqrt N$. On axis, the 160 nm image's field crosses zero, so its contrast at focus is essentially 1; three orders interfere, and defocus moves the first orders out of phase with the zeroth. The symmetric dipole's two orders accumulate the same defocus phase, so its contrast does not change.

## Discussion

1. Why does an ideal dipole tuned for one pitch print other pitches worse? Try a fixed dipole across a range of pitches.
2. The dipole image is immune to defocus here. What happens to a layout with lines in both directions?
3. Halving the photon noise needs four times the dose. Using Part 4, what does that cost in throughput?
4. Which of this lab's simplifications (scalar optics, thin mask, no resist blur) would matter most at EUV's smallest pitches?

## Optional hardware

None needed. A university cleanroom with a contact or projection aligner lets you expose a resolution target and see the cutoff directly; a microscope shows line-end shortening and corner rounding, the effects OPC corrects.
