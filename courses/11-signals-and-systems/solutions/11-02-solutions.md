# Solutions 11-02 · Systems and Their Properties

Problems: [11-02 problems](../problems/11-02-problems.md) · Chapter: [11-02](../chapters/11-02-system-properties.md). Every number below is recomputed by [verify_11_02.py](../verify/verify_11_02.py), which codes each system as a function and runs the stated tests on it.

---

## Solutions

### Solution 11-02.1

(a) $y(t)$ needs only $x(t)$: **memoryless**, hence causal. (It is not linear, because of the −2, but that is a different question.)

(b) $y(t)$ needs $x(t - 1)$ and $x(1 - t)$: memory. At $t = 0$ it needs $x(1)$, a future value: **noncausal**.

(c) The sum runs up to $k = n + 1$, so $y[0]$ needs $x[1]$: memory, **noncausal**.

(d) $y[n]$ needs $x[n]$ and $x[n - 1]$: memory, causal.

(e) The integral covers $[t - 1, t]$: memory (the past second), causal.

(f) $y(t)$ needs $x(t/2)$. For $t > 0$, $t/2 < t$ is in the past; for $t < 0$, $t/2 > t$ is in the future: $y(-2) = x(-1)$ needs the input one second ahead. Memory, **noncausal**. A system can be causal for some inputs and times and not others; causality requires it for all.

### Solution 11-02.2

(a) $\mathcal{T}\{1 + 2\} = 3^2$ = **9**, but $\mathcal{T}\{1\} + \mathcal{T}\{2\} = 1 + 4$ = **5**. Not additive, so not linear.

(b) $\mathcal{T}\{1 + (-1)\} = \lvert0\rvert$ = **0**, but $\mathcal{T}\{1\} + \mathcal{T}\{-1\} = 1 + 1$ = **2**. Not linear. (Homogeneity also fails for negative scalars: $\mathcal{T}\{-x\} = \lvert x\rvert \ne -\lvert x\rvert$.)

(c) Linear. For any inputs and scalars, $\mathcal{T}\{ax_1 + bx_2\}[n] = (ax_1[n] + bx_2[n]) + (ax_1[n - 1] + bx_2[n - 1]) = a(x_1[n] + x_1[n - 1]) + b(x_2[n] + x_2[n - 1]) = a\,\mathcal{T}\{x_1\}[n] + b\,\mathcal{T}\{x_2\}[n]$.

(d) Linear. $\mathcal{T}\{ax_1 + bx_2\}(t) = (ax_1(t) + bx_2(t))\cos t = a\,x_1(t)\cos t + b\,x_2(t)\cos t$. The multiplier $\cos t$ depends on time, not on the input.

(e) $\operatorname{round}(0.4) + \operatorname{round}(0.4)$ = **0**, but $\operatorname{round}(0.8)$ = **1**. Not linear. Quantization is the nonlinearity in every ADC (11-01); for signals much larger than one step it is modeled as linear plus a small additive error.

### Solution 11-02.3

(a) Time-invariant. Let $x_1[n] = x[n - n_0]$. Then $\mathcal{T}\{x_1\}[n] = x_1[n] - x_1[n - 1] = x[n - n_0] - x[n - n_0 - 1]$, and $y[n - n_0] = x[n - n_0] - x[n - n_0 - 1]$: identical.

(b) $\mathcal{T}\{p(t - 2)\}(t) = p(-t - 2)$, nonzero when $0 < -t - 2 < 1$, that is on $(-3, -2)$: from **−3** to **−2** s. The delayed output $y(t - 2) = p(-(t - 2)) = p(2 - t)$ is nonzero when $0 < 2 - t < 1$, on $(1, 2)$: from **1** to **2** s. Delaying the input moved the output *earlier*: time-varying.

(c) With $x = u(t + 1)$: $y = u(t + 1)u(t) = u(t)$, so the delayed output $y(t - 2) = u(t - 2)$ switches on at **2** s. The delayed input $u(t - 1)$ gives $u(t - 1)u(t) = u(t - 1)$, which switches on at **1** s. Time-varying: the switch closes at a fixed clock time.

(d) $\mathcal{T}\{\delta[n]\} = \delta[n]$, so the delayed output is $\delta[n - 1]$, weight **1**. The delayed input gives $(-1)^n\delta[n - 1] = -\delta[n - 1]$, weight **−1**. Time-varying, periodically with period 2.

### Solution 11-02.4

(a) $\lvert y\rvert = x^2 \le 3^2$ = **9**: stable.

