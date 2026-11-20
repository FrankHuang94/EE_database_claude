# Solutions 12-05 · Feedback: Theory and the Four Topologies

Problems: [12-05 problems](../problems/12-05-problems.md) · Chapter: [12-05](../chapters/12-05-feedback-topologies.md). Every number below is recomputed by [verify_12_05.py](../verify/verify_12_05.py), which solves each complete circuit by nodal analysis with test sources rather than reusing these formulas.

---

## Solutions

### Solution 12-05.1

$T = A\beta$ = **500**. $A_f = A/(1 + T) = 5000/501$ = **9.980**, against the ideal 10; the error is $1/(1 + T)$ = **0.200**%.

### Solution 12-05.2

The error is $1/(1 + T) \le 10^{-4}$, so $1 + T \ge 10^4$ and $T \ge$ **9999**. With β = 0.1, $A = T/\beta \ge$ **99990**, about 100 dB.

### Solution 12-05.3

$A_0 = 10^{130/20}$ = **3.162 × 10⁶**, so the pole is at $10\ \text{MHz}/A_0$ = **3.162** Hz. At a gain of 100 (β = 0.01), the bandwidth is $f_p(1 + A_0\beta)$ = **100.0** kHz; at a gain of 1 (β = 1), it is **10.00** MHz. Each is the gain–bandwidth product divided by the closed-loop gain.

### Solution 12-05.4

(a) **Series–shunt**: the divider samples the output voltage (shunt) and its voltage is subtracted in series with the input at the op-amp's differential input. A voltage amplifier.

(b) **Shunt–shunt**: $R_F$ samples the output voltage and returns a current to the input node, where it is subtracted from the photodiode's current. A transresistance amplifier.

(c) **Series–series**: the sense resistor carries the output (drain) current, so it samples current (series), and its voltage is subtracted from the input voltage at the op-amp's input (series). A transconductance amplifier: a voltage-to-current converter.

(d) **Shunt–series**: the small resistor samples the output current (series), and the feedback resistor returns a current to the input node (shunt). A current amplifier.

### Solution 12-05.5

The ratio of the closed-loop gains at the two corners is

$$
\frac{A_f(3A)}{A_f(A)} = \frac{3A/(1 + 3T)}{A/(1 + T)} = \frac{3(1 + T)}{1 + 3T} = 1 + \frac{2}{1 + 3T} .
$$

Requiring $2/(1 + 3T) \le 5 \times 10^{-4}$ gives $1 + 3T \ge 4000$, so $T \ge$ **1333** at the slow corner. With β = 0.01, $A_{min} = T/\beta$ = **1.333 × 10⁵**. The fast corner then has $T$ = 4000.

### Solution 12-05.6

$T = 2 \times 10^5 \times 0.1$ = **2 × 10⁴**. Series mixing: $R_{if} \approx 2\ \text{M}\Omega \times 20\,001$ = **40.00** GΩ. Shunt sampling: $R_{of} \approx 50\ \Omega/20\,001$ = **2.500** mΩ. (The divider and $R_{id}$ shift these by well under 1%.)

### Solution 12-05.7

Replace the op-amp's source $Av_d$ by an independent source $s_c$ at the output. With the photodiode current zero, the inverting input sits at $s_cR_S/(R_S + R_F)$ and $v_d$ is minus that, so

$$
T = A\,\frac{R_S}{R_S + R_F} = 10^4 \times \frac{1}{1.1} = \mathbf{9091} .
$$

As $A \to \infty$ the inverting input is a virtual ground, all of the photocurrent flows through $R_F$, and $A_\infty = -R_F$ = **−100** kΩ. With $A$ = 0 the output is held at 0 V by the ideal output, so $A_{\mathrm{dir}}$ = 0. Then $A_f = -100\ \text{k}\Omega \times 9091/9092$ = **−99.99** kΩ.

