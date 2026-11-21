# Lab 18-06 · Sampling Inputs, Averaging and a PWM DAC

Chapter: [18-06 · Analog Interfaces: ADC, DAC and PWM](../../chapters/18-06-adc-dac-pwm.md)

## Objective

- See how a sample-and-hold input settles from a real source, and how an external capacitor trades an instantaneous error for a rate-dependent DC error, in a model and in an ngspice simulation with real switches.
- Measure, by Monte Carlo through an ideal quantizer, when averaging adds resolution and when it does not.
- Design a PWM DAC's RC filter and confirm its ripple in ngspice.
- Implement and test the integer arithmetic firmware uses for ADC readings, supply monitoring, decimation and PWM compare values.

## Background

A sample capacitor charging through $R_s + R_{sw}$ settles to half an LSB in $\tau\ln 2^{N+1}$ (§3.2). An external capacitor shares charge with it at once, but at a sample rate $f$ the S/H draws current like a resistor $1/(fC_{sh})$. Averaging $M$ samples of white noise gains $\frac12\log_2 M$ bits only if the noise spreads the samples over several codes (§3.4). A PWM output through an RC filter ripples by about $V_HD(1 - D)T/\tau$ (§3.6).

MCU ADCs are not modelled by QEMU, so this lab uses Python models, ngspice for the analog circuits, and a host C program for the firmware arithmetic.

## Files

- `mcuanalog.py`: `lsb`, `adc_code`, `quantization_noise_rms`, `sqnr_db`, `enob`, `sinad_from_enob`, `settle_time`, `rs_max`, `charge_share_step`, `c_ext_min`, `mux_equilibrium`, `mux_error_approx`, `averaged_code`, `extra_bits`, `zoh_gain`, `pwm_ripple_exact`, `pwm_ripple_approx`, `pwm_tau_for_ripple`, `pwm_simulate`.
- `sh_mux.cir`: a 10 kΩ source with 100 nF at the pin, sampled at 100 kHz by a 3.3 pF S/H through 500 Ω switches, alternating with a 0 V channel (Example 18-06.3).
- `pwm_rc.cir`: a 62.5 kHz, 50% PWM through 4.096 kΩ and 1 µF (Example 18-06.6).
- `c/adcmath.h` and `c/adcmath_test.c`: integer conversions and their exhaustive host test (`python tools/run_c.py 18-06`).
- `18-06-analog-lab.ipynb`: the guided notebook.

## Procedure

1. **Settling.** For a 10 kΩ source with $R_{sw}$ = 0.5 kΩ and $C_{sh}$ = 3.3 pF, predict the worst-case (full-scale step) error in LSB after 62.5 ns and after 312 ns; plot $v_{sh}(t)$.
2. **The external capacitor.** Predict the sampled-value error of Example 18-06.3 at 1, 10 and 100 kHz; compare `mux_equilibrium` with `mux_error_approx`, then run `ngspice -b sh_mux.cir`.
3. **Averaging.** For an input 0.3 LSB above a code, predict the rms error of $M$-sample averages for noise of 0.1, 0.3 and 0.8 LSB rms; run `averaged_code` for $M$ = 1 to 256.
4. **PWM.** Predict the ripple at $D$ = 0.5 and 0.1 for Example 18-06.6's filter; run `ngspice -b pwm_rc.cir` and `pwm_simulate`; then add a second identical RC stage (buffered) and compare the ripple.
5. **Integer arithmetic.** Predict what the C functions return for code 1241 at 3300 mV (in µV), a bandgap code of 1489 for 1200 mV, and sixteen samples of 2047 and 2048 (eight of each, then six and ten) decimated to 14 bits; run the test.

## Expected results

