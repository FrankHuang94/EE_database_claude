# Solutions 10-02 · MOSFET DC Operation and Biasing

Problems: [10-02 problems](../problems/10-02-problems.md) · Chapter: [10-02](../chapters/10-02-mosfet-dc-operation-and-biasing.md). Every number below is recomputed by [verify_10_02.py](../verify/verify_10_02.py), which solves each circuit by root finding on the full three-region model and reads the region off the solution.

---

## Solutions

### Solution 10-02.1

(a) Cutoff: $V_{GS} < V_{TN}$. (b) Triode: $V_{ov}$ = 0.5 V exceeds $V_{DS}$ = 0.3 V. (c) Saturation: $V_{DS}$ = 0.8 V ≥ 0.5 V. (d) Triode: $V_{SG} - |V_{TP}|$ = 0.7 V exceeds $V_{SD}$ = 0.5 V.

### Solution 10-02.2

$V_{ov}$ = 0.5 V. Assuming saturation, $I_D = \tfrac12 \times 1 \times 0.25$ = **0.125** mA and $V_D = 1.8 - 5 \times 0.125$ = **1.175** V ≥ 0.5 V: saturation confirmed. The largest $R_D$ puts $V_D$ at 0.5 V: $(1.8 - 0.5)/0.125$ = **10.4** kΩ.

### Solution 10-02.3

$V_{SG}$ = 1.0 V, so the overdrive is **0.55** V and $I_D = \tfrac12 \times 0.5 \times 0.55^2$ = **0.0756** mA. $V_D = 2 \times 0.0756$ = **0.151** V and $V_{SD}$ = **1.649** V ≥ 0.55 V: saturation.

### Solution 10-02.4

(a) $V_{ov} = \sqrt{2I_D/k_n}$ = **0.707** V, $V_{GS}$ = **1.207** V and $V_G = V_{GS} + I_DR_S$ = **2.207** V.

(b) $V_D \ge V_S + 1.5$ = 2.5 V, so $R_D \le (5 - 2.5)/0.5$ = **5.0** kΩ.

(c) $R_2 = 1\text{ MΩ} \times 2.207/5$ = **441.4** kΩ to ground and $R_1$ = **558.6** kΩ to the supply.

### Solution 10-02.5

(a) $g_m = k_nV_{ov}$ = **1.414** mS and $1 + g_mR_S$ = **3.83**.

(b) Without $R_S$: $2 \times 0.04/0.707$ = **11.3**%. With it: **2.96**%.

(c) **0.5148** mA and **0.4853** mA, about ±3%, as predicted.

### Solution 10-02.6

(a) $V_{DS} = V_{GS}$, which always exceeds $V_{ov} = V_{GS} - V_{TN}$.

(b) $(3.3 - V)/10\text{ kΩ} = \tfrac12 \times 1\text{ mA/V}^2(V - 0.5)^2$ gives $V_{GS}$ = **1.155** V and $I_D$ = **0.2145** mA.

(c) **0.2188** mA and **0.2102** mA, about ±2%: the resistor carries most of the supply, so the current depends only weakly on the threshold.

### Solution 10-02.7

(a) $V_{GS}$ = **1.045** V, $I_{ref} = (5 - V_{GS})/20\text{ kΩ}$ = **0.1978** mA and $I_{D2} = 3I_{ref}$ = **0.5933** mA.

(b) With $(1 + \lambda V_{GS})$ for M1: $V_{GS}$ = **1.034** V and $I_{ref}$ = **0.1983** mA. M2 at 3 V: $I_{D2}$ = **0.6505** mA, **9.35**% above $3I_{ref}$.

### Solution 10-02.8

