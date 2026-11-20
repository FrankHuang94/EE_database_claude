<!-- status: reviewed -->
# 15-06 · Root Locus

| | |
|---|---|
| **Course** | [15 · Control Systems](../README.md) |
| **University equivalent** | The root-locus material of a first course in feedback control: angle and magnitude conditions, the sketching rules, gain selection, and the effect of added poles and zeros (Franklin, Powell & Emami-Naeini, *Feedback Control of Dynamic Systems*, ch. 5; Nise, *Control Systems Engineering*, ch. 8–9; Ogata, *Modern Control Engineering*, ch. 6) |
| **Prerequisites** | [15-03 Time Response and Specifications](15-03-time-response.md), [15-05 Stability and the Routh–Hurwitz Criterion](15-05-stability-routh-hurwitz.md), [02-01 Complex Numbers](../../02-complex-numbers-des-and-linear-algebra/chapters/02-01-complex-numbers-euler-and-phasors.md) |
| **Estimated study hours** | 8 |
| **Last verified** | 2026-11-20 |

**Learning objectives.** After this chapter you can:

1. State the angle and magnitude conditions and use them to test whether a point is on the locus and to find the gain that puts a pole there.
2. Sketch a root locus with the rules: branches, real-axis segments, asymptotes, breakaway and break-in points, imaginary-axis crossings and departure angles.
3. Choose a gain from a damping-ratio requirement and predict the response, including the effect of the other poles.
4. Predict how an added zero or pole reshapes the locus, and use a zero to meet a settling-time specification that gain alone cannot.
5. Read the root locus of a third-order PLL and of a positioning servo.

---

## 1. Big picture

A loop's gain is the most common knob a designer turns, and the closed-loop poles move as it turns. The **root locus** is the map of those moves: every path the closed-loop poles take as the gain runs from zero to infinity. It turns the Routh question ("for which gains is it stable?") into a picture that also shows *how* stable, how fast and how oscillatory the loop is at every gain. W. R. Evans introduced the method in 1948 so that designers could sketch the locus by hand from a few rules, without solving a polynomial at each gain. Computers now draw loci instantly, but the rules remain how engineers reason about a design: why a zero helps, why an extra pole hurts, and what no amount of gain can fix.

- **Gain selection.** Pick the point on the locus with the damping you want and read off the gain (Example 15-06.1).
- **Compensator design.** Adding a zero pulls the locus left, toward faster and better-damped responses; this is the root-locus view of lead and PD control (15-08, 15-09).
- **Knowing the limits.** If the locus never enters the region your specification requires (15-03), no gain will work; you need a different controller.
- **Chip loops.** A PLL's damping as its charge-pump current varies, or an amplifier's poles as its feedback factor varies, are root loci (Example 15-06.5).

## 2. Intuition first

**Poles as particles.** Picture each open-loop pole as a particle that starts moving when you raise the gain. Open-loop zeros attract them: some poles end at zeros. Poles without a zero to go to run off to infinity along fixed directions, the asymptotes. Two poles moving toward each other on the real axis collide and veer off into the complex plane as a conjugate pair, which is where oscillation begins.

**An analogy: tightening a spring.** Raising the gain is like stiffening the spring in a mass–spring–damper: the natural frequency rises, but the damping does not rise with it, so the response becomes more oscillatory. A zero is like adding velocity feedback, extra damping that grows with the gain. The analogy breaks down for loops with three or more poles, where higher gain does more than add stiffness: it can push poles into the right half-plane, which a passive spring never does.

**The one equation.** Everything follows from the closed-loop characteristic equation written as

$$
1 + KG(s) = 0 \quad\Longleftrightarrow\quad KG(s) = -1 ,
$$

where $G(s) = N(s)/D(s)$ collects the loop's poles and zeros and $K \ge 0$ is the gain. A complex number equals −1 when its magnitude is 1 and its angle is 180°.

## 3. Theory

### 3.1 The angle and magnitude conditions

Write $G(s) = \dfrac{(s - z_1)\cdots(s - z_m)}{(s - p_1)\cdots(s - p_n)}$. A point $s_0$ is on the root locus for some $K \ge 0$ if and only if

$$
\angle G(s_0) = \sum_{i=1}^{m}\angle(s_0 - z_i) - \sum_{j=1}^{n}\angle(s_0 - p_j) = \pm 180°(2k + 1) ,
$$

the **angle condition**. The gain that places a pole there then follows from the **magnitude condition**:

