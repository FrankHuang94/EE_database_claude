# Solutions 16-06 · FIR Filter Design

Problems: [16-06 problems](../problems/16-06-problems.md) · Chapter: [16-06](../chapters/16-06-fir-filter-design.md). Every number below is recomputed by [verify_16_06.py](../verify/verify_16_06.py): responses with `scipy.signal.freqz`, window and Kaiser designs against `scipy.signal.firwin`, equiripple designs with `scipy.signal.remez`, and order estimates from their formulas.

---

## Solutions

### Solution 16-06.1

| | Taps | Type | Delay (samples) | $\lvert H(e^{j0})\rvert$ | $\lvert H(e^{j\pi})\rvert$ |
|---|---|---|---|---|---|
| (a) | $(1, -2, 1)$ | I | 1 | 0 | 4 |
| (b) | $(1, 3, 3, 1)$ | II | 1.5 | 8 | 0 |
| (c) | $(1, 0, -1)$ | III | 1 | 0 | 0 |
| (d) | $(1, -3, 3, -1)$ | IV | 1.5 | 0 | 8 |
| (e) | $(1, 2, 3)$ | not linear phase | — | 6 | 2 |

The gains are $\lvert\sum h[n]\rvert$ at $\omega = 0$ and $\lvert\sum (-1)^n h[n]\rvert$ at $\omega = \pi$. A high-pass filter needs a nonzero gain at $\pi$: only types I and IV qualify, so (a) and (d) (indeed both are differences, $(1 - z^{-1})^2$ and $(1 - z^{-1})^3$, which block DC). Type II (b) has a forced zero at $\pi$, type III (c) forced zeros at 0 and $\pi$ (it is a band-pass, $1 - z^{-2}$), and (e) has no symmetry, so its phase is not linear.

### Solution 16-06.2

(a) $\delta_p = (10^{0.025} - 1)/(10^{0.025} + 1)$ = **0.02877**; $\delta_s = 10^{-2}$ = 0.01. The window method must meet the smaller, $\delta = 0.01$: $A$ = **40** dB.

(b) $\delta_p = (10^{0.0005} - 1)/(10^{0.0005} + 1)$ = **0.0005756**; $\delta_s = 10^{-4}$. The window method must meet $\delta = 10^{-4}$: $A$ = **80** dB.

The passband tolerance is looser than the stopband's in both cases, about three times in (a) and six times in (b), and the window design will waste it.

### Solution 16-06.3

With $m = n - 3$: $h[3] = \omega_c/\pi = 1/3$ = **0.3333**; $h[3 \pm 1] = \sin(\pi/3)/\pi$ = **0.2757**; $h[3 \pm 2] = \sin(2\pi/3)/(2\pi)$ = **0.1378**; $h[3 \pm 3] = \sin\pi/(3\pi) = 0$. The DC gain is the sum, $0.3333 + 2(0.2757 + 0.1378 + 0)$ = **1.1603**. It is not 1 because truncation discards the ideal response's tails, whose sum (alternating in sign) is $1 - 1.1603$: the passband ripple of Gibbs, here sampled at $\omega = 0$.

### Solution 16-06.4

Evaluating $A(\omega)$ densely below the cutoff:

| $M$ | Overshoot | Peak below the cutoff | Prediction $2\pi/(M + 1)$ |
|---|---|---|---|
| 30 | **8.19**% | **0.1953** rad | 0.2027 rad |
| 300 | **9.03**% | **0.02094** rad | 0.02087 rad |

The peak moved ten times closer to the cutoff, as predicted, but the overshoot did not fall; it rose slightly. Both are near the 8.95% limit, perturbed by the ringing from the band's other edge at $-0.3\pi$, which adds or subtracts depending on its phase at the peak and fades as $M$ grows.

### Solution 16-06.5

(a) $\delta_p = 10^{0.05/20} - 1$ = **0.005773** and $\delta_s = 10^{-2.5}$ = **0.003162**. The window method designs for the smaller, $A$ = **50** dB.

(b) Hann (−43.9 dB) falls short. Hamming (−54.2 dB) qualifies, with $M \ge 2\pi \times 3.3/(0.05\pi)$ = **132**. Blackman (−75.3 dB) qualifies but needs $2\pi \times 5.6/(0.05\pi)$ = **224**, **70**% more taps for attenuation that is not needed.

(c) $A = 50$ falls in the middle range: $\beta = 0.5842(29)^{0.4} + 0.07886 \times 29$ = **4.534**, and $M = (50 - 8)/(2.285 \times 0.05\pi)$ = **117.02**, rounded up to **118**.

