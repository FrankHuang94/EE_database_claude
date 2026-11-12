# Problems 01-08 · Sequences, Series and Taylor Expansions

Chapter: [01-08](../chapters/01-08-sequences-series-and-taylor.md) · Worked solutions: [01-08 solutions](../solutions/01-08-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** angles in radians; $V_T = 25.85$ mV; answers to 4 significant figures unless stated. For every series, say which test you use; for every approximation, estimate its error.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 01-08.1 [A]

Find each limit or sum.

(a) $\lim_{n\to\infty}\dfrac{2n + 1}{3n - 2}$  (b) $\lim_{n\to\infty}\left(1 + \dfrac{2}{n}\right)^n$  (c) $\displaystyle\sum_{k=0}^\infty\left(\tfrac{1}{3}\right)^k$  (d) $\displaystyle\sum_{k=1}^\infty0.9^k$  (e) $\displaystyle\sum_{k=0}^{9}2^k$

### Problem 01-08.2 [A]

Decide whether each series converges, naming the test. Give the sum where it is a known value.

(a) $\sum_{k\ge1}\dfrac{1}{k^2}$ (sum $\pi^2/6$)  (b) $\sum_{k\ge1}\dfrac{1}{k}$  (c) $\sum_{k\ge1}\dfrac{k}{2^k}$ (sum 2)  (d) $\sum_{k\ge1}\dfrac{(-1)^{k+1}}{k}$ (sum $\ln 2$)  (e) $\sum_{k\ge1}\dfrac{k!}{10^k}$

### Problem 01-08.3 [A]

(a) Write the first four nonzero terms of the Maclaurin series of $e^{-x}$, $\cos2x$, $1/(1 + x)$, $\ln(1 + x)$ and $\sqrt{1 + x}$.
(b) Evaluate the four-term series for $e^{-x}$ at $x = 0.1$, and compare with $e^{-0.1}$.

### Problem 01-08.4 [A]

Find the radius of convergence.

(a) $\sum\dfrac{x^k}{k}$  (b) $\sum\dfrac{x^k}{k!}$  (c) $\sum k!\,x^k$  (d) $\sum\dfrac{(x - 2)^k}{3^k}$, and the interval on which it converges (ignore the endpoints)

### Problem 01-08.5 [B]

**A first-order digital filter.** $y[n] = 0.8\,y[n-1] + x[n]$, with $y[-1] = 0$.

(a) Show that its impulse response is $h[n] = 0.8^n$ for $n \ge 0$.
(b) Find the DC gain $\sum_{n\ge0}h[n]$, which is also the final value of the step response.
(c) After how many samples does $h[n]$ first fall below 1% of $h[0]$?
(d) What happens if the coefficient 0.8 is replaced by 1.1?

### Problem 01-08.6 [B]

**Annuities and perpetuities** (for the finance-trained reader).

(a) Find the present value of 1 per year for 30 years at a 5% discount rate.
(b) Find the present value of a perpetuity of 1 per year at 5%.
(c) A datacenter efficiency upgrade saves \$1 M per year for 10 years. At an 8% discount rate, what is the present value of the savings?
(d) Explain why a perpetuity at a 0% discount rate has no finite value, in series terms.

### Problem 01-08.7 [B]

(a) Approximate $\cos0.5$ with $1 - x^2/2 + x^4/24$. Find the actual error and the alternating-series bound.
(b) How many nonzero terms of the Maclaurin series of $\sin x$ guarantee an error below $10^{-6}$ for all $\lvert x\rvert \le \pi/2$? Use the Lagrange bound $\lvert x\rvert^{2n+3}/(2n + 3)!$ after the term in $x^{2n+1}$.

### Problem 01-08.8 [B]

Approximate to first order, then estimate the error from the next term, and compare with the exact value.

(a) $\sqrt{1.05}$  (b) $1/0.98$  (c) $1.03^5$

### Problem 01-08.9 [B]

A non-inverting amplifier has ideal gain $1/\beta = 11$.

(a) For open-loop gain $A = 2\times10^5$, find the exact closed-loop gain and its relative error in ppm. Compare with $1/(A\beta)$.
(b) Repeat for $A = 1000$. Is the first-order estimate still adequate?
(c) What open-loop gain is needed for a 0.01% gain error?

### Problem 01-08.10 [B]

(a) Using the series for $e^x$, $\cos x$ and $\sin x$, show that $e^{j\theta} = \cos\theta + j\sin\theta$.
(b) Sum the series for $e^{j\pi/3}$ through the term $(j\pi/3)^6/6!$, and find the magnitude of the error against $\tfrac{1}{2} + j\tfrac{\sqrt{3}}{2}$.

### Problem 01-08.11 [B]

**Error terms of numerical derivatives.**

(a) Expand $f(x \pm h)$ to third order and show that the forward difference has error $\tfrac{h}{2}f''(x) + O(h^2)$ and the central difference $\tfrac{h^2}{6}f'''(x) + O(h^4)$.
(b) Check both for $f = e^x$ at $x = 0$ with $h = 0.1$.
(c) **Richardson extrapolation** combines two estimates to cancel the leading error: $D_R = \big(4D_0(h/2) - D_0(h)\big)/3$ for central differences. Compute its error for $h = 0.1$.

### Problem 01-08.12 [C]

**Compression and intercept points of a cubic amplifier.** An amplifier has $y = x - 0.05x^3$ (volts).

(a) For $x = A\cos\omega t$ with $A = 1$ V, find the fundamental output amplitude and HD3, defined here as the third-harmonic amplitude divided by the *actual* (compressed) fundamental. Compare with the small-signal formula of chapter §3.8.
(b) The **1 dB compression point** is the input amplitude at which the fundamental gain falls 1 dB below $a_1$. Find it.
(c) The **third-order intercept** (input-referred) is the amplitude at which the extrapolated third-order intermodulation product of a two-tone test would equal the fundamental. Show that for a cubic it is $A_{IP3} = \sqrt{\tfrac{4}{3}\lvert a_1/a_3\rvert}$ (hint: expand $a_3x^3$ with $x = A(\cos\omega_1t + \cos\omega_2t)$ and find the term at $2\omega_1 - \omega_2$). Evaluate it, and show that $A_{IP3}/A_{1dB}$ is about 9.6 dB, independent of $a_3$.

### Problem 01-08.13 [C]

**How good is the Taylor estimate of distortion?** For an exponential device, compare HD2 from $A/(4V_T)$ with the exact $I_2(A/V_T)/I_1(A/V_T)$ (modified Bessel functions; SciPy's `scipy.special.iv`) at $A = 1$, 5, 10 and 25.85 mV. At what amplitude does the Taylor estimate err by more than 1% of its own value?

### Problem 01-08.14 [C]

**Convergence speed matters.**

(a) The Leibniz series $\pi = 4\left(1 - \tfrac{1}{3} + \tfrac{1}{5} - \cdots\right)$ comes from $\arctan1$. How many terms guarantee π to within $10^{-6}$?
(b) Machin's formula $\pi = 16\arctan\tfrac{1}{5} - 4\arctan\tfrac{1}{239}$ uses the same series at much smaller arguments. Evaluate it with 5 terms of each arctan series, and find the error.
(c) Explain the difference in terms of the radius of convergence and the distance of the argument from its edge.

### Problem 01-08.15 [C]

**Reflections on a moderately matched line.** A 1 V step source with $R_s = 25\ \Omega$ drives a 50 Ω line terminated in $R_L = 100\ \Omega$.

(a) Find the launched wave, $\Gamma_s$ and $\Gamma_L$.
(b) Write the far-end voltage as a geometric series, and find its limit. Check it against the DC voltage divider.
(c) After how many arrivals is the far-end voltage within 1% of its final value?

### Problem 01-08.16 [A]

**Choosing a convergence test.** Decide whether each series converges, naming the test you use.

(a) $\displaystyle\sum_{k=1}^\infty\frac{1}{k^2 + 3k}$. If it converges, find its sum (hint: partial fractions make it telescope).
(b) $\displaystyle\sum_{k=1}^\infty\frac{1}{2k + 1}$
(c) $\displaystyle\sum_{k=1}^\infty\frac{\sin^2k}{k^2}$
(d) $\displaystyle\sum_{k=1}^\infty\left(\frac{k}{2k + 1}\right)^k$

### Problem 01-08.17 [B]

**Bracketing a slowly converging sum.** Let $S = \sum_{k=1}^\infty 1/k^3$.

(a) Compute the partial sum $S_{10}$.
(b) Use the integral test to bracket the remainder $S - S_{10}$, and so bracket $S$.
(c) Take the midpoint of your bracket as an estimate of $S$. Compare it with the true value, $S = 1.2020569$.
(d) How many terms would the plain partial sum need to guarantee an error below $10^{-6}$?

---

## Objective coverage

| Learning objective (chapter 01-08) | Problems |
|---|---|
| 1. Convergence of sequences and series; geometric sums | 1, 2, 5, 6, 15, 16, 17 |
| 2. Taylor and Maclaurin series; radius of convergence | 3, 4, 10, 14 |
| 3. Remainder bounds; number of terms | 7, 14 |
| 4. Engineering approximations; feedback gain error | 8, 9 |
| 5. Euler's formula, numerical error terms, distortion | 10, 11, 12, 13 |
