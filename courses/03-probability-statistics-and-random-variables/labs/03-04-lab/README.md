# Lab 03-04 · Joint Distributions, Correlation and the CLT

**Chapter:** [03-04](../../chapters/03-04-joint-distributions-and-clt.md) · **Notebook:** [03-04-joint-and-clt.ipynb](03-04-joint-and-clt.ipynb) · **Time:** about 75 minutes

## Objective

1. Estimate a joint PMF, marginals, a conditional probability and a covariance from samples.
2. Generate correlated Gaussian noise with a Cholesky factor and confirm $\sigma_d = \sigma\sqrt{2(1 - \rho)}$ for a differential receiver.
3. See that the density of a sum is the convolution of the densities.
4. Watch the CLT work in the center of a skewed sum and fail in its tail.
5. Confirm that a complex Gaussian has a Rayleigh envelope, a uniform phase, and the two independent.
6. Simulate Reed–Solomon codeword failures from bit errors, then see what error bursts do to them.

## Background

Chapter sections 3.1–3.8 and Examples 03-04.1 to 03-04.7. The random-number generator is seeded (2026), so the printed numbers match the ones below.

## Procedure

1. Run all cells in order, writing a prediction before each **🔮 Predict** cell.
2. **Part 2:** predict the differential noise at ρ = 0.9.
3. **Part 4:** predict whether the 30-term sum's tail at 3σ is above or below $Q(3)$.
4. **Part 5:** predict the mean envelope and whether envelope and phase are correlated.
5. **Part 6:** predict whether bursts raise or lower the codeword failure rate.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | joint PMF estimate | close to 0.85 / 0.05 / 0.05 / 0.05; covariance 0.04 (seeded 0.0398), correlation 0.4444 (seeded 0.4462) |
| 2 | differential noise, σ = 10 mV per wire | 17.32, 14.14, 10.00, 4.472 and 1.414 mV for ρ = −0.5, 0, 0.5, 0.9, 0.99, each matched within about 0.05% |
| 3 | sums of uniforms | three-term density at 0 is 0.75 against 0.7979 for the Gaussian; two-term variance 1/6 |
| 4 | CLT tails | skewness about $2/\sqrt n$; at $n = 30$, $P(Z > 3) = 0.004164$ exactly (seeded 0.00425), about 3.08 times $Q(3) = 0.001350$ |
| 5 | complex Gaussian | mean envelope 1.2533 (seeded 1.2540); mean power 2; $P(R > 3) = e^{-4.5} = 0.01111$; correlation of envelope and phase near 0 |
| 6 | FEC at BER $1.5\times10^{-3}$ | binomial formula 0.008722 (seeded simulation 0.00830); with bursts of mean length 2 and the same average, about 0.078: nine times worse |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 03-04.a | covariance of the die pair | 0.04 | — |
| Lab 03-04.b | correlation of the die pair | 0.4444 | — |
| Lab 03-04.c | differential noise at ρ = 0.9 | 4.472 | mV |
| Lab 03-04.d | differential noise at ρ = −0.5 | 17.32 | mV |
| Lab 03-04.e | density at 0 of three uniforms | 0.75 | — |
| Lab 03-04.f | exact tail of 30 exponentials at 3σ | 0.004164 | — |
| Lab 03-04.g | ratio to Q(3) | 3.08 | — |
| Lab 03-04.h | mean Rayleigh envelope, σ = 1 | 1.2533 | — |
| Lab 03-04.i | P(R > 3), σ = 1 | 0.01111 | — |
| Lab 03-04.j | UCR at BER 1.5e-3 | 0.008722 | — |
| Lab 03-04.k | mean wrong symbols at BER 1.5e-3 | 8.105 | — |

## Discussion questions

1. In Part 1 the dies are positively correlated. Explain why that *raises* the fraction of pairs with no defects, and what it implies for the yield of a large die compared with a Poisson model.
2. Part 4 shows the CLT underestimating the right tail of a skewed sum by a factor of three at 3σ. Name two engineering quantities that are sums of skewed terms, and say where a Gaussian budget for them would be risky.
3. In Part 6, what physical mechanism in a receiver produces bursts, and which two remedies does the chapter mention?

## Optional hardware version

With an FPGA transceiver or a BERT that reports error counts per frame or per block, run a link at a raised error rate (for example by reducing the transmit swing or adding attenuation). Histogram the errors per block and compare the variance with the mean: a Poisson process has them equal, while bursts make the variance larger (overdispersion, 03-03).
