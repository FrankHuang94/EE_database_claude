# Course 16 · Final Exam Solutions (Digital Signal Processing)

Exam: [README.md](README.md). Every number below is recomputed by [verify_16_exam.py](../verify/verify_16_exam.py):

- frequency responses and DFTs by direct evaluation, checked against `numpy.fft` and `scipy.signal.freqz`;
- design formulas from their definitions, and the designs themselves with `scipy.signal` (elliptic, Parks–McClellan), measured on dense grids;
- reflection coefficients by the step-down recursion, checked against the roots;
- multirate, quantization and hardware results from closed forms, checked by simulation where a simulation exists (aliasing by sampling a tone, the dead band by running the recursion, the CORDIC residual by iterating the angle).

---

## Solutions

### Solution 1

(a) The tone aliases to $\lvert 9 - 8\rvert$ = **1** kHz: $\cos(2\pi \cdot 9000\,n/8000) = \cos(2\pi n + 2\pi \cdot 1000\,n/8000)$, and the $2\pi n$ is invisible to the samples.

(b) $\omega = 2\pi \times 1/8 = \pi/4$ = **0.7854** rad/sample.

(c) The 4-point average has $\lvert H(e^{j\omega})\rvert = \left\lvert\dfrac{\sin(2\omega)}{4\sin(\omega/2)}\right\rvert$ (16-01). At DC the gain is **1** (the limit of the ratio, or simply the average of four equal samples). At 1 kHz, $\omega = \pi/4$: $\sin(\pi/2)/(4\sin(\pi/8)) = 1/(4 \times 0.38268)$ = **0.653**. At 2 kHz, $\omega = \pi/2$: $\sin\pi = 0$, so the gain is **0**: four samples span exactly one period of 2 kHz, which averages to zero.

(d) The pole is at $z = 0.5$, inside the unit circle, so the system is **stable**. Its impulse response is $h[n] = 0.5^n u[n]$; it falls by $e$ after $n = 1/\ln 2$ = **1.443** samples.

### Solution 2

(a) $\theta = 2\pi \times 0.06 = 0.37699$ rad, $2\cos\theta = 1.85955$, $2r\cos\theta = 1.84096$, $r^2 = 0.9801$:

$$
H(z) = \frac{1 - 1.8596z^{-1} + z^{-2}}{1 - 1.8410z^{-1} + 0.9801z^{-2}} .
$$

(b) By the rule of 16-02, $\Delta\omega_{3\,\text{dB}} \approx 2(1 - r) = 0.02$ rad/sample, so $\Delta f \approx (1 - r)f_s/\pi$ = **3.18** Hz. Solving $\lvert H\rvert = 1/\sqrt2$ (relative to the DC gain) on both sides of the notch gives **3.20** Hz: the rule is good to about 0.4%.

(c) The poles decay as $r^n = e^{-n/\tau_s}$ with $\tau_s = -1/\ln 0.99$ = **99.5** samples ($\approx 1/(1 - r) = 100$), that is **0.0995** s at 1 kHz. A transient (for example, the hum switching on) takes about $4\tau_s \approx 0.4$ s to settle: the narrow notch rings for a long time.

(d) At $z = 1$: $H(1) = (2 - 1.85955)/(1 - 1.84096 + 0.9801) = 0.14045/0.13914$ = **1.0094**. The far pole and the zeros do not cancel exactly. Multiply the numerator by $g = 1/1.0094$ = **0.9907**, which makes the DC gain exactly 1 and leaves the notch where it is.

### Solution 3

(a) $X[k] = \sum_n x[n]W_8^{kn} = 1 + W_8^k$. So $X[0]$ = **2**, $X[2] = 1 + W_8^2 = 1 - j$, $X[4] = 1 + W_8^4 = 1 - 1$ = **0**, and $\lvert X[1]\rvert = \lvert 1 + e^{-j\pi/4}\rvert = 2\cos(\pi/8)$ = **1.848**.

(b) $\Delta f = f_s/N = 48{,}000/1024$ = **46.875** Hz.

(c) Each block of $N$ outputs contains $M - 1 = 128$ circularly wrapped samples, so $N - M + 1 = 1024 - 129 + 1$ = **896** outputs are valid.

