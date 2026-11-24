# Solutions 20-05 · Comparators and Sample-and-Hold Circuits

Problems: [20-05 problem set](../problems/20-05-problems.md) · Chapter: [20-05](../chapters/20-05-comparators-and-sample-and-hold.md). Every number below is recomputed by [verify_20_05.py](../verify/verify_20_05.py).

---

## Solutions

### Solution 20-05.1

(a) $\sqrt{kT/C}$ = **203.5** µV at 100 fF, **64.4** µV at 1 pF and **20.4** µV at 10 pF: tenfold capacitance buys a factor $\sqrt{10}$.

(b) $\Delta$ = 1.0 V/1024 = **0.977** mV. Equal noise means $2kT/C = \Delta^2/12$, so $C = 24kT/\Delta^2$ = **104** fF per side. The ideal SNR is $10\log_{10}[(A^2/2)/(\Delta^2/12)]$ with $A$ = 0.5 V: **62.0** dB. With the kT/C noise added (doubling the noise power), **59.0** dB.

### Solution 20-05.2

$C = 24kT/\Delta^2$ with $\Delta = 1.6\text{ V}/2^N$:

| Bits | 10 | 12 | 14 | 16 |
|---|---|---|---|---|
| $C$ per side | **0.0407** pF | **0.651** pF | **10.4** pF | **167** pF |

Each bit halves $\Delta$, so $C$ grows by a factor of **4** per bit. The driver must charge four times the capacitance in the same time, so its current, and roughly its power, also grows fourfold per bit. Thermal noise, not quantization, is what makes high resolution expensive.

### Solution 20-05.3

(a) The track time is 2.5 ns and 10-bit settling to half an LSB needs $\ln 2^{11}$ = 7.62 time constants: $\tau \le$ **0.328** ns and $R_{on} \le \tau/C$ = 0.328 ns/104 fF = **3.15** kΩ.

(b) The worst case is the highest input, 0.85 V, where $V_{TH}$ = **0.606** V and the bootstrapped overdrive is $V_{DD} - V_{TH}$ = **0.594** V. Then $W/L = 1/(\mu C_{ox}R_{on}V_{ov})$ = **1.78** and $W$ = **0.231** µm.

**Check.** The capacitor is **6.25** times smaller than the 12-bit design's 0.651 pF (two fewer bits, but also a smaller 1.0 V full scale: the ratio is $(0.977\ \text{mV}/0.391\ \text{mV})^2$), so the switch is small too, despite the doubled rate.

### Solution 20-05.4

(a) Charge sharing gives $V_{GS} = V_{DD}C_b/(C_b + C_p)$ = 1.2 × 0.3/0.33 = **1.091** V.

(b) At 1.0 V the overdrive falls from 0.571 V to 1.091 − 0.629 = 0.462 V, so $R_{on}$ rises from 852 Ω to **1053** Ω. Restoring 852 Ω needs a width **1.236** times larger. The wider switch has more gate capacitance and more charge injection, so in practice $C_b$ is made larger instead, at the cost of area.

### Solution 20-05.5

(a) The NMOS turns off where $V_{DD} - v - V_{THn}(v) = 0$: above **0.630** V. The PMOS (gate at 0, well at $V_{DD}$, so $V_{SB} = V_{DD} - v$) turns off where $v - |V_{THp}(v)| = 0$: below **0.570** V.

(b) The conductances add:

| $v_{in}$ | NMOS | PMOS | $R_{on}$ |
|---|---|---|---|
| 0.2 V | on | off | **958** Ω |
| 0.6 V | barely on | barely on | **7.60** kΩ |
| 1.0 V | off | on | **1118** Ω |

(c) Near mid-supply both devices have almost no overdrive, because each threshold (raised by the body effect) is about half the supply. When supplies were 3.3 or 5 V, the sum of the two thresholds was far below $V_{DD}$ and the gate conducted everywhere; at 1.2 V the sum is close to $V_{DD}$ and a hole opens in the middle of the range. Bootstrapping fixes the NMOS's overdrive instead of relying on a second device.

### Solution 20-05.6

(a) $Q_{ch} = WLC_{ox}V_{ov}$ and $R_{on} = L/(\mu C_{ox}WV_{ov})$, so

