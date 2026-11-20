# Solutions 12-01 · Differential Pairs

Problems: [12-01 problems](../problems/12-01-problems.md) · Chapter: [12-01](../chapters/12-01-differential-pairs.md). Every number below is recomputed by [verify_12_01.py](../verify/verify_12_01.py).

---

## Solutions

### Solution 12-01.1

Each transistor carries 1 mA: $g_m = 1\ \text{mA}/V_T$ = **38.68** mA/V. Differential output: $g_mR_C$ = **77.36**; single-ended: **38.68**. Each base sees $r_\pi = \beta/g_m$, and the differential input sees two in series: $2r_\pi$ = **5.170** kΩ.

### Solution 12-01.2

$V_{ov} = \sqrt{I_{SS}/k_n}$ = **0.3162** V; $g_m = \sqrt{k_nI_{SS}}$ = **0.3162** mA/V; full switching at $\sqrt2V_{ov}$ = **0.4472** V.

### Solution 12-01.3

$i_{C1} = 1\ \text{mA}/(1 + e^{-25/25.852})$ = **0.7245** mA: a 25 mV input already moves the split from 50/50 to 72/28.

### Solution 12-01.4

$(1 + 2g_mR_{SS})/2 = 201/2$ = **100.5**, or **40.04** dB.

### Solution 12-01.5

$\Delta I = (k_nv_{id}/2)\sqrt{4I_{SS}/k_n - v_{id}^2} = 0.05\ \text{mA/V} \times \sqrt{0.4 - 0.01}$ V = 31.22 µA, so $i_{D1}$ = **65.61** µA and $i_{D2}$ = **34.39** µA.

### Solution 12-01.6

$V_{ov} = \sqrt{0.4/4}$ = **0.3162** V. $V_{IC,\min} = 0.5 + 0.3162 + 0.25$ = **1.066** V; $V_{IC,\max} = 3.3 - 0.2\ \text{mA} \times 5\ \text{k}\Omega + 0.5$ = **2.8** V.

### Solution 12-01.7

(a) $(V_{ov}/2)(\Delta R/R) = 0.1 \times 0.02$ = **2.0** mV. (b) Same direction: $2.0 + 1.5$ = **3.5** mV. (c) Independent: $\sqrt{2^2 + 1.5^2}$ = **2.5** mV.

### Solution 12-01.8

Exact: $V_T\ln(1.05)$ = **1.261** mV; linear: $V_T \times 0.05$ = **1.293** mV (the linearization overstates it by **2.5**% at a 5% mismatch). Drift: $1.261\ \text{mV}/300\ \text{K}$ = **4.204** µV/K.

### Solution 12-01.9

With $g_{m1,2} = g_m \pm \Delta g_m/2$ and a common-mode input $v_{ic}$, the tail node moves to $v_s$ with $(g_{m1} + g_{m2})(v_{ic} - v_s) = v_s/R_{SS}$, so $v_{ic} - v_s = v_{ic}/(1 + 2g_mR_{SS})$. The drain currents differ by $\Delta g_m(v_{ic} - v_s)$, so

$$
A_{cm\to dm} = \frac{R_D\Delta g_m}{1 + 2g_mR_{SS}}, \qquad \text{CMRR}_{diff} = \frac{g_mR_D}{A_{cm\to dm}} = \frac{g_m}{\Delta g_m}(1 + 2g_mR_{SS}) = 100 \times 201 = \mathbf{20\,100},
$$

or **86.06** dB.

### Solution 12-01.10

$g_m = 0.5\ \text{mA}/V_T$ = **19.34** mA/V; $1/(500 + 51.70)$ = **1.813** mA/V: degeneration cuts the transconductance **10.67**-fold and extends the linear range roughly to $\pm I_{EE}R_E$.

### Solution 12-01.11

$WL = (A_{VT}/\sigma)^2 = (3.5/0.5)^2$ = **49** µm², so $W$ = 49 µm at $L$ = 1 µm. $C_{gs} \approx \tfrac23 \times 49 \times 10$ = **326.7** fF per device: precision costs input capacitance.

