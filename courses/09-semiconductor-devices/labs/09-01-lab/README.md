# Lab 09-01 · Crystals, Energy Bands and the Semiconductor

**Chapter:** [09-01](../../chapters/09-01-crystals-and-energy-bands.md) · **Notebook:** [09-01-bands.ipynb](09-01-bands.ipynb) · **Time:** about 2 hours

## Objective

1. Build the diamond lattice from its FCC lattice and two-atom basis, and recover atomic and planar densities and bond lengths by counting, with no formula assumed.
2. Compute Kronig–Penney bands from the transfer matrix of one period of the Schrödinger equation, and extract effective masses by fitting the computed bands.
3. Watch the bands go from free electrons to isolated-well levels as the barriers strengthen.
4. Reproduce silicon's conductivity and density-of-states masses and its $N_C$ and $N_V$ from the valley masses.
5. Explore band gaps against temperature (Varshni) and composition (Ga$_{1-y}$In$_y$As with Vegard's law).

## Background

Chapter sections 3.1–3.8 and Examples 09-01.1 to 09-01.6. The tool that does the work is the **transfer matrix**: across one period, the pair $(\psi, \psi')$ is multiplied by a 2 × 2 matrix $\mathbf{T}(E)$, and a Bloch wave exists only where $\cos kd = \tfrac12\operatorname{tr}\mathbf{T}$ lies between −1 and 1 (chapter §3.3, "Math refresher"). For a delta-function barrier, $\psi$ is continuous and $\psi'$ jumps by $(2P/d)\psi$. You need Python with NumPy, SciPy and Matplotlib (see [SETUP.md](../../../../SETUP.md)).

## Files

| File | What it does | Checks against |
|---|---|---|
| [09-01-bands.ipynb](09-01-bands.ipynb) | The guided notebook (Parts 1 to 5) | Its own `assert`s, which compare with Examples 09-01.1, .3, .4 and .6 |

## Procedure

1. **The lattice (Part 1).** *Predict first:* atoms per cubic cell, number of nearest and second-nearest neighbors, and the bond length in silicon. Then count, and compute the (100), (110) and (111) planar densities by counting atoms inside an in-plane parallelogram.
2. **The bands (Part 2).** *Predict first:* for Example 09-01.3 ($P$ = 3, $d$ = 0.5 nm), where does band 1 start and end? Then compute $\tfrac12\operatorname{tr}\mathbf{T}(E)$, find the band edges with a root finder, plot the $E$–$k$ diagram and fit the band-bottom mass.
3. **Barrier strength (Part 3, the chapter's guided exercise).** *Predict first:* doubling $P$ from 3 to 6, does band 1 get wider or narrower, does the first gap get wider or narrower, and does the band-bottom mass rise or fall? Write down a number for the new mass. Then run the sweep from $P$ ≈ 0 to $P$ = 24.
4. **Silicon's masses (Part 4).** *Predict first:* which is larger, the conductivity mass or the density-of-states mass, and by roughly what factor? Then build the six valleys as inverse-mass tensors and compute $N_C$ by integrating the density of states against the Boltzmann factor.
5. **Gaps (Part 5).** *Predict first:* how much does silicon's gap change between 77 K and 300 K, and which indium fraction of GaInAs matches InP? Then plot both.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | lattice | 8 atoms per cell; 4 nearest neighbors at 2.352 Å and 12 second neighbors at 3.840 Å; densities as in Example 09-01.1 |
| 2 | bands, $P$ = 3 | band 1 from 0.5953 to 1.504 eV, band 2 from 2.883 to 6.016 eV; fitted $m^*$ = 1.125 $m_0$ |
| 3 | barrier sweep | see the answer key: band 1 narrows, the gap widens and the mass rises |
| 4 | silicon | $m_c$ = 0.2598, $m_{dn}$ = 1.084, $m_{dp}$ = 0.5492 $m_0$; $N_C$ = 2.832 × 10¹⁹, $N_V$ = 1.021 × 10¹⁹ cm⁻³ |
| 5 | gaps | Si 1.1245 eV and GaAs 1.4225 eV at 300 K; lattice match at $y$ = 0.5344 |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 09-01.a | band 1 width, P = 3 | 0.909 | eV |
| Lab 09-01.b | band 1 width, P = 6 | 0.637 | eV |
| Lab 09-01.c | first gap, P = 6 | 2.172 | eV |
| Lab 09-01.d | band-bottom mass, P = 6 | 1.359 | m0 |
| Lab 09-01.e | band 1 width, P = 12 | 0.394 | eV |
| Lab 09-01.f | first gap, P = 12 | 2.994 | eV |
| Lab 09-01.g | band-bottom mass, P = 12 | 1.908 | m0 |
| Lab 09-01.h | band 1 width change, P = 3 to 6 | -30 | % |
| Lab 09-01.i | mass change, P = 3 to 6 | 21 | % |
| Lab 09-01.j | second-neighbor distance in Si | 3.840 | Å |

## Discussion questions

1. Part 1 counts atoms inside a parallelogram rather than a circle. Why does that give an exact planar density, while counting inside a large circle only converges slowly?
2. In Part 2, the closed-form Kronig–Penney relation and the transfer-matrix half-trace give identical curves. Why must they?
3. In Part 3, doubling $P$ narrows band 1 by 30% but raises the mass by only 21%. Why is the mass less sensitive than the width at moderate $P$, and how do the two behave for very large $P$?
4. In Part 4, the conductivity mass uses a harmonic mean of valley masses and the density-of-states mass a sum of square roots of determinants. Explain each choice in a sentence.
5. Why can a one-dimensional model with one adjustable number explain gaps, effective masses and holes, yet not predict whether a real material's gap is direct or indirect?

<details><summary>Answers to the discussion questions</summary>

1. Two lattice vectors in the plane tile it exactly with copies of one parallelogram, so the atoms inside one copy (counting each boundary atom once, via the half-open interval) are exactly the atoms per tile. A circle cuts through the lattice irregularly, so the count fluctuates with the boundary and the error falls only as perimeter over area, about $1/R$.
2. Both describe the same physics: the closed form is just $\tfrac12\operatorname{tr}\mathbf{T}$ multiplied out algebraically. For the delta comb, $\mathbf{T} = \mathbf{K}\mathbf{F}$ with $\mathbf{F}$ the free-propagation matrix and $\mathbf{K}$ the slope kick, and the trace of that product is $2\cos x + (2P/x)\sin x$. The numerical product avoids the algebra, which is why it extends easily to any barrier shape.
3. The mass is set by the curvature at the band bottom, $m^*/m_0 = -F'(x_b)/x_b$. As $P$ rises, $F'$ steepens but $x_b$ also rises toward $\pi$, and the two partly cancel; the width, by contrast, shrinks directly as $x_b$ approaches $\pi$. For very large $P$ both scale with $1/P$: width $\approx 4\pi^2E_d/P$ (Problem 09-01.7) and $m^* \propto P$.
4. Conductivity: what adds is the *response* (acceleration per unit force, $1/m$) of each valley, so inverse masses are averaged. Density of states: what adds is the *number of states* below a given energy, proportional to the $k$-space volume of each valley's ellipsoid, $\propto\sqrt{m_xm_ym_z}$, so square roots of determinants are summed.
5. In one dimension there is only one direction of $k$, so there is nothing to be indirect *across*. Whether the conduction minimum sits at Γ, X or L depends on the full three-dimensional crystal potential and on which atomic orbitals form each band; it needs a three-dimensional band calculation.

</details>

## Optional extension

Replace the delta barrier with a finite square barrier (width $b$, height $V_0$): the transfer matrix over a barrier is the free-propagation matrix with $\alpha$ replaced by $j\beta$, i.e. $\cosh$ and $\sinh$ in place of $\cos$ and $\sin$. Check that, as $b \to 0$ with $V_0b$ fixed, the band edges converge to the delta-comb values of Part 2.
