# Solutions 10-09 · Real Op-Amps: Non-Idealities

Problems: [10-09 problems](../problems/10-09-problems.md) · Chapter: [10-09](../chapters/10-09-real-op-amps-nonidealities.md). Every number below is recomputed by [verify_10_09.py](../verify/verify_10_09.py).

---

## Solutions

### Solution 10-09.1

(a) Noise gain 5, bandwidth **1.0** MHz. (b) Noise gain 4, **1.25** MHz. (c) Noise gain 1, **5** MHz. The inverting stage is slower than the non-inverting one of the same gain magnitude.

### Solution 10-09.2

(a) $10^{90/20}$ = **31623**, so 1 V of common-mode change appears as **31.6** µV at the input. (b) $10^{-100/20}$ V/V = **10** µV/V.

### Solution 10-09.3

(a) $10^6/(2\pi \times 5)$ = **31.83** kHz. (b) $2\pi \times 20\text{ kHz} \times 10\text{ V}$ = **1.257** V/µs.

### Solution 10-09.4

(a) $A$ = 10⁵: $10^5/(1 + 10^5/50)$ = **49.975**, an error of **0.0500**%.

(b) $f_{-3dB}$ = 1 MHz/50 = **20** kHz. At 10 kHz, $x$ = 0.5: magnitude low by **−10.56**%, phase lag **26.6**°. The DC error is negligible next to the in-band error at a frequency only half the bandwidth.

### Solution 10-09.5

(a) $\tau = 1/(2\pi \times 5\text{ MHz})$ = **31.83** ns; steps up to $\text{SR}\cdot\tau$ = **63.7** mV stay linear.

(b) The output ramps at 2 V/µs until the remaining error equals 63.7 mV: $(4 - 0.0637)/2$ = **1.968** µs. Then it decays exponentially from 63.7 mV to 4 mV: $\tau\ln(63.7/4)$ = **88.1** ns. Total **2.056** µs.

(c) Linear 0.1% settling: $\tau\ln 1000$ = **219.9** ns. Slewing makes the large step almost ten times slower.

### Solution 10-09.6

(a) Bias current through $R_2$: $250\text{ nA} \times 100\text{ kΩ}$ = **25** mV; offset × noise gain 11: **5.5** mV; worst case **30.5** mV.

(b) With the compensating resistor, the bias-current term becomes $I_{OS}R_2$ = **17.5** mV, and the worst case **23** mV. The rule assumes $I_{OS} \ll I_B$; for this part the *maximum* offset current is 70% of the maximum bias current, so compensation cuts only 30% in the worst case (the typical values, 25 nA against 60 nA, do much better).

### Solution 10-09.7

(a) $0.53 \times 100$ = **53** µV.

(b) The guarantees allow the 25 °C offset to be anywhere within ±1.6 mV and the 125 °C offset anywhere within ±2 mV, so the change can be as large as **3.6** mV. A typical drift is not a guarantee; the guaranteed change is 68 times larger.

### Solution 10-09.8

Two decades above 100 Hz, PSRR = **40** dB, and 100 mV of ripple appears as **1.0** mV at the input. Supply filtering matters most at the regulator's switching frequency.

### Solution 10-09.9

(a) **2.5** mA, within the 5 mA limit. (b) **0.5** V peak (5 mA × 100 Ω). (c) $\omega CV_p = 2\pi \times 10\text{ kHz} \times 10\text{ nF} \times 2\text{ V}$ = **1.257** mA, feasible for current, but such a capacitive load would threaten stability (Course 12).

### Solution 10-09.10

(a) Settling time = slewing time + $\tau\ln(\text{boundary}/\text{tolerance})$, with boundary $\text{SR}\cdot\tau$ and tolerance 0.2 mV. Solving for 1 µs: GBW = **2.025** MHz.

(b) τ = **78.61** ns; boundary **314.5** mV; slewing **0.4214** µs; exponential **578.6** ns.

(c) Linear only: $\ln(10^4)/(2\pi \times 1\ \mu\text{s})$ = **1.466** MHz. The slew limit costs 38% more bandwidth.

### Solution 10-09.11

(a) 0.1 °C × 50 µV/°C = **5** µV over 70 °C: a drift of **0.0714** µV/°C.

(b) Only the OPA333 (0.05 µV/°C max [2]). The OPA1611's 4 µV/°C max [3] and the TLV9062's typical 0.53 µV/°C [1] both fail by large factors.

### Solution 10-09.12

$(V+) - 1.4\text{ V}$ = **0.4** V, only **22.2**% of the supply. An inverting configuration holds both inputs at a fixed reference voltage (say 0.2 V), inside the high-CMRR region, while the output swings rail to rail.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 10-09.1a | bandwidth, gain −4 | 1.0 | MHz |
| 10-09.1b | bandwidth, gain +4 | 1.25 | MHz |
| 10-09.1c | bandwidth, follower | 5 | MHz |
| 10-09.2a | CMRR ratio | 31623 | — |
| 10-09.2b | input error per volt | 31.6 | µV |
| 10-09.2c | PSRR | 10 | µV/V |
| 10-09.3a | full-power bandwidth | 31.83 | kHz |
| 10-09.3b | required slew rate | 1.257 | V/µs |
| 10-09.4a | DC gain | 49.975 | — |
| 10-09.4b | DC error | 0.0500 | % |
| 10-09.4c | closed-loop bandwidth | 20 | kHz |
| 10-09.4d | magnitude error at 10 kHz | -10.56 | % |
| 10-09.4e | phase lag at 10 kHz | 26.6 | ° |
| 10-09.5a | τ | 31.83 | ns |
| 10-09.5b | largest linear step | 63.7 | mV |
| 10-09.5c | slewing time | 1.968 | µs |
| 10-09.5d | exponential time | 88.1 | ns |
| 10-09.5e | total | 2.056 | µs |
| 10-09.5f | linear-only settling | 219.9 | ns |
| 10-09.6a | bias-current term | 25 | mV |
| 10-09.6b | offset term | 5.5 | mV |
| 10-09.6c | worst case, uncompensated | 30.5 | mV |
| 10-09.6d | offset-current term | 17.5 | mV |
| 10-09.6e | worst case, compensated | 23 | mV |
| 10-09.7a | typical drift to 125 °C | 53 | µV |
| 10-09.7b | guaranteed change | 3.6 | mV |
| 10-09.8a | PSRR at 100 kHz | 40 | dB |
| 10-09.8b | input-referred ripple | 1.0 | mV |
| 10-09.9a | current into 1 kΩ | 2.5 | mA |
| 10-09.9b | largest sine into 100 Ω | 0.5 | V |
| 10-09.9c | capacitor current | 1.257 | mA |
| 10-09.10a | minimum GBW | 2.025 | MHz |
| 10-09.10b | τ | 78.61 | ns |
| 10-09.10c | slew-to-linear boundary | 314.5 | mV |
| 10-09.10d | slewing time | 0.4214 | µs |
| 10-09.10e | exponential time | 578.6 | ns |
| 10-09.10f | GBW with no slew limit | 1.466 | MHz |
| 10-09.11a | allowable offset change | 5 | µV |
| 10-09.11b | allowable drift | 0.0714 | µV/°C |
| 10-09.12a | top of the high-CMRR region | 0.4 | V |
| 10-09.12b | fraction of the supply | 22.2 | % |
