# Lab 00-02 · Where Abstractions Hold and Where They Leak

**Chapter:** [00-02](../../chapters/00-02-the-abstraction-stack.md) · **Notebook:** [00-02-abstractions.ipynb](00-02-abstractions.ipynb) · **Netlist:** [tline_reflections.cir](tline_reflections.cir) · **Time:** about 45 minutes

## Objective

1. Build intuition for when wires can be treated as lumped.
2. See digital regeneration beat analog noise accumulation, in a Monte Carlo simulation of a million bits.
3. Watch the lumped abstraction fail on a transmission line, in both Python and ngspice.

## Background

Chapter sections 3.2–3.4 and Example 00-02.5 cover the background:

- **Lumped test:** a circuit is lumped if its size is less than λ/10, where $\lambda = v/f$.
- **Digital error probability:** a decision threshold a distance $d$ from the signal, with noise σ, gives error probability $p = Q(d/\sigma)$ per stage.
- **Transmission lines:** a wave reflects at each end with $\Gamma = (R - Z_0)/(R + Z_0)$.

## Procedure

1. Open the notebook and run all cells.
2. **Part 1:** use the `lumped(size, freq, v)` helper to classify five structures of your own choosing, for example a phone's internal antenna feed, a USB cable and a chip package trace.
3. **Part 2:** before running the regeneration cell with `sigma = 0.2`, predict the per-stage digital error rate and how many of 1,000,000 bits will be wrong after 10 stages. Run it and compare.
4. **Part 3:**
   - From the repository root, run `python tools/run_spice.py 00-02` and confirm that the netlist reproduces Example 00-02.5 and Problem 00-02.10.
   - Then change `RS1` in the netlist to `50` and predict the far-end waveform before running it. (Hint: what is $\Gamma_s$?)

## Expected results

| Exercise | Expected |
|---|---|
| Part 2, σ = 0.2 V: per-stage error probability | $Q(2.5) = 6.21\times10^{-3}$ |
| Part 2, σ = 0.2 V: probability of at least one error in 10 stages | 6.04%, about 60,400 of 1,000,000 bits (± about 240 from sampling) |
| Part 3, $R_s = 50\ \Omega$ | $\Gamma_s = 0$: the far end steps cleanly from 0 to 1 V at t = 1 ns, with no ringing (source termination) |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 00-02.1 | per-stage error probability, σ = 0.2 V | 6.21×10^-3 | — |
| Lab 00-02.2 | error probability over 10 stages | 6.04 | % |

## Discussion questions

1. Why does the analog histogram (Part 2) widen as $\sqrt{N}$ rather than $N$?
2. In Part 3, the slow-edge waveform overshoots by about 1.6%. Where does that small overshoot come from, given that the edge is 25 times longer than the round trip?
3. Name one product you use daily whose design must treat some wires as transmission lines, and estimate the relevant frequency.

## Optional hardware version

With a function generator, an oscilloscope and a few meters of 50 Ω coaxial cable (about 5 ns per meter), you can see real reflections:

1. Drive the cable through the generator's 50 Ω output with a fast square wave.
2. Probe the generator end, then leave the far end open.
3. You should see a step, a plateau lasting one round trip, then a second step as the reflection returns. That staircase is time-domain reflectometry in its simplest form ([13-07](../../../13-electromagnetics/chapters/13-07-transmission-lines-time-domain.md)).
