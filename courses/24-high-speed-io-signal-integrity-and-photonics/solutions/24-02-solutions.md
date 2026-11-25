# Solutions 24-02 · Eye Diagrams, Jitter and BER

Problems: [24-02 problems](../problems/24-02-problems.md) · Chapter: [24-02](../chapters/24-02-eye-diagrams-jitter-ber.md)

Every number is recomputed by [verify_24_02.py](../verify/verify_24_02.py).

---

## Solutions

### Solution 24-02.1

$Q^{-1}(p) = \sqrt2\,\text{erfc}^{-1}(2p)$, evaluated numerically.

- (a) $Q^{-1}(10^{-4})$ = **3.719**, multiplier **7.438**.
- (b) $Q^{-1}(10^{-10})$ = **6.361**, multiplier **12.72**.
- (c) $Q^{-1}(10^{-14})$ = **7.651**, multiplier **15.30**.

Ten orders of magnitude in BER, from 10⁻⁴ to 10⁻¹⁴, only double the multiplier.

### Solution 24-02.2

- (a) Thermal noise is **RJ**: Gaussian and unbounded, so it adds in quadrature with other random sources.
- (b) Supply ripple at a single frequency modulates the edge timing sinusoidally: **PJ**, which is bounded and adds linearly.
- (c) A pulse-response tail makes each edge's timing depend on the preceding bits: **DDJ** (ISI), bounded, added linearly.
- (d) An unequal high and low time shifts alternate edges: duty-cycle distortion, a form of **DDJ**, bounded, added linearly.
- (e) Crosstalk from unrelated data is bounded (a finite number of aggressors with finite coupling) but uncorrelated with the victim's data: **BUJ**, added linearly in a worst-case budget.

Only (a) belongs in the root-sum-square; (b)–(e) are summed in DJ.

### Solution 24-02.3

(a) For $0 \le t \le$ UI the output is $1 - e^{-t/\tau}$, which rises monotonically. At $t$ = UI the input steps back to zero, and from then on the output decays as $(1 - e^{-UI/\tau})e^{-(t - UI)/\tau}$. A rising curve followed by a falling one peaks at the junction, $t$ = 1 UI. With UI/τ = 2, sampling at $t$ = 1 UI gives $h_0 = 1 - e^{-2}$. Sampling $k$ UIs later gives $h_k = h_0e^{-2k}$. Before the pulse starts the output is zero, so there are no pre-cursors.

(b) $h_0$ = **0.8647**, $h_1 = 0.8647e^{-2}$ = **0.1170** and $h_2$ = **0.0158**.

(c) The ISI is a geometric series:

$$
\sum_{k \ge 1}h_k = h_0\frac{e^{-2}}{1 - e^{-2}} = e^{-2} = 0.1353 .
$$

So the ISI sum is **0.1353**, since $h_0 = 1 - e^{-2}$.

(d) NRZ: $h_0 - e^{-2} = 1 - 2e^{-2}$ = **0.7293**. PAM4: $h_0/3 - e^{-2}$ = **0.1529**.

The NRZ eye loses only 27% to ISI, but the PAM4 eye, whose signal is a third as large, keeps only 15% of the swing.

### Solution 24-02.4

The ISI magnitudes sum to $0.05 + 0.25 + 0.05 = 0.35$.

(a) NRZ: $0.60 - 0.35$ = **0.25**. PAM4: $0.60/3 - 0.35$ = **−0.15**, so the PAM4 eye is closed.

(b) Without $h_1$ the remaining ISI is 0.10. NRZ: $0.60 - 0.10$ = **0.50**. PAM4: $0.20 - 0.10$ = **0.10**, now open.

One tap that cancels the dominant post-cursor doubles the NRZ eye and opens the PAM4 eye. That is why DFEs were standard in NRZ SerDes and why their single remaining tap still matters in PAM4 receivers (24-03).

### Solution 24-02.5

The half-eye is 30 mV.

(a) BER = $Q(30/4) = Q(7.5)$ = **3.2** × 10⁻¹⁴.

(b) $\sigma_n = 30/Q^{-1}(10^{-12}) = 30/7.034$ = **4.26** mV.

