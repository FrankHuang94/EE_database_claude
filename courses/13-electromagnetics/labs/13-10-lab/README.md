# Lab 13-10 · Waveguides and Resonators

Chapter: [13-10 Waveguides and Resonators](../../chapters/13-10-waveguides-and-resonators.md)

## Objective

Visualize waveguide modes, quantify a waveguide's dispersion, confirm cutoffs with a numerical eigen-solve, size below-cutoff vents, and compute a single-mode fibre's fundamental mode. Then model a cavity resonator as a parallel RLC in ngspice.

## Background

TE modes and cutoff (§3.1), propagation above cutoff (§3.2), evanescent guides (§3.3), cavities (§3.4) and optical fibre (§3.5).

## Files

- [13-10-waveguides.ipynb](13-10-waveguides.ipynb): the notebook (Parts 1–4).
- [cavity_rlc.cir](cavity_rlc.cir): Example 13-10.5's cavity near TE₁₀₁ as a parallel RLC, swept around 9.27 GHz. Run with `ngspice -b cavity_rlc.cir`, or `python tools/run_spice.py 13-10` from the repository root.

## Procedure

1. **Mode patterns (Part 1).** Plot TE₁₀, TE₂₀ and TE₁₁ over the cross-section. *Predict first:* where is TE₁₀ strongest?
2. **Dispersion (Part 2).** Plot the group delay of 1 m of WR-90 across 7 to 13 GHz.
3. **Eigen-solve and below cutoff (Part 3).** Solve the cross-section numerically and compare the cutoffs; plot a 5 mm tube's attenuation against frequency.
4. **Fibre (Part 4).** Solve the LP₀₁ condition, plot $b(V)$ and the 1310 nm field, and check single-mode operation at 1260 nm.
5. **ngspice (the chapter's guided exercise).** Predict the resonance and the bandwidth, then run `cavity_rlc.cir`.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | Patterns | TE₁₀ peaks at the centre and vanishes at the side walls; TE₂₀ has two lobes |
| 2 | Group delay | 5.555 ns at 8.2 GHz, 3.930 ns at 12.4 GHz for 1 m |
| 3 | Cutoffs | Grid within about 0.01% of the formula; 5.44 dB/mm below cutoff at 2.4 GHz |
| 4 | Fibre | V = 2.385 at 1260 nm (single-mode); b = 0.5029 at 1310 nm |
| ngspice | Cavity | 9.273 GHz and Q ≈ 7838 |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 13-10.a | group-delay difference over 1 m of WR-90, 8.2 to 12.4 GHz | 1.625 | ns |
| Lab 13-10.b | fibre V-number at 1260 nm | 2.385 | — |
| Lab 13-10.c | group delay through 1 m of WR-90 at 8.2 GHz | 5.555 | ns |
| Lab 13-10.d | group delay through 1 m of WR-90 at 12.4 GHz | 3.930 | ns |

*These are recomputed by [verify_13_10.py](../../verify/verify_13_10.py) from its numerically found cutoff and the fibre parameters.*

## Discussion questions

1. Why does the group delay rise steeply toward cutoff?
2. Why does a coarse finite-difference grid reproduce the TE₁₀ cutoff almost exactly but the higher modes less well?
3. Why is the cavity's behaviour near resonance captured by a parallel RLC?

### Answers

1. The group velocity is $c\sqrt{1 - (f_c/f)^2}$, which goes to zero at cutoff: the two bouncing plane waves strike the walls almost perpendicularly and make little progress along the guide, so energy takes ever longer to traverse it.
2. The discretization error of the Laplacian falls as the inverse square of the number of grid cells per half-wave: TE₁₀ varies slowly across many cells, while TE₂₀ and TE₁₁ vary twice as fast (and TE₀₁ across the shorter dimension), so each sees fewer cells per variation and a larger error.
3. Near one resonance the cavity stores energy alternately in electric and magnetic fields, like C and L, and loses a fixed fraction per cycle in its walls, like R. Its impedance seen through a coupling port is that of a single resonant mode, which has the same frequency response as a parallel RLC with the same $f_0$ and Q; other modes are far away in frequency and contribute only small reactances.

## Optional hardware extension

Measure a section of WR-90 (or any rectangular waveguide with coax adapters) with a vector network analyzer from below to above its cutoff, and watch the transmission appear abruptly at $c/2a$. Then measure a cavity filter's response and estimate its Q from the 3 dB bandwidth.
