# Solutions 13-02 · Electrostatics: Boundary Conditions and Boundary-Value Problems

Problems: [13-02 problems](../problems/13-02-problems.md) · Chapter: [13-02](../chapters/13-02-electrostatics-boundary-value-problems.md). Every number below is recomputed by [verify_13_02.py](../verify/verify_13_02.py), which solves the boundary-value problems independently: symbolic integration for the one-dimensional cases, finite differences for the troughs, numerical integration of image fields, and a method-of-moments solution for the wires.

---

## Solutions

### Solution 13-02.1

At a conductor $D_n = \rho_s$, so $\rho_s = \varepsilon_0E_n = 8.854 \times 10^{-12} \times 2 \times 10^6$ = **17.71** µC/m². At breakdown, $\varepsilon_0 \times 3$ MV/m = **26.56** µC/m². Units: (F/m)(V/m) = C/m².

### Solution 13-02.2

Tangential: $E_{2x}$ = 2 kV/m. Normal $D$: $\varepsilon_0 \times 6 = 6\varepsilon_0E_{2z}$, so $E_{2z}$ = 1 kV/m. $\vec{E}_2 = 2\hat{x} + \hat{z}$ kV/m, magnitude **2.236** kV/m. Angles from the normal: $\arctan(2/6)$ = **18.4**° in air and $\arctan(2/1)$ = **63.4**° in the glass; their tangents are in the ratio 1/6, the permittivity ratio.

### Solution 13-02.3

The normal $D$ is the same in both layers, so the voltages add like series capacitors: $C/A = 1/(d_1/\varepsilon_1 + d_2/\varepsilon_2)$. Writing this as $\varepsilon_{ox}/\text{EOT}$ gives $\text{EOT} = d_1 + d_2(3.9/20)$ = 1 + 0.585 = **1.585** nm. Then $C/A = 3.9\varepsilon_0/1.585\ \text{nm}$ = 0.02179 F/m² = **21.79** fF/µm². The 3 nm high-permittivity layer counts as only 0.585 nm of oxide: physically thicker (less tunnelling leakage) but electrically thin.

### Solution 13-02.4

With spherical symmetry, $r^2\,dV/dr = A$, so $V = -A/r + B$. With $V(a) = V_0$ and $V(b) = 0$: $V = V_0(1/r - 1/b)/(1/a - 1/b)$. The field at $a$ is $E_r = V_0/[a^2(1/a - 1/b)]$, the charge $Q = 4\pi a^2\varepsilon_0E_r = 4\pi\varepsilon_0V_0/(1/a - 1/b)$, and

$$
C = \frac{4\pi\varepsilon_0ab}{b - a} = \frac{4\pi\varepsilon_0 \times 0.01 \times 0.02}{0.01} = \mathbf{2.225}\ \text{pF}.
$$

With $b \to \infty$, $C = 4\pi\varepsilon_0a$ = **1.113** pF. Bringing the outer shell in from infinity to twice the radius doubles the capacitance.

### Solution 13-02.5

At voltage $V_0$ the peak field is at the inner conductor, $E(a) = V_0/[a\ln(b/a)]$. Holding $E(a)$ at the breakdown field, $V_0 = E_{bd}\,a\ln(b/a)$, which is maximized where $d/da[a\ln(b/a)] = \ln(b/a) - 1 = 0$: $a = b/e$ = **1.839** mm. Then $V_0 = E_{bd}\,a$ = 3 MV/m × 1.839 mm = **5.518** kV. A thinner inner conductor concentrates the field; a fatter one leaves too little gap. (The same kind of trade, with loss or power handling as the criterion, sets the familiar 50 Ω and 75 Ω cable impedances, 13-09. With $b/a = e$ the impedance of an air line is $60\ln e$ = 60 Ω.)

### Solution 13-02.6

Put $x$ = 0 at the junction and $x = W$ at the far edge. In the depletion region $\rho_v = -qN_A$, so $d^2V/dx^2 = qN_A/\varepsilon$. Gauss's law in one dimension is $dE/dx = \rho_v/\varepsilon = -qN_A/\varepsilon$, and with $E(W) = 0$ this integrates to $E(x) = +(qN_A/\varepsilon)(W - x)$: positive, pointing from the n side toward the p side, and largest at the junction: $qN_AW/\varepsilon = 1.602 \times 10^{-19} \times 10^{22} \times 0.3 \times 10^{-6}/(11.7\varepsilon_0)$ = **4.640** MV/m. Integrating once more, the voltage across the region is the area under the triangular field, $qN_AW^2/(2\varepsilon)$ = **0.6960** V. (09-05 uses the same calculation for both sides of a junction.)

