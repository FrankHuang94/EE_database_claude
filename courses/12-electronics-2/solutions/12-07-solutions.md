# Solutions 12-07 · Output Stages and Power Amplifiers

Problems: [12-07 problems](../problems/12-07-problems.md) · Chapter: [12-07](../chapters/12-07-output-stages.md). Every number below is recomputed by [verify_12_07.py](../verify/verify_12_07.py), which integrates the device currents over a cycle and solves the device equations numerically rather than reusing these formulas.

---

## Solutions

### Solution 12-07.1

The supply power stays at $2V_{CC}^2/R_L$ while the load power falls with the square of the amplitude: $\eta = 25\% \times (1/2)^2$ = **6.25**%.

### Solution 12-07.2

$P_L = 12^2/(2 \times 4)$ = **18** W. $P_S = 2 \times 12 \times 12/(4\pi)$ = **22.92** W, and η = **78.54**%.

### Solution 12-07.3

$V_{op} = 2 \times 20/\pi$ = **12.73** V. $P_{D,max} = 2 \times 400/(8\pi^2)$ = **10.13** W in total, **5.066** W per transistor.

### Solution 12-07.4

Full negative swing needs $I_Q = V_{CC}/R_L$ = **100** mA. $P_S = 2 \times 5\ \text{V} \times 0.1\ \text{A}$ = **1** W, and $P_{L,max} = 25/100$ = **0.25** W: 25% at best.

### Solution 12-07.5

One third of the power means $V_{op} = V_{CC}/\sqrt3$, so $\eta = (\pi/4)/\sqrt3$ = **45.34**%.

### Solution 12-07.6

The op-amp needs to move its own input by only $0.7\ \text{V}/10^5$ = **7** µV to drive the stage across the dead band, so the input-referred dead band shrinks to ±7 µV. At high frequency the op-amp's gain falls (12-05 §3.3), so the input-referred dead band grows; and while the stage is cut off the loop is open, so the op-amp's output must slew across the 1.4 V gap at every zero crossing, which takes longer than a high-frequency signal allows.

### Solution 12-07.7

$i_N = 100 + \sqrt{100^2 + 10^2}$ mA = **200.50** mA and $i_P = i_N - 200$ = **0.4988** mA. At idle, $R_{out} = V_T/(2I_Q)$ = **1.293** Ω.

### Solution 12-07.8

$R_2 = 0.6\ \text{V}/1\ \text{mA}$ = **600** Ω. $V_{BB} = 0.6(1 + R_1/R_2) = 1.25$ gives $R_1/R_2$ = 1.0833 and $R_1$ = **650** Ω. The temperature coefficient is $-2\ \text{mV/°C} \times 1.25/0.6$ = **−4.167** mV/°C, about what two output $V_{BE}$s need.

### Solution 12-07.9

$\theta_{total} \le (150 - 50)/20$ = 5 °C/W, so $\theta_{SA} \le 5 - 1.0 - 0.3$ = **3.7** °C/W.

### Solution 12-07.10

$g_m = 200\ \text{mA}/25.852\ \text{mV}$ = **7.736** A/V, and $L = 20 \times 8 \times 7.736 \times 0.002$ = **2.476**: unstable. For $L$ = 0.5, $1 + g_mR_E = 2.476/0.5$ = 4.951, so $R_E \ge 3.951/7.736$ = **0.5107** Ω.

### Solution 12-07.11

At 50 W, $I_{rms} = \sqrt{50/8}$ = **2.5** A and the conduction loss is $6.25 \times 0.2$ = **1.25** W, so $\eta = 50/(50 + 1.25 + 1.5 + 1)$ = **93.02**%. At 1 W, the conduction loss is only **0.025** W, but the 2.5 W of fixed losses remain: $\eta = 1/(1 + 0.025 + 2.5)$ = **28.37**%. Fixed losses decide efficiency at typical listening levels.

### Solution 12-07.12

$P_{max} = 15^2/16$ = **14.06** W, so the average is **1.406** W, with $V_{op} = V_{CC}/\sqrt{10}$. Then $\eta = (\pi/4)/\sqrt{10}$ = **24.84**% and the dissipation is $1.406/0.2484 - 1.406$ = **4.256** W: three times the useful output.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 12-07.1a | efficiency at half amplitude | 6.25 | % |
| 12-07.2a | maximum output power | 18 | W |
| 12-07.2b | supply power | 22.92 | W |
| 12-07.2c | efficiency | 78.54 | % |
| 12-07.3a | amplitude of worst dissipation | 12.73 | V |
| 12-07.3b | total worst dissipation | 10.13 | W |
| 12-07.3c | per-transistor worst dissipation | 5.066 | W |
| 12-07.4a | bias current | 100 | mA |
| 12-07.4b | supply power | 1 | W |
| 12-07.4c | maximum load power | 0.25 | W |
| 12-07.5a | efficiency | 45.34 | % |
| 12-07.6a | input-referred dead band | 7 | µV |
| 12-07.7a | NPN current | 200.50 | mA |
| 12-07.7b | PNP current | 0.4988 | mA |
| 12-07.7c | idle output resistance | 1.293 | Ω |
| 12-07.8a | R_2 | 600 | Ω |
| 12-07.8b | R_1 | 650 | Ω |
| 12-07.8c | temperature coefficient | −4.167 | mV/°C |
| 12-07.8d | R_1/R_2 | 1.0833 | — |
| 12-07.9a | largest θ_SA | 3.7 | °C/W |
| 12-07.10a | g_m | 7.736 | A/V |
| 12-07.10b | loop gain | 2.476 | — |
| 12-07.10c | smallest emitter resistor | 0.5107 | Ω |
| 12-07.11a | load current | 2.5 | A |
| 12-07.11b | conduction loss at 50 W | 1.25 | W |
| 12-07.11c | efficiency at 50 W | 93.02 | % |
| 12-07.11d | conduction loss at 1 W | 0.025 | W |
| 12-07.11e | efficiency at 1 W | 28.37 | % |
| 12-07.12a | maximum power | 14.06 | W |
| 12-07.12b | average power | 1.406 | W |
| 12-07.12c | efficiency | 24.84 | % |
| 12-07.12d | dissipation | 4.256 | W |
