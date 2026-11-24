<!-- status: verified -->
# 21-02 · Impedance Matching Networks

| | |
|---|---|
| **Course** | [21 · RF and Microwave Engineering](../README.md) |
| **University equivalent** | The impedance-matching chapter of a senior microwave or RF circuits course: matching complex loads, π and T networks with a chosen Q, multi-section and wideband matching, multi-section quarter-wave transformers, losses from finite component Q, and the Bode–Fano limit (Pozar, *Microwave Engineering*, the impedance-matching chapter; Lee, *The Design of CMOS Radio-Frequency Integrated Circuits*, the matching and passive-component chapters) |
| **Prerequisites** | [13-09](../../13-electromagnetics/chapters/13-09-smith-chart-and-matching.md) (Smith chart, L-networks, single stubs, Bode–Fano), [21-01](21-01-s-parameters.md) (reflection, S-parameters), [07-08](../../07-circuit-analysis-2-transient-and-ac/chapters/07-08-filters-and-resonance.md) (resonance and Q) |
| **Estimated study hours** | 7 |
| **Last verified** | 2026-11-24 |

**Learning objectives.** After this chapter you can:

1. Match a complex load with an L-network by absorbing or resonating its reactance.
2. Design π and T networks for a chosen loaded Q, and explain when a higher Q is worth its narrower bandwidth.
3. Widen a match with multiple L-sections or a multi-section quarter-wave transformer, and compute the bandwidth gained.
4. Derive the insertion loss a match suffers from finite component Q, and see why large transformation ratios are lossy.
5. Use the Bode–Fano limit to tell whether a requested bandwidth is achievable at all.

## 1. Big picture

Chapter 13-09 showed that two reactances can match any resistance to any other at one frequency. Real designs ask more: the load is complex (a transistor's input capacitance, an antenna's reactance), the match must hold over a band (a 5G band of hundreds of megahertz, a Wi-Fi channel, an ultra-wideband pulse), it must filter harmonics (a power amplifier), and its own components lose power (an on-chip inductor with a Q of ten). This chapter turns the two-element L-network into a design discipline: choose the topology and Q for the job, spread a large transformation over several sections, count the loss, and check the fundamental limit before promising a bandwidth.

- **Every amplifier** has an input and an output match (21-04, 21-07); the matching network often sets the bandwidth and much of the loss.
- **Power amplifiers** must transform a 50 Ω antenna down to a few ohms, a large ratio that makes the match lossy and narrow.
- **Antennas in phones and wearables** are electrically small and highly reactive; their bandwidth is limited by Bode–Fano, which is why phones use tunable matching (21-09).
- **On-chip matching** uses spiral inductors of modest Q (best cases near 40, §9), so a few tenths of a dB to over a dB can disappear in the match itself.

## 2. Intuition first

```text
  R_low ──[ series X ]──┬── R_high        one big step: Q = √(R_high/R_low − 1)  (steep, narrow)
                        ═ shunt B
  R_low ──[X1]──┬──[X2]──┬── R_high       two small steps through √(R_low·R_high): lower Q each (gentle, wide)
                ═ B1      ═ B2
```

*Figure 1. One big impedance step or several small ones. The Q of each L-section is set by the ratio it transforms; splitting a large ratio into geometric steps lowers each section's Q and widens the band.*

**A gearbox analogy.** A matching network is a gearbox between an engine (the source impedance) and wheels (the load). One gear pair can make any ratio, but a large ratio in one stage is stiff and works well only near one speed (frequency); several stages with modest ratios run smoothly over a wider range, at the cost of more parts, each with its own friction (component loss). The analogy breaks because an electrical match also has a hard theoretical ceiling, Bode–Fano, set by the load's own stored energy: no gearbox, however elaborate, beats it.

## 3. Theory

### 3.1 The L-network revisited

From 13-09: to transform $R_{low}$ up to $R_{high}$, put a series reactance $X$ next to $R_{low}$ and a shunt susceptance $B$ across $R_{high}$, with

$$
Q = \sqrt{\frac{R_{high}}{R_{low}} - 1}, \qquad \lvert X\rvert = QR_{low}, \qquad \lvert B\rvert = \frac{Q}{R_{high}} ,
$$

and opposite signs (an inductor and a capacitor). The low-pass form (series L, shunt C) also filters harmonics; the high-pass form (series C, shunt L) passes DC blocking and bias. The network's Q is fixed by the resistance ratio, and so is its bandwidth: roughly, the match degrades over a fractional bandwidth of order $1/Q$. Here is how wide.

