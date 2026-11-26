# Solutions 24-08 · Silicon Photonics and Optical Transceivers

Problems: [24-08 problems](../problems/24-08-problems.md) · Chapter: [24-08](../chapters/24-08-silicon-photonics.md)

Every number is recomputed by [verify_24_08.py](../verify/verify_24_08.py).

---

## Solutions

### Solution 24-08.1

GaAs: $1239.84/1.42$ = **873** nm. InP: $1239.84/1.34$ = **925** nm.

Both cut off above 850 nm, so both absorb 850 nm light (GaAs photodiodes pair naturally with 850 nm GaAs VCSELs). Neither absorbs 1310 nm: its photons carry 0.946 eV, below both gaps. InP-based lasers emit at 1310 nm only through narrower-gap alloys (InGaAsP) grown on InP.

### Solution 24-08.2

(a) $\arcsin(1.44/2.0)$ = **46.1**°.

(b) $\sqrt{4 - 1.44^2}$ = **1.39**; $d < 1.31/(2 \times 1.39)$ = **0.472** µm.

(c) Silicon: $1.31/(2 \times 3.17)$ = **0.207** µm; nitride's limit is **2.28** times thicker.

Lower contrast gives nitride larger modes, gentler sidewall scattering and lower loss, at the price of larger bends: a common complement to silicon on the same chip.

### Solution 24-08.3

(a) $(2 \times 4.6 \times 2.0/(4.6^2 + 2.0^2))^2$ = **0.535**: **−2.72** dB.

(b) $\exp(-2 \times 1^2/(2 \times 4.6^2))$ = 0.954: **−0.21** dB.

(c) $\exp(-1/2.0^2)$ = 0.779: **−1.09** dB.

Shrinking the mode from 4.6 to 2.0 µm (2.3 times) raises the offset loss in dB 5.3 times, because the exponent goes as $1/w^2$.

### Solution 24-08.4

(a) $1550/(2.85 - \sin 8°)$ = **572** nm.

(b) $1/(572\ \text{nm} \times \cos 8°)$ in degrees: **0.101**°/nm.

(c) $w$ = 5.2 µm: $1.55/(\pi \times 5.2)$ rad = **5.44**°.

(d) $2 \times 5.44° \times \sqrt{0.1\ln 10}/0.101$ = **52** nm.

The longer wavelength helps twice: the period is longer, so the beam steers less per nanometre, and $\lambda/w$ rises slightly, so the beam diverges a little more. The larger fiber mode on its own would narrow the band, since $\theta_{div} = \lambda/(\pi w)$.

### Solution 24-08.5

(a) $-7 + 2 + 0.72 + 1.0 + 1.5 + 6$ = **4.22** dBm.

(b) $10^{0.422}$ = **2.64** mW.

(c) $4 \times 2.64$ = **10.6** mW.

Without a splitter each EML needs only a few milliwatts, but there are four of them, each with its own temperature control: the trade of Example 24-08.5 seen from the other side.

### Solution 24-08.6

(a) $f_0 = 1/(2\pi\sqrt{0.5\ \text{nH} \times 20\ \text{fF}})$ = **50.3** GHz; $\zeta = 25\sqrt{20\ \text{fF}/0.5\ \text{nH}}$ = **0.158**.

(b) Peak at $f_0\sqrt{1 - 2\zeta^2}$ = **49.1** GHz, height $1/(2\zeta\sqrt{1 - \zeta^2})$ = 3.20, that is **10.1** dB.

(c) $f_{3dB}$ = **76.8** GHz.

(d) **No.** The bandwidth now exceeds the 56.7 GHz Nyquist frequency, but a 10 dB resonance at 49 GHz sits inside the signal band. Halving $L$ raised $f_0$ by only $\sqrt 2$ and $\zeta$ by $\sqrt 2$: inductance must fall by orders of magnitude, which is what 3D bonding provides.

### Solution 24-08.7

(a) $1/Q^2 = 2/81 + 1/56.25$, so $Q$ = **4.85** and BER = **6.1** × 10⁻⁷.

(b) $2Q(9) + Q(7.5)$ = **3.2** × 10⁻¹⁴, almost all from the optical segment.

### Solution 24-08.8

(a) $64 \times 16$ = **1,024** W.