### Solution 12-01.12

From §3.2, $i_{D1} - i_{D2} = \frac{k_nv_{id}}{2}\sqrt{\frac{4I_{SS}}{k_n}}\sqrt{1 - \frac{k_nv_{id}^2}{4I_{SS}}}$. The first factor is $\sqrt{k_nI_{SS}}\,v_{id} = g_mv_{id}$, and $k_n/(4I_{SS}) = 1/(4V_{ov}^2)$, which gives the result. 1% compression: $1 - v_{id}^2/(4V_{ov}^2) = 0.99^2$, so $v_{id} = 2V_{ov}\sqrt{0.0199}$ = **0.2821** $V_{ov}$ = **89.22** mV, about ten times the BJT pair's 9.01 mV.

### Solution 12-01.13

$I_{SS} = 0.3\ \text{V}/50\ \Omega$ = **6** mA; $V_{ov} = \sqrt{6/150}$ = **0.2** V; full switching at **0.2828** V; pole $1/(2\pi \times 50 \times 200\ \text{fF})$ = **15.92** GHz; power **6** mW.

### Solution 12-01.14

$5/2.086$ = **2.397** standard deviations, so the fraction within ±5 mV is $2\Phi(2.397) - 1$ = **98.35**%: **1.65**% of parts fail a 5 mV limit, and they would be screened out at test.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 12-01.1a | g_m | 38.68 | mA/V |
| 12-01.1b | differential-output gain | 77.36 | — |
| 12-01.1c | single-ended gain | 38.68 | — |
| 12-01.1d | differential input resistance | 5.170 | kΩ |
| 12-01.2a | V_ov | 0.3162 | V |
| 12-01.2b | g_m | 0.3162 | mA/V |
| 12-01.2c | full-switching input | 0.4472 | V |
| 12-01.3a | i_C1 at 25 mV | 0.7245 | mA |
| 12-01.4a | single-ended CMRR | 100.5 | — |
| 12-01.4b | single-ended CMRR | 40.04 | dB |
| 12-01.5a | current difference | 31.22 | µA |
| 12-01.5b | i_D1 | 65.61 | µA |
| 12-01.5c | i_D2 | 34.39 | µA |
| 12-01.6a | V_ov | 0.3162 | V |
| 12-01.6b | V_IC,min | 1.066 | V |
| 12-01.6c | V_IC,max | 2.8 | V |
| 12-01.7a | load offset | 2.0 | mV |
| 12-01.7b | same-direction total | 3.5 | mV |
| 12-01.7c | RSS total | 2.5 | mV |
| 12-01.8a | exact offset | 1.261 | mV |
| 12-01.8b | linear offset | 1.293 | mV |
| 12-01.8c | drift | 4.204 | µV/K |
| 12-01.9a | differential CMRR | 20100 | — |
| 12-01.9b | differential CMRR | 86.06 | dB |
| 12-01.10a | undegenerated g_m | 19.34 | mA/V |
| 12-01.10b | degenerated transconductance | 1.813 | mA/V |
| 12-01.11a | gate area | 49 | µm² |
| 12-01.11b | C_gs | 326.7 | fF |
| 12-01.12a | 1% compression input, in V_ov | 0.2821 | — |
| 12-01.12b | 1% compression input | 89.22 | mV |
| 12-01.13a | tail current | 6 | mA |
| 12-01.13b | V_ov | 0.2 | V |
| 12-01.13c | full-switching input | 0.2828 | V |
| 12-01.13d | output pole | 15.92 | GHz |
| 12-01.13e | power | 6 | mW |
| 12-01.14a | limit in standard deviations | 2.397 | — |
| 12-01.14b | yield | 98.35 | % |
| 12-01.8d | linearization's overstatement | 2.5 | % |
| 12-01.10c | transconductance reduction | 10.67 | — |
| 12-01.14c | fraction failing | 1.65 | % |
