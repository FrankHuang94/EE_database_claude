<!-- status: verified -->
# 05-03 · SciPy, SymPy and Matplotlib

| | |
|---|---|
| **Course** | [05 · Programming for Engineers](../README.md) |
| **University equivalent** | Scientific computing with Python, continued (MIT 6.0002 and typical "computational methods for engineers" labs; VanderPlas, *Python Data Science Handbook*, ch. 4 on Matplotlib) |
| **Prerequisites** | [05-02 NumPy, Vectorization and Numerical Computing](05-02-numpy-and-vectorization.md) |
| **Estimated study hours** | 8 |
| **Last verified** | 2026-11-18 |

**Learning objectives.** After this chapter you can:

1. Solve nonlinear equations and optimization problems numerically with `scipy.optimize`, choosing brackets and starting points sensibly.
2. Fit a physical model to noisy data with `curve_fit`, and report the fitted parameters with their uncertainties.
3. Compute areas under curves and simulate a system described by its rate of change with `scipy.integrate`, and check the results against exact answers.
4. Manipulate formulas symbolically with SymPy (solve, simplify, substitute) and turn a symbolic result into a fast numerical function.
5. Make engineering-quality plots with Matplotlib: labeled axes with units, appropriate log scales, multiple panels, saved as vector files.

## 1. Big picture

NumPy (05-02) gives you arrays; three libraries built on it do most of the remaining numerical work an engineer meets. **SciPy** supplies tested algorithms: root-finders, optimizers, curve fitting, integration, differential-equation solvers, signal processing and statistics. **SymPy** does algebra with symbols, the way you would on paper but without slips. **Matplotlib** draws the figures that turn numbers into decisions. This chapter teaches each through engineering problems, and, just as important, teaches the habit of checking a numerical answer against something you know.

- **Operating points:** a diode, transistor or sensor equation rarely has a closed-form solution; a root-finder gives it in microseconds.
- **Characterization:** fitting a model (an RC time constant, a temperature coefficient, a reliability lifetime) to measured data, with honest uncertainty, is daily work in a test lab.
- **Design equations:** symbolic algebra rearranges and simplifies the formulas you derive, and checks your hand work.
- **Communication:** a clear plot is how engineering results reach reviews, papers and investment memos.

## 2. Intuition first

**Numerical methods answer questions by trying numbers cleverly.** You cannot rearrange $I = I_s(e^{V/V_T} - 1)$ and $I = (V_s - V)/R$ into "V = …", but you can ask: for which $V$ do the two currents agree? A **root-finder** tries values of $V$, uses each result to choose a better guess, and stops when the mismatch is negligible, exactly like the bisection of Example 05-01.7, only faster. An **optimizer** does the same for "which value makes this largest or smallest?". A **curve fit** asks "which parameter values make the model closest to the data?".

**A finance analogy, and its limits.** Solving for an internal rate of return is root-finding; calibrating a yield curve to bond prices is curve fitting; maximizing a portfolio's return for a risk budget is optimization. The same SciPy functions do all three. *Where it breaks:* engineering models come with physics that constrains the answer (a voltage cannot be negative, a time constant must be positive), and the most useful check is often physical, not statistical: does the fitted resistor value match the color code?

**Symbolic versus numerical.** SymPy keeps $R_1$ and $R_2$ as symbols and returns formulas; NumPy and SciPy need numbers and return numbers. Use symbols to derive and simplify a relationship once, then convert it to a numerical function to evaluate it millions of times.

**A plot is an argument.** The same data on linear axes and on logarithmic axes tell different stories (Figure 1). Choosing the axes, labeling them with units and showing the comparison that matters are engineering decisions, not decoration.

![Two panels showing the same RC low-pass filter response. Left: magnitude in volts per volt against frequency in kilohertz on linear axes, where the curve drops to near zero almost immediately and the interesting region is invisible. Right: magnitude in decibels against frequency on a logarithmic axis, flat at 0 dB, minus 3 dB at the 1 kHz corner frequency marked by dashed lines, then falling along a minus 20 dB per decade asymptote.](../../../assets/figures/05-03/axes-choice.svg)

*Figure 1. The same filter response. On linear axes (left) nothing can be read; with a logarithmic frequency axis and the magnitude in decibels (right), the corner and the roll-off slope are obvious.*

## 3. Theory

> **Notation for this chapter.** `np` is NumPy, `sp` is SymPy, `plt` is Matplotlib's `pyplot`, and SciPy functions are imported from their submodules (`from scipy.optimize import brentq`). Code blocks are run in order, as one session, and their outputs checked, as in 05-01. Plots are drawn with the non-interactive `Agg` backend and saved to files, as a script or test would.

### 3.1 Root-finding and optimization (`scipy.optimize`)

