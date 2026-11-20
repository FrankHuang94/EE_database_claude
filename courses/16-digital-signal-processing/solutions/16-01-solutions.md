# Solutions 16-01 · Discrete-Time Signals and Systems Review

Problems: [16-01 problems](../problems/16-01-problems.md) · Chapter: [16-01](../chapters/16-01-discrete-time-systems-review.md). Every number below is recomputed by [verify_16_01.py](../verify/verify_16_01.py): sample arrays compared directly for aliasing, brute-force period searches, numpy and scipy against the lab's sample-by-sample loops, and simulations against the closed forms.

---

## Solutions

### Solution 16-01.1

(a) $\omega = 2\pi f/f_s$. For 441 Hz, $f/f_s = 441/44{,}100 = 1/100$, so $\omega = 2\pi/100$ = **0.06283** rad/sample. For 11.025 kHz, $f/f_s = 1/4$, so $\omega = \pi/2$ = **1.571** rad/sample.

(b) In lowest terms, $\omega/2\pi = 1/100$ and $1/4$, so the periods are **100** and **4** samples.

(c) **0.25** cycles/sample: the tone advances a quarter turn per sample, so its samples (for a cosine of zero phase) are $1, 0, -1, 0, \dots$.

**Units check.** Hz/(samples/s) = cycles/sample.

### Solution 16-01.2

Reduce each frequency modulo $f_s$ = 1 kHz and fold into $[0, 500]$ Hz:

| Input | $f \bmod f_s$ | Apparent |
|---|---|---|
| 300 Hz | 300 Hz | **300** Hz |
| 700 Hz | 700 Hz → mirror: $1000 - 700$ | **300** Hz |
| 1.3 kHz | 300 Hz | **300** Hz |
| 1.7 kHz | 700 Hz → mirror | **300** Hz |
| 2.2 kHz | 200 Hz | **200** Hz |

For zero-phase cosines, the first four give identical samples: $\cos(2\pi \cdot 0.7n) = \cos(2\pi n - 2\pi \cdot 0.3n) = \cos(2\pi \cdot 0.3n)$, and adding whole cycles per sample changes nothing. (For sines, the mirrored tones at 700 Hz and 1.7 kHz come out with the sign flipped, because $\sin(-\theta) = -\sin\theta$: same frequency, opposite phase.)

### Solution 16-01.3

Periodic exactly when $\omega/2\pi$ is rational; the period is the denominator in lowest terms.

- (a) $\omega/2\pi = 1/12$: periodic, $N$ = **12**.
- (b) $\omega/2\pi = 1/(12\pi)$, irrational: not periodic.
- (c) $0.7\pi/2\pi = 0.35 = 7/20$: periodic, $N$ = **20** (7 analog cycles per period).
- (d) $\cos(0.8\pi n)$ has $\omega/2\pi = 0.4 = 2/5$, period 5; $\cos(0.5\pi n)$ has $\omega/2\pi = 1/4$, period **4**. The sum repeats at the least common multiple of 5 and 4: $N$ = **20**.
- (e) $5\pi/3 \div 2\pi = 5/6$: periodic, $N$ = **6**. (The same sequence as $e^{-j\pi n/3}$.)

### Solution 16-01.4

| System | Linear | Time-invariant | Causal | BIBO stable | Memoryless |
|---|---|---|---|---|---|
| (a) $3x[n] + 2$ | no: zero input gives 2, not 0 | yes | yes | yes | yes |
| (b) $n\,x[n]$ | yes | no: the gain depends on $n$ | yes | no: $x = u[n]$ gives $y = n$ | yes |
| (c) $x[n+1] - x[n]$ | yes | yes | no: uses $x[n+1]$ | yes ($\lvert y\rvert \le 2B_x$) | no |
| (d) $x[2n]$ | yes | no: delaying $x$ by 1 does not delay $y$ by 1 | no: $y[1] = x[2]$ | yes | no |
| (e) 3-point median | no: median$(a + b) \ne$ median$(a)$ + median$(b)$ in general | yes | yes | yes ($\lvert y\rvert \le B_x$) | no |

A counterexample for (e): inputs $(1, 0, 0)$ and $(0, 1, 0)$ in the window each have median 0, but their sum $(1, 1, 0)$ has median 1.

### Solution 16-01.5

$y[n] = \sum_k h[k]x[n-k]$, length $3 + 3 - 1 = 5$:

- $y[0] = 2 \cdot 1$ = **2**
- $y[1] = 2 \cdot 2 + (-1) \cdot 1$ = **3**
- $y[2] = 2 \cdot 3 + (-1) \cdot 2 + 1 \cdot 1$ = **5**
- $y[3] = (-1) \cdot 3 + 1 \cdot 2$ = **−1**
- $y[4] = 1 \cdot 3$ = **3**