(d) Fast convolution: $4(1024 \times 10 + 1024)/896 = 45{,}056/896$ = **50.3** real multiplications per output. Direct filtering of real data costs 129 per output (65 with symmetry folding, if the filter is linear phase). The FFT method is **2.57** times cheaper than direct filtering here. The advantage grows with $M$, because the FFT's cost per output grows only as $\log N$; for filters of a few tens of taps, direct filtering wins.

### Solution 4

(a) $\log_2 4096$ = **12** stages; $(N/2)\log_2N = 2048 \times 12$ = **24,576** butterflies, each with one complex multiplication by a twiddle. Non-trivial multiplications: $\frac N2\log_2N - \frac{3N}2 + 2 = 24{,}576 - 6144 + 2$ = **18,434** (16-04 §3.5).

(b) $N^2/\bigl(\tfrac N2\log_2N\bigr) = 2N/\log_2N = 8192/12$ = **682.7**.

(c) Even samples $(1, 0)$: $G = (1 + 0, 1 - 0) = (1, 1)$. Odd samples $(2, -1)$: $H = (2 - 1, 2 + 1) = (1, 3)$. The butterflies $X[k] = G[k] + W_4^kH[k]$ and $X[k + 2] = G[k] - W_4^kH[k]$, with $W_4^0 = 1$ and $W_4^1 = -j$, give

$$
X[0] = 1 + 1 = 2, \quad X[1] = 1 + (-j)(3) = 1 - 3j, \quad X[2] = 1 - 1 = 0, \quad X[3] = 1 - (-j)(3) = 1 + 3j .
$$

Check: $X[0] = \sum x = 2$, and $X[3] = X[1]^*$ as it must for real input.

(d) A butterfly can double a magnitude, $\lvert a \pm Wb\rvert \le \lvert a\rvert + \lvert b\rvert$, so the output can grow by $N$ (12 bits here) over all stages. Scaling by 1/2 at each stage keeps the words at their input width and delivers $X[k]/N$. The cost is precision: each shift discards a bit and adds rounding noise, so small signals lose dynamic range, and the scaling is applied even when the data do not grow. It also does not fully rule out overflow, since one component can grow by $1 + \sqrt2$ in a stage; production FFTs add a guard bit, saturate, or use block floating point (16-04 §3.8).

### Solution 5

(a) The bin spacing is $f_s/N = 10^8/8192 = 12{,}207.03$ Hz, so 10 MHz is bin 819.2. Since $8192 = 2^{13}$, any odd bin is relatively prime to $N$; the nearest is $k$ = **819**, at $f = 819 \times 10^8/8192$ = **9.997559** MHz (9,997,558.59 Hz exactly).

(b) As measured: $(70.0 - 1.76)/6.02$ = **11.34** bits. Referred to full scale, the SINAD becomes 71.0 dBFS and the ENOB $(71.0 - 1.76)/6.02$ = **11.50** bits.

(c) The processing gain is $10\log_{10}(N/2) = 10\log_{10}4096$ = **36.12** dB. The Hann window's ENBW of 1.5 bins raises each bin's noise by $10\log_{10}1.5 = 1.76$ dB, so the floor gains $10\log_{10}\bigl(N/(2 \times 1.5)\bigr)$ = **34.36** dB.

(d) The floor sits $\text{SNR} + 34.36 = 72 + 34.36$ = **106.4** dB below the tone (16-05 §3.4). Reading 106 dB as the converter's dynamic range would be the classic mistake: it is the SNR plus the processing gain.

### Solution 6

(a) $\delta_p = (10^{0.005} - 1)/(10^{0.005} + 1)$ = **0.005756** and $\delta_s = 10^{-50/20}$ = **0.003162**. The window method makes both ripples equal, so the smaller tolerance governs: **the stopband**, $A$ = 50 dB. With $21 \le A \le 50$: $\beta = 0.5842 \times 29^{0.4} + 0.07886 \times 29$ = **4.534**. With $\Delta\omega = 2\pi \times 1000/48{,}000$ = 0.1309 rad/sample, $M = (50 - 8)/(2.285 \times 0.1309)$ = **140.4**, so order **141** (142 taps).

