# Solutions 21-10 · Antennas, Arrays, Beamforming and mmWave

Problems: [21-10 problem set](../problems/21-10-problems.md) · Chapter: [21-10](../chapters/21-10-antennas-arrays-mmwave.md). Every number below is recomputed by [verify_21_10.py](../verify/verify_21_10.py).

---

## Solutions

### Solution 21-10.1

$c/2f_0$ = 3.843 mm.

(a) $W = 3.843\sqrt{2/4.5}$ = **2.562** mm.

(b) $W/h$ = 12.81, so $\varepsilon_{eff} = 2.25 + 1.25/\sqrt{1 + 12/12.81}$ = **3.148**.

(c) $\Delta L = 0.412 \times 0.2 \times (3.448 \times 13.08)/(2.890 \times 13.61)$ = **0.094** mm.

(d) $L = 3.843/\sqrt{3.148} - 2 \times 0.094$ = 2.166 − 0.189 = **1.977** mm.

(e) The cell is **3.843** mm square, so the patch fits.

### Solution 21-10.2

(a) $\lvert\Gamma\rvert$ = 1.5/3.5 = 0.4286, so $e_{tot} = 0.7 \times (1 - 0.1837)$ = **57.1** %, (b) **−2.43** dB.

(c) $\cos^2 30°$ = 0.75: **1.25** dB.

### Solution 21-10.3

λ = 345.4 mm at 868 MHz.

(a) $ka = 2\pi \times 20/345.4$ = **0.364**.

(b) $1/0.364^3 + 1/0.364$ = **23.5**.

(c) $0.707/23.5$ = **3.01** %.

(d) 7/866.5 = **0.81** %: the antenna can cover the band with margin, even with a few dB of detuning by the enclosure.

### Solution 21-10.4

(a) $(3 - 1)/(20\sqrt3)$ = **5.77** %. (b) $1/(20\sqrt2)$ = **3.54** %. (c) Relaxing the match from VSWR 2 to 3 buys **63** % more bandwidth, which is why phone antennas are often specified at VSWR 3.

### Solution 21-10.5

(a) $8 \times \lambda/2 = 8 \times 3.843$ mm = **30.7** mm.

(b) $5 + 10\log_{10}64$ = **23.06** dBi.

(c) $23.06 + 10\log_{10}\cos 50°$ = **21.14** dBi.

### Solution 21-10.6

(a) $\sin\theta_{max} = 1/0.6 - 1$ = 0.667: **41.8**°.

(b) $1/0.8 - 1$ = 0.25: **14.5**°.

(c) The grating lobe sits where $\sin\theta = \sin 30° - \lambda/d$ = 0.5 − 1.25 = −0.75: **−48.6**°.

### Solution 21-10.7

(a) $0.886/(64 \times 0.5 \times 0.7071)$ = **3.92** %. (b) **1527** MHz.

(c) $63 \times 3.843\ \text{mm} \times 0.7071/c$ = **571** ps.

(d) **1.59**° from the array factor ($0.886 \times 2/64$ rad = 1.59°).

### Solution 21-10.8

(a) $x = \pi/32$: $-20\log_{10}(\sin x/x)$ = **0.014** dB. (b) $5.625°/\sqrt3$ = **3.25**°. (c) **0.0035** dB.

### Solution 21-10.9

$8 - 1 + 5 + 20\log_{10}8$ = **30.06** dBm.

### Solution 21-10.10

$E$ = 100 W, $G_e$ = 3.162.

(a) $N^* = \sqrt{100/(3.162 \times 0.2 \times 0.05)}$ = **56.2**.

(b) $2\sqrt{100 \times 0.05/(3.162 \times 0.2)}$ = **5.62** W.

(c) $N^*$ grows by $\sqrt2$: **79.5**.

### Solution 21-10.11

(a) $20 \times 10^{-15} \times 2^6 \times 2 \times 10^9$ = **2.56** mW.

(b) $64 \times (40 + 5.12)$ mW = **2.89** W.

(c) $8 \times 45.12 + 64 \times 15$ mW = **1.32** W.

Lower resolution halves the converter power, but the digital array still pays for 64 full chains.

### Solution 21-10.12

(a) $-174 + 10\log_{10}(2.16 \times 10^9) + 10$ = **−70.66** dBm.

(b) λ = 4.997 mm: $20\log_{10}(4\pi \times 50/0.004997)$ = **101.99** dB. (c) 14.7 × 0.05 = **0.74** dB.

(d) 40 − 101.99 − 0.74 + 15 = **−47.73** dBm. (e) **22.9** dB.

(f) **121.99** dB. (g) **7.35** dB. (h) 40 − 121.99 − 7.35 + 15 = −74.34 dBm, SNR **−3.7** dB.

Ten times the distance costs 20 dB of spreading and 6.6 dB more absorption. Oxygen absorption is a feature for short-range 60 GHz links: it limits interference between neighbouring links and lets frequencies be reused closely.