(c) $\sigma_n = 30/7.941$ = **3.78** mV.

Tightening the target by 1,000 times costs only 11% in allowed noise.

### Solution 24-02.6

(a) Each 40 mV eye has a half-height of 20 mV, so the argument is $20/3$ = 6.667. SER $= 1.5\,Q(6.667)$ = **1.96** × 10⁻¹¹ and BER = **9.8** × 10⁻¹².

(b) The NRZ half-eye is 60 mV: BER = $Q(20)$ = **2.8** × 10⁻⁸⁹, effectively error-free.

(c) The PAM4 eye is a third of the NRZ eye for the same swing, so to match the eye-to-noise ratio the swing must triple: $20\log_{10}3$ = **9.54** dB.

The 9.5 dB penalty is the price of carrying two bits per symbol. PAM4 recovers it only when halving the Nyquist frequency saves more than 9.5 dB of channel loss, or when FEC relaxes the BER target (Problem 24-02.14).

### Solution 24-02.7

UI = 1/53.125 GBd = **18.82** ps.

(a) TJ = $14.07 \times 0.25 + 2.0$ = **5.52** ps. The opening is $18.82 - 5.52$ = **13.31** ps, or **0.707** UI.

(b) TJ = $15.88 \times 0.25 + 2.0$ = **5.97** ps. The opening is **12.85** ps, or **0.683** UI.

### Solution 24-02.8

On a Q-scale each wall is the line $Q^{-1}(\text{BER}) = (x - DJ/2)/\sigma$. Here $Q^{-1}(10^{-5})$ = 4.265 and $Q^{-1}(10^{-8})$ = 5.612.

(a) $\sigma = (2.55 - 2.10)/(5.612 - 4.265)$ = **0.334** ps. Then $DJ/2 = 2.10 - 4.265 \times 0.3340$ = 0.6753 ps, so DJ(δδ) = **1.35** ps.

(b) $x = 0.6753 + 7.034 \times 0.3340$ = **3.03** ps.

(c) The opening is $18.82 - 2 \times 3.025$ = **12.77** ps, or **0.679** UI.

### Solution 24-02.9

(a) TJ ≤ $0.40 \times 18.82$ = **7.53** ps. DJ = $0.8 + 2.0 + 0.7$ = **3.5** ps.

(b) $14.07\,\sigma_{RJ} \le 7.53 - 3.5$, so $\sigma_{RJ} \le 4.029/14.07$ = **0.286** ps.

(c) Random sources add in quadrature, so the reference clock may contribute $\sqrt{0.2864^2 - 0.15^2 - 0.12^2}$ = **0.212** ps rms.

Every picosecond of DJ removed frees $1/14.07$ ps of RJ budget. A clock vendor asked for 0.2 ps is being asked for something comparable to the PCIe 5.0 limit of 0.15 ps.

### Solution 24-02.10

With zero errors in $N$ bits, confidence $C$ that the BER is below $p$ requires $N = -\ln(1 - C)/p$ (03-05).

(a) $N = 2.996/10^{-12}$ = **3.0** × 10¹² bits, which takes $3.0 \times 10^{12}/106.25 \times 10^9$ = **28.2** s.

(b) $N = 4.605/10^{-12}$ = **4.61** × 10¹² bits, or **43.3** s.

(c) Solve $e^{-\lambda}(1 + \lambda) = 0.05$: λ = **4.744**, so $N$ = **4.74** × 10¹² bits, or **44.6** s.

Allowing one error costs 58% more test time than demanding zero, but it makes the test robust to a single stray error.

### Solution 24-02.11

(a) $f_c = 53.125 \times 10^9/26{,}562.5$ = **2.0** MHz.

(b) $A_{tol} = 0.25\sqrt{1 + (2\ \text{MHz}/100\ \text{kHz})^2} = 0.25\sqrt{401}$ = **5.01** UI.

(c) Setting $A_{tol}$ = 1 UI gives $\sqrt{1 + (f_c/f)^2} = 4$, so $f_c/f = \sqrt{15}$ and $f$ = 2 MHz/3.873 = **516** kHz.