- Part 1: after 62.5 ns a full-scale step is still about 675 LSB from its final value; after 312 ns it is within 0.50 LSB.
- Part 2: errors of 0.172 mV at 1 kHz, 1.14 mV at 10 kHz and 10.91 mV at 100 kHz; the average-current estimate agrees within 1% at 100 kHz but underestimates at 1 kHz, where the charge-sharing step dominates. The netlist reports 10.90 mV, within 0.1% of the recursion.
- Part 3: with 0.8 LSB of noise the rms error follows $\sigma/\sqrt{M}$; with 0.3 LSB it falls, then stalls at a bias of about 0.051 LSB; with 0.1 LSB it stays near the 0.277 LSB bias of Example 18-06.5 for every $M$.
- Part 4: the ripple is 3.2227 mV at $D$ = 0.5 and 1.160 mV at $D$ = 0.1. A second identical stage cuts it to 1.57 µV, a factor of about 2000, the order of $2\pi f_{PWM}\tau$ = 1608 (the factor differs because the second stage filters a triangle, not a sine).
- Part 5: 999829 µV, 3301 mV, and 8190 and 8191 (the second case, 8190.5, rounds up); `TEST PASSED`.

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 18-06.a | full-scale-step error after 62.5 ns, 10 kΩ source | 675 | LSB |
| Lab 18-06.b | full-scale-step error after 312 ns | 0.50 | LSB |
| Lab 18-06.c | sampled-value error at 10 kHz | 1.14 | mV |
| Lab 18-06.d | residual bias with 0.3 LSB of noise | 0.051 | LSB |
| Lab 18-06.e | PWM ripple at D = 0.1 | 1.160 | mV |
| Lab 18-06.j | ripple after two identical stages, D = 0.5 | 1.57 | µV |
| Lab 18-06.f | code 1241 at 3300 mV | 999829 | µV |
| Lab 18-06.g | V_DD from bandgap code 1489 | 3301 | mV |
| Lab 18-06.h | eight 2047s and eight 2048s, 14-bit | 8190 | — |
| Lab 18-06.i | six 2047s and ten 2048s, 14-bit | 8191 | — |

## Discussion

1. Why does the average-current model underestimate the error at 1 kHz but not at 100 kHz?
2. With 0.3 LSB of noise, why does averaging help at first and then stop?
3. Why does `adc_code_to_uv` use a 64-bit intermediate, and `decimate` add $2^{p-1}$ before shifting?
4. The PWM netlist starts its capacitor at the mean, 1.65 V. What would change if it started at 0 V, and how long would the simulation need?

## Answers

1. At 100 kHz the pin barely recovers between samples ($T \ll R_sC_{ext}$), so the S/H's charge removal acts like a steady current and the model fits. At 1 kHz the pin recovers almost completely between samples, and each sample sees the instantaneous charge-sharing step (0.109 mV) that the average model leaves out.
2. At first the noise moves samples across the nearest transition often enough that the average tracks the input. But with $\sigma$ = 0.3 LSB the noise rarely reaches the transition on the far side, so the average converges to a biased value (the input's expected code is not the input); more samples reduce the scatter around that biased value, not the bias.
3. $4095 \times 3300 \times 1000 \approx 1.35 \times 10^{10}$ exceeds $2^{32}$, so the product needs 64 bits. Adding half of the divisor before shifting turns truncation into rounding to nearest, removing a systematic −½ LSB bias that would otherwise appear in every averaged result.
4. Starting at 0 V the output would rise with $\tau$ = 4.096 ms towards 1.65 V; to measure ripple to 0.1% the start-up transient must decay below about 3 µV, roughly $\ln(1.65/3 \times 10^{-6}) \approx 13$ time constants, or 54 ms of simulation instead of 12.8 ms.

## Optional hardware

On a board, read a 10 kΩ/10 kΩ divider at the shortest and longest sampling times while alternating with a grounded channel, and compare the readings with the predictions of Part 1; then add 100 nF and sweep the sample rate (Part 2). Drive an LED with PWM at 100 Hz and 2 kHz and look for flicker on a phone camera; filter a PWM pin with 4.7 kΩ and 1 µF and measure the ripple with an oscilloscope on AC coupling.
