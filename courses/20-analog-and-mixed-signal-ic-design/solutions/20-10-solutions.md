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
