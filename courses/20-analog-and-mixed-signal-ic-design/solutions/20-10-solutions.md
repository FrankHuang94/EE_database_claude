# Solutions 20-10 · PLLs and Jitter

Problems: [20-10 problem set](../problems/20-10-problems.md) · Chapter: [20-10](../chapters/20-10-plls-and-jitter.md). Every number below is recomputed by [verify_20_10.py](../verify/verify_20_10.py).

---

## Solutions

### Solution 20-10.1

$f_{out} = 96 \times 25\text{ MHz}$ = **2.4** GHz; $K_{PD} = 200\text{ µA}/2\pi$ = **31.8** µA/rad.

### Solution 20-10.2

$\Delta f$ = 1 GHz/V × 10 mV = **10** MHz. The extra phase is $2\pi\Delta f\,t = 2\pi \times 10\text{ MHz} \times 1\text{ µs}$ = **62.8** rad (ten cycles): a frequency error makes phase grow without bound, which is why a phase detector can correct frequency.

### Solution 20-10.3

$\omega_n = \sqrt{I_{cp}K_{VCO}/(2\pi NC)} = \sqrt{100\text{ µA} \times 2\pi \times 200\text{ MHz}/(2\pi \times 40 \times 100\text{ pF})}$ = 2.24 × 10⁶ rad/s, **356** kHz. $\zeta = (R/2)\sqrt{I_{cp}K_{VCO}C/(2\pi N)}$ = **1.12**.

### Solution 20-10.4

$\arctan[(b - 1)/(2\sqrt b)]$: **36.9**° (b = 4), **54.9**° (b = 10), **64.8**° (b = 20). Wider spacing buys margin but moves the ripple pole higher, filtering less reference ripple.

### Solution 20-10.5

$K = I_{cp}K_{VCO}/(2\pi N)$; $C_1 + C_2 = (K/\omega_c^2)\sqrt{11/1.1}$ = **160** pF; $C_1$ = **144** pF, $C_2$ = **16.0** pF; $R = \sqrt{10}/(\omega_cC_1)$ = **6.98** kΩ. The lab confirms a 500 kHz crossover with 54.9° of margin.

### Solution 20-10.6

$f_{ref}/10$ = **2.5** MHz.

### Solution 20-10.7

$-155 + 20\log_{10}96$ = **−115.4** dBc/Hz.

### Solution 20-10.8

$\sigma_\phi^2 = 2\mathcal{L}_0(f_c - f_1) + 2\mathcal{L}_0f_c(1 - f_c/f_2)$ with $\mathcal{L}_0 = 10^{-10.5}$: $\sigma_\phi$ = **11.2** mrad, $\sigma_t = \sigma_\phi/(2\pi \times 2.4\text{ GHz})$ = **744** fs.

### Solution 20-10.9

$\sigma_t = 10^{-70/20}/(2\pi \times 500\text{ MHz})$ = **101** fs.

### Solution 20-10.10

Input-referred phase noise (one-sided) $(i_n/K_{PD})^2 = (10\text{ pA} \times 2\pi/200\text{ µA})^2$ = 9.87 × 10⁻¹⁴ rad²/Hz; halved for $\mathcal{L}$: **−133.1** dBc/Hz. At the output, $+20\log_{10}96$: **−93.4** dBc/Hz, far above the reference's −115.4 dBc/Hz: the pump, not the crystal, sets this PLL's in-band noise. A larger $I_{cp}$ helps, because $K_{PD}$ grows faster than a pump's noise current.

### Solution 20-10.11

$N$ = 2.41 GHz/25 MHz = **96.4**. MASH 1-1-1 noise: $(2\pi)^2/(12 \times 25\text{ MHz}) \times (2\sin(\pi \times 0.04))^4$ → **−92.8** dBc/Hz at 1 MHz. With a 25 MHz reference, 1 MHz is a much larger fraction of $f_{ref}$ than in Example 20-10.6, so the shaped noise is far higher: a low reference rate costs fractional-N noise.

### Solution 20-10.12

A pattern of period 5 cycles produces spurs at multiples of $f_{ref}/5$ = **5** MHz, which an ordinary loop bandwidth cannot remove.

### Solution 20-10.13

PLL: $20\log_{10}(2 \times 10^{-13}) + 10\log_{10}4$ = **−248.0** dB. Oscillator: $125 + 20\log_{10}2400 - 10\log_{10}2$ = **189.6** dB.

### Solution 20-10.14

