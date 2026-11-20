<!-- status: verified -->
# 13-09 · The Smith Chart and Impedance Matching

| | |
|---|---|
| **Course** | [13 · Electromagnetics](../README.md) |
| **University equivalent** | The Smith-chart and matching chapter of a junior electromagnetics or first microwave course: the chart's construction from the reflection-coefficient plane, impedance and admittance reading, moving along lines, lumped L-network matching, single-stub matching, and the bandwidth limits of matching including the Bode–Fano bound (Ulaby & Ravaioli, *Fundamentals of Applied Electromagnetics*, ch. 2; Pozar, *Microwave Engineering*, ch. 5) |
| **Prerequisites** | [13-08 Transmission Lines: Sinusoidal Steady State](13-08-transmission-lines-sinusoidal-steady-state.md), [07-08 Filters and Resonance](../../07-circuit-analysis-2-transient-and-ac/chapters/07-08-filters-and-resonance.md) (Q), [02-01 Complex Numbers, Euler and Phasors](../../02-complex-numbers-des-and-linear-algebra/chapters/02-01-complex-numbers-euler-and-phasors.md) |
| **Estimated study hours** | 10 |
| **Last verified** | 2026-11-20 |

**Learning objectives.** After this chapter you can:

1. Derive the Smith chart's constant-resistance and constant-reactance circles from $\Gamma = (z - 1)/(z + 1)$.
2. Read impedance, admittance, |Γ| and VSWR from the chart, and move a point along a lossless line.
3. Design two-element L-network matches analytically and check them on the chart.
4. Design a single shunt-stub match (both solutions) for any load.
5. Estimate the bandwidth of a match from its Q, and state the Bode–Fano limit on matching a reactive load.

---

## 1. Big picture

13-08 showed that a line transforms impedance along a circle in the Γ plane. The Smith chart draws that plane with a grid of impedance values on it, so that every operation of RF design (adding series or shunt elements, moving along a line, converting impedance to admittance) becomes a move along a circle. Engineers still reach for it because it shows at a glance what is matchable, with which elements, and over what bandwidth. Network analyzers display measurements on it, and matching networks are designed on it.