(b) $-10\log_{10}(\delta_p\delta_s) = 47.40$ dB, so $M \approx (47.40 - 13)/(2.324 \times 0.1309)$ = **113.1**: order 114 or so, about 20% shorter, because the equiripple design exploits the looser passband tolerance.

(c) A linear-phase filter of order 141 delays by $141/2$ = **70.5** samples, or $70.5/48{,}000$ = **1.469** ms.

(d) 142 taps fold into 71 symmetric pairs: **71** multipliers per output (the even length has no centre tap).

### Solution 7

(a) $\omega_p = 2\pi \times 1/8 = \pi/4$ and $\omega_s = \pi/2$. Prewarped (with $2f_s$ omitted, since only the ratio matters): $\Omega_p = \tan(\pi/8)$ = **0.4142**, $\Omega_s = \tan(\pi/4)$ = **1**, ratio **2.414**. With the factor $2f_s$: 6627 and 16,000 rad/s. $D = (10^{4} - 1)/(10^{0.1} - 1) = 9999/0.25893$ = **38,617**.

(b) Butterworth: $N \ge \log_{10}D/(2\log_{10}2.414) = 4.5868/0.76555$ = **5.99**, so **6**. Chebyshev I: $N \ge \operatorname{arccosh}\sqrt D/\operatorname{arccosh}2.414 = 5.9737/1.5286$ = **3.91**, so **4**.

(c) Use order **4**. The bound exceeds 3 by only 0.0012, so it is tempting to round down; an order-3 elliptic filter with exactly 1 dB ripple and the 2.414 edge ratio reaches only **39.98** dB at 2 kHz. That misses the specification by 0.02 dB, a margin that coefficient quantization would also eat. Rounding the order up is the rule; when the bound is this close to an integer, it is worth asking the specification's owner whether 39.98 dB or a slightly wider transition is acceptable, which would save a biquad.

(d) The bilinear transform maps the whole analog frequency axis onto $-\pi < \omega < \pi$ through $\Omega = 2f_s\tan(\omega/2)$, compressing high frequencies. Designing the analog prototype at the unwarped edges (6283 and 12,566 rad/s) would place them at **952.9** Hz and **1695** Hz after the transform. The passband would end 47 Hz early, so the response at 1 kHz would fail the 1 dB limit; the stopband would over-deliver. Prewarping moves the analog edges so that the transform carries them exactly onto 1 kHz and 2 kHz.

### Solution 8

(a) For $A(z) = 1 - 2\rho\cos\theta z^{-1} + \rho^2z^{-2}$: $\rho = \sqrt{0.81}$ = **0.9** and $\cos\theta = 1.2/(2 \times 0.9) = 0.6667$, so $\theta$ = **0.8411** rad (**48.19°**). The poles are $0.9e^{\pm j0.8411}$.

(b) Step-down: $k_2 = a_2$ = **0.81**; $k_1 = a_1/(1 + a_2) = -1.2/1.81$ = **−0.6630**. Both satisfy $\lvert k_i\rvert < 1$, so the filter is **stable** (consistent with $\rho = 0.9 < 1$).

(c) At $\omega = \theta$, $A(e^{j\theta}) = (1 - \rho)(1 - \rho e^{-j2\theta})$, so $\lvert A\rvert = 0.1 \times \lvert 1 - 0.9e^{-j1.6821}\rvert = 0.1 \times 1.4177$ and $\lvert 1/A\rvert$ = **7.05**. (The exact peak is **7.06**, at 0.836 rad.) The DF II state $w = x/A$ can therefore be about 7 times the input amplitude, **17.0** dB or about 3 bits more.

(d) DF I stores two past inputs and two past outputs: **4** registers. DF II shares one delay line: **2** registers. For 16-bit fixed point, choose **DF I** with a wide accumulator: its only internal sum is the accumulator, and its stored values are the input and output, which are bounded by the signal's own range. DF II's internal node would need 3 bits of headroom (or input scaling by about 1/7, which costs the same 17 dB of SNR). The lab's Verilog biquad (16-08) is DF I for this reason.