$$
\Delta V_{inj}\,\tau = \frac{WLC_{ox}V_{ov}}{2C}\cdot\frac{LC}{\mu C_{ox}WV_{ov}} = \frac{L^2}{2\mu} .
$$

Width, capacitance and overdrive all cancel.

(b) For T130, $L^2/(2\mu)$ = (0.13 µm)²/(2 × 350 cm²/V·s) = **2.41 × 10⁻¹³** V·s. At τ = 0.555 ns, $\Delta V_{inj}$ = **0.435** mV, the value Example 20-05.3 found at 1.0 V.

(c) At 65 nm the constant is four times smaller, so $\Delta V_{inj}$ = **0.109** mV at the same τ.

**Check.** This is a process figure of merit for switches: shorter channels give faster, cleaner switches, one of the few analog benefits of scaling (20-12). The units are V·s: volts of error times seconds of settling.

### Solution 20-05.7

(a) $\omega R_0C$ = 2π × 25 MHz × 767 Ω × 0.651 pF = 0.0785, so HD2 ≈ 0.0785 × 0.266 × 0.2/2 → **−53.6** dBc: half the frequency and half the amplitude each give 6 dB.

(b) Doubling the width halves $R_0$, so HD2 = −41.7 − 6.0 = **−47.8** dBc. A wider switch reduces the tracking error, at the cost of charge injection (Problem 20-05.6).

### Solution 20-05.8

$\text{SNR} = -20\log_{10}(2\pi f\sigma_t)$ and ENOB = (SNR − 1.76)/6.02:

| $f_{in}$ | SNR | ENOB |
|---|---|---|
| 10 MHz | **90.1** dB | **14.7** |
| 100 MHz | **70.1** dB | **11.3** |
| 1 GHz | **50.1** dB | **8.0** |

Each decade of frequency costs 20 dB, or 3.3 bits.

### Solution 20-05.9

Signal power is $A^2/2$ = 0.32 V². The noise powers:

- quantization: (112.8 µV)²;
- kT/C, differential: (112.8 µV)²;
- jitter: $0.32 \times (2\pi \times 49\text{ MHz} \times 0.5\text{ ps})^2$, that is **87.1** µV rms;
- comparator: (97.7 µV)².

The total is **206.3** µV rms, so SNR = $10\log_{10}(0.32/(206.3\text{ µV})^2)$ = **68.8** dB and ENOB = **11.1**.

**Check.** Four comparable contributions, none negligible: a balanced design. Removing any single one gains at most about 1.5 dB.

### Solution 20-05.10

(a) $A_{int}$ = 20 × 0.45 = **9.00**. $C = 4\gamma kT/(A_{int}\sigma^2)$ = 4(2/3)(4.1419 × 10⁻²¹)/(9 × (50 µV)²) = **491** fF.

(b) $E = 2CV_{DD}^2$ = **1.41** pJ, and $E\sigma^2$ = 1.41 pJ × (50 µV)² = **3.53 × 10⁻²¹** J·V², equal to $8\gamma kTV_{DD}^2/A_{int}$ = 8(2/3)(4.1419 × 10⁻²¹)(1.44)/9.

(c) At 15 S/A, $A_{int}$ = 6.75 and $C$ = **655** fF, **1.33** times more: the energy cost of noise is inversely proportional to the integration gain, which is why weak-inversion input pairs and dynamic preamplifiers are popular.

### Solution 20-05.11

(a) $\Delta$ = 1.0 V/64 = **15.6** mV; σ = $\Delta/4$ = **3.91** mV, so $WL = (A_{VT}/\sigma)^2$ = (3.5/3.91)² = **0.803** µm².

(b) Each offset lies within ±2σ with probability **0.9545**; all 63 independently: 0.9545⁶³ = **0.0532**. Only about 5% of parts would have every threshold within half an LSB.

(c) With σ = $\Delta/8$, $WL$ = **3.21** µm² and each comparator lies within ±4σ with probability 0.99994, so all 63 do with probability **0.996**.

**Check.** The yield of the whole array falls like a product of many probabilities, so each comparator must be far better than the average error budget suggests: a familiar effect in any system that fails if any one of many parts fails. Flash ADCs therefore use large input devices, preamplifiers and offset calibration.

### Solution 20-05.12

