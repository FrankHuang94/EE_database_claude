# Solutions 21-05 · Mixers

Problems: [21-05 problem set](../problems/21-05-problems.md) · Chapter: [21-05](../chapters/21-05-mixers.md). Every number below is recomputed by [verify_21_05.py](../verify/verify_21_05.py).

---

## Solutions

### Solution 21-05.1

With a high-side LO, $f_{LO} = f_{RF} + f_{IF}$ = **5.90** GHz, and the image lies the same distance above the LO: $f_{LO} + f_{IF}$ = **6.00** GHz.

### Solution 21-05.2

The 0/1 waveform is $\tfrac12 + \tfrac12s(t)$, whose fundamental is $\tfrac12 \cdot 4/\pi = 2/\pi$; half of that reaches the difference frequency: $1/\pi$, or **−9.94** dB, which is **6.02** dB below the double-balanced $2/\pi$.

### Solution 21-05.3

$G_c = (2/\pi)g_mR_L = 10^{12/20}$ = 3.981, so $g_m = 3.981\pi/(2 \times 400)$ = **15.6** mS.

### Solution 21-05.4

(a) With $\varepsilon$ = 0.03 and θ = 0.5°, the exact formula gives **36.24** dB. (b) Solving the exact formula for 45 dB with θ = 0.3° gives $\varepsilon$ = **1.00**%. In the small-error budget $\varepsilon^2 + \theta^2 = 4 \times 10^{-4.5}$, the 0.3° phase error takes about a fifth and the gain error the rest.

### Solution 21-05.5

With $\varepsilon$ = 0 the exact formula's numerator is $2 + 2\cos\theta$ and its denominator $2 - 2\cos\theta$, so

$$
\text{IRR} = \frac{1 + \cos\theta}{1 - \cos\theta} = \frac{2\cos^2(\theta/2)}{2\sin^2(\theta/2)} = \cot^2\frac\theta2 .
$$

For θ = 2°: $\cot^2 1°$ = 3282.6, **35.16** dB; the approximation $4/\theta^2$ with θ = 0.03491 rad gives **35.16** dB too, because $\cot x \approx 1/x$ for small $x$.

### Solution 21-05.6

The output noise density from each passed band is the source density times that band's power conversion gain; the signal band has $g = 4/\pi^2$.

- Signal and image pass: noise $2g$, signal $g$: $F$ = 2, **3.01** dB.
- Signal, image and the two bands around $3f_{LO}$ pass: noise $2g + 2g/9$: $F$ = 2.222, **3.47** dB.

### Solution 21-05.7

$F = 1.318 + (15.85 - 1)/63.10 + (100 - 1)/(63.10 \times 10)$ = 1.710, NF = **2.33** dB. The mixer's 12 dB noise figure adds 0.24 in noise factor even behind 18 dB of LNA gain.

### Solution 21-05.8

IM3 = $-2(15 + 10)$ = **−50** dBc. For −70 dBc, $\text{IP3} = P_{in} + 70/2$ = **25** dBm.

### Solution 21-05.9

By FFT of the composite LO:

- 2% weight error: 3rd at **−49.6** dB, 5th at **−54.1** dB. The estimate $\delta/6$ gives $20\log_{10}(0.02/6)$ = **−49.5** dB.
- 0.5° phase error: 3rd at **−50.2** dB, 5th at **−50.2** dB.

Half a degree of LO phase error is as damaging as 2% of weight error.

### Solution 21-05.10

$C = 1/(\pi NR_s\,\text{BW}) = 1/(\pi \times 8 \times 50 \times 20 \times 10^6)$ = **39.8** pF, and the centre loss is $[(8/\pi)\sin(\pi/8)]^{-2}$, **0.45** dB.

### Solution 21-05.11

(a) The leaked LO, $0.3\ \text{mV}\cos(\omega_{LO}t + \phi)$, multiplied by the square wave gives a DC term $(2/\pi)(0.3\ \text{mV})\cos\phi$: up to **0.191** mV, depending on the phase of the leakage path.

(b) −90 dBm in 50 Ω is an amplitude of $\sqrt{100 \times 10^{-12}}$ = **10** µV, converted to **6.37** µV at the IF. The offset is about 30 times larger: **29.5** dB.

(c) After 60 dB of gain the offset is **0.191** V against a 6.37 mV signal. A DC offset of that size consumes the ADC's range and can saturate later stages; and because the leakage depends on the antenna's surroundings, it changes over time. Zero-IF receivers therefore remove DC with high-pass coupling or a DC-offset servo and calibrate it, and design the LO distribution for high isolation.

### Solution 21-05.12

The 3rd harmonic lands in the band when $3f_{LO} \le 800$ MHz, i.e. for $f_{LO}$ from 50 MHz to **266.7** MHz; the 5th when $5f_{LO} \le 800$ MHz, from 50 to **160** MHz. Over a third of the tuning range, an unfiltered square-wave mixer would also receive strong signals at 3 or 5 times the tuned frequency. The mixer needs harmonic rejection (an eight-phase or harmonic-reject LO) or a tracking filter.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 21-05.1a | LO | 5.90 | GHz |
| 21-05.1b | image | 6.00 | GHz |
| 21-05.2a | single-balanced gain | −9.94 | dB |
| 21-05.2b | difference | 6.02 | dB |
| 21-05.3a | gm | 15.6 | mS |
| 21-05.4a | IRR at 3 % and 0.5° | 36.24 | dB |
| 21-05.4b | gain error for 45 dB | 1.00 | % |
| 21-05.5a | IRR at 2°, exact | 35.16 | dB |
| 21-05.5b | IRR at 2°, approximate | 35.16 | dB |
| 21-05.6a | NF with image | 3.01 | dB |
| 21-05.6b | NF with image and 3rd harmonic | 3.47 | dB |
| 21-05.7a | cascade NF | 2.33 | dB |
| 21-05.8a | IM3 | −50 | dBc |
| 21-05.8b | IP3 for −70 dBc | 25 | dBm |
| 21-05.9a | 3rd, 2 % weight error | −49.6 | dB |
| 21-05.9b | 5th, 2 % weight error | −54.1 | dB |
| 21-05.9c | estimate | −49.5 | dB |
| 21-05.9d | 3rd, 0.5° | −50.2 | dB |
| 21-05.9e | 5th, 0.5° | −50.2 | dB |
| 21-05.10a | C | 39.8 | pF |
| 21-05.10b | centre loss | 0.45 | dB |
| 21-05.11a | DC offset | 0.191 | mV |
| 21-05.11b | signal amplitude | 10 | µV |
| 21-05.11c | IF amplitude | 6.37 | µV |
| 21-05.11d | offset over signal | 29.5 | dB |
| 21-05.11e | offset after 60 dB | 0.191 | V |
| 21-05.12a | highest LO for an in-band 3rd | 266.7 | MHz |
| 21-05.12b | highest LO for an in-band 5th | 160 | MHz |
