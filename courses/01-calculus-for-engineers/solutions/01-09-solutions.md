# Solutions 01-09 · Multivariable Calculus I: Partial Derivatives and Gradients

Problems: [01-09 problems](../problems/01-09-problems.md) · Chapter: [01-09](../chapters/01-09-multivariable-calculus-1.md)

Every numerical answer below is listed in the answer key at the end and is recomputed independently by [verify_01_09.py](../verify/verify_01_09.py).

---

## Solutions

### Solution 01-09.1

(a) $f_x = 2xy + ye^{xy}$ and $f_y = x^2 + xe^{xy}$. At (1, 2): $f_x = 4 + 2e^2 = $ **18.78** and $f_y = 1 + e^2 = $ **8.389**.

(b) $f_{xy} = \partial_y(2xy + ye^{xy}) = 2x + e^{xy} + xye^{xy}$, and $f_{yx} = \partial_x(x^2 + xe^{xy}) = 2x + e^{xy} + xye^{xy}$. They are equal, as Clairaut's theorem promises. At (1, 2): $2 + e^2(1 + 2) = 2 + 3e^2 = $ **24.17**.

### Solution 01-09.2

$\partial P/\partial V = 2V/R = $ **0.4 W/V** (at fixed $R$) and $\partial P/\partial R = -V^2/R^2 = $ **−0.04 W/Ω** (at fixed $V$). +1 V raises $P$ by about 0.4 W; −1 Ω by about 0.04 W. **The voltage change** has ten times the effect. In relative terms, $P$'s elasticity is +2 to $V$ and −1 to $R$.

### Solution 01-09.3

(a) $f_x = 2x + y = 1$ and $f_y = x + 2y = -1$, so $\nabla f = (1, -1)$, with magnitude **1.414**.

(b) $D_{\mathbf{u}}f = (1, -1)\cdot(3, 4)/5 = (3 - 4)/5 = $ **−0.2**.

(c) Perpendicular to the gradient: along $\pm(1, 1)/\sqrt{2}$, which is tangent to the level curve through $(1, -1)$.

### Solution 01-09.4

$\dfrac{dz}{dt} = z_x\dfrac{dx}{dt} + z_y\dfrac{dy}{dt} = 2xy(-\sin t) + x^2\cos t$. At $t = \pi/4$, $x = y = \sqrt{2}/2$:

$$
2\cdot\tfrac{1}{2}\cdot\left(-\tfrac{\sqrt{2}}{2}\right) + \tfrac{1}{2}\cdot\tfrac{\sqrt{2}}{2} = -0.7071 + 0.3536 = \mathbf{-0.3536}.
$$

Check: $z = \cos^2t\sin t$, so $dz/dt = -2\cos t\sin^2t + \cos^3t$, which at π/4 is $-2(0.3536) + 0.3536 = -0.3536$ ✓.

### Solution 01-09.5

(a) $R = 1.72\times10^{-8}\times0.05/(0.2\times10^{-3}\times35\times10^{-6}) = $ **0.1229 Ω**.

(b) $\ln R = \ln\rho + \ln L - \ln w - \ln t$, so each elasticity is ±1. Worst case: $1 + 5 + 10 = $ **16%**. RSS: $\sqrt{1 + 25 + 100} = $ **11.22%**.

(c) **Copper thickness**, which contributes 100 of the 126 units of variance. Board vendors specify copper weight (thickness) tolerances for exactly this reason.

### Solution 01-09.6

(a) $V_{ov} = 0.3$ V and $1 + V_{DS}/V_A = 1.15$.

- $I_D = \tfrac{1}{2}(4\times10^{-3})(0.09)(1.15) = $ **207.0 µA**.
- $g_m = 4\times10^{-3}\times0.3\times1.15 = $ **1.380 mS**.
- $g_o = \tfrac{1}{2}(4\times10^{-3})(0.09)/6 = $ **30.00 µS**, so $r_o = $ **33.33 kΩ**.

