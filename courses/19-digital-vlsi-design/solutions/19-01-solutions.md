# Solutions 19-01 · The CMOS Inverter: Static Characteristics

Problems: [19-01 problem set](../problems/19-01-problems.md) · Chapter: [19-01](../chapters/19-01-cmos-inverter-static.md). Every number below is recomputed by [verify_19_01.py](../verify/verify_19_01.py).

---

## Solutions

### Solution 19-01.1

(a) $V_{in}$ = 0.2 V < $V_{TN}$: the NMOS is **off**, the PMOS is **linear** with zero current, and $V_{out}$ = **1.0** V exactly (region A).

(b) $V_{in}$ = 0.5 V is $V_M$ of the symmetric inverter, $(0.3 + 1.0 - 0.3)/2$ = **0.5** V. Both transistors are **saturated** (region C); with λ = 0 the output can sit anywhere between $V_{in} - V_{TN}$ = 0.2 V and $V_{in} + \lvert V_{TP}\rvert$ = 0.8 V, so it is not exact (the curve is vertical there).

(c) $V_{in}$ = 0.8 V > $V_{DD} - \lvert V_{TP}\rvert$ = 0.7 V: the PMOS is **off**, the NMOS **linear** with zero current, and $V_{out}$ = **0** V exactly (region E).

### Solution 19-01.2

$\sqrt3$ = 1.732: $V_M = (0.5 \times 1.732 + 1.8 - 0.5)/(1 + 1.732) = 2.166/2.732$ = **0.793** V, below the midpoint because the NMOS is stronger.

### Solution 19-01.3

$r = ((1.8 - 0.5 - 0.9)/(0.9 - 0.45))^2 = (0.4/0.45)^2$ = **0.790**, and $W_p/W_n = 2.8/0.790$ = **3.54**.

### Solution 19-01.4

$V_{IL} = (3 \times 1.8 + 2 \times 0.45)/8$ = **0.7875** V and $V_{IH} = (5 \times 1.8 - 0.9)/8$ = **1.0125** V, so $NM_L = NM_H$ = **0.7875** V. The region of gain is $V_{IH} - V_{IL} = (V_{DD} - 2V_T)/4$ = **0.225** V wide.

### Solution 19-01.5

$V_M = (0.45 \times 2 + 1.35)/3$ = **0.75** V. With $r$ = 4: $t = (2\sqrt{16 + 12} - 4)/(4 \times 8) = (10.583 - 4)/32 = 0.2057$, $t/(1 + t) = 0.1706$, so $V_{IL} = 0.45 + 0.1706 \times 0.9$ = **0.604** V. For $V_{IH}$, $r' = 0.25$: $t' = (2\sqrt{0.0625 + 0.75} - 0.25)/(0.25 \times 4.25) = 1.5528/1.0625 = 1.4615$, $t'/(1 + t') = 0.5937$, $V_{IL}' = 0.45 + 0.5937 \times 0.9 = 0.9844$, so $V_{IH} = 1.8 - 0.9844$ = **0.816** V. The margins are $NM_L$ = **0.604** V and $NM_H$ = **0.984** V. The low margin limits the gate: it is 0.18 V below the symmetric inverter's.

### Solution 19-01.6

(a) With $V_{ov}$ = 0.25 V for both and $g_{ds} \approx \lambda I_D$: $\lvert A_v\rvert \approx 2(1/0.25 + 1/0.25)/(0.15 + 0.2)$ = **45.7**.

(b) Solving the full model numerically: $V_M$ = **0.6017** V and $\lvert A_v\rvert$ = **50.6**. The approximation is about 10% low, mostly from the $(1 + \lambda V_{DS})$ factors.

(c) At $V_{out} = V_{in}$ = 0.6 V the two transistors have equal overdrives and equal $V_{DS}$, so the PMOS, with the larger λ, carries more current; the balance needs a slightly higher input, which strengthens the NMOS and weakens the PMOS.

### Solution 19-01.7

$\partial V_M/\partial V_{TN} = \sqrt r/(1 + \sqrt r)$ and $\partial V_M/\partial\lvert V_{TP}\rvert = -1/(1 + \sqrt r)$.

(a) $r$ = 1: **0.5** and **−0.5**; $\sigma_{V_M} = 25\sqrt{0.25 + 0.25}$ = **17.7** mV.

(b) $r$ = 4: **0.667** and **−0.333**; $\sigma_{V_M} = 25\sqrt{0.444 + 0.111}$ = **18.6** mV. A strong NMOS makes $V_M$ follow the NMOS threshold more closely.

### Solution 19-01.8

The first stage's output is **1.119** V: 0.55 V is 50 mV below $V_M$ = 0.6 V, and the high gain pushes the output most of the way up. That level, 1.119 V, is above $V_{DD} - \lvert V_{TP}\rvert$ = 0.85 V, so in the second stage the PMOS is **off** and the output is exactly **0** V (region E); from then on the levels are exact rails. Two stages restored a level that started 50 mV from the switching threshold.

### Solution 19-01.9

