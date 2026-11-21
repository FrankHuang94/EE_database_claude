# Solutions 18-10 · Sensors: IMU, PPG, MEMS and Audio

Problems: [18-10 problem set](../problems/18-10-problems.md) · Chapter: [18-10](../chapters/18-10-sensors.md). Every number below is recomputed by [verify_18_10.py](../verify/verify_18_10.py).

---

## Solutions

### Solution 18-10.1

(a) $f_0 = \sqrt{k/m}/2\pi = \sqrt{2/5 \times 10^{-9}}/2\pi$ = **3183** Hz.

(b) $x = m \cdot 2g/k = 5 \times 10^{-9} \times 19.61/2$ = **49.0** nm (the same as $2g/\omega_0^2$).

(c) $2x/d = 2 \times 49.0\ \text{nm}/2\ \mu\text{m}$ = **4.90** %.

### Solution 18-10.2

(a) $150\ \mu\text{g} \times \sqrt{1.57 \times 80}$ = **1.68** mg.

(b) $1.68 \times 10^{-3}$ rad = **0.0963** °.

### Solution 18-10.3

(a) $10^{-38/20}$ V = **12.6** mV rms.

(b) 120 dB SPL is 26 dB above 94: $12.6\ \text{mV} \times 10^{26/20}$ = **0.251** V rms.

(c) $94 - 64$ = **30** dB(A) SPL.

### Solution 18-10.4

(a) From $a_n^2 = 4k_BT\omega_0/(mQ)$: $m = 4k_BT\omega_0/(Qa_n^2)$ with $a_n = 20 \times 10^{-6} \times 9.80665$ m/s²/√Hz and $\omega_0 = 2\pi \times 3000$: $m$ = **8.12** µg.

(b) Raise $Q$ (less gas damping: lower package pressure), at the cost of ringing and a need for closed-loop or electronic damping; or lower $\omega_0$, at the cost of bandwidth and of a softer, larger structure more prone to stiction and shock damage. Electronic noise must then be reduced too, or it will dominate.

### Solution 18-10.5

(a) $N = 0.3/60 = 0.005$ °/s/√Hz; after 600 s, $0.005\sqrt{600}$ = **0.122** °.

(b) $2\ °/\text{h} \times 1/6\ \text{h}$ = **0.333** °.

(c) The bias drift dominates over 10 minutes and keeps growing linearly, while the random walk grows only as $\sqrt t$. Long integrations need the bias re-estimated (during still periods, or by fusion), not just a quieter sensor.

### Solution 18-10.6

(a) Bias error $b\tau \le 0.1°$ gives $\tau \le 0.1/0.2$ = **0.5** s.

(b) $\tau = \alpha\Delta t/(1 - \alpha)$, so $\alpha = \tau/(\tau + \Delta t) = 0.5/0.505$ = **0.9901**.

(c) $\sqrt{(1 - \alpha)/(1 + \alpha)}$ = **0.0705**: accelerometer noise is cut about fourteenfold.

### Solution 18-10.7

(a) SNR scales as $m^2$: $20\log_{10}(1/0.3)$ = **10.5** dB lower, so $71.9 - 10.5$ = **61.5** dB.

(b) SNR scales with $I$, so 6 dB needs **4** times the photocurrent, and roughly four times the LED current (and LED power).

(c) **67.5** dB.

### Solution 18-10.8

(a) $1/8\ \text{s} = 0.125$ Hz = **7.5** beats per minute.

(b) **3.75** beats per minute, but a heart rate that changes within 16 s smears the peak.

(c) Resolution is set by the observation time: two frequencies closer than about $1/T$ cannot be separated, however finely the spectrum is sampled. Zero-padding only interpolates the same smoothed spectrum, which helps locate a single peak's centre more precisely (16-05).

### Solution 18-10.9

(a) Averaging 25 samples: $1.5/\sqrt{25}$ = **0.30** Pa, which is $0.30/12.01$ m = **2.5** cm.

(b) $100\ \text{Pa} \times 30\ \text{s}/10\,800\ \text{s}$ = **0.28** Pa.

(c) Yes: one floor is about 36 Pa, more than a hundred times the averaged noise and the weather change during the climb. Over hours, weather would masquerade as floors, so floor counting looks at pressure changes over tens of seconds, together with the accelerometer's evidence of climbing.

### Solution 18-10.10

(a) 32 samples at 25 Hz is a wake every **1.28** s. Each wake is $2\ \text{ms} \times 3\ \text{mA} = 6\ \mu\text{C}$, an average of **4.69** µA.

(b) $8 + 0.05 \times 900 + 25 + 30 + 4.69 + 2$ = **114.7** µA.

(c) $200\ \text{mAh}/114.7\ \mu\text{A}$ = **72.7** days.

(d) The gyroscope (45 µA, 39%) and the PPG chain (55 µA, 48%) dominate. Run the gyroscope only when motion demands it, perhaps triggered by the accelerometer, and reduce the PPG duty cycle (or LED current) when the wearer is still. A larger FIFO watermark would save less than 5 µA.

### Solution 18-10.11

