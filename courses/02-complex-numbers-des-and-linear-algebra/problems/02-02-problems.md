# Problems 02-02 · First-Order Linear ODEs

Chapter: [02-02](../chapters/02-02-first-order-linear-odes.md) · Worked solutions: [02-02 solutions](../solutions/02-02-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** answers to 4 significant figures unless stated. Always check a solution by substituting it back into the equation and the initial condition. Use a calculator or Python freely, but show the method.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 02-02.1 [A]

**Classify and verify.**

(a) For each equation, state the order and whether it is linear, homogeneous and autonomous: (i) $y' + 4y = 0$; (ii) $y' = y\sin t$; (iii) $L\,di/dt + Ri = V_0\cos\omega t$; (iv) $y' = 1 - y^3$.
(b) Show that $y = 2 - e^{-3t}$ solves $y' = 6 - 3y$ with $y(0) = 1$.
(c) Show that $y = 1/(1 + t)$ solves $y' = -y^2$, and find the initial condition it satisfies.

### Problem 02-02.2 [A]

**Separable equations.**

(a) Solve $y' = -2ty$ with $y(0) = 5$, and evaluate $y(1)$.
(b) Solve $y' = 1 + y^2$ with $y(0) = 0$. At what time does the solution blow up?

### Problem 02-02.3 [A]

**A phase line.** For $y' = y^2 - y - 2$:

(a) Find the equilibria and classify each as stable or unstable.
(b) Find the local time constant at the stable equilibrium.
(c) Sketch the phase line. Where does a solution starting at $y(0) = 1$ go? And one starting at $y(0) = 3$?

### Problem 02-02.4 [A]

**Integrating factor with constant coefficients.** Solve $y' + 3y = 6$ with $y(0) = 0$. Identify the time constant and the steady state, and find when $y$ reaches 1.9.

### Problem 02-02.5 [B]

**A variable coefficient.** Solve $ty' - y = t^3$ for $t > 0$ with $y(1) = 2$, and evaluate $y(2)$. Check your answer by substitution.

### Problem 02-02.6 [B]

**The integrating factor as a discount factor.**

(a) A balance earns a continuously compounded rate $r(t) = 0.02 + 0.004t$ per year, with no deposits, starting from \$100,000. Solve $B' = r(t)B$ and find $B(10)$.
(b) Write the integrating factor $D(t)$ for (a) and evaluate $D(10)$. Interpret it.
(c) A second account earns a constant 5% per year, starts at \$50,000 and receives deposits at a steady \$10,000 per year. Solve $B' = 0.05B + 10\,000$ and find $B(10)$. Split the answer into the growth of the initial balance and the future value of the deposits.

### Problem 02-02.7 [B]

**A sluggish sensor.** A temperature probe with time constant $\tau = 4$ s obeys $\tau T_p' + T_p = T_{oven}(t)$. The oven starts at 25 °C, and the probe also reads 25 °C. From $t = 0$ the oven ramps at 2 °C/s.

(a) Find the probe's steady lag, in time and in degrees.
(b) How long until the error is within 1% of its final value?
(c) What does the probe read at $t = 10$ s, and what is the error then?

### Problem 02-02.8 [B]

**Exponential inputs, including the matched case.** An RC low-pass with $\tau = 1$ ms, initially at 0 V, is driven by $v_{in} = 5e^{-t/\tau_2}$ V.

(a) For $\tau_2 = 0.5$ ms, find $v(t)$. When does it peak, and at what value?
(b) For $\tau_2 = \tau = 1$ ms, find $v(t)$, its peak time and its peak value.
(c) Explain why the method of (a) fails in (b).

### Problem 02-02.9 [B]

**An RL circuit switched onto a sinusoid.** At $t = 0$ a source $10\cos(2\pi\cdot5000\,t)$ V is connected to a 1 mH inductor in series with 10 Ω. The current starts at zero.

(a) Find the time constant and $\omega\tau$.
(b) Find the steady-state current: amplitude and phase relative to the source.
(c) Find the full current $i(t)$, including the transient.

### Problem 02-02.10 [B]

**A technology-adoption S-curve.** A product's installed base follows the logistic equation with capacity $K = 200$ million units, $N(0) = 2$ million and $r = 0.8$ per year.

(a) When does the installed base reach half the capacity?
(b) How long does it take to go from 10% to 90% of capacity?
(c) What is the installed base after 3 years?
(d) An analyst fits pure exponential growth, $N_0e^{rt}$, to the first two years of data and extrapolates to year 6. What does that predict, and what does the logistic model say? What is the lesson for market sizing?

### Problem 02-02.11 [B]

**Existence and uniqueness.**

(a) $y' = 3y^{2/3}$ with $y(0) = 0$. Show that $y = 0$ and $y = t^3$ are both solutions. Which hypothesis of the uniqueness theorem fails?
(b) $y' + (\tan t)\,y = \cos t$ with $y(0) = 1$. On what interval does the linear-equation theorem guarantee a unique solution? Solve the problem.
(c) $y' = y^2$ with $y(0) = 2$. Solve it and find when it blows up.

### Problem 02-02.12 [B]

**Choosing a time step.** Integrate $y' = -y/\tau$ with $\tau = 1$ µs and $y(0) = 1$.

(a) What is the largest step for which forward Euler is stable?
(b) With $h = 0.5$ µs, find $y(2\text{ µs})$ by forward Euler, by backward Euler, $y_{n+1} = y_n/(1 + h/\tau)$, and by the trapezoidal rule, $y_{n+1} = y_n\dfrac{1 - h/(2\tau)}{1 + h/(2\tau)}$. Compare each with the exact value.
(c) Which method would you choose for a stiff circuit, and why?

### Problem 02-02.13 [C]

**A Bernoulli equation.** Solve $y' + y = y^2$ with $y(0) = 0.5$ by the substitution $v = 1/y$, and evaluate $y(1)$. Show that the result is a logistic-type curve, and identify its equilibria.

### Problem 02-02.14 [C]

**Burst performance and skin temperature.** A phone's case has heat capacity $C_{th} = 30$ J/K and thermal resistance $R_{th} = 10$ K/W to 25 °C ambient. The skin-temperature limit is 43 °C (illustrative values).

(a) What power can the phone sustain indefinitely?
(b) The phone idles at 1.0 W until it reaches equilibrium. What is its temperature?
(c) A game starts and the SoC draws 5 W. How long until the skin limit is reached? Repeat for 3 W.
(d) When the limit is reached, the governor drops the power to the sustainable level from (a). What happens to the temperature afterward, and why?
(e) Express the burst duration at 5 W as a fraction of the thermal time constant, and explain why a reviewer's single short benchmark run overstates the phone's sustained performance.

### Problem 02-02.15 [C]

**A switch that turns off slowly.** A sampling capacitor $C = 10$ pF, charged to $v_0$, discharges through a transistor switch whose resistance rises as it turns off: $R(t) = R_0e^{t/T}$, with $R_0 = 100$ Ω and $T = 2$ ns.

(a) Write the ODE for $v(t)$ and solve it (it is linear and separable, with a variable coefficient).
(b) What fraction of $v_0$ remains at $t = 2$ ns, and as $t \to \infty$?
(c) Compare with a switch of constant resistance $R_0$. What does this say about how fast a sampling switch must turn off, relative to $R_0C$?

---

## Objective coverage

| Learning objective (chapter 02-02) | Problems |
|---|---|
| 1. Classify ODEs; verify solutions of initial-value problems | 1, 11 |
| 2. Direction fields, phase lines, equilibria and their stability | 3, 10, 13 |
| 3. Separable equations, including nonlinear ones | 2, 10, 13, 15 |
| 4. Integrating factor; discount factor; Bernoulli substitution | 4, 5, 6, 11(b), 13, 15 |
| 5. Natural and forced responses; step, ramp, exponential and sinusoidal inputs | 7, 8, 9, 14 |
| 6. Existence and uniqueness; finite-time blow-up; Euler's method and stability | 2(b), 11, 12 |