Input resistance: with $A$ = 0, the input node sees $R_S \parallel R_F$ = **90.91** kΩ. Shorting the input node kills the loop ($T_{sc}$ = 0); with it open, $T_{oc} = T$. Blackman gives $R_{in} = 90.91\ \text{k}\Omega/9092$ = **9.999** Ω: the photodiode looks into almost a short, which keeps its voltage, and so its capacitance's effect, small.

### Solution 12-05.8

(a) $\beta = 1/11$, so the naive loop gain is $1000/11$ = **90.91**.

(b) Replace $Av_d$ by $s_c$ behind $R_o$. With the input source zeroed, the inverting node sees $R_1 \parallel R_{id}$ = 909.1 Ω to ground, fed from $s_c$ through $R_o + R_2$ = 11 kΩ:

$$
T = A\,\frac{R_1 \parallel R_{id}}{R_1 \parallel R_{id} + R_2 + R_o} = 1000 \times \frac{909.1}{11\,909.1} = \mathbf{76.34} .
$$

The naive value is 19% too high: it ignores $R_{id}$ shunting $R_1$ and $R_o$ in series with $R_2$.

(c) As $A \to \infty$ the inverting node is a virtual ground: $A_\infty = -R_2/R_1$ = **−10**. With $A$ = 0, the input drives $R_1$ into $R_{id} \parallel (R_2 + R_o)$ = 5238 Ω, giving 0.8397 of the input at the inverting node, and the divider $R_o/(R_2 + R_o)$ passes 1/11 of that to the output: $A_{\mathrm{dir}}$ = **0.07634**.

(d) $A_f = (-10 \times 76.34 + 0.07634)/77.34$ = **−9.870**, an error of **1.30**% from −10. A direct nodal solution agrees.

### Solution 12-05.9

Replace $g_mv_{gs}$ by a current $i_t$ into the source node. With the gate at 0, $v_s = i_t(r_o \parallel R_L)$ and the source would be $g_m(-v_s)$:

$$
T = g_m(r_o \parallel R_L) = 2\ \text{mA/V} \times 6.667\ \text{k}\Omega = \mathbf{13.33} .
$$

As $g_m \to \infty$, $v_{gs} \to 0$ and $A_\infty$ = 1; with $g_m$ = 0 nothing reaches the output, $A_{\mathrm{dir}}$ = 0. Gain $= T/(1 + T)$ = **0.9302**. At the output, $R^{(0)} = r_o \parallel R_L$ = **6.667** kΩ; shorting the output kills the loop and opening it leaves $T$, so $R_{out} = 6.667\ \text{k}\Omega/14.33$ = **465.1** Ω, exactly $1/g_m \parallel r_o \parallel R_L$. The follower is a series–shunt amplifier with β = 1.

### Solution 12-05.10

The bandwidth grows by $1 + T_0$, so $1 + T_0 = 10\ \text{MHz}/50\ \text{kHz}$ = 200, $T_0$ = **199** and $\beta = 199/2000$ = **0.0995**. The gain falls by the same 200: $A_f$ = **10**. GBW $= 2000 \times 50\ \text{kHz}$ = **100** MHz, unchanged by the feedback.

### Solution 12-05.11

The drain now sees $R_D' = R_D \parallel r_o$ = **8** kΩ in place of $R_D$. Then

$$
T = g_m\,[R_D' \parallel (R_F + R_S)]\,\frac{R_S}{R_F + R_S} = 4\ \text{mA/V} \times 7.059\ \text{k}\Omega \times \tfrac16 = \mathbf{4.706} .
$$

$A_\infty = -R_F$ = **−50** kΩ (a virtual ground at the gate sends all of $i_s$ through $R_F$ whatever $r_o$ is). $A_{\mathrm{dir}} = R_SR_D'/(R_S + R_F + R_D')$ = **1.176** kΩ. So $A_f = (-50 \times 4.706 + 1.176)/5.706$ kΩ = **−41.03** kΩ.