(a) τ = 40 fF/2 mS = **20.0** ps. For 1 mV, $v_0$ = 5 mV and $t_{dec}$ = 20 ps × ln(0.6/0.005) = **95.7** ps. For 10 µV, $v_0$ = 50 µV and $t_{dec}$ = **188** ps.

(b) $v_{min}$ = (0.6/5) $e^{-200/20}$ = **5.45** µV. $P \approx 2v_{min}/\Delta$ = 2 × 5.45 µV/15.6 mV = **6.97 × 10⁻⁴** per conversion.

(c) At 1 GS/s, about **7.0 × 10⁵** unresolved decisions per second. Fast flash ADCs therefore pipeline their latches (giving each decision more than one clock period) and design their encoders to tolerate an undecided comparator.

### Solution 20-05.13

(a) Each decision gets 7.5 ns/12 = 625 ps, minus 300 ps of DAC settling: **325** ps.

(b) $P_{SAR} = 2v_{min}(2^N - 1)/V_{FS}$ with $v_{min} = (V_L/A_0)e^{-T/\tau}$. Setting $P_{SAR}$ = 10⁻⁹:

$$
\frac{T}{\tau} = \ln\frac{2(V_L/A_0)(2^N - 1)}{V_{FS}\cdot 10^{-9}} = \textbf{26.84} ,
$$

so $\tau \le$ 325 ps/26.84 = **12.1** ps.

(c) $g_m \ge C/\tau$ = 60 fF/12.1 ps = **4.96** mS.

**Check.** The latch must be 1.65 times faster than the chapter's 20 ps design. Every time constant saved is worth a factor $e$ in error rate, so latch speed and DAC settling time trade directly against each other in the SAR's budget.

### Solution 20-05.14

(a) The kickback step is 1.2 V × 2 fF/(2 fF + 50 fF) = **46.2** mV, about three LSB. It decays with τ = 500 Ω × 52 fF = **26.0** ps, reaching 0.1 LSB (1.56 mV) after 26.0 ps × ln(46.2/1.56) = **88.0** ps.

(b) With 0.2 fF: **4.78** mV, τ = **25.1** ps, and **28.1** ps to settle. The preamplifier's isolation is as valuable as its gain.

### Solution 20-05.15

| Amplitude | HD2 | HD3 |
|---|---|---|
| 0.4 V | **−41.5** dBc | **−64.4** dBc |
| 0.2 V | **−47.6** dBc | **−76.6** dBc |