**The bandwidth of one L-section.** Take the low-pass form and detune by a fraction δ, $\omega = \omega_0(1 + \delta)$. Normalized to the 50 Ω side, the input admittance is $y = R_{high}\left[j\omega C + 1/(R_{low} + j\omega L)\right]$, which equals 1 at δ = 0. Differentiate at δ = 0 using $\omega_0L = QR_{low}$, $\omega_0C = Q/R_{high}$ and $R_{high} = R_{low}(1 + Q^2)$: the capacitor contributes $jQ$, and the series branch contributes $-jQ(1 - jQ)^2/(1 + Q^2)$. Adding them,

$$
y \approx 1 + \delta\,\frac{2Q^2}{1 + Q^2}\,(jQ - 1), \qquad \Gamma = \frac{1 - y}{1 + y} \approx -\delta\,\frac{Q^2(jQ - 1)}{1 + Q^2} ,
$$

so $\lvert\Gamma\rvert \approx \lvert\delta\rvert\,Q^2/\sqrt{1 + Q^2}$, and the band where $\lvert\Gamma\rvert \le \Gamma_m$ has a fractional width

$$
\frac{\Delta f}{f_0} \approx \frac{2\Gamma_m\sqrt{1 + Q^2}}{Q^2} \;\to\; \frac{2\Gamma_m}{Q} \quad (Q \gg 1) .
$$

For Example 21-02.1 ($Q$ = 2, $\Gamma_m$ = 0.316) this first-order estimate gives **35.4**%, against **38.0**% from the exact sweep: away from the center $\lvert\Gamma\rvert$ grows a little more slowly than linearly, so the estimate is slightly pessimistic. Either way, bandwidth is inversely proportional to Q.

### 3.2 Complex loads: absorb or resonate

A load $Z_L = R_L + jX_L$ adds its own reactance. Two ways to handle it:

- **Absorption.** Treat $X_L$ as part of the network's series element: design the L-network for $R_L$, then add a series reactance $X - X_L$. For a shunt-type load (a resistor in parallel with a capacitor), absorb the load's susceptance into the network's shunt element the same way.
- **Resonance.** First cancel $X_L$ with an equal and opposite reactance at the operating frequency, then match the remaining resistance. This always works but adds an element and narrows the bandwidth.

Absorption is preferred when the load reactance has the right sign and is not too large; otherwise its reactance already exceeds what the network needs, and resonance (or a different topology) is required (Example 21-02.2).

### 3.3 π and T networks: choosing the Q

An L-network has no free parameter. A three-element network (π: shunt–series–shunt, or T: series–shunt–series) adds one, which sets the **loaded Q** independently of the resistance ratio. View a π network as two L-networks back to back through a **virtual resistance** $R_v$ smaller than both terminations:

$$
R_v = \frac{R_{high}}{Q^2 + 1}, \qquad Q_1 = \sqrt{\frac{R_1}{R_v} - 1}, \quad Q_2 = \sqrt{\frac{R_2}{R_v} - 1} ,
$$