(b) $g_mr_o = 1.38\times10^{-3}\times33\,333 = $ **46.00**.

(c) $2I_D/V_{ov} = 2\times207\text{ µA}/0.3\text{ V} = $ **1.380 mS** ✓. A lower Early voltage (shorter channel) gives lower intrinsic gain than in Example 01-09.2.

(d) $\Delta I_D \approx g_m(5\text{ mV}) + g_o(0.2\text{ V}) = 6.90 + 6.00 = $ **12.90 µA**. Exactly, $I_D(0.705, 1.1) - I_D(0.7, 0.9) = $ **13.16 µA**. The linear estimate is 2% low, mostly from the square law's curvature in $V_{GS}$, as in Example 01-09.2.

### Solution 01-09.7

(a) $3kT/q$ at 350 K is 0.09048 V, so $dV/dT = (0.600 - 1.12 - 0.09048)/350 = $ **−1.744 mV/K**. The magnitude depends on both bias and temperature.

(b) $3x^2 + 3y^2y' = 0$, so $y' = -x^2/y^2 = -1/4 = $ **−0.25**.

### Solution 01-09.8

$f_x = 3x^2 - 3 = 0$ gives $x = \pm1$; $f_y = 2y - 2 = 0$ gives $y = 1$. The second partials are $f_{xx} = 6x$, $f_{yy} = 2$, $f_{xy} = 0$.

- At (1, 1): $D = 6\times2 = 12 > 0$ with $f_{xx} > 0$, a **local minimum**, $f = 1 - 3 + 1 - 2 = $ **−3**.
- At (−1, 1): $D = -12 < 0$, a **saddle**, $f = -1 + 3 + 1 - 2 = $ **1**.

### Solution 01-09.9

(a) $\bar{x} = 1.5$ and $\bar{y} = 3.5$. Then $\sum(x - \bar{x})(y - \bar{y}) = 3.75 + 0.25 + 0.25 + 3.75 = 8$ and $\sum(x - \bar{x})^2 = 5$. So $b = 8/5 = $ **1.6** and $a = 3.5 - 1.6\times1.5 = $ **1.1**.

(b) The residuals are −0.1, 0.3, −0.3, 0.1, so $S = $ **0.2**.

(c) $S_{aa} = 2n = 8$, $S_{bb} = 2\sum x_i^2 = 28$, $S_{ab} = 2\sum x_i = 12$, so $D = 8\times28 - 144 = 80 > 0$ with $S_{aa} > 0$: a minimum ✓.

(d) The stock's **beta**: its sensitivity to the market, a partial derivative estimated by regression.

### Solution 01-09.10

(a) $\nabla f = (2x, 20y)$, so $x \leftarrow x - 2\eta x = x(1 - 2\eta)$ and $y \leftarrow y(1 - 20\eta)$.

(b) Both factors must have magnitude below 1: $0 < \eta < 1$ for $x$ and $0 < \eta < 0.1$ for $y$. So **0 < η < 0.1**, i.e. $2/h_{max}$, where $h_{max} = 20$ is the larger curvature (Hessian eigenvalue; written $h$ here to keep λ for Lagrange multipliers).

(c) The factors are 0.92 and 0.2. After three steps: $x = 0.92^3 = $ **0.7787**, $y = 0.2^3 = $ **0.008**, and $f = 0.6064 + 0.00064 = $ **0.6070**.

(d) The condition number is $20/2 = $ **10**. The step size is capped by the steep direction ($y$), so the shallow direction ($x$) shrinks by only 8% per step. Convergence time grows in proportion to the condition number. Rescaling the variables (preconditioning) or momentum methods fix this.

### Solution 01-09.11

(a) Maximize $A = xy$ subject to $2x + 2y = 20$. $\nabla A = \lambda\nabla g$ gives $y = 2\lambda$ and $x = 2\lambda$, so $x = y = 5$: a square of area **25**.

