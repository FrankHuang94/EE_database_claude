# Solutions 25-02 · Lithography: DUV, Multipatterning, EUV and High-NA

Problems: [25-02 problems](../problems/25-02-problems.md) · Chapter: [25-02](../chapters/25-02-lithography.md)

Every number is recomputed by [verify_25_02.py](../verify/verify_25_02.py).

---

## Solutions

### Solution 25-02.1

(a) $248/0.80$ = **310** nm.

(b) $248/(2 \times 0.80)$ = **155** nm.

(c) **77.5** nm.

### Solution 25-02.2

(a) $1.65 \times 0.94$ = **1.55**.

(b) $193/(4 \times 1.55)$ = **31.1** nm, against 35.7 nm with water. High-index fluids were researched for exactly this gain, but no fluid and lens material combination reached production; EUV took over instead.

### Solution 25-02.3

(a) $s_0 = \lambda/(2p) = 13.5/48$ = **0.281**, inside the 0.33 pupil: it prints.

(b) $13.5/(2 \times 0.33)$ = **20.5** nm.

(c) $13.5/0.33$ = **40.9** nm.

A 24 nm pitch is printable by EUV only with off-axis illumination, and is near its practical limit ($k_1$ = 12 × 0.33/13.5 = 0.293, just above the 0.25 floor).

### Solution 25-02.4

(a) Dry: $\sqrt{1 - 0.93^2}$ = 0.368, so $z = 193/(4 \times 0.632)$ and DOF = **153** nm. Water: $\sqrt{1 - (0.93/1.44)^2}$ = 0.763, so $z = 193/(4 \times 1.44 \times 0.237)$ and DOF = **283** nm.

(b) **1.86** times. At the same NA the beams travel at shallower angles in water, so defocus shifts their phases less. Immersion was first sold to some fabs as a DOF improvement at existing NA, before NA rose above 1.

### Solution 25-02.5

(a) Over one period $p$, with the open region $|x| < fp/2$, the Fourier coefficients are $a_m = \frac{1}{p}\int_{-fp/2}^{fp/2} e^{-j2\pi mx/p}\,dx$. For $m = 0$ this is $f$. For $m = 1$:

$$
a_1 = \frac{1}{p}\cdot\frac{e^{-j\pi f} - e^{j\pi f}}{-j2\pi/p} = \frac{\sin(\pi f)}{\pi} .
$$

(b) From §3.2, $I(x) = a_0^2 + a_1^2 + 2a_0a_1\cos(2\pi x/p)$. Its maximum is $(a_0 + a_1)^2$ and minimum $(a_0 - a_1)^2$, so

$$
C = \frac{(a_0 + a_1)^2 - (a_0 - a_1)^2}{(a_0 + a_1)^2 + (a_0 - a_1)^2} = \frac{4a_0a_1}{2(a_0^2 + a_1^2)} = \frac{2a_0a_1}{a_0^2 + a_1^2} .
$$

Tilting the illumination shifts both orders' directions equally and multiplies the field by a common phase ramp, which leaves $|E|^2$ unchanged: the contrast does not depend on the tilt.

(c) $f$ = 0.5: $a_1 = 1/\pi$ = **0.318**, $C$ = **0.906**. $f$ = 0.25: $a_1 = \sin(\pi/4)/\pi$ = **0.225**, $C$ = **0.995**. The narrower opening balances the two orders' amplitudes, which maximizes two-beam contrast ($C = 1$ when $a_0 = a_1$).

### Solution 25-02.6

(a) $76/4$ = **19** nm.

(b) $10.5 \times 0.33/13.5$ = **0.257**: barely above the 0.25 floor and well below EUV's practical 0.32, so not a plausible single exposure.

(c) $10.5 \times 0.55/13.5$ = **0.428**: comfortable. A 21 nm pitch is High-NA single-exposure territory, or Low-NA EUV double patterning.

### Solution 25-02.7

(a) **21.5** and **26.5** nm: $2.5/24$ = **10.4**%.

(b) $0.08 \times 24$ = **1.92** nm.

### Solution 25-02.8

(a) $50 \times 10^{-3}/1.47 \times 10^{-17} \times 10^{-14}$ = **34.0** per nm².

(b) $34.0 \times 64$ = **2.17e3**.

(c) **435**.

(d) $1/\sqrt{435}$ = **4.8**%.

Raising the dose from 30 to 50 mJ/cm² does not keep pace with the smaller feature: 64 nm² at 50 mJ/cm² receives about as many photons as 100 nm² at 30 mJ/cm² (Example 25-02.6), and the fluctuation is no better.

### Solution 25-02.9

$N_{abs} \ge 1/0.03^2$ = **1.11e3** absorbed photons, so $1.11 \times 10^3/(0.25 \times 64)$ = **69.4** incident per nm², a dose of $69.4/20.4 \times 30$ = **102** mJ/cm².

### Solution 25-02.10

(a) $3600/220$ = 16.36 s per wafer, so $t_{exp}$ = **10.4** s.

(b) $t_{exp}$ scales to $10.36 \times 50/30$ = 17.27 s: $3600/(6 + 17.27)$ = **155** wph.

(c) $10.36 \times 102/30$ = 35.2 s: $3600/41.2$ = **87.3** wph.

Tripling the dose for noise cuts throughput by 60% here; this is why dose, not optics, often sets the practical limit of EUV at the smallest features.