MACs: 1 + 2 + 3 + 2 + 1 = **9**, which is $3 \times 3$: every input meets every coefficient once. Check: $\sum y = 2 + 3 + 5 - 1 + 3 = 12$ and $(\sum x)(\sum h) = 6 \times 2$ = **12**.

### Solution 16-01.6

(a) With $x = \delta$: $h[0] = 1$; $h[1] = 0.5 \cdot 1 + 1 = 1.5$; $h[2] = 0.5 \cdot 1.5 = 0.75$; $h[3]$ = **0.375**. For $n \ge 1$ only the feedback acts, so

$$
h[n] = \delta[n] + 1.5\,(0.5)^{n-1}u[n-1] .
$$

(b) $s[n] = \sum_{k=0}^{n}h[k] = 1 + 1.5\sum_{k=1}^{n}0.5^{k-1} = 1 + 1.5\,\frac{1 - 0.5^n}{1 - 0.5} = 4 - 3\,(0.5)^n$ for $n \ge 0$. So $s[0]$ = **1**, $s[3] = 4 - 0.375$ = **3.625**, $s[\infty]$ = **4**.

(c) $\sum h = 1 + 1.5/(1 - 0.5) = 4$, equal to $s[\infty]$, as it must be: the final value of the step response is the DC gain. The difference equation gives the same thing directly: at DC, $y = 0.5y + 2x$, so $y/x = 2/0.5 = 4$.

### Solution 16-01.7

- (a) Stable: $\sum 0.9^n = 1/(1 - 0.9)$ = **10**.
- (b) Unstable: $\lvert h[n]\rvert = 1.1^n$ grows.
- (c) Unstable: $\sum 1/(n + 1)$ is the harmonic series, which diverges (slowly, like $\ln n$), even though $h[n] \to 0$.
- (d) Stable: $\sum 1/(n + 1)^2 = \pi^2/6$ = **1.645**.
- (e) The characteristic equation $z^2 - 1.6z + 0.64 = (z - 0.8)^2$ has a double pole at 0.8, inside the unit circle: stable. Its impulse response is $h[n] = (n + 1)\,0.8^n u[n]$ (check: $h[0] = 1$, $h[1] = 1.6$, $h[2] = 1.6 \cdot 1.6 - 0.64 = 1.92 = 3 \times 0.64$). Then $\sum_n (n + 1)r^n = 1/(1 - r)^2$, so $\sum\lvert h\rvert = 1/0.2^2$ = **25**.
- (f) Poles at $z = \pm1$, on the unit circle: unstable. $h = 1, 0, 1, 0, \dots$ never decays, and the bounded input $u[n]$ gives an output that grows by one every two samples.

### Solution 16-01.8

Time constant $\tau_s = -1/\ln(1 - \alpha)$ samples, and at 1 kHz one sample is 1 ms, so we need $\tau_s \ge 50$. For $\alpha$ = 1/32, $\tau_s = 31.50$, too short; for $\alpha$ = **1/64**, $\tau_s = -1/\ln(63/64)$ = **63.50** samples = **63.5** ms. This is the largest power of 2 that works.

Equivalent moving-average length: $N_{eq} = (2 - \alpha)/\alpha = 2 \times 64 - 1$ = **127** samples.

1% settling: the error is $(63/64)^{n+1}$, below 0.01 when $n + 1 \ge \ln 0.01/\ln(63/64) = 292.42$, so $n + 1 = 293$ and the first sample within 1% is $n$ = **292** (about 0.29 s).

### Solution 16-01.9

(a) Nulls at $mf_s/N$; for the first at 60 Hz, $N = 960/60$ = **16**. All harmonics (120, 180, ... Hz) are nulls too.

(b) With $\omega = 2\pi \times 10/960$: $\lvert H\rvert = \sin(16\omega/2)/(16\sin(\omega/2))$ = **0.955**, or **−0.399** dB. At 50 Hz the gain is **0.192**: the filter is matched to 60 Hz mains only.

(c) $(N - 1)/2$ = **7.5** samples = 7.5/960 s = **7.81** ms.

### Solution 16-01.10

(a) Direct form I stores $x[n-1]$, $y[n-1]$ and $y[n-2]$: **3** delays. Direct form II shares one delay line of length $\max(M, N) = 2$: **2** delays. Both need **3** non-trivial multipliers (0.9, −0.5 and 0.5; $b_0$ = 1 is free) and **3** two-input adders to combine four terms.

