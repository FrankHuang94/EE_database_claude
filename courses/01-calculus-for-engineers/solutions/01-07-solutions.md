# Solutions 01-07 · Applications of Integration

Problems: [01-07 problems](../problems/01-07-problems.md) · Chapter: [01-07](../chapters/01-07-applications-of-integration.md)

Every numerical answer below is listed in the answer key at the end and is recomputed independently by [verify_01_07.py](../verify/verify_01_07.py).

---

## Solutions

### Solution 01-07.1

(a) Full-wave: average $2V_p/\pi = $ **6.366 V**. The square of a rectified sine equals the square of the sine, so RMS $= V_p/\sqrt{2} = $ **7.071 V**.

(b) Half-wave: average $V_p/\pi = $ **3.183 V**. The mean square is half the sine's: $\tfrac{1}{2}\cdot\tfrac{V_p^2}{2} = V_p^2/4$, so RMS $= V_p/2 = $ **5 V**.

(c) Sawtooth $x = 4u$ with $u$ uniform on $[0, 1]$: average $4\times\tfrac{1}{2} = $ **2 V**. Mean square $16\int_0^1u^2\,du = 16/3$, so RMS $= 4/\sqrt{3} = $ **2.309 V**. (This sawtooth runs from 0 to 4 V, not symmetrically about 0, so the $X_p/\sqrt{3}$ rule applies to its full range, not to a ±peak.)

(d) Crest factors: sine **1.414**, square **1**, triangle **1.732**.

### Solution 01-07.2

(a) Average $= DV_p = 0.2\times5 = $ **1 V**. RMS $= \sqrt{D}V_p = \sqrt{0.2}\times5 = $ **2.236 V**.

(b) $P = V_{rms}^2/R = 5/10 = $ **0.5 W**. Equivalently, 2.5 W while on, for 20% of the time.

(c) $1^2/10 = $ **0.1 W**, a factor of 5 too low. A resistor sized for 0.1 W would overheat.

### Solution 01-07.3

(a) $\tfrac{1}{2}(470\times10^{-6})(400^2) = $ **37.6 J**: enough to cause a dangerous shock or a sharp arc. Bleeder resistors discharge such banks after power-off.

(b) $\tfrac{1}{2}(10^{-5})(20^2) = $ **2 mJ**.

### Solution 01-07.4

(a) The mean is $\int_{-\Delta/2}^{\Delta/2}x\frac{1}{\Delta}dx = 0$ (an odd integrand). The variance is $\int_{-\Delta/2}^{\Delta/2}\frac{x^2}{\Delta}dx = \frac{1}{\Delta}\cdot\frac{2}{3}\left(\frac{\Delta}{2}\right)^3 = \frac{\Delta^2}{12}$. For $\Delta = 1$ mV, the RMS is $1/\sqrt{12} = $ **0.2887 mV**.

(b) $P(T > 8760) = e^{-10^{-6}\times8760} = $ **0.9913**.

### Solution 01-07.5

(a) The harmonics are orthogonal, so the mean squares add: $I_{rms} = \sqrt{(10^2 + 3^2 + 1^2)/2} = \sqrt{55} = $ **7.416 A**.

(b) THD $= \sqrt{3^2 + 1^2}/10 = $ **31.62%**.

(c) With harmonics: $I_{rms}^2R = 55\times0.1 = $ **5.5 W**. Fundamental only: $50\times0.1 = $ **5 W**. The harmonics add 10% to the wiring loss while delivering no average power from a sinusoidal source (orthogonality again: $\overline{v_1\,i_n} = 0$ for $n \ne 1$).

### Solution 01-07.6

(a) $p = 325\times8\cos\omega t\cos(\omega t - 45^\circ) = 1300\big[\cos45^\circ + \cos(2\omega t - 45^\circ)\big]$. The second term averages to zero, so $P = 1300\cos45^\circ = $ **919.2 W**.

(b) $S = V_{rms}I_{rms} = (325/\sqrt{2})(8/\sqrt{2}) = $ **1300 VA**, and PF $= \cos45^\circ = $ **0.7071**.

(c) $Q = 1300\sin45^\circ = $ **919.2 var**. At a 45° angle, real and reactive power are equal.

### Solution 01-07.7

(a) $\tfrac{1}{2}(1)(5^2 - 2.5^2) = $ **9.375 J**.

(b) $t = 9.375/0.5 = $ **18.75 s**.

(c) $v(t) = \sqrt{V_1^2 - 2Pt/C} = \sqrt{25 - t}$ V (with $t$ in seconds), reaching 2.5 V at $t = 18.75$ s ✓. The voltage falls *faster* as the capacitor empties, because a constant-power load draws more current at lower voltage.

### Solution 01-07.8

(a) $W = q\Delta V = 10^{-9}\times5 = $ **5 nJ**. Since 1 eV $= 1.602\times10^{-19}$ J, 1 J $= $ **6.242×10^18 eV**.