**Bracketing root-finders.** `brentq(f, a, b)` finds a root of $f$ between $a$ and $b$, provided $f$ is **continuous** on $[a, b]$ (no jumps, no poles) and $f(a)$ and $f(b)$ have opposite signs. Under those two conditions a continuous function must cross zero somewhere in between (the intermediate value theorem, [01-02](../../01-calculus-for-engineers/chapters/01-02-limits-and-continuity.md)). It combines bisection's guarantee with faster interpolation steps (Brent's method) and is the default choice for one equation in one unknown. Give it a bracket you know contains exactly one root; check the result by substituting it back.

```python
import math
import numpy as np
from scipy.optimize import brentq, minimize_scalar, curve_fit
from scipy.integrate import quad, solve_ivp

f = lambda x: x ** 3 - 2 * x - 5              # a classic test equation
root = brentq(f, 2, 3)
print(f"{root:.10f} {f(root):.1e}")
```

```text
2.0945514815 3.6e-15
```

The continuity condition is not a technicality. The tangent function changes sign between 1 and 2 by jumping through infinity at $\pi/2$, and `brentq` cannot tell a jump from a crossing:

```python
pole = brentq(math.tan, 1, 2)
print(f"{pole:.10f} {math.tan(pole):.1e}")
```

```text
1.5707963268 7.6e+11
```

It "converges" to the pole, where the function is about $10^{12}$, not zero. Substituting back catches it at once.

**Newton's method and the secant method.** Bracketing is safe but needs a bracket. The faster family starts from a single guess $x_k$ and uses the local slope. Near $x_k$ a smooth function is close to its tangent line, $f(x) \approx f(x_k) + f'(x_k)(x - x_k)$ (the first-order Taylor approximation of [01-08](../../01-calculus-for-engineers/chapters/01-08-sequences-series-and-taylor.md)). Setting the tangent line to zero and solving for $x$ gives the next guess:

$$
x_{k+1} = x_k - \frac{f(x_k)}{f'(x_k)} .
$$

Near a **simple root** (one where $f' \ne 0$), the error is roughly squared at every step, so the number of correct digits about doubles per iteration: **quadratic convergence**. The **secant method** replaces $f'(x_k)$ with the slope of the line through the last two points, $x_{k+1} = x_k - f(x_k)\,(x_k - x_{k-1})/[f(x_k) - f(x_{k-1})]$. It needs no derivative and is nearly as fast: the number of correct digits grows by a factor of about 1.6 (the golden ratio) per step. SciPy's `newton(f, x0)` uses the secant method, or Newton's method if you also pass `fprime=`.

```python
fp = lambda x: 3 * x ** 2 - 2                  # derivative of f
x = 2.0
for k in range(4):
    x = x - f(x) / fp(x)
    print(k + 1, f"{x:.15f}", f"{abs(x - root):.1e}")
```

```text
1 2.100000000000000 5.4e-03
2 2.094568121104185 1.7e-05
3 2.094551481698199 1.6e-10
4 2.094551481542327 4.4e-16
```

The errors go $5\times10^{-3}$, $2\times10^{-5}$, $2\times10^{-10}$: each is roughly the square of the one before. After four steps the two methods' answers differ only in the last of the 53 bits ($4.4\times10^{-16}$), the limit of double precision.

**What can go wrong.** A bracketing method without a valid bracket refuses to start (good). Newton-type methods have no such guard. Where the slope is nearly zero, the tangent line points far away and the next guess can land anywhere; from a poor start they can converge to a different root, cycle forever, or (SciPy's `newton`, which stops when successive steps become tiny) stop at a point that is not a root at all (bad; the lab shows each of these). Start Newton close to the root (a quick plot, or a few bisection steps, puts you there), always ask whether the problem has one solution and where it roughly is, and always substitute the answer back.
**Scalar optimization.** `minimize_scalar(g, bounds=(a, b), method="bounded")` finds the minimum of $g$ on an interval; to maximize, minimize $-g$. For several variables, `scipy.optimize.minimize` takes a starting point and a method; multi-dimensional problems may have several local minima, so try several starting points.

### 3.2 Fitting models to data (`curve_fit`)

`curve_fit(model, x, y, p0=...)` adjusts a model's parameters to minimize the sum of squared differences between the model and the data (**nonlinear least squares**), starting from the initial guess `p0`. It returns the best parameters and their **covariance matrix**; the square roots of its diagonal are the parameters' **standard errors**, estimates of how much each fitted value would scatter if the experiment were repeated (03-05).

Good fitting practice:

- Fit a model that comes from physics, with parameters that mean something (a time constant, not "coefficient c").
- Give a sensible `p0`; nonlinear fits can fail or find a poor local minimum from a bad start.
- Look at the **residuals** (data minus model): random scatter means the model fits; a pattern means it does not.
- Report uncertainties. "τ = 1.001 ms ± 0.007 ms" is a measurement; "τ = 1.0013174 ms" is false precision.

> **Going deeper — where the standard errors come from.** Near the best fit, the model is close to linear in its parameters. Let $J$ be its **Jacobian**, the $n \times p$ table of derivatives of the model value at each of the $n$ data points with respect to each of the $p$ parameters. Linear least-squares theory then gives the parameters' covariance matrix as $\sigma^2(J^\mathsf{T}J)^{-1}$, where σ is the standard deviation of the noise on each point. By default (`absolute_sigma=False`) `curve_fit` does not know σ and estimates it from the residuals, $s^2 = \text{SSR}/(n - p)$, where SSR is the sum of squared residuals; dividing by $n - p$ rather than $n$ corrects for the $p$ parameters having been tuned to these very data (the same reasoning as the $n - 1$ in a sample variance, 03-05). If you know the noise level (a calibrated instrument), pass `sigma=` with `absolute_sigma=True` to use it instead, as Example 05-03.2 shows. Either way, the standard errors assume independent noise of constant size, a correct model and the linear approximation. Correlated noise or a wrong model makes them too small, which is why the residual check comes first.

### 3.3 Areas and changes (`scipy.integrate`)

**Area under a curve.** Many engineering quantities are accumulations: the energy delivered by a varying power is the area under the power-versus-time curve; the charge delivered by a current is the area under the current curve. `quad(g, a, b)` computes the area under $g$ between $a$ and $b$ (its **integral**, which Course 01 develops) to a requested accuracy, and returns an error estimate as well. Compare the estimate with the result itself, not with 1: by default `quad` stops once its estimate is below an absolute tolerance of about $1.5\times10^{-8}$, which is generous when the answer is a few nanojoules (box below).

**Change over time.** Many systems are described not by a formula for the quantity but by a rule for how fast it changes. A capacitor charging through a resistor from a source $V_s$ changes its voltage at the rate

$$
\frac{dv}{dt} = \frac{V_s - v}{RC} ,
$$

fast when it is far from $V_s$, slowing as it approaches. `solve_ivp(rate, (t0, t1), [v0])` steps this rule forward from the initial value: an **initial-value problem**. Course 02 solves such equations exactly ($v = V_s(1 - e^{-t/RC})$ here) and explains why; here the point is that a computer can follow the rule numerically for systems with no exact solution, and that you should validate it on one that has one, as Example 05-03.4 does.

> **Going deeper — tolerances.** `quad` and `solve_ivp` choose their internal step sizes adaptively to meet tolerances. `quad` stops when its error estimate is below the larger of `epsabs` and `epsrel` × |result|, both $1.49\times10^{-8}$ by default. For a result that is itself small in SI units (10 nJ, 2 µC), that absolute tolerance is not small by comparison, so pass `epsabs=0` (relative accuracy only) or rescale to natural units (ns, mA). `solve_ivp` uses `rtol` (default $10^{-3}$) and `atol` (default $10^{-6}$), which are coarse for engineering checks; tighten them (`rtol=1e-9`) when you compare against exact results. A solver's answer is only as accurate as its tolerance and the model.

### 3.4 Symbolic algebra (SymPy)

SymPy manipulates expressions made of **symbols**. Declaring symbols `positive=True` lets it simplify square roots and logarithms that would otherwise need sign cases.

```python
import sympy as sp

R1, R2, vin, vout = sp.symbols("R1 R2 V_in V_out", positive=True)
divider = sp.Eq(vout, vin * R2 / (R1 + R2))
print(sp.solve(divider, R2))
Ra, Rb, Rc = sp.symbols("R_a R_b R_c", positive=True)
print(sp.simplify(1 / (1 / Ra + 1 / Rb + 1 / Rc)))
expr = vin * R2 / (R1 + R2)
print(expr.subs({vin: 3.3, R1: 10_000, R2: 4_700}).evalf(5))
```

```text
[R1*V_out/(V_in - V_out)]
R_a*R_b*R_c/(R_a*R_b + R_a*R_c + R_b*R_c)
1.0551
```

- `sp.solve(equation, unknown)` returns a list of solutions; `sp.simplify`, `sp.factor` and `sp.expand` reshape expressions.
- `expr.subs({...})` substitutes values; `evalf(n)` evaluates to `n` significant digits.
- `sp.lambdify(symbols, expr, "numpy")` converts an expression into a fast NumPy function: derive symbolically, evaluate numerically.
- SymPy also differentiates and integrates symbolically (`sp.diff`, `sp.integrate`), which you will use from Course 01 on.

Use SymPy to check hand derivations and to rearrange messy formulas; do not use it to replace understanding. A symbolic answer that is ten lines long is a sign to simplify the model, not to trust the algebra blindly.

### 3.5 Interpolation and statistics

**Interpolation** estimates values between tabulated points: a sensor calibration table, a datasheet curve, a lookup table in firmware. `np.interp(x, xp, fp)` interpolates linearly; `scipy.interpolate.CubicSpline` fits a smooth curve through the points. The choice of *variables* matters more than the method: a thermistor's resistance falls roughly exponentially with temperature, so interpolating temperature against $\ln R$ is far more accurate than against $R$. (In the Beta model used below, $R = R_0e^{B(1/T - 1/T_0)}$ with $T$ in kelvin, $\ln R$ is exactly a straight line in $1/T$, so interpolating $1/T$ against $\ln R$ would be exact for this model; temperature in °C against $\ln R$ is only nearly straight.)

```python
from scipy.interpolate import CubicSpline

t_table = np.array([0.0, 25.0, 50.0, 75.0, 100.0])                        # degrees C
r_table = 10e3 * np.exp(3950 * (1 / (t_table + 273.15) - 1 / 298.15))      # an illustrative 10 kohm NTC
r_meas = 6000.0
exact = 1 / (1 / 298.15 + math.log(r_meas / 10e3) / 3950) - 273.15
linear_r = np.interp(r_meas, r_table[::-1], t_table[::-1])                  # xp must increase, so reverse
linear_log = np.interp(math.log(r_meas), np.log(r_table[::-1]), t_table[::-1])
spline_log = float(CubicSpline(np.log(r_table[::-1]), t_table[::-1])(math.log(r_meas)))
print(f"exact {exact:.3f}, linear in R {linear_r:.3f}, linear in ln R {linear_log:.3f}, spline in ln R {spline_log:.3f}")
```

```text
exact 36.957, linear in R 40.596, linear in ln R 37.460, spline in ln R 36.954
```

Linear interpolation in $R$ is off by 3.6 °C; in $\ln R$ by about 0.5 °C, and a spline in $\ln R$ by only 0.003 °C. Transform the data so it is nearly straight before interpolating, and never extrapolate a table beyond its ends without a model.

**Statistics.** `scipy.stats` provides probability distributions with their densities, cumulative distributions and inverses: `norm.sf(1.5)` is 03-02's $Q(1.5)$ and `norm.isf(1e-12)` the $Q^{-1}$ used for bit-error-rate targets. It also has hypothesis tests and fits for the reliability distributions of 03-05 (Weibull, lognormal). **Signal processing** (`scipy.signal`: filters, spectra, convolution) and **sparse linear algebra** (`scipy.sparse`, for the huge matrices of circuit and field simulators) round out the library; Courses 11, 16 and 13 use them.

### 3.6 Plotting with Matplotlib

Matplotlib's explicit interface is the one to learn: create a **figure** and one or more **axes** (panels) with `fig, ax = plt.subplots()`, draw on each axes object, then save.

```python
import matplotlib
matplotlib.use("Agg")                 # draw to files, no window (scripts, tests, servers)
import matplotlib.pyplot as plt

f = np.logspace(1, 5, 200)            # 10 Hz to 100 kHz, evenly spaced on a log axis
h_db = 20 * np.log10(1 / np.sqrt(1 + (f / 1e3) ** 2))
fig, ax = plt.subplots(figsize=(6, 3.5))
line, = ax.semilogx(f, h_db, label="RC low-pass, $f_c$ = 1 kHz")
ax.set_xlabel("frequency (Hz)")
ax.set_ylabel("magnitude (dB)")
ax.grid(True, which="both", alpha=0.3)
ax.legend()
fig.tight_layout()
fig.savefig("lowpass.svg")
plt.close(fig)
print(len(line.get_xdata()), round(float(np.interp(3.0, np.log10(f), h_db)), 2))
```

```text
200 -3.01
```

Conventions for engineering plots:

- **Label every axis with its quantity and unit**, "frequency (Hz)", not "f".
- **Use log axes for quantities spanning decades** (frequency, current in a diode, failure rates) and decibels for gain (Figure 1).
- **Put compared quantities on the same axes** with a legend; use separate panels (`plt.subplots(1, 2)`) for different units.
- **Save vector formats** (SVG, PDF) for documents; they stay sharp at any size. This curriculum's figures are SVGs made by scripts in `assets/figures/src/` with a shared style ([plotstyle.py](../../../tools/plotstyle.py)).
- **Make figures from scripts, not by hand**, so they can be regenerated when the data change.
- **Close figures** (`plt.close(fig)`) in loops and scripts to free memory.

## 4. Worked examples

### Example 05-03.1 · A diode's operating point

**Setup.** A 5 V source drives a diode through 1 kΩ. The diode obeys $I = I_s(e^{V/V_T} - 1)$ with $I_s = 10^{-14}$ A and $V_T$ = 25.852 mV (the thermal voltage at 300 K); the resistor carries $(5 - V)/1000$. Find the diode voltage and current where the two agree.

**Solution.**

```python
i_s, v_t, v_s, r = 1e-14, 0.025852, 5.0, 1e3
mismatch = lambda v: (v_s - v) / r - i_s * (math.exp(v / v_t) - 1)
v_d = brentq(mismatch, 0.0, 1.0)
print(f"V = {v_d:.4f} V, I = {(v_s - v_d) / r * 1e3:.4f} mA, residual {abs(mismatch(v_d)):.1e} A")
```

```text
V = 0.6925 V, I = 4.3075 mA, residual 4.4e-15 A
```

The diode sits at **0.6925 V** and conducts **4.3075 mA**.

**Check.** At $V$ = 0 the mismatch is +5 mA (resistor current, no diode current); at 1 V the diode term is enormous, so the root is bracketed ✓. The answer is near the familiar "0.7 V" rule of thumb, and the current is close to $(5 - 0.7)/1000$ = 4.3 mA ✓. Course 10 analyzes diode circuits properly.

### Example 05-03.2 · Fitting a time constant to noisy data

**Setup.** A capacitor charging toward an unknown supply voltage $V_s$ with unknown time constant τ is sampled every 0.2 ms for 5 ms, with 20 mV of measurement noise (simulated with seed 2026, true values 3.3 V and 1 ms). Fit $v = V_s(1 - e^{-t/\tau})$ and report both parameters with standard errors.

**Solution.**

```python
rng = np.random.default_rng(2026)
t = np.linspace(0, 5e-3, 26)
v = 3.3 * (1 - np.exp(-t / 1e-3)) + rng.normal(0, 0.02, t.size)
model = lambda t, v_s, tau: v_s * (1 - np.exp(-t / tau))
(v_s_fit, tau_fit), cov = curve_fit(model, t, v, p0=(3.0, 0.5e-3))
err_vs, err_tau = np.sqrt(np.diag(cov))
resid = v - model(t, v_s_fit, tau_fit)
print(f"V_s = {v_s_fit:.4f} +/- {err_vs:.4f} V, tau = {tau_fit * 1e3:.4f} +/- {err_tau * 1e3:.4f} ms")
print(f"rms residual {np.sqrt(np.mean(resid ** 2)) * 1e3:.1f} mV")
```

```text
V_s = 3.3023 +/- 0.0056 V, tau = 1.0013 +/- 0.0065 ms
rms residual 15.2 mV
```

$V_s$ = **3.3023 ± 0.0056 V** and τ = **1.0013 ± 0.0065 ms**, both within one standard error of the true values; the RMS residual, 15 mV, is consistent with the 20 mV noise, so the model fits.

**Check.** If the residual RMS were much larger than the known noise, or the residuals curved systematically, the model would be wrong (a second time constant, a nonlinear capacitor). Report τ as 1.001 ± 0.007 ms: one or two digits of uncertainty set the digits worth quoting.

**Where the ± came from.** By default `curve_fit` estimated the noise from these 26 residuals. Here the noise level is known (20 mV), so it can be supplied instead:

```python
_, cov_known = curve_fit(model, t, v, p0=(3.0, 0.5e-3), sigma=np.full(t.size, 0.02), absolute_sigma=True)
s = np.sqrt(np.sum(resid ** 2) / (t.size - 2))
print(f"s = {s * 1e3:.1f} mV; known noise: +/- {np.sqrt(cov_known[0, 0]):.4f} V, +/- {np.sqrt(cov_known[1, 1]) * 1e3:.4f} ms")
```

```text
s = 15.8 mV; known noise: +/- 0.0071 V, +/- 0.0082 ms
```

This sample happens to scatter less than the true noise (estimated $s$ = **15.8 mV** against 20 mV), so the default standard errors are smaller by the ratio 15.8/20. With the noise level known, the honest uncertainties are **±0.0071 V** and **±0.0082 ms**: τ = 1.001 ± 0.008 ms. With only 26 points, $s$ itself is uncertain by roughly 15%, so either answer is reasonable; what matters is knowing which assumption produced it.

### Example 05-03.3 · Energy of a pulse as an area

**Setup.** A 1 V half-sine pulse lasting 1 µs, $v(t) = \sin(\pi t/T)$, drives a 50 Ω load. The instantaneous power is $v^2/R$ and the energy is the area under the power curve. Compute it with `quad` and compare with the exact value $T/(2R)$.

**Solution.**

```python
T, R_load = 1e-6, 50.0
energy, est_err = quad(lambda t: math.sin(math.pi * t / T) ** 2 / R_load, 0, T, epsabs=0)
print(f"{energy:.6e} J, exact {T / (2 * R_load):.6e} J, error estimate {est_err:.1e}")
```

```text
1.000000e-08 J, exact 1.000000e-08 J, error estimate 1.1e-22
```

The pulse delivers **1.000×10⁻⁸ J** (10 nJ), matching $T/(2R)$.

**Check.** The average of $\sin^2$ over a half period is ½, so the average power is $\tfrac12\times1^2/50$ = 10 mW, and 10 mW for 1 µs is 10 nJ ✓. The error estimate is far below the value, as it should be. Note `epsabs=0`: the answer, $10^{-8}$ J, is smaller than `quad`'s default absolute tolerance ($1.49\times10^{-8}$), so with the defaults `quad` would be entitled to stop at an answer that is wrong by 100%. It does not here, because the integrand is smooth, but in SI units small quantities need relative tolerances (or rescaling to ns and mW).

### Example 05-03.4 · Simulating a charging capacitor

**Setup.** A 1 µF capacitor charges from 0 V through 1 kΩ from a 5 V source. Using `solve_ivp` with tight tolerances, find the voltage at $t$ = 1 ms (one time constant) and compare with $V_s(1 - e^{-1})$.

**Solution.**

```python
tau = 1e3 * 1e-6
sol = solve_ivp(lambda t, v: (5.0 - v) / tau, (0, 5e-3), [0.0], rtol=1e-9, atol=1e-12, dense_output=True)
v_1ms = float(sol.sol(1e-3)[0])
print(f"{v_1ms:.6f} V, exact {5 * (1 - math.exp(-1)):.6f} V, {100 * v_1ms / 5:.2f}% of the supply")
```

```text
3.160603 V, exact 3.160603 V, 63.21% of the supply
```

After one time constant the capacitor holds **3.1606 V**, **63.21%** of the supply, matching the exact solution to the printed digits.

**Check.** The 63% rule is the signature of a first-order system ([07-02](../../07-circuit-analysis-2-transient-and-ac/chapters/07-02-first-order-rc-rl-transients.md)) ✓. Validating a solver on a problem with a known answer, before trusting it on one without, is the habit this example teaches.

### Example 05-03.5 · Maximum power transfer by optimization

**Setup.** A 1 V source with 50 Ω internal resistance drives a load $R_L$, which receives $P = V^2R_L/(R_s + R_L)^2$. Find the $R_L$ that maximizes $P$ and the maximum power.

**Solution.**

```python
power = lambda r_l: 1.0 ** 2 * r_l / (50 + r_l) ** 2
best = minimize_scalar(lambda r_l: -power(r_l), bounds=(1, 1000), method="bounded")
print(f"R_L = {best.x:.3f} ohm, P = {power(best.x) * 1e3:.4f} mW")
```

```text
R_L = 50.000 ohm, P = 5.0000 mW
```

The optimum is **$R_L$ = 50.000 Ω**, delivering **5.0000 mW**.

**Check.** The maximum-power-transfer theorem ([06-09](../../06-circuit-analysis-1-dc/chapters/06-09-maximum-power-transfer.md)) predicts $R_L = R_s$ and $P = V^2/(4R_s)$ = 5 mW ✓. Note that only half the source's power reaches the load at this point: maximum *power* is not maximum *efficiency*, which is why power systems do not operate there.

### Example 05-03.6 · Deriving with symbols, evaluating with arrays

**Setup.** For a divider from 3.3 V with $R_1$ = 10 kΩ on top, solve symbolically for the bottom resistor $R_2$ that gives a desired output, turn the result into a NumPy function, and evaluate it for outputs of 0.5, 1.0, 1.2 and 1.8 V.

**Solution.**

```python
r2_formula = sp.solve(sp.Eq(vout, vin * R2 / (R1 + R2)), R2)[0]
print(r2_formula)
r2_func = sp.lambdify(vout, r2_formula.subs({vin: 3.3, R1: 10_000}), "numpy")
targets = np.array([0.5, 1.0, 1.2, 1.8])
print(np.round(r2_func(targets), 1))
```

```text
R1*V_out/(V_in - V_out)
[ 1785.7  4347.8  5714.3 12000. ]
```

$R_2 = R_1V_{\text{out}}/(V_{\text{in}} - V_{\text{out}})$, giving **1785.7, 4347.8, 5714.3** and **12000.0 Ω** for the four targets.

**Check.** At 1.8 V the output is above half the supply, so $R_2$ must exceed $R_1$: 12 kΩ ✓. In practice you would then pick the nearest E-series value (05-02's broadcasting) and recompute the output.

### Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| T 05-03.a | root of x³ − 2x − 5 | 2.0945514815 | — |
| T 05-03.b | thermistor temperature at 6 kΩ, exact | 36.957 | °C |
| T 05-03.c | linear interpolation in R | 40.596 | °C |
| T 05-03.d | linear interpolation in ln R | 37.460 | °C |
| T 05-03.e | cubic spline in ln R | 36.954 | °C |
| Ex 05-03.1a | diode voltage | 0.6925 | V |
| Ex 05-03.1b | diode current | 4.3075 | mA |
| Ex 05-03.2a | fitted supply voltage | 3.3023 | V |
| Ex 05-03.2b | its standard error | 0.0056 | V |
| Ex 05-03.2c | fitted time constant | 1.0013 | ms |
| Ex 05-03.2d | its standard error | 0.0065 | ms |
| Ex 05-03.2e | noise estimated from the residuals, s | 15.8 | mV |
| Ex 05-03.2f | standard error of V_s with the known 20 mV noise | 0.0071 | V |
| Ex 05-03.2g | standard error of τ with the known 20 mV noise | 0.0082 | ms |
| Ex 05-03.3a | pulse energy | 1.000×10^-8 | J |
| Ex 05-03.4a | voltage after one time constant | 3.1606 | V |
| Ex 05-03.4b | fraction of the supply | 63.21 | % |
| Ex 05-03.5a | optimum load | 50.000 | Ω |
| Ex 05-03.5b | maximum power | 5.0000 | mW |
| Ex 05-03.6a | R₂ for 0.5 V | 1785.7 | Ω |
| Ex 05-03.6b | R₂ for 1.0 V | 4347.8 | Ω |
| Ex 05-03.6c | R₂ for 1.2 V | 5714.3 | Ω |
| Ex 05-03.6d | R₂ for 1.8 V | 12000.0 | Ω |

## 5. Simulate it

The lab ([labs/05-03-lab/](../labs/05-03-lab/README.md)) is a notebook in five parts:

1. **Root-finders compared:** solve the diode equation with bisection (05-01), `brentq` and Newton's method from several starting points, counting function evaluations. *Predict first:* which needs fewest, and which can fail?
2. **Fitting and residuals:** fit a single exponential to data that actually contain two time constants, and learn to spot the misfit in the residual plot.
3. **Integration accuracy:** compute the area under $e^t$ with a crude sum of rectangles, the trapezoid rule and `quad`, and watch the errors shrink at different rates as the number of points grows.
4. **SymPy as a checker:** verify a hand-derived formula (a Wheatstone bridge's balance condition) symbolically.
5. **A publication-quality figure:** reproduce Figure 1 from data and save it as SVG.

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Bracketing root-finder (brentq) versus Newton-type from a guess | Guaranteed convergence within the bracket | Needs a valid bracket; slightly more evaluations | Analyst |
| Physical model versus flexible curve (polynomial) in a fit | Parameters with meaning, sensible extrapolation | May not fit if the physics is incomplete | Characterization engineer |
| Tight solver tolerances | Accuracy that can be trusted for comparisons | Run time | Analyst |
| Symbolic derivation versus numerical only | General formulas, insight, checks of hand work | Expressions can blow up in size; slow to evaluate unless lambdified | Engineer |
| Log axes and dB in plots | Readable behavior across decades | Unfamiliar to some audiences; zero and negative values cannot be shown | Author of the figure |
| Scripted figures versus hand-made | Reproducible, regenerable with new data | Upfront effort | Team conventions |

## 7. Numbers to know

| Quantity | Value | Note |
|---|---|---|
| One time constant of charging | 63.21% of the final value | $1 - e^{-1}$ |
| −3 dB | power ratio ½, amplitude ratio $1/\sqrt2$ ≈ 0.7071 | First-order filter at its corner |
| First-order roll-off | −20 dB per decade | Figure 1 |
| Diode forward voltage (silicon, mA currents) | about 0.6–0.7 V | Example 05-03.1 |
| `solve_ivp` default relative tolerance | 10⁻³ | Tighten for verification |
| Maximum power transfer | $R_L = R_s$, $P = V^2/4R_s$, 50% efficiency | Example 05-03.5 |

## 8. Common mistakes

1. **Trusting a root without checking it.** Substitute it back and check it is in the physically meaningful range.
2. **No bracket, or a bracket with several roots.** Plot the function first.
3. **Bad initial guesses for nonlinear fits.** Start from physically sensible values; a time constant guess off by 1000× may never converge.
4. **Quoting fitted values without uncertainty**, or with more digits than the uncertainty supports.
5. **Ignoring residuals.** A good-looking curve through the points can hide a systematic misfit.
6. **Default solver tolerances in verification.** `solve_ivp`'s defaults are loose.
7. **Unlabeled axes, missing units, linear axes for multi-decade data.**
8. **Using SymPy results without simplifying or checking a special case** (set a value to zero or infinity and see if the answer makes sense).

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **The stack.** SciPy, SymPy and Matplotlib all build on NumPy, whose 2.0 release (June 2024) changed type-promotion rules and broke binary compatibility for compiled extensions; libraries had to release NumPy-2-compatible versions, a reminder that the scientific stack moves together ([R-087](../../../reference/research-log.md#r-087--python-releases-floating-point-and-developer-usage)) **[Established]**.
- **Where these tools sit.** Commercial engineering suites (circuit simulators, MATLAB-style environments) and the open Python stack coexist: circuit simulation stays in SPICE-class tools (Course 06 uses ngspice), while data analysis, fitting and plotting increasingly happen in Python, in which 58% of the Stack Overflow 2026 respondents who answered the language question reported extensive development work over the past year ([R-087](../../../reference/research-log.md#r-087--python-releases-floating-point-and-developer-usage)) **[Industry estimate]**.

### Why it matters commercially

Every characterization report, reliability qualification and benchmark chart in a data room is the output of a fit, a solver or a plot. The fits carry assumptions (the model, the weighting, which points were excluded); the plots carry choices (axes, ranges, what is compared). Knowing how these tools work lets you ask whether a "measured" number is a direct measurement or a model's output, and how sensitive it is to the analyst's choices.

### Marketing vs Reality

- **"Measured lifetime: 10 years."** *Reality:* usually a model (an Arrhenius or Weibull fit, 03-05) fitted to short accelerated tests and extrapolated. Ask for the model, the fitted parameters with uncertainties, and the extrapolation factor.
- **The chart that starts at 90%.** *Reality:* a truncated or logarithmic axis can make a 2% improvement look like a doubling, or hide a large one. Read the axes before the curves.
- **"Our model fits the data with R² = 0.99."** *Reality:* a high R² says little about extrapolation or about systematic misfit; residual plots and out-of-sample checks say more. Ask to see the residuals.

### Questions for engineering leaders

1. **"Which numbers in this report are measured directly, and which are model outputs?"** *Strong:* a clear distinction, with model assumptions and uncertainties. *Evasive:* "all measured".
2. **"What are the uncertainties on these fitted parameters, and how were they estimated?"** *Strong:* standard errors or confidence intervals, and the noise model. *Evasive:* single numbers only.
3. **"Can you regenerate this figure from the raw data?"** *Strong:* scripted analysis under version control. *Evasive:* "the analyst who made it has left".
4. **"How do you validate your numerical models?"** *Strong:* checks against analytical cases and measurements. *Evasive:* "the software is industry standard".

## 10. Concept check

1. What does `brentq` need from you, and what does it guarantee?

   <details><summary>Answer</summary>

   A function that is continuous on an interval, and an interval where it changes sign. It then guarantees to converge to a root inside that interval. Without continuity the guarantee is void: on $[1, 2]$, `brentq(math.tan, 1, 2)` converges to the pole at $\pi/2$, which is why you substitute the answer back.

   </details>

2. Why does `curve_fit` need a starting guess, and what should you report besides the fitted values?

   <details><summary>Answer</summary>

   Nonlinear least squares is solved iteratively and can fail or reach a poor local minimum from a bad start. Report standard errors (from the covariance matrix) and check the residuals.

   </details>

3. What does `quad` compute, and how do you know whether to trust it?

   <details><summary>Answer</summary>

   The area under a function between two limits (its integral). It returns an error estimate; check that it is small relative to the result, and test against a case with a known answer.

   </details>

4. Why compare `solve_ivp` against an exact solution with tight tolerances before using it on a new problem?

   <details><summary>Answer</summary>

   To confirm the setup (equation, initial condition, units) and that the tolerances are tight enough; default tolerances are loose and a wrong setup can produce plausible curves.

   </details>

5. When is SymPy the right tool and when is NumPy?

   <details><summary>Answer</summary>

   SymPy for deriving, rearranging and checking formulas with symbols; NumPy for evaluating numbers, especially many of them. `lambdify` bridges the two.

   </details>

6. Why plot a filter's response on a log-frequency axis in dB?

   <details><summary>Answer</summary>

   Its behavior spans decades of frequency and orders of magnitude of gain; log scales make the corner frequency and the constant roll-off slope visible, whereas linear axes compress everything into a corner.

   </details>

Problem set: [05-03 problems](../problems/05-03-problems.md) · [solutions](../solutions/05-03-solutions.md).

## 11. Key terms

[Root-finding](../../../reference/glossary.md#root-finding) ·
[Brent's method](../../../reference/glossary.md#brents-method) ·
[Nonlinear least squares](../../../reference/glossary.md#nonlinear-least-squares) ·
[Residual](../../../reference/glossary.md#residual) ·
[Standard error](../../../reference/glossary.md#standard-error) ·
[Initial-value problem](../../../reference/glossary.md#initial-value-problem) ·
[Symbolic computation](../../../reference/glossary.md#symbolic-computation) ·
[Decibel](../../../reference/glossary.md#decibel)

## 12. Connections

- **Previous:** [05-02](05-02-numpy-and-vectorization.md) (arrays, the foundation of all three libraries), [05-01](05-01-python-fundamentals.md) (bisection and functions as arguments).
- **Next:** [05-04 Jupyter, Testing and Reproducible Workflows](05-04-reproducible-workflows.md): making analyses like these trustworthy and repeatable.
- **Used in:** [01-05](../../01-calculus-for-engineers/chapters/01-05-integrals.md) (integrals, which `quad` computes), [02-02](../../02-complex-numbers-des-and-linear-algebra/chapters/02-02-first-order-linear-odes.md) (the differential equations `solve_ivp` solves), [02-10](../../02-complex-numbers-des-and-linear-algebra/chapters/02-10-numerical-methods.md) (how these algorithms work), [03-05](../../03-probability-statistics-and-random-variables/chapters/03-05-estimation-and-hypothesis-testing.md) (estimation and uncertainty), every lab notebook.

## 13. Further study

- VanderPlas, J., *Python Data Science Handbook*, 2nd ed., chapter 4, "Visualization with Matplotlib" (free online).
- The SciPy User Guide, docs.scipy.org: "Optimization", "Integration" and "Interpolation" tutorials.
- The SymPy Tutorial, docs.sympy.org: "Basic Operations", "Simplification" and "Solvers".
- *Video:* MIT OpenCourseWare 6.0002, *Introduction to Computational Thinking and Data Science* (Fall 2016), Lecture 9, "Understanding Experimental Data" (fitting models to measurements and judging the fit), and Lecture 10 (continuing the topic).

## 14. Sources

1. SciPy documentation (scipy.optimize, scipy.integrate), docs.scipy.org.
2. SymPy documentation, docs.sympy.org.
3. Matplotlib documentation, matplotlib.org.
4. VanderPlas, J., *Python Data Science Handbook*, O'Reilly.
5. NumPy 2.0 release notes; Stack Overflow Developer Survey 2026. [R-087]
