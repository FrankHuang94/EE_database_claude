# Problems 01-10 · Multivariable Calculus II: Multiple, Line and Surface Integrals

Chapter: [01-10](../chapters/01-10-multivariable-calculus-2.md) · Worked solutions: [01-10 solutions](../solutions/01-10-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** $\mu_0 = 1.25663706\times10^{-6}$ T·m/A, $\varepsilon_0 = 8.8541878\times10^{-12}$ F/m, $1/(4\pi\varepsilon_0) = 8.98755\times10^{9}$ m/F; answers to 4 significant figures unless stated. Sketch every region before setting limits, and include the Jacobian whenever you change coordinates.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 01-10.1 [A]

(a) $\displaystyle\int_0^1\int_0^2(x + y)\,dy\,dx$  (b) $\displaystyle\int_0^1\int_0^xxy\,dy\,dx$
(c) $\displaystyle\int_0^1\int_y^1e^{x^2}\,dx\,dy$: reverse the order of integration first.

### Problem 01-10.2 [A]

Use polar coordinates.

(a) The area of the annulus $1 \le r \le 2$.
(b) $\displaystyle\iint_{x^2+y^2\le1}(x^2 + y^2)\,dA$
(c) $\displaystyle\iint_{x^2+y^2\le4}e^{-(x^2+y^2)}\,dA$

### Problem 01-10.3 [A]

(a) Find the volume of a ball of radius 2 with a spherical-coordinate integral.
(b) Find the volume of a cylinder of radius 1 and height 3 with a cylindrical-coordinate integral.
(c) Evaluate $\iiint\rho^2\,dV$ over the unit ball (ρ = distance from the origin).

### Problem 01-10.4 [A]

Compute the divergence and curl of:

(a) $\mathbf{F} = (x^2, xy, z)$, and evaluate both at (1, 2, 3);
(b) $\mathbf{G} = (-y, x, 0)$.

### Problem 01-10.5 [B]

A rectangular plate occupies $0 \le x \le 0.1$ m, $0 \le y \le 0.05$ m and carries surface charge density $\sigma(x, y) = \sigma_0(1 + x/L)$ with $\sigma_0 = 2$ nC/m² and $L = 0.1$ m. Find the total charge and the average density.

### Problem 01-10.6 [B]

A die of 8 mm × 6 mm ($0 \le x \le 8$, $0 \le y \le 6$, in mm) has power density $p(x, y) = 0.3 + 0.9e^{-x/2}$ W/mm², hottest along the edge $x = 0$ where a CPU cluster sits.

(a) Find the total power.
(b) Find the average density and the peak-to-average ratio.

### Problem 01-10.7 [B]

A Gaussian beam has intensity $I(r) = I_0e^{-2r^2/w^2}$.

(a) Show that its total power is $\tfrac{\pi}{2}I_0w^2$.
(b) What fraction of the power lies within $r = w$? Within $r = 1.5w$?
(c) A single-mode fiber has a core radius of 4.5 µm, and the light reaching it is a Gaussian beam with $w = 5.2$ µm, centered on the core. As a rough estimate, what fraction of the power falls on the core?

### Problem 01-10.8 [B]

(a) Is $\mathbf{F} = (y^2, 2xy)$ conservative? If so, find its potential and evaluate $\int\mathbf{F}\cdot d\mathbf{r}$ from (0, 0) to (2, 1).
(b) Evaluate the circulation of $\mathbf{G} = (-y, x)$ around the circle of radius 2 (counterclockwise) directly, and check it with Green's theorem.

### Problem 01-10.9 [B]

(a) In a uniform field $\mathbf{E} = (1000, 0)$ V/m, find $V_A - V_B$ for $A = (0, 0)$ and $B = (0.02, 0.01)$ m. Why does the $y$ displacement not matter?
(b) How much work does it take to bring a 1 nC charge from infinity to 1 cm from another 1 nC point charge?

### Problem 01-10.10 [B]

(a) A long wire carries 2 A. Find $\oint\mathbf{B}\cdot d\mathbf{l}$ around any loop enclosing it, and the field magnitude 1 cm away.
(b) A signal path and its return form a loop of area 10 cm × 1 cm. A nearby 50 Hz field of 10 µT peak threads the loop perpendicularly. By Faraday's law, find the peak induced voltage. Why does this break KVL for the loop, and what layout change reduces it?

### Problem 01-10.11 [B]

(a) Verify the divergence theorem for $\mathbf{F} = (x, y, z)$ over a ball of radius 2: compute both the flux and the volume integral.
(b) A 1 nC point charge sits at the center of a sphere. What is the electric flux through the sphere? Does it depend on the sphere's radius?

### Problem 01-10.12 [C]

For the charged sphere of chapter Example 01-10.5 ($\rho = \rho_0(1 - r/R)$, $\rho_0 = 10^{-6}$ C/m³, $R = 0.1$ m):

(a) Find the enclosed charge $Q(r)$ for $r \le R$.
(b) Find $E(r)$ inside the sphere with Gauss's law, and evaluate it at $r = R/2$.
(c) Find where $E$ is largest, and its maximum value. Why does the maximum lie inside the sphere?

### Problem 01-10.13 [C]

**Skin effect (a simplified model).** At high frequency, AC current crowds toward a conductor's surface. The skin depth is $\delta = \sqrt{\rho/(\pi f\mu_0)}$. For copper ($\rho = 1.72\times10^{-8}$ Ω·m), model the current density magnitude in a round wire of radius $R = 1$ mm as $J(r) = J_0e^{(r - R)/\delta}$. (The exact solution involves Bessel functions and a phase shift with depth; this model keeps only the decay.)

(a) Find δ at 100 kHz and at 1 MHz.
(b) Show that the total current is $I = 2\pi J_0\left[\delta R - \delta^2\left(1 - e^{-R/\delta}\right)\right]$, and find the "effective area" $I/J_0$ at each frequency.
(c) As a rough estimate of the AC resistance increase, find $\pi R^2/(I/J_0)$ at each frequency. What does this imply for power-converter windings and PCB traces at high frequency?

### Problem 01-10.14 [C]

**Good dies per wafer.** Combine the dies-per-wafer formula of chapter Example 01-10.3 (300 mm wafer) with a simple Poisson yield model, $Y = e^{-D_0A}$, using an illustrative defect density $D_0 = 0.1$ defects/cm².

(a) For die areas of 25, 100, 400 and 800 mm², find the gross dies per wafer, the yield and the good dies per wafer.
(b) If the wafer costs the same in each case, how does the cost per good die scale from 100 mm² to 800 mm²?
(c) Splitting an 800 mm² design into four 200 mm² chiplets: how many good chiplet sets per wafer, ignoring packaging yield and overheads? Comment.

### Problem 01-10.15 [C]

(a) Use Green's theorem to show that the area enclosed by a curve $C$ is $\tfrac{1}{2}\oint_C(x\,dy - y\,dx)$. Apply it to the ellipse $x = 3\cos t$, $y = 2\sin t$.
(b) The field $\mathbf{F} = \dfrac{(-y, x)}{x^2 + y^2}$ has zero curl everywhere except the origin, where it is undefined. Compute its circulation around the unit circle. Explain why this does not contradict Green's theorem, and what physical field it describes.

---

## Objective coverage

| Learning objective (chapter 01-10) | Problems |
|---|---|
| 1. Double and triple integrals; totals and averages | 1, 5, 6 |
| 2. Polar, cylindrical, spherical coordinates | 2, 3, 7, 12, 13, 14 |
| 3. Line integrals; conservative fields | 8, 9, 10, 15 |
| 4. Flux and Gauss's law | 11, 12, 13 |
| 5. Divergence, curl and the integral theorems | 4, 8(b), 10(b), 11, 15 |