$R_{on} \le 50\text{ mV}/1\text{ A}$ = **50** mΩ. $W/L = 1/(R_{on}k_n'V_{ov}) = 1/(0.05 \times 200\times10^{-6} \times 2.7)$ = **37,037**, so $W$ = **18.5** mm at $L$ = 0.5 µm. Loss $I^2R_{on}$ = **50** mW. (Wide switches are laid out as many parallel fingers.)

### Solution 10-02.9

$30^2 \times 1.19$ mΩ = **1.071** W typical, $30^2 \times 1.45$ mΩ = **1.305** W maximum, and **1.96** W with the hot-junction factor. Design the heat path for the last number.

### Solution 10-02.10

(a) Solving $V_S = 10\text{ kΩ} \times \tfrac12k_n(3 - V_S - V_{TN}(V_S))^2$: $V_S$ = **1.605** V, $V_{TN}$ = **0.828** V and $I_D$ = **0.1605** mA.

(b) Without the body effect: $V_S$ = **1.886** V and $I_D$ = **0.1886** mA.

(c) $V_G - V_S$ = **1.395** V with the body effect and **1.114** V without. A follower's drop is $V_{TN} + V_{ov}$, not $V_{TN0}$: the overdrive needed to carry the current adds to it, and the body effect raises the threshold as the source rises.

### Solution 10-02.11

(a) $\sigma_I/I = 2\sigma_{V_T}/V_{ov} \le 0.05$ needs $V_{ov} \ge 2 \times 0.02/0.05$ = **0.8** V, so $k_n = 2I_D/V_{ov}^2$ = **0.625** mA/V².

(b) At $V_{ov}$ = 0.2 V, $g_m = 2I_D/V_{ov}$ = **2.0** mS, and $1 + g_mR_S$ = **11**: σ = **1.82**% with the resistor, against **20**% without. Degeneration buys stability without forcing a large overdrive, at the cost of 1 V of headroom across $R_S$.

### Solution 10-02.12

(a) $R_{on} = 1/[k_p(V_{SG} - |V_{TP}|)] = 1/(2 \times 2.5)$ = **0.2** Ω.

(b) **0.2** V and **0.2** W.

(c) A PMOS on the high side turns on with its gate pulled to ground, a voltage the system already has. An NMOS there would need its gate driven *above* the rail (a charge pump or bootstrap), though for the same size it would have two to three times lower resistance because electrons are more mobile. Load switches and ideal-diode controllers (10-01) include such charge pumps so they can use NMOS.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 10-02.2a | I_D | 0.125 | mA |
| 10-02.2b | V_D | 1.175 | V |
| 10-02.2c | largest R_D | 10.4 | kΩ |
| 10-02.3a | overdrive | 0.55 | V |
| 10-02.3b | I_D | 0.0756 | mA |
| 10-02.3c | V_D | 0.151 | V |
| 10-02.3d | V_SD | 1.649 | V |
| 10-02.4a | V_ov | 0.707 | V |
| 10-02.4b | V_GS | 1.207 | V |
| 10-02.4c | V_G | 2.207 | V |
| 10-02.4d | largest R_D | 5.0 | kΩ |
| 10-02.4e | R_2 | 441.4 | kΩ |
| 10-02.4f | R_1 | 558.6 | kΩ |
| 10-02.5a | g_m | 1.414 | mS |
| 10-02.5b | degeneration factor | 3.83 | — |
| 10-02.5c | sensitivity without R_S | 11.3 | % |
| 10-02.5d | sensitivity with R_S | 2.96 | % |
| 10-02.5e | I_D at V_TN 0.46 V | 0.5148 | mA |
| 10-02.5f | I_D at V_TN 0.54 V | 0.4853 | mA |
| 10-02.6a | V_GS | 1.155 | V |
| 10-02.6b | I_D | 0.2145 | mA |
| 10-02.6c | I_D at V_TN 0.45 V | 0.2188 | mA |
| 10-02.6d | I_D at V_TN 0.55 V | 0.2102 | mA |
| 10-02.7a | V_GS, λ = 0 | 1.045 | V |
| 10-02.7b | I_ref, λ = 0 | 0.1978 | mA |
| 10-02.7c | I_D2, λ = 0 | 0.5933 | mA |
| 10-02.7d | V_GS, λ = 0.05 | 1.034 | V |
| 10-02.7e | I_ref, λ = 0.05 | 0.1983 | mA |
| 10-02.7f | I_D2, λ = 0.05 | 0.6505 | mA |
| 10-02.7g | mirror error | 9.35 | % |
| 10-02.8a | required R_on | 50 | mΩ |
| 10-02.8b | W/L | 37037 | — |
| 10-02.8c | width | 18.5 | mm |
| 10-02.8d | conduction loss | 50 | mW |
| 10-02.9a | loss, typical | 1.071 | W |
| 10-02.9b | loss, maximum | 1.305 | W |
| 10-02.9c | loss, maximum when hot | 1.96 | W |
| 10-02.10a | V_S with body effect | 1.605 | V |
| 10-02.10b | V_TN with body effect | 0.828 | V |
| 10-02.10c | I_D with body effect | 0.1605 | mA |
| 10-02.10d | V_S without | 1.886 | V |
| 10-02.10e | I_D without | 0.1886 | mA |
| 10-02.10f | V_G − V_S with body effect | 1.395 | V |
| 10-02.10g | V_G − V_S without | 1.114 | V |
| 10-02.11a | minimum overdrive | 0.8 | V |
| 10-02.11b | k_n | 0.625 | mA/V² |
| 10-02.11c | g_m at 0.2 V | 2.0 | mS |
| 10-02.11d | degeneration factor | 11 | — |
| 10-02.11e | σ with R_S | 1.82 | % |
| 10-02.11f | σ without R_S | 20 | % |
| 10-02.12a | R_on | 0.2 | Ω |
| 10-02.12b | drop at 1 A | 0.2 | V |
| 10-02.12c | loss at 1 A | 0.2 | W |