(b) $F = \dfrac{Q^2}{2\varepsilon_0A} = \dfrac{(10^{-8})^2}{2\times8.854\times10^{-12}\times10^{-4}} = $ **0.05647 N**. At constant charge the force does not depend on the gap.

(c) $W = \int_{1\text{ mm}}^{2\text{ mm}}F\,dd = F\times10^{-3} = $ **5.647×10^−5 J**. The stored energy is $\dfrac{Q^2}{2C} = \dfrac{Q^2d}{2\varepsilon_0A}$, so it doubles when $d$ doubles: from **5.647×10^−5 J** to **1.129×10^−4 J**. The increase, $5.647\times10^{-5}$ J, equals the work ✓.

### Solution 01-07.9

(a) ±1% is ±100 Ω, i.e. ±2σ: **95.45%**.

(b) ±0.5% is ±50 Ω, i.e. ±1σ: **68.27%**.

(c) With σ = 25 Ω, ±50 Ω is ±2σ: **95.45%**. Halving σ makes the tighter specification as achievable as the looser one was. Process improvement shows up as yield in a tighter grade, which sells at a higher price.

### Solution 01-07.10

(a) The rates add: $\lambda = 1000\times2\times10^{-7} = $ **2×10^−4 per hour**, so MTBF $= 1/\lambda = $ **5000 h**.

(b) $e^{-2\times10^{-4}\times720} = e^{-0.144} = $ **0.8659**. About 13% of servers fail within a month, a strong argument for redundancy.

(c) $E[T] = \int_0^\infty t\lambda e^{-\lambda t}dt$. With $u = t$ and $dv = \lambda e^{-\lambda t}dt$ (so $v = -e^{-\lambda t}$):

$$
E[T] = \Big[-te^{-\lambda t}\Big]_0^\infty + \int_0^\infty e^{-\lambda t}dt = 0 + \frac{1}{\lambda}.
$$

### Solution 01-07.11

(a) 16-bit: $6.02\times16 + 1.76 = $ **98.08 dB**. 10-bit: **61.96 dB**.

(b) ENOB $= (70 - 1.76)/6.02 = $ **11.34 bits**.

(c) $10\log_{10}4 = $ **6.021 dB**, which is one bit. Oversampling by 4 buys one bit; 16× buys two. Sigma-delta converters go much further by also shaping the noise away from the signal band ([20](../../20-analog-and-mixed-signal-ic-design/README.md)).

### Solution 01-07.12

(a) $\int_0^\infty2500e^{-2t/\tau}dt = 2500\times\tau/2 = 2500\times0.5\times10^{-3} = $ **1.25 A²s**.

(b) $50^2\times t = 1.25$ gives $t = $ **0.5 ms**: half the time constant, because squaring the exponential halves its time constant.

(c) The 2 A²s fuse survives (1.25 < 2). The 1 A²s fuse blows (1.25 > 1). Inrush must be limited, for example with an NTC thermistor or a soft-start circuit, or a slower fuse chosen.

### Solution 01-07.13

(a) With $x = q/Q$, $E = Q\int_0^1(4.2 - 0.6x - 0.3x^2)\,dx = Q(4.2 - 0.3 - 0.1) = 3.0\text{ Ah}\times3.8\text{ V} = $ **11.4 Wh**.

(b) The charge-weighted average voltage is $E/Q = $ **3.8 V**, against the end-point average of **3.75 V**. The voltage curve bends downward (concave), staying high for most of the discharge and dropping at the end, so the true average sits above the straight-line average. This charge-weighted average is what "nominal voltage" means.

(c) $V = 3.5$ V at $0.3x^2 + 0.6x - 0.7 = 0$, i.e. $x = 0.8257$. The charge left is $(1 - 0.8257)\times3000 = $ **522.8 mAh**. The energy delivered up to that point is $Q(4.2x - 0.3x^2 - 0.1x^3) = $ **9.622 Wh**, leaving **1.778 Wh** unused. A device that works down to 3.3 V would gain over 15% more energy from the same cell.

### Solution 01-07.14

(a) Over each linear ramp the ripple is $\Delta\cdot u$ with $u$ uniform on $[-\tfrac{1}{2}, \tfrac{1}{2}]$, so its mean square is $\Delta^2\int_{-1/2}^{1/2}u^2\,du = \Delta^2/12$. The ripple averages to zero, so it is orthogonal to the DC level: $I_{rms} = \sqrt{I_0^2 + \Delta^2/12} = \sqrt{4 + 0.03} = $ **2.007 A**.

(b) $I_{rms}^2R = 4.03\times0.02 = $ **80.6 mW**. The ripple adds only 0.75%.

(c) The switch carries the same current shape, but only for a fraction $D$ of the time: $I_{rms,sw} = \sqrt{D(I_0^2 + \Delta^2/12)} = \sqrt{0.3\times4.03} = $ **1.100 A**.