### Solution 9

(a) The new Nyquist frequency is 24 kHz and components fold about multiples of 48 kHz: 30 kHz lands at $48 - 30$ = **18** kHz; 50 kHz lands at $50 - 48$ = **2** kHz.

(b) Direct (filter at 192 kHz, then discard three outputs in four): $64 \times 192{,}000$ = **12.29** million multiplications per second. Polyphase (compute only the kept outputs): $64 \times 48{,}000$ = **3.072** million per second, **4** times fewer.

(c) DC gain $R^N = 8^3$ = **512**; register growth $N\log_2R = 3 \times 3$ = **9** bits.

(d) The integrators have a pole at $z = 1$ and their sums grow without bound, but two's-complement arithmetic is arithmetic modulo $2^W$. The combs compute differences, and a difference computed modulo $2^W$ is correct as long as the true result fits in $W$ bits. The final output is bounded by the input's range times the DC gain, so with $W = B_{\text{in}} + N\log_2R$ bits the wrapped intermediate values cancel exactly. Saturating the integrators instead would break this cancellation (16-09 §3.7).

### Solution 10

(a) $6.02 \times 14 + 1.76$ = **86.04** dB (from the exact constants, $10\log_{10}(1.5 \times 4^{14})$ = **86.05** dB).

(b) $h[n] = 0.95^n$, so $\sum h^2 = 1/(1 - 0.95^2) = 1/0.0975$ = **10.26**, or **10.11** dB. Rounding noise injected at the input of this section is amplified about tenfold in power.

(c) A value $k$ (in LSB) is a fixed point when rounding $0.9k$ returns $k$, which requires $\lvert 0.1k\rvert \le 1/2$: $\lvert k\rvert \le 1/(2(1 - 0.9))$ = **5** LSB. Starting from 20 LSB, the output decays to 5 and stays there ($0.9 \times 5 = 4.5$ rounds back to 5).

(d) With wrap-around, an overflow turns a large positive value into a large negative one; the feedback treats the wrapped value as a real state and can sustain a full-scale oscillation with no input (an overflow limit cycle), even though the filter is stable in exact arithmetic. Saturation keeps the error in the same direction as the true value, so it acts like a temporary loss of gain and the response recovers. (CIC integrators are the exception, because the combs undo the wrap exactly; recursive filters have no such cancellation.)

### Solution 11

(a) Product: $18 + 18$ = **36** bits. Accumulator: $36 + \log_2 512$ = **45** bits.

(b) Folded: 128 multiplications per output × 200 MS/s = $2.56 \times 10^{10}$ per second; each block does $6 \times 10^8$: 42.67, so **43** blocks.

(c) The loop contains one multiplier and one adder and one register: $T_\infty = (1.5 + 0.5)/1$ = **2.0** ns (500 MHz). After look-ahead by 2, $y[n] = a^2y[n - 2] + x[n] + ax[n - 1]$: the loop still has one multiplier and one adder but two registers, so $T_\infty = 2.0/2$ = **1.0** ns (1 GHz). The added feed-forward term $x[n] + ax[n - 1]$ is outside the loop and can be pipelined freely.

(d) After $n$ iterations the residual is below $\arctan2^{-(n-1)} < 2^{-(n-1)}$. For $2^{-(n-1)} \le 2^{-10}$: $n$ = **11** iterations.

### Solution 12

(a) Elliptic: the first section has five non-trivial coefficients ($b_0 = b_2$ carry the gain, $b_1$, $a_1$, $a_2$) and the second three ($b_1$, $a_1$, $a_2$): **8** multiplications per output. FIR: 15 taps fold into 7 pairs plus the centre tap: **8** multiplications per output. They tie. (The 15-tap design has **0.731** dB peak-to-peak ripple and **42.7** dB attenuation; 14 taps gives **1.02** dB of ripple, just outside the mask.)

(b) The FIR delays every frequency by $(15 - 1)/2$ = **7** samples (0.875 ms). The elliptic filter is faster at low frequencies (2.69 samples at DC) but its delay doubles to 14.96 samples near the band edge, so a waveform with energy across the passband is smeared by **12.28** samples of delay spread. The FIR has none.

