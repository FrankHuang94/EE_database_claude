# Solutions 10-08 · Current Sources and Current Mirrors

Problems: [10-08 problems](../problems/10-08-problems.md) · Chapter: [10-08](../chapters/10-08-current-sources-and-mirrors.md). Every number below is recomputed by [verify_10_08.py](../verify/verify_10_08.py).

---

## Solutions

### Solution 10-08.1

(a) $50 \times 30/10$ = **150** µA. (b) $150 \times 2$ = **300** µA, now sourced from the positive supply: an NMOS mirror sinks, a PMOS mirror sources, and chaining them converts one into the other.

### Solution 10-08.2

(a) Basic: $V_{ov}$ = **0.25** V. Simple cascode: $V_{TH} + 2V_{ov}$ = **0.95** V. Low-voltage cascode: $2V_{ov}$ = **0.5** V.

(b) $1.2 - 0.25 - 0.25$ = **0.7** V of swing.

(c) $1.2 - 0.95 - 0.25$ = **0** V: no room at all. On a 1.2 V supply a simple cascode is unusable; low-voltage cascodes (or no cascode, and gain from more stages) are the alternatives.

### Solution 10-08.3

The reference supplies $I_{C1}$ plus the base currents of Q1 ($I_{C1}/\beta$) and Q2 ($3I_{C1}/\beta$): $I_{ref} = I_{C1}(1 + 4/\beta)$, and $I_{out} = 3I_{C1}$. With β = 80: $3/1.05$ = **2.857** mA. Scaling up the output also scales up the base-current error.

### Solution 10-08.4

(a) $0.1 \times 0.5/2$ = **0.025** V⁻¹.

(b) $\lambda\Delta V$: **10**% at 0.5 µm and **2.5**% at 2 µm.

(c) $k_n \propto W/L$, so $W$ must grow 4×; the gate area $WL$ grows **16**×. Accuracy from longer channels is paid for in area (and capacitance).

### Solution 10-08.5

(a) $r_o + R_S + g_mr_oR_S = 10^6$: $R_S = 900\text{ kΩ}/(100 + 1)$ = **8.911** kΩ, costing $100\ \mu\text{A} \times 8.911\text{ kΩ}$ = **0.891** V of compliance.

(b) About $g_mr_o^2$ = **10** MΩ, ten times more, for about $V_{TH} + V_{ov}$ of extra compliance.

### Solution 10-08.6

$2r_o + (g_m + g_{mb})r_o^2$ = 200 kΩ + 12 MΩ = **12.2** MΩ.

### Solution 10-08.7

Basic: $200/(1 + 2/40)$ = **190.5** µA, **−4.76**%. With the helper: $200/(1 + 2/1640)$ = **199.76** µA, **−0.122**%.

### Solution 10-08.8

(a) $3.5/\sqrt4$ = **1.75** mV; $(2/0.15) \times 1.75$ mV = **2.333**%; 3σ = **7.0**%.

(b) σ = 0.333% needs $\sigma(\Delta V_{TH}) = 0.00333 \times 0.15/2$ = **0.25** mV and $WL = (3.5/0.25)^2$ = **196** µm².

### Solution 10-08.9

(a) Both gates share a voltage $V_G$, and each source sits at $IR_S$. For the output transistor, a threshold shift $\Delta V_{TH}$ changes its current by $\Delta I = g_m(-\Delta V_{TH} - \Delta I\,R_S)$, so $\Delta I = -g_m\Delta V_{TH}/(1 + g_mR_S)$. A resistor error $\Delta R$ shifts the source by $I\Delta R$: $\Delta I = g_m(-I\Delta R - \Delta I\,R_S)$, so $\Delta I/I = -[g_mR_S/(1 + g_mR_S)]\Delta R/R$.

(b) Without degeneration, **1.107**%. With $g_mR_S$ = 2, the threshold part falls to **0.369**% and the resistors add $(2/3) \times 0.1\%$ = **0.0667**%; the total (root-sum-square of independent terms) is **0.375**%. Resistors match better than thresholds, so degeneration shifts the burden to the better-matched element.

### Solution 10-08.10