$$
K = \frac{1}{\lvert G(s_0)\rvert} = \frac{\prod_j\lvert s_0 - p_j\rvert}{\prod_i\lvert s_0 - z_i\rvert} .
$$

Each factor $s_0 - p_j$ is a vector from the pole $p_j$ to the point $s_0$ (02-01), so the conditions are geometric: angles and lengths of vectors drawn from the poles and zeros to the test point.

### 3.2 The sketching rules

Let $n$ be the number of open-loop poles and $m \le n$ the number of zeros.

**Rule 1 · Branches.** There are $n$ branches. They start at the open-loop poles ($K = 0$, where $D(s) = 0$) and end at the open-loop zeros ($K \to \infty$, where $N(s) = 0$); the remaining $n - m$ go to infinity. The locus is symmetric about the real axis.

**Rule 2 · Real-axis segments.** A real point is on the locus if the number of real poles and zeros to its right is odd. (Complex pairs contribute angles that cancel; each real pole or zero to the right contributes 180°.)

**Rule 3 · Asymptotes.** The $n - m$ branches that go to infinity approach straight lines at angles $\dfrac{(2k + 1)180°}{n - m}$, $k = 0, 1, \ldots$, which meet the real axis at the **centroid**

$$
\sigma_a = \frac{\sum p_j - \sum z_i}{n - m} .
$$

**Rule 4 · Breakaway and break-in points.** Where branches meet on the real axis and leave it (or arrive), $K$ as a function of real $s$ has a local extremum. With $K = -D(s)/N(s)$ on the locus, $dK/ds = 0$ gives

$$
N(s)D'(s) - D(s)N'(s) = 0 ,
$$

keeping only roots that lie on a real-axis segment (positive $K$).

**Rule 5 · Imaginary-axis crossings.** Use Routh (15-05): the gain that zeroes a first-column entry, and the auxiliary polynomial's roots, give the crossing.

**Rule 6 · Departure and arrival angles.** Apply the angle condition at a point infinitesimally close to a complex pole $p$: the branch leaves $p$ at

$$
\theta_{dep} = 180° - \sum_{p_j \ne p}\angle(p - p_j) + \sum_i\angle(p - z_i) ,
$$

and arrives at a complex zero at the analogous angle with the roles of poles and zeros swapped. At a pole of multiplicity $q$ (for example a double pole at the origin), the $q$ branches leave at

$$
\theta_{dep} = \frac{(2k + 1)180° - \sum_{p_j \ne p}\angle(p - p_j) + \sum_i\angle(p - z_i)}{q}, \qquad k = 0, 1, \ldots, q - 1 ,
$$

because near $p$ the factor $(s - p)^q$ contributes $q$ times the angle of $s - p$. A double pole with no net angle from the rest of the map leaves at ±90° (Example 15-06.5).

**Rule 7 · Constant sum.** If $n - m \ge 2$, the sum of the closed-loop poles equals the sum of the open-loop poles for every $K$ (the coefficient of $s^{n-1}$ does not involve $K$). When some poles move right, others must move left.

> **Going deeper — why the asymptotes meet at the centroid.** For large $\lvert s\rvert$, $G(s) \approx s^{-(n-m)}(1 + (\sum p - \sum z)/s + \cdots)$, so $G(s) \approx (s - \sigma_a)^{-(n-m)}$ with $\sigma_a$ as above, by the binomial expansion. The far locus therefore behaves like $n - m$ poles all sitting at $\sigma_a$, whose locus is a star of straight lines from $\sigma_a$ at the asymptote angles.

### 3.3 Choosing a gain from the locus

Draw the ray of the desired damping ratio, at angle $\arccos\zeta$ from the negative real axis (15-03). Where the locus crosses it, read the point $s_0$ and compute $K$ from the magnitude condition. Then find the other closed-loop poles at that $K$, either by dividing them out or by noting where the other branches are. They tell you whether the dominant-pair approximation holds (15-03 §3.5). The locus also shows what the gain cannot do. In Example 15-06.1 the complex poles move along a vertical line, so no gain changes the settling time.

### 3.4 What added zeros and poles do

