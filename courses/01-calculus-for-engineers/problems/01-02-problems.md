# Problems 01-02 · Limits and Continuity

Chapter: [01-02](../chapters/01-02-limits-and-continuity.md) · Worked solutions: [01-02 solutions](../solutions/01-02-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** angles in radians; $\ln$ is the natural log; answers to 4 significant figures unless stated. Use a calculator or Python freely, but show the method. Where a problem asks for an algebraic limit, find it exactly, then check it numerically.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 01-02.1 [A]

Estimate each limit from a table of values on both sides of the point. Report the values at the stated points to 5 significant figures, then state the limit.

(a) $\lim_{x\to 0}\dfrac{e^x - 1}{x}$, using $x = 0.1$ and $0.01$ (and the corresponding negative values).
(b) $\lim_{x\to 0}\dfrac{\sin 3x}{x}$, using $x = 0.1$ and $0.01$.
(c) $\lim_{x\to 1}\dfrac{x^3 - 1}{x - 1}$, using $x = 1.1$ and $1.01$.

### Problem 01-02.2 [A]

Find each limit exactly by algebra.

(a) $\lim_{x\to 3}\dfrac{x^2 - 9}{x - 3}$  (b) $\lim_{x\to 0}\dfrac{\sqrt{4 + x} - 2}{x}$  (c) $\lim_{x\to -1}\dfrac{x^2 + 3x + 2}{x + 1}$  (d) $\lim_{h\to 0}\dfrac{(1 + h)^3 - 1}{h}$

### Problem 01-02.3 [A]

Use the standard limit $\sin\theta/\theta \to 1$ and its companions.

(a) $\lim_{x\to 0}\dfrac{\sin 5x}{x}$  (b) $\lim_{x\to 0}\dfrac{\tan x}{x}$  (c) $\lim_{x\to 0}\dfrac{1 - \cos x}{x^2}$  (d) $\lim_{x\to 0}\dfrac{x}{\sin \pi x}$

### Problem 01-02.4 [A]

(a) Let $f(x) = x^2$ for $x < 1$ and $f(x) = 2x + c$ for $x \ge 1$. Find $c$ so that $f$ is continuous at 1.
(b) With $c = 0$ instead, find both one-sided limits at 1 and the size of the jump.
(c) Find $\lim_{x\to 0^-}\lvert x\rvert/x$ and $\lim_{x\to 0^+}\lvert x\rvert/x$. Does the two-sided limit exist?
(d) $g(x) = (x^2 - 9)/(x + 3)$ is undefined at $x = -3$. What value of $g(-3)$ makes $g$ continuous there?

### Problem 01-02.5 [A]

Find each limit at infinity.

(a) $\lim_{x\to\infty}\dfrac{3x^2 + 5}{2x^2 - x}$  (b) $\lim_{x\to\infty}\dfrac{5x + 1}{x^2 + 2}$  (c) $\lim_{x\to\infty}\left(\sqrt{x^2 + 4x} - x\right)$  (d) $\lim_{x\to\infty} x e^{-x}$  (e) $\lim_{x\to\infty}\dfrac{\ln x}{x}$

### Problem 01-02.6 [A]

Classify each discontinuity as removable, jump, infinite or oscillatory, and give an engineering quantity that behaves the same way, where one exists.

(a) $\dfrac{x^2 - 4}{x - 2}$ at $x = 2$  (b) $\dfrac{1}{(x - 1)^2}$ at $x = 1$  (c) the floor function $\lfloor x\rfloor$ (the largest integer $\le x$) at $x = 3$  (d) $\sin(1/x)$ at $x = 0$  (e) $\sin(x)/x$ at $x = 0$

### Problem 01-02.7 [B]

At $t = 0$ a switch connects a 12 V source to a series $R = 6\ \Omega$, $L = 30$ mH circuit with no initial current. For $t > 0$, $i(t) = (12/R)\left(1 - e^{-t/\tau}\right)$ and $v_L(t) = 12\,e^{-t/\tau}$ V, with $\tau = L/R$.

(a) Find $\tau$.
(b) Find $i(0^-)$, $i(0^+)$, $v_L(0^-)$ and $v_L(0^+)$. Which quantity is continuous at $t = 0$, and why must it be?
(c) Find $\lim_{t\to\infty} i(t)$ and $\lim_{t\to\infty} v_L(t)$.
(d) Evaluate $i$ and $v_L$ at $t = 10$ ms.

### Problem 01-02.8 [B]

(a) Evaluate $(1 + 0.06/n)^n$ for $n = 1, 4, 12, 365$ (annual, quarterly, monthly, daily compounding at 6%) to 6 significant figures, and compare with $e^{0.06}$.
(b) Prove that $\lim_{n\to\infty}(1 + r/n)^n = e^r$. Take the natural log, substitute $x = r/n$, and use $\lim_{x\to0}\ln(1 + x)/x = 1$.
(c) A bank quotes "6% compounded daily". What effective annual rate is that, and how far is it from the continuous limit, in basis points (hundredths of a percent)?

### Problem 01-02.9 [B]

A 3.3 V supply drives a diode through 10 kΩ. The diode has $I_s = 10^{-15}$ A and $V_T = 25.85$ mV.

(a) Write the KCL equation $g(V) = 0$ for the diode voltage and show that a root exists in $[0, 1]$ V.
(b) How many bisection steps give a bracket narrower than 0.1 mV?
(c) Find the operating point $V$ and the current.
(d) Compare with Example 01-02.4 (5 V, 1 kΩ, $I_s = 10^{-14}$ A). The current here is about 16 times smaller, yet the voltage is only about 13 mV lower. Explain using the 60 mV-per-decade rule of [01-01](../chapters/01-01-functions-models-and-units.md).

### Problem 01-02.10 [B]

An audio coupling capacitor forms a first-order high-pass filter with $\lvert H(f)\rvert = \dfrac{f/f_c}{\sqrt{1 + (f/f_c)^2}}$ and $f_c = 100$ Hz.

(a) Find $\lim_{f\to\infty}\lvert H\rvert$ and $\lim_{f\to 0}\lvert H\rvert$.
(b) Show that at low frequency $\lvert H\rvert \sim f/f_c$, and give the slope of the low-frequency asymptote in dB per decade.
(c) Evaluate $\lvert H\rvert$ in dB at 100 Hz, 10 Hz and 1 kHz, and compare each with the asymptotic sketch.

### Problem 01-02.11 [B]

Use the squeeze theorem.

(a) Show that $\lim_{x\to 0}x^2\sin(1/x) = 0$, although $\sin(1/x)$ itself has no limit at 0.
(b) A damped oscillation is $y(t) = e^{-t}\cos(10t)$, with $t$ in seconds. Show that $y \to 0$ as $t \to \infty$. After what time is $\lvert y\rvert$ guaranteed to stay below 0.01?
(c) Show that $\lim_{x\to\infty}\sin(x)/x = 0$.

### Problem 01-02.12 [B]

(a) Evaluate $(1 - \cos x)/x^2$ in double precision (Python) at $x = 10^{-1}, 10^{-3}, 10^{-5}, 10^{-7}$ and $10^{-8}$. Describe what happens.
(b) Just below 1, adjacent doubles are $2^{-53} \approx 1.11\times10^{-16}$ apart, so the stored value of $\cos x$ can be off by up to half of that. Estimate the worst-case *relative* error in $1 - \cos x$ caused by this rounding, as a function of $x$. Evaluate it at $x = 10^{-5}$ and $10^{-7}$.
(c) Rewrite the expression in a form that is accurate for small $x$, and evaluate it at $x = 10^{-8}$.

### Problem 01-02.13 [C]

The forward difference $D(h) = (e^h - 1)/h$ approximates the slope of $e^x$ at 0, whose exact value is 1.

(a) Evaluate $D(h)$ for $h = 0.1$, $0.01$ and $10^{-5}$. Show that the error is close to $h/2$.
(b) In double precision, computing $e^h - 1$ carries an absolute rounding error of about $\epsilon_{\text{mach}} = 2.22\times10^{-16}$, so $D(h)$ carries an error of about $\epsilon_{\text{mach}}/h$. Write the total error estimate $E(h) = h/2 + \epsilon_{\text{mach}}/h$ and find the $h$ that minimizes it, and the minimum error. (Hint: at the minimum the two terms are equal; you can confirm this with calculus in 01-04.)
(c) What rounding error does the estimate predict at $h = 10^{-12}$? Run the computation and compare.
(d) Python's `math.expm1(h)` computes $e^h - 1$ without forming $e^h$ first. Why does that remove the problem?

### Problem 01-02.14 [C]

**When the ideal limit misleads.** A 10 µF capacitor charged to 5 V is connected by a switch to an identical, uncharged 10 µF capacitor. The wires and switch have total resistance $R$.

(a) Using conservation of charge, find the final common voltage.
(b) Find the total stored energy before and after. How much energy is lost?
(c) For $R > 0$ the current is $i(t) = (5/R)e^{-t/\tau}$ with $\tau = R\,C_s$, where $C_s = C_1C_2/(C_1 + C_2)$ is the series capacitance. Find $\tau$ and the peak current for $R = 1\ \Omega$ and for $R = 0.01\ \Omega$.
(d) The energy dissipated in $R$ turns out to equal your answer to (b) for *every* $R > 0$ (you can verify this by integration after [01-05](../chapters/01-05-integrals.md)). What happens to $\tau$, the peak current and the lost energy as $R \to 0$? Why does the "ideal" circuit with $R = 0$ have no consistent answer, and what physical effects take over in a real circuit?

### Problem 01-02.15 [C]

**Asymptotic claims at practical sizes.**

(a) A direct discrete Fourier transform costs about $N^2$ operations and an FFT about $N\log_2 N$. Find the ratio of costs at $N = 1024$ and at $N = 2^{20}$, and prove that the ratio $N\log_2 N/N^2 \to 0$.
(b) The growth hierarchy says $\ln N/N^{0.1} \to 0$. Evaluate the ratio at $N = 10^{10}$.
(c) Find numerically both values of $N$ where $\ln N = N^{0.1}$. Over what range is the "slower-growing" function actually larger?
(d) What does (c) teach you about a claim that one design "scales better asymptotically"?

---

## Objective coverage

| Learning objective (chapter 01-02) | Problems |
|---|---|
| 1. Evaluate limits numerically, graphically and algebraically; standard limits | 1, 2, 3, 8, 11 |
| 2. One-sided limits; classify discontinuities; $0^-$/$0^+$ at a switch | 4, 6, 7, 14 |
| 3. Continuity, the IVT and bisection | 4, 9 |
| 4. Limits at infinity, asymptotes, dominant terms | 5, 7, 10, 11, 15 |
| 5. Limits behind the derivative and $e$; floating-point limits | 2(d), 8, 12, 13 |
