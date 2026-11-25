# Solutions 24-07 · Photonics Fundamentals

Problems: [24-07 problems](../problems/24-07-problems.md) · Chapter: [24-07](../chapters/24-07-photonics-fundamentals.md)

Every number is recomputed by [verify_24_07.py](../verify/verify_24_07.py).

---

## Solutions

### Solution 24-07.1

(a) $\mathcal R = 0.8 \times q\lambda/hc$ = **0.845** A/W.

(b) −6 dBm is **251** µW, so $I$ = **212** µA.

### Solution 24-07.2

(a) $10^{-20/10}$ mW = **10** µW.

(b) Each lane is 0.631 mW; four make **2.52** mW = **4.02** dBm, 6.02 dB above one lane, because four times the power is $10\log_{10}4$ dB more.

### Solution 24-07.3

$100 \times 1.468/c$ = **0.490** µs one way; **0.979** µs round trip, essentially the whole 1 µs that Ultra Ethernet's link-level retry assumes. The retry buffer of 24-05 is sized by fiber length.

### Solution 24-07.4

(a) $(1.31\ \mu\text{m})^2 \times 113.4375\ \text{GHz}/c$ = **0.649** nm.

(b) $3.5 \times 2 \times 0.649$ = **4.55** ps.

(c) The UI is 8.82 ps, so the spread is **0.52** UI, against 0.11 UI at 53.125 GBd.

Doubling the symbol rate doubled the spectral width and halved the UI, so the fractional spread rose about fourfold (4.6 here, because the rates differ by 2.14). This is why 2 km 200 Gb/s-per-lane links need careful wavelength plans, DSP equalization and stronger FEC.

### Solution 24-07.5

$\Delta\lambda = (1.55\ \mu\text{m})^2 \times 26.5625\ \text{GHz}/c$ = 0.213 nm and the UI is 37.6 ps. Then $L = 0.25 \times 37.6/(17 \times 0.213)$ = **2.6** km.

### Solution 24-07.6

(a) $2.3/1$ = **2.3** cm.

(b) $\Delta\phi = \pi/2 \pm 0.4\pi$: $\cos^2(\pi/4 - 0.2\pi)$ = **0.976** and $\cos^2(\pi/4 + 0.2\pi)$ = **0.024**; the extinction ratio is 39.9 = **16.0** dB and the OMA **0.951** $P_{in}$.

A 0.8 $V_\pi$ swing reaches 16 dB of extinction, where Example 24-07.5's half-$V_\pi$ swing reached 7.7 dB: the $\cos^2$ flattens near its extremes, so the last 20% of swing would add little OMA.

### Solution 24-07.7

(a) $40 \times 0.05614$ = **2.25** nm.

(b) $2.25/0.25$ = **9.0** mW.

(c) $9.0\ \text{mW}/100\ \text{Gb/s}$ = **90** fJ/bit, 18 times the modulation energy.

The heater, not the modulator, dominates a ring's energy in the worst case. Real systems reduce it with better thermal isolation, by sharing the tuning budget across rings and by locking the laser rather than every ring.

### Solution 24-07.8

(a) $15 \times 10^{-12}\sqrt{60 \times 10^9}$ = **3.67** µA.

(b) $Q$ = 3.49, so $P$ = $3.49 \times 3.67/0.85$ = **15.1** µW = **−18.2** dBm.

(c) A 4 dB extinction ratio (2.51) costs **3.66** dB; adding PAM4's 4.77 dB gives **−9.8** dBm.

### Solution 24-07.9

$1 - 0.5 \times 0.36 - 2 \times 0.75$ = **−0.68** dBm received, a margin of **7.32** dB over −8 dBm.

### Solution 24-07.10

(a) $R_F = (1 + A)/(2\pi BC_{in})$ = $9/(2\pi \times 30\ \text{GHz} \times 80\ \text{fF})$ = **597** Ω.

(b) $\sqrt{4kT/R_F}$ = **5.27** pA/√Hz.

