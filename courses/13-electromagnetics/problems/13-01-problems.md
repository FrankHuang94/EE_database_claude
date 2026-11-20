# Problems 13-01 · Vector Calculus Refresher

Chapter: [13-01](../chapters/13-01-vector-calculus-refresher.md) · Worked solutions: [13-01 solutions](../solutions/13-01-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** cylindrical $(\rho, \phi, z)$, spherical $(r, \theta, \phi)$ with θ from $+z$; angles in degrees where stated; lengths in metres unless stated; $\varepsilon_0$ = 8.854 × 10⁻¹² F/m.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 13-01.1 [A]

**Cartesian to curvilinear.** Express the point $(x, y, z) = (-2, 2, 1)$ in cylindrical and spherical coordinates.

### Problem 13-01.2 [A]

**Spherical to Cartesian.** Find the Cartesian coordinates of the point $(r, \theta, \phi) = (4, 30^\circ, 210^\circ)$.

### Problem 13-01.3 [A]

**Lengths and areas.** Find the length of the arc ρ = 3 m, $z = 0$, from φ = 0 to 90°, and the area of the cap θ ≤ 30° on a sphere of radius 2 m.

### Problem 13-01.4 [B]

**A gradient in cylindrical coordinates.** For $V = 10\rho^2\sin\phi$ (V, with ρ in metres), find $\nabla V$ and its magnitude at ρ = 1 m, φ = 30°.

### Problem 13-01.5 [B]

**A divergence in cylindrical coordinates.** Find $\nabla\cdot\vec{A}$ for $\vec{A} = \rho^2\cos\phi\,\hat\rho + \rho\sin\phi\,\hat\phi$, and evaluate it at ρ = 2, φ = 0.

### Problem 13-01.6 [B]

**A curl in spherical coordinates.** Find $\nabla\times\vec{A}$ for $\vec{A} = r\sin\theta\,\hat\phi$. Express the result in Cartesian form and explain it.

### Problem 13-01.7 [B]

**Laplacians.** Find $\nabla^2V$ for $V = 1/r$ (away from the origin), $V = \ln\rho$ (away from the axis), $V = r^2$ and $V = \rho^2$.

### Problem 13-01.8 [B]

**The divergence theorem on a cylinder.** For $\vec{F} = \rho\hat\rho + z\hat{z}$, verify the divergence theorem on the cylinder ρ ≤ 1, 0 ≤ $z$ ≤ 2: find the volume integral of the divergence and the flux through each face.

### Problem 13-01.9 [B]

**Stokes's theorem on a square.** For $\vec{F} = x^2\hat{y}$, find the circulation around the unit square with corners (0, 0), (1, 0), (1, 1), (0, 1) traversed counterclockwise, and the flux of the curl through it.

### Problem 13-01.10 [B]

**Checking identities.** For $\vec{A} = xy\,\hat{x} + yz\,\hat{y} + zx\,\hat{z}$, find $\nabla\times\vec{A}$ and show that its divergence is zero. For $V = x^2y$, show that $\nabla\times\nabla V = 0$.

### Problem 13-01.11 [C]

**Gauss's law with a non-uniform charge.** A long cylinder of radius $a$ = 1 cm holds charge density $\rho_v = \rho_0\rho/a$ with $\rho_0$ = 1 µC/m³. Find $\vec{D}$ inside and outside from the integral form of Gauss's law, check it with the differential form, and find $E$ at the surface.

### Problem 13-01.12 [C]

**A point source inside a cube.** Find the flux of $\vec{F} = \hat{r}/r^2$ through the surface of a cube of side 2 centred on the origin, and through a cube of side 1 centred on (3, 0, 0). Explain the results with the divergence theorem.

---

## Objective coverage

| Learning objective (chapter 13-01) | Problems |
|---|---|
| 1. Coordinate and component conversions | 1, 2, 3 |
| 2. Operators in curvilinear coordinates | 4, 5, 6, 7 |
| 3. Divergence and Stokes theorems | 8, 9, 11, 12 |
| 4. Vector identities | 6, 10 |
| 5. Symmetry and source-free fields | 7, 11, 12 |