At $V_M$ both transistors are saturated with $V_{ov}$ = 0.25 V: $I = \tfrac12 \times 200\ \mu\text{A/V}^2 \times 0.25^2$ = **6.25** µA. The current is zero for $V_{in} < V_{TN}$ and $V_{in} > V_{DD} - \lvert V_{TP}\rvert$ (regions A and E), so a static gate draws it only while its input is between levels. This **short-circuit current** flows briefly during every input transition (19-06).

### Solution 19-01.10

The derivation is that of §3.3: differentiating the region-B balance $\tfrac r2b^2 = au - u^2/2$ at slope −1 gives $u = (a - rb)/2$, and substituting gives $(r^2 + 4r)b^2 + 2rab - 3a^2 = 0$, whose positive root in $t = b/a$ is the stated $t$. Since $a + b = V_{DD} - V_{TN} - \lvert V_{TP}\rvert$, $b = \tfrac{t}{1 + t}(a + b)$. For $r$ = 1, $t = 3/5$ and $t/(1 + t) = 3/8$, so $V_{IL} = V_T + \tfrac38(V_{DD} - 2V_T) = (3V_{DD} + 2V_T)/8$.

For $r$ = 2: $t = (2\sqrt{10} - 2)/12$ = **0.360**, $t/(1 + t) = 0.2650$, and $V_{IL} = 0.3 + 0.2650 \times 0.4$ = **0.406** V.

### Solution 19-01.11

$V_M$ = 0.5 V needs $r = ((1.0 - 0.35 - 0.5)/(0.5 - 0.3))^\alpha = 0.75^\alpha$.

(a) α = 2: $r$ = 0.5625 and $W_p/W_n = 1.8/0.5625$ = **3.20**.

(b) α = 1.4: $r = 0.75^{1.4}$ = 0.6685 and $W_p/W_n = 1.8/0.6685$ = **2.69**.

With a smaller α the current depends less steeply on the overdrive, so the PMOS's smaller overdrive (0.15 V against the NMOS's 0.20 V) costs it less current, and less extra width compensates.

### Solution 19-01.12

(a) $(e^{V_{DD}/2V_T} - 1)/1.3 = 10$ gives $e^{V_{DD}/2V_T} = 14$ and $V_{DD} = 2 \times 25.85\ \text{mV} \times \ln 14$ = **136** mV.

(b) At 300 K, $2 \times 25.85\ \text{mV} \times \ln 2.3$ = **43.1** mV. At 85 °C (358.15 K) $V_T$ = 30.86 mV, so $V_{DD,min}$ = **51.4** mV: the floor rises in proportion to absolute temperature.

(c) Gain above 1 is only the threshold of regeneration. Real circuits need noise margins against supply noise and crosstalk, enough current to meet a speed target (subthreshold current is tiny), and robustness to variation, which in subthreshold changes currents exponentially: a threshold shift of $nV_T\ln 10 \approx$ 80 mV changes a transistor's current tenfold. Designs therefore run at a few hundred millivolts.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 19-01.1a | output at 0.2 V | 1.0 | V |
| 19-01.1b | V_M of the symmetric inverter | 0.5 | V |
| 19-01.1c | output at 0.8 V | 0 | V |
| 19-01.2a | switching threshold | 0.793 | V |
| 19-01.3a | required kn/kp | 0.790 | — |
| 19-01.3b | required Wp/Wn | 3.54 | — |
| 19-01.4a | V_IL | 0.7875 | V |
| 19-01.4b | V_IH | 1.0125 | V |
| 19-01.4c | noise margins | 0.7875 | V |
| 19-01.4d | width of the gain region | 0.225 | V |
| 19-01.5a | V_M, r = 4 | 0.75 | V |
| 19-01.5b | V_IL, r = 4 | 0.604 | V |
| 19-01.5c | V_IH, r = 4 | 0.816 | V |
| 19-01.5d | NM_L, r = 4 | 0.604 | V |
| 19-01.5e | NM_H, r = 4 | 0.984 | V |
| 19-01.6a | approximate gain magnitude | 45.7 | — |
| 19-01.6b | numerical V_M | 0.6017 | V |
| 19-01.6c | numerical gain magnitude | 50.6 | — |
| 19-01.7a | dV_M/dV_TN, r = 1 | 0.5 | — |
| 19-01.7b | dV_M by d(abs V_TP), r = 1 | -0.5 | — |
| 19-01.7c | sigma of V_M, r = 1 | 17.7 | mV |
| 19-01.7d | dV_M/dV_TN, r = 4 | 0.667 | — |
| 19-01.7e | dV_M by d(abs V_TP), r = 4 | -0.333 | — |
| 19-01.7f | sigma of V_M, r = 4 | 18.6 | mV |
| 19-01.8a | first stage output | 1.119 | V |
| 19-01.8b | second stage output | 0 | V |
| 19-01.9a | through-current at V_M | 6.25 | µA |
| 19-01.10a | t for r = 2 | 0.360 | — |
| 19-01.10b | V_IL for r = 2 | 0.406 | V |
| 19-01.11a | Wp/Wn, square law | 3.20 | — |
| 19-01.11b | Wp/Wn, alpha = 1.4 | 2.69 | — |
| 19-01.12a | supply for a gain of 10 | 136 | mV |
| 19-01.12b | minimum supply, 300 K | 43.1 | mV |
| 19-01.12c | minimum supply, 85 °C | 51.4 | mV |