(b) $e^{x} \le e^{3}$ = **20.09**: stable. (A lower bound, $e^{-3}$, is not needed: BIBO asks only that $\lvert y\rvert$ be bounded.)

(c) Five terms, each at most 3 in magnitude: $\lvert y[n]\rvert \le 5 \times 3$ = **15**: stable.

(d) The bounded input $x = u(t)$ gives $y = t\,u(t)$, which grows without limit: **unstable**.

(e) The bounded input $x[n] = 1$ gives $y[n] = n$: **unstable**.

(f) $1/(1 + t^2) \le 1$, so $\lvert y\rvert \le$ **3**: stable, even though the system is time-varying.

### Solution 11-02.5

(a) Solve for $x$: $x[n] = y[n] + 0.5\,x[n - 1]$, so the inverse is the recursion $w[n] = y[n] + 0.5\,w[n - 1]$, S10 with $a = 0.5$. Its impulse response is $0.5^nu[n]$, with $\sum\lvert h\rvert = 1/(1 - 0.5)$ = **2**: stable.

(b) $x = y^{1/3}$, the real cube root, which is single-valued for every real $y$: invertible, and the inverse is stable ($\lvert x\rvert \le B^{1/3}$ when $\lvert y\rvert \le B$).

(c) Not invertible: $x$ and $x + c$ have the same derivative for every constant $c$, so the output cannot tell them apart.

(d) Not invertible: inputs that differ only at odd $n$ give the same output.

(e) The causal inverse is $w[n] = y[n] - w[n - 1]$, with impulse response $(-1)^nu[n]$. Its magnitudes sum to infinity, so it is not BIBO-stable, although its impulse response is bounded. For the input $(-1)^nu[n]$: $w[0] = 1$, $w[1] = -1 - 1 = -2$, $w[2] = 1 + 2 = 3$ (verified sample by sample), and in general $w[n] = (-1)^n(n + 1)$, so $\lvert w[9]\rvert$ = **10** and growing. This is the borderline case $\lvert b\rvert = 1$ of Example 11-02.7.

### Solution 11-02.6

(a) With $e^{u} = 1 + u + u^2/2 + u^3/6 + \cdots$ and $u = v/V_T$:

$$
i_C = I_C + \frac{I_C}{V_T}v + \frac{I_C}{2V_T^2}v^2 + \frac{I_C}{6V_T^3}v^3 + \cdots ,
$$

so $a_1 = I_C/V_T$ (the transconductance $g_m$ of 10-04), $a_2 = I_C/(2V_T^2)$ and $a_3 = I_C/(6V_T^3)$.

(b) From §3.3, $\text{HD2} \approx a_2A/(2a_1) = \dfrac{I_C/(2V_T^2)}{2I_C/V_T}A = \dfrac{A}{4V_T}$, and $\text{HD3} \approx a_3A^2/(4a_1) = \dfrac{I_C/(6V_T^3)}{4I_C/V_T}A^2 = \dfrac{A^2}{24V_T^2}$. Every coefficient is proportional to $I_C$, so $I_C$ cancels from the ratios: a bipolar transistor's distortion depends only on the signal amplitude relative to $V_T$, whatever its bias. (A MOSFET's depends on its overdrive voltage instead, 10-04.)

(c) At $A$ = 1 mV: HD2 = $1/(4 \times 25.852)$ = **0.967**% and HD3 = $(1/25.852)^2/24$ = **0.00623**%. At 5 mV: HD2 = **4.835**% and HD3 = **0.156**%.

(d) $A = 0.04V_T$ = **1.034** mV. This is why 10-04 calls a bipolar small signal "small" only when it is about a millivolt or less.

(e) With $x = 5/25.852$ = **0.1934**, $I_2(x)/I_1(x)$ = **4.828**%: the Taylor approximation, 4.835%, is high by only **0.16**% of itself. The approximation is excellent for $x \ll 1$.

### Solution 11-02.7

(a) Let $\mathcal{T} = \mathcal{T}_2\circ\mathcal{T}_1$. Then $\mathcal{T}\{ax_1 + bx_2\} = \mathcal{T}_2\{a\,\mathcal{T}_1\{x_1\} + b\,\mathcal{T}_1\{x_2\}\}$ by the linearity of $\mathcal{T}_1$, which equals $a\,\mathcal{T}_2\{\mathcal{T}_1\{x_1\}\} + b\,\mathcal{T}_2\{\mathcal{T}_1\{x_2\}\}$ by the linearity of $\mathcal{T}_2$.