with shunt susceptances $Q_1/R_1$ and $Q_2/R_2$ at the two ends and a series reactance $(Q_1 + Q_2)R_v$ in the middle (the two halves' series reactances add). A T network does the same through a virtual resistance larger than both. A higher Q gives a narrower bandwidth and more harmonic rejection, which is why power-amplifier output networks are often π networks with a moderate loaded Q. The cost is sensitivity: a high-Q network detunes more for a given component tolerance, and loses more power in its components (§3.5).

### 3.4 Wider bandwidth: several small steps

To widen the band, transform in several steps. With $n$ L-sections and intermediate resistances in geometric progression,

$$
R_k = R_{low}\left(\frac{R_{high}}{R_{low}}\right)^{k/n}, \qquad Q_{section} = \sqrt{\left(\frac{R_{high}}{R_{low}}\right)^{1/n} - 1} ,
$$

each section's Q falls, and with it the sensitivity to frequency. Two sections from 5 Ω to 50 Ω have Q = 1.47 each instead of 3, and their 10 dB return-loss band is three times wider (Example 21-02.4, Figure 2).

![Return loss in dB against frequency from 0.8 to 4 GHz for two matches from 5 to 50 ohms at 2 GHz: one L-section peaks sharply at 2 GHz and stays above 10 dB from 1.75 to 2.22 GHz; two L-sections have two reflection zeros, near 2 and 2.8 GHz, and stay above 10 dB from 1.61 to 3.02 GHz; the two bands are shaded below a dashed 10 dB line](../../../assets/figures/21-02/sections.svg)

*Figure 2. One step or two (Example 21-02.4). Splitting a 10:1 transformation into two √10 steps lowers each section's Q from 3 to 1.47 and triples the 10 dB return-loss band.* The limit as $n \to \infty$ is a smooth taper, the lumped analog of a tapered transmission line.

**Multi-section quarter-wave transformers.** With lines instead of lumped elements, $N$ quarter-wave sections of impedances $Z_1, \ldots, Z_N$ between $Z_0$ and $Z_L$ create small reflections at each step. For small steps the total reflection is approximately the sum of the partial reflections with their phase delays,

$$
\Gamma(\theta) \approx \sum_{n=0}^{N}\Gamma_ne^{-2jn\theta}, \qquad \Gamma_n \approx \tfrac12\ln\frac{Z_{n+1}}{Z_n} ,
$$

where θ is each section's electrical length (90° at the design frequency). Choosing the $\Gamma_n$ proportional to binomial coefficients, $\Gamma_n = 2^{-N}\binom{N}{n}\tfrac12\ln(Z_L/Z_0)$, makes $\Gamma(\theta) \propto \cos^N\theta$: maximally flat at the center. Its magnitude is $2^N\lvert A\rvert\,\lvert\cos\theta\rvert^N$ with $A \approx 2^{-N}(Z_L - Z_0)/(Z_L + Z_0)$, so the band where $\lvert\Gamma\rvert \le \Gamma_m$ has edges at $\cos\theta_m = \tfrac12(\Gamma_m/\lvert A\rvert)^{1/N}$ and a fractional width

$$
\frac{\Delta f}{f_0} = 2 - \frac{4\theta_m}{\pi} .
$$

This small-reflection result slightly overstates the bandwidth (by about a percentage point in Example 21-02.6) because it neglects multiple reflections between steps. Chebyshev (equal-ripple) transformers trade a small in-band ripple for more bandwidth at the same N [10].

### 3.5 Losses from finite component Q

Real inductors and capacitors have an unloaded quality factor $Q_u = X/r$ (series resistance $r$). In an L-network the series inductor carries the full current of the low-resistance side, so its loss resistance $r = X/Q_u = Q_nR_{low}/Q_u$ sits in series with $R_{low}$, where $Q_n$ is the network's Q. The fraction of power reaching the load is $R_{low}/(R_{low} + r)$, an insertion loss of

$$
\text{IL} = 10\log_{10}\left(1 + \frac{Q_n}{Q_u}\right)\ \text{dB}
$$

from the inductor, plus a similar term from the capacitor's (usually higher) Q. The lesson is the ratio $Q_n/Q_u$: large transformation ratios (high $Q_n$) with on-chip inductors (low $Q_u$) lose a lot. A $Q_n = 3$ match with a $Q_u = 8$ on-chip inductor loses 1.38 dB, a quarter of the power (Example 21-02.5). This is why high-power amplifiers put their output match off chip or use transformers, and why multi-section matches, with lower $Q_n$ per section, also help with loss (Figure 3).

![Insertion loss in dB against inductor unloaded Q from 3 to 200 on a logarithmic axis, for network Q of 1, 2, 3 and 5: every curve falls as the inductor Q rises, and higher network Q sits higher; three dots mark the cases of Example 21-02.5 at 0.54, 0.79 and 1.38 dB](../../../assets/figures/21-02/loss.svg)

*Figure 3. Inductor loss in a match, $10\log_{10}(1 + Q_n/Q_u)$. What matters is the ratio of the network's Q to the component's.*

### 3.6 The Bode–Fano limit

Chapter 13-09 stated the Bode–Fano integral for a load of R in parallel with C [1, 2]:

$$
\int_0^\infty\ln\frac{1}{\lvert\Gamma(\omega)\rvert}\,d\omega \le \frac{\pi}{RC} .
$$

No lossless network, however many elements it has, does better. The best use of this "reflection budget" is a constant $\lvert\Gamma\rvert = \Gamma_m$ over a band Δω and total reflection ($\ln 1 = 0$) elsewhere. The integral is then just $\Delta\omega\ln(1/\Gamma_m) \le \pi/(RC)$, which with $\Delta\omega = 2\pi\Delta f$ gives

$$
\Delta f \le \frac{1}{2RC\ln(1/\Gamma_m)} .
$$

For 50 Ω in parallel with 1 pF and $\Gamma_m$ = 0.1 (20 dB return loss), $\Delta f \le$ 4.34 GHz (Example 21-02.6). Asking for a better match (smaller $\Gamma_m$) costs bandwidth only logarithmically, but a larger load capacitance costs it in direct proportion. An electrically small antenna or a large transistor's input is high-Q by nature, and its bandwidth is limited before any matching network is designed.

> **Going deeper — where the limit comes from.** Bode's integral follows from applying Cauchy's theorem to $\ln(1/\Gamma)$ of a minimum-phase reflection, whose behaviour at infinite frequency is set by the shunt capacitor ($\Gamma \to -1 + 2/(j\omega RC)$). Fano generalized it to arbitrary loads [2], and Youla recast the theory in 1964 [3]. The bound is reached only with infinitely many elements; a few-element network gets close.

## 4. Worked examples

All examples use 50 Ω sources unless stated. "Bandwidth" means the band where the return loss is at least 10 dB ($\lvert\Gamma\rvert \le 0.316$).

### Example 21-02.1 · An L-match and its bandwidth (tier A)

**Setup.** Match a 10 Ω load to 50 Ω at 2.4 GHz with a low-pass L-network. Find the element values and the 10 dB return-loss bandwidth.

**Solution.**

- $Q = \sqrt{50/10 - 1}$ = **2**; series reactance $QR_{low}$ = **20** Ω next to the load, $L = 20/(2\pi \times 2.4\ \text{GHz})$ = **1.326** nH; shunt susceptance $Q/R_{high}$ = **0.04** S at the source side, $C$ = **2.653** pF.
- Sweeping the network's input reflection gives 10 dB return loss from **1.901** to **2.812** GHz, a fractional bandwidth of **38.0**%.

**Units check.** Ω/(rad/s) = H; S/(rad/s) = F.

**Sanity check.** A fractional bandwidth of about **0.76**/Q at this return loss: of the order 1/Q, as promised.

### Example 21-02.2 · A complex load (tier B)

**Setup.** An antenna presents 20 − j15 Ω at 900 MHz. Match it to 50 Ω with a series inductor next to the antenna and a shunt capacitor at the 50 Ω side.

**Solution.**

- For 20 Ω to 50 Ω, $Q$ = √1.5 = **1.225**; the network needs a series reactance of $QR_{low}$ = **24.49** Ω.
- The antenna already contributes −15 Ω, so the series inductor must supply 24.49 + 15 = **39.49** Ω: $L$ = **6.984** nH (absorption).
- The shunt capacitor has susceptance $Q/50$ = 0.0245 S: $C$ = **4.332** pF.
- Check: the input impedance is **50.0** + j0 Ω.

**Units check.** As in Example 1.

**Sanity check.** Had the antenna been inductive (20 + j30 Ω), its reactance would exceed the 24.49 Ω the network needs; a series capacitor would then remove the excess.

### Example 21-02.3 · A π network for a power amplifier (tier B)

**Setup.** A power amplifier needs a 10 Ω load at 2.4 GHz, matched to 50 Ω through a π network with loaded Q = 5 for harmonic rejection. Find the virtual resistance and element values, and compare the bandwidth with the simple L-network of Example 1.

**Solution.**

- $R_v = 50/(5^2 + 1)$ = **1.923** Ω. The 50 Ω half has $Q_1$ = √(50/1.923 − 1) = 5, so $B_1 = Q_1/50$ = **0.1** S; the 10 Ω half has $Q_2 = \sqrt{10/1.923 - 1}$ = 2.049, so $B_2 = Q_2/10$ = **0.205** S. The series reactance is $(Q_1 + Q_2)R_v$ = **13.56** Ω.
- The 10 dB return-loss band is **2.266**–**2.516** GHz, **10.4**%, against 38.0% for the L-network.

**Units check.** Ω and S.

**Sanity check.** Higher Q, narrower band: the price of the extra harmonic rejection.

### Example 21-02.4 · One step or two? (tier B)

**Setup.** Match 5 Ω to 50 Ω at 2 GHz with one L-section, and with two L-sections through the geometric mean. Compare Q and bandwidth.

**Solution.**

- One section: Q = √9 = **3**; band **1.750**–**2.222** GHz, **23.6**%.
- Two sections: intermediate resistance √(5 × 50) = **15.81** Ω; each section Q = √(√10 − 1) = **1.470**; band **1.609**–**3.018** GHz, **70.5**%.

**Units check.** Ratios and frequencies.

**Sanity check.** Two sections triple the bandwidth. A real PA output match of 5 Ω or less to 50 Ω therefore usually has two or three sections.

### Example 21-02.5 · What the match itself costs (tier B)

**Setup.** Find the insertion loss due to the inductor in: (a) Example 1's match ($Q_n$ = 2) with a discrete inductor of $Q_u$ = 15; (b) a $Q_n$ = 3 match with $Q_u$ = 15; (c) the same with an on-chip inductor of $Q_u$ = 8.

**Solution.** $\text{IL} = 10\log_{10}(1 + Q_n/Q_u)$:

- (a) **0.544** dB; (b) **0.792** dB; (c) **1.383** dB, **27**% of the power.

**Units check.** Dimensionless ratios.

**Sanity check.** In a power amplifier delivering 1 W, 1.38 dB of match loss is **0.27** W of heat in the inductor: a reason PA output matches use high-Q off-chip or laminate components.

### Example 21-02.6 · Bode–Fano and a two-section transformer (tier C)

**Setup.** (a) A load is 50 Ω in parallel with 1 pF. What is the widest band over which it can be matched with $\lvert\Gamma\rvert \le 0.1$? (b) A two-section binomial transformer matches 50 Ω to 100 Ω. Find its section impedances and its fractional bandwidth for $\lvert\Gamma\rvert \le 0.05$, and compare a single quarter-wave section.

**Solution.**

- (a) $\Delta f \le 1/[2RC\ln(1/0.1)]$ = 1/(2 × 50 ps × 2.303) = **4.34** GHz.
- (b) With $\ln(100/50)$ = 0.693 split in binomial proportions 1:2:1 (quarters), $Z_1 = 50e^{0.693/4}$ = **59.46** Ω and $Z_2 = 59.46e^{0.693/2}$ = **84.09** Ω. With $A = 2^{-2}(1/3)$, $\cos\theta_m = \tfrac12(0.05/0.0833)^{1/2}$ gives a fractional bandwidth of **50.6**%, against **19.2**% for one section (70.71 Ω). These come from the small-reflection approximation; cascading the exact line equations gives **49.1**% and **18.1**%, close enough for design.

**Units check.** 1/(Ω·F) = 1/s; ratios for the transformer.

**Sanity check.** Doubling the capacitance would halve the bound in (a); doubling the sections in (b) more than doubles the bandwidth here, because the binomial response is flat to higher order.

### Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 21-02.1a | Q | 2 | — |
| Ex 21-02.1b | series reactance | 20 | Ω |
| Ex 21-02.1c | L | 1.326 | nH |
| Ex 21-02.1d | shunt susceptance | 0.04 | S |
| Ex 21-02.1e | C | 2.653 | pF |
| Ex 21-02.1f | lower band edge | 1.901 | GHz |
| Ex 21-02.1g | upper band edge | 2.812 | GHz |
| Ex 21-02.1h | fractional bandwidth | 38.0 | % |
| Ex 21-02.2a | Q | 1.225 | — |
| Ex 21-02.2b | network series reactance | 24.49 | Ω |
| Ex 21-02.2c | inductor reactance | 39.49 | Ω |
| Ex 21-02.2d | L | 6.984 | nH |
| Ex 21-02.2e | C | 4.332 | pF |
| Ex 21-02.2f | input resistance | 50.0 | Ω |
| Ex 21-02.3a | virtual resistance | 1.923 | Ω |
| Ex 21-02.3b | B1 | 0.1 | S |
| Ex 21-02.3c | B2 | 0.205 | S |
| Ex 21-02.3d | series reactance | 13.56 | Ω |
| Ex 21-02.3e | lower band edge | 2.266 | GHz |
| Ex 21-02.3f | upper band edge | 2.516 | GHz |
| Ex 21-02.3g | fractional bandwidth | 10.4 | % |
| Ex 21-02.4a | one-section Q | 3 | — |
| Ex 21-02.4b | one-section lower edge | 1.750 | GHz |
| Ex 21-02.4c | one-section upper edge | 2.222 | GHz |
| Ex 21-02.4d | one-section bandwidth | 23.6 | % |
| Ex 21-02.4e | intermediate resistance | 15.81 | Ω |
| Ex 21-02.4f | section Q | 1.470 | — |
| Ex 21-02.4g | two-section lower edge | 1.609 | GHz |
| Ex 21-02.4h | two-section upper edge | 3.018 | GHz |
| Ex 21-02.4i | two-section bandwidth | 70.5 | % |
| Ex 21-02.5a | loss, Qn 2, Qu 15 | 0.544 | dB |
| Ex 21-02.5b | loss, Qn 3, Qu 15 | 0.792 | dB |
| Ex 21-02.5c | loss, Qn 3, Qu 8 | 1.383 | dB |
| Ex 21-02.5d | power lost, Qn 3, Qu 8 | 27 | % |
| Ex 21-02.6a | Bode–Fano bandwidth | 4.34 | GHz |
| Ex 21-02.6b | Z1 | 59.46 | Ω |
| Ex 21-02.6c | Z2 | 84.09 | Ω |
| Ex 21-02.6d | two-section bandwidth | 50.6 | % |
| Ex 21-02.6e | one-section bandwidth | 19.2 | % |
| Ex 21-02.6f | two-section bandwidth, exact | 49.1 | % |
| Ex 21-02.6g | one-section bandwidth, exact | 18.1 | % |
| Txt 21-02.a | bandwidth times Q | 0.76 | — |
| Txt 21-02.b | heat per watt in, Qn 3, Qu 8 | 0.27 | W |
| Txt 21-02.c | reflection magnitude at 10 dB return loss | 0.316 | — |
| Txt 21-02.d | Bode–Fano bandwidth at 10 dB return loss, 50 Ω ∥ 1 pF | 8.69 | GHz |
| Txt 21-02.e | reflection magnitude at 7 dB return loss | 0.447 | — |
| Txt 21-02.f | first-order L-section bandwidth, Q 2, 10 dB | 35.4 | % |

## 5. Simulate it

The lab ([labs/21-02-lab](../labs/21-02-lab/README.md)) collects the design formulas in `match.py`, sweeps networks with optional component Q, and confirms three networks' band edges with ngspice.

**Predict, then run.**

1. Predict the 10 dB return-loss band of Example 21-02.1 from its Q of 2, then sweep it (Part 1).
2. Predict how the bandwidth of a π network from 50 Ω to 10 Ω scales as its Q rises from 2 to 10, then plot it (Part 2).
3. Predict the bandwidths of one, two and three L-sections from 5 Ω to 50 Ω, compute them, and run `ngspice -b matchnets.cir` to confirm six band edges (Part 3).
4. Predict whether the exact bandwidths of binomial transformers lie above or below the small-reflection estimates, then compute both (Part 4).
5. Predict how many sections minimize the inductor loss from 2 Ω to 50 Ω with $Q_u$ = 20, then tabulate it, and compare the lab's bandwidths with the Bode–Fano bound for 50 Ω in parallel with 1 pF (Part 5).

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Network Q (π/T versus L) | Harmonic rejection, selectivity | Bandwidth, tolerance sensitivity, loss | RF designer |
| Number of sections | Bandwidth, loss per section | Area, component count, cost | RF designer |
| On-chip versus off-chip passives | Integration, cost, size | Component Q, so insertion loss | Product architect |
| Lumped versus distributed (lines, stubs) | Distributed: accuracy at mmWave | Distributed: size at low frequency | RF/packaging engineer |
| Tunable matching | Bandwidth across bands for small antennas | Switches' loss and linearity, control complexity | Front-end architect |

## 7. Numbers to know

| Quantity | Typical value | Note |
|---|---|---|
| L-network Q for a ratio $r = R_{high}/R_{low}$ | $\sqrt{r - 1}$: **2** at 5:1, **3** at 10:1, **4.90** at 25:1 | Bandwidth falls as 1/Q |
| 10 dB return-loss band of one L-section | about **0.76**/Q (fractional) | Example 21-02.1 |
| 10 dB return loss | $\lvert\Gamma\rvert$ = **0.316** | The usual "matched" threshold for bandwidth |
| Match loss from the inductor | $10\log_{10}(1 + Q_n/Q_u)$: 0.79 dB at $Q_n/Q_u$ = 0.2, 1.38 dB at 3/8 | Example 21-02.5 |
| Bode–Fano bound, 50 Ω ∥ 1 pF | **4.34** GHz at $\lvert\Gamma\rvert \le 0.1$; **8.69** GHz at $\lvert\Gamma\rvert \le 0.316$ | Inversely proportional to RC |
| On-chip spiral inductors | Q "up to 40" in a 1998 thick-copper process; a patterned ground shield raises Q "up to 33%" | Best cases, not typical [5, 6, R-365] |
| Spiral-inductance hand formulas | within about 3% of a field solver, against about 20% for older expressions | Mohan et al., 1999 [8, R-365] |
| LNA input return loss in data sheets | 9 dB min, 13 dB typical (a 2.6 GHz LNA); 6 dB min, 7 dB typical (a Wi-Fi 7 front-end receive path) | Dec 2023 and Sep 2024 data sheets [12, 13, R-366] |

## 8. Common mistakes

- **Ignoring the load's reactance.** Design for the complex load, by absorption or resonance.
- **Choosing a high-Q network without counting loss.** Insertion loss grows with $Q_n/Q_u$.
- **Expecting a single L-section to cover a wide band at a large ratio.** Split the ratio.
- **Promising bandwidth without checking Bode–Fano.** A reactive load caps the achievable band.
- **Forgetting component tolerances.** High-Q networks detune; simulate with tolerances.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **The limits are seventy years old [Established].** Bode's 1945 book on network analysis and feedback amplifiers gave the integral for a parallel RC load [1]; Fano's two-part 1950 paper in the *Journal of the Franklin Institute*, developed from a 1948 MIT Research Laboratory of Electronics report, extended it to arbitrary loads [2]; Youla's 1964 "new theory of broad-band matching" generalized the method [3]. Nothing since has moved the bound; what has changed is how close practical networks and tunable matching get to it.
- **The Smith chart is from 1939 [Established].** Phillip H. Smith, then an engineer in the Radio Development Department of Bell Telephone Laboratories, published it as a "Transmission Line Calculator" in *Electronics* in January 1939 [4, R-364]; every matching tool still draws it.
- **On-chip inductors set the loss of integrated matches [Established].** Burghartz and colleagues at IBM showed in 1998 that "spiral inductors with inductances of 0.5-100 nH and Q's up to 40" are feasible in silicon, with thick copper wiring, a best case rather than a typical one [5]. Yue and Wong showed that a patterned ground shield "increases the inductor quality factor up to 33%" at 1–2 GHz and reduces substrate coupling "by as much as 25 dB" [6]. Niknejad and Meyer's ASITIC tool (1998) made spiral analysis routine [7], and Mohan, Hershenson, Boyd and Lee's 1999 expressions match field solvers "typically within around 3%" [8]. Burghartz and Rejaei's 2003 review relates Q, self-resonance and area to the substrate's resistivity [9]. We found no primary source that states a "typical" standard-CMOS inductor Q: it depends on metal thickness, substrate and frequency, and this chapter's examples use 8 to 20 as working assumptions.
- **Discrete LNAs leave the match to the board [Established].** Infineon's BGA9H1BN6 (2.3–2.7 GHz) specifies 9 dB minimum and 13 dB typical input return loss at 2.6 GHz with its recommended external parts, and notes that performance "Can be tuned by using different external matching components" [12]. Qorvo's QPF4609 Wi-Fi 7 front end specifies a receive-path antenna-port return loss of 6 dB minimum and 7 dB typical alongside a 1.8 dB typical noise figure [13]: its input is matched for noise, not for power (21-03, 21-04).

### Why it matters commercially

- **Matching parts are bill-of-materials lines and board area.** Front-end modules (21-09) absorb them, which is part of what a module vendor sells; a discrete design pays for them in parts, placement and tuning time.
- **The match sets much of an amplifier's band and loss.** In a power amplifier, match loss is heat and battery drain (Example 21-02.5); in a receiver, loss before the LNA adds directly to the noise figure (21-03).
- **Small antennas are Bode–Fano limited.** In wearables and phones the antenna is electrically small and highly reactive, so its bandwidth is bounded before any network is designed; covering several bands takes tuning, not a cleverer fixed network.

### Marketing vs Reality

- **"A broadband, well-matched input."** Check it against Bode–Fano. For 50 Ω in parallel with 1 pF, no lossless network gives 20 dB return loss over more than 4.34 GHz, or 10 dB over more than 8.69 GHz. A claim beyond the bound means the network is lossy (a resistive pad, which costs gain and noise figure) or the claim is wrong.
- **"Poor" input return loss.** A 7 dB return loss is $\lvert\Gamma\rvert$ = **0.447**, which looks bad until you notice that the same part has a 1.8 dB noise figure: the input is deliberately matched to the source impedance that minimizes noise. Judge an LNA's input match against its noise and gain, not against 50 Ω alone.
- **"On-chip inductors with Q of 40."** Headline Q values come from thick-metal, shielded or high-resistivity test structures at their best frequency. Ask for Q at the operating frequency, the self-resonance margin and the area, in the process the product actually uses.
- **"Typical" data-sheet performance.** It assumes the vendor's matching network on the vendor's board. Move one capacitor on a customer's board and noise figure, gain and linearity move together.

### Questions for engineering leaders

1. **"What is the Bode–Fano bound for this load, and how close does your match get?"** *Strong:* extracts the load's R and C (or Q), computes the bound, and states the margin. *Evasive:* "We'll add more sections if we need bandwidth."
2. **"How much of your loss or noise figure is in the matching network, and with what component Q?"** *Strong:* gives $Q_u$ at the operating frequency and a loss budget per element. *Evasive:* "The match is lossless in simulation."
3. **"How do return loss, gain and noise figure move over component tolerance and board variation?"** *Strong:* shows a tolerance Monte Carlo and explains why the chosen network Q is not higher. *Evasive:* "We tune it on the bench."
4. **"Is the input matched for noise or for power, and why?"** *Strong:* explains the noise-optimal source reflection, the return loss it costs and how the system tolerates it. *Evasive:* "It's matched to 50 Ω."
5. **"Why is this match on chip (or off chip)?"** *Strong:* compares component Q, loss, area and cost with numbers. *Evasive:* "That's how the last design did it."

## 10. Concept check

**Q1.** Why does a π network let you choose Q while an L-network does not?

<details><summary>Answer</summary>

The L-network's two elements are fixed by the two conditions of a match (real and imaginary parts) at a given resistance ratio, so its Q is fixed by that ratio. A third element adds a degree of freedom: the virtual resistance, which sets the Q.

</details>

**Q2.** Why do two L-sections give more bandwidth than one?

<details><summary>Answer</summary>

Each section transforms a smaller ratio (the square root of the total), so each has a lower Q and a slower phase variation with frequency; the match degrades more gently away from the center.

</details>

**Q3.** A match with $Q_n$ = 4 uses an inductor with $Q_u$ = 20. Estimate its insertion loss.

<details><summary>Answer</summary>

$10\log_{10}(1 + 4/20)$ ≈ 0.79 dB.

</details>

**Q4.** What does the Bode–Fano limit say about matching a small antenna?

<details><summary>Answer</summary>

A small antenna stores much reactive energy relative to the power it radiates (high Q), so its "RC" is large; the achievable bandwidth for a given return loss is inversely proportional to it, regardless of the matching network.

</details>

**Q5.** When would you resonate a load's reactance rather than absorb it?

<details><summary>Answer</summary>

When the load's reactance has the wrong sign or is larger than the network's required element, so that it cannot be absorbed into the network.

</details>

Problems: [21-02 problem set](../problems/21-02-problems.md) · Worked solutions: [21-02 solutions](../solutions/21-02-solutions.md)

## 11. Key terms

[L-network](../../../reference/glossary.md#l-network) · [Quality factor](../../../reference/glossary.md#quality-factor) · [Pi network](../../../reference/glossary.md#pi-network) · [Quarter-wave transformer](../../../reference/glossary.md#quarter-wave-transformer) · [Bode–Fano limit](../../../reference/glossary.md#bode-fano-limit) · [Insertion loss](../../../reference/glossary.md#insertion-loss)

## 12. Connections

- **Builds on:** [13-09](../../13-electromagnetics/chapters/13-09-smith-chart-and-matching.md) (Smith chart, L-networks), [21-01](21-01-s-parameters.md) (reflection and S-parameters).
- **Next:** [21-03](21-03-noise-figure-and-linearity.md) adds noise and linearity to the figures a front end must meet.
- **Used later:** LNA input matching ([21-04](21-04-low-noise-amplifiers.md)), PA output networks ([21-07](21-07-power-amplifiers.md)), antenna tuning ([21-09](21-09-rf-front-end.md)).

## 13. Further study

- D. M. Pozar, *Microwave Engineering*, 4th ed., Wiley, 2012: the impedance-matching chapter (L-sections, stubs, multi-section transformers, Bode–Fano).
- T. H. Lee, *The Design of CMOS Radio-Frequency Integrated Circuits*, 2nd ed., Cambridge, 2004: the chapters on passive components and matching.
- R. M. Fano's 1950 paper [2] for the full broadband-matching theory, and Mohan et al. [8] for spiral-inductance formulas that are accurate enough for hand design.

## 14. Sources

1. H. W. Bode, *Network Analysis and Feedback Amplifier Design*, D. Van Nostrand, 1945 (bibliographic entry confirmed; the book was not read) [R-364].
2. R. M. Fano, "Theoretical limitations on the broadband matching of arbitrary impedances," *J. Franklin Inst.*, vol. 249, no. 1, pp. 57–83, Jan. 1950, DOI 10.1016/0016-0032(50)90006-8, and no. 2, pp. 139–154, Feb. 1950, DOI 10.1016/S0016-0032(50)91101-X; MIT RLE Technical Report No. 41, 1948 [R-364].
3. D. C. Youla, "A New Theory of Broad-band Matching," *IEEE Trans. Circuit Theory*, vol. 11, no. 1, pp. 30–50, 1964, DOI 10.1109/TCT.1964.1082267 [R-364].
4. P. H. Smith, "Transmission Line Calculator," *Electronics*, vol. 12, no. 1, Jan. 1939 (read through a reprint) [R-364].
5. J. N. Burghartz, D. C. Edelstein, M. Soyuer, H. A. Ainspan and K. A. Jenkins, "RF circuit design aspects of spiral inductors on silicon," *IEEE J. Solid-State Circuits*, vol. 33, no. 12, pp. 2028–2034, Dec. 1998, DOI 10.1109/4.735544 [R-365].
6. C. P. Yue and S. S. Wong, "On-chip spiral inductors with patterned ground shields for Si-based RF ICs," *IEEE J. Solid-State Circuits*, vol. 33, no. 5, pp. 743–752, May 1998, DOI 10.1109/4.668989 [R-365].
7. A. M. Niknejad and R. G. Meyer, "Analysis, design, and optimization of spiral inductors and transformers for Si RF ICs," *IEEE J. Solid-State Circuits*, vol. 33, no. 10, pp. 1470–1481, 1998, DOI 10.1109/4.720393 [R-365].
8. S. S. Mohan, M. del Mar Hershenson, S. P. Boyd and T. H. Lee, "Simple accurate expressions for planar spiral inductances," *IEEE J. Solid-State Circuits*, vol. 34, no. 10, pp. 1419–1424, 1999, DOI 10.1109/4.792620 [R-365].
9. J. N. Burghartz and B. Rejaei, "On the design of RF spiral inductors on silicon," *IEEE Trans. Electron Devices*, vol. 50, no. 3, pp. 718–729, Mar. 2003, DOI 10.1109/TED.2003.810474 [R-365].
10. D. M. Pozar, *Microwave Engineering*, 4th ed., Wiley, 2012: the impedance-matching chapter.
11. T. H. Lee, *The Design of CMOS Radio-Frequency Integrated Circuits*, 2nd ed., Cambridge University Press, 2004.
12. Infineon, BGA9H1BN6 data sheet, Rev. 2.1, 20 Dec 2023 [R-366].
13. Qorvo, QPF4609 data sheet (preliminary), Rev. C, Sep 2024 [R-366].
