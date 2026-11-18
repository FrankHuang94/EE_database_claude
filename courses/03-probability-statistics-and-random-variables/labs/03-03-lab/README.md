# Lab 03-03 · Expectation, Variance and Functions of Random Variables

**Chapter:** [03-03](../../chapters/03-03-expectation-and-functions-of-rvs.md) · **Notebook:** [03-03-expectation.ipynb](03-03-expectation.ipynb) · **Time:** about 75 minutes

## Objective

1. Watch sample averages converge to expectations, at the rate $\sigma/\sqrt n$.
2. Confirm that linearity of expectation survives clustered defects while the spread does not.
3. Check the power decomposition (total = DC + AC) on a converter current and a random-phase sinusoid.
4. Compare sampled functions of random variables (squared Gaussian, log-normal) with the change-of-variables densities.
5. See how loose Chebyshev's inequality is, and which distribution makes it tight.
6. Measure the PAPR of OFDM and DFT-spread OFDM against the complex-Gaussian prediction.
7. Find the best loading factor for an 8-bit ADC with a Gaussian input.

## Background

Chapter sections 3.1–3.9 and Examples 03-03.1 to 03-03.7. As in Labs 03-01 and 03-02, the "hardware" is a seeded random-number generator (seed 2026), so the printed numbers match the ones quoted below.

## Procedure

1. Run all notebook cells in order, writing a prediction before each **🔮 Predict** cell.
2. **Part 2:** predict whether clustering changes the mean, the standard deviation, or both.
3. **Part 4:** predict the fraction of noise-power samples above 4 times the average, and the mean-to-median ratio of the leakage.
4. **Part 5:** predict which distribution comes closest to the Chebyshev bound.
5. **Part 6:** predict the OFDM PAPR at $10^{-4}$ and the improvement from DFT spreading.
6. **Part 7:** predict the best loading factor for 8 bits.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | retransmissions | theory $\mathbb{E}[K] = 1.1275$, σ = 0.3791; the seeded 200,000-packet run gives 1.1267 and 0.3779 |
| 2 | good dies per wafer | mean 540 in both models (seeded 539.99 and 540.04); standard deviation 7.141 in theory for independent dies (seeded 7.118) but about 47 with clustering |
| 3 | inductor current | variance 0.75 A², RMS 10.04 A; random-phase sinusoid of amplitude 2: mean square 2 |
| 4 | functions | $P(X^2 > 4) = 2Q(2) = 0.04550$ (seeded 0.04558); standard deviation over mean of $X^2$: 1.414; log-normal mean over median 1.269 (seeded 1.2704) |
| 5 | Chebyshev | at ±3σ: uniform 0, Gaussian about 0.0027, Laplace about 0.014, three-point 0.1111, which equals the bound $1/9$ |
| 6 | PAPR | OFDM at $10^{-4}$: seeded 9.60 dB against the complex-Gaussian 9.643 dB; DFT-spread OFDM about 3 dB lower (seeded 6.67 dB) |
| 7 | ADC loading | optimum $k = 3.924$, SNR 40.60 dB; measured SNRs within about 0.3 dB of the formula; at $k = 3$ about 33.4 dB |
| Your turn 1 | 12-bit loading | optimum $k = 5.013$, 62.71 dB; at $k = 4$ only 51.87 dB |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 03-03.a | mean transmissions | 1.1275 | — |
| Lab 03-03.b | expected good dies per wafer | 540 | — |
| Lab 03-03.c | standard deviation, independent dies | 7.141 | — |
| Lab 03-03.d | RMS inductor current | 10.04 | A |
| Lab 03-03.e | P(X² > 4) | 0.04550 | — |
| Lab 03-03.f | log-normal mean over median | 1.269 | — |
| Lab 03-03.g | Chebyshev bound at ±3σ | 0.1111 | — |
| Lab 03-03.h | complex Gaussian PAPR at 1e-4 | 9.643 | dB |
| Lab 03-03.i | optimum loading, 8 bits | 3.924 | — |
| Lab 03-03.j | optimum SNR, 8 bits | 40.60 | dB |
| Lab 03-03.k | formula SNR at k = 3, 8 bits | 33.44 | dB |
| Lab 03-03.l | Laplace tail beyond ±3 at unit variance | 0.01437 | — |

## Discussion questions

1. In Part 2 the clustered model's standard deviation is more than six times the independent one, with the same mean. A fab reports an average yield of 90% and plans capacity from it. What else should a buyer of wafers ask for, and why?
2. Part 6 shows DFT spreading lowering PAPR by about 3 dB. In the ideal class-B model of Example 03-03.7, what is that worth in average efficiency? Why might a base station still prefer OFDM in the downlink?
3. A product manager proposes setting an ADC's full scale "with 20 dB of headroom above the RMS signal" for a noise-like input. Translate that into a loading factor, and use Part 7 to judge it for 8 and 12 bits.

## Optional hardware version

With any signal generator that can produce an OFDM or noise waveform, and a spectrum analyzer or oscilloscope with a CCDF or statistics function (most modern instruments have one), measure the CCDF of the signal's power. Compare the PAPR at $10^{-2}$ and $10^{-4}$ with the complex-Gaussian predictions of 6.63 dB and 9.64 dB, then capture for ten times longer and watch the reported "peak" or crest factor rise while the CCDF at a fixed probability stays put.