(b) The characteristic equation is $z^2 - 0.9z + 0.5 = 0$, so $z = 0.45 \pm j\sqrt{0.5 - 0.2025} = 0.45 \pm j0.5454$. In polar form, $r = \sqrt{0.5}$ = **0.7071** (the product of a conjugate pair is $r^2 = 0.5$) and $\theta = \arccos(0.45/0.7071)$ = **50.5**°. Both poles are inside the unit circle: stable, with a damped oscillation of about $360/50.5 \approx 7$ samples per cycle.

(c) $h[0] = 1$; $h[1] = 0.9 \cdot 1 + 0.5$ = **1.4**; $h[2] = 0.9 \cdot 1.4 - 0.5 \cdot 1$ = **0.76**; $h[3] = 0.9 \cdot 0.76 - 0.5 \cdot 1.4$ = **−0.016**.

### Solution 16-01.11

$H(e^{j\omega}) = 0.25 + 0.5e^{-j\omega} + 0.25e^{-j2\omega} = e^{-j\omega}\bigl(0.25e^{j\omega} + 0.5 + 0.25e^{-j\omega}\bigr) = e^{-j\omega}\,(0.5 + 0.5\cos\omega)$. So $A(\omega) = 0.5 + 0.5\cos\omega \ge 0$, and the phase is $-\omega$: a one-sample delay at every frequency (linear phase).

- (a) DC: $A(0) = 1$, so $y$ = **2**.
- (b) $\omega = \pi/2$: $A$ = **0.5**, phase −90°: $y[n] = 0.5\cos(\pi n/2 - \pi/2)$.
- (c) $\omega = \pi/3$: $A$ = **0.75**, phase −60°: $y[n] = 0.75\cos(\pi n/3 - \pi/3)$.
- (d) $\omega = \pi$: $A$ = **0**: the alternating sequence is removed completely (check: $0.25 - 0.5 + 0.25 = 0$).

The outputs hold from $n = 2$ on, once the filter's memory is full of the sinusoid.

### Solution 16-01.12

(a) A product of a 12-bit and a 16-bit signed number needs $12 + 16 = 28$ bits; adding 64 of them can grow the sum by a factor of 64, which needs $\log_2 64 = 6$ more bits: **34** bits. A 48-bit accumulator leaves **14** guard bits.

(b) The true moving sum of 64 twelve-bit samples fits in $12 + 6$ = **18** bits, and with wraparound arithmetic the accumulator only needs to hold the final result, so 18 bits suffice even though intermediate values wrap.

(c) $s[0] = 3$; $s[1] = 3 + 4 = 7$ (no subtraction yet). At $n = 2$, $s[1] + x[2] = 9$, which wraps to $9 - 16$ = **−7**; then $-7 - x[0] = -7 - 3 = -10$, which wraps to $-10 + 16$ = **6**. The true sum $x[1] + x[2] = 4 + 2 = 6$: correct.

### Solution 16-01.13

(a) MACs per sample per microphone: $128 + 4 \times 5 = 148$. Rate: $2 \times 16{,}000 \times 148$ = **4.736** million MACs/s. Cycles: $4.736 \times 10^6 \times 1.5 = 7.104 \times 10^6$ per second, out of 48 million: a load of **14.8**%.

(b) FIR delay: $(128 - 1)/2 = 63.5$ samples = **3.969** ms. Double-buffered 32-sample blocks: $2 \times 32$ samples = **4.0** ms. Total **7.97** ms: below 10 ms, with about 2 ms left for the converters' own filters.

(c) With 64-sample blocks the buffering adds **8.0** ms, for a total of **11.97** ms: over budget. Larger blocks improve processor efficiency but cost latency directly.

### Solution 16-01.14

(a) With $x = \delta$: $h[0] = 1$; $h[1] = 2 \cdot 1 - 2 = 0$; $h[2] = 2 \cdot 0 - 1 + 1 = 0$; and from then on every term is zero. So $h[n] = \delta[n]$: the filter is the identity, $y[n] = x[n]$, and BIBO stable.

(b) The recursion is linear, so the error $e[n]$ obeys the homogeneous equation $e[n] = 2e[n-1] - e[n-2]$ with $e[n_0] = \varepsilon$ and $e[n_0 - 1] = 0$. Then $e[n_0 + 1] = 2\varepsilon$, $e[n_0 + 2] = 4\varepsilon - \varepsilon = 3\varepsilon$, and by induction (if $e[k] = (k - n_0 + 1)\varepsilon$ for the two previous $k$, then $2(m + 1)\varepsilon - m\varepsilon = (m + 2)\varepsilon$):

$$
e[n] = (n - n_0 + 1)\,\varepsilon .
$$

1000 samples later, $n - n_0 = 1000$ and the error is **1001** ε: it grows without bound.