Input: $R^{(0)} = R_S \parallel (R_F + R_D')$ = **8.529** kΩ, divided by $1 + T$: **1.495** kΩ. Output: $R^{(0)} = R_D' \parallel (R_F + R_S)$ = **7.059** kΩ, divided by $1 + T$: **1.237** kΩ. The lower loop gain makes the transresistance a little further from $-R_F$ and the port resistances a little higher than in Example 12-05.4.

### Solution 12-05.12

Short the drain to ground and take the drain current $i_o$ as the output.

- **Asymptotic gain.** As $g_m \to \infty$, $v_{gs} \to 0$, so the source follows the gate: $v_s = v_i$. The current in $R_S$ is $v_i/R_S$, and by KCL at the source all of it arrives from the drain, so $A_\infty = 1/R_S$ = **1** mA/V.
- **Direct transmission.** With $g_m$ = 0 there is no path from the gate to the output: $A_{\mathrm{dir}}$ = 0.
- **Return ratio.** With the drain shorted, a current injected by the controlled source flows into $R_S \parallel r_o$, so $T = g_m(R_S \parallel r_o)$ = **1.961**.

Then $G_m = (1\ \text{mA/V}) \times 1.961/2.961$ = **0.6623** mA/V, which is exactly $g_m/(1 + g_mR_S + R_S/r_o)$, the value Example 12-05.6 quoted from the full circuit.

### Solution 12-05.13

The error $1/(1 + T) \le 5 \times 10^{-4}$ needs $T \ge$ **1999**, so with β = 1/20, $A_0 \ge 1999 \times 20$ = **3.998 × 10⁴**. At that gain $1 + T_0$ = 2000, and the closed-loop bandwidth $f_p(1 + T_0) \ge 1$ MHz requires $f_p \ge$ **500** Hz. The gain–bandwidth product is then $A_0f_p$ = **19.99** MHz: about 20 times the required bandwidth, as the rule "GBW ≈ gain × bandwidth" says.

### Solution 12-05.14

Distortion generated inside the loop falls by $1 + T$ = **50** at the same output level, to about **0.02**%. Noise at the amplifier's input is indistinguishable from the signal, so it is amplified by the closed-loop gain: **100** nV/√Hz at the output, the same 10 nV/√Hz referred to the input as without feedback.

### Solution 12-05.15

(a) $\beta = R_1/(R_1 + R_2)$ = **0.1**. With the network's output port shorted, its input port sees $R_{11} = R_1 \parallel R_2$ = **900** Ω; with its input port open, its output port sees $R_{22} = R_1 + R_2$ = **10** kΩ. The loaded gain is

$$
A_L = 1000 \times \frac{10\ \text{k}\Omega}{10\ \text{k}\Omega + 900\ \Omega} \times \frac{10\ \text{k}\Omega}{10\ \text{k}\Omega + 1\ \text{k}\Omega} = \mathbf{834.0} ,
$$

so $T = A_L\beta$ = **83.40**, $A_f = A_L/(1 + T)$ = **9.882**, $R_{if} = (10\ \text{k}\Omega + 900\ \Omega)(1 + T)$ = **920.0** kΩ and $R_{of} = (1\ \text{k}\Omega \parallel 10\ \text{k}\Omega)/(1 + T)$ = **10.77** Ω.

(b) Replace the op-amp's internal source by an independent $v_x$ behind $R_o$, with the input grounded. The output node feeds $R_2$ into the inverting node, which sees $R_1 \parallel R_{id}$ = 909.1 Ω, so the inverting node receives $v_x \times 909.1/(1000 + 9000 + 909.1) = v_x/12$. The op-amp would respond with $A(0 - v_x/12)$, so the return ratio is $T = 1000/12$ = **83.33**. With $A$ = 0, the input drives $R_{id}$ into the inverting node, which sees $R_1 \parallel (R_2 + R_o)$ = 909.1 Ω, and $R_o/(R_2 + R_o)$ of that node's voltage reaches the output: $A_{\mathrm{dir}} = (909.1/10\,909) \times 0.1$ = **0.008333**. With $A_\infty = 1 + R_2/R_1$ = 10, the asymptotic-gain formula gives $A_f = (10 \times 83.33 + 0.008333)/84.33$ = **9.882**. Blackman's formula gives the impedances: $Z^{(0)}_{in} = R_{id} + R_1 \parallel (R_2 + R_o)$ = **10.91** kΩ with $T_{sc}$ = 83.33 and $T_{oc}$ = 0, so $R_{in}$ = **920.0** kΩ; $Z^{(0)}_{out} = R_o \parallel (R_2 + R_1 \parallel R_{id})$ = **908.3** Ω with $T_{oc}$ = 83.33, so $R_{out}$ = **10.77** Ω.

(c) The loading method treats the input and output loading as independent factors, while the real divider couples them, so its loop gain is off in the second order of the loading ratios (here by under 0.1%). The loop gain is not itself a measurable output, and its error reaches the closed-loop gain only through the desensitivity factor $1 + T \approx 84$; the direct transmission the method ignores is similarly diluted. Both routes give 9.882, 920.0 kΩ and 10.77 Ω.

### Solution 12-05.16

*With $g_m$ = 0*, the gate sees $R_G \parallel (R_B + R_S) = 1\ \text{M}\Omega \parallel 1.01\ \text{M}\Omega$: $Z^{(0)}$ = **502.5** kΩ.

*Port shorted.* With the gate grounded, inject a test current $i_t$ into the source node in place of $g_mv_{gs}$. The source sees $R_S \parallel R_B$ = 9.901 kΩ, so $v_s = 9.901\ \text{k}\Omega \times i_t$ and $v_{gs} = -v_s$. The source would return $g_mv_{gs} = -g_m \times 9.901\ \text{k}\Omega \times i_t$, so $T_{sc} = g_m(R_S \parallel R_B)$ = **19.80**.

*Port open.* The gate still connects to ground through $R_G$ and to the source through $R_B$. The source sees $R_S \parallel (R_B + R_G)$ = 9.950 kΩ, the gate sits at $v_s R_G/(R_G + R_B) = v_s/2$, and $v_{gs} = -v_s/2$, so $T_{oc} = g_m \times 9.950\ \text{k}\Omega \times 0.5$ = **9.950**.

$$
R_{in} = 502.5\ \text{k}\Omega \times \frac{1 + 19.80}{1 + 9.950} = \mathbf{954.6}\ \text{k}\Omega .
$$

*Why it exceeds $R_G \parallel (R_B + R_S)$.* The follower holds the source close to the gate, so little voltage appears across $R_B$ and little current flows in it: $R_B$ is **bootstrapped**. The gain from gate to source by the asymptotic-gain formula, with the gate driven by an ideal source (the port shorted for the loop, $T = T_{sc}$), $A_\infty$ = 1 and $A_{\mathrm{dir}} = R_S/(R_B + R_S)$ = 0.009901, is $A_v = (19.80 + 0.009901)/20.80$ = **0.9524**. The current into the gate is $v_g/R_G + v_g(1 - A_v)/R_B$, so $R_B$ acts like $R_B/(1 - A_v)$ = **21.01** MΩ, and $R_G \parallel 21.01\ \text{M}\Omega$ = 954.6 kΩ, as Blackman's formula found. Bootstrapping is used to raise the input resistance of AC-coupled followers and to cancel cable capacitance with a driven guard.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 12-05.1a | loop gain | 500 | — |
| 12-05.1b | closed-loop gain | 9.980 | — |
| 12-05.1c | gain error | 0.200 | % |
| 12-05.2a | minimum loop gain | 9999 | — |
| 12-05.2b | minimum open-loop gain | 99990 | — |
| 12-05.3a | open-loop gain | 3.162 × 10⁶ | — |
| 12-05.3b | open-loop pole | 3.162 | Hz |
| 12-05.3c | bandwidth at gain 100 | 100.0 | kHz |
| 12-05.3d | bandwidth at gain 1 | 10.00 | MHz |
| 12-05.5a | minimum loop gain | 1333 | — |
| 12-05.5b | minimum open-loop gain | 1.333 × 10⁵ | — |
| 12-05.6a | loop gain | 2 × 10⁴ | — |
| 12-05.6b | input resistance | 40.00 | GΩ |
| 12-05.6c | output resistance | 2.500 | mΩ |
| 12-05.7a | return ratio | 9091 | — |
| 12-05.7b | asymptotic gain | −100 | kΩ |
| 12-05.7c | transresistance | −99.99 | kΩ |
| 12-05.7d | input resistance with A = 0 | 90.91 | kΩ |
| 12-05.7e | input resistance | 9.999 | Ω |
| 12-05.8a | naive loop gain | 90.91 | — |
| 12-05.8b | return ratio | 76.34 | — |
| 12-05.8c | asymptotic gain | −10 | — |
| 12-05.8d | direct transmission | 0.07634 | — |
| 12-05.8e | closed-loop gain | −9.870 | — |
| 12-05.8f | error | 1.30 | % |
| 12-05.9a | return ratio | 13.33 | — |
| 12-05.9b | gain | 0.9302 | — |
| 12-05.9c | resistance with g_m = 0 | 6.667 | kΩ |
| 12-05.9d | output resistance | 465.1 | Ω |
| 12-05.10a | loop gain | 199 | — |
| 12-05.10b | feedback factor | 0.0995 | — |
| 12-05.10c | closed-loop gain | 10 | — |
| 12-05.10d | gain–bandwidth product | 100 | MHz |
| 12-05.11a | R_D ∥ r_o | 8 | kΩ |
| 12-05.11b | return ratio | 4.706 | — |
| 12-05.11c | asymptotic gain | −50 | kΩ |
| 12-05.11d | direct transmission | 1.176 | kΩ |
| 12-05.11e | transresistance | −41.03 | kΩ |
| 12-05.11f | input resistance with g_m = 0 | 8.529 | kΩ |
| 12-05.11g | input resistance | 1.495 | kΩ |
| 12-05.11h | output resistance with g_m = 0 | 7.059 | kΩ |
| 12-05.11i | output resistance | 1.237 | kΩ |
| 12-05.12a | asymptotic gain | 1 | mA/V |
| 12-05.12b | return ratio | 1.961 | — |
| 12-05.12c | transconductance | 0.6623 | mA/V |
| 12-05.13a | minimum loop gain | 1999 | — |
| 12-05.13b | minimum open-loop gain | 3.998 × 10⁴ | — |
| 12-05.13c | minimum pole frequency | 500 | Hz |
| 12-05.13d | gain–bandwidth product | 19.99 | MHz |
| 12-05.14a | distortion reduction factor | 50 | — |
| 12-05.14b | closed-loop second harmonic | 0.02 | % |
| 12-05.14c | output noise density | 100 | nV/√Hz |
| 12-05.15a | β | 0.1 | — |
| 12-05.15b | R_11 | 900 | Ω |
| 12-05.15c | R_22 | 10 | kΩ |
| 12-05.15d | loaded gain | 834.0 | — |
| 12-05.15e | loop gain, loading method | 83.40 | — |
| 12-05.15f | closed-loop gain, loading method | 9.882 | — |
| 12-05.15g | input resistance, loading method | 920.0 | kΩ |
| 12-05.15h | output resistance, loading method | 10.77 | Ω |
| 12-05.15i | return ratio | 83.33 | — |
| 12-05.15j | direct transmission | 0.008333 | — |
| 12-05.15k | closed-loop gain, asymptotic | 9.882 | — |
| 12-05.15l | input Z with A = 0 | 10.91 | kΩ |
| 12-05.15m | input resistance, Blackman | 920.0 | kΩ |
| 12-05.15n | output Z with A = 0 | 908.3 | Ω |
| 12-05.15o | output resistance, Blackman | 10.77 | Ω |
| 12-05.16a | Z with g_m = 0 | 502.5 | kΩ |
| 12-05.16b | T with the port shorted | 19.80 | — |
| 12-05.16c | T with the port open | 9.950 | — |
| 12-05.16d | input resistance | 954.6 | kΩ |
| 12-05.16e | gain, gate to source | 0.9524 | — |
| 12-05.16f | effective R_B | 21.01 | MΩ |