### Solution 21-10.13

(a) 2° = 0.0349 rad, so $N_v \ge 2/0.0349$ = 57.3: **58** virtual elements.

(b) $8 \times 8$ = 64 ≥ 58 (7 × 8 = 56 falls short): **8** TX and RX each, (c) **16** physical antennas.

(d) $2/64$ rad = **1.79**°.

### Solution 21-10.14

(a) $16\sin 60°$ = 13.9: **14** beams. (b) $14 \times 0.125$ ms = **1.75** ms.

(c) $14 \times 14$ = 196 beams: **24.5** ms. Exhaustive sweeps of large panels are too slow to track a moving user, which is why systems search hierarchically (wide beams first, then narrow ones) and track around the last good beam.

### Solution 21-10.15

(a) 4 × 4 = **16**. (b) $c/(2 \times 77\ \text{GHz})$ = **1.95** mm. (c) $15 \times 1.947$ = **29.2** mm. (d) $2/16$ rad = **7.16**°.

(e) $13.5 + 10\log_{10}4$ = **19.5** dBm. (f) Coherent voltages add: $20\log_{10}4$ = **12.04** dB, 6 dB from the extra power and 6 dB from the array gain.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 21-10.1a | patch width | 2.562 | mm |
| 21-10.1b | effective permittivity | 3.148 | |
| 21-10.1c | fringing extension | 0.094 | mm |
| 21-10.1d | patch length | 1.977 | mm |
| 21-10.1e | half-wavelength cell | 3.843 | mm |
| 21-10.2a | total efficiency | 57.1 | % |
| 21-10.2b | total efficiency | −2.43 | dB |
| 21-10.2c | polarization loss at 30° | 1.25 | dB |
| 21-10.3a | ka | 0.364 | |
| 21-10.3b | Chu bound | 23.5 | |
| 21-10.3c | VSWR-2 bandwidth | 3.01 | % |
| 21-10.3d | bandwidth needed | 0.81 | % |
| 21-10.4a | bandwidth at VSWR 3 | 5.77 | % |
| 21-10.4b | bandwidth at VSWR 2 | 3.54 | % |
| 21-10.4c | gain from relaxing to VSWR 3 | 63 | % |
| 21-10.5a | side length | 30.7 | mm |
| 21-10.5b | broadside gain | 23.06 | dBi |
| 21-10.5c | gain at 50° | 21.14 | dBi |
| 21-10.6a | scan limit, 0.6λ | 41.8 | deg |
| 21-10.6b | scan limit, 0.8λ | 14.5 | deg |
| 21-10.6c | grating-lobe direction | −48.6 | deg |
| 21-10.7a | squint bandwidth | 3.92 | % |
| 21-10.7b | squint bandwidth | 1527 | MHz |
| 21-10.7c | TTD delay span | 571 | ps |
| 21-10.7d | broadside beamwidth | 1.59 | deg |
| 21-10.8a | gain loss, 5 bits | 0.014 | dB |
| 21-10.8b | rms error, 5 bits | 3.25 | deg |
| 21-10.8c | gain loss, 6 bits | 0.0035 | dB |
| 21-10.9 | handset EIRP | 30.06 | dBm |
| 21-10.10a | optimal element count | 56.2 | |
| 21-10.10b | minimum DC power | 5.62 | W |
| 21-10.10c | optimal count, half overhead | 79.5 | |
| 21-10.11a | power per ADC | 2.56 | mW |
| 21-10.11b | digital array | 2.89 | W |
| 21-10.11c | hybrid array | 1.32 | W |
| 21-10.12a | noise floor | −70.66 | dBm |
| 21-10.12b | path loss, 50 m | 101.99 | dB |
| 21-10.12c | absorption, 50 m | 0.74 | dB |
| 21-10.12d | received power, 50 m | −47.73 | dBm |
| 21-10.12e | SNR, 50 m | 22.9 | dB |
| 21-10.12f | path loss, 500 m | 121.99 | dB |
| 21-10.12g | absorption, 500 m | 7.35 | dB |
| 21-10.12h | SNR, 500 m | −3.7 | dB |
| 21-10.13a | virtual elements needed | 58 | |
| 21-10.13b | TX and RX each | 8 | |
| 21-10.13c | physical antennas | 16 | |
| 21-10.13d | achieved resolution | 1.79 | deg |
| 21-10.14a | beams per axis | 14 | |
| 21-10.14b | sweep time, linear array | 1.75 | ms |
| 21-10.14c | sweep time, panel | 24.5 | ms |
| 21-10.15a | virtual channels | 16 | |
| 21-10.15b | half wavelength | 1.95 | mm |
| 21-10.15c | virtual aperture | 29.2 | mm |
| 21-10.15d | angular resolution | 7.16 | deg |
| 21-10.15e | total conducted power | 19.5 | dBm |
| 21-10.15f | coherent gain of four transmitters | 12.04 | dB |
