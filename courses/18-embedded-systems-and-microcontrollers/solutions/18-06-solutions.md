# Solutions 18-06 · Analog Interfaces: ADC, DAC and PWM

Problems: [18-06 problem set](../problems/18-06-problems.md) · Chapter: [18-06](../chapters/18-06-adc-dac-pwm.md). Every number below is recomputed by [verify_18_06.py](../verify/verify_18_06.py).

---

## Solutions

### Solution 18-06.1

(a) $2.5/1024$ = **2.441** mV.

(b) $1.8/2.441\ \text{mV} = 737.3$, which rounds to code **737**. Code 512 is $512 \times 2.441\ \text{mV}$ = **1.25** V, mid-scale.

(c) Half an LSB, **1.221** mV. SQNR $= 6.02 \times 10 + 1.76$ = **61.97** dB.

### Solution 18-06.2

(a) $(54.0 - 1.76)/6.02$ = **8.68** bits, the "8.7 ENOB" of the data sheet.

(b) $(61.5 - 1.76)/6.02$ = **9.92** bits.

(c) SNR excludes harmonic distortion; SINAD includes it. A 7.5 dB gap means distortion, not noise, dominates the errors: a deterministic nonlinearity of the transfer function. That matches the RP2040's erratum, which attributes the shortfall to DNL spikes at four codes ([R-307]). Averaging cannot remove such errors (§3.4).

### Solution 18-06.3

(a) $0.005 \times 4096$ = **20.5** LSB at full scale.

(b) $2 + 3 + 2 + 20.5$ = **27.5** LSB, $27.5 \times 0.806\ \text{mV}$ = **22.1** mV.

(c) $\sqrt{2^2 + 3^2 + 2^2 + 20.5^2}$ = **20.9** LSB (**16.8** mV). The reference dominates: the converter's own errors add less than half an LSB to it in quadrature.

(d) Measuring two known inputs (near zero and near full scale) and correcting by a straight line removes offset and gain error, and with them the reference's tolerance at the calibration temperature. INL, noise and drift after calibration remain.

### Solution 18-06.4

(a) $14/(40\ \text{MHz})$ = **350** ns.

(b) $1/(62.5 + 350\ \text{ns})$ = **2.42** Msps.

(c) $1/(312.2 + 350\ \text{ns})$ = **1.51** Msps. The source's impedance, not the converter, costs 38% of the throughput.

### Solution 18-06.5

(a) $4.2/(2\ \text{MΩ})$ = **2.1** µA, permanently.

(b) The Thévenin resistance is 500 kΩ: $t_s \ge 500.5\ \text{kΩ} \times 3.3\ \text{pF} \times 9.01$ = **14.9** µs, far beyond most sampling-time settings.

(c) $50\ \text{nA} \times 500\ \text{kΩ}$ = **25** mV = **31.0** LSB, **1.19** % of the 2.1 V reading.

(d) $500\ \text{kΩ} \times 100\ \text{nF}$ = **50** ms. At 10 samples a second the S/H's average-current error is only $2.1 \times 500\ \text{kΩ} \times 10\ \text{Hz} \times 3.3\ \text{pF}$ ≈ **35** µV. Because the pin recovers largely between samples ($T$ = 100 ms = 2τ), the charge-sharing step (69 µV) adds most of an exact error of **80** µV, about 0.1 LSB.

(e) **The leakage** (25 mV) dwarfs everything else. Lower the divider's impedance and switch it (a MOSFET that connects the divider only while measuring, as in Problem 18-06.11), buffer it, or calibrate at a known voltage if the leakage is stable. A 100 kΩ/100 kΩ switched divider reduces the leakage error tenfold and draws current only during the measurement.

### Solution 18-06.6

(a) $(3.3 - 0.5) \times 3.3\ \text{pF}/47.003\ \text{nF}$ = **0.197** mV.

(b) $g = R_sfC_{sh} = 4.7\ \text{kΩ} \times 200\ \text{kHz} \times 3.3\ \text{pF} = 0.003102$, so the average-current estimate is $2.8 \times g/(1 + g)$ = **8.66** mV. The recursion of §3.2 with $V_0$ = 3.3 V gives **8.76** mV, or **10.9** LSB, and the reading is **high**: the S/H arrives charged to 3.3 V and pulls the pin up.

(c) At 50 kHz: **2.27** mV.

(d) **No, not here.** The first conversion moves the S/H from 3.3 V to the pin's voltage; the second starts there and moves almost no charge. The charge drawn per scan, and therefore the DC error, is unchanged. **Without** the external capacitor it does help: the problem there is settling, and the second conversion starts from the first's nearly settled value, so its error is that much smaller.

### Solution 18-06.7

(a) The factory value fixes the reference's actual voltage: $V_{BG} = 3.000 \times 1652/4096$ = **1.210** V. Then $V_{DD} = 4096\,V_{BG}/1502 = 3.000 \times 1652/1502$ = **3.300** V.

(b) $3.2996 \times 2000/4096$ = **1.611** V.

(c) $3.2996/1502$ ≈ **2.20** mV per code.