(b) $\lambda = 2.5$. With perimeter $P$, the optimum is a square of side $P/4$, so $A^\ast = P^2/16$ and $dA^\ast/dP = P/8 = 2.5$ at $P = 20$ ✓. One extra unit of perimeter buys about 2.5 units of area.

### Solution 01-09.12

(a) $\dfrac{\partial C}{\partial P_i} = \dfrac{1}{\ln2}\cdot\dfrac{1}{N_i + P_i} = \lambda$ for each $i$, so $N_i + P_i = 1/(\lambda\ln2) \equiv \mu$, the same "water level" for both channels.

(b) $P_1 + P_2 = 2\mu - (N_1 + N_2) = 6$ gives $\mu = $ **5 mW**, so $P_1 = $ **4 mW** and $P_2 = $ **2 mW**. Then $C = \log_25 + \log_2(5/3) = $ **3.059 b/s/Hz**. The equal split (3/3) gives $\log_24 + \log_22 = $ **3** b/s/Hz, so water-filling gains about 2%.

(c) For $P = 1$: $\mu = 2.5$, which would make $P_2 = -0.5$: impossible. The constraint $P_2 \ge 0$ binds. Put all the power in the better channel: $P_1 = 1$, $P_2 = 0$, so $C = \log_22 = $ **1 b/s/Hz**. Check that this corner is optimal: the marginal capacity of channel 1 there is proportional to $1/(N_1 + P_1) = 1/2$, larger than that of the unused channel 2, $1/N_2 = 1/3$, so moving any power to channel 2 would lower $C$. At low total power the noisy channel is not worth using, which is why bit-loading systems switch off poor subcarriers.

### Solution 01-09.13

(a) $3c_if_i^2 = \lambda$ for every $i$, so $f_i = \sqrt{\lambda/(3c_i)} \propto 1/\sqrt{c_i}$.

(b) The weights $1/\sqrt{c_i}$ are 3.162, 1.581 and 1.054, summing to 5.797. Scaling to $F = 3.4$:

- $f_1 = $ **1.855 GHz**, $f_2 = $ **0.9273 GHz**, $f_3 = $ **0.6182 GHz**;
- total power $\sum c_if_i^3 = $ **1.169 W**;
- $\lambda = 3(0.1)(1.855)^2 = $ **1.032 W/GHz**.

(c) At $f_i = 0$ a core's marginal cost $3c_if_i^2$ is zero, below λ, so it always pays to give every core some work. With a fixed idle power, an active core costs that power even at zero work. Then switching a core off entirely can win, and the optimum becomes a discrete choice: which cores to power, then a Lagrange split among them. Real schedulers face exactly this.

### Solution 01-09.14

(a) $dV_T/dT = k/q = $ **0.08617 mV/K**: proportional to absolute temperature (PTAT).

(b) From Example 01-09.3, $dV_{BE}/dT = -1.8092$ mV/K, and $k/q = 0.086173$ mV/K. So $K = 1.8092/0.086173 = 20.995 \approx $ **21.00**.

(c) $V_{out} = 0.6548 + 21.00\times0.02585 = $ **1.198 V**. In general, $dV_{BE}/dT = (V_{BE} - E_g/q - 3V_T)/T$ and $d(KV_T)/dT = KV_T/T$. Setting the sum to zero gives

$$
V_{BE} + KV_T = \frac{E_g}{q} + 3\frac{kT}{q} = 1.12 + 0.0776 = 1.198\text{ V},
$$

whatever the bias current. The output of a zero-tempco reference sits at (nearly) the silicon bandgap energy expressed in volts, hence the name. Practical bandgap references output about 1.2–1.25 V; refined models (a temperature-dependent bandgap, the exact current dependence) shift the details but not the principle.

### Solution 01-09.15

(a) Let $u = V^2$ = 0.36, 0.64, 1.00. Then $P = au + b$ is a straight-line fit in $u$, and the normal equations give $a = $ **1.014 W/V²** and $b = $ **0.04093 W**.

(b) The residual sum of squares is **1.62×10^−4 W²**.