### Solution 01-07.15

(a) Two-sided: $2Q(3) = $ **0.270%**, and $2Q(6) = $ **1.97×10^−9**. Peaks beyond 3σ are routine; beyond 6σ, extremely rare. That is why a noise signal's "peak-to-peak" is often quoted as about 6.6σ.

(b) $E\lvert x\rvert = 2\int_0^\infty x\frac{1}{\sigma\sqrt{2\pi}}e^{-x^2/2\sigma^2}dx$. Substitute $u = x^2/(2\sigma^2)$, $du = x\,dx/\sigma^2$: $= \frac{2\sigma}{\sqrt{2\pi}}\int_0^\infty e^{-u}du = \sigma\sqrt{2/\pi}$, i.e. **0.7979σ**.

(c) The meter reads $1.111\times0.7979\sigma = $ **0.8862σ**, an error of **−11.4%**. Average-responding meters under-read noise. Noise must be measured with a true-RMS meter or a spectrum analyzer.

---

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 01-07.1a | full-wave average | 6.366 | V |
| 01-07.1b | full-wave RMS | 7.071 | V |
| 01-07.1c | half-wave average | 3.183 | V |
| 01-07.1d | half-wave RMS | 5 | V |
| 01-07.1e | sawtooth average | 2 | V |
| 01-07.1f | sawtooth RMS | 2.309 | V |
| 01-07.1g | crest factor, sine | 1.414 | — |
| 01-07.1h | crest factor, triangle | 1.732 | — |
| 01-07.2a | average voltage | 1 | V |
| 01-07.2b | RMS voltage | 2.236 | V |
| 01-07.2c | true power | 0.5 | W |
| 01-07.2d | wrong power from average | 0.1 | W |
| 01-07.3a | DC-bus energy | 37.6 | J |
| 01-07.3b | inductor energy | 2 | mJ |
| 01-07.4a | RMS quantization error | 0.2887 | mV |
| 01-07.4b | one-year survival | 0.9913 | — |
| 01-07.5a | RMS current | 7.416 | A |
| 01-07.5b | THD | 31.62 | % |
| 01-07.5c | wiring loss with harmonics | 5.5 | W |
| 01-07.5d | wiring loss, fundamental only | 5 | W |
| 01-07.6a | average power | 919.2 | W |
| 01-07.6b | apparent power | 1300 | VA |
| 01-07.6c | power factor | 0.7071 | — |
| 01-07.6d | reactive power | 919.2 | var |
| 01-07.7a | usable energy | 9.375 | J |
| 01-07.7b | hold-up time | 18.75 | s |
| 01-07.8a | work on 1 nC through 5 V | 5 | nJ |
| 01-07.8b | eV per joule | 6.242×10^18 | — |
| 01-07.8c | plate force | 0.05647 | N |
| 01-07.8d | work to separate | 5.647×10^-5 | J |
| 01-07.8e | energy at 1 mm | 5.647×10^-5 | J |
| 01-07.8f | energy at 2 mm | 1.129×10^-4 | J |
| 01-07.9a | within ±1 % | 95.45 | % |
| 01-07.9b | within ±0.5 % | 68.27 | % |
| 01-07.9c | within ±0.5 % at σ = 25 Ω | 95.45 | % |
| 01-07.10a | server failure rate | 2×10^-4 | 1/h |
| 01-07.10b | MTBF | 5000 | h |
| 01-07.10c | 30-day survival | 0.8659 | — |
| 01-07.11a | ideal SNR, 16 bits | 98.08 | dB |
| 01-07.11b | ideal SNR, 10 bits | 61.96 | dB |
| 01-07.11c | ENOB at 70 dB | 11.34 | bits |
| 01-07.11d | gain from 4× oversampling | 6.021 | dB |
| 01-07.12a | inrush I²t | 1.25 | A²s |
| 01-07.12b | equivalent pulse length | 0.5 | ms |
| 01-07.13a | energy | 11.4 | Wh |
| 01-07.13b | charge-weighted average voltage | 3.8 | V |
| 01-07.13c | end-point average | 3.75 | V |
| 01-07.13d | charge left at 3.5 V | 522.8 | mAh |
| 01-07.13e | energy used to 3.5 V | 9.622 | Wh |
| 01-07.13f | energy left unused | 1.778 | Wh |
| 01-07.14a | inductor RMS current | 2.007 | A |
| 01-07.14b | inductor conduction loss | 80.6 | mW |
| 01-07.14c | switch RMS current | 1.100 | A |
| 01-07.15a | P(abs x > 3σ) | 0.270 | % |
| 01-07.15b | P(abs x > 6σ) | 1.97×10^-9 | — |
| 01-07.15c | mean of abs x, over σ | 0.7979 | — |
| 01-07.15d | meter reading / σ | 0.8862 | — |
| 01-07.15e | meter error | −11.4 | % |