### Solution 13-02.7

With $a$ = 2 cm and $b$ = 1 cm, at the centre $x = a/2$ (so $\sin(n\pi/2) = \pm1$) and $y = b/2$. The first term is $(4 \times 10/\pi)\sinh(\pi/4)/\sinh(\pi/2)$ = **4.806** V. The first three nonzero terms ($n$ = 1, 3, 5) give **4.458** V, and the converged series **4.451** V. The series converges more slowly than for the square trough of Example 13-02.4 because the hyperbolic factors decay as $e^{-n\pi(b - y)/a}$, and here $(b - y)/a$ is only 1/4.

### Solution 13-02.8

With the image $-\rho_\ell$ at depth $h$, the field at the plane at horizontal distance $x$ from the line is normal, $E_z = -\rho_\ell h/[\pi\varepsilon_0(x^2 + h^2)]$, so $\rho_s = -\rho_\ell h/[\pi(x^2 + h^2)]$. Its peak, at $x$ = 0, is $-\rho_\ell/(\pi h)$ = **−31.83** nC/m². Integrating over $x$, $\int_{-\infty}^{\infty}h\,dx/(x^2 + h^2) = \pi$, so the total is $-\rho_\ell$ = **−1** nC/m. The force per metre is the attraction of the image line at distance $2h$: $\rho_\ell^2/(2\pi\varepsilon_0 \cdot 2h)$ = **0.8988** µN/m.

### Solution 13-02.9

$C' = \pi\varepsilon_0/\cosh^{-1}(D/2a) = \pi\varepsilon_0/\cosh^{-1}6$ = **11.23** pF/m. The thin-wire form, $\pi\varepsilon_0/\ln(D/a) = \pi\varepsilon_0/\ln 12$, gives **11.19** pF/m, **0.28**% low: at $D/2a$ = 6 the line charges sit only slightly off the wire axes.

### Solution 13-02.10

Place the corner at the origin with the planes along the axes and $Q$ at $(d, d)$. Images: $-Q$ at $(-d, d)$ (reflection in the $y$ axis), $-Q$ at $(d, -d)$ (reflection in the $x$ axis), and $+Q$ at $(-d, -d)$ (the reflection of either image in the other plane), which together make both planes equipotentials at zero. The two negative images are $2d$ away and pull along $-\hat{x}$ and $-\hat{y}$ with $kQ^2/(2d)^2$ each; the positive one is $2\sqrt2d$ away and pushes along $(\hat{x} + \hat{y})/\sqrt2$ with $kQ^2/(8d^2)$. Each component is $(kQ^2/4d^2)\,\big(-1 + 1/(2\sqrt2)\big)$ = **−14.5** µN, and the net force is **20.54** µN, directed toward the corner. (With $k = 1/(4\pi\varepsilon_0)$, $Q$ = 1 nC and $d$ = 1 cm.)

### Solution 13-02.11

(a) See §3.4: the difference $W$ of two solutions satisfies Laplace's equation with $W$ = 0 on the boundary, and $\int\lvert\nabla W\rvert^2\,dv = \oint W\nabla W\cdot d\vec{S} - \int W\nabla^2W\,dv = 0$, so $\nabla W = 0$ and $W$ = 0.

(b) In the region above the plane, the charge-plus-image potential satisfies Poisson's equation with the real charge as the only source (the image lies outside the region), is zero on the plane, and vanishes at infinity. Those are the boundary conditions of the real problem, so by (a) it is the real potential there.

(c) Images in two planes at angle α close up into a finite set only when 360°/α is an even integer (90° needs 3 images, 60° needs 5). For 120°, 360°/120° = 3 is odd: the reflections generate an image that falls inside the region of interest, which would add charge where there is none. Separation of variables in polar coordinates, or a numerical solution, is needed instead.

### Solution 13-02.12

