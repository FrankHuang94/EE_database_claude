# Problems 02-01 · Complex Numbers, Euler's Formula and Phasors

Chapter: [02-01](../chapters/02-01-complex-numbers-euler-and-phasors.md) · Worked solutions: [02-01 solutions](../solutions/02-01-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** angles as principal values in $(-180^\circ, 180^\circ]$; answers to 4 significant figures unless stated; cosine-reference, peak-amplitude phasors. Use a calculator or Python freely, but show the method.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 02-01.1 [A]

Convert to polar form $r\angle\theta$ (θ in degrees, principal value). Sketch each point first.

(a) $-3 + j3$  (b) $-2 - j5$  (c) $j7$  (d) $-4$

### Problem 02-01.2 [A]

Convert to rectangular form $x + jy$.

(a) $10\angle 120^\circ$  (b) $2e^{-j\pi/3}$  (c) $5\angle -90^\circ$  (d) $0.5\angle 210^\circ$

### Problem 02-01.3 [A]

Simplify to the form $x + jy$ without a calculator.

(a) $j^7$  (b) $j^{-3}$  (c) $1/j$  (d) $(1 + j)(1 - j)$  (e) $j^{2026}$

### Problem 02-01.4 [A]

(a)–(c) Write the phasor (peak amplitude, cosine reference) of each sinusoid:

(a) $12\cos(377t - 45^\circ)$ V  (b) $-3\sin(2\pi\cdot 50\,t)$ A  (c) $4\sin(\omega t + 60^\circ)$ V

(d)–(e) Write the time function for each phasor:

(d) $\mathbf{V} = 8\angle -150^\circ$ V at $\omega = 1000$ rad/s  (e) $\mathbf{I} = -j2$ A at angular frequency $\omega$

### Problem 02-01.5 [B]

Let $z_1 = 2 - j3$ and $z_2 = -1 + j4$. Compute, in rectangular form unless stated:

(a) $z_1z_2^{\ast}$  (b) $z_1/z_2$  (c) $\lvert z_1 + z_2\rvert$  (d) $z_1^2$  (e) $\operatorname{Re}\lbrace z_1z_2\rbrace$  (f) $z_1/z_2$ in polar form

### Problem 02-01.6 [B]

(a) Using only the rectangular form $z_1 = a + jb$, $z_2 = c + jd$, prove that $\lvert z_1z_2\rvert = \lvert z_1\rvert\,\lvert z_2\rvert$.
(b) Use (a) to prove $\lvert z_1/z_2\rvert = \lvert z_1\rvert/\lvert z_2\rvert$ for $z_2 \ne 0$.
(c) Prove $(z_1z_2)^{\ast} = z_1^{\ast}z_2^{\ast}$.

### Problem 02-01.7 [B]

Use Euler's formula (not memorized identities) to derive:

(a) $\cos 3\theta = 4\cos^3\theta - 3\cos\theta$  (Hint: expand $(\cos\theta + j\sin\theta)^3$ and take the real part.)
(b) $\sin\alpha\sin\beta = \tfrac{1}{2}\big[\cos(\alpha - \beta) - \cos(\alpha + \beta)\big]$

Identity (b) is the reason mixing two frequencies in a radio produces sum and difference frequencies.

### Problem 02-01.8 [B]

Find all solutions of $z^3 = -8j$. Give each in polar and rectangular form, sketch them, and verify one solution by cubing it.

### Problem 02-01.9 [B]

Express as a single sinusoid $A\cos(\omega t + \phi)$:

$$
v(t) = 4\cos(\omega t + 60^\circ) - 3\sin(\omega t) + 2\cos(\omega t - 135^\circ)\ \text{V}.
$$

### Problem 02-01.10 [B]

Phase is time delay at a given frequency.

(a) A 100 MHz clock is delayed by 1.5 ns. What phase shift (in degrees) does that represent?
(b) A 2.4 GHz signal travels along 5.0 cm of circuit-board trace, on which signals propagate at $1.5\times10^{8}$ m/s. Find the delay (ps) and the phase shift (degrees).
(c) Find the wavelength on the trace (mm) and confirm your phase in (b) by comparing the trace length with the wavelength.

### Problem 02-01.11 [B]

Find the sinusoidal steady-state solution of

$$
2\frac{dy}{dt} + 8y = 10\cos(4t + 30^\circ).
$$

Then verify your answer by substituting it back into the differential equation.

### Problem 02-01.12 [B]

A series RL circuit obeys $L\dfrac{di}{dt} + Ri = V_m\cos\omega t$, with $R = 50\ \Omega$, $L = 10$ mH, $V_m = 20$ V and $f = 1$ kHz.

(a) Find the impedance $Z = R + j\omega L$ in rectangular and polar form.
(b) Find $i(t)$ in steady state.
(c) Find the amplitudes of the resistor and inductor voltages. Explain why they add to more than 20 V, and show how they combine to give exactly 20 V.

### Problem 02-01.13 [B]

A series RLC circuit has $R = 100\ \Omega$, $L = 1$ mH and $C = 10$ nF.

(a) Find the resonant frequency $\omega_0 = 1/\sqrt{LC}$ (rad/s) and $f_0$ (kHz).
(b) Find the impedance $Z = R + j\big(\omega L - \tfrac{1}{\omega C}\big)$ at $f = 25$ kHz, in rectangular and polar form. Is the circuit inductive or capacitive there?
(c) Repeat (b) at $f = 100$ kHz.
(d) State $Z$ at $f_0$.

### Problem 02-01.14 [C]

A second-order system (a mass–spring–damper, or an RLC circuit; see [02-03](../chapters/02-03-second-order-linear-odes.md)) obeys

$$
\frac{d^2y}{dt^2} + 2\zeta\omega_n\frac{dy}{dt} + \omega_n^2\,y = \omega_n^2\cos\omega t .
$$

(a) Derive the frequency response $H(j\omega) = \mathbf{Y}/\mathbf{X}$ and write $\lvert H\rvert$ and $\angle H$ in terms of the ratio $u = \omega/\omega_n$.
(b) For $\zeta = 0.1$ and $\omega_n = 1000$ rad/s, evaluate $H$ (polar) at $\omega = 500$, $1000$ and $2000$ rad/s.
(c) By minimizing the denominator of $\lvert H\rvert^2$, show that the peak response occurs at $\omega_{pk} = \omega_n\sqrt{1 - 2\zeta^2}$ (for $\zeta < 1/\sqrt{2}$) with peak value $1/\big(2\zeta\sqrt{1 - \zeta^2}\big)$. Evaluate both for $\zeta = 0.1$.
(d) Interpret: why might a lightly damped power-delivery network on a chip be dangerous?

### Problem 02-01.15 [C] (hardware design)

A complex multiplier computes $(a + jb)(c + jd)$.

(a) The direct form uses 4 real multiplications and 2 additions. Show that with $k_1 = c(a + b)$, $k_2 = a(d - c)$ and $k_3 = b(c + d)$, the product is $(k_1 - k_3) + j(k_1 + k_2)$. Count the multiplications and additions/subtractions.
(b) In an FFT, $c + jd$ is a fixed twiddle factor. Which operations can then be precomputed, and what is the per-multiply cost?
(c) A radix-2 FFT of size $N$ has $(N/2)\log_2 N$ butterflies, each with one complex multiplication (count all of them, including trivial ones). For $N = 4096$, how many complex multiplications is that, and how many real multiplications are needed with the 4-multiplier and 3-multiplier forms?
(d) Name two costs of the 3-multiplier form that a hardware architect must weigh against the multiplier savings.

### Problem 02-01.16 [C]

(a) Use Euler's formula to show that $\cos\omega_1t + \cos\omega_2t = 2\cos\!\Big(\dfrac{\omega_1 - \omega_2}{2}t\Big)\cos\!\Big(\dfrac{\omega_1 + \omega_2}{2}t\Big)$.
(b) Two tones at 440 Hz and 444 Hz are played together. Find the frequency of the fast oscillation, and the frequency and period at which the loudness (the envelope) peaks.
(c) Explain, in terms of rotating arrows, why the sum cannot be represented by a single phasor.

### Problem 02-01.17 [C]

A voltage $v(t) = V_m\cos(\omega t + \theta_v)$ drives a current $i(t) = I_m\cos(\omega t + \theta_i)$ through a load.

(a) Using a product-to-sum identity, show that the instantaneous power is
$p(t) = \tfrac{1}{2}V_mI_m\cos(\theta_v - \theta_i) + \tfrac{1}{2}V_mI_m\cos(2\omega t + \theta_v + \theta_i)$.
(b) Show that the average power is $P = \tfrac{1}{2}\operatorname{Re}\lbrace\mathbf{V}\mathbf{I}^{\ast}\rbrace$.
(c) For $\mathbf{V} = 10\angle 30^\circ$ V and $\mathbf{I} = 2\angle -15^\circ$ A, compute $P$. Then compute the incorrect quantity $\tfrac{1}{2}\operatorname{Re}\lbrace\mathbf{V}\mathbf{I}\rbrace$ and explain why it is wrong.

### Problem 02-01.18 [B]

Damped sinusoids as complex exponentials (chapter §3.7). Let $s = -2 + j10$ (in 1/s).

(a) Write $e^{st}$ in the form (magnitude) × (rotation), and show that $y(t) = e^{-2t}\cos 10t$ equals $\operatorname{Re}\lbrace e^{st}\rbrace$.
(b) How long does the envelope $e^{-2t}$ take to halve? What is the period of the oscillation? How many oscillation periods fit into one halving time?
(c) Evaluate $y(0.5\text{ s})$.
(d) Show that $s = -2 \pm j10$ are the roots of $s^2 + 4s + 104 = 0$. (In [02-03](../chapters/02-03-second-order-linear-odes.md) you will see that this is the characteristic equation of a ringing second-order circuit.)

---

## Objective coverage

| Learning objective (chapter 02-01) | Problems |
|---|---|
| 1. Convert forms; complex arithmetic, powers and roots | 1, 2, 3, 5, 6, 8 |
| 2. Derive and use Euler's formula; trig identities; complex exponentials | 7, 16, 17(a), 18 |
| 3. Phasors; adding same-frequency sinusoids | 4, 9, 10, 16(c) |
| 4. Calculus as $j\omega$; sinusoidal steady state of ODEs; impedance | 11, 12, 13, 14 |
| 5. Geometric interpretation; complex arithmetic in hardware | 10, 15, 17(c) |