Let each matched transistor carry collector current $I_C$ for Q1 and Q2 (they share $V_{BE}$), with base current $I_C/\beta$ each.

- Q3's emitter current feeds Q2's collector and the two bases: $I_{E3} = I_C + 2I_C/\beta = I_C(1 + 2/\beta)$.
- So Q3's collector (the output) is $I_{out} = \frac{\beta}{\beta + 1}I_C(1 + 2/\beta) = I_C\frac{\beta + 2}{\beta + 1}$, and its base current is $I_{out}/\beta$.
- At Q1's collector node, the reference supplies Q1's collector and Q3's base: $I_{ref} = I_C + I_{out}/\beta$.

Substituting $I_C = I_{out}(\beta + 1)/(\beta + 2)$:

$$
I_{ref} = I_{out}\left[\frac{\beta + 1}{\beta + 2} + \frac{1}{\beta}\right] = I_{out}\frac{\beta^2 + 2\beta + 2}{\beta(\beta + 2)} ,
$$

so $I_{out}/I_{ref} = (\beta^2 + 2\beta)/(\beta^2 + 2\beta + 2) = 1 - 2/(\beta^2 + 2\beta + 2)$. At β = 50 the error is **0.0769**%.

### Solution 10-08.11

(a) $9 \times 20$ µA = **180** µA, **0.216** mW.

(b) The block's effective $V_{GS}$ falls by 5 mV, and $\Delta I/I = (2/V_{ov})\Delta V$ = **5.0**%. A current, by contrast, arrives intact at any ground potential: the block's own diode-connected transistor regenerates the right $V_{GS}$ locally.

### Solution 10-08.12

$1/(V_{DD} - V_{GS}) = 1/1.1$ V = **90.9**%/V, so 90 mV moves the reference by about **8.18**%. (The diode's own $V_{GS}$ rise makes the exact value slightly smaller, as in Example 10-08.7.) A resistor reference on a low supply is very supply-sensitive.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 10-08.1a | NMOS output | 150 | µA |
| 10-08.1b | PMOS output | 300 | µA |
| 10-08.2a | basic compliance | 0.25 | V |
| 10-08.2b | simple cascode compliance | 0.95 | V |
| 10-08.2c | low-voltage cascode compliance | 0.5 | V |
| 10-08.2d | swing, basic mirrors | 0.7 | V |
| 10-08.2e | swing, NMOS cascode | 0 | V |
| 10-08.3a | output current | 2.857 | mA |
| 10-08.4a | λ at 2 µm | 0.025 | 1/V |
| 10-08.4b | error at 0.5 µm | 10 | % |
| 10-08.4c | error at 2 µm | 2.5 | % |
| 10-08.4d | area factor | 16 | — |
| 10-08.5a | R_S | 8.911 | kΩ |
| 10-08.5b | compliance cost | 0.891 | V |
| 10-08.5c | cascode R_out | 10 | MΩ |
| 10-08.6a | cascode R_out with body effect | 12.2 | MΩ |
| 10-08.7a | basic output | 190.5 | µA |
| 10-08.7b | basic error | -4.76 | % |
| 10-08.7c | helper output | 199.76 | µA |
| 10-08.7d | helper error | -0.122 | % |
| 10-08.8a | σ(ΔV_TH) | 1.75 | mV |
| 10-08.8b | σ(ΔI/I) | 2.333 | % |
| 10-08.8c | 3σ error | 7.0 | % |
| 10-08.8d | σ(ΔV_TH) needed | 0.25 | mV |
| 10-08.8e | area for 1% at 3σ | 196 | µm² |
| 10-08.9a | σ(ΔI/I) without degeneration | 1.107 | % |
| 10-08.9b | threshold part with degeneration | 0.369 | % |
| 10-08.9c | resistor part | 0.0667 | % |
| 10-08.9d | total | 0.375 | % |
| 10-08.10a | Wilson error at β = 50 | 0.0769 | % |
| 10-08.11a | total bias current | 180 | µA |
| 10-08.11b | bias power | 0.216 | mW |
| 10-08.11c | current change from 5 mV | 5.0 | % |
| 10-08.12a | supply sensitivity | 90.9 | %/V |
| 10-08.12b | change for 90 mV | 8.18 | % |