(d) The reference's initial tolerance, whatever it is, is measured out in production: the formula uses the ratio of today's code to the factory code, so only the reference's drift since calibration (with temperature and age) and the conversion noise remain.

### Solution 18-06.8

(a) 2 bits need $4^2$ = **16** samples: $1\ \text{Msps}/16$ = **62.5** ksps.

(b) $16 \times 4095$ = **65 520** fits in **16** bits; $256 \times 4095$ = **1 048 320** needs **20** bits.

(c) Independent noises add in power: $\sqrt{0.5^2 - 0.1^2}$ = **0.490** LSB rms.

(d) Averaging improves resolution, not accuracy. Offset, gain error, INL and the reference are unchanged, so a 14-bit result can still be off by many 12-bit LSBs (compare Problem 18-06.3's 20.9 LSB budget).

### Solution 18-06.9

(a) $\operatorname{sinc}(0.05)$ = **0.9959**, **−0.036** dB: negligible.

(b) At $f_s - f$ = **950** kHz, with relative level $\operatorname{sinc}(0.95)/\operatorname{sinc}(0.05)$. Because $\sin(0.95\pi) = \sin(0.05\pi)$, this is exactly $0.05/0.95$ = **0.0526**, or **−25.6** dB.

(c) $74.0 - 25.6$ = **48.4** dB more. Second order: $40\log_{10}9.5$ = **39.1** dB, not enough; third order: $60\log_{10}9.5$ = **58.7** dB, enough.

(d) The sine's steepest slope is $\pi f V_{pp} = \pi \times 50\ \text{kHz} \times 3.3$ V = **0.518** V/µs, a tenth of the DAC's 5.5 V/µs.

(e) $10^6 \times 2$ = **2 000 000** bytes/s: 2 MB/s of DMA traffic (18-04).

### Solution 18-06.10

(a) $80\ \text{MHz}/4096$ = **19.53** kHz, $T$ = **51.2** µs.

(b) $\tau \ge 4096 \times 51.2\ \mu\text{s}/4$ = **52.4** ms, so $f_c$ = **3.04** Hz and settling $\tau\ln 2^{13}$ = **472** ms: almost half a second to settle after a step.

(c) $\tau$ is four times smaller, so $f_c$ = **12.1** Hz.

(d) A single stage attenuates the PWM fundamental only by $f_c/f_{PWM}$, so meeting the ripple needs $f_c$ far below $f_{PWM}$. Two stages attenuate by about $(f_c/f_{PWM})^2$, so the same ripple allows each stage's corner to sit at roughly the geometric mean of the single-stage corner and $f_{PWM}$, which is a much higher bandwidth. The buffer stops the second stage from loading the first. Alternatively, use fewer PWM bits with dithering of the duty cycle, or a real DAC.

### Solution 18-06.11

(a) $3.3/20\ \text{kΩ}$ = **165** µA, which would dominate a wearable's standby budget (18-09).

(b) The pin sees the Thévenin resistance $(10\,050 \parallel 10\,000)$ Ω = 5.01 kΩ, so $\tau$ = **0.501** ms, and 12-bit settling from 0 V takes $9.01\tau$ = **4.52** ms.

(c) With the steady divider current, about 164.6 µA, flowing for the whole 4.52 ms, the estimate is $0.743\ \mu\text{C}$, plus $100\ \text{nF} \times 1.646\ \text{V} = 0.165\ \mu\text{C}$ to charge the capacitor: **0.908** µC. That is an upper bound, because the thermistor's current is smaller while the pin is still rising. Integrating exactly gives **0.825** µC, so at one measurement per second the average is **0.83** µA, about 200 times less than the permanent divider.

(d) The pin settles to $3.3 \times 10\,000/20\,050$ V instead of 1.65 V, so the code is $4096 \times 10\,000/20\,050 = 2042.9$ instead of 2048: **5.1** codes low, or **0.11** K at 45.5 codes/K.

(e) Correct for it in firmware (add the 50 Ω to $R_f$ in the conversion formula; it varies with the pin's drive and temperature, so calibrate it), use a high-drive pin with lower output resistance, or measure the GPIO's high level on a second ADC channel and compute the ratio against it. The power saving is worth far more than the 0.1 K for a skin-temperature reading.

### Solution 18-06.12

(a) $t_s = (R_s + 500\ \Omega) \times 3.3\ \text{pF} \times 9.01$, but at least 62.5 ns: **62.5** ns (50 Ω), **164** ns (5 kΩ), **610** ns (20 kΩ), **2988** ns (100 kΩ).

(b) $\sum t_s + 4 \times 350\ \text{ns}$ = 5.224 µs, a scan rate of **191** kHz.

(c) $4 \times 2988 + 1400$ ns = 13.35 µs: **74.9** kHz. One slow channel slows the whole scan.

(d) The scan shrinks to 2.298 µs, **435** kHz. Now $g = 100\ \text{kΩ} \times 435\ \text{kHz} \times 3.3\ \text{pF} = 0.144$, so the 2.0 V channel is pulled toward the 1.0 V channel by about $1.0 \times 0.144/1.144$ = **126** mV, or **156** LSB. The exact recursion agrees.

(e) Buffer the 100 kΩ source with an op-amp (the robust fix), or scan it in a separate, slow sequence (at 1 kHz its error falls to about 0.35 mV), or keep its long sampling time and accept the 191 kHz scan. An external capacitor only works when the channel's own sample rate is low compared with $1/(R_sC_{sh})$.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 18-06.1a | LSB | 2.441 | mV |
| 18-06.1b | code for 1.8 V | 737 | — |
| 18-06.1c | voltage of code 512 | 1.25 | V |
| 18-06.1d | largest quantization error | 1.221 | mV |
| 18-06.1e | SQNR, 10 bits | 61.97 | dB |
| 18-06.2a | ENOB from SINAD | 8.68 | bits |
| 18-06.2b | ENOB from SNR | 9.92 | bits |
| 18-06.3a | reference tolerance at full scale | 20.5 | LSB |
| 18-06.3b | worst-case total | 27.5 | LSB |
| 18-06.3c | worst-case total | 22.1 | mV |
| 18-06.3d | root-sum-square total | 20.9 | LSB |
| 18-06.3e | root-sum-square total | 16.8 | mV |
| 18-06.4a | conversion phase | 350 | ns |
| 18-06.4b | rate at 62.5 ns sampling | 2.42 | Msps |
| 18-06.4c | rate at 312 ns sampling | 1.51 | Msps |
| 18-06.5a | divider current | 2.1 | µA |
| 18-06.5b | sampling time without a capacitor | 14.9 | µs |
| 18-06.5c | leakage error | 25 | mV |
| 18-06.5d | leakage error | 31.0 | LSB |
| 18-06.5e | leakage error | 1.19 | % |
| 18-06.5f | recovery time constant | 50 | ms |
| 18-06.5g | S/H error, average-current model | 35 | µV |
| 18-06.5h | S/H error, exact | 80 | µV |
| 18-06.6a | charge-sharing step | 0.197 | mV |
| 18-06.6b | error, average-current model | 8.66 | mV |
| 18-06.6c | error, exact | 8.76 | mV |
| 18-06.6d | error in LSB | 10.9 | LSB |
| 18-06.6e | error at 50 kHz | 2.27 | mV |
| 18-06.7a | reference's actual voltage | 1.210 | V |
| 18-06.7b | V_DD | 3.300 | V |
| 18-06.7c | other channel | 1.611 | V |
| 18-06.7d | V_DD change per code | 2.20 | mV |
| 18-06.8a | samples for 14 bits | 16 | — |
| 18-06.8b | output rate | 62.5 | ksps |
| 18-06.8c | largest sum of 16 samples | 65520 | — |
| 18-06.8d | its word length | 16 | bits |
| 18-06.8e | largest sum of 256 samples | 1048320 | — |
| 18-06.8f | its word length | 20 | bits |
| 18-06.8g | dither to add | 0.490 | LSB |
| 18-06.9a | ZOH gain at 50 kHz | 0.9959 | — |
| 18-06.9b | ZOH droop at 50 kHz | −0.036 | dB |
| 18-06.9c | first image frequency | 950 | kHz |
| 18-06.9d | image relative to tone | 0.0526 | — |
| 18-06.9e | image relative to tone | −25.6 | dB |
| 18-06.9f | further attenuation needed | 48.4 | dB |
| 18-06.9g | second-order attenuation at 950 kHz | 39.1 | dB |
| 18-06.9h | third-order attenuation at 950 kHz | 58.7 | dB |
| 18-06.9i | sine's slew rate | 0.518 | V/µs |
| 18-06.9j | DMA traffic | 2000000 | bytes/s |
| 18-06.10a | PWM frequency | 19.53 | kHz |
| 18-06.10b | PWM period | 51.2 | µs |
| 18-06.10c | time constant | 52.4 | ms |
| 18-06.10d | bandwidth | 3.04 | Hz |
| 18-06.10e | settling time | 472 | ms |
| 18-06.10f | bandwidth with 4 LSB ripple | 12.1 | Hz |
| 18-06.11a | permanent divider current | 165 | µA |
| 18-06.11b | pin time constant | 0.501 | ms |
| 18-06.11c | settling time | 4.52 | ms |
| 18-06.11d | charge per measurement, estimate | 0.908 | µC |
| 18-06.11e | charge per measurement, exact | 0.825 | µC |
| 18-06.11f | average current | 0.83 | µA |
| 18-06.11g | codes lost to the GPIO drop | 5.1 | codes |
| 18-06.11h | temperature error | 0.11 | K |
| 18-06.12a | sampling time, 50 Ω | 62.5 | ns |
| 18-06.12b | sampling time, 5 kΩ | 164 | ns |
| 18-06.12c | sampling time, 20 kΩ | 610 | ns |
| 18-06.12d | sampling time, 100 kΩ | 2988 | ns |
| 18-06.12e | scan rate, own sampling times | 191 | kHz |
| 18-06.12f | scan rate, shared sampling time | 74.9 | kHz |
| 18-06.12g | scan rate with the capacitor | 435 | kHz |
| 18-06.12h | error with the capacitor | 126 | mV |
| 18-06.12i | error with the capacitor | 156 | LSB |
