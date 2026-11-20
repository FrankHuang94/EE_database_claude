# Solutions 12-10 · Noise in Circuits

Problems: [12-10 problems](../problems/12-10-problems.md) · Chapter: [12-10](../chapters/12-10-noise-in-circuits.md). Every number below is recomputed by [verify_12_10.py](../verify/verify_12_10.py), which integrates spectra numerically and finds design values by root finding rather than reusing these formulas.

---

## Solutions

### Solution 12-10.1

$\sqrt{4kT \times 10\ \text{k}\Omega}$ = **12.87** nV/√Hz at 300 K and **6.521** nV/√Hz at 77 K: cooling by a factor of 3.9 lowers the density by its square root.

### Solution 12-10.2

In series, 4 kΩ: **8.141** nV/√Hz (the two noise powers add). In parallel, 750 Ω: **3.525** nV/√Hz. In both cases the result is the thermal noise of the combined resistance.

### Solution 12-10.3

$\sqrt{2q \times 10\ \text{nA}}$ = **56.61** fA/√Hz, and over 1 kHz, $56.61\ \text{fA} \times \sqrt{1000}$ = **1.790** pA RMS.

### Solution 12-10.4

$\sqrt{kT/10\ \text{pF}}$ = **20.35** µV. For 10 µV, $C = kT/(10\ \mu\text{V})^2$ = **41.42** pF.

### Solution 12-10.5

Flicker: $(10\ \text{nV})^2 \times 1\ \text{kHz} \times \ln(100)$ gives **678.6** nV. White: $(10\ \text{nV})^2 \times 9.9\ \text{Hz}$ gives **31.46** nV. Total: **679.3** nV. Below the corner the white floor is irrelevant; this is why precision DC amplifiers use chopping.

### Solution 12-10.6

$g_m = 100\ \mu\text{A}/25.852\ \text{mV}$ = **3.868** mA/V, so $R_{eq} = 1/(2g_m)$ = **129.3** Ω and $e_n = \sqrt{4kTR_{eq}}$ = **1.463** nV/√Hz. $I_B$ = 1 µA, so $i_n = \sqrt{2qI_B}$ = **0.5661** pA/√Hz.

### Solution 12-10.7

$R_{eq} = (2\ \text{nV})^2/(4kT)$ = **241.4** Ω, so $g_m = \gamma/R_{eq}$ = **2.761** mA/V and $I_D = g_mV_{ov}/2$ = **276.1** µA.

### Solution 12-10.8

$\sqrt{2^2 + (10/10)^2}$ = **2.236** nV/√Hz. With a gain of 3: $\sqrt{4 + (10/3)^2}$ = **3.887** nV/√Hz: a low first-stage gain lets the second stage matter.

### Solution 12-10.9

$\sqrt{4kT \times 10\ \text{k}\Omega}$ = **12.87** nV/√Hz; $i_nR_s$ = **20** nV/√Hz; total $\sqrt{5^2 + 12.87^2 + 20^2}$ = **24.30** nV/√Hz, so NF $= 20\log_{10}(24.30/12.87)$ = **5.521** dB. The optimum is $R_{opt} = e_n/i_n$ = **2.5** kΩ, where $F_{min} = 1 + e_ni_n/(2kT)$ = **2.207**, or NF = **3.438** dB.

### Solution 12-10.10

LSB = 2 V/2¹⁴ = **122.1** µV; quantization noise LSB/√12 = **35.24** µV; $C = kT/(35.24\ \mu\text{V})^2$ = **3.336** pF.

### Solution 12-10.11

$R_{eq} = (1.5\ \text{nV})^2/(4kT)$ = **135.8** Ω. The transistor gets 90%: $\gamma/g_m = 0.9R_{eq}$, so $g_m$ = **5.454** mA/V. The load gets 10%: $1/(g_m^2R_D) = 0.1R_{eq}$, so $R_D$ = **2.475** kΩ, and the gain is $g_mR_D$ = **13.5**.

### Solution 12-10.12

$\int_0^\infty df/(1 + (f/f_c)^2) = (\pi/2)f_c$ = **15.71** kHz, so the RMS output is $4\ \text{nV} \times \sqrt{15\,708}$ = **501.3** nV. The noise bandwidth is larger because a first-order filter rolls off slowly: noise above the corner, attenuated but not removed, still adds power.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 12-10.1a | density at 300 K | 12.87 | nV/√Hz |
| 12-10.1b | density at 77 K | 6.521 | nV/√Hz |
| 12-10.2a | series | 8.141 | nV/√Hz |
| 12-10.2b | parallel | 3.525 | nV/√Hz |
| 12-10.3a | shot noise density | 56.61 | fA/√Hz |
| 12-10.3b | RMS over 1 kHz | 1.790 | pA |
| 12-10.4a | kT/C at 10 pF | 20.35 | µV |
| 12-10.4b | C for 10 µV | 41.42 | pF |
| 12-10.5a | flicker part | 678.6 | nV |
| 12-10.5b | white part | 31.46 | nV |
| 12-10.5c | total | 679.3 | nV |
| 12-10.6a | g_m | 3.868 | mA/V |
| 12-10.6b | equivalent noise resistance | 129.3 | Ω |
| 12-10.6c | voltage noise density | 1.463 | nV/√Hz |
| 12-10.6d | current noise density | 0.5661 | pA/√Hz |
| 12-10.7a | equivalent noise resistance | 241.4 | Ω |
| 12-10.7b | g_m | 2.761 | mA/V |
| 12-10.7c | drain current | 276.1 | µA |
| 12-10.8a | input noise, gain 10 | 2.236 | nV/√Hz |
| 12-10.8b | input noise, gain 3 | 3.887 | nV/√Hz |
| 12-10.9a | source thermal noise | 12.87 | nV/√Hz |
| 12-10.9b | current-noise term | 20 | nV/√Hz |
| 12-10.9c | total input noise | 24.30 | nV/√Hz |
| 12-10.9d | noise figure | 5.521 | dB |
| 12-10.9e | optimum source resistance | 2.5 | kΩ |
| 12-10.9f | minimum noise factor | 2.207 | — |
| 12-10.9g | minimum noise figure | 3.438 | dB |
| 12-10.10a | LSB | 122.1 | µV |
| 12-10.10b | quantization noise | 35.24 | µV |
| 12-10.10c | sampling capacitance | 3.336 | pF |
| 12-10.11a | equivalent noise resistance | 135.8 | Ω |
| 12-10.11b | g_m | 5.454 | mA/V |
| 12-10.11c | R_D | 2.475 | kΩ |
| 12-10.11d | gain | 13.5 | — |
| 12-10.12a | noise bandwidth | 15.71 | kHz |
| 12-10.12b | RMS output | 501.3 | nV |