(b) Let $D$ denote a delay by $t_0$. Time invariance of each part says $\mathcal{T}_k\{D\{x\}\} = D\{\mathcal{T}_k\{x\}\}$. Then $\mathcal{T}_2\{\mathcal{T}_1\{D\{x\}\}\} = \mathcal{T}_2\{D\{\mathcal{T}_1\{x\}\}\} = D\{\mathcal{T}_2\{\mathcal{T}_1\{x\}\}\}$: the delay passes through each block in turn.

(c) $\mathcal{T}_1\{ax_1 + bx_2\} + \mathcal{T}_2\{ax_1 + bx_2\} = a\,\mathcal{T}_1\{x_1\} + b\,\mathcal{T}_1\{x_2\} + a\,\mathcal{T}_2\{x_1\} + b\,\mathcal{T}_2\{x_2\}$, which regroups as $a(\mathcal{T}_1 + \mathcal{T}_2)\{x_1\} + b(\mathcal{T}_1 + \mathcal{T}_2)\{x_2\}$.

(d) Let $y_1 = \mathcal{T}\{x_1\}$ and $y_2 = \mathcal{T}\{x_2\}$, so $x_k = \mathcal{T}^{-1}\{y_k\}$. By linearity of $\mathcal{T}$, $\mathcal{T}\{ax_1 + bx_2\} = ay_1 + by_2$. Applying $\mathcal{T}^{-1}$ to both sides: $ax_1 + bx_2 = \mathcal{T}^{-1}\{ay_1 + by_2\}$, that is, $\mathcal{T}^{-1}\{ay_1 + by_2\} = a\,\mathcal{T}^{-1}\{y_1\} + b\,\mathcal{T}^{-1}\{y_2\}$. Since every output of $\mathcal{T}$ arises this way, $\mathcal{T}^{-1}$ is linear on them.

### Solution 11-02.8

(a) Square, then gain: $2 \times 3^2$ = **18**. Gain, then square: $(2 \times 3)^2$ = **36**. The squarer is not linear, so it does not commute with a gain.

(b) Decimate, then delay: $y[n] = x[2(n - 1)] = 2n - 2$, which is **4** at $n = 3$. Delay, then decimate: $x[2n - 1] = 2n - 1$, which is **5** at $n = 3$. The decimator is not time-invariant, so it does not commute with a delay.

(c) Gain, then delay: $3x[n - 2]$. Delay, then gain: $3\cdot x[n - 2]$. Identical for every input. In general, any two LTI systems commute (11-03 proves it with convolution), and this is the simplest case.

### Solution 11-02.9

(a) Unrolling, $y[n] = y[-1] + \sum_{k=0}^{n}x[k]$. For $x = u[n]$, $y[3] = 5 + 4$ = **9**. For $x = 2u[n]$, $y[3] = 5 + 8$ = **13**. Twice the first is **18** ≠ 13: doubling the input did not double the output.

(b) The zero-input part is $y[-1]$ = **5** in both cases. The zero-state parts are 4 and 8, exactly proportional to the inputs.

(c) Not linear (the zero input gives 5, not 0). Incrementally linear: $y = 5 + \mathcal{L}\{x\}$ with $\mathcal{L}$ the accumulator at rest, which is linear. The accumulator at rest is also unstable, so neither part bounds the output for a step.

### Solution 11-02.10

(a) $\omega_0 = 1/\sqrt{LC} = 1/\sqrt{10^{-3} \times 10^{-6}}$ = **31.62** krad/s, and $f_0 = \omega_0/2\pi$ = **5.033** kHz.

(b) Dividing by $LC$, the equation is $\ddot v_C + \omega_0^2v_C = \omega_0^2\cos\omega_0t$. With $v_C = \tfrac12\omega_0t\sin\omega_0t$:

$$
\dot v_C = \tfrac12\omega_0\left(\sin\omega_0t + \omega_0t\cos\omega_0t\right), \qquad \ddot v_C = \tfrac12\omega_0\left(2\omega_0\cos\omega_0t - \omega_0^2t\sin\omega_0t\right) .
$$

So $\ddot v_C + \omega_0^2v_C = \omega_0^2\cos\omega_0t - \tfrac12\omega_0^3t\sin\omega_0t + \tfrac12\omega_0^3t\sin\omega_0t = \omega_0^2\cos\omega_0t$, as required, and $v_C(0) = 0$, $\dot v_C(0) = 0$: the circuit starts at rest. The amplitude $\tfrac12\omega_0t$ (in volts, for the 1 V drive) is **15.81** V at 1 ms and **158.1** V at 10 ms, growing without limit from a 1 V input: not BIBO-stable.

