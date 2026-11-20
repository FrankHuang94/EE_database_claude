# Solutions 12-02 · Active Loads, Cascodes and Multistage Amplifiers

Problems: [12-02 problems](../problems/12-02-problems.md) · Chapter: [12-02](../chapters/12-02-active-loads-cascodes-multistage.md). Every number below is recomputed by [verify_12_02.py](../verify/verify_12_02.py), which solves each small-signal circuit by nodal analysis rather than reusing these formulas.

---

## Solutions

### Solution 12-02.1

$g_mr_o = (2I_D/V_{ov})\cdot 1/(\lambda I_D) = 2/(\lambda V_{ov}) = 2/(0.2 \times 0.15)$ = **66.67**. A short channel and a small overdrive still give only tens.

### Solution 12-02.2

$g_m = 2 \times 50\ \mu\text{A}/0.25\ \text{V}$ = **0.4** mA/V. $r_{on} = 1/(0.1 \times 50\ \mu\text{A})$ = **200** kΩ and $r_{op} = 1/(0.15 \times 50\ \mu\text{A})$ = **133.3** kΩ, in parallel **80** kΩ. Gain $0.4\ \text{mA/V} \times 80\ \text{k}\Omega$ = **32**. The leakier PMOS sets most of the output resistance.

### Solution 12-02.3

$R_{out} = r_{o1} + r_{o2} + g_{m2}r_{o2}r_{o1} = 20 + 20 + 2 \times 20 \times 20$ kΩ = **840** kΩ: 42 times one device's $r_o$.

### Solution 12-02.4

Each side carries 50 µA: $g_m = 2 \times 50\ \mu\text{A}/0.2\ \text{V}$ = **0.5** mA/V and $r_o = 1/(0.2 \times 50\ \mu\text{A})$ = **100** kΩ. $A_d = g_m(r_{o2} \parallel r_{o4}) = 0.5\ \text{mA/V} \times 50\ \text{k}\Omega$ = **25**, or **27.96** dB. The short-circuit output current is $g_mv_{id}$ = **1** µA for 2 mV: both halves' signal currents reach the output through the mirror.

### Solution 12-02.5

The tail carries 100 µA: $R_{SS} = 1/(0.2 \times 100\ \mu\text{A})$ = **50** kΩ. $\lvert A_{cm}\rvert \approx 1/(2g_{m3}R_{SS}) = 1/(2 \times 0.5\ \text{mA/V} \times 50\ \text{k}\Omega)$ = **0.02**, so CMRR ≈ 25/0.02 = **1250**, or **61.94** dB. Raising $R_{SS}$ twentyfold divides $A_{cm}$ by 20 and adds $20\log_{10}20$ = **26.02** dB, giving **87.96** dB.

### Solution 12-02.6

With an ideal current-source load the output carries no small-signal current, so neither does M2, and since M2's source current is M1's drain current, M1 carries none either. M1: $g_{m1}v_{in} + v_x/r_{o1} = 0$, so $v_x = -g_{m1}r_{o1}v_{in}$. M2, with its gate grounded: $g_{m2}(0 - v_x) + (v_{out} - v_x)/r_{o2} = 0$, so $v_{out} = v_x(1 + g_{m2}r_{o2})$. Together, $A = -g_{m1}r_{o1}(1 + g_{m2}r_{o2})$. With $g_mr_o$ = 50: $50 \times 51$ = **2550**.

### Solution 12-02.7

Telescopic: five overdrives per side, $1.2 - 5 \times 0.15$ = **0.45** V per output, and the antiphase outputs give a differential **0.9** V peak to peak. Two-stage: the output stage needs one overdrive from each rail, $1.2 - 2 \times 0.15$ = **0.9** V per side, twice the telescopic swing. At low supply voltages this is why two-stage (or folded) designs win.

### Solution 12-02.8

Stage 1 drives its own 50 kΩ in parallel with stage 2's 50 kΩ input: $A_1 = 1\ \text{mA/V} \times 25\ \text{k}\Omega$ = **25**. Stage 2: $A_2 = 40\ \text{mA/V} \times 10\ \text{k}\Omega$ = **400**. Total **10 000**, or **80** dB. With an infinite input resistance, $A_1$ would be 50 and the total **20 000**: the loading costs a factor of 2 (**6.02** dB).

