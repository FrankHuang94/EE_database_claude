# Lab 13-01 · Vector Calculus Refresher

Chapter: [13-01 Vector Calculus Refresher](../../chapters/13-01-vector-calculus-refresher.md)

## Objective

See curvilinear unit vectors turn from point to point; derive the gradient, divergence, curl and Laplacian in cylindrical and spherical coordinates from scale factors with a computer-algebra system and check them; verify the divergence and Stokes theorems on two surfaces each; and expose the delta function hidden in the inverse-square field.

## Background

Coordinate systems and scale factors (§3.1), the operators (§3.2–3.5), the integral theorems and the delta function (§3.6).

## Files

- [13-01-vector-calculus.ipynb](13-01-vector-calculus.ipynb): the notebook (Parts 1–4).

## Procedure

1. **Unit vectors (Part 1).** Plot $\hat\rho$ and $\hat\phi$ at eight points on a circle.
2. **Operators (Part 2).** Implement the general orthogonal-coordinate formulas once and apply them to $r^n\hat r$, $r\sin\theta\,\hat\phi$, $1/r$, $\ln\rho$ and the dipole potential; then build fields in Cartesian form, differentiate there, project onto the spherical unit vectors and confirm that the differences are zero.
3. **Theorems (Part 3).** Compute both sides of the divergence theorem on spheres of radius 1 and 2 and on a cube, and the flux of the curl of $(\rho + z)\hat\phi$ through a flat disc and through a cone over the same circle (different integrands, the same circulation).
4. **Delta function (Part 4, the chapter's guided exercise).** *Predict first:* the flux of $\hat r/r^2$ through spheres of radius 0.01 and 100. Then run it, and integrate the field's divergence on a grid over a cube while leaving out a shrinking ball around the origin: the integral stays near zero while the flux out of the cube stays 4π.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Unit vectors | Rotate with φ; orthogonal at every point |
| 2 | Operators | $(n + 2)r^{n-1}$; $2\cos\theta\,\hat r - 2\sin\theta\,\hat\theta$; zero Laplacians; the dipole field |
| 3 | Theorems | Both sides equal for each surface |
| 4 | Flux of $\hat r/r^2$ | The same for every radius |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 13-01.a | flux through the sphere of radius 0.01 | 12.57 | — |
| Lab 13-01.b | flux through the sphere of radius 100 | 12.57 | — |

*These are recomputed by [verify_13_01.py](../../verify/verify_13_01.py) by surface quadrature of the Cartesian field.*

## Discussion questions

1. Why must the scale factors stay inside the derivatives in the divergence?
2. Why does every surface spanning the same loop carry the same flux of a curl?
3. If the divergence of $\hat r/r^2$ is zero everywhere except the origin, where does the flux come from?

### Answers

1. The face areas of a curvilinear cell change across the cell; the flux difference between opposite faces includes that change.
2. The curl has zero divergence, so by the divergence theorem the net flux through the closed surface formed by two such surfaces is zero.
3. From the origin itself: the divergence there is $4\pi\delta^3(\vec r)$, a point source of total strength $4\pi$.