- **A zero pulls the locus toward itself and to the left.** It reduces the number of asymptotes by one, so the asymptotes open out (from ±60° for three to vertical for two), and the new centroid is $(\sum p - \sum z - z_{new})/(n - m - 1)$. Two effects compete: for a left-half-plane zero ($z_{new} < 0$) its own term $-z_{new}/(n - m - 1)$ is positive and pulls the centroid right, while dividing the (usually negative) $\sum p - \sum z$ by a smaller number pulls it left. In Example 15-06.3 the net move is left, from −2 to −2.5. With $n - m = 2$ the asymptotes are vertical lines through the centroid, so a centroid in the left half-plane guarantees stability at large gains. It does not by itself guarantee stability at every gain: Problem 15-05.4's loop $K(s + 1)/[s(s - 1)(s + 6)]$ has its centroid at −2 yet is unstable for $0 < K < 7.5$, because its plant has a right-half-plane pole. For a stable three-pole plant with one zero, Routh's cubic test reduces to $K(a_2 - b_0) > a_0 - a_2a_1$ (plant denominator $s^3 + a_2s^2 + a_1s + a_0$, zero factor $s + b_0$), which holds for every $K > 0$ exactly when the centroid $(b_0 - a_2)/2$ is in the left half-plane; that is the case of Example 15-06.3. A zero placed too far left pushes the centroid into the right half-plane, and then large gains destabilize the loop (lab Part 2). This is the root-locus explanation of why derivative (PD) and lead compensation stabilize and speed up loops (15-08, 15-09).
- **A pole pushes the locus to the right.** It adds an asymptote, so the asymptotes close in toward the imaginary axis (from vertical for two to ±60° for three), and ±60° lines eventually cross into the right half-plane whatever the centroid. The centroid itself can move either way: adding a pole at −10 to $s(s + 4)$ moves it from −2 to −4.67, yet the loop now goes unstable at high gain (Problem 15-06.7). A third pole bends the branches into the right half-plane (Example 15-06.2 against 15-06.1). Every parasitic pole is a potential instability.
- **A pole–zero pair close together (a dipole) barely moves the locus** except near itself, but it changes the low-frequency gain. A lag compensator places such a pair near the origin to raise $K_v$ without disturbing the dominant poles (15-09).

![Three root-locus plots. Left: K/[s(s+2)(s+4)]. Poles at 0, -2 and -4. The branches from 0 and -2 meet near -0.85 and curve up and down into the right half-plane, crossing the imaginary axis near plus and minus j2.8; the branch from -4 runs left along the real axis. A dashed damping-ratio line at 60 degrees from the negative real axis meets the upper branch at -0.67 + j1.15. Middle: the same loop with a zero at -1. The pole at 0 moves to the zero; the poles at -2 and -4 meet near -2.9 and rise and fall almost vertically near Re s = -2.5, never reaching the right half-plane; the damping line meets them at -2.57 + j4.45. Right: K(s+8)/[s(s+4)]. The poles at 0 and -4 meet at -2.34, travel around a circle centered at the zero -8 of radius 5.66, and rejoin the real axis at -13.7; the 45-degree damping line just touches the circle at -4 + j4.](../../../assets/figures/15-06/loci.svg)

*Figure 1. Left: three poles, so the locus enters the right half-plane (Example 15-06.2). Middle: a zero at −1 pulls it left and keeps it stable for every gain (Example 15-06.3). Right: two poles and a zero give a circle; the design point is where the damping ray is tangent (Example 15-06.6). Crosses are open-loop poles, circles zeros, dots the chosen closed-loop poles.*

### 3.5 The circle with two poles and a zero

For $G(s) = (s - z)/[(s - p_1)(s - p_2)]$ with one real zero $z$ and two poles (real or a complex pair), where the zero lies to the left of the real-axis segment between real poles, the complex part of the locus is a circle centered at the zero. Its radius is the geometric mean of the zero's distances to the two poles,

$$
\rho = \sqrt{\lvert z - p_1\rvert\,\lvert z - p_2\rvert} .
$$

For a complex pair the two distances are equal, so the circle passes through both poles (Example 15-06.4). The proof substitutes $s = z + \rho e^{j\phi}$ into the angle condition and shows it holds for every $\phi$ on this circle (Problem 15-06.9). The circle makes design by hand easy: the least damping on the circle, a floor that holds for every gain, is at the point where a ray from the origin is tangent to it (Example 15-06.6).

### 3.6 Negative gain and other parameters

The method works for any parameter that enters the characteristic polynomial linearly. Rewrite the polynomial as $D(s) + \alpha N(s)$ and draw the locus in $\alpha$. For a negative gain (positive feedback) the angle condition becomes $0°$ instead of $180°$, the real-axis rule flips to an even count, and the asymptote angles become $k \cdot 360°/(n - m)$. Problem 15-06.12 draws a locus in a loop-filter time constant.

## 4. Worked examples

### Example 15-06.1 · Two poles: the vertical line (tier A)

**Setup.** Sketch the locus of $L = K/[s(s + 4)]$ and find the gain for $\zeta$ = 0.707.