Label the top-row nodes $p$ (left and right, equal by symmetry) and the bottom-row nodes $q$. Each node's potential is the average of its four neighbours. A top node has neighbours: the top boundary (1), its row neighbour ($p$), the node below ($q$) and the side wall (0): $4p = 1 + p + q$. A bottom node: $4q = p + q + 0 + 0$, so $q = p/3$. Substituting, $3p = 1 + p/3$, so $p$ = **0.375** V and $q$ = **0.125** V. The exact series at the same points, $(a/3, 2a/3)$ and $(a/3, a/3)$, gives **0.3807** V and **0.1193** V: the coarse grid is within 0.006 V, and both pairs sum to exactly 0.5, by the same symmetry argument as the centre value.

### Solution 13-02.13

In the dielectric, $E_\rho = V_0/[\rho\ln(b/a)]$. The energy per metre is

$$
W'_e = \frac12\int_a^b\varepsilon E_\rho^2\,2\pi\rho\,d\rho = \frac{\pi\varepsilon V_0^2}{\ln^2(b/a)}\int_a^b\frac{d\rho}{\rho} = \frac{\pi\varepsilon V_0^2}{\ln(b/a)} = \mathbf{0.4996}\ \mu\text{J/m}
$$

at 100 V, and $C' = 2W'_e/V_0^2$ = **99.92** pF/m, the value of Example 13-02.2. Units: (F/m)(V²) = J/m.

### Solution 13-02.14

The thin-wire error is $1 - \cosh^{-1}(h/a)/\ln(2h/a)$: **5.0**% at $h/a$ = 2, **0.44**% at 5, **0.084**% at 10 and **0.017**% at 20. It reaches 1% at $h/a$ = **3.61** (by root finding), so the thin-wire formula is good to 1% once the axis is about 3.6 radii above the plane.

### Solution 13-02.15

(a) Outside the sphere there is no charge, so $\nabla^2V = 0$, and the problem is symmetric about the $z$-axis, so $V$ is a sum of the separated solutions $r^nP_n(\cos\theta)$ and $r^{-(n+1)}P_n(\cos\theta)$. Far away, $V \to -E_0z = -E_0r\cos\theta$, which contains only $n = 1$; the boundary condition on the sphere must hold for every θ, so no other $n$ can enter either. Try

$$
V = \Big(Ar + \frac{B}{r^2}\Big)\cos\theta .
$$

The far field fixes $A = -E_0$; $V(a, \theta) = 0$ for all θ gives $-E_0a + B/a^2 = 0$, so $B = E_0a^3$:

$$
V = -E_0\cos\theta\,\Big(r - \frac{a^3}{r^2}\Big) .
$$

It satisfies Laplace's equation and every boundary condition, so by uniqueness it is the answer.

(b) The field at the surface is radial: $E_r = -\partial V/\partial r = E_0\cos\theta\,(1 + 2a^3/r^3)$, which is $3E_0\cos\theta$ at $r = a$. The surface charge is $\rho_s = \varepsilon_0E_r(a) = 3\varepsilon_0E_0\cos\theta$, largest at the poles: $3\varepsilon_0E_0$ = **26.56** µC/m², where the field is $3E_0$ = **3** MV/m. A rounded conductor triples the applied field at its tip; a sharper one does worse, which is why high-voltage hardware has large radii and why air breaks down first at points.

(c) $Q = \int\rho_s\,dA = 3\varepsilon_0E_0a^2\int_0^{2\pi}\!\!\int_0^\pi\cos\theta\sin\theta\,d\theta\,d\phi = 0$, because the integral of $\cos\theta\sin\theta$ over $0$ to π vanishes: the charge is only redistributed. The second term of $V$, $E_0a^3\cos\theta/r^2$, has the form of a dipole's potential $p\cos\theta/(4\pi\varepsilon_0r^2)$, so $p = 4\pi\varepsilon_0a^3E_0$ = **1.113 × 10⁻¹³** C·m.

### Solution 13-02.16

(a) By symmetry the field is radial, and Gauss's law around a cylinder of radius ρ gives $D = Q'/(2\pi\rho)$ in both layers: $D$ is normal to the interface, so it is continuous there. The field is $E = D/\varepsilon$, and integrating from the inner to the outer conductor,

