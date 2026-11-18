# Course 02 · Final Exam — Solutions

Exam: [README.md](README.md). All numbers are recomputed by [verify_02_exam.py](../verify/verify_02_exam.py), and the circuit results of Questions 2, 5, 9 and 13 are confirmed in ngspice by [exam_circuits.cir](exam_circuits.cir). Each solution names the chapter to revisit if you lost points.

**1.** *(02-01)* (a) $|z_1| = \sqrt{3^2 + 4^2} = 5$, and $z_1$ is in the first quadrant, so its angle is $\arctan(4/3) = 53.13°$: $z_1 = 5\angle53.13°$. Multiply in rectangular form: $z_1z_2 = (3 + j4)(1 - j) = 3 - j3 + j4 - j^2 4 = 7 + j1$. Divide by multiplying top and bottom by the conjugate $z_2^* = 1 + j$:

$$
\frac{z_1}{z_2} = \frac{(3 + j4)(1 + j)}{(1 - j)(1 + j)} = \frac{3 + j3 + j4 - 4}{2} = -0.5 + j3.5 .
$$

Check with magnitudes: $|z_1/z_2| = 5/\sqrt2 = 3.536$, and $\sqrt{0.5^2 + 3.5^2} = \sqrt{12.5} = 3.536$ ✓.

(b) Write $8j = 8e^{j90°}$. The cube roots have magnitude $8^{1/3} = 2$ and angles $(90° + 360°k)/3 = 30°, 150°, 270°$:

- $2\angle30° = 1.732 + j1$;
- $2\angle150° = -1.732 + j1$;
- $2\angle270° = -j2$.

Check: the three roots of $z^3 - 8j = 0$ must sum to zero (there is no $z^2$ term), and $1.732 - 1.732 + 0 = 0$, $1 + 1 - 2 = 0$ ✓.

(c) Convert to cosines first: $5\sin\omega t = 5\cos(\omega t - 90°)$. The phasors are $10\angle30° = 8.660 + j5$ and $5\angle-90° = -j5$. Their sum is $8.660 + j0$, so $v(t) = 8.660\cos(\omega t)$: amplitude **8.660**, phase **0°**. The sine term exactly cancels the quadrature part of the first term.

**2.** *(02-01; resonance from 02-04)* (a) $Z_R = 100\ \Omega$, $Z_L = j\omega L = j100\ \Omega$ and $Z_C = 1/(j\omega C) = -j/(1000\times20\times10^{-6}) = -j50\ \Omega$. In series,

$$
Z = 100 + j50\ \Omega = 111.8\angle26.57°\ \Omega .
$$

(b) $\mathbf{I} = \mathbf{V}_s/Z = 10\angle0°/111.8\angle26.57° = 0.08944\angle-26.57°$ A, so $i(t) = 89.44\cos(1000t - 26.57°)$ mA. The net reactance is positive (inductive), so the current **lags** the source by 26.57°.

(c) $\mathbf{V}_C = Z_C\mathbf{I} = 50\angle-90° \times 0.08944\angle-26.57° = 4.472\angle-116.57°$ V, so $v_C(t) = 4.472\cos(1000t - 116.57°)$ V.

(d) From the source: $P = \tfrac12V_mI_m\cos\theta = \tfrac12(10)(0.08944)\cos26.57° = 0.4000$ W. Check from the resistor, the only element that dissipates: $P = \tfrac12I_m^2R = \tfrac12(0.08944)^2(100) = 0.4000$ W ✓. The factor ½ is there because phasors carry peak values.

(e) The current is in phase when the reactances cancel, $\omega L = 1/(\omega C)$, at $\omega_0 = 1/\sqrt{LC} = 1/\sqrt{0.1\times20\times10^{-6}} = 707.1$ rad/s. Then $Z = R$ and the current amplitude is $10/100 = 0.1$ A $=$ **100 mA**.

**3.** *(02-02)* (a) KVL with $i = C\,dv/dt$ gives $RC\,v' + v = 5$, with $\tau = RC = 2000\times10^{-5} = 20$ ms. The solution is the final value plus a decaying difference:

$$
v(t) = 5 + (1 - 5)e^{-t/\tau} = 5 - 4e^{-t/20\text{ ms}}\ \text{V}.
$$

(b) $v(10\text{ ms}) = 5 - 4e^{-0.5} = 2.574$ V. For $v = 4$ V: $4e^{-t/\tau} = 1$, so $t = \tau\ln4 = 27.73$ ms.

(c) Forward Euler on $v' = (5 - v)/\tau$ multiplies the deviation from the final value, $v - 5$, by $1 - h/\tau$ each step. Stability needs $|1 - h/\tau| < 1$, so $h < 2\tau = $ **40 ms**. The factor is negative for $h > \tau$, so the deviation alternates in sign, and the numerical solution overshoots the final value back and forth, unless $h \le \tau = $ **20 ms**. Accuracy needs a much smaller step still, say $\tau/20$.

**4.** *(02-02)* (a) Divide by $t$: $y' + (3/t)y = 1$. The integrating factor is $\mu = e^{\int 3/t\,dt} = t^3$, and $t^3y' + 3t^2y = (t^3y)'$, so $(t^3y)' = t^3$ and $t^3y = t^4/4 + K$. From $y(1) = 0$, $K = -1/4$:

$$
y(t) = \frac{t}{4} - \frac{1}{4t^3}, \qquad y(2) = \frac12 - \frac{1}{32} = 0.46875 .
$$

Check: $y' = 1/4 + 3/(4t^4)$, so $ty' + 3y = t/4 + 3/(4t^3) + 3t/4 - 3/(4t^3) = t$ ✓.

(b) The equation is $\tau v' + v = kt$. Try $v_p = at + b$: $\tau a + at + b = kt$, so $a = k$ and $b = -k\tau$. Adding the natural response and using $v(0) = 0$:

$$
v_{out}(t) = k(t - \tau) + k\tau e^{-t/\tau}.
$$