(c) $Q = \tfrac11\sqrt{10^{-3}/10^{-6}}$ = **31.62**, so the steady-state amplitude is **31.62** V. The resistor turns unbounded growth into a bounded, if large, response: the resonant growth stops when the energy lost per cycle equals the energy the source adds.

**Units check.** $\omega_0t$ is (rad/s)·s, dimensionless, so $\tfrac12\omega_0t$ multiplies the 1 V drive and gives volts.

### Solution 11-02.11

(a) Linear: $s(t)$ is a known function of time, so $\mathcal{T}\{ax_1 + bx_2\} = (ax_1 + bx_2)s = a\,x_1s + b\,x_2s$.

(b) With $x = u(t)$, $y(t) = u(t)s(t)$ and $y(t - 4\ \mu\text{s}) = u(t - 4\ \mu\text{s})\,s(t - 4\ \mu\text{s})$. At $t$ = 5 µs that is $s(1\ \mu\text{s})$ = **+1**. The delayed input gives $\mathcal{T}\{u(t - 4\ \mu\text{s})\} = u(t - 4\ \mu\text{s})\,s(t)$, which at 5 µs is $s(5\ \mu\text{s})$ = **−1**. Time-varying.

(c) Delays by whole multiples of the period, 8 µs, 16 µs, …: then $s(t - t_0) = s(t)$ and the two paths agree. The chopper is periodically time-varying.

(d) Invertible: since $s^2 = 1$ at every instant, $y\,s = x\,s^2 = x$. The inverse is the same chopper. Chopper amplifiers use exactly this: chop the input, amplify it (together with the amplifier's own offset, which is not chopped), then chop again, which restores the signal and moves the offset to the chopping frequency, where a filter removes it.

(e) $1/8\ \mu\text{s}$ = **125** kHz, the OPA333's correction rate (chapter §9).

### Solution 11-02.12

(a) $1/(1 - 0.99)$ = **100**.

(b) $y[n] = \sum_{k=0}^{n}0.99^k = (1 - 0.99^{n+1})/0.01$. Then $y[n] \ge 99$ requires $0.99^{n+1} \le 0.01$, that is $n + 1 \ge \ln0.01/\ln0.99$ = **458.2**, so $n + 1 \ge 459$ and the first such $n$ is **458** ($y[457]$ = **98.998**, $y[458]$ = **99.008**). At 1 kHz that is **0.458** s. A pole close to the unit circle means a high bound *and* a slow approach to it.

(c) To maximize $\lvert y[N]\rvert = \lvert\sum_k(-0.99)^kx[N - k]\rvert$, make every term positive: $x[N - k] = (-1)^k$, that is $x[n] = (-1)^{N-n}$, an input alternating in sign with the right phase at $n = N$. The result approaches the bound of (a), as in Example 11-02.4(b).

(d) For $a = 1$, the step gives $y[n] = n + 1$. For $a = -1$, the input $(-1)^n$ gives $y[n] = (-1)^n(n + 1)$. Both are bounded inputs with unbounded outputs, so no bound exists.

### Solution 11-02.13

(a) $2\ \text{ms} \times 48\ \text{kHz}$ = **96** samples.

(b) The FIR may add $96 - 40 = 56$ samples, so $(N - 1)/2 \le 56$ and $N \le 113$: the longest odd-length symmetric FIR has **113** taps. (Even-length symmetric filters have a half-sample delay, $(N - 1)/2$ with $N$ even; the budget would allow 113 at most in either case.)

(c) $10\ \text{ms} \times 48\ \text{kHz}$ = **480** samples of look-ahead, five times the whole budget: it cannot be used live. A live envelope follower must be causal, typically a recursion like S10 that reacts to the past only, at the cost of lagging the true envelope.

### Solution 11-02.14

(a) The AGC drives the output to 0.5 V rms. With a 10 mV rms input the settled gain is $0.5/0.01$ = **50**; with 20 mV rms it is $0.5/0.02$ = **25**. Doubling the input left the output unchanged: homogeneity fails, so the AGC, and the path, are not linear.

(b) Yes, if its rule does not depend on clock time: delaying the input delays the gain trajectory and the output. The AGC's gain changes because the *input* changed, not because the clock advanced. It is a nonlinear, time-invariant system with memory (its gain depends on the input's recent history).