(d) Hamming, $M$ = 132: **52.31** dB of attenuation, passband within **±0.021** dB. Kaiser, $M$ = 118: **50.04** dB, passband within **±0.0277** dB. Both meet the specification; the Kaiser design is **14** taps shorter, because it does not carry Hamming's 2 dB of unneeded attenuation.

### Solution 16-06.6

(a) $\beta = 0.1102(70 - 8.7)$ = **6.755**; $\Delta\omega = 0.05\pi$ = **0.1571**; $M = 62/(2.285 \times 0.1571)$ = **172.74**, so $M$ = 173. Checked: **69.93** dB in the stopband, and the passband error **3.187** × 10⁻⁴ just exceeds $\delta = 3.162 \times 10^{-4}$. Both bands miss by about 0.07 dB.

(b) *Adding taps at $\beta = 6.755$:* the attenuation creeps up and first clears 70 dB at $M$ = **192**: 19 extra taps, because attenuation belongs to the window's shape, not its length. *Re-running for 71 dB:* $\beta = 0.1102 \times 62.3$ = **6.865** and $M = 63/(2.285 \times 0.1571)$ = **175.52**, so $M$ = 176, which gives **70.24** dB and meets both bands: 3 extra taps. Raise $\beta$ (with a margin in $A$) for attenuation; raise $M$ for transition width.

### Solution 16-06.7

(a) From §3.6 with $N = 15$, $M/2 = 7$: $h[7 + m] = \frac1{15}\big[1 + 2\cos(2\pi m/15) + 2\cos(4\pi m/15)\big]$.

- $m = 0$: $h[7] = 5/15$ = **0.3333**.
- $m = \pm1$: $\cos 24° = 0.91355$, $\cos 48° = 0.66913$, so $h[6] = h[8] = (1 + 1.82709 + 1.33826)/15$ = **0.2777**.
- $m = -7$: $\cos 168° = -0.97815$, $\cos 336° = 0.91355$, so $h[0] = h[14] = (1 - 1.95630 + 1.82709)/15$ = **0.05805**.

(b) $A(\omega_k) = h[7] + 2\sum_{m=1}^{7} h[7 - m]\cos(m\omega_k)$. Substituting the cosine formula for the taps and using the orthogonality of cosines over a full period (16-03 §3.1) leaves exactly $A_k$: 1 for $k \le 2$ and 0 for $k \ge 3$. (The lab confirms it numerically to $10^{-15}$.)

(c) Midway, at $\omega = 2\pi \times 2.5/15$, the interpolated response is **0.538**: roughly half-way down, as the Dirichlet interpolation of a jump from 1 to 0 should give.

### Solution 16-06.8

(a) $W = \delta_p/\delta_s$ = **10** in the stopband (1 in the passband).

(b) $\delta_p\delta_s = 10^{-5}$, so $-10\log_{10}(\delta_p\delta_s) = 50$, and $\Delta\omega = 2\pi \times 0.02 = 0.04\pi$. Kaiser: $M \approx (50 - 13)/(2.324 \times 0.04\pi)$ = **126.7**, so 127 (128 taps). Bellanger: $N \approx \frac23\log_{10}(10^4) \times 50$ = **133.3**, so 134 taps.

(c) The shortest equiripple filter that meets the specification has **130** taps ($M$ = 129). Kaiser's estimate was 2 taps short, Bellanger's 4 taps long: a few taps either way, which is why every design is checked.

### Solution 16-06.9

Without folding: 255 multiplications per output. With folding: $(255 + 1)/2$ = **128** (127 pre-added pairs plus the middle tap). Per second with folding: $128 \times 100 \times 10^6$ = **12.8** × 10⁹. Each slice delivers $400 \times 10^6$ per second, so folded: $12.8 \times 10^9/(400 \times 10^6)$ = **32** slices; unfolded: $255 \times 10^8/(4 \times 10^8) = 63.75$, so **64** slices. Folding halves the DSP budget, which is why the slices contain a pre-adder.

### Solution 16-06.10

For three taps, $A(\omega) = a_0 + a_1\cos\omega$ with $L = 1$: the theorem needs $L + 2 = 3$ alternations. With $\cos(\pi/3) = 0.5$, $\cos(\pi/2) = 0$, $\cos\pi = -1$, impose $E(\pi/3) = -\delta$, $E(\pi/2) = +\delta$, $E(\pi) = -\delta$:

$$
a_0 + 0.5a_1 - 1 = -\delta, \qquad a_0 = \delta, \qquad a_0 - a_1 = -\delta .
$$

The second and third give $a_1 = 2\delta$; the first then gives $\delta + \delta - 1 = -\delta$, so $\delta$ = **1/3** (0.3333), $a_0$ = **1/3**, $a_1$ = **2/3**.

*Check:* $A(\omega) = \frac13 + \frac23\cos\omega$ decreases monotonically. In the passband it runs from $A(0) = 1$ (error 0) to $A(\pi/3) = 2/3$ (error $-1/3$); in the stopband from $1/3$ at $\pi/2$ to $-1/3$ at $\pi$. The error never exceeds $1/3$ and alternates three times, so this is the unique minimax filter. Its taps are $h = (a_1/2, a_0, a_1/2) = (1, 1, 1)/3$: **the 3-tap moving average** is the optimal 3-tap low-pass filter for these bands. (SciPy's `remez` returns the same taps.) Its error of 1/3, only **9.5** dB below the passband, shows how little three taps can do.

### Solution 16-06.11

$\delta_p = 0.005756$ (0.1 dB peak to peak), $\delta_s = 10^{-4}$, $-10\log_{10}(\delta_p\delta_s)$ = **62.40**.

(a) At 122.88 MS/s: $\Delta\omega = 2\pi \times 1/122.88$ = **0.05113** rad/sample; $M \approx (62.40 - 13)/(2.324 \times 0.05113)$ = **415.7**, so $M$ = 416 and 417 taps, **209** multipliers after folding, $209 \times 122.88 \times 10^6$ = **25.68** × 10⁹ multiplications per second.

(b) At 30.72 MS/s: $\Delta\omega$ is four times wider (**0.2045** rad/sample); $M \approx$ **103.9**, so $M$ = 104 and 105 taps, **53** multipliers, $53 \times 30.72 \times 10^6$ = **1.628** × 10⁹ per second.

(c) The ratio is $25.68/1.628$ = **15.8**: a quarter of the taps, each computed a quarter as often, so about $4^2 = 16$ (not exactly, because of rounding to whole taps). Narrow filtering belongs at the lowest rate (16-09).

(d) The shortest equiripple filters that meet the specification have **416** taps at 122.88 MS/s and **104** taps at 30.72 MS/s, one tap fewer than the estimates in both cases.

### Solution 16-06.12

(a) The truncated ideal taps are $h[M/2 + m] = w[M/2 + m]\sin(\pi m/2)/(\pi m)$. For even $m \ne 0$, $\sin(\pi m/2) = 0$, whatever the window. The middle tap is $w[M/2] \times (\omega_c/\pi) = 1/2$.

(b) Write $A(\omega) = h_c + 2\sum_{m \ge 1} h_m\cos(m\omega)$ with $h_c = 1/2$ and $h_m = h[M/2 + m]$. Then $A(\pi - \omega) = h_c + 2\sum h_m\cos(m\pi - m\omega) = h_c + 2\sum h_m(-1)^m\cos(m\omega)$. Only odd $m$ have $h_m \ne 0$, and for them $(-1)^m = -1$, so $A(\pi - \omega) = h_c - (A(\omega) - h_c) = 1 - A(\omega)$. At $\omega = \pi/2$ this gives $2A(\pi/2) = 1$. The response is antisymmetric about the point $(\pi/2, 1/2)$: passband and stopband ripples are mirror images.

(c) $M/2 = 23$; the nonzero offsets are the middle and the odd offsets $\pm1, \pm3, \dots, \pm23$ (12 on each side): **25** nonzero taps. Folded, the 12 symmetric pairs need **12** general multipliers, and the middle tap of 1/2 is a shift. A general 47-tap symmetric filter needs **24**: the half-band structure halves the cost again (16-09). (Choosing $M/2$ odd matters: with $M/2$ even the two end taps would be zero and wasted.)

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 16-06.1a | type of (a) | 1 | — |
| 16-06.1b | gain of (a) at π | 4 | — |
| 16-06.1c | type of (b) | 2 | — |
| 16-06.1d | delay of (b) | 1.5 | samples |
| 16-06.1e | gain of (b) at 0 | 8 | — |
| 16-06.1f | type of (c) | 3 | — |
| 16-06.1g | type of (d) | 4 | — |
| 16-06.1h | gain of (d) at π | 8 | — |
| 16-06.1i | gain of (e) at 0 | 6 | — |
| 16-06.1j | gain of (e) at π | 2 | — |
| 16-06.2a | δp for 0.5 dB | 0.02877 | — |
| 16-06.2b | attenuation for (a) | 40 | dB |
| 16-06.2c | δp for 0.01 dB | 0.0005756 | — |
| 16-06.2d | attenuation for (b) | 80 | dB |
| 16-06.3a | h[3] | 0.3333 | — |
| 16-06.3b | h[2] | 0.2757 | — |
| 16-06.3c | h[1] | 0.1378 | — |
| 16-06.3d | DC gain | 1.1603 | — |
| 16-06.4a | overshoot, M = 30 | 8.19 | % |
| 16-06.4b | peak offset, M = 30 | 0.1953 | rad |
| 16-06.4c | overshoot, M = 300 | 9.03 | % |
| 16-06.4d | peak offset, M = 300 | 0.02094 | rad |
| 16-06.5a | δp | 0.005773 | — |
| 16-06.5b | δs | 0.003162 | — |
| 16-06.5c | design attenuation | 50 | dB |
| 16-06.5d | Hamming order | 132 | — |
| 16-06.5e | Blackman order | 224 | — |
| 16-06.5f | Kaiser β | 4.534 | — |
| 16-06.5g | Kaiser order estimate | 117.02 | — |
| 16-06.5h | Kaiser order | 118 | — |
| 16-06.5i | Hamming attenuation | 52.31 | dB |
| 16-06.5j | Kaiser attenuation | 50.04 | dB |
| 16-06.5k | Kaiser passband deviation | 0.0277 | dB |
| 16-06.5l | Hamming passband deviation | 0.021 | dB |
| 16-06.5m | Blackman extra taps over Hamming | 70 | % |
| 16-06.5n | taps saved by Kaiser | 14 | — |
| 16-06.6a | β | 6.755 | — |
| 16-06.6b | order estimate | 172.74 | — |
| 16-06.6c | attenuation at M = 173 | 69.93 | dB |
| 16-06.6d | order needed at the same β | 192 | — |
| 16-06.6e | β for 71 dB | 6.865 | — |
| 16-06.6f | order estimate for 71 dB | 175.52 | — |
| 16-06.6g | attenuation at M = 176 | 70.24 | dB |
| 16-06.6h | transition width | 0.1571 | rad/sample |
| 16-06.6i | passband error at M = 173 | 3.187e-4 | — |
| 16-06.7a | h[7] | 0.3333 | — |
| 16-06.7b | h[6] | 0.2777 | — |
| 16-06.7c | h[0] | 0.05805 | — |
| 16-06.7d | midway response | 0.538 | — |
| 16-06.8a | stopband weight | 10 | — |
| 16-06.8b | Kaiser order estimate | 126.7 | — |
| 16-06.8c | Bellanger length estimate | 133.3 | taps |
| 16-06.8d | actual shortest length | 130 | taps |
| 16-06.9a | folded multiplications per output | 128 | — |
| 16-06.9b | multiplications per second | 12.8 | G/s |
| 16-06.9c | slices, folded | 32 | — |
| 16-06.9d | slices, unfolded | 64 | — |
| 16-06.10a | minimax error | 0.3333 | — |
| 16-06.10b | a0 | 0.3333 | — |
| 16-06.10c | a1 | 0.6667 | — |
| 16-06.10d | stopband depth | 9.5 | dB |
| 16-06.11a | ripple-product term | 62.40 | dB |
| 16-06.11b | order estimate at 122.88 MS/s | 415.7 | — |
| 16-06.11c | multipliers at 122.88 MS/s | 209 | — |
| 16-06.11d | multiplications per second at 122.88 MS/s | 25.68 | G/s |
| 16-06.11e | order estimate at 30.72 MS/s | 103.9 | — |
| 16-06.11f | multipliers at 30.72 MS/s | 53 | — |
| 16-06.11g | multiplications per second at 30.72 MS/s | 1.628 | G/s |
| 16-06.11h | cost ratio | 15.8 | — |
| 16-06.11i | actual length at 122.88 MS/s | 416 | taps |
| 16-06.11j | actual length at 30.72 MS/s | 104 | taps |
| 16-06.11k | transition width at 122.88 MS/s | 0.05113 | rad/sample |
| 16-06.11l | transition width at 30.72 MS/s | 0.2045 | rad/sample |
| 16-06.12a | nonzero taps | 25 | — |
| 16-06.12b | half-band multipliers | 12 | — |
| 16-06.12c | general 47-tap multipliers | 24 | — |
