# Solutions 21-02 · Impedance Matching Networks

Problems: [21-02 problem set](../problems/21-02-problems.md) · Chapter: [21-02](../chapters/21-02-impedance-matching-networks.md). Every number below is recomputed by [verify_21_02.py](../verify/verify_21_02.py).

---

## Solutions

### Solution 21-02.1

$Q = \sqrt{50/25 - 1}$ = **1**; series reactance $QR_{low}$ = **25** Ω, $L = 25/(2\pi \times 1\ \text{GHz})$ = **3.979** nH; shunt susceptance $Q/R_{high}$ = **0.02** S, $C$ = **3.183** pF.

### Solution 21-02.2

Same Q = 2 and magnitudes, opposite element types: series $X = -20$ Ω gives $C = 1/(\omega \times 20)$ = **3.316** pF; shunt $B = -0.04$ S gives $L = 1/(\omega \times 0.04)$ = **1.658** nH. The high-pass form blocks DC and can feed bias through the shunt inductor.

### Solution 21-02.3

$Q = \sqrt{50/30 - 1}$ = **0.8165**; the network needs $+24.49$ Ω in series; the load supplies +10 Ω, so add **14.49** Ω: $L$ = **1.153** nH. Shunt $B = Q/50$ = 0.01633 S: $C$ = **1.299** pF. The input is 50.0 Ω.

### Solution 21-02.4

Q = √(100/50 − 1) = 1. The high-pass network needs a shunt susceptance of −Q/100 = −0.01 S at the load and a series reactance of −QR_low = −50 Ω at the 50 Ω side. The load already has +ωC = **0.01257** S, so the inductor must supply −0.01 − 0.01257 = −0.02257 S: $L$ = **7.053** nH. Series $C = 1/(\omega \times 50)$ = **3.183** pF. The input is 50.0 Ω.

### Solution 21-02.5

$R_v = 50/(4^2 + 1)$ = **2.941** Ω. $Q_1 = 4$ on the 50 Ω side gives $B_1$ = **0.08** S; $Q_2 = \sqrt{25/2.941 - 1}$ = 2.739 gives $B_2 = Q_2/25$ = **0.1095** S; series $X = (4 + 2.739)R_v$ = **19.82** Ω.

### Solution 21-02.6

Ratio 25, per section $25^{1/3}$ = 2.924: intermediate resistances **5.848** Ω and **17.10** Ω; each section's Q = √1.924 = **1.387**.

### Solution 21-02.7

$\ln(25/50) = -0.693$, split 1:3:3:1 (eighths): $Z_1 = 50e^{-0.0866}$ = **45.85** Ω, $Z_2 = Z_1e^{-0.260}$ = **35.36** Ω, $Z_3$ = **27.26** Ω. With $A = 2^{-3}(1/3)$, $\cos\theta_m = \tfrac12(0.05/0.04167)^{1/3}$ and the small-reflection fractional bandwidth is **71.3**%; the exact cascade of the three lines gives **69.7**%.

### Solution 21-02.8

$10\log_{10}(1 + 1/10)$ = **0.414** dB; $10\log_{10}(1 + 5/10)$ = **1.761** dB.

### Solution 21-02.9

$R_{opt} = 3^2/4$ = **2.25** Ω; ratio **22.2**. One section: Q = √21.2 = **4.61**, loss $10\log_{10}(1 + 4.61/30)$ = **0.620** dB. Two sections: Q = √(√22.2 − 1) = **1.93** each, total loss $2 \times 10\log_{10}(1 + 1.93/30)$ = **0.541** dB, with a much wider band.

### Solution 21-02.10

$\Delta f \le 1/[2RC\ln(1/\Gamma_m)]$ with RC = 150 ps: 10 dB ($\Gamma_m$ = 0.316): **2.90** GHz; 20 dB: **1.45** GHz.

### Solution 21-02.11

