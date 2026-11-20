# Problems 16-06 · FIR Filter Design

Chapter: [16-06](../chapters/16-06-fir-filter-design.md) · Worked solutions: [16-06 solutions](../solutions/16-06-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** A filter of order $M$ has $M + 1$ taps $h[0..M]$; $\omega$ is in rad/sample; $A(\omega)$ is the real amplitude response of §3.2. Ripple "$\pm x$ dB" means $20\log_{10}(1 + \delta_p) = x$; "peak to peak" means $20\log_{10}\big((1 + \delta_p)/(1 - \delta_p)\big)$. Use the window table of §3.4 and Kaiser's formulas of §3.5 as given. Problems marked *(lab)* ask for a number that needs the lab's `firdesign.py` (or any equivalent tool).

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 16-06.1 [A]

**Five small filters.** For each tap sequence, give the linear-phase type (or "not linear phase"), the group delay in samples, and $\lvert H\rvert$ at $\omega = 0$ and $\omega = \pi$: (a) $(1, -2, 1)$; (b) $(1, 3, 3, 1)$; (c) $(1, 0, -1)$; (d) $(1, -3, 3, -1)$; (e) $(1, 2, 3)$. Which of them could be the starting point for a high-pass design, and why can the others not?

### Problem 16-06.2 [A]

**Specifications in decibels.** Convert to linear tolerances $\delta_p$ and $\delta_s$: (a) 0.5 dB peak-to-peak passband ripple and 40 dB stopband attenuation; (b) 0.01 dB peak to peak and 80 dB. For each, which tolerance must a window-method design meet, and with what attenuation $A$?

### Problem 16-06.3 [A]

**Truncating by hand.** Compute the taps of the truncated ideal low-pass filter with $\omega_c = \pi/3$ and $M$ = 6, and its DC gain $A(0)$. Why is the DC gain not exactly 1?

### Problem 16-06.4 [B]

**Gibbs, measured.** *(lab)* Truncate the ideal low-pass filter with $\omega_c = 0.3\pi$ to $M$ = 30 and to $M$ = 300 (rectangular window). For each, find the passband overshoot and how far below the cutoff it peaks, and compare the peak positions with the prediction $2\pi/(M + 1)$ of §3.3. Did ten times as many taps reduce the overshoot?

### Problem 16-06.5 [B]

**Choosing a window.** A low-pass filter needs a passband edge $0.4\pi$, stopband edge $0.45\pi$, passband ripple within ±0.05 dB and 50 dB stopband attenuation. (a) Which tolerance governs a window design, and what attenuation must it reach? (b) Which fixed windows of §3.4 qualify, and what order does each need? (c) What do Kaiser's formulas give? (d) *(lab)* Check the Hamming and Kaiser designs against the specification.

### Problem 16-06.6 [B]

**When the Kaiser formula falls short.** *(lab)* Design a low-pass filter with $\omega_p = 0.3\pi$, $\omega_s = 0.35\pi$ and 70 dB attenuation in both bands ($\delta_p = \delta_s = 10^{-3.5}$). (a) Compute $\beta$ and $M$ from Kaiser's formulas and check the design. (b) It falls just short. Compare two repairs: adding taps at the same $\beta$, or re-running the formulas for 71 dB.

### Problem 16-06.7 [B]

**Frequency sampling by hand.** A 15-tap type I filter is specified by $A_k = 1$ for $k$ = 0, 1, 2 and $A_k = 0$ for $k$ = 3 to 7, at $\omega_k = 2\pi k/15$. (a) Compute $h[7]$, $h[6]$ and $h[0]$. (b) Show that $A(\omega_k)$ equals the specified samples. (c) *(lab)* Evaluate $A(\omega)$ midway between the last passband sample and the first stopband sample.

### Problem 16-06.8 [B]

**Estimating an equiripple order.** A low-pass filter needs $\delta_p = 0.01$, $\delta_s = 0.001$ and a transition width of $0.02f_s$ (passband edge $0.25f_s$). (a) Give the stopband weight. (b) Estimate the order with Kaiser's formula and the length with Bellanger's. (c) *(lab)* Find the actual shortest equiripple filter that meets the specification.

### Problem 16-06.9 [B]

**An FPGA budget.** A 255-tap symmetric FIR filter runs at 100 MS/s on an FPGA whose DSP slices each complete one multiplication per cycle at 400 MHz. How many multiplications per output are needed with and without folding, how many per second with folding, and how many DSP slices in each case?

### Problem 16-06.10 [C]

**A Remez design by hand.** Find the minimax 3-tap type I low-pass filter for the passband $[0, \pi/3]$ and stopband $[\pi/2, \pi]$ with equal weights. Use the alternation theorem: guess the extremal set $\{\pi/3, \pi/2, \pi\}$, solve for $a_0$, $a_1$ and $\delta$, check that the error nowhere exceeds $\delta$, and identify the filter.

### Problem 16-06.11 [C]

**Why decimate first.** A receiver must select a channel with a passband to 9 MHz and a stopband from 10 MHz, 0.1 dB peak-to-peak ripple and 80 dB attenuation. (a) Estimate the order, folded multipliers and multiplications per second of an equiripple filter running at 122.88 MS/s. (b) Repeat at 30.72 MS/s, after the signal has been decimated by 4 (assume the decimation itself is handled separately). (c) What is the ratio of costs, and why is it close to 16? (d) *(lab)* Find the actual shortest equiripple lengths at both rates.

### Problem 16-06.12 [C]

**Half-band filters.** A low-pass filter with $\omega_c = \pi/2$ is designed by the window method with a symmetric window whose middle value is 1 and which has no zero samples (a Hamming or Kaiser window, for example; a symmetric Hann window's end samples are zero). (a) Show that every tap at an even, nonzero offset from the middle is zero. (b) Show that $A(\omega) + A(\pi - \omega) = 1$ for all $\omega$, and hence $A(\pi/2) = 1/2$. (c) For $M$ = 46, how many taps are nonzero, and how many general multipliers does a folded implementation need, compared with a general 47-tap symmetric filter?

---

## Objective coverage

| Learning objective (chapter 16-06) | Problems |
|---|---|
| 1. Linear-phase types, delay and forced zeros | 1, 12 |
| 2. Specifications and ripple conversions | 2, 5 |
| 3. Window and Kaiser designs, Gibbs | 3, 4, 5, 6 |
| 4. Frequency sampling | 7 |
| 5. Equiripple design and the alternation theorem | 8, 10 |
| 6. Order estimates and implementation cost | 8, 9, 11, 12 |
