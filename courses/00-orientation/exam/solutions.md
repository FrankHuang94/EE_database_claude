# Course 00 · Final Exam — Solutions

Exam: [README.md](README.md). All numbers are recomputed by [verify_00_exam.py](../verify/verify_00_exam.py).

**1.** Energy $= 5.000\text{ Ah} \times 3.87\text{ V} = 19.35$ Wh. Average power $= 19.35/30 = 0.645$ W.

**2.** Rubric: 8 points, about 1.5 per part; full marks need a plausible subdiscipline, the leaked abstraction and an owner for each.

- (a) Power electronics and circuits. The leaked abstraction is the **ideal supply** of the digital-logic view (supply droop). Owner: power-integrity or PMIC engineer, with the RF and board designers.
- (b) Systems and embedded engineering. The leaked abstraction is **"power is free"** in the software and RTL views: sleep states not entered, radio duty cycle higher than modeled. Owner: system power architect, with firmware.
- (c) Signal integrity and electromagnetics. The leaked abstraction is the **lumped circuit**: the cable is long compared with the edge rate, so it is a transmission line with reflections and loss. Owner: signal-integrity and package/board engineers.
- (d) Devices and analog/mixed-signal (image sensors). Dim light means few photons, so noise that the digital abstraction hides (shot and read noise) dominates. Owner: sensor and analog designers; image-processing software can only partly compensate.
- (e) Digital VLSI and architecture. The leaked abstraction is the **ISA**: functionally identical code can produce different switching activity and timing, and therefore different power. Owner: power and performance architects, with the software team.

**3.** (a) $\lambda = 1.5\times10^8/10^9 = 0.15$ m, so the trace is $0.30/0.15 = 2.0$ wavelengths long: **not lumped** (a transmission line). (b) $\lambda = 15$ m, so the trace is $0.30/15 = 0.020$ wavelengths long: **lumped**.

**4.** $NM_L = 0.45 - 0.15 = 0.30$ V and $NM_H = 1.05 - 0.75 = 0.30$ V.

**5.** $p = Q(0.45/0.1) = Q(4.5) = 3.40\times10^{-6}$. Over 1,000 stages: $1 - (1 - p)^{1000} = 3.39\times10^{-3}$, i.e. **0.34%**.

**6.** $\Gamma_s = (30 - 50)/(30 + 50) = -0.25$. Launched wave: $50/80 = 0.625$ V. First arrival at the open end: $2 \times 0.625 = 1.25$ V. Second arrival: the reflected 0.625 V returns, reflects to $0.625 \times (-0.25) = -0.15625$ V and doubles at the open end, so the far end reads $1.25 - 0.3125 = 0.9375$ V.

**7.** (a) **10 mF**: `M` is milli in SPICE; mega is `MEG`. (b) $3.3 \times 20/30 = 2.200$ V.

**8.** (a) $\sqrt{b^2 - 4} = 10^8\sqrt{1 - 4\times10^{-16}} \approx 10^8 - 2\times10^{-8}$. Near $10^8$, adjacent doubles are $1.49\times10^{-8}$ apart, so the square root is stored as $10^8 - 1.49\times10^{-8}$. Subtracting it from $b$ keeps only that rounding step: **catastrophic cancellation**. The literal result is $1.49\times10^{-8}/2 = 7.45\times10^{-9}$. (b) Multiplying top and bottom by $b + \sqrt{b^2 - 4}$ gives $x = \dfrac{b^2 - (b^2 - 4)}{2\big(b + \sqrt{b^2 - 4}\big)} = \dfrac{2}{b + \sqrt{b^2 - 4}} = 1.000\times10^{-8}$. Check: the roots multiply to 1 and the large root is about $10^8$, so the small one is about $10^{-8}$ ✓. (c) $(7.45 - 10)/10 = $ **−25.5%**, an error no tolerance would forgive.

**9.**

- (a) F·V² = (C/V)·V² = C·V = J ✓.
- (b) Ω/H = Ω/(Ω·s) = 1/s ✓. This is in fact the corner frequency of an RL low-pass.
- (c) $\sqrt{\text{H·F}} = \sqrt{\text{s}^2}$ = s ✓.
- (d) A²/Ω = A³/V, not W ✗. The correct forms are $P = I^2R$ or $P = V^2/R$.