At 1 ms: $2(1 - 0.5) + 2(0.5)e^{-2} = 1 + 0.1353 = 1.135$ V. Once the exponential dies, $v_{in} - v_{out} = k\tau = $ **1 V**: the output is the input delayed by exactly $\tau = $ **0.5 ms**. This is why a slow RC node delays a ramping signal by one time constant.

(c) $f(y) = 1 - y^2 = 0$ at $y = \pm1$. Since $f'(y) = -2y$, $f'(1) = -2 < 0$ (stable) and $f'(-1) = 2 > 0$ (unstable). On the phase line, $y' > 0$ between −1 and 1, and $y' < 0$ outside, so solutions flow toward +1 and away from −1 ✓. Near +1 a deviation decays as $e^{-2t}$: local time constant $1/|f'(1)| = $ **0.5**. Separating, $\int dy/(1 - y^2) = \int dt$. With partial fractions, $\tfrac12\ln\frac{1 + y}{1 - y} = t + K$, and $y(0) = 0$ gives $K = 0$, so $y = \tanh t$ and $y(1) = 0.7616$. It approaches the stable equilibrium +1, as the phase line predicts.

**5.** *(02-03)* (a) KVL around the loop with $i = C\,dv_C/dt$: $v_s = Ri + L\,di/dt + v_C$, so

$$
LC\,v_C'' + RC\,v_C' + v_C = v_s \quad\Longrightarrow\quad v_C'' + \frac{R}{L}v_C' + \frac{1}{LC}v_C = \frac{v_s}{LC}.
$$

Matching $v'' + 2\alpha v' + \omega_0^2v$: $\omega_0 = 1/\sqrt{LC} = 1/\sqrt{10^{-12}} = 1\times10^6$ rad/s, $\alpha = R/(2L) = 0.5/(2\times10^{-6}) = 2.5\times10^5$ s⁻¹, $\zeta = \alpha/\omega_0 = 0.25$ and $Q = 1/(2\zeta) = 2$. Check: $Q = (1/R)\sqrt{L/C} = 2\times1 = 2$ ✓.

(b) $s = -\alpha \pm j\omega_d$, with $\omega_d = \omega_0\sqrt{1 - \zeta^2} = 10^6\sqrt{0.9375} = 9.682\times10^5$ rad/s.

(c) From rest, the step response is

$$
v_C(t) = 1 - e^{-\alpha t}\left[\cos\omega_dt + \frac{\alpha}{\omega_d}\sin\omega_dt\right]\ \text{V}, \qquad \frac{\alpha}{\omega_d} = 0.2582 .
$$

The first peak is where $v_C' = 0$ first, at $t_p = \pi/\omega_d = 3.245$ µs. There the bracket equals $-1$, so $v_C = 1 + e^{-\alpha\pi/\omega_d}$ and the overshoot is $e^{-\pi\zeta/\sqrt{1 - \zeta^2}} = e^{-0.8112} = 44.43\%$, a peak of **1.444 V**. The envelope rule gives the 2% settling time as $4/\alpha = 16$ µs. That is about 2.5 ring periods, consistent with $Q = 2$.

(d) Critical damping needs ζ = 1, $\alpha = \omega_0$: $R = 2\sqrt{L/C} = $ **2 Ω**.

**6.** *(02-04)* (a) The homogeneous roots are $\pm j2$, and the input is at that same frequency, so the ordinary guess fails: multiply it by $t$. Write $y_p = t\,g(t)$ with $g = A\cos2t + B\sin2t$, which satisfies $g'' = -4g$. Then $y_p'' = 2g' + tg''$, so $y_p'' + 4y_p = 2g'$. Setting $2g' = 3\cos2t$ needs $g' = -2A\sin2t + 2B\cos2t = 1.5\cos2t$, so $A = 0$, $B = 0.75$ and $y_p = 0.75\,t\sin2t$. The general solution adds $c_1\cos2t + c_2\sin2t$; $y(0) = 0$ gives $c_1 = 0$ and $y'(0) = 2c_2 = 0$ gives $c_2 = 0$. So

$$
y(t) = \tfrac34\,t\sin2t,
$$

an oscillation whose envelope grows linearly, by 0.75 per unit time, without bound: undamped resonance. $y(\pi/4) = \tfrac34\cdot\tfrac{\pi}{4}\cdot1 = 3\pi/16 = 0.5890$.

(b) Replace the input by $10e^{j2t}$ and try $Ye^{j2t}$: $p(j2)\,Y = 10$ with $p(s) = s^2 + 2s + 5$, so $p(j2) = -4 + j4 + 5 = 1 + j4$. Then $Y = 10/(1 + j4)$, with magnitude $10/\sqrt{17} = 2.425$ and angle $-\arctan4 = -75.96°$:

$$
y_{ss}(t) = 2.425\cos(2t - 75.96°).
$$

The amplitude is $10/|p(j\omega)|$, with $|p(j\omega)|^2 = (5 - \omega^2)^2 + 4\omega^2$. Setting the derivative with respect to $\omega^2$ to zero, $2(\omega^2 - 5) + 4 = 0$, gives $\omega^2 = 3$: the peak is at $\omega = \sqrt3 = 1.732$ rad/s, where $|p|^2 = 4 + 12 = 16$ and the amplitude is $10/4 = $ **2.5**. Check with the peak formula: here $\omega_0 = \sqrt5$ and $\zeta = 1/\sqrt5$, so $\omega_0\sqrt{1 - 2\zeta^2} = \sqrt5\sqrt{0.6} = \sqrt3$ ✓.

(c) $\omega_0 = 2\pi\times10^7 = 6.283\times10^7$ rad/s, so $C = 1/(\omega_0^2L) = 253.3$ pF. For a series RLC, $Q = \omega_0L/R$, so $R = \omega_0L/Q = 62.83/50 = 1.257\ \Omega$. The half-power bandwidth is $f_0/Q = $ **200 kHz**. The free ring decays as $e^{-\alpha t}$ with $1/\alpha = 2L/R = 2Q/\omega_0 = 1.592$ µs, which is $1.592\text{ µs}\times10\text{ MHz} = 15.92$ cycles, or $Q/\pi$ ✓. The narrow bandwidth and the slow ring are the same fact.