(c) $5.27\ \text{pA/√Hz} \times \sqrt{30\ \text{GHz}}$ = **0.91** µA.

Bandwidth forces $R_F$ down and its noise up. The amplifier's own noise usually adds as much again or more, so a receiver's total input-referred noise is several times the feedback resistor's alone.

### Solution 24-07.11

$\lambda^2\Delta f/c$ = **0.572** nm; 16 channels span 15 spacings, **8.59** nm.

### Solution 24-07.12

(a) The current is proportional to optical power, so the eye shrinks by a factor of $10^{0.3}$ ≈ **2**.

(b) Electrical power goes as current squared: **6** dB, twice the optical 3 dB.

(c) $Q$ falls from 7.03 to $7.03/10^{0.3}$ = **3.53**, so the BER becomes $Q(3.53)$ = **2.1** × 10⁻⁴: 3 dB of light turns a near-perfect link into one that needs FEC.

### Solution 24-07.13

$(ER + 1)/(ER - 1) = 10^{0.1}$ gives $ER$ = **8.72**, or **9.41** dB.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 24-07.1a | responsivity | 0.845 | A/W |
| 24-07.1b0 | power | 251 | µW |
| 24-07.1b | photocurrent | 212 | µA |
| 24-07.2a | -20 dBm | 10 | µW |
| 24-07.2b0 | one lane | 0.631 | mW |
| 24-07.2b | four lanes | 2.52 | mW |
| 24-07.2b1 | four lanes in dBm | 4.02 | dBm |
| 24-07.2b2 | four lanes over one | 6.02 | dB |
| 24-07.3a | one-way delay | 0.490 | µs |
| 24-07.3b | round trip | 0.979 | µs |
| 24-07.4a | spectral width | 0.649 | nm |
| 24-07.4b | spread | 4.55 | ps |
| 24-07.4c0 | UI | 8.82 | ps |
| 24-07.4c | spread in UI | 0.52 | UI |
| 24-07.4d | growth in fractional spread | 4.6 | |
| 24-07.4d1 | rate ratio | 2.14 | |
| 24-07.5a | spectral width | 0.213 | nm |
| 24-07.5a1 | UI | 37.6 | ps |
| 24-07.5 | reach | 2.6 | km |
| 24-07.6a | length | 2.3 | cm |
| 24-07.6b | high level | 0.976 | |
| 24-07.6b1 | low level | 0.024 | |
| 24-07.6b2 | extinction ratio | 39.9 | |
| 24-07.6b3 | extinction ratio in dB | 16.0 | dB |
| 24-07.6b4 | OMA | 0.951 | |
| 24-07.7a | tuning range | 2.25 | nm |
| 24-07.7b | heater power | 9.0 | mW |
| 24-07.7c | heater energy | 90 | fJ/bit |
| 24-07.7c1 | heater over modulation | 18 | |
| 24-07.8a | noise current | 3.67 | µA |
| 24-07.8b0 | Q | 3.49 | |
| 24-07.8b | OOK sensitivity | 15.1 | µW |
| 24-07.8b1 | OOK sensitivity in dBm | -18.2 | dBm |
| 24-07.8c0 | ER penalty | 3.66 | dB |
| 24-07.8c | PAM4 sensitivity | -9.8 | dBm |
| 24-07.9a | received power | -0.68 | dBm |
| 24-07.9b | margin | 7.32 | dB |
| 24-07.10a | largest RF | 597 | Ω |
| 24-07.10b | RF noise density | 5.27 | pA/√Hz |
| 24-07.10c | RF noise current | 0.91 | µA |
| 24-07.11a | spacing | 0.572 | nm |
| 24-07.11b | 16-channel span | 8.59 | nm |
| 24-07.12a | eye shrink | 2 | |
| 24-07.12b | electrical SNR drop | 6 | dB |
| 24-07.12c0 | new Q | 3.53 | |
| 24-07.12c | new BER | 2.1e-4 | |
| 24-07.13a | extinction ratio | 8.72 | |
| 24-07.13b | extinction ratio in dB | 9.41 | dB |
