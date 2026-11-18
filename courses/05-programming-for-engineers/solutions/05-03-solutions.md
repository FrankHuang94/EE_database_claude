# Solutions 05-03 · SciPy, SymPy and Matplotlib

Problems: [05-03 problems](../problems/05-03-problems.md) · Chapter: [05-03](../chapters/05-03-scipy-sympy-matplotlib.md). Every code block below is run by [verify_05_03.py](../verify/verify_05_03.py), which checks that it prints exactly what is shown and recomputes every number in the answer key independently.

---

## Solutions

### Solution 05-03.1

```python
import math
import numpy as np
import sympy as sp
from scipy.optimize import brentq, minimize_scalar, curve_fit
from scipy.integrate import quad, solve_ivp
from scipy.interpolate import CubicSpline

g = lambda x: math.cos(x) - x
print(g(0.0), round(g(1.0), 4), f"{brentq(g, 0, 1):.10f}")
```

```text
1.0 -0.4597 0.7390851332
```

$g(0) = 1 > 0$ and $g(1) = \cos1 - 1 < 0$, so the bracket contains a sign change, and since $g$ is decreasing it contains exactly one root: **0.7390851332**.

### Solution 05-03.2

```python
res = minimize_scalar(lambda x: x * x - 4 * x + 7, bounds=(-10, 10), method="bounded")
print(f"{res.x:.6f} {res.fun:.6f}")
```

```text
2.000000 3.000000
```

The minimum is at **x = 2** with value **3**. By hand, $x^2 - 4x + 7 = (x - 2)^2 + 3$, which is smallest when the square is zero ✓.

### Solution 05-03.3

```python
i_s, v_t = 1e-14, 0.025852
v_d = brentq(lambda v: (3.3 - v) / 330 - i_s * (math.exp(v / v_t) - 1), 0.0, 1.0)
print(f"{v_d:.4f} V, {(3.3 - v_d) / 330 * 1e3:.4f} mA")
```

```text
0.7081 V, 7.8543 mA
```

**0.7081 V** and **7.8543 mA**. The larger current needs a slightly larger voltage: the diode voltage rises by $V_T\ln(7.854/4.308) =$ **15.5 mV** for an 82% increase in current, the logarithmic behavior that makes a diode's voltage nearly constant.

### Solution 05-03.4

```python
rng = np.random.default_rng(11)
t = np.linspace(0, 10e-3, 21)
y = 5.0 * np.exp(-t / 2e-3) + rng.normal(0, 0.05, t.size)
(v0, tau), cov = curve_fit(lambda t, v0, tau: v0 * np.exp(-t / tau), t, y, p0=(4.0, 1e-3))
e_v0, e_tau = np.sqrt(np.diag(cov))
print(f"V0 = {v0:.3f} +/- {e_v0:.3f} V, tau = {tau * 1e3:.3f} +/- {e_tau * 1e3:.3f} ms")
```

```text
V0 = 5.032 +/- 0.032 V, tau = 1.998 +/- 0.021 ms
```

$V_0$ = **5.032 ± 0.032 V** and τ = **1.998 ± 0.021 ms**, both within about one standard error of the true 5 V and 2 ms.

### Solution 05-03.5

```python
total, _ = quad(lambda t: 2e-3 * math.exp(-t / 1e-3), 0, np.inf)
first_ms, _ = quad(lambda t: 2e-3 * math.exp(-t / 1e-3), 0, 1e-3)
print(f"{total * 1e6:.4f} uC {first_ms * 1e6:.4f} uC {100 * first_ms / total:.2f}%")
```

```text
2.0000 uC 1.2642 uC 63.21%
```

The total charge is **2.0000 µC** (peak current × time constant, 2 mA × 1 ms), and **1.2642 µC**, 63.21%, arrives in the first time constant. `quad` handles the infinite upper limit by a change of variables.

### Solution 05-03.6

```python
sol = solve_ivp(lambda t, i: (12 - 6 * i) / 3e-3, (0, 2e-3), [0.0], rtol=1e-10, atol=1e-12, dense_output=True)
print(f"{float(sol.sol(0.5e-3)[0]):.4f} A, exact {12 / 6 * (1 - math.exp(-0.5e-3 * 6 / 3e-3)):.4f} A")
```

```text
1.2642 A, exact 1.2642 A
```

The current is **1.2642 A** at 0.5 ms, which is one time constant ($L/R$ = 0.5 ms), so 63.2% of the final 2 A ✓. An inductor's current rises with the same shape as a capacitor's voltage.

### Solution 05-03.7

```python
r2 = sp.symbols("R2", positive=True)
sol7 = sp.solve(sp.Eq(10_000 * r2 / (10_000 + r2), 4_700), r2)
print(sol7, sp.N(sol7[0], 6))
```

```text
[470000/53] 8867.92
```

$R_2 = 470000/53$ = **8867.92 Ω**. The nearest E12 value is 8.2 kΩ (giving **4.505 kΩ** in parallel) and the nearest E24 value 9.1 kΩ (**4.764 kΩ**): the exact value is rarely available, so designs choose the nearest standard part and accept the error.

### Solution 05-03.8

```python
r1, r2b = sp.symbols("R1 R2", positive=True)
print(sp.simplify((r1 * r2b / (r1 + r2b)) * (1 / r1 + 1 / r2b)))
```

```text
1
```