$R_v = 50/(3^2 + 1)$ = **5** Ω, $Q_1 = Q_2 = 3$: shunt susceptances 0.06 S each, $C$ = **3.979** pF each; series reactance $(3 + 3) \times 5$ = 30 Ω, $L$ = **1.989** nH. Simulated 10 dB band: **2.235**–**2.536** GHz, **12.5**%: a third-order low-pass (harmonic) filter whose response has a reflection zero at 2.4 GHz. It also passes DC and reflects strongly between about 0.3 and 2.2 GHz, so the 2.235–2.536 GHz band is the match around the upper reflection zero of a low-pass, not a passband.

### Solution 21-02.12

Section Q and total loss $n \times 10\log_{10}(1 + Q_s/20)$:

| n | Q per section | total loss (dB) |
|---|---|---|
| 1 | **4.90** | **0.952** |
| 2 | **2.00** | **0.828** |
| 3 | **1.39** | **0.874** |
| 4 | **1.11** | **0.940** |

Two sections are best. Each added section lowers Q but adds another lossy inductor; past two sections the extra components cost more than the lower Q saves (for small $Q_s/Q_u$ the total loss is about $4.34\,nQ_s/Q_u$ dB, and $nQ_s$ grows again as $n$ increases).

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 21-02.1a | Q | 1 | — |
| 21-02.1b | series reactance | 25 | Ω |
| 21-02.1c | L | 3.979 | nH |
| 21-02.1d | shunt susceptance | 0.02 | S |
| 21-02.1e | C | 3.183 | pF |
| 21-02.2a | series C | 3.316 | pF |
| 21-02.2b | shunt L | 1.658 | nH |
| 21-02.3a | Q | 0.8165 | — |
| 21-02.3b | added series reactance | 14.49 | Ω |
| 21-02.3c | L | 1.153 | nH |
| 21-02.3d | C | 1.299 | pF |
| 21-02.4a | load susceptance | 0.01257 | S |
| 21-02.4b | shunt L | 7.053 | nH |
| 21-02.4c | series C | 3.183 | pF |
| 21-02.5a | virtual resistance | 2.941 | Ω |
| 21-02.5b | B1 | 0.08 | S |
| 21-02.5c | B2 | 0.1095 | S |
| 21-02.5d | series reactance | 19.82 | Ω |
| 21-02.6a | first intermediate | 5.848 | Ω |
| 21-02.6b | second intermediate | 17.10 | Ω |
| 21-02.6c | section Q | 1.387 | — |
| 21-02.7a | Z1 | 45.85 | Ω |
| 21-02.7b | Z2 | 35.36 | Ω |
| 21-02.7c | Z3 | 27.26 | Ω |
| 21-02.7d | fractional bandwidth | 71.3 | % |
| 21-02.7e | fractional bandwidth, exact | 69.7 | % |
| 21-02.8a | loss, Qn 1 | 0.414 | dB |
| 21-02.8b | loss, Qn 5 | 1.761 | dB |
| 21-02.9a | R_opt | 2.25 | Ω |
| 21-02.9b | ratio | 22.2 | — |
| 21-02.9c | one-section Q | 4.61 | — |
| 21-02.9d | one-section loss | 0.620 | dB |
| 21-02.9e | two-section Q | 1.93 | — |
| 21-02.9f | two-section loss | 0.541 | dB |
| 21-02.10a | bandwidth, 10 dB | 2.90 | GHz |
| 21-02.10b | bandwidth, 20 dB | 1.45 | GHz |
| 21-02.11a | virtual resistance | 5 | Ω |
| 21-02.11b | shunt C | 3.979 | pF |
| 21-02.11c | series L | 1.989 | nH |
| 21-02.11d | lower edge | 2.235 | GHz |
| 21-02.11e | upper edge | 2.536 | GHz |
| 21-02.11f | fractional bandwidth | 12.5 | % |
| 21-02.12a | Q, one section | 4.90 | — |
| 21-02.12b | loss, one section | 0.952 | dB |
| 21-02.12c | Q, two sections | 2.00 | — |
| 21-02.12d | loss, two sections | 0.828 | dB |
| 21-02.12e | Q, three sections | 1.39 | — |
| 21-02.12f | loss, three sections | 0.874 | dB |
| 21-02.12g | Q, four sections | 1.11 | — |
| 21-02.12h | loss, four sections | 0.940 | dB |
| 21-02.12i | small-ratio coefficient | 4.34 | dB |