### Solution 25-02.11

$350 \times 10^6/(35{,}064 \times 135)$ = **€73.9** per pass, **1.30** times the €57.0 at specification.

### Solution 25-02.12

(a) Yes; $700/858$ = **82**% of the field.

(b) No: it exceeds the 429 mm² half field and must be stitched.

### Solution 25-02.13

(a) Exposure time falls by 600/1000 to $0.6 \times 10.36$ = 6.22 s: $3600/(6 + 6.22)$ = **295** wph, **34**% more, half the 67% power gain.

(b) With overhead $t_{oh}$ and exposure time $x$ at the lower power: $t_{oh} + x = 3600/220$ = 16.36 s and $t_{oh} + 0.6x = 3600/330$ = 10.91 s. Subtracting, $0.4x$ = 5.45 s, so $x$ = **13.6** s and $t_{oh}$ = **2.7** s. A 50% throughput gain from 67% more power requires overhead to be only about a sixth of the wafer time; in practice the roadmap also assumes faster stages and other improvements.

### Solution 25-02.14

(a) Alternate spaces are the mandrel width, **18** nm, and the gap between neighbouring mandrels minus two spacers, $64 - 18 - 2 \times 16$ = **14** nm.

(b) The difference is **4** nm, twice the 2 nm mandrel error: one space gains the error and the other loses it.

(c) ±**1** nm.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 25-02.1a | on-axis minimum pitch | 310 | nm |
| 25-02.1b | off-axis minimum pitch | 155 | nm |
| 25-02.1c | half-pitch | 77.5 | nm |
| 25-02.2a | NA with n = 1.65 | 1.55 | |
| 25-02.2b | half-pitch at k1 = 0.25 | 31.1 | nm |
| 25-02.3a | dipole position | 0.281 | |
| 25-02.3b | off-axis minimum pitch | 20.5 | nm |
| 25-02.3c | on-axis minimum pitch | 40.9 | nm |
| 25-02.3d | k1 of 24 nm pitch | 0.293 | |
| 25-02.4a0 | cosine, dry | 0.368 | |
| 25-02.4a1 | one minus cosine, dry | 0.632 | |
| 25-02.4a | DOF, dry | 153 | nm |
| 25-02.4a2 | cosine, water | 0.763 | |
| 25-02.4a3 | one minus cosine, water | 0.237 | |
| 25-02.4b | DOF, water | 283 | nm |
| 25-02.4c | ratio | 1.86 | |
| 25-02.5a | a1 for f = 0.5 | 0.318 | |
| 25-02.5b | contrast for f = 0.5 | 0.906 | |
| 25-02.5c | a1 for f = 0.25 | 0.225 | |
| 25-02.5d | contrast for f = 0.25 | 0.995 | |
| 25-02.6a | SAQP pitch | 19 | nm |
| 25-02.6b | k1 at NA 0.33 | 0.257 | |
| 25-02.6c | k1 at NA 0.55 | 0.428 | |
| 25-02.7a | narrow space | 21.5 | nm |
| 25-02.7a1 | wide space | 26.5 | nm |
| 25-02.7a2 | space error | 10.4 | % |
| 25-02.7b | overlay budget | 1.92 | nm |
| 25-02.8a | photons per nm² at 50 mJ/cm² | 34.0 | nm⁻² |
| 25-02.8b | photons on feature | 2.17e3 | |
| 25-02.8c | absorbed photons | 435 | |
| 25-02.8d | fluctuation | 4.8 | % |
| 25-02.9a | absorbed photons needed | 1.11e3 | |
| 25-02.9b | incident photons per nm² | 69.4 | nm⁻² |
| 25-02.9c | dose | 102 | mJ/cm² |
| 25-02.10a0 | wafer time at 220 wph | 16.36 | s |
| 25-02.10a | exposure time | 10.4 | s |
| 25-02.10a1 | exposure time, 4 s.f. | 10.36 | s |
| 25-02.10b0 | exposure time at 50 mJ/cm² | 17.27 | s |
| 25-02.10b | throughput at 50 mJ/cm² | 155 | wph |
| 25-02.10c0 | exposure time at 102 mJ/cm² | 35.2 | s |
| 25-02.10c1 | wafer time at 102 mJ/cm² | 41.2 | s |
| 25-02.10c | throughput at 102 mJ/cm² | 87.3 | wph |
| 25-02.10d | throughput loss from tripled dose | 60 | % |
| 25-02.11a | cost per pass at 135 wph | 73.9 | € |
| 25-02.11b | ratio to specification | 1.30 | |
| 25-02.12a | field fraction used | 82 | % |
| 25-02.13a0 | exposure time at 1,000 W | 6.22 | s |
| 25-02.13a | throughput at 1,000 W | 295 | wph |
| 25-02.13a1 | throughput gain | 34 | % |
| 25-02.13b0 | wafer time at 330 wph | 10.91 | s |
| 25-02.13b1 | difference | 5.45 | s |
| 25-02.13b | exposure time implied | 13.6 | s |
| 25-02.13b2 | overhead implied | 2.7 | s |
| 25-02.14a | first space | 18 | nm |
| 25-02.14a1 | second space | 14 | nm |
| 25-02.14b | space difference | 4 | nm |
| 25-02.14c | mandrel tolerance | 1 | nm |