The product simplifies to **1**: the parallel resistance is exactly the reciprocal of the sum of conductances $1/R_1 + 1/R_2$. Simplifying to a constant is a quick check that two forms of a formula agree.

### Solution 05-03.9

```python
bias = np.array([0, 1, 2, 3, 4, 5.0])
cap = np.array([10, 9.6, 8.7, 7.5, 6.3, 5.2])
print(f"{np.interp(2.5, bias, cap):.3f} {float(CubicSpline(bias, cap)(2.5)):.3f}")
```

```text
8.100 8.117
```

Linear interpolation gives **8.100 µF** and the cubic spline **8.117 µF**: the curve is smooth, so the two agree to 0.2%. A "10 µF" capacitor at 2.5 V bias provides only about 8.1 µF, the DC-bias loss of class 2 ceramics (04-04).

### Solution 05-03.10

```python
rng = np.random.default_rng(5)
t2 = np.linspace(0, 25e-3, 51)
y2 = 5 * (1 - np.exp(-t2 / 1e-3)) + 0.5 * (1 - np.exp(-t2 / 5e-3)) + rng.normal(0, 0.01, t2.size)
model = lambda t, vs, tau: vs * (1 - np.exp(-t / tau))
(vs, tau2), _ = curve_fit(model, t2, y2, p0=(5.0, 1e-3))
resid = y2 - model(t2, vs, tau2)
print(f"Vs = {vs:.3f} V, tau = {tau2 * 1e3:.3f} ms, rms residual {np.sqrt(np.mean(resid ** 2)) * 1e3:.1f} mV")
print(np.sign(resid[[2, 10, 20, 40]]))
```

```text
Vs = 5.446 V, tau = 1.148 ms, rms residual 49.7 mV
[ 1. -1. -1.  1.]
```

The fit gives $V_s$ = **5.446 V** and τ = **1.148 ms**, with an RMS residual of **49.7 mV**, five times the 10 mV noise. The residuals are not random: they have long runs of the same sign (the signs printed at four times show the pattern), the signature of a missing slow component. A two-exponential model would fit to the noise level.

### Solution 05-03.11

```python
f = np.logspace(1, 6, 50_001)
h_db = 20 * np.log10(1 / np.sqrt(1 + (f / 1e3) ** 2))
f_cross = np.interp(-20.0, h_db[::-1], f[::-1])        # h_db falls, so reverse to increasing
print(f"{f_cross:.1f} Hz, exact {1e3 * math.sqrt(99):.1f} Hz")
```

```text
9949.9 Hz, exact 9949.9 Hz
```

The response crosses −20 dB at **9949.9 Hz**. Exactly, $1 + (f/f_c)^2 = 100$ gives $f = f_c\sqrt{99}$ = **9949.9 Hz**: slightly below one decade above the corner, because the −20 dB/decade asymptote is approached only gradually.

### Solution 05-03.12

```python
x = sp.symbols("x")
p = x ** 3 - 6 * x ** 2 + 11 * x - 6
print(sp.solve(p, x), sp.factor(p))
f12 = sp.lambdify(x, p)
print([round(brentq(f12, a, b), 10) for a, b in ((0.5, 1.5), (1.5, 2.5), (2.5, 3.5))], f12(0) * f12(4) < 0)
```

```text
[1, 2, 3] (x - 3)*(x - 2)*(x - 1)
[1.0, 2.0, 3.0] True
```

The roots are exactly **1, 2 and 3** ($p = (x-1)(x-2)(x-3)$), and `brentq` finds each from its own bracket. On $[0, 4]$ the endpoints have opposite signs ($p(0) = -6$, $p(4) = 6$), so `brentq` would run, but it returns only *one* of the three roots, and which one depends on the algorithm's steps: a valid bracket guarantees a root, not a particular root. Plot first, then bracket each root separately.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 05-03.1a | root of cos x = x | 0.7390851332 | — |
| 05-03.2a | location of the minimum | 2.000000 | — |
| 05-03.2b | minimum value | 3.000000 | — |
| 05-03.3a | diode voltage | 0.7081 | V |
| 05-03.3b | diode current | 7.8543 | mA |
| 05-03.3c | rise in diode voltage from Example 05-03.1 | 15.5 | mV |
| 05-03.4a | fitted V₀ | 5.032 | V |
| 05-03.4b | its standard error | 0.032 | V |
| 05-03.4c | fitted τ | 1.998 | ms |
| 05-03.4d | its standard error | 0.021 | ms |
| 05-03.5a | total charge | 2.0000 | µC |
| 05-03.5b | charge in the first millisecond | 1.2642 | µC |
| 05-03.6a | current at 0.5 ms | 1.2642 | A |
| 05-03.7a | parallel partner for 4.7 kΩ | 8867.92 | Ω |
| 05-03.7b | 10 kΩ ∥ 8.2 kΩ | 4.505 | kΩ |
| 05-03.7c | 10 kΩ ∥ 9.1 kΩ | 4.764 | kΩ |
| 05-03.9a | linear interpolation at 2.5 V | 8.100 | µF |
| 05-03.9b | cubic spline at 2.5 V | 8.117 | µF |
| 05-03.10a | fitted Vs (wrong model) | 5.446 | V |
| 05-03.10b | fitted τ (wrong model) | 1.148 | ms |
| 05-03.10c | RMS residual | 49.7 | mV |
| 05-03.11a | −20 dB crossing | 9949.9 | Hz |
| 05-03.12a | number of real roots | 3 | — |