(d) The tracking error is $\lvert1 - H\rvert = (f/f_c)/\sqrt{1 + (f/f_c)^2}$. At 200 kHz, $f/f_c$ = 0.1, giving **0.0995**. At $f_c$ it is $1/\sqrt2$ = **0.707**.

At 200 kHz the CDR removes 90% of the jitter; at its corner it removes only 29%, by amplitude.

### Solution 24-02.12

All amplitudes are in units of half the swing, and σ = 0.05.

(a) The four equally likely patterns put the sample at $0.7 \pm 0.2 \pm 0.1$, that is at 1.0, 0.8, 0.6 and 0.4. The exact BER is

$$
\tfrac14\left[Q(20) + Q(16) + Q(12) + Q(8)\right] \approx \tfrac14Q(8) = 1.56 \times 10^{-16} .
$$

So the exact BER is **1.56** × 10⁻¹⁶. The worst-case bound is $Q(0.4/0.05) = Q(8)$ = **6.22** × 10⁻¹⁶, four times higher.

(b) Worst case: $\sigma = 0.4/7.034$ = **0.0569**. Exact: the worst pattern dominates, so $\tfrac14Q(0.4/\sigma) = 10^{-12}$, giving $\sigma = 0.4/Q^{-1}(4 \times 10^{-12})$ = **0.0585**, only 3% more.

(c) With 20 cursors of 0.015, the worst pattern (all 20 against the bit) has probability $2^{-20}$. Summing $\binom{20}{j}2^{-20}Q\big((0.7 - 0.015(20 - 2j))/0.05\big)$ over all $j$ gives a BER of **6.7** × 10⁻²², against the same 6.22 × 10⁻¹⁶ bound. Solving for 10⁻¹² gives σ = **0.0779**, which is 37% more noise than the worst-case analysis allows.

With a few large cursors the worst-case eye is nearly right. With many small cursors, as in a long channel or after imperfect equalization, it is far too pessimistic, which is why COM and modern link simulators use statistical eyes.

### Solution 24-02.13

(a) The level is $\mathcal{L}$ = −140 dBc/Hz = 10⁻¹⁴ /Hz. Integrating both sidebands:

$$
\sigma_t = \frac{\sqrt{2 \times 10^{-14} \times (2 \times 10^7 - 1.2 \times 10^4)}}{2\pi \times 10^8} = 1.01\ \text{ps} .
$$

So $\sigma_t$ = **1.01** ps.

(b) That is **6.7** times the 0.15 ps limit.

(c) Jitter scales as $\sqrt{\mathcal L}$, so the level must fall by $20\log_{10}6.71$ = 16.5 dB, to **−156.5** dBc/Hz.

In practice the PCIe weighting filters suppress much of the low-offset band, so a real clock is judged on its weighted, not its raw, jitter (§3.7).

### Solution 24-02.14

(a) $Q^{-1}(10^{-12}/0.75)$ = **6.994**.

(b) $Q^{-1}(10^{-6}/0.75)$ = **4.695**.

(c) $20\log_{10}(6.994/4.695)$ = **3.46** dB.

(d) $N = 2.996/10^{-6}$ = **3.0** × 10⁶ bits, which takes **23.4** µs at 128 Gb/s.

FEC buys about 3.5 dB, a third of the PAM4 penalty of Problem 24-02.6. It also turns a test that takes tens of seconds into one that takes microseconds, which is why the FBER of 10⁻⁶ can be monitored in the field.

### Solution 24-02.15

(a) COM = $20\log_{10}(30/20)$ = **3.52** dB.

(b) **Yes**: 3.52 dB exceeds the 3 dB threshold.

(c) It fails when $A_{ni} > 30/10^{3/20}$ = **21.2** mV, only 6% above its present value.

A pass by 0.5 dB leaves little room for manufacturing spread in the channel.

### Solution 24-02.16