(c) The FIR's order scales as $1/\Delta\omega$ and with $\log(1/\delta_p\delta_s)$; the elliptic order grows only logarithmically with sharpness. Here the transition is $\pi/4$ rad/sample, 6 times wider than the audio example's 0.1309, and the tolerances are looser (1 dB and 40 dB against 0.1 dB and 60 dB). The equiripple estimate falls from **129.5** for the audio specification to **10.63** here, while the elliptic order only halves (8 to 4). Wide transitions relative to $f_s$ remove the IIR filter's advantage.

(d) *FIR:* linear phase (no delay spread, so pulse shapes survive), unconditional stability, no limit cycles and benign fixed-point behaviour, and it can be polyphase-decimated if the stream is later downsampled. *IIR:* lower delay at low frequencies (2.69 samples at DC, against 7), a steeper skirt than required (42.3 dB already at 2 kHz), and fewer state registers (4 against 14).

### Solution 13

(a) **Noise model.** For a busy signal that crosses many levels, the rounding error $e = Q(x) - x$ is modelled as uniform on $[-\Delta/2, \Delta/2]$, white, and uncorrelated with the signal. Its power is

$$
\sigma_e^2 = \frac1\Delta\int_{-\Delta/2}^{\Delta/2}e^2\,de = \frac{\Delta^2}{12} .
$$

A full-scale sine has amplitude 1 and power $1/2$. With $\Delta = 2^{1-N}$:

$$
\text{SQNR} = \frac{1/2}{\Delta^2/12} = \frac{6}{\Delta^2} = 6 \times 2^{2N - 2} = 1.5 \times 4^N ,
\qquad
10\log_{10}\text{SQNR} = 10\log_{10}1.5 + N \cdot 20\log_{10}2 = 1.76 + 6.02N\ \text{dB} .
$$

Units: both powers are in (full scale)², so the ratio is dimensionless. The model fails for small or periodic signals locked to the sample rate, where the error becomes deterministic harmonics (16-10 §3.2).

(b) A type II filter has odd order $M$ (even length $M + 1$) and $h[n] = h[M - n]$. Then

$$
H(z) = \sum_{n=0}^{M}h[n]z^{-n} = \sum_{n=0}^{M}h[M - n]z^{-n} = \sum_{m=0}^{M}h[m]z^{-(M - m)} = z^{-M}H(z^{-1}) .
$$

At $z = -1$: $H(-1) = (-1)^{-M}H(-1) = -H(-1)$ because $M$ is odd, so $H(-1) = 0$. Since $\lvert H(e^{j\pi})\rvert = \lvert A(\pi)\rvert$, $A(\pi) = 0$. Equivalently, pairing terms, $A(\omega) = \sum_{n=0}^{(M-1)/2}2h[n]\cos\bigl(\omega(M/2 - n)\bigr)$ and every $M/2 - n$ is a half-integer, so each cosine vanishes at $\omega = \pi$. A type II filter can therefore never be a high-pass or band-stop filter.

(c) Let $g$ be the impulse response of $H(z^M)$: $g[k] = h[k/M]$ when $M$ divides $k$, and 0 otherwise. Its output is

$$
u[n] = \sum_k g[k]x[n - k] = \sum_m h[m]\,x[n - mM] .
$$

Downsampling keeps $y[n] = u[nM] = \sum_m h[m]\,x[nM - mM] = \sum_m h[m]\,x_d[n - m]$, where $x_d[n] = x[nM]$ is the downsampled input. The last sum is $H(z)$ applied to $x_d$, which is the other side of the identity. ∎ The identity is what lets a polyphase decimator move each branch filter after its downsampler, so that it runs at the low rate (16-09).

### Solution 14

