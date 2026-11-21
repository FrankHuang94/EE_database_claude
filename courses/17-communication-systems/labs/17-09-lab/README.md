# Lab 17-09 · Path Loss, Multipath and Fading

Chapter: [17-09 · Wireless Channels: Fading and Multipath](../../chapters/17-09-wireless-channels.md)

## Objective

Model a wireless channel at every scale and check the chapter's results:

- free-space and two-ray path loss, and the two-ray breakpoint;
- lognormal shadowing and coverage probability;
- frequency selectivity from an exponential power-delay profile;
- Doppler, the Jakes autocorrelation, and the level-crossing statistics of Rayleigh fading;
- Rayleigh and Rician outage;
- BPSK error rates in fading with and without maximal-ratio combining.

## Background

Free-space power falls as $1/d^2$; with a ground reflection it falls as $1/d^4$ beyond $4h_th_r/\lambda$ (§3.1–3.2). Shadowing adds a Gaussian term in decibels (§3.3). Multipath makes $H(f) = \sum a_ie^{-j2\pi f\tau_i}$, whose frequency correlation is the Fourier transform of the PDP (§3.4). Motion makes each path's phase rotate at up to $f_D$, giving the $J_0$ autocorrelation (§3.5). Many paths sum to a complex Gaussian gain: Rayleigh fading (§3.6), whose average BPSK error rate is $\tfrac12(1 - \sqrt{\bar\gamma/(1 + \bar\gamma)})$ (§3.7).

## Files

- `channels.py`: `fspl_db`, `fspl_p525_db`, `friis_pr_dbm`, `two_ray_loss_db`, `two_ray_breakpoint`, `log_distance_db`, `umi_breakpoint`, `umi_los_db`, `umi_nlos_db`, `shadow_margin_db`, `pdp_stats`, `freq_correlation`, `coherence_bandwidth`, `exp_pdp_coherence_bw`, `lognormal_ds_median`, `doppler_hz`, `jakes_corr`, `coherence_time`, `lcr`, `afd`, `rayleigh_sos`, `rayleigh_outage`, `rician_outage`, `ber_bpsk_rayleigh`, `ber_bpsk_mrc`, `required_db`.
- `17-09-channels-lab.ipynb`: the guided notebook.

## Procedure

1. **Two rays.** For antennas at 10 m and 1.5 m at 3.5 GHz, predict the breakpoint and the slope beyond it. Plot the exact two-ray loss against free space from 10 m to 10 km.
2. **Coverage.** Simulate 100 000 NLOS users with σ = 7.82 dB shadowing. Predict, then measure, the fraction whose loss exceeds the median by less than 10 dB.
3. **Frequency selectivity.** Draw 2000 random channels with 200 exponentially distributed path delays (τ_rms = 100 ns) and complex Gaussian gains. Estimate the correlation of $H(f)$ against frequency separation and find where it falls to 0.5.
4. **Doppler.** Generate one second of Rayleigh fading at $f_D$ = 100 Hz. Compare its autocorrelation with $J_0(2\pi f_D\tau)$, then count fades below −10 dB and their durations against the formulas.
5. **Outage.** Predict the outage at 10 dB margin for Rayleigh fading and for Rician fading with K = 6 dB; simulate both.
6. **BER in fading.** Simulate BPSK over flat Rayleigh fading with 1, 2 and 4 MRC branches from 0 to 30 dB and compare with the closed forms.

## Expected results

- Part 1: breakpoint 700 m; free-space slope (20 dB/decade) with oscillations before it and 40 dB/decade after.
- Part 2: about 90% (the 90% margin is 1.28σ = 10.0 dB).
- Part 3: correlation 0.5 near 2.76 MHz.
- Part 4: autocorrelation on $J_0$; about 72 fades per second lasting about 1.3 ms on average.
- Part 5: 9.5% (Rayleigh) and about 1.6% (Rician, K = 6 dB).
- Part 6: simulation on the formulas; at 15 dB the BER falls from $7.7 \times 10^{-3}$ (one branch) to $1.8 \times 10^{-4}$ (two) and about $10^{-7}$ (four).

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 17-09.a | two-ray breakpoint, 10 m and 1.5 m, 3.5 GHz | 700 | m |
| Lab 17-09.b | fraction within 10 dB of the median loss | 0.900 | — |
| Lab 17-09.c | coherence bandwidth, τrms = 100 ns | 2.76 | MHz |
| Lab 17-09.d | −10 dB fades per second, fD = 100 Hz | 71.7 | 1/s |
| Lab 17-09.e | average fade duration | 1.33 | ms |
| Lab 17-09.f | Rician (K = 6 dB) outage, 10 dB margin | 1.65 | % |
| Lab 17-09.g | BPSK, 2-branch MRC at 15 dB | 1.78e-4 | — |

## Discussion

1. Why does the two-ray loss stop depending on frequency beyond the breakpoint?
2. In Part 4, why do fades below −20 dB last much shorter than the coherence time, while −10 dB fades do not?
3. Why does a Rician channel with K = 6 dB still show a slope of one decade per 10 dB at very small outage probabilities?

## Answers

1. Beyond the breakpoint the direct and reflected rays nearly cancel, and the residual is proportional to their phase difference $4\pi h_th_r/(\lambda d)$. That factor's $1/\lambda$ cancels the $\lambda$ of the free-space term, leaving $h_t^2h_r^2/d^4$.
2. A deep fade is a narrow notch in the envelope: the gain passes close to zero and moves away quickly, because the derivative of the complex gain is not small at the crossing. The coherence time measures how long the whole gain stays correlated, which is much longer than the time spent in a deep notch. At $f_D$ = 100 Hz, $T_c$ = 2.42 ms; the mean −10 dB fade lasts 1.33 ms, not much shorter, but the mean −20 dB fade lasts only 0.40 ms, a sixth of $T_c$. For deep fades the average fade duration $(e^{\rho^2} - 1)/(\sqrt{2\pi}f_D\rho) \approx \rho/(\sqrt{2\pi}f_D)$ scales with ρ, so each further 10 dB of depth divides it by about 3.
3. At small thresholds the noncentral chi-square CDF is still linear in the threshold (the density at zero power is finite, $\propto e^{-K}$), so the slope is the same as Rayleigh; the line-of-sight path only lowers the constant, by about $e^{-K}(K + 1)$.

## Optional hardware

A software-defined radio receiving a continuous tone while being carried around a room shows Rayleigh-like fading directly: record the envelope, plot its histogram against the Rayleigh density, and measure fade durations at walking speed. Moving the antenna by a few centimetres shows how quickly the field decorrelates.
