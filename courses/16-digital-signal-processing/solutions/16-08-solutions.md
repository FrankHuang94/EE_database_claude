# Solutions 16-08 · Filter Structures and Implementation

Problems: [16-08 problems](../problems/16-08-problems.md) · Chapter: [16-08](../chapters/16-08-filter-structures.md). Every number below is recomputed by [verify_16_08.py](../verify/verify_16_08.py): structures against `scipy.signal.lfilter`, peaks and norms by `freqz` and impulse responses, roots with `numpy.roots`, and the fixed-point model against the committed test vectors that the Verilog testbench uses.

---

## Solutions

### Solution 16-08.1

With $N = 6$: DF I: **13** multipliers, **12** adders, **12** delays. DF II: 13 multipliers, 12 adders, **6** delays. Three biquads: **15** multipliers (5 each), 12 adders, 6 delays.

### Solution 16-08.2

The transposed structure broadcasts $x[n]$ to all three multipliers and puts the delays in the adder chain:

```text
 x[n] ──┬──────────────┬──────────────┐
        │×h0           │×h1           │×h2
        ↓              ↓              ↓
 y[n] ←(+)←─[z⁻¹]─ s0 ←(+)←─[z⁻¹]─ s1 ←┘
```

It computes $y[n] = h_0x[n] + s_0$, then updates $s_0 \leftarrow h_1x[n] + s_1$ and $s_1 \leftarrow h_2x[n]$:

| $n$ | $x$ | $y = x + s_0$ | new $s_0 = -x + s_1$ | new $s_1 = 0.5x$ |
|---|---|---|---|---|
| 0 | 1 | 1 | −1 | 0.5 |
| 1 | 2 | 2 − 1 = **1** | −2 + 0.5 = −1.5 | 1 |
| 2 | 3 | 3 − 1.5 = **1.5** | −3 + 1 = −2 | 1.5 |
| 3 | 0 | **−2** | 1.5 | 0 |
| 4 | 0 | **1.5** | 0 | 0 |

Direct convolution: $y = (1, 2 - 1, 3 - 2 + 0.5, -3 + 1, 1.5) = (1, 1, 1.5, -2, 1.5)$, the same.

### Solution 16-08.3

$w[n] = x[n] + 0.5w[n - 1]$, $y[n] = w[n] + w[n - 1]$. For an impulse: $w = (1, 0.5, 0.25, 0.125, \dots)$, so $y = (1, 1.5, 0.75, 0.375)$: $h[0]$ = **1**, $h[1]$ = **1.5**, $h[2]$ = **0.75**, $h[3]$ = **0.375**.

### Solution 16-08.4

(a) $1.5 + 31 \times 0.4$ = **13.9** ns, **71.9** MHz. (b) $\log_2 32 = 5$ adder levels: $1.5 + 5 \times 0.4$ = **3.5** ns, **285.7** MHz. (c) $1.5 + 0.4$ = **1.9** ns, **526.3** MHz.

### Solution 16-08.5

The peak of $\lvert 1/A\rvert$ is **11.84** at $\omega$ = **0.333**π, just below the pole angle $\pi/3$ (the conjugate pole tilts it). That is 21.5 dB, $\log_2 11.84$ = **3.57** bits, so DF II needs **4** extra bits at its internal node for full-scale sinusoids.

### Solution 16-08.6

$a_1 = -2\rho\cos\theta$ with $\rho = \sqrt{a_2}$ fixed, so $da_1/d\theta = 2\rho\sin\theta$ and $d\theta/da_1 = 1/(2\rho\sin\theta)$. At $\theta = \pi/2$: $1/1.98$ = **0.5051**. At $\theta = 0.01$: $1/(1.98 \times 0.0099998)$ = **50.51**, a hundred times more sensitive.

### Solution 16-08.7

(a) $k_2 = 0.9$, $k_1 = a_1/(1 + k_2) = 0.5/1.9$ = **0.2632**: both below 1, **stable**.

(b) $k_2 = 1.2$: $\lvert k_2\rvert > 1$, **unstable**. ($k_1 = -1.8/2.2 = -0.818$ is irrelevant once one coefficient fails.) The roots of $z^2 - 1.8z + 1.2$ are complex with magnitude $\sqrt{1.2}$ = **1.0954**, outside the circle.

### Solution 16-08.8

(a) Rounding $16384 \times$ each coefficient: $b = (1600, 3199, 1600)$, $a_1 = -15447$, $a_2 = 5461$. Quantized DC gain $= (1600 + 3199 + 1600)/(16384 - 15447 + 5461) = 6399/6398$ = **1.00016**.

(b) Yes. The digital Butterworth biquad overshoots its step by 5.5% (floating-point peak **33,774**), above 32,767, so the 16-bit output saturates for **2** samples. It settles to $\text{round}(32{,}000 \times 6399/6398)$ = **32,005**.

### Solution 16-08.9

