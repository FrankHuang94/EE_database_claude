<!-- status: verified -->
# 21-04 · Low-Noise Amplifiers

| | |
|---|---|
| **Course** | [21 · RF and Microwave Engineering](../README.md) |
| **University equivalent** | The LNA chapter of a senior or first-year graduate RF IC course: input-matching topologies and their noise limits, the inductively degenerated common-source LNA (input impedance, effective transconductance, noise), loss in the gate inductor, gain and linearity tradeoffs, and wideband noise-cancelling LNAs (Razavi, *RF Microelectronics*, the LNA chapter; Lee, *The Design of CMOS Radio-Frequency Integrated Circuits*, the LNA chapter) |
| **Prerequisites** | [21-03](21-03-noise-figure-and-linearity.md) (noise factor, noise parameters, IIP3, cascades), [21-02](21-02-impedance-matching-networks.md) (matching, component Q), [12-03](../../12-electronics-2/chapters/12-03-frequency-response-miller-poles-zeros.md) ($C_{gs}$, $f_T$), [12-10](../../12-electronics-2/chapters/12-10-noise-in-circuits.md) (channel thermal noise) |
| **Estimated study hours** | 7 |
| **Last verified** | 2026-11-24 |

**Learning objectives.** After this chapter you can:

1. Explain why a resistor cannot be used to match an LNA's input without at least a 3 dB noise figure, and derive the noise factor of a common-gate input stage.
2. Derive the input impedance, effective transconductance and drain-noise contribution of the inductively degenerated common-source LNA, and design its elements for a match.
3. Quantify how the gate inductor's loss and the input network's Q trade noise figure, gain and linearity.
4. Derive the noise-cancelling condition of a wideband common-gate/common-source LNA and compute its noise figure.
5. Set an LNA's gain from the noise of the stage that follows it, and read LNA specifications critically.

## 1. Big picture

The low-noise amplifier is the first active circuit a received signal meets, so by the Friis formula (21-03) its noise figure is most of the receiver's. It must also present a defined impedance to the antenna or filter in front of it (usually 50 Ω), because filters and duplexers are designed for that termination and a mismatch distorts their passband. The difficulty is that the obvious way to make a 50 Ω input, a 50 Ω resistor, adds as much noise as the source itself. LNA design is the art of making an input that *looks* like a resistor without *being* one: by feedback through reactances (inductive degeneration), by a transistor's own transconductance (the common-gate stage), or by cancelling the matching device's noise at the output (noise-cancelling LNAs).

- **Every receiver** in a phone, Wi-Fi access point, GNSS chip, radar or satellite terminal starts with an LNA, discrete or integrated.
- **Front-end modules** combine LNAs with switches and filters (21-09); their noise figure, including the switch's loss, is what the system sees.
- **mmWave arrays** have one LNA per antenna element (21-10), so LNA power is multiplied by the element count.
- **Always-on IoT radios** trade a few decibels of noise figure for milliwatts of current, because battery life matters more than range.

## 2. Intuition first

```text
   Rs ──┬── Rs (match)          Rs ── 1/gm (CG source)          Rs ── Lg ──┤ Cgs ├── Ls ──┐
        │                                                                 g_m v_gs  →     │
       amp                       noise of the device                    "real part" ωT·Ls ─┘
   F ≥ 2 (3 dB):                F = 1 + γ/α at match:           no resistor at all: F → 1 as ω0/ωT → 0
   half the noise is the        about 2.2 to 3 dB               (until losses and gate noise intervene)
   terminating resistor's
```

*Figure 1. Three ways to make a 50 Ω input. A resistor matches by dissipating, so it adds its own thermal noise. A common-gate transistor matches with its $1/g_m$, so its channel noise adds. Inductive source degeneration creates a real input impedance from a reactance and a transconductance, which add no noise of their own.*

**An accounting analogy.** A real resistor is like a bank that charges a fee for every deposit: the input "looks right" (the deposit is accepted at a fair rate) but a fee is skimmed. Inductive degeneration is like an exchange that matches buyers and sellers through a clearing mechanism that charges nothing itself; the only costs are the brokers' (the transistor's channel noise and the inductor's resistance). The analogy breaks because the clearing mechanism only works at one frequency: the inductive "resistance" exists only near resonance, which is why this LNA is narrowband.

## 3. Theory

### 3.1 What an LNA must deliver

An LNA specification lists, at minimum: noise figure; input return loss (often better than 10 dB across the band, $\lvert S_{11}\rvert < -10$ dB); gain, enough to bury the next stage's noise (§3.7) but not so much that it ruins linearity (21-03 §3.6); IIP3 and P1dB; supply current; stability (21-01 §3.7) across all source and load impedances the system can present; and reverse isolation, so that LO leakage from the mixer does not reach the antenna. The topologies below differ in how they trade these.

### 3.2 Why a resistor costs at least 3 dB

Terminate the source $R_s$ with a shunt resistor $R_T = R_s$ and follow it with a noiseless voltage amplifier of high input impedance. The source and the terminating resistor form a divider of two equal resistors at the same temperature, so each contributes the same noise at the amplifier's input, while only the source carries the signal. The output noise is twice what the source alone would produce, so

$$
F = 1 + \frac{R_s}{R_T} = 2 \qquad (3.01\ \text{dB}),
$$

before the amplifier adds anything. If the amplifier has its own noise factor $F_A$ referred to the divided source, the total is $2 + 4(F_A - 1)$: the divider halves the signal voltage, so the amplifier's excess noise counts four times. Resistive termination is acceptable only where noise figure hardly matters (instrumentation inputs, some test equipment).

### 3.3 The common-gate stage