(a) Write the filter with $u_n = \omega_n\Delta t = \theta_{g,n} - \theta_{g,n-1}$: $\hat\theta_n = \alpha\hat\theta_{n-1} + \alpha(\theta_{g,n} - \theta_{g,n-1}) + (1 - \alpha)\theta_{acc,n}$. Taking $z$-transforms, $\hat\Theta(1 - \alpha z^{-1}) = \alpha(1 - z^{-1})\Theta_g + (1 - \alpha)\Theta_{acc}$, which gives the two transfer functions. Their sum is $[(1 - \alpha) + \alpha - \alpha z^{-1}]/(1 - \alpha z^{-1}) = 1$: a tilt seen identically by both sensors passes unchanged, while each sensor's errors see only its own filter.

(b) $H_{acc}$'s impulse response is $h_k = (1 - \alpha)\alpha^k$, $k \ge 0$. White noise of variance $\sigma^2$ gives an output variance $\sigma^2\sum h_k^2 = \sigma^2(1 - \alpha)^2/(1 - \alpha^2) = \sigma^2(1 - \alpha)/(1 + \alpha)$, using the geometric series and $1 - \alpha^2 = (1 - \alpha)(1 + \alpha)$.

(c) $\tau = \alpha\Delta t/(1 - \alpha) = 1$ s with $\Delta t$ = 5 ms gives $\alpha = \tau/(\tau + \Delta t) = 1/1.005$ = **0.99502**, and the rms factor $\sqrt{(1 - \alpha)/(1 + \alpha)}$ = **0.0499**.

### Solution 18-10.12

(a) $v = 2\pi \times 25\,000 \times 4 \times 10^{-6}$ = 0.628 m/s; $a_c = 2 \times (10 \times \pi/180) \times 0.628$ = **0.219** m/s².

(b) $y = a_c/(\omega_s^2 - \omega_d^2) = 0.219/((2\pi)^2(27\,000^2 - 25\,000^2))$ = **0.0534** nm, about half an ångström.

(c) Matched, $y = Q_sa_c/\omega_s^2$ = **4.44** nm, 83 times more. The price is bandwidth (the sense resonance is only $f/Q$ = 50 Hz wide, which limits how fast the rate can change and makes the response depend on temperature), and the need to tune the modes electronically and hold them matched.

### Solution 18-10.13

(a) On the −½ slope $\sigma(\tau) = N_2/\sqrt\tau$, so $N_2 = 0.004$ °/√s at $\tau$ = 1 s, and ARW $= 60N_2$ = **0.24** °/√h.

(b) The flat level is about 0.664 times the bias instability: $0.0012/0.664$ = **0.00181** °/s, or **6.51** °/h.

(c) $N_2$ corresponds to the two-sided level, so the one-sided density is $\sqrt2N_2$ = **0.00566** °/s/√Hz.

(d) About 200 s, where the curve is lowest: shorter averages are dominated by white noise, which falls as $1/\sqrt\tau$, while longer ones see the bias itself wander (and temperature drift), so the estimate gets worse again. The bias instability is the floor any calibration by averaging can reach.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 18-10.1a | resonance | 3183 | Hz |
| 18-10.1b | deflection at 2 g | 49.0 | nm |
| 18-10.1c | relative capacitance change | 4.90 | % |
| 18-10.2a | rms noise | 1.68 | mg |
| 18-10.2b | tilt noise | 0.0963 | ° |
| 18-10.3a | output at 1 Pa | 12.6 | mV |
| 18-10.3b | output at 120 dB SPL | 0.251 | V |
| 18-10.3c | noise floor | 30 | dB(A) SPL |
| 18-10.4a | minimum proof mass | 8.12 | µg |
| 18-10.5a | angle noise after 10 min | 0.122 | ° |
| 18-10.5b | bias error after 10 min | 0.333 | ° |
| 18-10.6a | time constant | 0.5 | s |
| 18-10.6b | alpha | 0.9901 | — |
| 18-10.6c | noise reduction factor | 0.0705 | — |
| 18-10.7a | SNR loss | 10.5 | dB |
| 18-10.7b | SNR at 0.3% | 61.5 | dB |
| 18-10.7c | photocurrent factor for 6 dB | 4 | — |
| 18-10.7d | SNR with four times the current | 67.5 | dB |
| 18-10.8a | resolution, 8 s | 7.5 | bpm |
| 18-10.8b | resolution, 16 s | 3.75 | bpm |
| 18-10.9a | averaged noise | 0.30 | Pa |
| 18-10.9b | altitude noise | 2.5 | cm |
| 18-10.9c | weather change during the climb | 0.28 | Pa |
| 18-10.10a | wake interval | 1.28 | s |
| 18-10.10b | MCU wake cost | 4.69 | µA |
| 18-10.10c | total average current | 114.7 | µA |
| 18-10.10d | battery life | 72.7 | days |
| 18-10.11a | α for a 1 s time constant at 200 Hz | 0.99502 | — |
| 18-10.11b | rms noise factor | 0.0499 | — |
| 18-10.12a | Coriolis acceleration | 0.219 | m/s² |
| 18-10.12b | sense displacement, 2 kHz split | 0.0534 | nm |
| 18-10.12c | sense displacement, matched, Q = 500 | 4.44 | nm |
| 18-10.13a | angle random walk | 0.24 | °/√h |
| 18-10.13b | bias instability | 0.00181 | °/s |
| 18-10.13c | bias instability | 6.51 | °/h |
| 18-10.13d | one-sided rate noise density | 0.00566 | °/s/√Hz |