**10.** $3\times10^{10} \times 0.02 \times 2.5\times10^9 \times 0.4\times10^{-15} = 600$ W. That is plausible only for the very largest datacenter chips, and high for most. The activity factor is the most uncertain input, and leakage is ignored.

**11.** $0.995^{40} = 0.818$, i.e. **81.8%**.

**12.** Sum of the most-likely values: $10 + 14 = 24$ weeks. Expected: $(8 + 10 + 15)/3 + (12 + 14 + 22)/3 = 11 + 16 = 27.0$ weeks. Each phase can overrun much more than it can underrun, so the averages sit above the most-likely values. Adding the most-likely values therefore produces a plan that is met well under half the time.

**13.** SNR $= 10^{1.5} = 31.62$, so $C = 40\times10^6 \times \log_2(32.62) = 201.1$ Mb/s. Doubling the bandwidth doubles $C$ to **402.2 Mb/s** (assuming the noise power, which grows with bandwidth, is held fixed by raising signal power to keep SNR at 15 dB). Doubling the SNR adds only about 1 bit/s/Hz: $40\times10^6\log_2(64.25) = $ **240.2 Mb/s**, a gain of **39.1 Mb/s**. Choose bandwidth when it is available; at high SNR, capacity grows only logarithmically with power.

**14.** Rubric: 8 points (3 for (a) and (b), 2 for (c)).

- (a) A letter change (A→B) means a **full-layer revision**: the fix needs transistor-layer masks, not just metal. A metal-only fix would have been named A1. So the bug could not be fixed by rewiring spare gates or hidden in firmware.
- (b) **Not plausible.** A full-layer revision restarts the wafers from the beginning: 14–20 weeks of fab cycle time for an advanced process (2021 data, [R-020](../../../reference/research-log.md#r-020--fab-cycle-time-and-maskeuv-layer-counts)), plus mask making, packaging, testing and validation of the new silicon, then qualification before volume shipment. A realistic span from tapeout to volume is two quarters or more.
- (c) Good questions include: Why could this not be a metal-only fix or a firmware workaround? What else did A0 validation find, and how much of the chip has been validated? Are there parked or early-started wafers, and what does the fab commit to on cycle time? What is the qualification plan, and do customers accept A0 samples meanwhile? What changed in verification so the same class of bug cannot escape again?

**15.** Rubric: 8 points.

- **Right:** WSTS's Spring 2026 forecast did put 2026 sales at about \$1.51 trillion, up 89.9% **[Industry estimate]**.
- **Misleading:** (1) It is a *forecast* for 2026, not a measured market size; the last full-year actual was \$795.6 B for 2025. (2) "Growing 90% a year" turns one boom year into a rate. The growth is driven largely by memory (+249% forecast), mostly through prices, which are cyclical. (3) A forecast made mid-boom is volatile, and WSTS itself warned its later updates were not new forecasts. (4) There is no date on the claim.
- **Accurate restatement:** "The semiconductor market was \$796 B in 2025 (WSTS actual); WSTS's June 2026 forecast projected about \$1.5 trillion for 2026, driven mainly by memory prices, a boom-year figure that should not be extrapolated."

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| X00.1a | battery energy | 19.35 | Wh |
| X00.1b | average power | 0.645 | W |
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
| X00.7a | SPICE value of 10M | 10 | mF |
| X00.7b | divider output | 2.200 | V |
| X00.8a | literal evaluation | 7.45×10^-9 | — |
| X00.8b | stable value | 1.000×10^-8 | — |
| X00.8c | relative error of literal value | −25.5 | % |
| X00.10 | dynamic power estimate | 600 | W |
| X00.11 | first-silicon success probability | 81.8 | % |
| X00.12a | sum of most-likely values | 24 | weeks |
| X00.12b | expected total duration | 27.0 | weeks |
| X00.13a | Shannon capacity | 201.1 | Mb/s |
| X00.13b | capacity with doubled bandwidth | 402.2 | Mb/s |
| X00.13c | capacity with doubled SNR | 240.2 | Mb/s |
| X00.13d | gain from doubled SNR | 39.1 | Mb/s |
| X00.15a | WSTS 2026 forecast | 1.51 | US$ T |
| X00.15b | WSTS 2025 actual | 795.6 | US$ B |