(c) The chopper is linear but periodically time-varying (period 8 µs). The decimator is linear but periodically time-varying. Neither is time-invariant, so the path is not LTI even with the AGC disabled. In practice, a good design makes these effects small in the band of interest (the chopper's artifacts sit near 125 kHz, the decimator is preceded by filtering), so an LTI model can be *adequate* in band; that is a quantitative claim to be measured, not a property to be assumed.

(d) Three tests. (1) **Two-amplitude test:** apply the same signal at two levels, say 10 and 20 mV rms, with the AGC frozen and active; a linear path doubles its output. (2) **Shift test:** apply the same burst at different times, or at different phases relative to the chopping and decimation clocks; an LTI path gives identical, shifted outputs. (3) **Spur search:** apply a single tone and look for output at any other frequency, especially near multiples of the chopping and sample-rate clocks and at harmonics; an LTI path produces only the input frequency. Results matching all three, to a stated accuracy in the hearing band, support "LTI in band"; any failure refutes the unqualified claim.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 11-02.2a | T{1 + 2} for the squarer | 9 | — |
| 11-02.2b | T{1} + T{2} for the squarer | 5 | — |
| 11-02.2c | T{1 + (−1)} for the absolute value | 0 | — |
| 11-02.2d | T{1} + T{−1} for the absolute value | 2 | — |
| 11-02.2e | round(0.4) + round(0.4) | 0 | — |
| 11-02.2f | round(0.8) | 1 | — |
| 11-02.3a | start of T{p(t − 2)} | −3 | s |
| 11-02.3b | end of T{p(t − 2)} | −2 | s |
| 11-02.3c | start of y(t − 2) | 1 | s |
| 11-02.3d | end of y(t − 2) | 2 | s |
| 11-02.3e | switch-on of the delayed output | 2 | s |
| 11-02.3f | switch-on for the delayed input | 1 | s |
| 11-02.3g | weight of the delayed output | 1 | — |
| 11-02.3h | weight for the delayed input | −1 | — |
| 11-02.4a | bound, squarer | 9 | — |
| 11-02.4b | bound, exponential | 20.09 | — |
| 11-02.4c | bound, five-sample sum | 15 | — |
| 11-02.4d | bound, x/(1 + t²) | 3 | — |
| 11-02.5a | inverse's absolute sum | 2 | — |
| 11-02.5b | magnitude of w[9] for the alternating input | 10 | — |
| 11-02.6a | HD2 at 1 mV | 0.967 | % |
| 11-02.6b | HD3 at 1 mV | 0.00623 | % |
| 11-02.6c | HD2 at 5 mV | 4.835 | % |
| 11-02.6d | HD3 at 5 mV | 0.156 | % |
| 11-02.6e | amplitude for 1% HD2 | 1.034 | mV |
| 11-02.6f | exact HD2 at 5 mV | 4.828 | % |
| 11-02.6g | x = A/V_T at 5 mV | 0.1934 | — |
| 11-02.6h | approximation's relative excess | 0.16 | % |
| 11-02.8a | square, then gain | 18 | — |
| 11-02.8b | gain, then square | 36 | — |
| 11-02.8c | decimate, then delay, at n = 3 | 4 | — |
| 11-02.8d | delay, then decimate, at n = 3 | 5 | — |
| 11-02.9a | y[3] for u[n] | 9 | — |
| 11-02.9b | y[3] for 2u[n] | 13 | — |
| 11-02.9c | twice the first output | 18 | — |
| 11-02.9d | zero-input part | 5 | — |
| 11-02.10a | ω_0 | 31.62 | krad/s |
| 11-02.10b | f_0 | 5.033 | kHz |
| 11-02.10c | amplitude at 1 ms | 15.81 | V |
| 11-02.10d | amplitude at 10 ms | 158.1 | V |
| 11-02.10e | Q with 1 Ω | 31.62 | — |
| 11-02.10f | steady-state amplitude with 1 Ω | 31.62 | V |
| 11-02.11a | y(t − 4 µs) at 5 µs | 1 | — |
| 11-02.11b | T{u(t − 4 µs)} at 5 µs | −1 | — |
| 11-02.11c | chopping frequency | 125 | kHz |
| 11-02.12a | bound | 100 | — |
| 11-02.12b | first n with y ≥ 99 | 458 | — |
| 11-02.12c | time at 1 kHz | 0.458 | s |
| 11-02.12d | ln 0.01 / ln 0.99 | 458.2 | — |
| 11-02.12e | y[457] | 98.998 | — |
| 11-02.12f | y[458] | 99.008 | — |
| 11-02.13a | budget | 96 | samples |
| 11-02.13b | longest odd symmetric FIR | 113 | taps |
| 11-02.13c | look-ahead of 10 ms | 480 | samples |
| 11-02.14a | AGC gain at 10 mV rms | 50 | — |
| 11-02.14b | AGC gain at 20 mV rms | 25 | — |
