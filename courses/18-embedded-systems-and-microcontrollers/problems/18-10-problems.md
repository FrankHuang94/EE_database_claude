# Problems 18-10 · Sensors: IMU, PPG, MEMS and Audio

Chapter: [18-10](../chapters/18-10-sensors.md) · Worked solutions: [18-10 solutions](../solutions/18-10-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** $g$ = 9.80665 m/s², $k_B$ = 1.380649 × 10⁻²³ J/K, $T$ = 300 K unless stated. Noise densities are white. A first-order filter with corner $f_c$ has noise bandwidth $1.57f_c$. Problems marked *(lab)* can be checked with `labs/18-10-lab/sensors.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 18-10.1 [A]

**Spring and mass.** A 5 µg proof mass hangs on flexures of 2 N/m with 2 µm electrode gaps. (a) What is its resonance? (b) How far does 2 g deflect it? (c) What relative differential capacitance change is that?

### Problem 18-10.2 [A]

**Data-rate noise.** An accelerometer has 150 µg/√Hz and a first-order filter at 80 Hz. (a) What is its rms noise? (b) What tilt noise near level?

### Problem 18-10.3 [A]

**An analog microphone.** A microphone's sensitivity is −38 dBV at 94 dB SPL and its SNR 64 dB(A). (a) What rms voltage does it give at 1 Pa? (b) At 120 dB SPL (if still linear)? (c) What is its noise floor in dB(A) SPL?

### Problem 18-10.4 [B]

**Designing for noise.** An accelerometer with a 3 kHz resonance and $Q$ = 1 must have a thermomechanical noise floor of at most 20 µg/√Hz. (a) What minimum proof mass does that need? (b) How else could the designer lower the floor, and at what cost?

### Problem 18-10.5 [B]

**Which gyroscope error dominates?** A gyroscope has an angle random walk of 0.3 °/√h and a residual bias of 2 °/h after calibration. Over a 10-minute integration: (a) what is the angle noise from the random walk? (b) What angle error does the residual bias produce? (c) Which dominates, and what does that imply for calibration?

### Problem 18-10.6 [B]

**Designing a complementary filter.** *(lab)* A tilt estimator runs at 200 Hz with a gyroscope whose uncorrected bias can be 0.2 °/s. (a) What time constant keeps the steady-state bias error at 0.1°? (b) What $\alpha$ is that? (c) By what factor does it then reduce the accelerometer's white noise?

### Problem 18-10.7 [B]

**PPG on a cold wrist.** *(lab)* A PPG front end measures 1 µA of DC photocurrent in a 10 Hz bandwidth. (a) The perfusion index falls from 1% to 0.3%. By how many dB does the shot-noise-limited SNR fall, and what is it? (b) How much must the photocurrent (and roughly the LED current) rise to win back 6 dB? (c) What is the SNR then?

### Problem 18-10.8 [B]

**Heart-rate resolution.** A heart rate is estimated from the spectrum of an 8 s PPG window. (a) What is the frequency resolution in beats per minute? (b) What with a 16 s window? (c) Why does zero-padding the FFT not improve the true resolution, and what does it do?

### Problem 18-10.9 [B]

**Counting floors.** A barometer gives 1.5 Pa rms noise per sample at 25 Hz. (a) What is the noise of 1 s averages, in pascals and in centimetres of altitude (at −12.01 Pa/m)? (b) Weather changes pressure by about 100 Pa in 3 hours. How much does that change pressure during a 30 s climb? (c) Can the device detect one 3 m floor reliably?

### Problem 18-10.10 [C]

**A wristband's sensor budget.** A wristband runs an accelerometer continuously at 8 µA, turns its gyroscope (900 µA) on 5% of the time, pulses its PPG LED as in Example 18-10.5(c) (25 µA) with a hypothetical next-generation AFE drawing 30 µA (the AFE4404 of 18-10 §9 draws about 300 µA in its power-down mode), and wakes its MCU when the accelerometer's FIFO holds 32 samples at 25 Hz, each wake costing 2 ms at 3 mA. The MCU otherwise sleeps at 2 µA. (a) How often does the MCU wake, and what does it cost on average? (b) What is the total average current? (c) How long does a 200 mAh battery last? (d) Which two changes would you make first?

### Problem 18-10.11 [B]

**The complementary filter's algebra.** (a) Show that the filter of §3.3 acts on the accelerometer's tilt through $H_{acc}(z) = (1 - \alpha)/(1 - \alpha z^{-1})$ and on the gyroscope's integrated angle through $H_{gyro}(z) = \alpha(1 - z^{-1})/(1 - \alpha z^{-1})$, and that they sum to 1. (b) Derive the white-noise variance factor $(1 - \alpha)/(1 + \alpha)$. (c) At 200 Hz, what α gives a 1 s time constant, and what fraction of the accelerometer's white-noise rms passes?

### Problem 18-10.12 [B]

**Sense-mode motion.** A gyroscope drives its proof mass at 25 kHz with 4 µm amplitude. (a) What is the Coriolis acceleration at 10 °/s? (b) What is the sense displacement with the sense mode at 27 kHz (Q large)? (c) With the modes matched and a sense Q of 500, what is it, and what does matching cost?

### Problem 18-10.13 [B]

**Reading an Allan plot.** A stationary gyroscope's Allan deviation falls with slope −½ through 0.004 °/s at $\tau$ = 1 s and flattens to a minimum of 0.0012 °/s near $\tau$ = 200 s. (a) What is its angle random walk in °/√h? (b) What is its bias instability, in °/s and °/h? (c) What one-sided rate noise density does the ARW correspond to? (d) What is the best averaging time for estimating its bias, and why does averaging longer not help?

---

## Objective coverage

| Learning objective (chapter 18-10) | Problems |
|---|---|
| 1. Accelerometer physics and noise floor | 1, 4 |
| 2. Noise density, bandwidth and tilt | 2, 9 |
| 3. Gyroscopes and integration | 5, 12, 13 |
| 4. Complementary filtering | 6, 11 |
| 5. PPG signal, noise and power | 7, 8, 10 |
| 6. Microphone and barometer specifications | 3, 9 |