- **Matching sets power transfer.** Amplifiers, antennas and mixers must be matched to deliver or receive maximum power and to keep reflections from upsetting filters and oscillators.
- **Two elements are enough at one frequency.** An L-network of one series and one shunt element matches any resistive pair; stubs do the same with lines.
- **Bandwidth is fundamentally limited.** Reactive loads (antennas, transistors' input capacitance) cannot be matched over an arbitrarily wide band; the Bode–Fano limit says how wide.

## 2. Intuition first

**A map of all impedances in a disc.** Every passive impedance has $\lvert\Gamma\rvert \le 1$. The Smith chart is the unit disc of Γ, with the impedance each point represents written on it. The centre is a perfect match (Γ = 0, $z$ = 1); the left edge is a short; the right edge an open; the top half inductive, the bottom capacitive. A lossless line is a clockwise walk around a circle centred on the middle; a series reactance slides you along a constant-resistance circle; a shunt susceptance slides you along a constant-conductance circle.

**Matching as navigation.** To match, start at the load and get to the centre using only allowed moves. An L-network uses two moves: one along a circle of constant resistance (series element) and one along a circle of constant conductance (shunt element). A stub match uses a walk along the line to reach the "unit conductance circle", then a shunt stub to cancel the remaining susceptance.

**An analogy from finance, and its limits.** Matching resembles hedging a position with two instruments: one adjusts one exposure (reactance), the other another (susceptance), and two independent instruments can neutralize two coordinates. The analogy breaks at bandwidth: a hedge built at one price drifts as prices move, just as a match built at one frequency degrades off it, but the Bode–Fano limit is a hard physical bound with no counterpart in a frictionless market.

## 3. Theory

> **Conventions.** Normalized impedance $z = Z/Z_0 = r + jx$ and admittance $y = Y Z_0 = g + jb$. Γ is the voltage reflection coefficient, $\Gamma = \Gamma_r + j\Gamma_i$. Distances on the chart's outer scale are in wavelengths; "toward generator" (TG) is clockwise. Series elements add to $z$; shunt elements add to $y$.

### 3.1 From the Γ plane to the chart

Invert $\Gamma = (z - 1)/(z + 1)$ to get $z = (1 + \Gamma)/(1 - \Gamma)$, and separate real and imaginary parts:

$$
r = \frac{1 - \Gamma_r^2 - \Gamma_i^2}{(1 - \Gamma_r)^2 + \Gamma_i^2}, \qquad x = \frac{2\Gamma_i}{(1 - \Gamma_r)^2 + \Gamma_i^2} .
$$

Rearranging each into the equation of a circle takes one completed square. For $r$: multiply out, $r(1 - \Gamma_r)^2 + r\Gamma_i^2 = 1 - \Gamma_r^2 - \Gamma_i^2$, collect terms, $(1 + r)(\Gamma_r^2 + \Gamma_i^2) - 2r\Gamma_r = 1 - r$, and divide by $1 + r$; adding $[r/(1 + r)]^2$ to both sides completes the square in $\Gamma_r$, and the right side becomes $(1 - r)/(1 + r) + r^2/(1 + r)^2 = 1/(1 + r)^2$. For $x$: $x[(1 - \Gamma_r)^2 + \Gamma_i^2] = 2\Gamma_i$, so $(\Gamma_r - 1)^2 + \Gamma_i^2 - (2/x)\Gamma_i = 0$, and adding $1/x^2$ completes the square in $\Gamma_i$. The results:

$$
\Big(\Gamma_r - \frac{r}{1 + r}\Big)^2 + \Gamma_i^2 = \Big(\frac{1}{1 + r}\Big)^2, \qquad
(\Gamma_r - 1)^2 + \Big(\Gamma_i - \frac{1}{x}\Big)^2 = \Big(\frac{1}{x}\Big)^2 .
$$

So the points of constant $r$ lie on circles centred at $(r/(1 + r), 0)$ of radius $1/(1 + r)$, all touching at Γ = 1; and the points of constant $x$ lie on circles centred at $(1, 1/x)$ of radius $1/\lvert x\rvert$, also passing through Γ = 1. The $r$ = 0 circle is the unit circle (pure reactances), $r$ = 1 passes through the centre, and $x$ = 0 is the real axis. Drawing these two families over the disc gives the Smith chart (Figure 1).

![The Smith chart drawn from its definition: circles of constant normalized resistance (0, 0.2, 0.5, 1, 2, 5) tangent at the right edge, and arcs of constant normalized reactance (±0.2, ±0.5, ±1, ±2, ±5) all passing through the right edge, inside the unit circle; marked points show the load 2 + j1 and its position after λ/8 of line, 1 − j1](../../../assets/figures/13-09/smith.svg)

*Figure 1. A Smith chart built from the two circle families, with Example 13-09.2's load $z$ = 2 + j1 and its image after moving λ/8 toward the generator, $z$ = 1 − j1. Both lie on the same |Γ| circle (dashed).*

> **Going deeper — the chart is a Möbius map.** $\Gamma = (z - 1)/(z + 1)$ is a bilinear (Möbius) transformation of the complex plane. Such maps send circles and straight lines to circles and straight lines, which is why the vertical lines of constant $r$ and the horizontal lines of constant $x$ in the $z$-plane become the chart's two families of circles, and why the right half of the $z$-plane (passive loads, $r \ge 0$) lands exactly inside the unit circle. A lossless two-port is also a Möbius map of Γ, so any lossless matching network carries the chart's circles into circles: the geometric reason every lossless match can be designed as a sequence of rotations and moves along circles.

### 3.2 Reading and moving

- **|Γ| and VSWR.** The distance from the centre is $\lvert\Gamma\rvert$. The circle of constant |Γ| crosses the positive real axis at $r$ = VSWR: on that axis $z$ is real and greater than 1, and equals $(1 + \lvert\Gamma\rvert)/(1 - \lvert\Gamma\rvert)$.
- **Moving along a lossless line.** $\Gamma(d) = \Gamma_Le^{-j2\beta d}$: rotate clockwise (toward the generator) by $2\beta d$, a full turn per half wavelength. The chart's outer scale is marked in wavelengths for this.
- **Admittance.** $y = 1/z = (1 - \Gamma)/(1 + \Gamma)$ is the same formula with Γ replaced by −Γ. So the admittance of a point is read by reflecting it through the centre (rotating by 180°) and reading the same grid. Alternatively, rotate the whole grid by 180° and read admittance directly at the same point: the "admittance chart" overlaid on a combined (ZY) chart.
- **Adding elements.** A series reactance $jx_s$ moves along a constant-$r$ circle (up for inductance, down for capacitance). A shunt susceptance $jb_p$ moves along a constant-$g$ circle (on the admittance grid: capacitance moves clockwise, inductance counterclockwise).

### 3.3 L-network matching

Two reactive elements, one in series and one in shunt, can match any resistance $R_L$ to any other $R_0$ at one frequency. Let $R_{high}$ and $R_{low}$ be the larger and smaller. The shunt element goes across the larger resistance, the series element in line with the smaller. Requiring the shunt combination to present the smaller resistance:

$$
\frac{1}{R_{high}^{-1} + jB} = R_{low} - jX \quad\Rightarrow\quad
Q = \sqrt{\frac{R_{high}}{R_{low}} - 1}, \qquad X = QR_{low}, \qquad B = \frac{Q}{R_{high}} .
$$

Here $Q$ is the ratio of reactance to resistance in each branch, and it sets the bandwidth (§3.5). There are two solutions: series inductor with shunt capacitor (a low-pass form, which also filters harmonics) or series capacitor with shunt inductor (high-pass, which blocks DC). A complex load is handled by absorbing its reactance into the series element, or by first cancelling it.

### 3.4 Single-stub matching

A shunt stub match uses a length $d$ of line followed by a shunt stub. Choose $d$ so that the admittance seen at that point has unit conductance, $y(d) = 1 + jb$: on the chart, rotate the load's admittance clockwise until it meets the $g$ = 1 circle. Then add a shunt stub of susceptance $-jb$ to cancel the remainder. A shorted stub of length ℓ has $y_{stub} = -j\cot\beta\ell$, so it needs $\cot\beta\ell = b$; an open stub has $y_{stub} = j\tan\beta\ell$. The $g$ = 1 circle is crossed twice per half wavelength, so there are always two solutions; the one with the shorter $d$ and stub is usually preferred for bandwidth. Analytically, write $Z_L = R_L + jX_L$ and $t = \tan\beta d$. The input-impedance formula gives the conductance at distance $d$ as $G = R_L(1 + t^2)/[R_L^2 + (X_L + Z_0t)^2]$, and setting $G = 1/Z_0$ gives a quadratic in $t$:

$$
Z_0(R_L - Z_0)\,t^2 - 2X_LZ_0\,t + (R_LZ_0 - R_L^2 - X_L^2) = 0 \quad\Rightarrow\quad
t = \frac{X_L \pm \sqrt{R_L\big[(Z_0 - R_L)^2 + X_L^2\big]/Z_0}}{R_L - Z_0}
$$

(for $R_L = Z_0$ the single root is $t = -X_L/2Z_0$). Each root gives $d = (\lambda/2\pi)\arctan t$, adding λ/2 if the arctangent is negative. On the chart the same answer is a rotation and an intersection.

### 3.5 Bandwidth, Q and the Bode–Fano limit

An L-network matches exactly at one frequency. Away from it, the reactances change ($X \propto \omega$ for an inductor), and the reflection grows. The rate is set by Q: each branch is a resonant circuit with loaded Q of roughly $Q/2$ (it sees the source and the load resistances), so the fractional bandwidth over which the reflection stays small is of order $2/Q$, narrower for larger impedance ratios (Example 13-09.4). Cascading several L sections with intermediate resistances lowers each Q and widens the band, at the cost of more parts.

For a load with fixed reactance, no network of any complexity can do better than a fundamental limit. For a parallel RC load, Bode and Fano showed that any lossless matching network satisfies

$$
\int_0^\infty\ln\frac{1}{\lvert\Gamma(\omega)\rvert}\,d\omega \le \frac{\pi}{RC} .
$$

If the network achieves a constant $\lvert\Gamma\rvert = \Gamma_m$ over a band $\Delta\omega$ and total reflection elsewhere (the best possible shape), then $\Delta\omega\ln(1/\Gamma_m) \le \pi/(RC)$, and

$$
\Delta f \le \frac{1}{2RC\ln(1/\Gamma_m)} .
$$

The limit trades bandwidth against match quality: halving $\ln(1/\Gamma_m)$ (accepting a worse match) doubles the possible bandwidth. It is why wideband matching of antennas and of transistors with large input capacitance is hard, and why some devices are simply designed with smaller capacitance.

### 3.6 Which match? Conjugate, reflectionless and noise matching

"Matched" means different things depending on the goal, and the chart serves all of them.

- **Reflectionless match.** Make the load look like $Z_0$ so that nothing reflects on the line: $Z_{in} = Z_0$, the chart's centre. This is what a 50 Ω test system and a long cable want.
- **Conjugate match.** Deliver the most power from a source of impedance $Z_s = R_s + jX_s$: the load must present $Z_s^*$ (07-06's maximum power transfer theorem). When $Z_s$ is a real $Z_0$ the two coincide. When a transistor's output impedance is complex, the matching network targets the conjugate point on the chart, not the centre.
- **Noise and power matches for amplifiers.** A low-noise amplifier's input is matched for minimum noise figure, which generally differs from the conjugate match for maximum gain; a power amplifier's output is matched to a load line chosen for output power and efficiency, not for conjugate match. Both are points on the chart chosen by device data, with circles of constant noise figure or output power drawn around them (Course 21).

In practice designers use a combined **ZY chart**, with the admittance grid overlaid in a second colour, so that series moves (on the impedance grid) and shunt moves (on the admittance grid) can be drawn without rotating anything. A lossy line, finally, makes the |Γ| circle a spiral toward the centre, which is how a long cable seen on a network analyzer appears.

## 4. Worked examples

### Example 13-09.1 · Placing a point (tier A)

**Setup.** On a 50 Ω chart, locate $Z_L$ = 100 + j50 Ω. Find Γ (magnitude and angle) and the VSWR.

**Solution.** $z$ = 2 + j1 and $\Gamma = (1 + j1)/(3 + j1)$ = **0.4 + j0.2**: magnitude **0.4472**, angle **26.57**°. VSWR = (1 + 0.4472)/(1 − 0.4472) = **2.618**.

**Units check.** Γ = (z − 1)/(z + 1) uses the normalized $z = Z/Z_0$, a pure number, so Γ and the VSWR are dimensionless.

**Sanity check.** The point lies on the $r$ = 2 circle (centre (2/3, 0), radius 1/3) and the $x$ = 1 circle (centre (1, 1), radius 1): $(0.4 - 0.6667)^2 + 0.2^2 = 0.1111 = (1/3)^2$, and $(0.4 - 1)^2 + (0.2 - 1)^2 = 1$.

### Example 13-09.2 · Moving λ/8 toward the generator (tier A)

**Setup.** Move the load of Example 13-09.1 by λ/8 toward the generator. Find the new Γ and $Z_{in}$, and check with the formula of 13-08.

**Solution.** λ/8 is a rotation of $2\beta d$ = 90° clockwise: Γ becomes **0.4472** at **−63.43**°, and $z = (1 + \Gamma)/(1 - \Gamma)$ = **1 − j1**, so $Z_{in}$ = **50 − j50** Ω. The 13-08 formula gives $50(100 + j50 + j50)/(50 + j(100 + j50))$ = 50 − j50 Ω, the same.

**Units check.** The rotation angle $2\beta d$ = 2(2π/λ)(λ/8) = π/2 rad is dimensionless; $Z_{in}$ = $Z_0z$ carries ohms.

**Sanity check.** The point stayed on the |Γ| = 0.4472 circle and landed on the $r$ = 1 circle: one shunt or series element away from a match.

### Example 13-09.3 · Admittance by reflection (tier B)

**Setup.** Find the normalized admittance of $z$ = 2 + j1 by the 180° rotation, and check it directly.

**Solution.** −Γ = −0.4 − j0.2, and $y = (1 + (-\Gamma))/(1 - (-\Gamma))$ = **0.4 − j0.2**. Directly, $1/(2 + j1) = (2 - j1)/5$ = 0.4 − j0.2.

**Units check.** Admittance normalized to $Y_0 = 1/Z_0$ is dimensionless, as is $z$.

**Sanity check.** An inductive impedance has a capacitive-signed (negative) susceptance, as it must: the 180° rotation carries the upper half to the lower half.

### Example 13-09.4 · An L-network for a power amplifier (tier B)

**Setup.** A power amplifier needs to see 10 Ω at 2.4 GHz, delivered from a 50 Ω antenna port. Design a low-pass L-network (series inductor at the 10 Ω side, shunt capacitor at the 50 Ω side), and find the bandwidth over which $\lvert\Gamma\rvert$ < 0.1 at the 50 Ω port.

**Solution.** $Q = \sqrt{50/10 - 1}$ = **2**. The series reactance is $QR_{low}$ = 20 Ω, an inductor of $20/\omega$ = **1.326** nH; the shunt susceptance is $Q/R_{high}$ = 0.04 S, a capacitor of $0.04/\omega$ = **2.653** pF. Sweeping frequency and computing the input impedance of the network with its 10 Ω load gives $\lvert\Gamma\rvert$ < 0.1 over **11.25**% of the centre frequency.

**Units check.** $X/\omega$ is Ω·s = H and $B/\omega$ is S·s = F; Q is a ratio of resistances under a square root, so it is dimensionless.

**Sanity check.** At 2.4 GHz the network shows exactly 50 Ω: $10 + j20$ in parallel with $-j25$ gives $(10 + j20)(-j25)/(10 - j5) = 50$ Ω. For a single L-section the |Γ| < Γₘ band is close to $2\Gamma_m/(Q\sqrt{1 - \Gamma_m^2})$ = 10.05%, which the exact 11.25% confirms (the estimate is good for Q ≥ 2).

### Example 13-09.5 · A single-stub match (tier B)

**Setup.** Match $Z_L$ = 25 − j50 Ω to a 50 Ω air line at 1 GHz with a shorted shunt stub. Find both solutions: the distance from the load to the stub and the stub length, in wavelengths and centimetres.

**Solution.** The load's normalized admittance is $1/(0.5 - j1)$ = 0.4 + j0.8. Rotating toward the generator until $g$ = 1 (by the quadratic of §3.4, with $R_L$ = 25 Ω and $X_L$ = −50 Ω, or numerically): the first crossing is at $d$ = **0.06313**λ (**1.893** cm) where $y$ = 1 + j1.581; the stub must add −j1.581, so $\cot\beta\ell$ = 1.581 and ℓ = **0.08975**λ (**2.691** cm). The second crossing is at $d$ = **0.2067**λ (**6.196** cm) where $y$ = 1 − j1.581, needing ℓ = **0.4102**λ (**12.30** cm).

**Units check.** Distances in wavelengths times λ = c/f (m) give metres; $\cot\beta\ell$ is dimensionless.

**Sanity check.** The two susceptances are equal and opposite, as they must be: the two crossings of the $g$ = 1 circle are mirror images about the real axis. The first solution is shorter on both counts and has the wider bandwidth.

### Example 13-09.6 · How wide can a match be? (tier C)

**Setup.** A load is 50 Ω in parallel with 1 pF (a rough model of a broadband detector or a transistor input). Using the Bode–Fano limit, find the widest band over which any lossless network could hold the return loss at 20 dB, and at 10 dB.

**Solution.** π/(RC) = π/(50 Ω × 1 pF). For a 20 dB return loss, $\Gamma_m$ = 0.1 and $\Delta f \le 1/(2RC\ln 10)$ = **4.343** GHz. For 10 dB, $\Gamma_m$ = 0.3162 and $\Delta f \le$ **8.686** GHz, exactly twice as wide.

**Units check.** $\pi/(RC)$ is 1/(Ω·F) = 1/s, an angular bandwidth; dividing by 2π gives hertz.

**Sanity check.** $\ln(1/\Gamma_m)$ halves from 2.303 to 1.151, so the bandwidth doubles: matching quality and bandwidth trade one for one in the logarithm of the reflection. The bound is reached only with an infinite number of elements; real networks fall short.

### Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 13-09.1a | Γ real part | 0.4 | — |
| Ex 13-09.1b | Γ imaginary part | 0.2 | — |
| Ex 13-09.1c | Γ magnitude | 0.4472 | — |
| Ex 13-09.1d | Γ angle | 26.57 | ° |
| Ex 13-09.1e | VSWR | 2.618 | — |
| Ex 13-09.2a | Γ magnitude after λ/8 | 0.4472 | — |
| Ex 13-09.2b | Γ angle after λ/8 | −63.43 | ° |
| Ex 13-09.2c | input resistance | 50 | Ω |
| Ex 13-09.2d | input reactance | −50 | Ω |
| Ex 13-09.3a | normalized conductance | 0.4 | — |
| Ex 13-09.3b | normalized susceptance | −0.2 | — |
| Ex 13-09.4a | network Q | 2 | — |
| Ex 13-09.4b | series inductance | 1.326 | nH |
| Ex 13-09.4c | shunt capacitance | 2.653 | pF |
| Ex 13-09.4d | bandwidth for Γ below 0.1 | 11.25 | % |
| Ex 13-09.5a | first stub position | 0.06313 | λ |
| Ex 13-09.5b | first stub position | 1.893 | cm |
| Ex 13-09.5c | first stub length | 0.08975 | λ |
| Ex 13-09.5d | first stub length | 2.691 | cm |
| Ex 13-09.5e | second stub position | 0.2067 | λ |
| Ex 13-09.5f | second stub position | 6.196 | cm |
| Ex 13-09.5g | second stub length | 0.4102 | λ |
| Ex 13-09.5h | second stub length | 12.30 | cm |
| Ex 13-09.5i | susceptance to cancel | 1.581 | — |
| Ex 13-09.6a | Bode–Fano bandwidth at 20 dB | 4.343 | GHz |
| Ex 13-09.6b | Bode–Fano bandwidth at 10 dB | 8.686 | GHz |
| Prac 13-09.a | air-coax impedance for minimum loss | 76.65 | Ω |
| Prac 13-09.b | air-coax impedance for maximum power | 29.98 | Ω |
| Prac 13-09.c | their geometric mean | 47.94 | Ω |
| Prac 13-09.d | minimum-loss impedance with ε_r = 2.25 | 51.10 | Ω |
| Sim 13-09.a | simulated L-network input resistance | 50 | Ω |
| Sim 13-09.b | simulated stub-match input resistance | 50 | Ω |

*Every value is recomputed by [verify_13_09.py](../verify/verify_13_09.py): chart geometry by checking the circle equations numerically, line moves by marching the phasor line equations, the L-network and stub match by nodal analysis of the matched circuit with root finding for the positions, and the coax optima by numerical minimization. The L-network and the stub match are also simulated in ngspice.*

## 5. Simulate it

The lab, [labs/13-09-lab](../labs/13-09-lab/README.md), has a notebook and an ngspice netlist:

1. Draws a Smith chart from the two circle families and plots points, |Γ| circles and line moves.
2. Designs both L-network solutions for any pair of resistances and plots each design's path on the chart and its |Γ| against frequency.
3. Finds both single-stub solutions for any load by intersecting the rotated admittance with the $g$ = 1 circle.
4. Compares one-, two- and three-section L-matches of a 10 Ω load to 50 Ω over frequency, and tabulates the Bode–Fano bound for a 50 Ω ∥ 1 pF load at several return losses.

The netlist [match.cir](../labs/13-09-lab/match.cir) builds Example 13-09.4's L-network and Example 13-09.5's stub match and prints their input impedances.

**Guided exercise (predict, then run).** **Before running the netlist**, predict both input impedances at the design frequencies. Then run it. (Both **50** Ω, purely resistive.)

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Low-pass L-network | Harmonic filtering, DC path through the inductor | Band limited by Q | RF designer |
| Multi-section matching | Bandwidth | Parts, loss, area | RF designer |
| Stubs instead of lumped parts | Precision at microwave frequencies | Area, narrower band for long stubs | Microwave designer |
| Lower device capacitance | Wider Bode–Fano limit | Device size, power, gain | Device and IC designers |
| Accepting a worse match | Bandwidth (Bode–Fano) | Mismatch loss, ripple | System architect |

## 7. Numbers to know

| Quantity | Value | Note |
|---|---|---|
| Chart centre | Γ = 0, $z$ = 1 | Perfect match |
| One full turn | λ/2 of line | Clockwise toward the generator |
| Admittance | Rotate 180° | $y$ = $z$ with Γ → −Γ |
| L-network Q | $\sqrt{R_{high}/R_{low} - 1}$ | 2 for a 5:1 step |
| Bode–Fano (parallel RC) | $\Delta f \le 1/[2RC\ln(1/\Gamma_m)]$ | 4.3 GHz at 20 dB for 50 Ω ∥ 1 pF |
| 50 Ω | Between 30 Ω (max power) and 77 Ω (min loss) for air coax | Derived in §9 |

## 8. Common mistakes

- **Rotating the wrong way.** Toward the generator is clockwise; toward the load is counterclockwise.
- **Adding a shunt element on the impedance grid.** Shunt elements add admittance; switch to the admittance grid (or rotate by 180°) first.
- **Forgetting a full turn is λ/2, not λ.** Γ rotates by twice the electrical length.
- **Designing a match without checking bandwidth.** A perfect match at one frequency may be useless across the band.
- **Expecting any network to beat Bode–Fano.** More elements approach the limit, never exceed it.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **Why 50 Ω?** For air-filled coax, the conductor loss $\alpha_c \propto (1/a + 1/b)/\ln(b/a)$ is lowest at $b/a$ = 3.591, an impedance of **76.65** Ω in air (for a solid-polyethylene filling, $\varepsilon_r$ = 2.25, the same geometry gives **51.10** Ω, so 75 Ω cable is a minimum-loss choice only for air or low-permittivity foam dielectrics), and the power that can be carried before air breaks down is highest at $b/a = \sqrt e$, an impedance of **29.98** Ω (our arithmetic, Problems 13-09.12 and 13-09.13). Their geometric mean is **47.94** Ω; 50 Ω is widely explained as a compromise of this kind, and 75 Ω (near minimum loss) is used where power is low and loss matters, as in video and cable TV **[Established]** (textbook derivation; the history is often retold but rarely documented precisely).
- **The chart lives on in instruments.** Vector network analyzers and RF simulators display $S_{11}$ on Smith charts; matching networks for phones, Wi-Fi and radar front ends are designed and tuned on them **[Industry estimate]** (standard practice; no source is logged here).
- **Tunable matching.** Phones use antenna tuners (switched capacitor banks and inductors) to re-match antennas detuned by hands and heads, moving the operating point back toward the chart's centre **[Industry estimate]** (common in current handsets; no product data are logged here).

### Why it matters commercially

- **Power amplifier output matching** sets efficiency and linearity, hence battery life and heat in every radio.
- **Low-noise amplifier input matching** sets the receiver's noise figure (Course 21).
- **Wideband limits** shape product decisions: covering many cellular bands with one antenna is a Bode–Fano problem, solved with tuners and switches rather than a single wideband match.

### Marketing vs Reality

- **"Perfectly matched from DC to 40 GHz."** *Reality:* a resistive (lossy) match can be broadband by absorbing power; a lossless match to a reactive load cannot beat Bode–Fano. *Sanity check:* ask whether the match is resistive (and how much loss it adds) or reactive (and its return loss across the band).
- **"Our antenna needs no tuner."** *Reality:* a small antenna covering several bands at a good match violates Bode–Fano unless it is lossy (low efficiency). *Sanity check:* ask for radiated efficiency, not just return loss.

### Questions for engineering leaders

1. **"What is the bandwidth of your matching networks, and what limits it?"**
   *Strong:* a Q or Bode–Fano argument with the device capacitance, and the number of sections chosen. *Evasive:* "it's broadband."
2. **"How do you keep the antenna matched in the user's hand?"**
   *Strong:* closed-loop or switched tuning with measured detuning ranges. *Evasive:* "the antenna is robust."
3. **"Where is the loss in your match: components, layout, or mismatch?"**
   *Strong:* a breakdown with component Q values and layout parasitics. *Evasive:* "less than 1 dB."

## 10. Concept check

**Q1.** Why are constant-resistance contours circles in the Γ plane?

<details><summary>Answer</summary>

The map $\Gamma = (z - 1)/(z + 1)$ is a bilinear (Möbius) transformation, which maps lines and circles to lines and circles. The vertical line Re$\{z\}$ = $r$ therefore maps to a circle, centred at $(r/(1 + r), 0)$ with radius $1/(1 + r)$.

</details>

**Q2.** How do you read admittance on an impedance Smith chart?

<details><summary>Answer</summary>

Reflect the point through the centre (rotate by 180°) and read the impedance grid there: $y = (1 - \Gamma)/(1 + \Gamma)$ is the impedance formula with −Γ.

</details>

**Q3.** Which element moves a point along a constant-resistance circle?

<details><summary>Answer</summary>

A series reactance: it changes $x$ but not $r$. A shunt susceptance moves along a constant-conductance circle instead.

</details>

**Q4.** Why does an L-network's bandwidth shrink as the impedance ratio grows?

<details><summary>Answer</summary>

The required Q is $\sqrt{R_{high}/R_{low} - 1}$; larger ratios need larger reactances relative to the resistances, so the reactances' frequency dependence pulls the match off faster.

</details>

**Q5.** Why are there two single-stub solutions?

<details><summary>Answer</summary>

Rotating the load's admittance around its |Γ| circle crosses the $g$ = 1 circle twice per half wavelength, at susceptances $+b$ and $-b$; each needs a stub of the opposite susceptance.

</details>

**Q6.** What does the Bode–Fano limit say in words?

<details><summary>Answer</summary>

For a load with a fixed reactive part, the area under $\ln(1/\lvert\Gamma\rvert)$ across frequency is bounded by a constant set by the load's RC (or L/R). A better match (larger $\ln(1/\Gamma)$) can only be had over a proportionally narrower band.

</details>

Next: the [13-09 problem set](../problems/13-09-problems.md).

## 11. Key terms

[Smith chart](../../../reference/glossary.md#smith-chart) · [Normalized impedance](../../../reference/glossary.md#normalized-impedance) · [Reflection coefficient](../../../reference/glossary.md#reflection-coefficient) · [Voltage standing-wave ratio](../../../reference/glossary.md#voltage-standing-wave-ratio-vswr) · [Impedance matching](../../../reference/glossary.md#impedance-matching) · [L-network](../../../reference/glossary.md#l-network) · [Stub](../../../reference/glossary.md#stub) · [Single-stub matching](../../../reference/glossary.md#single-stub-matching) · [Bode–Fano limit](../../../reference/glossary.md#bode-fano-limit) · [Quality factor](../../../reference/glossary.md#quality-factor)

## 12. Connections

- **Builds on:** Γ(d), input impedance and stubs from [13-08](13-08-transmission-lines-sinusoidal-steady-state.md); Q and resonance from [07-08](../../07-circuit-analysis-2-transient-and-ac/chapters/07-08-filters-and-resonance.md); complex numbers from [02-01](../../02-complex-numbers-des-and-linear-algebra/chapters/02-01-complex-numbers-euler-and-phasors.md).
- **Next:** [13-10 Waveguides and Resonators](13-10-waveguides-and-resonators.md) moves from TEM lines to hollow guides and cavities.
- **Used later:** amplifier matching, noise matching and multi-section transformers in Course 21; antenna matching in [13-11](13-11-radiation-and-antennas.md).

## 13. Further study

- D. M. Pozar, *Microwave Engineering*, ch. 2 (Smith chart) and ch. 5 (impedance matching, Bode–Fano).
- F. T. Ulaby and U. Ravaioli, *Fundamentals of Applied Electromagnetics*, ch. 2.
- R. M. Fano, "Theoretical limitations on the broadband matching of arbitrary impedances," *Journal of the Franklin Institute* 249 (1950) (the original limit).

## 14. Sources

The theory (Smith chart, L-network and stub matching, the Bode–Fano limit) is textbook material (Further study); the coax optima in §9 are derived here. The practitioner statements about instruments and tunable matching are tagged as industry estimates; no perishable figures are cited.