Halving the amplitude lowers HD2 by **6.1** dB and HD3 by **12.2** dB. The second harmonic comes from $\alpha A$, proportional to amplitude (−6 dB per halving). Both terms behind the third harmonic, $\beta A^2$ and the second-order $(\alpha A)^2$ mixing term, scale as amplitude squared (−12 dB). Backing off the input by 6 dB therefore buys 12 dB of HD3: a standard trade of SNR for SFDR.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 20-05.1a | sqrt(kT/C) at 100 fF | 203.5 | µV |
| 20-05.1b | sqrt(kT/C) at 1 pF | 64.4 | µV |
| 20-05.1c | sqrt(kT/C) at 10 pF | 20.4 | µV |
| 20-05.1d | 10-bit LSB | 0.977 | mV |
| 20-05.1e | capacitance per side | 104 | fF |
| 20-05.1f | ideal SNR | 62.0 | dB |
| 20-05.1g | SNR with kT/C | 59.0 | dB |
| 20-05.2a | C for 10 bits | 0.0407 | pF |
| 20-05.2b | C for 12 bits | 0.651 | pF |
| 20-05.2c | C for 14 bits | 10.4 | pF |
| 20-05.2d | C for 16 bits | 167 | pF |
| 20-05.2e | growth per bit | 4 | — |
| 20-05.3a | largest tau | 0.328 | ns |
| 20-05.3b | largest R_on | 3.15 | kΩ |
| 20-05.3c | V_TH at 0.85 V | 0.606 | V |
| 20-05.3d | worst-case overdrive | 0.594 | V |
| 20-05.3e | W/L | 1.78 | — |
| 20-05.3f | W | 0.231 | µm |
| 20-05.3g | ln 2^11 | 7.62 | — |
| 20-05.3h | capacitor ratio to the 12-bit design | 6.25 | — |
| 20-05.4a | V_GS with charge sharing | 1.091 | V |
| 20-05.4b | R_on at 1.0 V | 1053 | Ω |
| 20-05.4c | width factor | 1.236 | — |
| 20-05.4d | overdrive at 1.0 V | 0.462 | V |
| 20-05.5a | NMOS off above | 0.630 | V |
| 20-05.5b | PMOS off below | 0.570 | V |
| 20-05.5c | R_on at 0.2 V | 958 | Ω |
| 20-05.5d | R_on at 0.6 V | 7.60 | kΩ |
| 20-05.5e | R_on at 1.0 V | 1118 | Ω |
| 20-05.6a | L^2/(2 mu) | 2.41e-13 | V·s |
| 20-05.6b | injection at tau = 0.555 ns | 0.435 | mV |
| 20-05.6c | injection at 65 nm | 0.109 | mV |
| 20-05.7a | omega R_0 C at 25 MHz | 0.0785 | — |
| 20-05.7b | HD2 at 25 MHz, 0.2 V | −53.6 | dBc |
| 20-05.7c | HD2 with double width | −47.8 | dBc |
| 20-05.8a | SNR at 10 MHz | 90.1 | dB |
| 20-05.8b | ENOB at 10 MHz | 14.7 | bits |
| 20-05.8c | SNR at 100 MHz | 70.1 | dB |
| 20-05.8d | ENOB at 100 MHz | 11.3 | bits |
| 20-05.8e | SNR at 1 GHz | 50.1 | dB |
| 20-05.8f | ENOB at 1 GHz | 8.0 | bits |
| 20-05.8g | bits per decade | 3.3 | bits |
| 20-05.9a | jitter noise | 87.1 | µV |
| 20-05.9b | total noise | 206.3 | µV |
| 20-05.9c | SNR | 68.8 | dB |
| 20-05.9d | ENOB | 11.1 | bits |
| 20-05.9e | most gained by removing one term | 1.5 | dB |
| 20-05.10a | A_int | 9.00 | — |
| 20-05.10b | capacitance | 491 | fF |
| 20-05.10c | energy | 1.41 | pJ |
| 20-05.10d | E sigma^2 | 3.53e-21 | J·V² |
| 20-05.10e | capacitance at 15 S/A | 655 | fF |
| 20-05.10f | ratio | 1.33 | — |
| 20-05.11a | LSB | 15.6 | mV |
| 20-05.11b | sigma | 3.91 | mV |
| 20-05.11c | area | 0.803 | µm² |
| 20-05.11d | P within 2 sigma | 0.9545 | — |
| 20-05.11e | P all 63 | 0.0532 | — |
| 20-05.11f | area for LSB/8 | 3.21 | µm² |
| 20-05.11g | P all 63 at LSB/8 | 0.996 | — |
| 20-05.12a | tau | 20.0 | ps |
| 20-05.12b | decision time at 1 mV | 95.7 | ps |
| 20-05.12c | decision time at 10 uV | 188 | ps |
| 20-05.12d | v_min | 5.45 | µV |
| 20-05.12e | P per conversion | 6.97e-4 | — |
| 20-05.12f | events per second | 7.0e5 | 1/s |
| 20-05.13a | time per comparison | 325 | ps |
| 20-05.13b | T/tau | 26.84 | — |
| 20-05.13c | largest tau | 12.1 | ps |
| 20-05.13d | latch g_m | 4.96 | mS |
| 20-05.13e | speed-up over 20 ps | 1.65 | — |
| 20-05.14a | kickback | 46.2 | mV |
| 20-05.14b | tau | 26.0 | ps |
| 20-05.14c | settling time | 88.0 | ps |
| 20-05.14d | kickback with preamp | 4.78 | mV |
| 20-05.14e | tau with preamp | 25.1 | ps |
| 20-05.14f | settling with preamp | 28.1 | ps |
| 20-05.15a | HD2 at 0.4 V | −41.5 | dBc |
| 20-05.15b | HD3 at 0.4 V | −64.4 | dBc |
| 20-05.15c | HD2 at 0.2 V | −47.6 | dBc |
| 20-05.15d | HD3 at 0.2 V | −76.6 | dBc |
| 20-05.15e | HD2 change | 6.1 | dB |
| 20-05.15f | HD3 change | 12.2 | dB |
