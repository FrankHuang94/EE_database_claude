# Lab 18-10 · Noise Floors, Sensor Fusion and a Synthetic PPG

Chapter: [18-10 · Sensors: IMU, PPG, MEMS and Audio](../../chapters/18-10-sensors.md)

## Objective

- Compute a MEMS accelerometer's deflection, capacitance change and thermomechanical noise floor, and see how mass, resonance and damping move it.
- Fuse a noisy accelerometer and a biased gyroscope with a complementary filter, and find the best blend.
- Recover a heart rate from a synthetic PPG with shot noise and a motion artefact, and see when it fails.
- Turn barometer noise into altitude noise and detect a floor change.

## Background

Deflection is $a/\omega_0^2$ and the thermomechanical floor $\sqrt{4k_BT\omega_0/(mQ)}$ (§3.1). A complementary filter with $\tau = \alpha\Delta t/(1 - \alpha)$ leaves a bias error $b\tau$ and passes $\sqrt{(1 - \alpha)/(1 + \alpha)}$ of the accelerometer's white noise (§3.3). A PPG's shot-noise-limited SNR is $m^2I/(4qB)$ (§3.4). Pressure falls by about 12 Pa per metre near sea level (§3.6).

## Files

- `sensors.py`: `resonance_hz`, `static_deflection`, `capacitance_change`, `brownian_noise_density`, `rms_noise`, `coriolis_acceleration`, `angle_random_walk_deg_per_rt_hour`, `angle_drift_from_bias`, `angle_noise_after`, `tilt_deg`, `complementary_time_constant`, `simulate_fusion`, `beer_lambert`, `perfusion_index`, `shot_noise_snr_db`, `heart_rate_from_signal`, `spl_db`, `pressure_from_spl`, `full_scale_spl`, `noise_floor_spl`, `altitude_m`, `pressure_gradient_pa_per_m`.
- `18-10-sensors-lab.ipynb`: the guided notebook.

## Procedure

1. **Noise floor.** For Example 18-10.1's structure, predict the floor when the mass doubles and when $Q$ rises from 2 to 200; compute.
2. **Fusion.** Predict the fused rms error for $\alpha$ = 0.9, 0.98 and 0.998 with Example 18-10.4's noise and bias; run `simulate_fusion` and scan $\alpha$ for the minimum.
3. **Heart rate.** Build 8 s of PPG at 50 Hz: a DC photocurrent of 1 µA with a 1% pulse at 72 beats per minute, shot noise in a 25 Hz bandwidth, and a 1.5 Hz motion artefact of increasing size. Predict the artefact size at which `heart_rate_from_signal` locks onto the artefact; run.
4. **Altitude.** Simulate 60 s of pressure at 25 Hz with 1.5 Pa rms noise and a 3 m climb between 20 and 40 s; convert to altitude with 1 s averages.

## Expected results

- Part 1: doubling the mass lowers the floor by $\sqrt2$ (to 23.3 µg/√Hz); raising $Q$ from 2 to 200 lowers it tenfold (to 3.29 µg/√Hz).
- Part 2: about 0.26°, 0.29° and 2.5° rms for $\alpha$ = 0.9, 0.98 and 0.998; the minimum, about 0.21°, lies near $\alpha$ = 0.96, where accelerometer noise and bias error balance.
- Part 3: the 72 beats-per-minute peak is found while the artefact is smaller than the pulse; once the artefact's amplitude exceeds the pulse's, the estimate jumps to 90 beats per minute (1.5 Hz).
- Part 4: the climb appears as a 3 m step in the 1 s averages, with about 2.5 cm of noise.

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 18-10.a | floor with double mass | 23.3 | µg/√Hz |
| Lab 18-10.b | floor with Q = 200 | 3.29 | µg/√Hz |
| Lab 18-10.c | heart rate estimated with a small artefact | 72 | bpm |
| Lab 18-10.d | rate locked onto by a large artefact | 90 | bpm |

## Discussion

1. Why does the fused error grow again for $\alpha$ very close to 1?
2. Why does the heart-rate estimate fail abruptly rather than gradually as the artefact grows?
3. Why do wearables combine PPG with the accelerometer?

## Answers

1. The time constant grows towards infinity, so the bias error $b\tau$ grows without limit while the extra noise reduction is small; at $\alpha$ = 0.998, $\tau$ is about 5 s and the bias error 2.5°.
2. The estimator picks the largest spectral peak. While the pulse's peak is larger it wins regardless of the artefact; as soon as the artefact's peak is larger, the answer jumps to the artefact's frequency. Peak picking has no notion of "probably wrong".
3. The accelerometer measures the motion that causes artefacts, so its frequency content can be removed from, or used to discount peaks in, the PPG spectrum (adaptive filtering), and it tells the algorithm when the signal is unreliable.

## Optional hardware

Log a development board's IMU at rest for an hour; compute the gyroscope's bias drift and angle random walk from the Allan deviation, and compare with its data sheet. Then tilt the board slowly and quickly and compare accelerometer-only, gyroscope-only and fused tilt.