(a) Take the left crossing's distribution as a Gaussian of rms $RJ$ centred at $-DJ/2$ (relative to the nominal edge). The probability that an edge lands beyond a sampling point $x$ to its right is $Q((x + DJ/2)/RJ)$ for the outer Dirac and $Q((x - DJ/2)/RJ)$ for the inner one; the inner term dominates. Setting $Q((x - DJ/2)/RJ)$ = BER gives $x = DJ/2 + Q^{-1}(\text{BER})\,RJ$: the eye closes by that much from the left, and by symmetry from the right. The total closure is $TJ = 2Q^{-1}(\text{BER})\,RJ + DJ(\delta\delta)$.

(b) Strictly, each Dirac carries half the transitions, and only transitions cause timing errors, so the tail probability is $\tfrac12Q(\cdot)$ times the transition density. The standard convention (§3.5) defines the multiplier from $Q^{-1}(\text{BER})$ alone, which absorbs these factors: at 10⁻¹² it gives 14.07 rather than the 13.87 of $\tfrac12Q$. The difference is small because $Q$ falls so steeply.

(c) $2 \times 7.034 \times 0.2 + 1.5$ = **4.31** ps at 10⁻¹²; $2 \times 7.941 \times 0.2 + 1.5$ = **4.68** ps at 10⁻¹⁵. The UI is 18.82 ps, so the eye is **14.5** ps wide at 10⁻¹².

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 24-02.1a | inverse Q at 1e-4 | 3.719 | |
| 24-02.1a1 | multiplier at 1e-4 | 7.438 | |
| 24-02.1b | inverse Q at 1e-10 | 6.361 | |
| 24-02.1b1 | multiplier at 1e-10 | 12.72 | |
| 24-02.1c | inverse Q at 1e-14 | 7.651 | |
| 24-02.1c1 | multiplier at 1e-14 | 15.30 | |
| 24-02.3b | main cursor | 0.8647 | |
| 24-02.3b1 | first post-cursor | 0.1170 | |
| 24-02.3b2 | second post-cursor | 0.0158 | |
| 24-02.3c | ISI sum | 0.1353 | |
| 24-02.3d | NRZ eye | 0.7293 | |
| 24-02.3d1 | PAM4 eye | 0.1529 | |
| 24-02.3e | NRZ eye lost to ISI | 27 | % |
| 24-02.3e1 | PAM4 eye as share of swing | 15 | % |
| 24-02.4a | NRZ eye | 0.25 | |
| 24-02.4a1 | PAM4 eye | -0.15 | |
| 24-02.4b | NRZ eye with DFE | 0.50 | |
| 24-02.4b1 | PAM4 eye with DFE | 0.10 | |
| 24-02.5a | BER at 4 mV | 3.2e-14 | |
| 24-02.5b | noise for 1e-12 | 4.26 | mV |
| 24-02.5c | noise for 1e-15 | 3.78 | mV |
| 24-02.5d | allowed-noise reduction | 11 | % |
| 24-02.6a0 | Q argument | 6.667 | |
| 24-02.6a | PAM4 SER | 1.96e-11 | |
| 24-02.6a1 | PAM4 BER | 9.8e-12 | |
| 24-02.6b | NRZ BER | 2.8e-89 | |
| 24-02.6c | PAM4 penalty | 9.54 | dB |
| 24-02.6c1 | PAM4 penalty, 2 s.f. | 9.5 | dB |
| 24-02.7a0 | UI | 18.82 | ps |
| 24-02.7a | TJ at 1e-12 | 5.52 | ps |
| 24-02.7a1 | opening at 1e-12 | 13.31 | ps |
| 24-02.7a2 | opening at 1e-12 in UI | 0.707 | UI |
| 24-02.7b | TJ at 1e-15 | 5.97 | ps |
| 24-02.7b1 | opening at 1e-15 | 12.85 | ps |
| 24-02.7b2 | opening at 1e-15 in UI | 0.683 | UI |
| 24-02.8a0 | inverse Q at 1e-5 | 4.265 | |
| 24-02.8a00 | inverse Q at 1e-8 | 5.612 | |
| 24-02.8a | sigma | 0.334 | ps |
| 24-02.8a1 | sigma, 4 s.f. | 0.3340 | ps |
| 24-02.8a2 | half DJ | 0.6753 | ps |
| 24-02.8a3 | DJ | 1.35 | ps |
| 24-02.8b | wall at 1e-12 | 3.03 | ps |
| 24-02.8b1 | wall at 1e-12, 4 s.f. | 3.025 | ps |
| 24-02.8c | opening at 1e-12 | 12.77 | ps |
| 24-02.8c1 | opening in UI | 0.679 | UI |
| 24-02.9a | allowed TJ | 7.53 | ps |
| 24-02.9a1 | total DJ | 3.5 | ps |
| 24-02.9b | largest RJ | 0.286 | ps |
| 24-02.9b0 | TJ minus DJ | 4.029 | ps |
| 24-02.9b1 | largest RJ, 4 s.f. | 0.2864 | ps |
| 24-02.9c | refclk allowance | 0.212 | ps |
| 24-02.10a | bits for 95% | 3.0e12 | |
| 24-02.10a0 | minus log of 0.05 | 2.996 | |
| 24-02.10a1 | time for 95% | 28.2 | s |
| 24-02.10b0 | minus log of 0.01 | 4.605 | |
| 24-02.10b | bits for 99% | 4.61e12 | |
| 24-02.10b1 | time for 99% | 43.3 | s |
| 24-02.10c | Poisson mean, one error | 4.744 | |
| 24-02.10c1 | bits, one error allowed | 4.74e12 | |
| 24-02.10c2 | time, one error allowed | 44.6 | s |
| 24-02.10d | extra time for one error | 58 | % |
| 24-02.11a | CDR corner | 2.0 | MHz |
| 24-02.11b | tolerance at 100 kHz | 5.01 | UI |
| 24-02.11c0 | sqrt 15 | 3.873 | |
| 24-02.11c | frequency of 1 UI tolerance | 516 | kHz |
| 24-02.11d | tracking error at 200 kHz | 0.0995 | |
| 24-02.11d1 | tracking error at corner | 0.707 | |
| 24-02.11e | jitter removed at 200 kHz | 90 | % |
| 24-02.11e1 | jitter removed at corner | 29 | % |
| 24-02.12a | exact BER, two cursors | 1.56e-16 | |
| 24-02.12a1 | worst-case bound | 6.22e-16 | |
| 24-02.12a2 | bound over exact | 4 | |
| 24-02.12b | sigma, worst case | 0.0569 | |
| 24-02.12b1 | sigma, exact | 0.0585 | |
| 24-02.12b2 | extra noise allowed, two cursors | 3 | % |
| 24-02.12c | exact BER, 20 cursors | 6.7e-22 | |
| 24-02.12c1 | sigma, 20 cursors | 0.0779 | |
| 24-02.12c2 | extra noise allowed, 20 cursors | 37 | % |
| 24-02.13a | refclk jitter | 1.01 | ps |
| 24-02.13b | ratio to PCIe 5.0 limit | 6.7 | |
| 24-02.13c0 | required improvement | 16.5 | dB |
| 24-02.13c | phase-noise level for 0.15 ps | -156.5 | dBc/Hz |
| 24-02.13c1 | ratio, 3 s.f. | 6.71 | |
| 24-02.14a | Q for 1e-12 | 6.994 | |
| 24-02.14b | Q for 1e-6 | 4.695 | |
| 24-02.14c | difference | 3.46 | dB |
| 24-02.14c1 | difference, 2 s.f. | 3.5 | dB |
| 24-02.14d | bits for 1e-6 | 3.0e6 | |
| 24-02.14d1 | time at 128 Gb/s | 23.4 | µs |
| 24-02.15a | COM | 3.52 | dB |
| 24-02.15b | margin over threshold | 0.5 | dB |
| 24-02.15c | noise-plus-interference limit | 21.2 | mV |
| 24-02.15c1 | growth before failing | 6 | % |
| 24-02.16a | multiplier with half-Q at 1e-12 | 13.87 | |
| 24-02.16c | TJ at 1e-12 | 4.31 | ps |
| 24-02.16c1 | TJ at 1e-15 | 4.68 | ps |
| 24-02.16c2 | eye width | 14.5 | ps |