Solve $\mathcal{L} = (2\pi)^2(\Delta t\,f_0)^2/(12f_{ref})$ for Δt: $\Delta t = \sqrt{12f_{ref}\mathcal{L}}/(2\pi f_0) = \sqrt{12 \times 25\text{ MHz} \times 10^{-11}}/(2\pi \times 2.4\text{ GHz})$ = **3.63** ps, finer than one inverter delay in most processes: hence interpolating or ΔΣ TDCs.

### Solution 20-10.15

(a) $K = 500\ \mu\text{A} \times 2\pi \times 500\ \text{MHz/V}/(2\pi \times 100)$ = 2500 A/(V·s), in the units that make $K/(s^2C)$ dimensionless. With $\omega_c = 2\pi \times 0.3$ MHz = 1.885 × 10⁶ rad/s, $C_1 + C_2 = 2500\sqrt{10}/\omega_c^2$ = **2.23** nF; $C_2 = (C_1 + C_2)/b$ = **223** pF and $C_1$ = **2.00** nF; the zero at $\omega_c/\sqrt b$ needs $R = \sqrt b/(\omega_cC_1)$ = **838** Ω.

(b) Without $C_2$ the loop is second order with $\omega_n = \sqrt{K/C_1}$ = 1.117 × 10⁶ rad/s, so $\omega_n/2\pi$ = **178** kHz, and $\zeta = (R/2)\sqrt{KC_1}$ = **0.937**.

(c) The frequency error after the hop is the 50 MHz step times one minus the closed loop's step response, which decays as $e^{-\zeta\omega_nt}$ once the fast terms have died. Reaching 10 kHz is a factor of 5000: $t \approx \ln 5000/(\zeta\omega_n)$ = 8.52/(1.047 × 10⁶ s⁻¹) = **8.13** µs. The exact 8.17 µs is close because the ripple pole $C_2$ adds at $\sqrt b\,\omega_c$, well above $\zeta\omega_n$, and changes the slow envelope only slightly.

(d) At fixed b every time constant of the loop scales as $1/\omega_c$, so halving the crossover doubles the settling time, to about **16.3** µs: narrow loops filter noise and spurs better but settle slowly.

### Solution 20-10.16

(a) $N^2 \times 10^{-15}$ is −110 dBc/Hz. The VCO line $-120 + 20\log_{10}(1\ \text{MHz}/f)$ reaches −110 at $f$ = **0.316** MHz. The MASH noise is −107.9 dBc/Hz at 1 MHz and rises 40 dB per decade there; it falls to −110 dBc/Hz at **0.884** MHz (solving $\mathcal{L}_{\Sigma\Delta} = 10^{-11}$). The reference and VCO alone would put the optimum near 0.3 MHz, and above about 0.9 MHz the loop would pass ΔΣ noise larger than the reference floor, so the bandwidth should sit well below 0.9 MHz; how far below depends on how much MASH noise leaks just beyond the crossover.

(b) Integrating $\mathcal{L}_{ref}\lvert H/N\rvert^2 + \mathcal{L}_{VCO}\lvert 1/(1 + G)\rvert^2 + \mathcal{L}_{\Sigma\Delta}\lvert H/N\rvert^2$ from 10 kHz to 20 MHz at 5.0123 GHz:

| Crossover | Jitter | Settling to 10 kHz |
|---|---|---|
| 0.2 MHz | **199** fs | **12.3** µs |
| 0.3 MHz | **257** fs | **8.17** µs |
| 0.5 MHz | **551** fs | **4.90** µs |

The MASH noise moves the jitter optimum below the 0.3 MHz of part (a): at 0.3 MHz it raises the jitter from **171** fs to 257 fs (the MASH term alone is **192** fs rms; independent contributions add in quadrature). No crossover meets both specifications: the bandwidth that is quiet enough settles too slowly, and the one that settles in time lets in too much ΔΣ noise.

(c) The shaped noise is $\mathcal{L}_{\Sigma\Delta} = \frac{(2\pi)^2}{12f_{ref}}[2\sin(\pi f/f_{ref})]^4 \approx \frac{(2\pi)^2}{12f_{ref}}(2\pi f/f_{ref})^4 \propto f^4/f_{ref}^5$ at low offsets, so doubling $f_{ref}$ lowers it by $10\log_{10}2^5$ = **15.1** dB. Halving N lowers the multiplied reference noise by $20\log_{10}2$ = **6.02** dB. At a 0.3 MHz crossover the jitter falls to **142** fs while the settling stays **8.17** µs (the normalized closed loop is unchanged), so both specifications are met. With $K$ doubled (N halved), $C_1 + C_2$ = **4.44** nF, $C_1$ = **4.00** nF, $C_2$ = **444** pF and $R$ = **420** Ω.

