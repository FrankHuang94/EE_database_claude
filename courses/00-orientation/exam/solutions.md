# Course 00 · Final Exam — Solutions

Exam: [README.md](README.md). All numbers are recomputed by [verify_00_exam.py](../verify/verify_00_exam.py).

**1.** Energy $= 5.000\text{ Ah} \times 3.87\text{ V} = 19.35$ Wh. Average power $= 19.35/30 = 0.645$ W.

**2.** One lane: $4\times10^{-12} \times 224\times10^9 = 0.896$ W. 32 lanes: $28.7$ W.

**3.** (a) $\lambda = 1.5\times10^8/10^9 = 0.15$ m, so the trace is $0.30/0.15 = 2.0$ wavelengths long: **not lumped** (a transmission line). (b) $\lambda = 15$ m, so the trace is $0.30/15 = 0.020$ wavelengths long: **lumped**.

**4.** $NM_L = 0.45 - 0.15 = 0.30$ V and $NM_H = 1.05 - 0.75 = 0.30$ V.

**5.** $p = Q(0.45/0.1) = Q(4.5) = 3.40\times10^{-6}$. Over 1,000 stages: $1 - (1 - p)^{1000} = 3.39\times10^{-3}$, i.e. **0.34%**.

**6.** $\Gamma_s = (30 - 50)/(30 + 50) = -0.25$. Launched wave: $50/80 = 0.625$ V. First arrival at the open end: $2 \times 0.625 = 1.25$ V. Second arrival: the reflected 0.625 V returns, reflects to $0.625 \times (-0.25) = -0.15625$ V and doubles at the open end, so the far end reads $1.25 - 0.3125 = 0.9375$ V.

**7.** (a) 10 mF: `M` is milli in SPICE; mega is `MEG`. (b) $3.3 \times 20/30 = 2.200$ V.

**8.** $\sqrt{10^{16} + 1}$ rounds to exactly $10^8$, because $10^{16} + 1$ is not representable (the spacing of doubles there is 2), so the difference cancels to 0. Stable form: $\sqrt{x + 1} - \sqrt{x} = \frac{1}{\sqrt{x + 1} + \sqrt{x}} \approx \frac{1}{2\times10^8} = 5.00\times10^{-9}$.

**9.**

- (a) F·V² = (C/V)·V² = C·V = J ✓.
- (b) Ω/H = Ω/(Ω·s) = 1/s ✓. This is in fact the corner frequency of an RL low-pass.
- (c) $\sqrt{\text{H·F}} = \sqrt{\text{s}^2}$ = s ✓.
- (d) A²/Ω = A³/V, not W ✗. The correct forms are $P = I^2R$ or $P = V^2/R$.

**10.** $3\times10^{10} \times 0.02 \times 2.5\times10^9 \times 0.4\times10^{-15} = 600$ W. That is plausible only for the very largest datacenter chips, and high for most. The activity factor is the most uncertain input, and leakage is ignored.

**11.** $0.995^{40} = 0.818$, i.e. **81.8%**.

**12.** Sum of the most-likely values: $10 + 14 = 24$ weeks. Expected: $(8 + 10 + 15)/3 + (12 + 14 + 22)/3 = 11 + 16 = 27.0$ weeks. Each phase can overrun much more than it can underrun, so the averages sit above the most-likely values. Adding the most-likely values therefore produces a plan that is met well under half the time.

**13.** SNR $= 10^{1.5} = 31.62$, so $C = 40\times10^6 \times \log_2(32.62) = 201.1$ Mb/s. Doubling the bandwidth doubles $C$ (402 Mb/s). Doubling the SNR adds only about 1 bit/s/Hz (about 40 Mb/s here), so choose bandwidth.

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| X00.1a | battery energy | 19.35 | Wh |
| X00.1b | average power | 0.645 | W |
| X00.2a | one-lane power | 0.896 | W |
| X00.2b | 32-lane power | 28.7 | W |
| X00.3a | length in wavelengths at 1 GHz | 2.0 | — |
| X00.3b | length in wavelengths at 10 MHz | 0.020 | — |
| X00.4a | $NM_L$ | 0.30 | V |
| X00.4b | $NM_H$ | 0.30 | V |
| X00.5a | per-stage error probability | 3.40×10^-6 | — |
| X00.5b | error probability over 1000 stages | 0.34 | % |
| X00.6a | $\Gamma_s$ | −0.25 | — |
| X00.6b | launched wave | 0.625 | V |
| X00.6c | far end, first arrival | 1.25 | V |
| X00.6d | far end, second arrival | 0.9375 | V |
| X00.7 | divider output | 2.200 | V |
| X00.8 | stable value | 5.00×10^-9 | — |
| X00.10 | dynamic power estimate | 600 | W |
| X00.11 | first-silicon success probability | 81.8 | % |
| X00.12a | sum of most-likely values | 24 | weeks |
| X00.12b | expected total duration | 27.0 | weeks |
| X00.13 | Shannon capacity | 201.1 | Mb/s |