(c) At 0.8 V the fit gives $1.014\times0.64 + 0.0409 = 0.690$ W, of which the leakage $b$ is **5.94%**. Distrust it: real leakage depends strongly on voltage (DIBL, gate leakage) and exponentially on temperature, so a "constant $b$" is a crude model. Three points over a narrow range barely constrain the intercept, which is an extrapolation to $V = 0$. A credible leakage estimate needs measurements with the clock stopped, across voltage and temperature.

---

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 01-09.1a | f_x at (1, 2) | 18.78 | — |
| 01-09.1b | f_y at (1, 2) | 8.389 | — |
| 01-09.1c | f_xy at (1, 2) | 24.17 | — |
| 01-09.2a | ∂P/∂V | 0.4 | W/V |
| 01-09.2b | ∂P/∂R | −0.04 | W/Ω |
| 01-09.3a | magnitude of ∇f | 1.414 | — |
| 01-09.3b | directional derivative | −0.2 | — |
| 01-09.4a | dz/dt at π/4 | −0.3536 | — |
| 01-09.5a | nominal resistance | 0.1229 | Ω |
| 01-09.5b | worst case | 16 | % |
| 01-09.5c | RSS | 11.22 | % |
| 01-09.6a | I_D | 207.0 | µA |
| 01-09.6b | g_m | 1.380 | mS |
| 01-09.6c | g_o | 30.00 | µS |
| 01-09.6d | r_o | 33.33 | kΩ |
| 01-09.6e | intrinsic gain | 46.00 | — |
| 01-09.7a | dV/dT at 0.6 V, 350 K | −1.744 | mV/K |
| 01-09.7b | dy/dx | −0.25 | — |
| 01-09.8a | f at the minimum (1, 1) | −3 | — |
| 01-09.8b | f at the saddle (−1, 1) | 1 | — |
| 01-09.9a | intercept a | 1.1 | — |
| 01-09.9b | slope b | 1.6 | — |
| 01-09.9c | sum of squared residuals | 0.2 | — |
| 01-09.10a | x after 3 steps | 0.7787 | — |
| 01-09.10b | y after 3 steps | 0.008 | — |
| 01-09.10c | f after 3 steps | 0.6070 | — |
| 01-09.10d | stability limit on η | 0.1 | — |
| 01-09.10e | condition number | 10 | — |
| 01-09.11a | maximum area | 25 | — |
| 01-09.11b | λ | 2.5 | — |
| 01-09.12a | P1 | 4 | mW |
| 01-09.12b | P2 | 2 | mW |
| 01-09.12c | capacity, water-filling | 3.059 | b/s/Hz |
| 01-09.12d | capacity, equal split | 3 | b/s/Hz |
| 01-09.12e | capacity at P = 1 mW | 1 | b/s/Hz |
| 01-09.13a | f1 | 1.855 | GHz |
| 01-09.13b | f2 | 0.9273 | GHz |
| 01-09.13c | f3 | 0.6182 | GHz |
| 01-09.13d | total power | 1.169 | W |
| 01-09.13e | λ | 1.032 | W/GHz |
| 01-09.14a | dV_T/dT | 0.08617 | mV/K |
| 01-09.14b | K | 21.00 | — |
| 01-09.14c | V_out | 1.198 | V |
| 01-09.15a | a | 1.014 | W/V² |
| 01-09.15b | b | 0.04093 | W |
| 01-09.15c | residual sum of squares | 1.62×10^-4 | W² |
| 01-09.15d | leakage share at 0.8 V | 5.94 | % |
| 01-09.6f | linear estimate of ΔI_D | 12.90 | µA |
| 01-09.6g | exact ΔI_D | 13.16 | µA |
| 01-09.12f | water level μ | 5 | mW |
| 01-09.14d | dV_BE/dT magnitude, five digits | 1.8092 | mV/K |
| 01-09.14e | k/q | 0.086173 | mV/K |
| 01-09.14f | K before rounding | 20.995 | — |