(d) $C_1 + C_2 = K\sqrt b/\omega_c^2$ is proportional to $I_{cp}K_{VCO}$ at a fixed crossover, so it must fall by 4.44 nF/0.5 nF = **8.9**. Lowering $I_{cp}$ raises the pump's input-referred noise (its current noise falls more slowly than its gain $I_{cp}/2\pi$), eating into the margin of part (c); lowering $K_{VCO}$ narrows the tuning range per band, so the VCO needs more switched-capacitor bands and band calibration. A typical answer splits the factor, for example $I_{cp}$ down 3× and $K_{VCO}$ down 3×, and rechecks the jitter.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 20-10.1a | output frequency | 2.4 | GHz |
| 20-10.1b | PFD/pump gain | 31.8 | µA/rad |
| 20-10.2a | frequency step | 10 | MHz |
| 20-10.2b | extra phase | 62.8 | rad |
| 20-10.3a | natural frequency | 356 | kHz |
| 20-10.3b | damping | 1.12 | — |
| 20-10.4a | PM, b = 4 | 36.9 | ° |
| 20-10.4b | PM, b = 10 | 54.9 | ° |
| 20-10.4c | PM, b = 20 | 64.8 | ° |
| 20-10.5a | C1 + C2 | 160 | pF |
| 20-10.5b | C1 | 144 | pF |
| 20-10.5c | C2 | 16.0 | pF |
| 20-10.5d | R | 6.98 | kΩ |
| 20-10.6a | bandwidth limit | 2.5 | MHz |
| 20-10.7a | multiplied reference noise | −115.4 | dBc/Hz |
| 20-10.8a | rms phase | 11.2 | mrad |
| 20-10.8b | rms jitter | 744 | fs |
| 20-10.9a | allowed jitter | 101 | fs |
| 20-10.10a | pump noise, input | −133.1 | dBc/Hz |
| 20-10.10b | pump noise, output | −93.4 | dBc/Hz |
| 20-10.11a | divide ratio | 96.4 | — |
| 20-10.11b | MASH noise at 1 MHz | −92.8 | dBc/Hz |
| 20-10.12a | spur spacing | 5 | MHz |
| 20-10.13a | PLL FoM | −248.0 | dB |
| 20-10.13b | oscillator FoM | 189.6 | dB |
| 20-10.14a | TDC resolution | 3.63 | ps |
| 20-10.15a | C1 + C2 | 2.23 | nF |
| 20-10.15b | C2 | 223 | pF |
| 20-10.15c | C1 | 2.00 | nF |
| 20-10.15d | R | 838 | Ω |
| 20-10.15e | natural frequency | 178 | kHz |
| 20-10.15f | damping | 0.937 | — |
| 20-10.15g | settling estimate | 8.13 | µs |
| 20-10.15h | settling at half the crossover | 16.3 | µs |
| 20-10.16a | reference-VCO crossing | 0.316 | MHz |
| 20-10.16b | MASH reaches the floor | 0.884 | MHz |
| 20-10.16c | jitter, 0.2 MHz | 199 | fs |
| 20-10.16d | settling, 0.2 MHz | 12.3 | µs |
| 20-10.16e | jitter, 0.3 MHz | 257 | fs |
| 20-10.16f | settling, 0.3 MHz | 8.17 | µs |
| 20-10.16g | jitter, 0.5 MHz | 551 | fs |
| 20-10.16h | settling, 0.5 MHz | 4.90 | µs |
| 20-10.16i | MASH reduction for 2× reference | 15.1 | dB |
| 20-10.16j | reference-noise reduction | 6.02 | dB |
| 20-10.16k | jitter, 100 MHz reference | 142 | fs |
| 20-10.16l | C1 + C2 | 4.44 | nF |
| 20-10.16m | C1 | 4.00 | nF |
| 20-10.16n | C2 | 444 | pF |
| 20-10.16o | R | 420 | Ω |
| 20-10.16p | required reduction of Icp·KVCO | 8.9 | — |
| 20-10.16q | MASH contribution alone, 0.3 MHz | 192 | fs |
| 20-10.16r | jitter without MASH, 0.3 MHz | 171 | fs |