$\theta = 2\pi \times 50/48{,}000$. Rounding to 14 fractional bits: the direct form ($a_1 = -2\rho\cos\theta$, $a_2 = \rho^2$) realizes a pole at **59.58** Hz, 19% high; the coupled form ($\rho\cos\theta$, $\rho\sin\theta$) realizes **49.92** Hz. The direct-form recursion costs **2** multiplications per sample; the coupled form **4**.

### Solution 16-08.10

Peak gain from the input to the output of sections 1 to 4:

| Ordering | Section 1 | Section 2 | Section 3 | Section 4 |
|---|---|---|---|---|
| SciPy's (poles far from the circle first) | **0.080** | **0.386** | **0.730** | 1.000 |
| Reversed | **6.25** | **17.22** | **53.57** | 1.000 |

The reverse ordering's worst node is 53.57 times (34.6 dB) the input, so it needs $\lceil\log_2 53.57\rceil$ = **6** extra bits there, where SciPy's ordering needs none.

### Solution 16-08.11

$A(z) = 1 - 3.3569z^{-1} + 4.6785z^{-2} - 3.1232z^{-3} + 0.86488z^{-4}$. Step-down: $k_4$ = **0.8649**, $k_3$ = **−0.8726**, $k_2$ = **0.9978**, $k_1$ = **−0.8667**. All magnitudes are below 1, so it is **stable**; $k_2 = 0.9978$ is within 0.3% of 1, a warning that the step-down is close to $\lvert k\rvert = 1$, so small coefficient errors in this direct fourth-order form could push it past 1 and a root outside the circle.

### Solution 16-08.12

The impulse response $g$ of $1/A$ decays slowly (poles at 0.985); $\sum g^2$ = **66.05**, **18.2** dB. A rounding error of variance $\sigma_e^2 = \Delta^2/12$ (16-10) therefore appears at the output with variance $66\sigma_e^2$: the section's own rounding contributes noise 18 dB above the noise of a single rounding, $\Delta^2/12$. Sharp sections are noisy sections; more accumulator bits before the final rounding, or error feedback, are the remedies (16-10).

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 16-08.1a | DF I multipliers | 13 | — |
| 16-08.1b | DF I delays | 12 | — |
| 16-08.1c | DF II delays | 6 | — |
| 16-08.1d | cascade multipliers | 15 | — |
| 16-08.1e | adders | 12 | — |
| 16-08.2a | y[1] | 1 | — |
| 16-08.2b | y[2] | 1.5 | — |
| 16-08.2c | y[3] | −2 | — |
| 16-08.2d | y[4] | 1.5 | — |
| 16-08.3a | h[1] | 1.5 | — |
| 16-08.3b | h[2] | 0.75 | — |
| 16-08.3c | h[3] | 0.375 | — |
| 16-08.4a | direct critical path | 13.9 | ns |
| 16-08.4b | direct clock | 71.9 | MHz |
| 16-08.4c | tree critical path | 3.5 | ns |
| 16-08.4d | tree clock | 285.7 | MHz |
| 16-08.4e | transposed critical path | 1.9 | ns |
| 16-08.4f | transposed clock | 526.3 | MHz |
| 16-08.5a | peak of 1/A | 11.84 | — |
| 16-08.5b | peak frequency | 0.333 | π rad/sample |
| 16-08.5c | log2 of the peak | 3.57 | bits |
| 16-08.5d | extra bits | 4 | bits |
| 16-08.6a | sensitivity at π/2 | 0.5051 | — |
| 16-08.6b | sensitivity at 0.01 rad | 50.51 | — |
| 16-08.7a | k1 of (a) | 0.2632 | — |
| 16-08.7b | root magnitude of (b) | 1.0954 | — |
| 16-08.8a | quantized DC gain | 1.00016 | — |
| 16-08.8b | floating-point step peak | 33774 | — |
| 16-08.8c | saturated samples | 2 | — |
| 16-08.8d | final output | 32005 | — |
| 16-08.9a | direct-form pole frequency | 59.58 | Hz |
| 16-08.9b | coupled-form pole frequency | 49.92 | Hz |
| 16-08.10a | SciPy order, section 1 peak | 0.080 | — |
| 16-08.10b | SciPy order, section 2 peak | 0.386 | — |
| 16-08.10c | SciPy order, section 3 peak | 0.730 | — |
| 16-08.10d | reversed, section 1 peak | 6.25 | — |
| 16-08.10e | reversed, section 2 peak | 17.22 | — |
| 16-08.10f | reversed, section 3 peak | 53.57 | — |
| 16-08.10g | extra bits, reversed | 6 | bits |
| 16-08.11a | k4 | 0.8649 | — |
| 16-08.11b | k3 | −0.8726 | — |
| 16-08.11c | k2 | 0.9978 | — |
| 16-08.11d | k1 | −0.8667 | — |
| 16-08.12a | noise power gain | 66.05 | — |
| 16-08.12b | noise power gain | 18.2 | dB |
