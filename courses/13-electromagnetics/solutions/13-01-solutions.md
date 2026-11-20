# Solutions 13-01 · Vector Calculus Refresher

Problems: [13-01 problems](../problems/13-01-problems.md) · Chapter: [13-01](../chapters/13-01-vector-calculus-refresher.md). Every number below is recomputed by [verify_13_01.py](../verify/verify_13_01.py), which differentiates in Cartesian coordinates with sympy and integrates numerically rather than reusing these formulas.

---

## Solutions

### Solution 13-01.1

$\rho = \sqrt{4 + 4}$ = **2.828**, $\phi = \operatorname{atan2}(2, -2)$ = **135**°, $z$ = 1. $r = \sqrt{4 + 4 + 1}$ = **3**, $\theta = \arccos(1/3)$ = **70.53**°, φ = 135°. Note that atan2 puts φ in the second quadrant; $\arctan(y/x)$ alone would give −45°.

### Solution 13-01.2

$x = 4\sin 30^\circ\cos 210^\circ$ = **−1.732**, $y = 4\sin 30^\circ\sin 210^\circ$ = **−1**, $z = 4\cos 30^\circ$ = **3.464**.

### Solution 13-01.3

The arc is $\int\rho\,d\phi = 3 \times \pi/2$ = **4.712** m. The cap is $\int_0^{2\pi}\int_0^{\pi/6}R^2\sin\theta\,d\theta\,d\phi = 2\pi R^2(1 - \cos 30^\circ)$ = **3.367** m².

### Solution 13-01.4

$\nabla V = \partial_\rho V\,\hat\rho + \frac1\rho\partial_\phi V\,\hat\phi = 20\rho\sin\phi\,\hat\rho + 10\rho\cos\phi\,\hat\phi$. At the point, $\nabla V$ = **10** $\hat\rho$ + **8.660** $\hat\phi$ V/m, with magnitude **13.23** V/m.

### Solution 13-01.5

$\nabla\cdot\vec{A} = \frac1\rho\partial_\rho(\rho^3\cos\phi) + \frac1\rho\partial_\phi(\rho\sin\phi) = 3\rho\cos\phi + \cos\phi$, which is **7** at ρ = 2, φ = 0.

### Solution 13-01.6

$$
\nabla\times\vec{A} = \frac{1}{r\sin\theta}\partial_\theta(r\sin^2\theta)\,\hat{r} - \frac1r\partial_r(r^2\sin\theta)\,\hat\theta = 2\cos\theta\,\hat{r} - 2\sin\theta\,\hat\theta .
$$

Since $\hat{z} = \cos\theta\,\hat{r} - \sin\theta\,\hat\theta$, this is $2\hat{z}$, of magnitude **2** everywhere. The field is $r\sin\theta\,\hat\phi = \rho\hat\phi$, a rigid rotation about $z$, whose curl is twice the angular rate, the same in any coordinates.

### Solution 13-01.7

$\frac{1}{r^2}\partial_r(r^2 \cdot (-1/r^2)) = 0$ and $\frac1\rho\partial_\rho(\rho \cdot 1/\rho) = 0$: both are **0** away from their singularities. For $r^2$: $\frac{1}{r^2}\partial_r(2r^3)$ = **6**. For $\rho^2$: $\frac1\rho\partial_\rho(2\rho^2)$ = **4**. (In Cartesian form $r^2 = x^2 + y^2 + z^2$ gives 2 + 2 + 2 and $\rho^2$ gives 2 + 2: a check.)

### Solution 13-01.8

$\nabla\cdot\vec{F} = \frac1\rho\partial_\rho(\rho^2) + 1 = 3$, so the volume integral is $3 \times \pi \times 1^2 \times 2$ = **18.85**. Side (ρ = 1): $F_\rho = 1$ over $2\pi \times 1 \times 2$, flux **12.57**. Top ($z$ = 2): $F_z = 2$ over π, flux **6.283**. Bottom ($z$ = 0): $F_z$ = 0, flux **0**. Total 18.85.

### Solution 13-01.9

Only the edges along $y$ contribute ($\vec{F}$ has no $x$-component): up along $x$ = 1 gives $\int_0^1 1\,dy = 1$; down along $x = 0$ gives 0. Circulation **1**. The curl is $\partial_x(x^2)\hat{z} = 2x\hat{z}$, whose flux is $\int_0^1\int_0^1 2x\,dx\,dy$ = **1**.

### Solution 13-01.10

$\nabla\times\vec{A} = (0 - y)\hat{x} + (0 - z)\hat{y} + (0 - x)\hat{z} = -y\hat{x} - z\hat{y} - x\hat{z}$; its divergence is $0 + 0 + 0$ = **0**. For $V = x^2y$, $\nabla V = (2xy, x^2, 0)$ and $\nabla\times\nabla V = (0, 0, 2x - 2x)$ = **0**.

### Solution 13-01.11

Inside, the charge per unit length within radius ρ is $\int_0^\rho(\rho_0\rho'/a)2\pi\rho'\,d\rho' = 2\pi\rho_0\rho^3/(3a)$; dividing by the side area $2\pi\rho$ per unit length gives $D_\rho = \rho_0\rho^2/(3a)$. Outside, $D_\rho = \rho_0a^2/(3\rho)$. Check: $\frac1\rho\partial_\rho(\rho \cdot \rho_0\rho^2/(3a)) = \rho_0\rho/a$ inside and $\frac1\rho\partial_\rho(\rho_0a^2/3) = 0$ outside. At the surface $D$ = **3.333 × 10⁻⁹** C/m² and $E = D/\varepsilon_0$ = **376.5** V/m.

### Solution 13-01.12

The first cube encloses the origin, where $\nabla\cdot\vec{F} = 4\pi\delta^3(\vec{r})$, so the flux is **12.57** (4π), the same as through any sphere around the origin. The second cube excludes the origin; $\vec{F}$ is source-free inside it, so the flux is **0**: what enters one face leaves through the others.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 13-01.1a | ρ | 2.828 | — |
| 13-01.1b | φ | 135 | ° |
| 13-01.1c | r | 3 | — |
| 13-01.1d | θ | 70.53 | ° |
| 13-01.2a | x | −1.732 | — |
| 13-01.2b | y | −1 | — |
| 13-01.2c | z | 3.464 | — |
| 13-01.3a | arc length | 4.712 | m |
| 13-01.3b | cap area | 3.367 | m² |
| 13-01.4a | ρ-component | 10 | V/m |
| 13-01.4b | φ-component | 8.660 | V/m |
| 13-01.4c | magnitude | 13.23 | V/m |
| 13-01.5a | divergence at the point | 7 | — |
| 13-01.6a | magnitude of the curl | 2 | — |
| 13-01.7a | Laplacian of 1/r and ln ρ | 0 | — |
| 13-01.7b | Laplacian of r² | 6 | — |
| 13-01.7c | Laplacian of ρ² | 4 | — |
| 13-01.8a | volume integral | 18.85 | — |
| 13-01.8b | side flux | 12.57 | — |
| 13-01.8c | top flux | 6.283 | — |
| 13-01.8d | bottom flux | 0 | — |
| 13-01.9a | circulation | 1 | — |
| 13-01.9b | flux of the curl | 1 | — |
| 13-01.10a | divergence of the curl | 0 | — |
| 13-01.10b | curl of the gradient | 0 | — |
| 13-01.11a | D at the surface | 3.333 × 10⁻⁹ | C/m² |
| 13-01.11b | E at the surface | 376.5 | V/m |
| 13-01.12a | flux through the centred cube | 12.57 | — |
| 13-01.12b | flux through the offset cube | 0 | — |