(b) $1024/(1024 + 1500)$ = **41**%.

(c) $1024\ \text{W}/51.2\ \text{Tb/s}$ = **20** pJ/bit.

Two fifths of the box is pluggable optics, which is the case 24-09's linear and co-packaged optics try to make.

### Solution 24-08.9

(a) $0.998^{16}$ = **0.968**.

(b) $4/0.968$ = **4.13**.

(c) $1/0.968 + 3$ = **4.03**.

(d) **2.4**%.

Better lanes cut the saving, but a module with 16 lanes still discards one assembly in about 32 without test.

### Solution 24-08.10

(a) $16 \times 32$ = **512** Gb/s per fiber per direction.

(b) $8 \times 2 \times 512$ = **8,192** Gb/s in both directions, matching the electrical side's 16 × 512 Gb/s.

(c) $8192/896$ = **9.14** mm of shoreline.

(d) At 32 Gb/s NRZ, each lane needs no DSP and no ADC: simple drivers, ring modulators and TIAs suffice, which keeps the energy per bit low. Wavelength multiplexing then restores the per-fiber bandwidth. The cost is many wavelengths (here an external 16-wavelength source) and many rings to tune, the thermal-control problem of 24-07.

### Solution 24-08.11

(a) $(20/8)^{1/5} - 1$ = **20.1**% a year.

(b) $26/16.5 - 1$ = **57.6**%.

(c) They measure different markets: LightCounting's figure covers Ethernet transceivers and CPO for AI clusters; TrendForce's covers AI optical transceivers more broadly, and its 2025 base is twice LightCounting's. A five-year average also smooths a boom year. Compare like with like before quoting either.

### Solution 24-08.12

(a) Outer channels are 30 nm off centre: $\Delta\theta = 30 \times 0.117$ = 3.50°, loss $10\log_{10}e^{-(3.50/5.19)^2}$ = **2.0** dB.

(b) Inner channels, 10 nm off: 1.17° and **0.22** dB.

(c) A 2 dB penalty on the worst channels uses most of a short-reach link's margin. Use an edge coupler for the multiplexed CWDM4 output, keep grating couplers for wafer-level test structures, or use a parallel single-wavelength design (DR4) instead.

### Solution 24-08.13

(a) Two-tier: $2 \times 2 \times 16$ = **64** W per GPU; three-tier: **96** W.

(b) **6.4** MW and **9.6** MW.

(c) $0.25 \times 9.6$ = **2.4** MW.

At these scales optics power is a facilities question, and a quarter off every module is worth megawatts.

### Solution 24-08.14

(a) With $w_2 = w_1(1 + \epsilon)$ the amplitude factor is

$$
\frac{2w_1w_2}{w_1^2 + w_2^2} = \frac{2(1 + \epsilon)}{2 + 2\epsilon + \epsilon^2} = \frac{1}{1 + \epsilon^2/[2(1 + \epsilon)]} = 1 - \frac{\epsilon^2}{2} + O(\epsilon^3),
$$

using $1/(1 + u) = 1 - u + O(u^2)$ with $u = \epsilon^2/[2(1 + \epsilon)] = \epsilon^2/2 + O(\epsilon^3)$. Squaring gives $\eta = 1 - \epsilon^2 + O(\epsilon^3)$. Since $-\ln(1 - u) \approx u$, the loss is $-10\log_{10}\eta \approx 10\log_{10}(e)\,\epsilon^2$ = **4.34** $\epsilon^2$ dB. There is no first-order term: coupling is stationary at a perfect match, so small mismatches are cheap.

(b) By the approximation, $\epsilon = \sqrt{0.1/4.34}$ = **0.152**, about 15%. Solving the exact formula numerically gives **0.164** for a larger second mode and **−0.141** for a smaller one; the $O(\epsilon^3)$ term makes the tolerance asymmetric.

(c) With $w_1 = w_2 = w$, $\eta = \exp(-d^2/w^2)$ and the loss is $10\log_{10}(e)\,d^2/w^2$ dB. Setting it to 0.1 dB gives $d = w\sqrt{0.1/4.34} = 0.152\,w$: **0.70** µm for $w$ = 4.6 µm and **0.30** µm for $w$ = 2.0 µm.

