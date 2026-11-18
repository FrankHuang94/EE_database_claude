# Lab 03-02 · Random Variables and Distributions

**Chapter:** [03-02](../../chapters/03-02-random-variables-and-distributions.md) · **Notebook:** [03-02-distributions.ipynb](03-02-distributions.ipynb) · **Time:** about 75 minutes

## Objective

1. See sampled histograms converge to their PMFs and PDFs, and see why tails rarer than one over the sample count are invisible to sampling.
2. Measure how fast the binomial approaches the Poisson as $n$ grows with $np$ fixed.
3. Build a Poisson process from exponential gaps, and confirm that its counts are Poisson with variance equal to the mean.
4. Contrast the memoryless exponential lifetime with a wear-out lifetime.
5. Measure a bit error rate by Monte Carlo and compare it with $Q(A/\sigma)$.
6. Check the dual-Dirac model's tail claim and the eye opening $1\,\text{UI} - TJ$ against a numerically computed bathtub curve.

## Background

Chapter sections 3.1–3.8 and Examples 03-02.1 to 03-02.7. No circuit simulation is needed: the "hardware" is a random-number generator with a fixed seed (2026), so your printed numbers match the ones quoted here.

## Procedure

1. Run all notebook cells in order, writing down a prediction before each **🔮 Predict** cell.
2. **Part 1:** predict how many Gaussian samples you need for 100 beyond ±3σ and beyond ±5σ.
3. **Part 2:** predict how the binomial–Poisson distance scales with $n$.
4. **Part 3:** predict the fraction of empty unit windows at a rate of 2 per unit time.
5. **Part 4:** predict whether a 500 h survivor's mean remaining life is above, at or below 1000 h for each model.
6. **Part 5:** predict the number of bits needed for 100 errors at $A/\sigma = 4$.
7. **Part 6:** predict the tail fraction of edge crossings beyond $DJ/2 + 3\sigma$.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Gaussian tails | 100 events beyond ±3σ need about 37,040 samples; beyond ±5σ, about $1.744\times10^8$. With $10^5$ samples the seeded run measures $2.65\times10^{-3}$ beyond ±3σ (theory $2.700\times10^{-3}$) and none beyond ±5σ |
| 2 | Poisson limit | total variation distance 0.02841 at $n = 12$, falling tenfold per decade to $2.675\times10^{-5}$ at $n$ = 12,000; always below Le Cam's bound $\lambda^2/n$ |
| 3 | Poisson process | count mean and variance both close to 2 (seeded run: 2.0061 and 2.0136); empty windows 0.1333 against $e^{-2} = 0.1353$ |
| 4 | memorylessness | exponential survivors to 500 h: 0.6065 (theory), mean remaining life about 1000 h (seeded 998.2 h). Weibull shape 3: survivors 0.9148, mean remaining life 558.4 h |
| 5 | Monte Carlo BER | measured BER within Poisson scatter of $Q(A/\sigma)$ at $A/\sigma$ = 2, 3, 4; 100 errors at $A/\sigma = 4$ need $3.157\times10^6$ bits |
| 6 | dual-Dirac | crossings beyond $DJ/2 + 3\sigma$: seeded $6.710\times10^{-4}$ against $\tfrac12Q(3) = 6.749\times10^{-4}$; the far Dirac contributes about $10^{-22}$. Eye opening at $10^{-12}$ from the bathtub 6.367 ps, equal to $1\,\text{UI} - TJ$ (industry convention); the literal model, a factor 4 lower in BER, gives 6.837 ps (multiplier 13.677) |
| Your turn 1 | offset slicer at $A/\sigma = 4$ | $\tfrac12[Q(3.5) + Q(4.5)] = 1.180\times10^{-4}$ |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 03-02.a | samples for 100 beyond ±3σ | 37040 | samples |
| Lab 03-02.b | samples for 100 beyond ±5σ | 1.744×10^8 | samples |
| Lab 03-02.c | total variation distance, n = 12 | 0.02841 | — |
| Lab 03-02.d | total variation distance, n = 12,000 | 2.675×10^-5 | — |
| Lab 03-02.e | Poisson P(0) at λ = 2 | 0.1353 | — |
| Lab 03-02.f | exponential survival to 500 h | 0.6065 | — |
| Lab 03-02.g | Weibull survival to 500 h | 0.9148 | — |
| Lab 03-02.h | Weibull mean remaining life after 500 h | 558.4 | h |
| Lab 03-02.i | bits for 100 errors at A/σ = 4 | 3.157×10^6 | bits |
| Lab 03-02.j | near-Dirac tail fraction | 6.749×10^-4 | — |
| Lab 03-02.k | eye opening at 1e-12 | 6.367 | ps |
| Lab 03-02.l | BER with offset slicer | 1.180×10^-4 | — |
| Lab 03-02.m | eye opening at 1e-12, literal model | 6.837 | ps |
| Lab 03-02.n | literal multiplier 2 Qinv(4e-12) | 13.677 | — |
| Lab 03-02.o | BER bound from 1e12 error-free bits at 95% | 2.996×10^-12 | — |

## Discussion questions

1. Part 1 shows that $10^5$ samples see nothing beyond 5σ. A vendor claims a BER of $10^{-15}$ from a measurement of $10^{12}$ bits with no errors. What did they actually measure, and what model are they relying on for the rest?
2. In Part 3, what would you see in the count variance if events arrived in bursts of two? Which real mechanisms produce bursty errors in a link or memory?
3. A supplier quotes 50 FIT for a component that is known to wear out (for example a flash cell or an electrolytic capacitor). Using Part 4, explain what that FIT number can and cannot tell you about field returns in year five.

<details><summary>Answers to the discussion questions</summary>

1. Zero errors in $10^{12}$ bits demonstrate, at 95% confidence, only a BER below $-\ln0.05/10^{12} = 2.996\times10^{-12}$ (03-01). The remaining three decades to $10^{-15}$ come from a model: a Gaussian (dual-Dirac) extrapolation of the bathtub walls, which is only as good as the Gaussian tail assumption.
2. If errors came in bursts of two, the count's variance would be twice its mean (a Poisson number of bursts, each of two errors: variance $\lambda\,\mathbb{E}[K^2] = 4\lambda$ against mean $2\lambda$; 03-04 §3.5). Bursty mechanisms include decision-feedback equalizer error propagation in links and multi-cell upsets, where one particle strike flips adjacent memory cells.
3. A FIT number is a constant rate; for a wear-out part the hazard rises, so year-five returns will exceed FIT × hours, and Part 4's Weibull survivors have less remaining life (558 h against 1000 h), not the same. Ask for the Weibull shape or the $B_1$ life at the mission profile, not the FIT.

</details>

## Optional hardware version

With any oscilloscope or FPGA transceiver that offers an eye or bathtub scan (most vendor transceiver tools include one), measure a bathtub curve at a data rate you can reach. Fit the dual-Dirac model to its walls between $10^{-4}$ and $10^{-9}$, extract DJ and RJ, and extrapolate the eye opening to $10^{-12}$. Then compare the extrapolation with a longer error-free run at a sampling point inside your predicted eye.
