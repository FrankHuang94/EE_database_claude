# Solutions 10-10 · Op-Amp Application Circuits

Problems: [10-10 problems](../problems/10-10-problems.md) · Chapter: [10-10](../chapters/10-10-op-amp-application-circuits.md). Every number below is recomputed by [verify_10_10.py](../verify/verify_10_10.py).

---

## Solutions

### Solution 10-10.1

$(1 + 2)/(4 \times 0.01)$ = **75**, or **37.5** dB. Solving the circuit with the resistors at their worst-case corners gives a common-mode gain of 0.0263, so 2 V of common mode produces **52.6** mV of output error (the first-order estimate $2 \times 2/75$ = 53.3 mV is 1.3% high, because at 1% tolerance the second-order terms are no longer negligible).

### Solution 10-10.2

$R_G = 100\text{ kΩ}/(G - 1)$: **11.11** kΩ for $G$ = 10 and **100.1** Ω for $G$ = 1000.

### Solution 10-10.3

$V_{TH+} = 1.65(1 + 10/330)$ = **1.7** V; hysteresis $3.3 \times 10/330$ = **0.1** V; $V_{TH-}$ = **1.6** V.

### Solution 10-10.4

KCL at the + input, $(V_{ref} - v_+)/R_1 + (v_o - v_+)/R_2 = 0$, gives

$$
v_+ = \frac{V_{ref}R_2 + v_oR_1}{R_1 + R_2} = 2.5 \times \frac{240}{250} + v_o\,\frac{10}{250} = 2.4\text{ V} + 0.04\,v_o .
$$

With $v_o$ = 5 V the threshold is **2.6** V; with $v_o$ = 0 it is **2.4** V; the hysteresis is **0.2** V. The comparator inverts: while the input is low, the output is high and the threshold is 2.6 V, so a rising input switches the output low at 2.6 V, and a falling input switches it back at 2.4 V.

### Solution 10-10.5

(a) The capacitor current is $V_{OS}/R + I_B$ = 5 nA + 10 nA = 15 nA, so the output ramps at 15 nA/100 nF = **0.15** V/s.

(b) The offset appears as $V_{OS}(1 + R_F/R) + I_BR_F$ = 50.5 mV + 100 mV = **150.5** mV; the corner is $1/(2\pi R_FC)$ = **0.159** Hz. (A resistor $R \parallel R_F$ in the + input would cancel most of the bias-current term.)

### Solution 10-10.6

Dead time $2 \times 0.7/0.5$ = **2.8** µs. The input reached during the dead time is $V_p\sin(2\pi f\Delta t)$: **17.6** mV at 1 kHz and **345** mV at 20 kHz (the linear estimate $2\pi fV_p\Delta t$ gives 352 mV, 2% high, because the sine is already curving). A slow op-amp is unusable as a precision rectifier across the audio band.

### Solution 10-10.7

(a) τ = 10 kΩ × 15 pF = **150** ns; 10–90% rise $\tau\ln 9$ = **329.6** ns.

(b) $R = 50\text{ ns}/(15\text{ pF} \times \ln 9)$ = **1.517** kΩ, drawing $3.3/1.517$ = **2.175** mA when the output is low. Open-drain outputs trade speed against static current; push-pull outputs avoid the trade.

### Solution 10-10.8

$f_0 = \sqrt{50\text{ MHz}/(2\pi \times 1\text{ MΩ} \times 5\text{ pF})}$ = **1.262** MHz and $Q = \sqrt{2\pi \times 50\text{ MHz} \times 1\text{ MΩ} \times 5\text{ pF}}$ = **39.6**: a resonance close to oscillation.

### Solution 10-10.9

(a) Solving $Q(C_F) = 1/\sqrt2$ from §3.5: $C_F$ = **0.1784** pF, a value small enough that the board's stray capacitance across $R_F$ may already supply it.

(b) $f_0$ = **1.240** MHz, which is also the −3 dB bandwidth, since the transimpedance is then a Butterworth low-pass.

(c) The approximation gives **0.1816** pF, within 2%: here $\omega_tR_FC_F$ ≈ 56 is much greater than 1.

### Solution 10-10.10

At 60 Hz, δ = $2\pi \times 60 \times 10^4 \times 10^{-12}$ = 3.77 × 10⁻⁶ and CMRR = 2/δ = **5.3 × 10⁵**, or **114.5** dB. At 50 kHz, δ = 3.14 × 10⁻³ and CMRR = **637**, or **56.1** dB. A picofarad of layout asymmetry destroys high-frequency CMRR; that is why INA data sheets show CMRR falling with frequency and why layout symmetry matters.

### Solution 10-10.11

$25 + 75/1000$ = **25.075** µV, **25.075** mV at the output, **2.51**% of full scale. High-gain bridge readings need calibration or a lower-offset front end.

### Solution 10-10.12

$360° \times 1\text{ MHz} \times 47\text{ ns}$ = **16.9°**. A known, constant delay can be subtracted in timing logic, or the detector can compare against a slightly shifted threshold; what cannot be subtracted is the delay's variation with overdrive and temperature.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 10-10.1a | worst-case CMRR | 75 | — |
| 10-10.1b | worst-case CMRR | 37.5 | dB |
| 10-10.1c | output error for 2 V | 52.6 | mV |
| 10-10.2a | R_G for G = 10 | 11.11 | kΩ |
| 10-10.2b | R_G for G = 1000 | 100.1 | Ω |
| 10-10.3a | upper threshold | 1.7 | V |
| 10-10.3b | hysteresis | 0.1 | V |
| 10-10.3c | lower threshold | 1.6 | V |
| 10-10.4a | threshold with output high | 2.6 | V |
| 10-10.4b | threshold with output low | 2.4 | V |
| 10-10.4c | hysteresis | 0.2 | V |
| 10-10.5a | ramp rate | 0.15 | V/s |
| 10-10.5b | output offset with leak | 150.5 | mV |
| 10-10.5c | lower corner | 0.159 | Hz |
| 10-10.6a | dead time | 2.8 | µs |
| 10-10.6b | missed voltage at 1 kHz | 17.6 | mV |
| 10-10.6c | missed voltage at 20 kHz | 345 | mV |
| 10-10.7a | time constant | 150 | ns |
| 10-10.7b | 10–90% rise time | 329.6 | ns |
| 10-10.7c | pull-up for 50 ns | 1.517 | kΩ |
| 10-10.7d | current when low | 2.175 | mA |
| 10-10.8a | f_0 | 1.262 | MHz |
| 10-10.8b | Q | 39.6 | — |
| 10-10.9a | C_F | 0.1784 | pF |
| 10-10.9b | f_0 and bandwidth | 1.240 | MHz |
| 10-10.9c | approximate C_F | 0.1816 | pF |
| 10-10.10a | CMRR at 60 Hz | 5.3e5 | — |
| 10-10.10b | CMRR at 60 Hz | 114.5 | dB |
| 10-10.10c | CMRR at 50 kHz | 637 | — |
| 10-10.10d | CMRR at 50 kHz | 56.1 | dB |
| 10-10.11a | input-referred offset | 25.075 | µV |
| 10-10.11b | output offset | 25.075 | mV |
| 10-10.11c | fraction of full scale | 2.51 | % |
| 10-10.12a | phase error | 16.9 | ° |