(a) A 128-tap filter at 48 kHz performs $128 \times 48{,}000$ = **6.144** million MACs per second. At 4 µW that is $4 \times 10^{-6}/6.144 \times 10^6$ = **0.651** pJ per MAC, **4.9** times below the 45 nm figure for a 32-bit integer MAC (3.2 pJ). Folding halves the multiplications (**1.30** pJ per multiplication), but the claim must also cover a coefficient and a sample read per tap: a single 8 KB cache read at 45 nm costs 10 pJ, **15.4** times the whole budget per MAC. The claim is plausible only in a much newer process, with operands in registers or a hard-wired coefficient set, and with "4 µW" excluding memory, clocking and leakage. It needs an explanation, not acceptance.

(b) $N = (120 - 1.76)/6.02$ = **19.64**, so at least **20** bits in the signal path. The accumulator needs about 20 + (coefficient bits) + 7 bits, and the 6 dB/bit rule makes each extra bit cost energy (multiplier energy grows roughly with the square of the width).

(c) A 128-tap linear-phase FIR has order 127 and delay $127/2$ = **63.5** samples, or **1.323** ms at 48 kHz: **13.2** times the claimed 0.1 ms. No 128-tap linear-phase filter at 48 kHz can have 0.1 ms latency (**4.8** samples). The claims are consistent only if the filter is not linear phase (a minimum-phase design), if "latency" excludes the filter's group delay, or if the rate is not 48 kHz.

(d) Rubric (3 points; any four well-chosen questions with the matching consistency condition earn full credit):

| Question to the founders | What would make the claims consistent |
|---|---|
| What process node, supply voltage and word lengths? Is 4 µW measured silicon or a simulation? | A recent node at low voltage, a measured number with the test conditions |
| Does 4 µW include memory reads, clocking, leakage and I/O? | The coefficients are hard-wired or in registers; the figure is total block power, or the exclusions are listed |
| Is "120 dB" SQNR of the arithmetic or end-to-end SNR with a converter? Measured how (bandwidth, weighting)? | 120 dB is the datapath's own noise floor (≥ 20-bit data and a wide accumulator), not a converter's SNR |
| Is the filter linear phase, and what is its group delay? What does "0.1 ms latency" measure? | A minimum-phase or asymmetric filter with a few samples of delay, or latency defined as processing time excluding group delay |
| Are the 128 taps programmable, and at what cost? | Fixed coefficients (multiplierless, CSD) explain the low energy; programmable ones would need memory and multipliers |
| Who has validated these figures, on what part? | A customer evaluation or an independent measurement report |