**7.** *(02-05)* (a) Transform with the initial conditions: $\mathcal{L}\{y''\} = s^2Y - s$ and $\mathcal{L}\{3y'\} = 3sY - 3$. So $(s^2 + 3s + 2)Y - s - 3 = 4/s$, and

$$
Y(s) = \frac{s^2 + 3s + 4}{s(s + 1)(s + 2)} = \frac{2}{s} - \frac{2}{s + 1} + \frac{1}{s + 2},
$$

with residues found by cover-up: at $s = 0$, $4/2 = 2$; at $s = -1$, $(1 - 3 + 4)/((-1)(1)) = -2$; at $s = -2$, $(4 - 6 + 4)/((-2)(-1)) = 1$. So $y(t) = 2 - 2e^{-t} + e^{-2t}$ for $t \ge 0$. Check: $y(0) = 1$ ✓ and $y'(0) = 2 - 2 = 0$ ✓. Then $y(1) = 2 - 0.7358 + 0.1353 = 1.400$.

(b) IVT: $y(0^+) = \lim_{s\to\infty}sY = \lim (s^2 + 3s + 4)/((s + 1)(s + 2)) = 1$ ✓. FVT: the poles of $sY$ are at −1 and −2, in the left half-plane, so it applies: $y(\infty) = \lim_{s\to0}sY = 4/2 = 2$ ✓. $F(s) = s/(s^2 + 4)$ has poles at $\pm j2$, on the imaginary axis. Its inverse, $\cos2t$, oscillates forever and has no final value, but blind use of the theorem returns $\lim_{s\to0} s^2/(s^2 + 4) = 0$, a wrong answer.

(c) $s^2 + 2s + 10 = (s + 1)^2 + 9 = 0$ gives poles $-1 \pm j3$. Here $\omega_0 = \sqrt{10} = 3.162$ rad/s and $2\zeta\omega_0 = 2$, so $\zeta = 1/\sqrt{10} = 0.3162$. The impulse response is

$$
h(t) = \mathcal{L}^{-1}\left\{\frac{10}{3}\cdot\frac{3}{(s + 1)^2 + 9}\right\} = \frac{10}{3}e^{-t}\sin3t\quad(t \ge 0),
$$

and the DC gain is $H(0) = 10/10 = $ **1**.

(d) The pulse is $u(t) - u(t - 2)$. The step response of $1/(s + 1)$ is $1 - e^{-t}$, and the time-shift property delays the second copy by 2 s:

$$
y(t) = (1 - e^{-t})u(t) - (1 - e^{-(t - 2)})u(t - 2).
$$

At $t = 3$ s: $(1 - e^{-3}) - (1 - e^{-1}) = e^{-1} - e^{-3} = 0.3181$ V. After the pulse ends the output simply decays from its $t = 2$ value, $1 - e^{-2} = 0.8647$, and indeed $0.8647e^{-1} = 0.3181$ ✓.

**8.** *(02-06)* (a) $\mathbf{a}\cdot\mathbf{b} = 2 + 0 + 2 + 0 = 4$. $\lVert\mathbf{a}\rVert = \sqrt{1 + 4 + 4} = 3$ and $\lVert\mathbf{b}\rVert = \sqrt{4 + 0 + 1 + 4} = 3$. So $\cos\theta = 4/9$ and $\theta = 63.61°$.

(b) $\mathbf{p} = \dfrac{\mathbf{a}\cdot\mathbf{b}}{\mathbf{a}\cdot\mathbf{a}}\mathbf{a} = \tfrac49(1, 2, 2, 0) = (0.4444, 0.8889, 0.8889, 0)$. Then $\mathbf{b} - \mathbf{p} = (14/9, -8/9, 1/9, 2)$, and $(\mathbf{b} - \mathbf{p})\cdot\mathbf{a} = (14 - 16 + 2)/9 + 0 = 0$ ✓. By Pythagoras, $\lVert\mathbf{b} - \mathbf{p}\rVert^2 = \lVert\mathbf{b}\rVert^2 - \lVert\mathbf{p}\rVert^2 = 9 - 16/9 = 65/9$, so $\lVert\mathbf{b} - \mathbf{p}\rVert = 2.687$.

(c)

$$
\mathbf{A}\mathbf{B} = \begin{bmatrix}1 + 6 & 0 + 2\\ 0 + 3 & 0 + 1\end{bmatrix} = \begin{bmatrix}7 & 2\\ 3 & 1\end{bmatrix}, \qquad
\mathbf{B}\mathbf{A} = \begin{bmatrix}1 & 2\\ 3 & 6 + 1\end{bmatrix} = \begin{bmatrix}1 & 2\\ 3 & 7\end{bmatrix},
$$

so $\mathbf{A}\mathbf{B} \ne \mathbf{B}\mathbf{A}$. And $\mathbf{B}^{\mathsf{T}}\mathbf{A}^{\mathsf{T}} = \begin{bmatrix}1 & 3\\ 0 & 1\end{bmatrix}\begin{bmatrix}1 & 0\\ 2 & 1\end{bmatrix} = \begin{bmatrix}7 & 3\\ 2 & 1\end{bmatrix} = (\mathbf{A}\mathbf{B})^{\mathsf{T}}$ ✓.

**9.** *(02-06, 02-07)* (a) Each resistor of conductance $g$ between nodes $j$ and $k$ adds $g$ to entries $(j,j)$ and $(k,k)$ and $-g$ to $(j,k)$ and $(k,j)$; a resistor to ground adds only to its diagonal entry. In mS:

$$
\begin{bmatrix}1.5 & -0.5 & 0\\ -0.5 & 2 & -1\\ 0 & -1 & 2\end{bmatrix}
\begin{bmatrix}v_1\\ v_2\\ v_3\end{bmatrix} = \begin{bmatrix}1\\ 0\\ 0\end{bmatrix}\text{ mA}.
$$

It is symmetric because each stamp is symmetric. Each diagonal entry is the total conductance at that node: the sum of the magnitudes of the off-diagonal entries in its row plus the conductance to ground. Every node here has a resistor to ground, so all three rows are strictly dominant: $1.5 > 0.5$, $2 > 0.5 + 1$ and $2 > 1$.

(b) Eliminate: $\ell_{21} = -0.5/1.5 = -1/3$, which changes row 2 to $(0,\ 2 - 1/6,\ -1) = (0,\ 11/6,\ -1)$. Then $\ell_{32} = -1/(11/6) = -6/11$, which changes row 3 to $(0,\ 0,\ 2 - 6/11) = (0, 0, 16/11)$:

$$
\mathbf{L} = \begin{bmatrix}1 & 0 & 0\\ -1/3 & 1 & 0\\ 0 & -6/11 & 1\end{bmatrix},\qquad
\mathbf{U} = \begin{bmatrix}1.5 & -0.5 & 0\\ 0 & 11/6 & -1\\ 0 & 0 & 16/11\end{bmatrix}.
$$

$\det\mathbf{G} = 1.5\times\tfrac{11}{6}\times\tfrac{16}{11} = 4$ mS³.

(c) Forward: $\mathbf{L}\mathbf{y} = \mathbf{i}$ gives $y_1 = 1$, $y_2 = 1/3$, $y_3 = (6/11)(1/3) = 2/11$. Back: $v_3 = (2/11)/(16/11) = 0.125$ V; $v_2 = (1/3 + 0.125)/(11/6) = 0.25$ V; $v_1 = (1 + 0.5\times0.25)/1.5 = 0.75$ V. (mA/mS = V.) Power balance: the source delivers $1\text{ mA}\times0.75\text{ V} = 0.75$ mW. The resistors absorb $0.75^2/1 + 0.5^2/2 + 0.25^2/2 + 0.125^2/1 + 0.125^2/1 = 0.5625 + 0.125 + 0.03125 + 0.015625 + 0.015625 = 0.75$ mW ✓ (V²/kΩ = mW).

(d) Now $\mathbf{i} = (0, 0, 1)$. Forward: $\mathbf{y} = (0, 0, 1)$. Back: $v_3 = 11/16 = 0.6875$ V, $v_2 = 0.6875\times6/11 = 0.375$ V, $v_1 = 0.5\times0.375/1.5 = 0.125$ V. The new $v_1$ equals the old $v_3$, 0.125 V. Both are the transfer resistance $r_{13} = r_{31} = 125\ \Omega$, entries of $\mathbf{R} = \mathbf{G}^{-1}$, which is symmetric because $\mathbf{G}$ is. This is reciprocity. The driving-point resistances check by series–parallel reduction: node 1 sees $1\text{ k}\parallel(2\text{ k} + 2\text{ k}\parallel2\text{ k}) = 750\ \Omega$ ✓, and node 3 sees $1\text{ k}\parallel(1\text{ k} + 2\text{ k}\parallel3\text{ k}) = 687.5\ \Omega$ ✓.

(e) Dense LU costs about $\tfrac23n^3 = \tfrac23(3000)^3 = 1.8\times10^{10}$ flops. Each extra right-hand side costs one forward and one back substitution, about $2n^2 = 1.8\times10^7$ flops, a thousandth as much. That is why simulators factor once and reuse the factors. (Real circuit matrices are sparse, which cuts both counts enormously.)

**10.** *(02-07)* (a) Eliminate: $R_2 - 2R_1 = (0, 0, 1)$ and $R_3 - 3R_1 = (0, 0, 1)$, then $R_3 - R_2 = (0, 0, 0)$. Only two pivots (columns 1 and 3), so the rank is **2** and $\det\mathbf{A} = 0$. Column 2 is free: set $x_2 = 1$; then $x_3 = 0$ and $x_1 = -2$. The null space is the line through $(-2, 1, 0)$ (column 2 is twice column 1). Rank–nullity: $2 + 1 = 3$ columns ✓.

(b) The same steps on $\mathbf{b} = (1, 3, 4)$ give $(1, 1, 0)$ on the right: the zero row reads $0 = 0$, so the system is consistent. Back substitution with $x_2 = 0$ gives $x_3 = 1$ and $x_1 = 1 - x_3 = 0$, so the complete solution is

$$
\mathbf{x} = (0, 0, 1) + c\,(-2, 1, 0), \quad c \in \mathbb{R}.
$$

For $\mathbf{b} = (1, 3, 5)$ the zero row reads $0 = 1$: no solution. In column-space terms, every column has third entry equal to the sum of the first two, so every $\mathbf{A}\mathbf{x}$ does too. $(1, 3, 4)$ has that property; $(1, 3, 5)$ does not, so it lies outside the column space.

(c) The design matrix has a column of ones and the column $\mathbf{x} = (0, 1, 2, 3)$. The normal equations are

$$
\begin{bmatrix}4 & 6\\ 6 & 14\end{bmatrix}\begin{bmatrix}c\\ m\end{bmatrix} = \begin{bmatrix}12\\ 23\end{bmatrix},
$$

using $\sum x = 6$, $\sum x^2 = 14$, $\sum y = 12$ and $\sum xy = 0 + 3 + 8 + 12 = 23$. The determinant is 20, so $c = (12\times14 - 6\times23)/20 = 1.5$ and $m = (4\times23 - 6\times12)/20 = 1.0$. The fit is $y = 1.5 + x$. The residuals are $y - (1.5 + x) = (-0.5, 0.5, 0.5, -0.5)$, with sum of squares **1.0**. Against the ones column they sum to 0; against $\mathbf{x}$, $0 + 0.5 + 1 - 1.5 = 0$ ✓. The residual is orthogonal to the column space, which is what makes the fit a projection.

**11.** *(02-08)* (a) Column $j$ holds the probabilities of leaving state $j$:

$$
\mathbf{M} = \begin{bmatrix}0.9 & 0.2\\ 0.1 & 0.8\end{bmatrix}.
$$

$\det(\mathbf{M} - \lambda\mathbf{I}) = \lambda^2 - 1.7\lambda + 0.7 = (\lambda - 1)(\lambda - 0.7)$, so $\lambda = 1$ and $\lambda = 0.7$. Checks: the trace is $1.7 = 1 + 0.7$ ✓ and the determinant is $0.72 - 0.02 = 0.70 = 1\times0.7$ ✓. For $\lambda = 1$: $-0.1x_1 + 0.2x_2 = 0$, so the eigenvector is $(2, 1)$. For $\lambda = 0.7$: $0.2x_1 + 0.2x_2 = 0$, so it is $(1, -1)$.

(b) Scale $(2, 1)$ to sum to 1: the steady state is $(2/3, 1/3)$. The radio is awake **0.6667** of the time. The average power is $\tfrac23(10) + \tfrac13(0.1) = 6.700$ mW.

(c) Expand $\mathbf{x}_0 = (0, 1) = (2/3, 1/3) + c(1, -1)$: $c = -2/3$. Each step multiplies the first component by 1 and the second by 0.7, so

$$
\mathbf{x}_k = \begin{bmatrix}2/3\\ 1/3\end{bmatrix} - \frac23(0.7)^k\begin{bmatrix}1\\ -1\end{bmatrix}, \qquad p_k = \frac23\left[1 - (0.7)^k\right].
$$

$p_5 = \tfrac23(1 - 0.16807) = 0.5546$. Within 0.01 needs $\tfrac23(0.7)^k \le 0.01$, so $(0.7)^k \le 0.015$ and $k \ge \ln0.015/\ln0.7 = 11.77$: **12 slots**. (Check: $k = 11$ leaves 0.0132; $k = 12$ leaves 0.0092.)

(d) Now $\mathbf{M} = \begin{bmatrix}0.7 & 0.2\\ 0.3 & 0.8\end{bmatrix}$. Steady state: $-0.3p + 0.2q = 0$ with $p + q = 1$ gives $p = 0.4$. The average power is $0.4(10) + 0.6(0.1) = 4.060$ mW, a 39% cut. The trace is 1.5, so the second eigenvalue is $1.5 - 1 = 0.5$. (For any two-state chain it is 1 minus the two exit probabilities: $1 - 0.3 - 0.2$.) It sets how fast the chain forgets where it started: deviations from the steady state now shrink by 0.5 per slot instead of 0.7.

**12.** *(02-08)* (a) $\det(\mathbf{K} - \lambda\mathbf{I}) = (2 - \lambda)^2 - 1 = 0$, so $\lambda = 1$ and $\lambda = 3$, with orthonormal eigenvectors $\mathbf{q}_1 = (1, 1)/\sqrt2$ and $\mathbf{q}_2 = (1, -1)/\sqrt2$:

$$
\mathbf{K} = \mathbf{Q}\boldsymbol{\Lambda}\mathbf{Q}^{\mathsf{T}} = \frac12\begin{bmatrix}1 & 1\\ 1 & -1\end{bmatrix}\begin{bmatrix}1 & 0\\ 0 & 3\end{bmatrix}\begin{bmatrix}1 & 1\\ 1 & -1\end{bmatrix}.
$$

Positive definite three ways: both eigenvalues are positive; the pivots, 2 and $2 - (-1)(-1)/2 = 1.5$, are positive; and the energy is $\mathbf{x}^{\mathsf{T}}\mathbf{K}\mathbf{x} = 2x_1^2 - 2x_1x_2 + 2x_2^2 = x_1^2 + x_2^2 + (x_1 - x_2)^2 > 0$ for every $\mathbf{x} \ne \mathbf{0}$.

(b) $\mathbf{H}^{\mathsf{T}}\mathbf{H} = \begin{bmatrix}25 & 20\\ 20 & 25\end{bmatrix}$, with eigenvalues $45$ and $5$ and eigenvectors $\mathbf{v}_1 = (1, 1)/\sqrt2$ and $\mathbf{v}_2 = (1, -1)/\sqrt2$. So $\sigma_1 = \sqrt{45} = 6.708$ and $\sigma_2 = \sqrt5 = 2.236$. The left singular vectors are $\mathbf{u}_i = \mathbf{H}\mathbf{v}_i/\sigma_i$: $\mathbf{u}_1 = (3, 9)/(\sqrt2\sqrt{45}) = (1, 3)/\sqrt{10}$ and $\mathbf{u}_2 = (3, -1)/(\sqrt2\sqrt5) = (3, -1)/\sqrt{10}$, which are orthogonal ✓. Checks: $\sigma_1\sigma_2 = 15 = |\det\mathbf{H}|$ ✓, and $\sigma_1^2 + \sigma_2^2 = 50 = 9 + 16 + 25$, the sum of squared entries ✓. The condition number is $\sigma_1/\sigma_2 = $ **3**.

(c) Sending along $\mathbf{v}_i$ and receiving along $\mathbf{u}_i$ gives two independent channels with power gains $\sigma_1^2 = 45$ (16.53 dB) and $\sigma_2^2 = 5$ (6.990 dB). The best rank-1 approximation, $\sigma_1\mathbf{u}_1\mathbf{v}_1^{\mathsf{T}}$, has 2-norm error $\sigma_2 = 2.236$. Dropping the weak channel loses that much gain.

**13.** *(02-09)* (a) KVL gives $u = Ri_L + L\,di_L/dt + v_C$, and the capacitor gives $C\,dv_C/dt = i_L$. So

$$
v_C' = \frac{i_L}{C} = 3\times10^6\,i_L\ \text{V/s}, \qquad i_L' = \frac{u - v_C - Ri_L}{L} = 10^6(u - v_C - 4i_L)\ \text{A/s}.
$$

Per microsecond the factors $10^6$ drop out, giving $\mathbf{A} = \begin{bmatrix}0 & 3\\ -1 & -4\end{bmatrix}$ and $\mathbf{B} = (0, 1)$. The trace is −4 and the determinant is $0 - (3)(-1) = 3$. Since $\text{tr}^2 - 4\det = 4 > 0$, $\det > 0$ and $\text{tr} < 0$, the eigenvalues are real, distinct and negative: a **stable node** (overdamped, no ringing). They are the roots of $\lambda^2 + 4\lambda + 3$: −1 and −3 per µs.

(b) For $\lambda = -1$: $(\mathbf{A} + \mathbf{I})\mathbf{x} = \mathbf{0}$ gives $x_1 + 3x_2 = 0$, eigenvector $(3, -1)$. For $\lambda = -3$: $3x_1 + 3x_2 = 0$, eigenvector $(1, -1)$. Fit $(1, 0) = c_1(3, -1) + c_2(1, -1)$: $c_1 = \tfrac12$, $c_2 = -\tfrac12$. So

$$
v_C(t) = \tfrac32e^{-t} - \tfrac12e^{-3t}\ \text{V}, \qquad i_L(t) = -\tfrac12e^{-t} + \tfrac12e^{-3t}\ \text{A} \qquad (t \text{ in µs}).
$$

At 1 µs: $v_C = 0.5518 - 0.0249 = 0.5269$ V and $i_L = -0.1839 + 0.0249 = -0.1590$ A. The current is most negative where $i_L' = \tfrac12e^{-t} - \tfrac32e^{-3t} = 0$, at $e^{2t} = 3$, $t = \tfrac12\ln3 = 0.5493$ µs, where $i_L = \tfrac12\big(3^{-3/2} - 3^{-1/2}\big) = -0.19245$ A. The negative sign means the capacitor discharges through the loop. Check: $v_C' = -\tfrac32e^{-t} + \tfrac32e^{-3t} = 3i_L$ ✓, and $\mathbf{x}(0) = (1, 0)$ ✓.

(c) $(s\mathbf{I} - \mathbf{A})^{-1} = \dfrac{1}{s^2 + 4s + 3}\begin{bmatrix}s + 4 & 3\\ -1 & s\end{bmatrix}$. With $\mathbf{C} = (1, 0)$ and $D = 0$:

$$
\frac{V_C(s)}{U(s)} = \frac{3}{s^2 + 4s + 3}\quad(s\text{ in rad/µs}), \quad\text{or}\quad \frac{3\times10^{12}}{s^2 + 4\times10^6s + 3\times10^{12}}\ \text{in SI}.
$$

The DC gain is $3/3 = $ **1**. The steady state is $-\mathbf{A}^{-1}\mathbf{B}\cdot1$, with $\mathbf{A}^{-1} = \tfrac13\begin{bmatrix}-4 & -3\\ 1 & 0\end{bmatrix}$, giving $(1, 0)$: $v_C = 1$ V and no current, as a capacitor in DC steady state requires.

(d) The eigenvalues of $\mathbf{A}_d = e^{\mathbf{A}T}$ are $e^{\lambda T}$: $e^{-0.1} = 0.9048$ and $e^{-0.3} = 0.7408$, inside the unit circle as they must be. Forward Euler multiplies each mode by $1 + h\lambda$. It needs $|1 - 3h| < 1$ for the fast mode, so $h < 2/3 = $ **0.6667 µs**; the slow mode allows up to 2 µs. The fast mode sets the limit.

**14.** *(02-10)* (a) With 23 fraction bits, the floats in $[1, 2)$ are $2^{-23}$ apart, and those in $[\tfrac12, 1)$ half as far: the spacing just below 1 is $2^{-24} = 5.960\times10^{-8}$. The Taylor series gives $1 - \cos x = x^2/2 - x^4/24 + \dots = 5.000\times10^{-9}$ for $x = 10^{-4}$ (the second term is $4\times10^{-18}$). In single precision the computed cosine, $0.999\,999\,995$, must be rounded to a float. It lies less than half a spacing ($2.98\times10^{-8}$) below 1, so it rounds to exactly 1, and the subtraction gives 0: a 100% error. The information was destroyed when the cosine was rounded, and the subtraction exposes it. The fix uses $1 - \cos x = 2\sin^2(x/2)$: $\sin(5\times10^{-5})$ is stored to full relative precision, and squaring and doubling it gives $5.000\times10^{-9}$ correctly.

(b) $f'(x) = 3x^2 - 2$, so $x_{k+1} = x_k - (x_k^3 - 2x_k - 5)/(3x_k^2 - 2)$. The root is $x^* = 2.0945515$.

| $k$ | $x_k$ | $e_k = x_k - x^*$ | $e_k/e_{k-1}^2$ |
|---|---|---|---|
| 0 | 2 | −0.09455 | — |
| 1 | 2.1 | 5.449×10⁻³ | 0.6095 |
| 2 | 2.094568 | 1.664×10⁻⁵ | 0.5605 |
| 3 | 2.0945515 | 1.559×10⁻¹⁰ | 0.5630 |

The theoretical limit is $f''(x^*)/(2f'(x^*)) = 6x^*/\big(2(3x^{*2} - 2)\big) = 0.5630$: the ratios settle onto it, and the correct digits roughly double each step. Bisection halves the bracket each step: $0.5\times2^{-n} < 10^{-8}$ needs $n > \log_2(5\times10^7) = 25.58$, so **26 steps**, against Newton's 3 to reach $10^{-10}$.

(c) Halving $h$ divided the error by $3.2\times10^{-5}/2.0\times10^{-6} = 16 = 2^4$, so the method is **fourth order** (RK4 behaves this way). Halving again should give $2.0\times10^{-6}/16 = 1.25\times10^{-7}$.

(d) Forward Euler needs $|1 + h\lambda_1| < 1$, so $h < 2/1000 = 2$ ms, even long after the fast mode has died. Covering 5 s then takes at least **2500 steps**, though the slow mode alone would allow steps of hundreds of milliseconds. With $h = 10$ ms, $h\lambda_1 = -10$:

- **Backward Euler:** $1/(1 - h\lambda_1) = 1/11 = 0.09091$. The fast mode is crushed, without oscillation.
- **Trapezoidal rule:** $(1 + h\lambda_1/2)/(1 - h\lambda_1/2) = (1 - 5)/(1 + 5) = -0.6667$. It decays, but slowly, and flips sign every step: the trapezoidal ringing that simulators suppress with occasional backward-Euler steps.

Both handle the slow mode well. Its factors are $1/1.01 = 0.9901$ for backward Euler and $0.995/1.005 = 0.99005$ for trapezoidal, against an exact $e^{-0.01} = 0.99005$. The second-order trapezoidal rule is the more accurate.

**15.** *(02-10)* (a) $\mathbf{K}$ is symmetric, so $\kappa = \lambda_{\max}/\lambda_{\min}$. Its trace is 2.5005 and its determinant is $1.001 - 1 = 0.001$, so $\lambda = \tfrac12\left(2.5005 \pm \sqrt{2.5005^2 - 0.004}\right)$, giving $2.5001$ and $4.000\times10^{-4}$. So $\kappa = 6250.5$. Quick check: $\lambda_{\min} \approx \det/\lambda_{\max}$, so $\kappa \approx \lambda_{\max}^2/\det = 2.5001^2/0.001 = 6250$ ✓. Physically, the second row is almost half the first: the two paths are nearly redundant.

(b) $\kappa u$ is about:

- **FP16:** $6250.5\times2^{-11} = 3.052$. The error can be several times the answer: no correct digits.
- **FP32:** $6250.5\times2^{-24} = 3.726\times10^{-4}$, about 3 correct digits.
- **FP64:** $6250.5\times2^{-53} = 6.939\times10^{-13}$, about 12 digits.

(c) Rubric: 2 of the question's 5 points. Award 1 for the reasoning and 1 for two good questions.

- **Reasoning:** no algorithm beats the conditioning of the problem. With $\kappa u > 1$, a pure FP16 solve can lose every digit even on this small, harmless-looking matrix. Real circuit matrices mix conductances from about 1 S down to GMIN-level $10^{-12}$ S and can be far worse conditioned. What can work is **mixed-precision iterative refinement**: factor in FP16 for speed, but compute residuals and accumulate corrections in FP32 or FP64. It converges to high accuracy when $\kappa u_{factor}$ is comfortably below 1. So the claim can be true only if higher precision is hidden in the loop, and only for well-conditioned matrices.
- **Good questions:**
  - What condition numbers do your target matrices have, and what happens above $1/u \approx 2000$?
  - In what precision are residuals computed and solutions accumulated?
  - What accuracy did you measure against a double-precision reference, and on which circuits (stiff, badly scaled, near-singular)?
  - How do you pivot, and how do you detect a refinement that is not converging?

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| X02.1a | magnitude of z1 | 5 | — |
| X02.1b | angle of z1 | 53.13 | ° |
| X02.1c | Re(z1 z2) | 7 | — |
| X02.1d | Im(z1 z2) | 1 | — |
| X02.1e | Re(z1/z2) | −0.5 | — |
| X02.1f | Im(z1/z2) | 3.5 | — |
| X02.1g | real part of the 30° cube root | 1.732 | — |
| X02.1h | imaginary part of the 270° cube root | −2 | — |
| X02.1i | amplitude of the phasor sum | 8.660 | — |
| X02.1j | phase of the phasor sum | 0 | ° |
| X02.2a | impedance magnitude | 111.8 | Ω |
| X02.2b | impedance angle | 26.57 | ° |
| X02.2c | current amplitude | 89.44 | mA |
| X02.2d | current phase | −26.57 | ° |
| X02.2e | capacitor voltage amplitude | 4.472 | V |
| X02.2f | capacitor voltage phase | −116.57 | ° |
| X02.2g | average power | 0.4000 | W |
| X02.2h | in-phase frequency | 707.1 | rad/s |
| X02.2i | current amplitude at that frequency | 100 | mA |
| X02.3a | time constant | 20 | ms |
| X02.3b | v at 10 ms | 2.574 | V |
| X02.3c | time to reach 4 V | 27.73 | ms |
| X02.3d | largest stable Euler step | 40 | ms |
| X02.3e | largest non-alternating Euler step | 20 | ms |
| X02.4a | y(2) | 0.46875 | — |
| X02.4b | ramp response at 1 ms | 1.135 | V |
| X02.4c | ramp tracking error | 1 | V |
| X02.4d | ramp time lag | 0.5 | ms |
| X02.4e | local time constant at y = 1 | 0.5 | — |
| X02.4f | y(1) for y' = 1 − y² | 0.7616 | — |
| X02.5a | natural frequency | 1×10^6 | rad/s |
| X02.5b | neper frequency | 2.5×10^5 | 1/s |
| X02.5c | damping ratio | 0.25 | — |
| X02.5d | quality factor | 2 | — |
| X02.5e | ringing frequency | 9.682×10^5 | rad/s |
| X02.5f | alpha/omega_d | 0.2582 | — |
| X02.5g | peak time | 3.245 | µs |
| X02.5h | overshoot | 44.43 | % |
| X02.5i | peak voltage | 1.444 | V |
| X02.5j | 2% settling estimate | 16 | µs |
| X02.5k | critical-damping resistance | 2 | Ω |
| X02.6a | y(pi/4), resonant case | 0.5890 | — |
| X02.6b | envelope growth rate | 0.75 | per unit time |
| X02.6c | steady-state amplitude at omega = 2 | 2.425 | — |
| X02.6d | steady-state phase at omega = 2 | −75.96 | ° |
| X02.6e | frequency of largest amplitude | 1.732 | rad/s |
| X02.6f | largest amplitude | 2.5 | — |
| X02.6g | band-pass capacitance | 253.3 | pF |
| X02.6h | band-pass resistance | 1.257 | Ω |
| X02.6i | half-power bandwidth | 200 | kHz |
| X02.6j | ring-down time constant | 1.592 | µs |
| X02.6k | cycles per time constant | 15.92 | — |
| X02.7a | y(1) | 1.400 | — |
| X02.7b | y(0+) from the IVT | 1 | — |
| X02.7c | y(inf) from the FVT | 2 | — |
| X02.7d | pole real part | −1 | 1/s |
| X02.7e | pole imaginary part | 3 | rad/s |
| X02.7f | damping ratio of H(s) | 0.3162 | — |
| X02.7g | natural frequency of H(s) | 3.162 | rad/s |
| X02.7h | DC gain | 1 | — |
| X02.7i | pulse response at 3 s | 0.3181 | V |
| X02.7j | pulse response at 2 s | 0.8647 | V |
| X02.8a | a·b | 4 | — |
| X02.8b | length of a | 3 | — |
| X02.8c | length of b | 3 | — |
| X02.8d | angle between a and b | 63.61 | ° |
| X02.8e | projection component 1 | 0.4444 | — |
| X02.8f | projection component 2 | 0.8889 | — |
| X02.8g | length of b − p | 2.687 | — |
| X02.8h | (AB) entry 1,1 | 7 | — |
| X02.8i | (BA) entry 2,2 | 7 | — |
| X02.9a | U entry 2,2 | 1.833 | mS |
| X02.9b | U entry 3,3 | 1.455 | mS |
| X02.9c | L entry 3,2 | −0.5455 | — |
| X02.9d | det G | 4 | mS³ |
| X02.9e | v1 | 0.75 | V |
| X02.9f | v2 | 0.25 | V |
| X02.9g | v3 | 0.125 | V |
| X02.9h | source power | 0.75 | mW |
| X02.9i | v1, source at node 3 | 0.125 | V |
| X02.9j | v2, source at node 3 | 0.375 | V |
| X02.9k | v3, source at node 3 | 0.6875 | V |
| X02.9l | driving-point resistance at node 1 | 750 | Ω |
| X02.9m | driving-point resistance at node 3 | 687.5 | Ω |
| X02.9n | LU flops, n = 3000 | 1.8×10^10 | — |
| X02.9o | flops per extra right-hand side | 1.8×10^7 | — |
| X02.10a | det A | 0 | — |
| X02.10b | rank | 2 | — |
| X02.10c | intercept c | 1.5 | — |
| X02.10d | slope m | 1.0 | — |
| X02.10e | residual sum of squares | 1.0 | — |
| X02.11a | second eigenvalue | 0.7 | — |
| X02.11b | steady-state fraction awake | 0.6667 | — |
| X02.11c | average power | 6.700 | mW |
| X02.11d | p5 | 0.5546 | — |
| X02.11e | slots to within 0.01 | 12 | — |
| X02.11f | new fraction awake | 0.4 | — |
| X02.11g | new average power | 4.060 | mW |
| X02.11h | new second eigenvalue | 0.5 | — |
| X02.12a | smaller eigenvalue of K | 1 | — |
| X02.12b | larger eigenvalue of K | 3 | — |
| X02.12c | second pivot of K | 1.5 | — |
| X02.12d | sigma 1 | 6.708 | — |
| X02.12e | sigma 2 | 2.236 | — |
| X02.12f | condition number of H | 3 | — |
| X02.12g | strong-channel gain | 16.53 | dB |
| X02.12h | weak-channel gain | 6.990 | dB |
| X02.13a | trace of A | −4 | 1/µs |
| X02.13b | det A | 3 | 1/µs² |
| X02.13c | v_C at 1 µs | 0.5269 | V |
| X02.13d | i_L at 1 µs | −0.1590 | A |
| X02.13e | time of most negative current | 0.5493 | µs |
| X02.13f | most negative current | −0.19245 | A |
| X02.13g | DC gain | 1 | — |
| X02.13h | discrete eigenvalue, slow mode | 0.9048 | — |
| X02.13i | discrete eigenvalue, fast mode | 0.7408 | — |
| X02.13j | largest stable Euler step | 0.6667 | µs |
| X02.14a | single-precision spacing just below 1 | 5.960×10^-8 | — |
| X02.14b | half of that spacing | 2.98×10^-8 | — |
| X02.14c | 1 − cos(1e-4) | 5.000×10^-9 | — |
| X02.14d | Newton x2 | 2.094568 | — |
| X02.14e | Newton x3 | 2.0945515 | — |
| X02.14f | Newton error e1 | 5.449×10^-3 | — |
| X02.14g | Newton error e2 | 1.664×10^-5 | — |
| X02.14h | Newton error e3 | 1.559×10^-10 | — |
| X02.14i | ratio e2/e1² | 0.5605 | — |
| X02.14j | ratio e3/e2² | 0.5630 | — |
| X02.14k | limiting ratio | 0.5630 | — |
| X02.14l | bisection steps | 26 | — |
| X02.14m | order of accuracy | 4 | — |
| X02.14n | predicted error at h = 0.005 | 1.25×10^-7 | — |
| X02.14o | largest stable Euler step | 2 | ms |
| X02.14p | Euler steps for 5 s | 2500 | — |
| X02.14q | backward-Euler fast factor | 0.09091 | — |
| X02.14r | trapezoidal fast factor | −0.6667 | — |
| X02.14s | backward-Euler slow factor | 0.9901 | — |
| X02.14t | trapezoidal slow factor | 0.99005 | — |
| X02.14u | Newton error e0 | −0.09455 | — |
| X02.14v | ratio e1/e0² | 0.6095 | — |
| X02.15a | condition number | 6250.5 | — |
| X02.15b | FP16 error estimate | 3.052 | — |
| X02.15c | FP32 error estimate | 3.726×10^-4 | — |
| X02.15d | FP64 error estimate | 6.939×10^-13 | — |
| X02.14w | root of x³ − 2x − 5 | 2.0945515 | — |
| X02.15e | larger eigenvalue of K | 2.5001 | S |
| X02.15f | smaller eigenvalue of K | 4.000×10^-4 | S |