A common-gate transistor with its gate at AC ground presents $1/g_m$ at its source (ignoring body effect and output resistance), so $g_m = 1/R_s$ = 20 mS matches 50 Ω, over a wide band. Its channel thermal noise is a current of density $4kT_0\gamma g_{d0}$ between drain and source, where $g_{d0}$ is the drain–source conductance at $V_{DS} = 0$ and $\gamma$ is the excess-noise factor (2/3 for a long-channel device in saturation; how much larger it is in short channels is disputed, §9). Write $\alpha = g_m/g_{d0}$ (1 for a long channel, below 1 in short channels). The noise current flows into the source node, which sees $R_s \parallel 1/g_m$; the fraction of it that reaches the drain and the fraction of the source's signal current that reaches it work out (Problem 21-04.3) to

$$
F = 1 + \frac{\gamma}{\alpha}\,\frac{1}{g_mR_s} \quad\xrightarrow{\ g_mR_s = 1\ }\quad F = 1 + \frac{\gamma}{\alpha} .
$$

With $\gamma/\alpha$ = 2/3 that is 1.67 (2.22 dB); with $\gamma/\alpha$ = 1 it is 2 (3.01 dB), no better than a resistor. The match itself fixes $g_m$, so the designer cannot trade current for noise. The common gate's merits are a broadband match and good linearity and reverse isolation; its noise figure is the price.

### 3.4 Inductive source degeneration: a noiseless real input

Put an inductor $L_s$ in the source of a common-source transistor and look into its gate. Ignoring $C_{gd}$ and the output, the gate current $i$ charges $C_{gs}$, so $v_{gs} = i/(sC_{gs})$, and the source node carries $i + g_mv_{gs}$ through $L_s$. The input voltage is

$$
v_{in} = \frac{i}{sC_{gs}} + sL_s\left(i + \frac{g_mi}{sC_{gs}}\right) \quad\Longrightarrow\quad Z_{in} = sL_s + \frac{1}{sC_{gs}} + \frac{g_mL_s}{C_{gs}} = sL_s + \frac{1}{sC_{gs}} + \omega_TL_s ,
$$

with $\omega_T = g_m/C_{gs}$ (12-03). The term $\omega_TL_s$ is **real** and frequency-independent, yet no resistor produced it: it is the voltage the transconductance current develops across the reactance $L_s$, appearing in phase with the input current because $1/(sC_{gs})$ and $sL_s$ each contribute 90°. Add a gate inductor $L_g$ in series to resonate the remaining reactance at $\omega_0$:

$$
\omega_TL_s = R_s, \qquad \omega_0^2(L_g + L_s)C_{gs} = 1 .
$$

**Effective transconductance.** At resonance the input is a pure resistance $R_s$ in series with the source's $R_s$, so the input current is $v_s/2R_s$ for a source EMF $v_s$, and the voltage across $C_{gs}$ is $Q_{in}$ times $v_s$, where

$$
Q_{in} = \frac{1}{2\omega_0R_sC_{gs}}, \qquad G_m = \frac{i_{out}}{v_s} = g_mQ_{in} = \frac{\omega_T}{2\omega_0R_s} .
$$

The series-resonant input is a passive voltage amplifier, and the effective transconductance depends only on $\omega_T/\omega_0$: for a given device technology and bias ($\omega_T$ fixed), it does not depend on the device's width or current.

**Drain noise reaches the output halved.** Inject the channel noise current $i_{nd}$ between drain and source and set $v_s = 0$. The noise current flows through $L_s$ and drives the input loop: KVL around the loop, with total loop impedance $2R_s$ at resonance, gives a loop current $i = -sL_si_{nd}/(2R_s)$, hence $v_{gs} = i/(sC_{gs}) = -L_si_{nd}/(2R_sC_{gs})$ and a transconductance current $g_mv_{gs} = -(\omega_TL_s/2R_s)\,i_{nd} = -i_{nd}/2$. The output carries $i_{nd} - i_{nd}/2 = i_{nd}/2$: the degeneration feeds half the noise back in antiphase. With noise powers,

$$
F = 1 + \frac{\tfrac14\,4kT_0\gamma g_{d0}}{G_m^2\,4kT_0R_s} = 1 + \frac{\gamma}{\alpha}\,g_mR_s\left(\frac{\omega_0}{\omega_T}\right)^2 .
$$

(Substitute $G_m = \omega_T/2\omega_0R_s$ and $g_{d0} = g_m/\alpha$.) The noise figure falls as $(\omega_0/\omega_T)^2$: a fast transistor at a low frequency is nearly noiseless. ngspice confirms the halving exactly (§5, Example 21-04.2).

> **Going deeper — induced gate noise.** At high frequency the channel's thermal fluctuations also couple capacitively to the gate, producing a gate noise current partly correlated with the drain noise. Including it adds a term that grows as $Q_{in}$ falls and changes the optimization: for a fixed power budget there is an optimum device width (and $Q_{in}$) at which the noise figure is minimum. Shaeffer and Lee's analysis of this LNA, with its 1.5 GHz CMOS demonstration, is the classic treatment (read it with its 2005 correction) [1]; the textbooks reproduce it [2, 3]. With the long-channel constants ($\delta$ = 4/3 for the gate noise, correlation $\lvert c\rvert$ = 0.395), the transistor's own minimum noise factor becomes $F_{min} = 1 + 2(\omega_0/\omega_T)\sqrt{\delta\gamma(1 - \lvert c\rvert^2)/5}$ [3, 8], **0.32** dB at $f_0/f_T$ = 0.1. The drain-noise-only result above is the right first-order picture and the one this chapter verifies.

### 3.5 Losses in the gate inductor

$L_g$ is usually the largest inductor in the LNA (several nanohenries at 2.4 GHz, §4), and its series loss $r_g = \omega_0L_g/Q_L$ sits directly in series with the source, where it adds noise exactly like a resistor in the signal path. Re-matching the input so that $r_g + \omega_TL_s = R_s$ keeps $Z_{in} = R_s$; repeating the noise calculation with the loop now containing $r_g$ (Problem 21-04.6) gives

$$
F = 1 + \frac{r_g}{R_s} + \frac{\gamma}{\alpha}\,g_m\frac{(R_s + r_g)^2}{R_s}\left(\frac{\omega_0}{\omega_T}\right)^2 .
$$