$$
V = \frac{Q'}{2\pi\varepsilon_0}\Big[\frac{\ln(c/a)}{\varepsilon_{r1}} + \frac{\ln(b/c)}{\varepsilon_{r2}}\Big] ,
$$

the two layers acting as capacitors in series. With $a$ = 0.5, $c$ = 1 and $b$ = 2 mm, $C' = Q'/V$ = **107.0** pF/m.

(b) $Q' = C'V$ = 107.0 nC/m at 1 kV, so $E = Q'/(2\pi\varepsilon_0\varepsilon_r\rho)$: **0.9618** MV/m at the inner conductor; **0.4809** MV/m just inside the interface (ε_r = 4) and **0.9618** MV/m just outside it (ε_r = 2), since $D$ is continuous and ε halves; and **0.4809** MV/m at the outer conductor.

(c) Insulated throughout with $\varepsilon_r$ = 2, the cable would have its largest field at the inner conductor, $V/[a\ln(b/a)]$ = **1.443** MV/m. Grading puts the high-permittivity layer where $D$ is largest, so the field there is smaller; the field profile is flattened and the peak falls by a third for the same voltage and size. High-voltage cables and bushings grade their insulation (by permittivity, or with conducting foils) for exactly this reason: breakdown is set by the peak field, not the average.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 13-02.1a | surface charge at 2 MV/m | 17.71 | µC/m² |
| 13-02.1b | at breakdown | 26.56 | µC/m² |
| 13-02.2a | field magnitude in the glass | 2.236 | kV/m |
| 13-02.2b | angle in air | 18.4 | ° |
| 13-02.2c | angle in glass | 63.4 | ° |
| 13-02.3a | equivalent oxide thickness | 1.585 | nm |
| 13-02.3b | capacitance per area | 21.79 | fF/µm² |
| 13-02.4a | concentric spheres | 2.225 | pF |
| 13-02.4b | isolated sphere | 1.113 | pF |
| 13-02.5a | optimum inner radius | 1.839 | mm |
| 13-02.5b | maximum voltage | 5.518 | kV |
| 13-02.6a | peak field | 4.640 | MV/m |
| 13-02.6b | voltage across the region | 0.6960 | V |
| 13-02.7a | centre, one term | 4.806 | V |
| 13-02.7b | centre, three terms | 4.458 | V |
| 13-02.7c | centre, converged | 4.451 | V |
| 13-02.8a | peak surface charge | −31.83 | nC/m² |
| 13-02.8b | total induced charge | −1 | nC/m |
| 13-02.8c | force per metre | 0.8988 | µN/m |
| 13-02.9a | exact capacitance | 11.23 | pF/m |
| 13-02.9b | thin-wire capacitance | 11.19 | pF/m |
| 13-02.9c | thin-wire shortfall | 0.28 | % |
| 13-02.10a | force component along each axis | −14.5 | µN |
| 13-02.10b | net force | 20.54 | µN |
| 13-02.12a | top-row nodes | 0.375 | V |
| 13-02.12b | bottom-row nodes | 0.125 | V |
| 13-02.12c | exact at (a/3, 2a/3) | 0.3807 | V |
| 13-02.12d | exact at (a/3, a/3) | 0.1193 | V |
| 13-02.13a | stored energy per metre | 0.4996 | µJ/m |
| 13-02.13b | capacitance from energy | 99.92 | pF/m |
| 13-02.14a | error at h/a = 2 | 5.0 | % |
| 13-02.14b | error at h/a = 5 | 0.44 | % |
| 13-02.14c | error at h/a = 10 | 0.084 | % |
| 13-02.14d | error at h/a = 20 | 0.017 | % |
| 13-02.14e | h/a for 1% error | 3.61 | — |
| 13-02.15a | largest surface charge | 26.56 | µC/m² |
| 13-02.15b | largest surface field | 3 | MV/m |
| 13-02.15c | induced dipole moment | 1.113 × 10⁻¹³ | C·m |
| 13-02.16a | graded coax capacitance | 107.0 | pF/m |
| 13-02.16b | field at inner conductor | 0.9618 | MV/m |
| 13-02.16c | field inside interface | 0.4809 | MV/m |
| 13-02.16d | field outside interface | 0.9618 | MV/m |
| 13-02.16e | field at outer conductor | 0.4809 | MV/m |
| 13-02.16f | ungraded peak field | 1.443 | MV/m |