A strong answer computes the three inconsistencies first (energy per MAC, bits for 120 dB, latency of linear phase) and then asks the questions that would resolve each.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| X16.1a | alias of 9 kHz | 1 | kHz |
| X16.1b | digital frequency of 1 kHz | 0.7854 | rad/sample |
| X16.1c | 4-point average gain at DC | 1 | — |
| X16.1d | 4-point average gain at 1 kHz | 0.653 | — |
| X16.1e | 4-point average gain at 2 kHz | 0 | — |
| X16.1f | 1/e decay time | 1.443 | samples |
| X16.2a | 2 cos θ | 1.8596 | — |
| X16.2b | 2 r cos θ | 1.8410 | — |
| X16.2c | r² | 0.9801 | — |
| X16.2d | notch width by the rule | 3.18 | Hz |
| X16.2e | exact notch width | 3.20 | Hz |
| X16.2f | time constant | 99.5 | samples |
| X16.2g | time constant | 0.0995 | s |
| X16.2h | DC gain | 1.0094 | — |
| X16.2i | normalizing factor | 0.9907 | — |
| X16.3a | X[0] | 2 | — |
| X16.3b | X[4] | 0 | — |
| X16.3c | abs X[1] | 1.848 | — |
| X16.3d | bin spacing | 46.875 | Hz |
| X16.3e | valid outputs per block | 896 | — |
| X16.3f | fast-convolution cost | 50.3 | per output |
| X16.3g | advantage over direct | 2.57 | — |
| X16.4a | stages | 12 | — |
| X16.4b | butterflies | 24576 | — |
| X16.4c | non-trivial multiplications | 18434 | — |
| X16.4d | reduction factor | 682.7 | — |
| X16.5a | coherent bin | 819 | — |
| X16.5b | input frequency | 9.997559 | MHz |
| X16.5c | ENOB as measured | 11.34 | bits |
| X16.5d | ENOB referred to full scale | 11.50 | bits |
| X16.5e | processing gain | 36.12 | dB |
| X16.5f | floor gain with Hann | 34.36 | dB |
| X16.5g | floor below tone | 106.4 | dB |
| X16.6a | delta_p | 0.005756 | — |
| X16.6b | delta_s | 0.003162 | — |
| X16.6c | Kaiser beta | 4.534 | — |
| X16.6d | Kaiser order estimate | 140.4 | — |
| X16.6e | equiripple order estimate | 113.1 | — |
| X16.6f | delay | 70.5 | samples |
| X16.6g | delay | 1.469 | ms |
| X16.6h | folded multipliers | 71 | — |
| X16.7a | prewarped passband edge | 0.4142 | — |
| X16.7b | edge ratio | 2.414 | — |
| X16.7c | prewarped passband edge with 2fs | 6627 | rad/s |
| X16.7d | discrimination | 38617 | — |
| X16.7e | Butterworth order bound | 5.99 | — |
| X16.7f | Chebyshev order bound | 3.91 | — |
| X16.7g | order-3 elliptic attenuation | 39.98 | dB |
| X16.7h | unwarped passband edge | 952.9 | Hz |
| X16.7i | unwarped stopband edge | 1695 | Hz |
| X16.8a | pole radius | 0.9 | — |
| X16.8b | pole angle | 0.8411 | rad |
| X16.8c | pole angle | 48.19 | ° |
| X16.8d | k2 | 0.81 | — |
| X16.8e | k1 | −0.6630 | — |
| X16.8f | state gain at the pole angle | 7.05 | — |
| X16.8g | exact peak state gain | 7.06 | — |
| X16.8h | state gain at the pole angle | 17.0 | dB |
| X16.9a | alias of 30 kHz | 18 | kHz |
| X16.9b | alias of 50 kHz | 2 | kHz |
| X16.9c | direct multiplication rate | 12.29 | M/s |
| X16.9d | polyphase multiplication rate | 3.072 | M/s |
| X16.9e | CIC DC gain | 512 | — |
| X16.9f | CIC register growth | 9 | bits |
| X16.10a | 14-bit SQNR, rounded constants | 86.04 | dB |
| X16.10b | 14-bit SQNR, exact | 86.05 | dB |
| X16.10c | noise gain | 10.26 | — |
| X16.10d | noise gain | 10.11 | dB |
| X16.10e | dead band | 5 | LSB |
| X16.11a | product width | 36 | bits |
| X16.11b | accumulator width | 45 | bits |
| X16.11c | DSP blocks | 43 | — |
| X16.11d | iteration bound | 2.0 | ns |
| X16.11e | iteration bound after look-ahead | 1.0 | ns |
| X16.11f | CORDIC iterations | 11 | — |
| X16.12a | elliptic multiplications | 8 | — |
| X16.12b | FIR multiplications | 8 | — |
| X16.12c | FIR delay | 7 | samples |
| X16.12d | equiripple estimate, audio specification | 129.5 | — |
| X16.12e | equiripple estimate, this specification | 10.63 | — |
| X16.12f | elliptic attenuation at 2 kHz | 42.3 | dB |
| X16.12g | 15-tap FIR ripple | 0.731 | dB |
| X16.12h | 15-tap FIR attenuation | 42.7 | dB |
| X16.12i | 14-tap FIR ripple | 1.02 | dB |
| X16.12j | elliptic delay spread | 12.28 | samples |
| X16.14a | MAC rate | 6.144 | M/s |
| X16.14b | energy per MAC | 0.651 | pJ |
| X16.14c | ratio to 3.2 pJ | 4.9 | — |
| X16.14d | bits for 120 dB | 19.64 | bits |
| X16.14e | linear-phase delay | 63.5 | samples |
| X16.14f | linear-phase delay | 1.323 | ms |
| X16.14g | ratio to the claim | 13.2 | — |
| X16.14h | energy per multiplication, folded | 1.30 | pJ |
| X16.14i | cache read over MAC budget | 15.4 | — |
| X16.14j | 0.1 ms in samples | 4.8 | samples |