(c) The numerator $(1 - z^{-1})^2$ cancels a double pole at $z = 1$. The input–output map is the identity, but the realization contains a double integrator, which is internally unstable: any disturbance of its state grows linearly. Implement the cancelled form, $y[n] = x[n]$, or more generally cancel poles and zeros on paper before building the structure.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 16-01.1a | ω of 441 Hz at 44.1 kHz | 0.06283 | rad/sample |
| 16-01.1b | ω of 11.025 kHz at 44.1 kHz | 1.571 | rad/sample |
| 16-01.1c | period of the 441 Hz sequence | 100 | samples |
| 16-01.1d | period of the 11.025 kHz sequence | 4 | samples |
| 16-01.1e | 11.025 kHz in cycles per sample | 0.25 | cycles/sample |
| 16-01.2a | apparent frequency of 700 Hz | 300 | Hz |
| 16-01.2b | apparent frequency of 1.3 kHz | 300 | Hz |
| 16-01.2c | apparent frequency of 1.7 kHz | 300 | Hz |
| 16-01.2d | apparent frequency of 2.2 kHz | 200 | Hz |
| 16-01.3a | period of cos(πn/6) | 12 | samples |
| 16-01.3b | period of sin(0.7πn) | 20 | samples |
| 16-01.3c | period of cos(0.8πn) + cos(0.5πn) | 20 | samples |
| 16-01.3d | period of exp(j5πn/3) | 6 | samples |
| 16-01.3e | period of cos(0.5πn) | 4 | samples |
| 16-01.5a | y[0] | 2 | — |
| 16-01.5b | y[1] | 3 | — |
| 16-01.5c | y[2] | 5 | — |
| 16-01.5d | y[3] | −1 | — |
| 16-01.5e | y[4] | 3 | — |
| 16-01.5f | MACs | 9 | — |
| 16-01.5g | sum check | 12 | — |
| 16-01.6a | h[3] | 0.375 | — |
| 16-01.6b | s[0] | 1 | — |
| 16-01.6c | s[3] | 3.625 | — |
| 16-01.6d | s[∞] | 4 | — |
| 16-01.7a | absolute sum of h for 0.9^n | 10 | — |
| 16-01.7b | absolute sum of h for 1/(n+1)² | 1.645 | — |
| 16-01.7c | absolute sum of h for the double pole at 0.8 | 25 | — |
| 16-01.8a | 1/α for the chosen EMA factor | 64 | — |
| 16-01.8b | time constant | 63.50 | samples |
| 16-01.8c | time constant | 63.5 | ms |
| 16-01.8d | equivalent moving-average length | 127 | samples |
| 16-01.8e | first sample within 1% | 292 | — |
| 16-01.9a | moving-average length | 16 | — |
| 16-01.9b | gain at 10 Hz | 0.955 | — |
| 16-01.9c | gain at 10 Hz | −0.399 | dB |
| 16-01.9d | gain at 50 Hz | 0.192 | — |
| 16-01.9e | delay | 7.5 | samples |
| 16-01.9f | delay | 7.81 | ms |
| 16-01.10a | DF-I delays | 3 | — |
| 16-01.10b | DF-II delays | 2 | — |
| 16-01.10c | non-trivial multipliers | 3 | — |
| 16-01.10d | two-input adders | 3 | — |
| 16-01.10e | pole radius | 0.7071 | — |
| 16-01.10f | pole angle | 50.5 | ° |
| 16-01.10g | h[1] | 1.4 | — |
| 16-01.10h | h[2] | 0.76 | — |
| 16-01.10i | h[3] | −0.016 | — |
| 16-01.11a | output for the constant 2 | 2 | — |
| 16-01.11b | gain at π/2 | 0.5 | — |
| 16-01.11c | gain at π/3 | 0.75 | — |
| 16-01.11d | gain at π | 0 | — |
| 16-01.12a | exact accumulator width | 34 | bits |
| 16-01.12b | guard bits in 48 | 14 | bits |
| 16-01.12c | wraparound running-sum width | 18 | bits |
| 16-01.12d | wrapped intermediate | −7 | — |
| 16-01.12e | s[2] | 6 | — |
| 16-01.13a | MAC rate | 4.736 | M/s |
| 16-01.13b | processor load | 14.8 | % |
| 16-01.13c | FIR latency | 3.969 | ms |
| 16-01.13d | block latency, 32-sample blocks | 4.0 | ms |
| 16-01.13e | total latency, 32-sample blocks | 7.97 | ms |
| 16-01.13f | block latency, 64-sample blocks | 8.0 | ms |
| 16-01.13g | total latency, 64-sample blocks | 11.97 | ms |
| 16-01.14a | error 1000 samples later, in units of ε | 1001 | — |
