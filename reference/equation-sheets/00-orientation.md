# Equation Sheet · 00 Orientation

The relations to know cold from Course 00, each with its conditions and where it is derived.

## Energy, power and information

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $p = vi$ (W = V·A) | Power absorbed under the passive sign convention | [00-01](../../courses/00-orientation/chapters/00-01-map-of-electrical-engineering.md) |
| Energy (Wh) = capacity (Ah) × voltage (V); 1 Wh = 3600 J; 1 mAh = 3.6 C | Nominal-voltage approximation for batteries | [00-01](../../courses/00-orientation/chapters/00-01-map-of-electrical-engineering.md) |
| $P = E_b R_b$ | Energy per bit × data rate | [00-01](../../courses/00-orientation/chapters/00-01-map-of-electrical-engineering.md) |
| $E_{min} = kT\ln 2$ ($2.87\times10^{-21}$ J at 300 K) | Landauer: minimum energy to erase one bit | [00-01](../../courses/00-orientation/chapters/00-01-map-of-electrical-engineering.md) |
| $C = B\log_2(1 + \text{SNR})$ | Shannon capacity of an AWGN channel; SNR as a power ratio | [00-01](../../courses/00-orientation/chapters/00-01-map-of-electrical-engineering.md) |
| $\text{ratio} = 10^{\text{dB}/10}$ (power) | Decibel conversion | [00-01](../../courses/00-orientation/chapters/00-01-map-of-electrical-engineering.md) |

## Abstractions and their limits

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\lambda = v/f$; $v = c/\sqrt{\varepsilon_r}$ | Wave speed in a material; $v \approx c/2$ on FR-4 | [00-02](../../courses/00-orientation/chapters/00-02-the-abstraction-stack.md) |
| Lumped if $\ell < \lambda/10$, or line delay $< t_r/6$ | Rules of thumb (authors vary between $t_r/4$ and $t_r/10$) | [00-02](../../courses/00-orientation/chapters/00-02-the-abstraction-stack.md) |
| $NM_L = V_{IL} - V_{OL}$, $NM_H = V_{OH} - V_{IH}$ | Static discipline: $V_{OL} < V_{IL} < V_{IH} < V_{OH}$ | [00-02](../../courses/00-orientation/chapters/00-02-the-abstraction-stack.md) |
| Analog chain: $\sigma_{tot} = \sigma\sqrt{N}$ | Independent noise adds in variance | [00-02](../../courses/00-orientation/chapters/00-02-the-abstraction-stack.md) |
| Digital chain: $p = Q(d/\sigma)$ per stage; $P_{any} = 1 - (1-p)^N \approx Np$ | Gaussian noise, regenerating stages | [00-02](../../courses/00-orientation/chapters/00-02-the-abstraction-stack.md) |
| $\Gamma = (R - Z_0)/(R + Z_0)$; launched wave $= V Z_0/(R_s + Z_0)$ | Lossless line; open end doubles the incident wave | [00-02](../../courses/00-orientation/chapters/00-02-the-abstraction-stack.md) |

## Numerical tools and checks

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $x_{k+1} = x_k - g(x_k)/g'(x_k)$ | Newton–Raphson; quadratic convergence near the root | [00-04](../../courses/00-orientation/chapters/00-04-toolchain-walkthrough.md) |
| $\varepsilon = 2^{-52} \approx 2.22\times10^{-16}$ | Double-precision machine epsilon | [00-04](../../courses/00-orientation/chapters/00-04-toolchain-walkthrough.md) |
| $2^n$ test vectors for $n$ input bits | Exhaustive testing of combinational logic | [00-04](../../courses/00-orientation/chapters/00-04-toolchain-walkthrough.md) |
| Ω·F = s; H/Ω = s; $1/\sqrt{\text{H·F}}$ = 1/s; V²/Ω = W | Dimensional checks | [00-03](../../courses/00-orientation/chapters/00-03-how-to-study-this-curriculum.md) |

## Project risk

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $P(\text{all } n \text{ blocks OK}) = p^n$ | Independent blocks (an optimistic model) | [00-05](../../courses/00-orientation/chapters/00-05-how-chip-companies-are-organized.md) |
| Triangular mean $= (a + m + b)/3$ | Means add across sequential phases | [00-05](../../courses/00-orientation/chapters/00-05-how-chip-companies-are-organized.md) |
| Wafer cycle time ≈ (mask layers) × (1–1.5 days) | Industry rule of thumb ([R-020](../research-log.md#r-020--fab-cycle-time-and-maskeuv-layer-counts)) | [00-05](../../courses/00-orientation/chapters/00-05-how-chip-companies-are-organized.md) |