### Solution 12-02.9

Refer each offset to the input by dividing by the gain before it: $2 + 10/20 + 20/(20 \times 50) = 2 + 0.5 + 0.02$ = **2.52** mV if they add. Independent: $\sqrt{2^2 + 0.5^2 + 0.02^2}$ = **2.062** mV. The first stage dominates either way.

### Solution 12-02.10

$V_{ov} = \sqrt{2I/k_n} = \sqrt{2 \times 50\ \mu\text{A}/2\ \text{mA/V}^2}$ = **0.2236** V, so the shift is $V_{GS} = 0.5 + 0.2236$ = **0.7236** V. With the threshold raised to 0.6 V by body effect, **0.8236** V: the source's rise above the body increases the shift, which the designer must include.

### Solution 12-02.11

M6 must carry 450 µA instead of the 400 µA it would carry at $V_{SG6} = V_{SG4}$, so $V_{SG6}$ must rise by $\Delta I/g_{m6} = 50\ \mu\text{A}/(4\ \text{mA/V})$ = **12.5** mV; the first stage's output must move down by that much, which requires an input imbalance of $12.5\ \text{mV}/50$ = **0.25** mV. The cure is to make the second stage's current ratio equal its width ratio: here, a 400 µA sink.

### Solution 12-02.12

(a) $g_m(r_o \parallel r_o) = 1\ \text{mA/V} \times 10\ \text{k}\Omega$ = **10**, with 2 overdrives (0.3 V) of headroom.

(b) The cascode has $R_{out} = 20 + 20 + 1 \times 20 \times 20$ kΩ = **440** kΩ and short-circuit transconductance $G_m = g_mr_o(1 + g_mr_o)/R_{out} = 20 \times 21/440\ \text{k}\Omega$ = **0.9545** mA/V. With the simple load: $0.9545\ \text{mA/V} \times (440\ \text{k}\Omega \parallel 20\ \text{k}\Omega)$ = **18.26**, with 3 overdrives (0.45 V).

(c) With a cascode load: $0.9545\ \text{mA/V} \times 220\ \text{k}\Omega$ = **210**, or **46.44** dB, with 4 overdrives (**0.6** V).

Per volt of headroom: 10/0.3 = **33.3**, 18.26/0.45 = **40.6** and 210/0.6 = **350** per volt. Cascoding both sides gives by far the most gain per volt, as long as the supply has room for the fourth overdrive.

### Solution 12-02.13

(a) The diode transistor's collector carries $I$ while the node also feeds two base currents, so the copy is $I/(1 + 2/\beta)$: short by $1 - 1/1.02$ = **1.961**%. The output balances only when the input pair delivers that much less current to the mirror side than to the output side: $I_{C1}/I_{C2} = 1 + 2/\beta$, so $v_{id} = V_T\ln(1.02)$ = **0.5119** mV of systematic offset; the estimate $2V_T/\beta$ gives **0.5170** mV.

(b) $g_m = 100\ \mu\text{A}/25.852\ \text{mV}$ = 3.868 mA/V and $r_\pi = \beta/g_m$ = 25.85 kΩ. The emitter of the cascode device sees $r_{o1} \parallel r_{\pi2}$ = 20.54 kΩ, because the base current returns signal to AC ground through $r_\pi$. So $R_{out} = r_{o2} + (r_{o1} \parallel r_{\pi2})(1 + g_{m2}r_{o2})$ = **8.066** MΩ, close to $\beta r_o$ = **10** MΩ and far below the MOS-style $g_mr_o^2$ = **38.68** MΩ.

### Solution 12-02.14

Each half is a cascode with a cascode load: $G_m = g_mr_o(1 + g_mr_o)/R_{out}$ and $R_{out} = 2r_o + g_mr_o^2$ for each side, so $A_d = G_m(R_{out}/2) = g_mr_o(1 + g_mr_o)/2 = 50 \times 51/2$ = **1275**, or **62.11** dB. Each output can move over $1.5 - 5 \times 0.15$ = **0.75** V, so the differential output swings **1.5** V peak to peak.

### Solution 12-02.15

