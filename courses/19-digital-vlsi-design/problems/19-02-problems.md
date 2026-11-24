# Problems 19-02 · The CMOS Inverter: Dynamic Behavior and Delay

Chapter: [19-02](../chapters/19-02-cmos-inverter-dynamic.md) · Worked solutions: [19-02 solutions](../solutions/19-02-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Square-law transistors with λ = 0 and $k = \mu C_{ox}W/L$, driving a lumped load. A step input is instantaneous. $t_p = (t_{pHL} + t_{pLH})/2$, measured between 50% points. The RC model uses $t_p = \ln 2\,R_{eq}C$. γ = $C_{int}/C_g$. Problems marked *(lab)* can be checked with `labs/19-02-lab/delay.py`, `delay.cir` or `ring.cir`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 19-02.1 [A]

**The load.** An inverter has $W_n$ = 0.3 µm and $W_p$ = 0.6 µm, in a process with $C_g'$ = 1.2 fF/µm of input capacitance and $C_d'$ = 1.0 fF/µm of drain capacitance (Miller doubling included). It drives three identical inverters through 1.5 fF of wire. Find its input capacitance, intrinsic capacitance, external load, total load and γ.

### Problem 19-02.2 [A]

**The Miller term.** Each transistor of an inverter has 0.3 fF of drain-junction capacitance and 0.1 fF of gate–drain capacitance. (a) What intrinsic capacitance does the output see during a full-swing transition? (b) What would you get if you forgot the Miller effect? (c) Why does $C_{gd}$ count twice?

### Problem 19-02.3 [A]

**Ring arithmetic.** A 31-stage ring oscillator runs at 450 MHz. (a) What is its stage delay? (b) What frequency would a 51-stage ring of the same stages give?

### Problem 19-02.4 [B]

**Exact step delay.** An NMOS with $k_n$ = 300 µA/V² and $V_{TN}$ = 0.3 V discharges 15 fF from $V_{DD}$ = 1.0 V after an input step. Find the time spent in saturation, the time in the linear region down to the 50% point, and $t_{pHL}$.

### Problem 19-02.5 [B] *(lab)*

**The RC stand-in.** For the transistor of Problem 4: (a) compute $R_{eq}$ as the average of $V/I$ from $V_{DD}$ to $V_{DD}/2$ (numerically, or with Problem 10's closed form), and the approximation $3V_{DD}/(4I_{sat})$; (b) find the RC model's $t_{pHL}$ for 15 fF and its error against Problem 4; (c) what does the RC model give with the approximate resistance?

### Problem 19-02.6 [B]

**Balancing rise and fall.** An inverter with equal NMOS and PMOS widths drives a large fixed load (its own capacitance is negligible by comparison) with $t_{pHL}$ = 40 ps and $t_{pLH}$ = 100 ps; $\mu_n/\mu_p$ = 2.5. (a) What is $t_p$? (b) The PMOS is widened 2.5 times. What are $t_{pLH}$ and $t_p$ now? (c) By what factor has the inverter's input capacitance grown, and who pays for it?

### Problem 19-02.7 [B]

**Intrinsic delay and upsizing.** A unit inverter has $R_{eq}$ = 10 kΩ (both edges), $C_{int}$ = 1.5 fF and $C_g$ = 2 fF. Find (a) its intrinsic delay, (b) γ and its FO4 delay, (c) its delay driving 100 fF, (d) the delay driving 100 fF when it is made 10 times larger, and its new input capacitance.

### Problem 19-02.8 [B]

**From a ring to FO4.** A 101-stage ring oscillator of inverters, each loaded only by the next (fan-out of 1), runs at 150 MHz. (a) What is the FO1 stage delay? (b) Estimate the FO4 delay assuming γ = 1. (c) Estimate it instead with the rule of thumb that an FO1 delay is one-third of an FO4 delay. (d) Which γ does (c) imply?

### Problem 19-02.9 [B]

**Lowering the supply.** A design has $V_{TH}$ = 0.3 V and follows the alpha-power law with α = 1.4. Its supply is lowered from 0.9 V to 0.5 V. (a) By what factor does the delay grow? (b) By what factor does the energy per transition fall? (c) What happens to the energy–delay product? (d) Where is the EDP minimum?

### Problem 19-02.10 [C]

**$R_{eq}$ in closed form.** (a) Show that, for $V_{TN} < V_{DD}/2$ and $V_{ov} = V_{DD} - V_{TN}$,

$$
R_{eq} = \frac{2}{V_{DD}}\left[\frac{V_{DD}^2 - V_{ov}^2}{k V_{ov}^2} + \frac{2}{k}\ln\frac{4V_{ov} - V_{DD}}{2V_{ov}}\right] .
$$

(b) Check it against the chapter's 12.57 kΩ ($k$ = 200 µA/V², $V_{DD}$ = 1.2 V, $V_{TN}$ = 0.35 V). (c) The ratio of the RC-model delay to the exact step delay depends only on $V_{TN}/V_{DD}$. Evaluate it for 0.2 and 0.4. *(lab)*

### Problem 19-02.11 [C]

**The delay-optimal PMOS width.** An inverter with $W_p = \beta W_n$ drives $N$ copies of itself, with no wire. At equal widths the PMOS resistance is $r$ times the NMOS's. (Here β is a width ratio, not a current gain; $r$ is the same number as 19-01's $k_n/k_p$ at equal widths.) (a) Show that $t_p \propto (1 + \beta)(1 + r/\beta)$, so that the delay is minimized at $\beta = \sqrt r$. (b) For $r$ = 2.5, find $\beta_{opt}$ and how much faster it is than β = $r$ (equal rise and fall) and than β = 1. (c) Why is the optimum not at equal rise and fall delays?

### Problem 19-02.12 [C]

**Other figures of merit.** (Here $n$ is an exponent, not the subthreshold factor.) With $E \propto V_{DD}^2$ and $D \propto V_{DD}/(V_{DD} - V_{TH})^\alpha$: (a) show that $E\,D^n$ is minimized at $V_{DD} = (2 + n)V_{TH}/(2 + n - n\alpha)$ when $2 + n > n\alpha$. (b) For $V_{TH}$ = 0.35 V and α = 1.3, evaluate the optimum for $n$ = 1, 2 and 3. (c) Why does $E\,D^2$ have no finite optimum for the square law, and what does a designer who cares mostly about speed conclude?

### Problem 19-02.13 [B]

**Capacitances from device data.** An inverter has $W_n$ = 0.5 µm and $W_p$ = 1.0 µm, both with $L$ = 0.15 µm, and drives four copies of itself. Take $C_{ox}$ = 8.5 fF/µm², gate–source and gate–drain overlap capacitance 0.3 fF/µm of width each, and for both drain junctions a zero-bias bottom capacitance of 1.0 fF/µm² and sidewall capacitance of 0.25 fF/µm. Each drain extends 0.5 µm from the gate; count the sidewall on the three sides away from the gate. Over the output swing, the junction capacitances average to $K_{eq}$ = 0.62 (bottom) and 0.75 (sidewall) times their zero-bias values (09-06). (a) Find the input capacitance $C_g$ of one inverter (channel plus both overlaps). (b) Find each device's contribution to the driver's self-loading $C_{int}$, counting its gate–drain overlap twice (Miller effect), and the total. (c) Find γ and the FO4 load capacitance.

### Problem 19-02.14 [B] *(lab)*

**Fall time.** For the step-driven NMOS of Example 19-02.2 ($k_n$ = 200 µA/V², $V_{TN}$ = 0.35 V, $V_{DD}$ = 1.2 V, 20 fF), derive the time for the output to fall from 90 % to 10 % of $V_{DD}$, using §3.3's saturation and linear phases. Compare it with $t_{pHL}$, and with the 10–90 % time $\ln 9\,R_{eq}C_L$ that the RC model would give with $R_{eq}$ = 12.573 kΩ. What does the comparison say about using $R_{eq}$ for edge rates?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Identify and add up the load capacitances | 1, 2, 13 |
| 2. Derive the step delay and the equivalent-resistance model | 4, 5, 10, 14 |
| 3. Intrinsic delay, self-loading, sizing and FO4 | 6, 7, 8, 11 |
| 4. Ring oscillators | 3, 8 |
| 5. Supply scaling and the energy–delay product | 9, 12 |