The first term usually dominates. An on-chip spiral with $Q_L$ of 10 at 2.4 GHz can add about a decibel by itself (Example 21-04.3), which is why discrete and module LNAs put $L_g$ off chip as a high-Q component or bond wire, and why fully integrated designs fight for inductor Q (21-02 §9).

![Noise figure in dB against the gate inductor's Q from 5 to 200 on a logarithmic axis: the curve falls steeply from 2.2 dB at Q = 5 through marked points at Q = 10 (1.32 dB), 15 (1.01 dB) and 30 (0.68 dB) and flattens toward a dashed line at 0.33 dB for an ideal inductor](../../../assets/figures/21-04/gate-q.svg)

*Figure 2. Example 21-04.2's LNA with a lossy gate inductor, re-matched at each Q. Below a Q of about 30 the inductor contributes more noise than the transistor.*

### 3.6 Gain, Q and linearity

The input network's voltage gain $Q_{in}$ is free gain, but it is not free linearity. The transistor's nonlinearity depends on $v_{gs}$, which is $Q_{in}$ times the source EMF. If the device reaches its own intercept at a gate–source amplitude $A_{gs}$, the source reaches it at $A_{gs}/Q_{in}$, so the input-referred IIP3 is lower than the device's own by

$$
\Delta\text{IIP3} = 20\log_{10}Q_{in}\ \text{dB}.
$$

At fixed $g_m$, a device with a higher $\omega_T$ has a smaller $C_{gs}$ and so a larger $Q_{in}$: more gain and lower noise figure, but a lower intercept (Example 21-04.4). The output load sets the voltage gain: with a cascode (which also improves reverse isolation and stability by shielding $C_{gd}$, 12-02) driving a parallel tank of resistance $R_p$ at resonance, the voltage gain from the source EMF is $G_mR_p$.

### 3.7 How much gain an LNA needs

The Friis formula sets the minimum gain. If the LNA has noise factor $F_1$ and the following stage $F_2$, the cascade degrades the LNA's noise figure by $\Delta$ dB when

$$
F_1 + \frac{F_2 - 1}{G_1} = F_1\cdot 10^{\Delta/10} \quad\Longrightarrow\quad G_1 = \frac{F_2 - 1}{F_1\left(10^{\Delta/10} - 1\right)} .
$$

A 1 dB LNA followed by a 10 dB mixer needs 20 dB of gain to keep the degradation to 0.3 dB (Example 21-04.6). More gain than that buys little noise figure and costs linearity downstream, which is why receivers switch LNA gain with signal strength (21-03 §3.6).

### 3.8 Wideband: noise cancelling

Wideband receivers (software-defined radios, multi-band cellular, cable and satellite tuners) cannot use a resonant input. Bruccoleri, Klumperink and Nauta showed in 2004 that the matching device's noise can be cancelled at the output while its signal is kept [4]. In the common-gate/common-source version: a common-gate transistor M1 with $g_{m1} = 1/R_s$ matches the input and drives a load $R_1$; a common-source transistor M2 senses the same input node $x$ and drives a load $R_2$; the output is the difference of the two drain voltages.

Write M1's channel current (drain to source, into node $x$) as $-g_{m1}v_x + i_{n1}$. KCL at $x$ gives $v_x = v_s/2 + i_{n1}R_s/2$ (the node sees $R_s \parallel 1/g_{m1} = R_s/2$). Then

$$
v_{d1} = g_{m1}R_1v_x - R_1i_{n1} = \frac{R_1}{2R_s}v_s - \frac{R_1}{2}i_{n1}, \qquad v_{d2} = -g_{m2}R_2v_x = -\frac{g_{m2}R_2}{2}\left(v_s + R_si_{n1}\right),
$$

$$
v_{out} = v_{d1} - v_{d2} = \frac{v_s}{2}\left(\frac{R_1}{R_s} + g_{m2}R_2\right) + \frac{i_{n1}}{2}\left(g_{m2}R_2R_s - R_1\right).
$$

The signal adds; M1's noise appears at the two drains in phase and cancels when

$$
g_{m2}R_2 = \frac{R_1}{R_s} = g_{m1}R_1 .
$$

The remaining noise comes from M2 and the loads. With the cancelling condition, the voltage gain from $v_s$ is $g_{m2}R_2$ and

$$
F = 1 + \frac{\gamma}{\alpha}\,\frac{1}{g_{m2}R_s} + \frac{1}{g_{m2}R_2} + \frac{1}{g_{m2}^2R_2R_s} ,
$$

which can fall well below the common gate's $1 + \gamma/\alpha$ by making $g_{m2}R_s$ large: the match no longer fixes the noise.

![Noise figure in dB against the common-source transconductance g_m2 from 20 to 300 mS: the noise-cancelling LNA's curve falls from above 3 dB, crosses the common-gate stage's dashed 2.22 dB line near 32 mS, passes 0.77 dB at 100 mS (marked as Example 21-04.5) and approaches 0.3 dB at 300 mS](../../../assets/figures/21-04/noise-cancelling.svg)

*Figure 3. The noise-cancelling LNA with $R_2$ = 200 Ω and $R_1$ held at cancellation. Above about **32** mS it beats the common-gate stage that sets its match; every further halving of the excess noise costs about double the current.* The price is the current needed for a large $g_{m2}$, and cancellation that holds only as well as the two paths' gains match across frequency (Example 21-04.5, Problem 21-04.10).

## 4. Worked examples

All examples use $R_s$ = 50 Ω, $T_0$ = 290 K and drain noise only (no induced gate noise). "x" stands for $\gamma/\alpha$.

### Example 21-04.1 · Resistor or common gate? (tier A)

**Setup.** (a) What is the minimum noise figure of a resistively terminated input? (b) A common-gate stage matches 50 Ω. What $g_m$ does it need, and what noise figure does it reach for $x$ = 2/3 and for $x$ = 1?

**Solution.**

- (a) $F = 1 + R_s/R_T = 2$: **3.01** dB, before the amplifier's own noise.
- (b) $g_m = 1/R_s$ = **20** mS. $F = 1 + x$: **1.667** (**2.22** dB) for $x$ = 2/3, and **2** (**3.01** dB) for $x$ = 1.

**Units check.** $g_mR_s$ is dimensionless.

**Sanity check.** A short-channel device with $x \approx 1$ makes a common-gate LNA no quieter than a resistor; its attraction is bandwidth and linearity.

### Example 21-04.2 · Designing an inductively degenerated LNA (tier B)

**Setup.** At 2.4 GHz, a transistor biased for $g_m$ = 40 mS has $f_T$ = 12 GHz. Design the input for a 50 Ω match. Find $C_{gs}$, $L_s$, $L_g$, $Q_{in}$, $G_m$ and the noise figure for $x$ = 1, and the voltage gain into a 200 Ω tank.

**Solution.**

- $C_{gs} = g_m/\omega_T = 0.04/(2\pi \times 12 \times 10^9)$ = **530.5** fF; $L_s = R_s/\omega_T$ = **0.663** nH.
- $L_g + L_s = 1/(\omega_0^2C_{gs})$ = **8.289** nH, so $L_g$ = **7.626** nH.
- $Q_{in} = 1/(2\omega_0R_sC_{gs})$ = **1.25**; $G_m = \omega_T/(2\omega_0R_s) = 5/100$ = **50** mS (check: $g_mQ_{in}$ = 0.04 × 1.25).
- $F = 1 + 1 \times 0.04 \times 50 \times (2.4/12)^2$ = **1.080**, NF = **0.334** dB.
- Voltage gain from the source EMF: $G_mR_p = 0.05 \times 200$ = **10** (20 dB).

**Units check.** S/(rad/s) = F; Ω/(rad/s) = H.

**Sanity check.** ngspice's noise analysis of this model gives 0.334 dB and an input resistance of exactly 50 Ω (§5). Without the halving of the drain noise the noise factor would be $1 + 4 \times 0.08$ = 1.32, or **1.21** dB.

### Example 21-04.3 · The gate inductor's loss (tier B)

**Setup.** In Example 2's LNA, the gate inductor has $Q_L$ = 10, 15 or 30 at 2.4 GHz. Re-match the input (so that $r_g + \omega_TL_s = R_s$) and find $r_g$ and the noise figure in each case.

**Solution.** Solving $r_g = (\omega_0/Q_L)\left[L_{tot} - (R_s - r_g)/\omega_T\right]$ for $r_g$, with $L_{tot}$ = 8.289 nH:

- $Q_L$ = 10: $r_g$ = **11.73** Ω, NF = **1.32** dB.
- $Q_L$ = 15: $r_g$ = **7.77** Ω, $L_g$ = **7.729** nH, $L_s$ = **0.560** nH, NF = **1.01** dB.
- $Q_L$ = 30: $r_g$ = **3.86** Ω, NF = **0.68** dB.

**Units check.** $\omega L/Q$ in ohms.

**Sanity check.** With an ideal inductor the LNA reached 0.33 dB; a $Q$ of 15 triples the noise figure in decibels. The inductor, not the transistor, is the bottleneck.

### Example 21-04.4 · Q, gain and IIP3 (tier B)

**Setup.** Suppose the transistor's own third-order intercept corresponds to a gate–source amplitude of 0.3 V. Find the input-referred IIP3 (available power from a 50 Ω source) for Example 2's design, and for a faster device with the same $g_m$ and $f_T$ = 24 GHz. Compare their noise figures.

**Solution.**

- Example 2: $Q_{in}$ = 1.25, so the source EMF reaches the intercept at 0.3/1.25 = 0.24 V; available power $v_s^2/(8R_s)$ = **−8.42** dBm.
- $f_T$ = 24 GHz: $C_{gs}$ halves, $Q_{in}$ = **2.5**, the EMF intercept is 0.12 V and IIP3 = **−14.44** dBm, lower by $20\log_{10}2.5$ = **7.96** dB minus the first design's 1.94 dB, i.e. **6.02** dB.
- Noise figure: **0.086** dB for the faster device against 0.334 dB.

**Units check.** A peak EMF $v_s$ across a matched load delivers $(v_s/2)^2/(2R_s) = v_s^2/(8R_s)$.

**Sanity check.** Doubling $Q_{in}$ doubles the gate voltage for a given input: 6 dB more voltage gain and 6 dB less IIP3. The faster device's noise advantage is real but its linearity cost is the same 6 dB.

### Example 21-04.5 · A noise-cancelling wideband LNA (tier C)

**Setup.** A common-gate/common-source LNA has $g_{m1}$ = 20 mS, $g_{m2}$ = 100 mS and $R_2$ = 200 Ω, with $x$ = 2/3. (a) Choose $R_1$ for cancellation. (b) Find the voltage gain and noise figure. (c) Compare with the common-gate stage alone. (d) What current does M2 need at $g_m/I_D$ = 10 S/A?

**Solution.**

- (a) $R_1 = g_{m2}R_2R_s = 0.1 \times 200 \times 50$ = **1000** Ω.
- (b) Gain $g_{m2}R_2$ = **20** (26 dB). $F = 1 + (2/3)/5 + 1/20 + 1/(0.01 \times 200 \times 50) = 1 + 0.133 + 0.05 + 0.01$ = **1.193**: NF = **0.768** dB.
- (c) The common gate alone gives 2.22 dB (Example 1), so cancellation saves **1.45** dB.
- (d) $I_D = g_{m2}/(g_m/I_D)$ = **10** mA for M2 alone.

**Units check.** $g_mR$ dimensionless; S/(S/A) = A.

**Sanity check.** ngspice gives 0.768 dB (§5). The noise figure is now set by M2's $g_{m2}R_s = 5$; doubling $g_{m2}$ (and the current) would approach 0.4 dB. Wideband low noise is bought with current.

### Example 21-04.6 · How much LNA gain? (tier B)

**Setup.** An LNA with a 1.0 dB noise figure is followed by a mixer with a 10 dB noise figure. What LNA gain keeps the cascade within 0.3 dB of the LNA's noise figure? What does 15 dB of gain give?

**Solution.**

- $F_1$ = 1.259, $F_2$ = 10: $G_1 = 9/[1.259(10^{0.03} - 1)]$ = 99.96, i.e. **20.0** dB.
- With 15 dB: $F = 1.259 + 9/31.62$ = 1.543, NF = **1.89** dB, **0.89** dB worse than the LNA alone.

**Units check.** All ratios.

**Sanity check.** Five decibels less LNA gain costs 0.9 dB of noise figure: the gain is not optional, but beyond about 20 dB it buys little (Problem 21-04.8).

### Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 21-04.1a | resistive termination NF | 3.01 | dB |
| Ex 21-04.1b | CG transconductance for match | 20 | mS |
| Ex 21-04.1c | CG noise factor, x = 2/3 | 1.667 | — |
| Ex 21-04.1d | CG noise figure, x = 2/3 | 2.22 | dB |
| Ex 21-04.1e | CG noise factor, x = 1 | 2 | — |
| Ex 21-04.1f | CG noise figure, x = 1 | 3.01 | dB |
| Ex 21-04.2a | Cgs | 530.5 | fF |
| Ex 21-04.2b | Ls | 0.663 | nH |
| Ex 21-04.2c | Lg + Ls | 8.289 | nH |
| Ex 21-04.2d | Lg | 7.626 | nH |
| Ex 21-04.2e | Qin | 1.25 | — |
| Ex 21-04.2f | Gm | 50 | mS |
| Ex 21-04.2g | noise factor | 1.080 | — |
| Ex 21-04.2h | noise figure | 0.334 | dB |
| Ex 21-04.2i | voltage gain into 200 ohm | 10 | — |
| Ex 21-04.2j | NF without the halving | 1.21 | dB |
| Ex 21-04.3a | rg at Q 10 | 11.73 | Ω |
| Ex 21-04.3b | NF at Q 10 | 1.32 | dB |
| Ex 21-04.3c | rg at Q 15 | 7.77 | Ω |
| Ex 21-04.3d | Lg at Q 15 | 7.729 | nH |
| Ex 21-04.3e | Ls at Q 15 | 0.560 | nH |
| Ex 21-04.3f | NF at Q 15 | 1.01 | dB |
| Ex 21-04.3g | rg at Q 30 | 3.86 | Ω |
| Ex 21-04.3h | NF at Q 30 | 0.68 | dB |
| Ex 21-04.4a | IIP3, f_T 12 GHz | −8.42 | dBm |
| Ex 21-04.4b | Qin, f_T 24 GHz | 2.5 | — |
| Ex 21-04.4c | IIP3, f_T 24 GHz | −14.44 | dBm |
| Ex 21-04.4d | 20 log Qin at 2.5 | 7.96 | dB |
| Ex 21-04.4e | IIP3 difference | 6.02 | dB |
| Ex 21-04.4f | NF, f_T 24 GHz | 0.086 | dB |
| Ex 21-04.5a | R1 | 1000 | Ω |
| Ex 21-04.5b | voltage gain | 20 | — |
| Ex 21-04.5c | noise factor | 1.193 | — |
| Ex 21-04.5d | noise figure saving over CG | 1.45 | dB |
| Ex 21-04.5e | noise figure | 0.768 | dB |
| Ex 21-04.5f | M2 current | 10 | mA |
| Ex 21-04.6a | LNA gain for 0.3 dB | 20.0 | dB |
| Ex 21-04.6b | cascade NF with 15 dB | 1.89 | dB |
| Ex 21-04.6c | degradation with 15 dB | 0.89 | dB |
| Txt 21-04.a | Q_in voltage gain IIP3 shift at 1.25 | 1.94 | dB |
| Txt 21-04.b | gm2 where noise cancelling beats the common gate | 32 | mS |
| Txt 21-04.c | device Fmin with gate noise, f0/fT = 0.1 | 0.32 | dB |
| Txt 21-04.d | GNSS LNA power | 4.5 | mW |
| Txt 21-04.e | base-station LNA power | 0.60 | W |
| Txt 21-04.f | PMA3-83LN+ input intercept at +6 V | 13.1 | dBm |
| Txt 21-04.g | PMA3-83LN+ input intercept at +5 V | 8.7 | dBm |

## 5. Simulate it

The lab ([labs/21-04-lab](../labs/21-04-lab/README.md)) collects the design formulas in `lna.py` and confirms four noise figures with ngspice's noise analysis (`lna_noise.cir`), using a trick worth knowing: each transistor's channel noise is generated by a resistor in a separate loop and copied between drain and source by a current-controlled current source, so the transconductance itself stays noiseless.

**Predict, then run.**

1. Predict the 10 dB return-loss band of Example 21-04.2's input from its loop Q, then sweep the input impedance (Part 1).
2. Predict the gate-inductor Q at which the noise figure reaches 1 dB, then sweep Q with re-matching (Part 2).
3. Predict how the noise figure and the IIP3 penalty change when $f_T$ doubles at fixed $g_m$, then sweep $f_T$ (Part 3).
4. Predict the noise-cancelling LNA's noise figure at 50, 100 and 200 mS, and its sensitivity to $R_1$, then compute both (Part 4).
5. Predict the four noise figures of `lna_noise.cir`, then run `ngspice -b lna_noise.cir` (Part 5).

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Gate-inductor quality (off-chip, thick metal, shield) | Noise figure (often the largest single term) | Pins, board area, die area, cost | RF designer and package engineer |
| Input-network $Q_{in}$ (device $f_T$, $C_{gs}$) | Gain, noise figure | IIP3 (20 log $Q_{in}$), bandwidth, sensitivity to tolerances | RF designer |
| LNA gain | Cascade noise figure (Friis) | Cascade IIP3, blocker tolerance | RF system architect |
| Bias current | $f_T$ and $g_m$, hence noise and linearity | Power, battery life | RF designer and product owner |
| Narrowband (inductive) versus wideband (noise-cancelling, CG) | Noise at one band versus coverage of many | Inductor area versus current | Transceiver architect |
| Cascode | Reverse isolation, stability, gain | Headroom, one more device's noise and parasitics | RF designer |

## 7. Numbers to know

| Quantity | Typical value | Note |
|---|---|---|
| Resistive termination | NF ≥ 3.01 dB | Before any amplifier noise |
| Common-gate input at match | $1 + \gamma/\alpha$: 2.2 dB ($\gamma/\alpha$ = 2/3) to 3.0 dB (1) | Match fixes $g_m = 1/R_s$ |
| Long-channel noise constants | $\gamma$ = 2/3, $\delta$ = 4/3, $\lvert c\rvert$ = 0.395 | Short-channel values contested (§9) [8] |
| Device $F_{min}$ with induced gate noise | $1 + 2(\omega_0/\omega_T)\sqrt{\delta\gamma(1 - \lvert c\rvert^2)/5}$: **0.32** dB at $f_0/f_T$ = 0.1 | Long-channel constants [3, 8] |
| Discrete GNSS LNA | NF 0.55 dB typ (1.0 max), gain 19.6 dB, 2.5 mA at 1.8 V (**4.5** mW) | Infineon BGA524N6, 2021 [R-373] |
| Base-station LNA | NF 0.6 dB typ (1.0 max), gain 34 dB, 120 mA at 5 V (**0.60** W) | Skyworks SKY67177-11, Aug 2025 [R-373] |
| mmWave CMOS LNA research | minimum NF about 2.2–3.6 dB at 28–40 GHz; 3.4–6.5 dB at 70–86 GHz | 2023–2026 papers [R-372] |
| Single-chip 77 GHz radar receiver | NF 12–15 dB (whole receive chain) | TI data sheets [R-373] |
| Published CMOS LNAs surveyed | about 500 over 20 years; more than 30 figures of merit in use | Belostotski and Klumperink, 2022 [8] |

## 8. Common mistakes

- **Matching with a resistor and expecting low noise.** A resistive termination costs at least 3 dB.
- **Forgetting the gate inductor's loss.** An on-chip $L_g$ with $Q$ of 10 can add a decibel; budget it before choosing the device.
- **Designing $\omega_TL_s = R_s$ and then adding $r_g$.** Re-match so that $r_g + \omega_TL_s = R_s$, or the input moves off 50 Ω.
- **Quoting the drain-noise-only noise figure as the answer.** Induced gate noise, the inductors' loss, the pads and ESD protection, and the cascode all add; the textbook formula is a floor, not a prediction.
- **Maximizing $Q_{in}$ for gain.** Every doubling costs 6 dB of IIP3 and narrows the match.
- **Giving the LNA more gain than the next stage needs.** Past the Friis requirement, gain buys little noise figure and costs linearity.
- **Assuming noise cancellation is free.** It needs current in the cancelling path and gain matching across the band.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **The classic designs are three decades old [Established].** Shaeffer and Lee's 1997 inductively degenerated CMOS LNA for GPS gave 22 dB of gain and a 3.5 dB noise figure from 30 mW at 1.5 V in 0.6 µm CMOS, with the first careful treatment of induced gate noise; a correction to the paper appeared in 2005 [1]. Bruccoleri, Klumperink and Nauta's 2004 noise-cancelling LNA addressed the "fundamental tradeoff between noise figure (NF) and source impedance matching, which limits the NF to values typically above 3 dB" and reached under 2.4 dB from 150 to 2000 MHz with 13.7 dB of gain at 14 mA from 2.5 V [4]. Belostotski and Haslett's 2007 radio-astronomy LNA reached "sub-0.2 dB noise figure from 800 MHz to 1400 MHz" in 90 nm CMOS, but with a source resistance chosen for noise and presented by custom antenna elements, not 50 Ω [5].
- **The short-channel noise factor is disputed [Contested].** Abidi reported in 1986 that submicrometre MOSFETs were noisier "by factors of 2 to 4" than long-channel theory [6]; later models added velocity saturation and hot carriers. Scholten and colleagues at Philips found "only a moderate enhancement of the drain current noise for short-channel MOSFETs", attributing much of the excess to gate resistance [7]. We found no recent FinFET or FDSOI measurement that settles a value; foundry models, checked against measured LNAs, are the practical answer.
- **Removing the lossy gate inductor is still an active research goal [Established].** A 2025 6.8 GHz CMOS LNA reached 2.8 dB and 13.6 dB of gain at 1.2 mW by moving the noise and input match away from an on-chip gate inductor [9], the loss mechanism of §3.5.
- **mmWave LNAs pay in noise figure [Established per paper].** Recent CMOS designs report minimum noise figures of 2.2 dB at 36.5 GHz (65 nm, 22 mA at 1 V) and 3.36 dB at 77 GHz (22 nm, 18.6 mW); a 60–74 GHz 22 nm FDSOI LNA reports 2.32 dB minimum but 3.23 dB averaged over its band; a 70–86 GHz noise-cancelling design reports 4.8 to 6.5 dB; and a 100 GHz SiGe LNA gives 4 dB at 23.5 mW or 6.3 dB at 3.8 mW [10].
- **Discrete parts reach well under 1 dB [Established].** Infineon's SiGe GNSS LNA BGA524N6 specifies 0.55 dB typical (1.0 dB maximum) at 2.5 mA; Skyworks' SKY67177-11 base-station LNA specifies 0.6 dB typical with 34 dB of gain at about 120 mA from 5 V, and a bypass mode for strong signals; Mini-Circuits' PMA3-83LN+ quotes 1.3 dB at 2 GHz with a high output intercept [12].
- **Integrated receivers trade noise figure for cost [Established].** TI's single-chip 77 GHz radars specify 12 to 15 dB for the whole receive chain [12], and a 2024 Bluetooth LE receiver drops the LNA altogether, reaching an 8.5 dB noise figure at 167 µW in total [11].

> **Deeper:** see companion repo *Quantum Computing* for cryogenic CMOS LNAs used in qubit readout, where noise temperatures of a few kelvin, not noise figures, are the language.

### Why it matters commercially

- **Every phone, watch and car has GNSS and cellular LNAs**, and base stations have one per antenna element in massive-MIMO arrays; LNA sockets are high-volume and contested on tenths of a decibel.
- **Power differs by a factor of a hundred for similar noise figures.** The GNSS LNA above draws about 4.5 mW, the base-station LNA about 0.6 W, for 0.55 and 0.6 dB: the difference buys gain, linearity and ruggedness, which is what the application pays for.
- **Integration moves the LNA's cost elsewhere.** A system-on-chip without an external LNA saves a part and a matching network but gives up noise figure; whether that is acceptable depends on the standard's sensitivity margin (21-03 Problem 8).

### Marketing vs Reality

- **"0.55 dB noise figure."** On the BGA524N6 data sheet it is typical, at 1.8 V and 25 °C, with "PCB losses are subtracted" and "Verification based on AQL; not 100% tested in production"; the maximum is 1.0 dB [12]. Your board, connector and ESD losses before the LNA add to it decibel for decibel.
- **Front-page numbers mix conditions.** The same data sheet's headline −12 dBm compression point and −4 dBm out-of-band IIP3 come from its 2.8 V table; at 1.8 V they are −16 and −5 dBm. The PMA3-83LN+'s headline +35 dBm IP3 is at +6 V and is an *output* intercept: subtracting its 22.1 dB gain gives an input intercept of about **13.1** dBm, and at +5 V the output intercept is +30.0 dBm (about **8.7** dBm at the input) [12].
- **"Sub-0.2 dB noise figure."** True, for a source impedance chosen for noise rather than 50 Ω [5]. A noise figure is meaningful only with its source impedance (21-03 §3.2).
- **Minimum versus average.** Papers headline the best frequency: the 60 GHz-band LNA above reports 2.32 dB minimum and 3.23 dB averaged over its band [10]. With more than 30 figures of merit in use, authors can also choose a flattering one [8].

### Questions for engineering leaders

1. **"What is the noise figure at the antenna connector, not at the LNA pins?"** *Strong:* itemizes switch, filter, ESD and trace losses, gives a Friis cascade, separates measured from de-embedded values, and quotes a maximum over temperature. *Evasive:* quotes the data-sheet typical.
2. **"Which blocker scenario sets the LNA's linearity, and what is its IIP3 in the gain mode used there?"** *Strong:* names the standard's blocking test, the gain step or bypass mode used at high signal levels, and the margin. *Evasive:* "Our OIP3 is +35 dBm."
3. **"How did you model the transistor noise ($\gamma$, gate resistance), and how close was the prediction to silicon?"** *Strong:* names the model, the measured-versus-simulated noise figure difference and the de-embedding method, and acknowledges that short-channel noise is contested. *Evasive:* "The PDK handles it."
4. **"Where is the gate inductor, and what is its Q at the operating frequency?"** *Strong:* gives the Q, its contribution to the noise figure and the reason for on- or off-chip placement. *Evasive:* "It's integrated."
5. **"Why does your integrated receiver need, or not need, an external LNA?"** *Strong:* computes sensitivity from noise figure and required SNR against the standard, and the current and cost of each option. *Evasive:* "Integration is always better."

## 10. Concept check

**Q1.** Why does matching an LNA input with a 50 Ω resistor cost at least 3 dB of noise figure?

<details><summary>Answer</summary>

The resistor is a noise source at the same temperature as the source resistance, and the two form a divider: the resistor contributes as much noise at the amplifier's input as the source does, while only the source carries the signal. The output noise is twice the source's share, so $F \ge 2$.

</details>

**Q2.** Where does the inductively degenerated LNA's real input impedance come from?

<details><summary>Answer</summary>

From the transconductance current flowing in the source inductor. The gate current charges $C_{gs}$, the resulting $g_mv_{gs}$ flows through $L_s$, and the voltage it develops is in phase with the input current: $Z_{in}$ gains a real part $g_mL_s/C_{gs} = \omega_TL_s$ without a resistor.

</details>

**Q3.** Why is the effective transconductance $\omega_T/(2\omega_0R_s)$ independent of the transistor's width?

<details><summary>Answer</summary>

Widening the device raises $g_m$ and $C_{gs}$ together. The larger $C_{gs}$ lowers the input network's voltage gain $Q_{in}$ in proportion, so $g_mQ_{in}$, the effective transconductance, is unchanged; only $\omega_T = g_m/C_{gs}$ matters.

</details>

**Q4.** Half the drain noise reaches the output of a matched inductively degenerated LNA. Why half?

<details><summary>Answer</summary>

The noise current also flows through $L_s$, driving the input loop, whose total resistance at resonance is $2R_s$. The resulting gate voltage makes the transistor conduct $-(\omega_TL_s/2R_s)i_{nd} = -i_{nd}/2$, which cancels half the noise current at the drain.

</details>

**Q5.** A colleague doubles the device's $f_T$ (at the same $g_m$) to lower the noise figure. What does the LNA lose?

<details><summary>Answer</summary>

$C_{gs}$ halves, so $Q_{in}$ doubles: the gate sees twice the voltage for a given input, so IIP3 falls by 6 dB, and the match's bandwidth narrows. The noise figure gain is real but small if it was already well below 1 dB.

</details>

**Q6.** What does a noise-cancelling LNA cancel, and what does it not?

<details><summary>Answer</summary>

It cancels the noise of the matching device (the common-gate transistor), which appears at the two outputs in phase while the signal appears in antiphase. It does not cancel the noise of the cancelling path's own transistor or of the load resistors; those set the remaining noise figure, which falls as the cancelling transistor's $g_m$ (and current) rises.

</details>

Problems: [21-04 problem set](../problems/21-04-problems.md) · Worked solutions: [21-04 solutions](../solutions/21-04-solutions.md)

## 11. Key terms

[Low-noise amplifier (LNA)](../../../reference/glossary.md#low-noise-amplifier-lna) · [Inductive source degeneration](../../../reference/glossary.md#inductive-source-degeneration) · [Common-gate amplifier](../../../reference/glossary.md#common-gate-amplifier) · [Channel noise factor (gamma)](../../../reference/glossary.md#channel-noise-factor-gamma) · [Induced gate noise](../../../reference/glossary.md#induced-gate-noise) · [Noise-cancelling LNA](../../../reference/glossary.md#noise-cancelling-lna) · [Cascode](../../../reference/glossary.md#cascode) · [Noise figure](../../../reference/glossary.md#noise-figure)

## 12. Connections

- **Builds on:** [21-03](21-03-noise-figure-and-linearity.md) (noise factor, Friis, IIP3), [21-02](21-02-impedance-matching-networks.md) (matching, inductor Q), [12-03](../../12-electronics-2/chapters/12-03-frequency-response-miller-poles-zeros.md) ($C_{gs}$, $f_T$), [12-10](../../12-electronics-2/chapters/12-10-noise-in-circuits.md) (channel noise).
- **Next:** [21-05](21-05-mixers.md) converts the amplified signal to a lower frequency.
- **Used later:** front-end modules in [21-09](21-09-rf-front-end.md), phased-array receivers in [21-10](21-10-antennas-arrays-mmwave.md), link budgets in [21-11](21-11-link-budgets.md).

## 13. Further study

- B. Razavi, *RF Microelectronics*, 2nd ed., Prentice Hall, 2012: the LNA chapter (topologies, inductive degeneration, noise cancelling, linearity).
- T. H. Lee, *The Design of CMOS Radio-Frequency Integrated Circuits*, 2nd ed., Cambridge University Press, 2004: the LNA chapter, including induced gate noise and the power-constrained optimum.

## 14. Sources

1. D. K. Shaeffer and T. H. Lee, "A 1.5-V, 1.5-GHz CMOS low noise amplifier," *IEEE J. Solid-State Circuits*, vol. 32, no. 5, pp. 745–759, May 1997, DOI 10.1109/4.568846; corrections in vol. 40, no. 6, pp. 1397–1398, Jun. 2005, DOI 10.1109/JSSC.2005.848626 [R-371].
2. B. Razavi, *RF Microelectronics*, 2nd ed., Prentice Hall, 2012.
3. T. H. Lee, *The Design of CMOS Radio-Frequency Integrated Circuits*, 2nd ed., Cambridge University Press, 2004.
4. F. Bruccoleri, E. A. M. Klumperink and B. Nauta, "Wide-band CMOS low-noise amplifier exploiting thermal noise canceling," *IEEE J. Solid-State Circuits*, vol. 39, no. 2, pp. 275–282, Feb. 2004, DOI 10.1109/JSSC.2003.821786 [R-371].
5. L. Belostotski and J. W. Haslett, "Sub-0.2 dB noise figure wideband room-temperature CMOS LNA with non-50 Ω signal-source impedance," *IEEE J. Solid-State Circuits*, vol. 42, no. 11, pp. 2492–2502, Nov. 2007, DOI 10.1109/JSSC.2007.907172 [R-371].
6. A. A. Abidi, "High-frequency noise measurements on FET's with small dimensions," *IEEE Trans. Electron Devices*, vol. 33, no. 11, pp. 1801–1805, Nov. 1986, DOI 10.1109/T-ED.1986.22743 [R-371].
7. A. J. Scholten et al., "Noise modeling for RF CMOS circuit simulation," *IEEE Trans. Electron Devices*, vol. 50, no. 3, pp. 618–632, Mar. 2003, DOI 10.1109/TED.2003.810480 [R-371].
8. L. Belostotski and E. A. M. Klumperink, "Figures of merit for CMOS low-noise amplifiers and estimates for their theoretical limits," *IEEE Trans. Circuits Syst. II*, vol. 69, no. 3, pp. 734–738, Mar. 2022, DOI 10.1109/TCSII.2021.3113607 [R-371].
9. P. B. T. Huynh, G.-S. Lee, J.-Y. Park and T.-Y. Yun, "An inductive loading simultaneous noise and input matching technique with current reuse for low-power LNA," *IEEE J. Solid-State Circuits*, vol. 60, no. 7, pp. 2461–2472, Jul. 2025, DOI 10.1109/JSSC.2024.3511578 [R-372].
10. mmWave LNAs: J.-H. Kim et al., RFIC 2023, pp. 125–128, DOI 10.1109/RFIC54547.2023.10186167; J. Deng et al., RFIC 2026, pp. 215–218, DOI 10.1109/RFIC70222.2026.11602368; B. Lin et al., *IEEE JSSC*, vol. 61, no. 5, pp. 1752–1763, May 2026, DOI 10.1109/JSSC.2025.3646869; C. Han, J. Zhou and X. Luo, *IEEE JSSC*, vol. 60, no. 3, pp. 1030–1042, Mar. 2025, DOI 10.1109/JSSC.2024.3440053; K. Smirnova et al., *IEEE MWTL*, vol. 33, no. 8, pp. 1171–1174, Aug. 2023, DOI 10.1109/LMWT.2023.3279574 [R-372].
11. H. Shao, R. P. Martins and P.-I. Mak, "A 167-µW 71.7-dB SFDR 2.4-GHz BLE receiver using a passive quadrature front end, a double-sided double-balanced cascaded mixer, and a dual-transformer-coupled class-D VCO," *IEEE J. Solid-State Circuits*, vol. 59, no. 12, pp. 3980–3992, Dec. 2024, DOI 10.1109/JSSC.2024.3462093 [R-372].
12. Data sheets: Infineon BGA524N6 (Rev. 3.5, Aug 2021); Skyworks SKY67177-11 (205909M, Aug 2025); Mini-Circuits PMA3-83LN+ (Rev. E, 2024); Texas Instruments AWR2944 (SWRS273E, rev. Feb 2026) and AWR1843 (SWRS222D, rev. Sep 2024) [R-373].