With matched halves the output equals the diode node: $V_{DD} - V_{SG3} = 1.8 - (0.5 + 0.25)$ = **1.05** V. The lowest input common mode keeps the tail saturated: $V_{TN} + V_{ov} + V_{ov,t}$ = **0.9** V. The highest keeps M1 saturated with its drain at 1.05 V: $V_{IC} \le 1.05 + V_{TN}$ = **1.55** V.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 12-02.1a | intrinsic gain | 66.67 | — |
| 12-02.2a | g_m | 0.4 | mA/V |
| 12-02.2b | r_o, NMOS | 200 | kΩ |
| 12-02.2c | r_o, PMOS | 133.3 | kΩ |
| 12-02.2d | output resistance | 80 | kΩ |
| 12-02.2e | gain | 32 | — |
| 12-02.3a | output resistance | 840 | kΩ |
| 12-02.3b | ratio to one r_o | 42 | — |
| 12-02.4a | g_m | 0.5 | mA/V |
| 12-02.4b | r_o | 100 | kΩ |
| 12-02.4c | differential gain | 25 | — |
| 12-02.4d | differential gain | 27.96 | dB |
| 12-02.4e | output current for 2 mV | 1 | µA |
| 12-02.5a | tail resistance | 50 | kΩ |
| 12-02.5b | common-mode gain | 0.02 | — |
| 12-02.5c | CMRR | 1250 | — |
| 12-02.5d | CMRR | 61.94 | dB |
| 12-02.5e | improvement from a 20× tail | 26.02 | dB |
| 12-02.5f | CMRR with the cascode tail | 87.96 | dB |
| 12-02.6a | cascode gain | 2550 | — |
| 12-02.7a | telescopic swing per output | 0.45 | V |
| 12-02.7b | telescopic differential peak-to-peak | 0.9 | V |
| 12-02.7c | two-stage swing per output | 0.9 | V |
| 12-02.8a | loaded first-stage gain | 25 | — |
| 12-02.8b | second-stage gain | 400 | — |
| 12-02.8c | total gain | 10000 | — |
| 12-02.8d | total gain | 80 | dB |
| 12-02.8e | total gain without loading | 20000 | — |
| 12-02.8f | loss from loading | 6.02 | dB |
| 12-02.9a | offset, all adding | 2.52 | mV |
| 12-02.9b | offset, independent | 2.062 | mV |
| 12-02.10a | overdrive | 0.2236 | V |
| 12-02.10b | level shift | 0.7236 | V |
| 12-02.10c | level shift with body effect | 0.8236 | V |
| 12-02.11a | first-stage output shift | 12.5 | mV |
| 12-02.11b | systematic offset | 0.25 | mV |
| 12-02.12a | CS gain, simple load | 10 | — |
| 12-02.12b | cascode output resistance | 440 | kΩ |
| 12-02.12c | cascode transconductance | 0.9545 | mA/V |
| 12-02.12d | cascode gain, simple load | 18.26 | — |
| 12-02.12e | cascode gain, cascode load | 210 | — |
| 12-02.12f | cascode gain, cascode load | 46.44 | dB |
| 12-02.12g | headroom, cascode with cascode load | 0.6 | V |
| 12-02.12h | gain per volt, cascode with cascode load | 350 | 1/V |
| 12-02.12i | gain per volt, simple CS | 33.3 | 1/V |
| 12-02.12j | gain per volt, cascode with simple load | 40.6 | 1/V |
| 12-02.13a | mirror shortfall | 1.961 | % |
| 12-02.13b | systematic offset | 0.5119 | mV |
| 12-02.13c | estimate 2V_T/β | 0.5170 | mV |
| 12-02.13d | bipolar cascode output resistance | 8.066 | MΩ |
| 12-02.13e | βr_o | 10 | MΩ |
| 12-02.13f | g_m r_o² | 38.68 | MΩ |
| 12-02.14a | differential gain | 1275 | — |
| 12-02.14b | differential gain | 62.11 | dB |
| 12-02.14c | swing per output | 0.75 | V |
| 12-02.14d | differential swing | 1.5 | V |
| 12-02.15a | output DC level | 1.05 | V |
| 12-02.15b | lowest input common mode | 0.9 | V |
| 12-02.15c | highest input common mode | 1.55 | V |