**Solution.** Two branches start at 0 and −4. The real-axis segment $[-4, 0]$ is on the locus (one pole to the right). The breakaway point solves $d[s(s + 4)]/ds = 2s + 4 = 0$: $s$ = **−2**, where $K = 2 \times 2$ = **4**. There are two asymptotes at ±90° through the centroid $(0 - 4)/2 = -2$, so above $K$ = 4 the poles move along the vertical line $\mathrm{Re}\,s = -2$.

For $\zeta$ = 0.707 the ray at 45° meets the line at $s_0 = -2 + j2$. The magnitude condition gives $K = \lvert s_0\rvert\,\lvert s_0 + 4\rvert = 2\sqrt2 \times 2\sqrt2$ = **8**.

**Units check.** $K$ has units of 1/s², as the product of two distances in the s-plane.

**Sanity check.** The characteristic polynomial $s^2 + 4s + 8$ has roots $-2 \pm j2$. Every gain above 4 gives the same real part, so the settling time ($4/\sigma$ ≈ 2 s) cannot be improved by gain.

### Example 15-06.2 · Three poles: the locus enters the right half-plane (tier B)

**Setup.** Sketch the locus of $L = K/[s(s + 2)(s + 4)]$ (15-05's loop) and choose $K$ for $\zeta$ = 0.5.

**Solution.**

- Real-axis segments: $[-2, 0]$ and $(-\infty, -4]$.
- Asymptotes: $n - m$ = 3, at 60°, 180° and 300°, from the centroid $(0 - 2 - 4)/3$ = **−2**.
- Breakaway: $3s^2 + 12s + 8 = 0$ gives $s$ = **−0.845** (the other root, −3.15, is not on the locus), at $K$ = **3.08**.
- Imaginary-axis crossing (15-05): $\pm j$**2.828** at $K$ = 48.

The $\zeta$ = 0.5 ray, $s = r(-0.5 + j0.866)$, satisfies the angle condition at $r$ = 4/3: $s_0$ = **−0.667 + j1.155**, where $K = \lvert s_0\rvert\,\lvert s_0 + 2\rvert\,\lvert s_0 + 4\rvert$ = **8.30** (exactly 224/27). The third pole follows from the constant sum: $-6 - 2(-0.667)$ = **−4.67**, seven times farther left than the dominant pair. Simulating the closed loop gives an overshoot of **15.5**%, close to the 16.3% of a pure second-order system at $\zeta$ = 0.5.

**Units check.** $K$ has units of 1/s³.

**Sanity check.** The constant-sum rule checks the third pole: $-0.667 \times 2 - 4.667 = -6$.

### Example 15-06.3 · A zero pulls the locus left (tier B)

**Setup.** Add a zero at −1 to Example 15-06.2: $L = K(s + 1)/[s(s + 2)(s + 4)]$. Sketch the locus and find $K$ for $\zeta$ = 0.5.

**Solution.**

- Real-axis segments: $[-1, 0]$ (the pole at 0 goes to the zero at −1) and $[-4, -2]$.
- Asymptotes: $n - m$ = 2, at ±90°, from the centroid $[(0 - 2 - 4) - (-1)]/2$ = **−2.5**.
- Breakaway: $(s + 1)(3s^2 + 12s + 8) - (s^3 + 6s^2 + 8s) = 2s^3 + 9s^2 + 12s + 8 = 0$ has one real root, **−2.91**, between −4 and −2, at $K$ = **1.51**.

The branches from −2 and −4 meet at −2.91 and then head up and down toward the vertical asymptotes at −2.5. They never cross the imaginary axis: the loop is stable for every $K$. On the $\zeta$ = 0.5 ray, the angle condition holds at $s_0$ = **−2.567 + j4.447**, with $K$ = **22.8**. The real part is nearly four times that of Example 15-06.2: the zero has made a much faster loop possible.

**Units check.** $K$ now has units of 1/s², since $L$ has one zero.

**Sanity check.** The third closed-loop pole lies on $[-1, 0]$, near the zero at −1. That pole and the zero nearly cancel, but its slow mode is still visible in the step response (15-03 §3.6, a doublet).

### Example 15-06.4 · Departure angles and the circle (tier B)

**Setup.** $L = K(s + 2)/(s^2 + 2s + 5)$ has complex poles at $-1 \pm j2$ and a zero at −2. Find the departure angle from $-1 + j2$, the break-in point and its gain, and show the complex part of the locus is a circle.

**Solution.** From $p_1 = -1 + j2$: the angle from the other pole $p_2 = -1 - j2$ is 90°, and from the zero is $\angle(1 + j2)$ = 63.43°. So

$$
\theta_{dep} = 180° - 90° + 63.43° = \mathbf{153.4}° .
$$

The branch leaves the pole heading up and to the left. The real-axis segment is $(-\infty, -2]$. The break-in point solves $(s + 2)(2s + 2) - (s^2 + 2s + 5) = s^2 + 4s - 1 = 0$: $s = -2 - \sqrt5$ = **−4.236**, at $K$ = **6.47**. By §3.5 the complex branches lie on a circle centered at the zero, of radius $\lvert p_1 - (-2)\rvert = \sqrt{1 + 4}$ = **2.236**, which indeed passes through both poles and the break-in point.

**Units check.** Angles in degrees; distances in 1/s.

**Sanity check.** The break-in point is $\sqrt5$ left of the zero, on the circle, as it must be.

### Example 15-06.5 · A third-order PLL as gain varies (tier C)

**Setup.** Example 15-05.5's PLL has $L = K(1 + s\tau_z)/[s^2(1 + s\tau_p)]$ with $\tau_z$ = 5 µs and $\tau_p = \tau_z/11$. Its gain $K$ is proportional to the charge-pump current. Describe the locus as $K$ varies, find the real-axis meeting points and their gains, and the damping at the design gain $K = 9.09 \times 10^{10}$ s⁻².

**Solution.** The open-loop poles are a double pole at the origin and $-1/\tau_p$ = −2.2 × 10⁶ s⁻¹; the zero is at $-1/\tau_z$ = −2 × 10⁵ s⁻¹. With $n - m$ = 2, the asymptotes are vertical, at the centroid $(-2.2 \times 10^6 + 2 \times 10^5)/2 = -10^6$ s⁻¹. The double pole at the origin splits vertically ($\pm$90°) into the left half-plane, pulled by the zero.

The breakpoint equation $N D' - D N' = 0$ reduces to $s[2 + (3\tau_p + \tau_z)s + 2\tau_z\tau_ps^2] = 0$, with real roots **−4.764 × 10⁵** and **−9.236 × 10⁵** s⁻¹, at $K$ = **1.287 × 10¹¹** and **1.368 × 10¹¹** s⁻². The complex pair from the origin comes down to the real axis at the first point; for gains between the two values all three poles are real; above the second, two of them leave the axis again toward the asymptotes. (Real meeting points exist only because $\tau_z/\tau_p$ = 11 exceeds 9.)

At the design gain the closed-loop poles are $-2.630 \times 10^5 \pm j2.243 \times 10^5$ and $-1.674 \times 10^6$ s⁻¹ (15-05), so the dominant pair has $\zeta$ = **0.761**. Raising the charge-pump current by about 40% would make the loop's dominant poles real and its step response overshoot-free in the second-order sense, though the closed-loop zero still adds overshoot (15-03).

**Units check.** $K\tau_z$ is in 1/s; the breakpoints are in 1/s.

**Sanity check.** The locus is stable for every $K$, as Example 15-05.5's condition $\tau_z > \tau_p$ promised.

### Example 15-06.6 · A zero meets a settling-time specification (tier C)

**Setup.** The servo of Example 15-06.1 must settle in about 1 s with $\zeta \ge$ 0.707. Show that proportional gain cannot do it, and that a PD controller $C = K(s + 8)$ can. Find $K$, the closed-loop poles and the step response.

**Solution.** With $C = K$, $\sigma$ = 2 for every underdamped gain, so $t_s \approx 4/\sigma$ = 2 s; at $K$ = 8 ($\zeta$ = 0.707) the exact 2% settling time is **2.11** s. Gain alone cannot help.

With $C = K(s + 8)$, $L = K(s + 8)/[s(s + 4)]$. By §3.5 the complex locus is a circle centered at −8 with radius $\sqrt{8 \times 4}$ = **5.657**. The $\zeta$ = 0.707 ray (45°) passes at distance $8\sin 45°$ = 5.657 from the center, so it is exactly tangent to the circle: $\zeta$ = 0.707 is the smallest damping the circle reaches, at the tangent point $s_0$ = **−4 ± j4**. The magnitude condition gives $K = \lvert s_0\rvert\,\lvert s_0 + 4\rvert/\lvert s_0 + 8\rvert = 5.657 \times 4/5.657$ = **4**. The closed loop is $T = 4(s + 8)/(s^2 + 8s + 32)$.

Simulating: overshoot **6.70**% (above 4.3% because of the closed-loop zero at −8) and 2% settling time **0.932** s, less than half the proportional loop's.

**Units check.** $K$ in 1/s here (one zero, two poles).

**Sanity check.** The real part doubled from −2 to −4, as the circle's geometry required. The zero bought speed, and its own overshoot is the price (15-03 §3.6).

### Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 15-06.1a | breakaway point | −2 | 1/s |
| Ex 15-06.1b | K at the breakaway | 4 | 1/s² |
| Ex 15-06.1c | K for ζ = 0.707 | 8 | 1/s² |
| Ex 15-06.2a | centroid | −2 | 1/s |
| Ex 15-06.2b | breakaway point | −0.845 | 1/s |
| Ex 15-06.2c | K at the breakaway | 3.08 | 1/s³ |
| Ex 15-06.2d | imaginary-axis crossing | 2.828 | rad/s |
| Ex 15-06.2e | pole for ζ = 0.5 | −0.667 + j1.155 | 1/s |
| Ex 15-06.2f | K for ζ = 0.5 | 8.30 | 1/s³ |
| Ex 15-06.2g | third pole | −4.67 | 1/s |
| Ex 15-06.2h | overshoot | 15.5 | % |
| Ex 15-06.3a | centroid | −2.5 | 1/s |
| Ex 15-06.3b | breakaway point | −2.91 | 1/s |
| Ex 15-06.3c | K at the breakaway | 1.51 | 1/s² |
| Ex 15-06.3d | pole for ζ = 0.5 | −2.567 + j4.447 | 1/s |
| Ex 15-06.3e | K for ζ = 0.5 | 22.8 | 1/s² |
| Ex 15-06.4a | departure angle | 153.4 | ° |
| Ex 15-06.4b | break-in point | −4.236 | 1/s |
| Ex 15-06.4c | K at the break-in | 6.47 | 1/s |
| Ex 15-06.4d | circle radius | 2.236 | 1/s |
| Ex 15-06.5a | first real meeting point | −4.764e5 | 1/s |
| Ex 15-06.5b | its gain | 1.287e11 | 1/s² |
| Ex 15-06.5c | second real meeting point | −9.236e5 | 1/s |
| Ex 15-06.5d | its gain | 1.368e11 | 1/s² |
| Ex 15-06.5e | ζ at the design gain | 0.761 | — |
| Ex 15-06.6a | settling, proportional | 2.11 | s |
| Ex 15-06.6b | circle radius | 5.657 | 1/s |
| Ex 15-06.6c | pole real part | −4 | 1/s |
| Ex 15-06.6d | K | 4 | 1/s |
| Ex 15-06.6e | overshoot | 6.70 | % |
| Ex 15-06.6f | settling time | 0.932 | s |

## 5. Simulate it

The lab, [labs/15-06-lab](../labs/15-06-lab/README.md), provides `rlocus.py`: a numerical locus with continuous branch tracking, and each sketching rule computed exactly (asymptotes, real-axis segments, breakpoints, departure angles, gain at a point, points on a constant-damping ray). You:

1. **Overlay the rules on the numerical locus** for Examples 15-06.1 to 15-06.4 and check each rule's prediction.
2. **Move a zero** along the real axis for Example 15-06.3's loop and watch the centroid and the largest stable gain change.
3. **Sweep the PLL's charge-pump current** (Example 15-06.5) and plot $\zeta$ of the dominant pair against $K$.
4. **Build the PD servo** of Example 15-06.6 in ngspice (`pd_servo.cir`) and compare its overshoot and settling time with the design.

**Guided exercise (predict, then run).** **Before Part 2,** predict where the zero must sit for the loop $K(s + z)/[s(s + 2)(s + 4)]$ to have asymptotes centered at −3. (At $z$ = 0, since $(−6 + z)/2 = −3$; then the zero cancels the pole at the origin, a warning that centroid targets alone do not make a design.)

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Gain along the locus | Speed and accuracy, until damping falls | Overshoot, and instability if a branch crosses the axis | Control designer |
| Adding a zero (PD, lead) | Pulls the locus left: faster and better damped | Noise amplification at high frequency; the closed-loop zero adds overshoot | Control designer |
| Removing or moving parasitic poles farther left | Raises the gain at which branches cross | Power and area (faster stages) | Circuit designer |
| A pole–zero dipole near the origin (lag) | Low-frequency gain without moving dominant poles | A slow tail (doublet) in the step response | Control designer |
| PLL zero-to-pole ratio $\tau_z/\tau_p$ | Damping and margin (and real poles above a ratio of 9) | Less reference-spur filtering | PLL designer |

## 7. Numbers to know

| Quantity | Value | Source |
|---|---|---|
| Asymptote angles for $n - m$ = 1, 2, 3, 4 | 180°; ±90°; ±60° and 180°; ±45° and ±135° | §3.2 |
| Centroid | $(\sum p - \sum z)/(n - m)$ | §3.2 |
| Two poles at 0 and $-a$, gain $K$ | vertical line at $-a/2$; settling time fixed at about $8/a$ | Example 15-06.1 |
| Two poles and a zero to their left | circle centered at the zero, radius $\sqrt{\lvert z - p_1\rvert\,\lvert z - p_2\rvert}$ | §3.5 |
| Smallest damping on that circle | $\cos\theta$ with $\sin\theta$ = radius / distance from origin to the zero | Example 15-06.6 |

## 8. Common mistakes

- **Counting complex poles in the real-axis rule.** Only real poles and zeros to the right count.
- **Measuring angles from the wrong end.** Vectors go *from* each pole or zero *to* the test point.
- **Forgetting the zeros at infinity.** With $n > m$, $n - m$ branches go to infinity along asymptotes; they do not stop.
- **Keeping breakaway candidates that are not on the locus.** A root of $ND' - DN' = 0$ is a breakpoint only on a real-axis segment, with positive $K$.
- **Reading the dominant-pole response without checking the other poles and zeros.** Example 15-06.3's slow pole near its zero and Example 15-06.6's closed-loop zero both change the response.
- **Using the 180° condition for a negative gain.** Positive feedback uses the 0° locus.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

These are established practice; no perishable figures are quoted.

- **Software draws the locus; engineers read it.** MATLAB's `rlocus` and the Python Control Systems Library's `root_locus` (15-02's R-229) plot loci directly, and interactive tools let a designer drag poles and zeros. The rules remain the way to understand what a plot shows and to sanity-check it **[Established]**.
- **Root locus in parameter, not just gain.** Circuit designers trace closed-loop poles against a bias current, a compensation capacitor or a load, by sweeping a simulation parameter; the plot is a root locus in that parameter (§3.6) **[Established]**.
- **Analog loops are often designed with Bode plots instead** (15-07), because measured frequency responses are available and delays are easy to include; root locus is preferred when pole positions themselves are specified, as in damping requirements for PLLs and servos **[Established]**.

### Why it matters commercially

- **Product variation moves poles.** A charge-pump current that varies by tens of percent over process and temperature (±30% is an illustrative design budget, not a sourced figure) moves a PLL along its root locus; the design must have acceptable damping over the whole stretch (Example 15-06.5).
- **"More gain" has a ceiling.** The locus shows where gain stops helping (a fixed real part) or starts hurting (branches toward the axis), which is often the argument for a better controller or a faster part.
- **Compensation is a product feature.** Customers who can add a zero (feedforward capacitors in regulators, for instance) can trade stability for speed; data sheets that show how are more valuable.

### Marketing vs Reality

- **"Higher loop gain for faster response."** *Reality:* with two poles, gain does not shorten settling; with three or more, it eventually destabilizes. *Sanity check:* ask where the dominant poles sit at the proposed gain, and what the third pole is doing.
- **"Stable for all load conditions."** *Reality:* a load moves the plant's poles, which reshapes the locus. *Sanity check:* ask for the locus or the closed-loop poles at the load extremes.
- **"Adding a zero fixes it."** *Reality:* it does pull the locus left, but the closed-loop zero adds overshoot and the derivative action amplifies noise. *Sanity check:* ask for the step response and the noise bandwidth after the change.

### Questions for engineering leaders

1. **"Across your process and temperature spread, how far do the dominant poles move, and what is the worst damping?"**
   *Strong:* a locus or pole plot over corners with the worst case marked. *Evasive:* a typical-corner design only.
2. **"What limits the loop's speed: the plant, a parasitic pole, or the controller structure?"**
   *Strong:* identifies the pole or zero that sets the locus's shape. *Evasive:* "we can always raise the gain".
3. **"If you add a zero for speed, what does it do to noise and overshoot?"**
   *Strong:* quantifies both. *Evasive:* speed only.
4. **"Where are the closed-loop zeros, and are any near the dominant poles?"**
   *Strong:* lists them and explains their effect on settling. *Evasive:* poles only.

## 10. Concept check

**Q1.** State the angle and magnitude conditions.

<details><summary>Answer</summary>

$s_0$ is on the locus if $\angle G(s_0)$ is an odd multiple of 180°; the gain there is $K = 1/\lvert G(s_0)\rvert$, the product of distances from the poles divided by the product of distances from the zeros.

</details>

**Q2.** Why does a real-axis point lie on the locus when the count of real poles and zeros to its right is odd?

<details><summary>Answer</summary>

Each real pole or zero to the right contributes 180° to the angle of $G$, each one to the left contributes 0°, and complex pairs contribute angles that cancel. An odd count gives an odd multiple of 180°.

</details>

**Q3.** How many asymptotes are there, and where do they meet?

<details><summary>Answer</summary>

$n - m$, at angles $(2k + 1)180°/(n - m)$, meeting at the centroid $(\sum p - \sum z)/(n - m)$.

</details>

**Q4.** Why can raising the gain of $K/[s(s + 4)]$ never shorten the settling time?

<details><summary>Answer</summary>

Above $K$ = 4 the poles move vertically along $\mathrm{Re}\,s = -2$; settling time depends on the real part, which stays at −2.

</details>

**Q5.** Why does adding a zero to the left of the poles tend to stabilize a loop?

<details><summary>Answer</summary>

It removes one asymptote and pulls the branches toward itself. With $n - m$ = 2 the asymptotes are vertical lines through the centroid, so a left-half-plane centroid keeps the loop stable at large gains. Intermediate gains still need checking (Routh): with a stable plant, as in Example 15-06.3, the branches never reach the right half-plane at any gain, but Problem 15-05.4's unstable plant has a left-half-plane centroid and is still unstable at low gain.

</details>

**Q6.** How do you find breakaway points?

<details><summary>Answer</summary>

Solve $N(s)D'(s) - D(s)N'(s) = 0$ (equivalently $dK/ds = 0$ along the real axis) and keep the real roots on locus segments with positive $K$.

</details>

**Q7.** What does the constant-sum rule tell you about a three-pole loop as gain rises?

<details><summary>Answer</summary>

With $n - m \ge 2$, the closed-loop poles' sum is fixed. If the complex pair moves right toward the axis, the third pole must move left by twice as much.

</details>

Practice: [Problems 15-06](../problems/15-06-problems.md) · [Solutions](../solutions/15-06-solutions.md)

## 11. Key terms

[Root locus](../../../reference/glossary.md#root-locus) · [Angle condition](../../../reference/glossary.md#angle-condition) · [Magnitude condition](../../../reference/glossary.md#magnitude-condition) · [Asymptote centroid](../../../reference/glossary.md#asymptote-centroid) · [Breakaway point](../../../reference/glossary.md#breakaway-point) · [Departure angle](../../../reference/glossary.md#departure-angle) · [Dominant poles](../../../reference/glossary.md#dominant-poles)

## 12. Connections

- **Builds on:** pole locations and specifications ([15-03](15-03-time-response.md)); Routh and gain ranges ([15-05](15-05-stability-routh-hurwitz.md)); complex numbers as vectors ([02-01](../../02-complex-numbers-des-and-linear-algebra/chapters/02-01-complex-numbers-euler-and-phasors.md)).
- **Next:** [15-07 Frequency-Domain Design](15-07-frequency-domain-design.md), which studies the same loops through $L(j\omega)$, margins and Nyquist.
- **Used later:** PD and PID control ([15-08](15-08-pid-control.md)); lead and lag compensation by root locus ([15-09](15-09-lead-lag-compensation.md)); pole placement by state feedback ([15-10](15-10-state-space-introduction.md)); PLL design ([15-12](15-12-control-applications-pll-regulators-thermal.md)).

## 13. Further study

- G. F. Franklin, J. D. Powell and A. Emami-Naeini, *Feedback Control of Dynamic Systems*, ch. 5 (the root-locus rules, design with dynamic compensation).
- N. S. Nise, *Control Systems Engineering*, ch. 8–9 (root-locus techniques and design via root locus).
- W. R. Evans, "Control system synthesis by root locus method," *Transactions of the AIEE* 69(1), 1950 (the method's original exposition).
- MIT OpenCourseWare 6.302, *Feedback Systems*: lectures on root locus.

## 14. Sources

1. Franklin, Powell and Emami-Naeini; Nise (Further study): the root-locus rules (textbook material).
2. W. R. Evans, *Transactions of the AIEE* 69(1), 1950: the method.

This chapter has no perishable industry figures; its practitioner statements are tagged [Established]. Every number in the examples is recomputed by the verify script from the angle and magnitude conditions and checked against numerically computed closed-loop roots; Example 15-06.6 is confirmed in ngspice.