(d) Offset tolerance scales with the mode radius. A spot-size converter that enlarges the chip's mode **2.3** times to match the fiber also buys 2.3 times the placement tolerance for the same loss, which can decide between passive placement and active alignment.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 24-08.1a | GaAs cutoff | 873 | nm |
| 24-08.1b | InP cutoff | 925 | nm |
| 24-08.2a | SiN critical angle | 46.1 | ° |
| 24-08.2b0 | sqrt(n1^2 - n2^2), SiN | 1.39 | |
| 24-08.2b | SiN single-mode thickness | 0.472 | µm |
| 24-08.2c | Si single-mode thickness at 1310 nm | 0.207 | µm |
| 24-08.2c1 | thickness ratio | 2.28 | |
| 24-08.3a | efficiency into 2.0 um | 0.535 | |
| 24-08.3a1 | loss into 2.0 um | -2.72 | dB |
| 24-08.3b0 | offset efficiency, 4.6 um | 0.954 | |
| 24-08.3b | offset loss, 4.6 um | -0.21 | dB |
| 24-08.3c0 | offset efficiency, 2.0 um | 0.779 | |
| 24-08.3c | offset loss, 2.0 um | -1.09 | dB |
| 24-08.3e0 | mode-size ratio | 2.3 | |
| 24-08.3e | offset-loss ratio in dB | 5.3 | |
| 24-08.4a | period | 572 | nm |
| 24-08.4b | angular dispersion | 0.101 | °/nm |
| 24-08.4c | divergence half-angle | 5.44 | ° |
| 24-08.4d | 1-dB bandwidth | 52 | nm |
| 24-08.5a | laser section output | 4.22 | dBm |
| 24-08.5b | laser section output | 2.64 | mW |
| 24-08.5c | four lanes | 10.6 | mW |
| 24-08.6a | natural frequency | 50.3 | GHz |
| 24-08.6a1 | damping ratio | 0.158 | |
| 24-08.6b | peak frequency | 49.1 | GHz |
| 24-08.6b0 | peak gain | 3.20 | |
| 24-08.6b1 | peaking | 10.1 | dB |
| 24-08.6c | bandwidth | 76.8 | GHz |
| 24-08.7a | linear Q | 4.85 | |
| 24-08.7a1 | linear BER | 6.1e-7 | |
| 24-08.7b | retimed BER | 3.2e-14 | |
| 24-08.8a | optics power | 1024 | W |
| 24-08.8b | optics share | 41 | % |
| 24-08.8c | energy per bit | 20 | pJ/bit |
| 24-08.9a | yield | 0.968 | |
| 24-08.9b | cost without test | 4.13 | |
| 24-08.9c | cost with test | 4.03 | |
| 24-08.9d | saving | 2.4 | % |
| 24-08.9e | assemblies discarded, one in | 32 | |
| 24-08.10a | per fiber per direction | 512 | Gb/s |
| 24-08.10b | optical bandwidth | 8192 | Gb/s |
| 24-08.10c | shoreline needed | 9.14 | mm |
| 24-08.11a | LightCounting CAGR | 20.1 | % |
| 24-08.11b | TrendForce growth | 57.6 | % |
| 24-08.12a | outer-channel loss | 2.0 | dB |
| 24-08.12a0 | outer-channel steer | 3.50 | ° |
| 24-08.12b0 | inner-channel steer | 1.17 | ° |
| 24-08.12b | inner-channel loss | 0.22 | dB |
| 24-08.13a | two-tier per GPU | 64 | W |
| 24-08.13a1 | three-tier per GPU | 96 | W |
| 24-08.13b | two-tier total | 6.4 | MW |
| 24-08.13b1 | three-tier total | 9.6 | MW |
| 24-08.13c | saving | 2.4 | MW |
| 24-08.14a | loss coefficient | 4.34 | dB |
| 24-08.14b | mismatch for 0.1 dB, approximate | 0.152 | |
| 24-08.14b1 | mismatch for 0.1 dB, larger mode | 0.164 | |
| 24-08.14b2 | mismatch for 0.1 dB, smaller mode | -0.141 | |
| 24-08.14c | offset for 0.1 dB, w = 4.6 um | 0.70 | µm |
| 24-08.14c1 | offset for 0.1 dB, w = 2.0 um | 0.30 | µm |
| 24-08.14d | mode-radius ratio | 2.3 | |
