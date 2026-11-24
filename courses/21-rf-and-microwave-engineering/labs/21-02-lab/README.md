# Lab 21-02 · Matching Networks: Q, Sections, Transformers and Loss

Chapter: [21-02 · Impedance Matching Networks](../../chapters/21-02-impedance-matching-networks.md)

## Objective

- Design L, π and multi-section matches and measure their 10 dB return-loss bandwidths, in Python and in ngspice.
- Compare a one-section, two-section and binomial transformer, and see how close the small-reflection theory is.
- Count the loss that finite component Q adds, and find the number of sections that minimizes it.
- Check a requested bandwidth against the Bode–Fano limit.

## Background

`match.py` contains `l_match`, `pi_match`, `cascade_l`, `binomial_transformer` and `binomial_bandwidth`, `zin_ladder` (input impedance of a ladder of series and shunt elements, with optional component Q, or of line sections) and `bode_fano_bw`. `matchnets.cir` drives three networks from 50 Ω sources into their design loads and measures where the return loss crosses 10 dB: the L-match of Example 21-02.1, the π network of Example 21-02.3 and the two-section match of Example 21-02.4.

## Procedure

1. **One L-section.** *Predict* the bandwidth of Example 21-02.1 from its Q, then sweep its return loss (Part 1).
2. **Q on purpose.** Sweep π networks with Q from 2 to 10 between 50 Ω and 10 Ω and plot bandwidth against Q (Part 2).
3. **Sections.** Compare one, two and three L-sections from 5 Ω to 50 Ω; then run `ngspice -b matchnets.cir` (Part 3).
4. **Transformers.** Plot the reflection of one-, two- and three-section binomial transformers from 50 Ω to 100 Ω, computed exactly, against the small-reflection estimate (Part 4).
5. **Loss and limits.** Add inductor Q from 5 to 100 to Example 21-02.1's network and plot the loss; tabulate total loss against the number of sections for 2 Ω to 50 Ω; compare the bandwidths found with the Bode–Fano limit of a 50 Ω ∥ 1 pF load (Part 5).

## Expected results

- **Part 1.** The 10 dB band runs from 1.901 to 2.812 GHz, about 0.76/Q in fractional terms.
- **Part 2.** Bandwidth falls roughly as 1/Q.
- **Part 3.** One section: 23.6%; two: 70.5%; three wider still. ngspice gives the same six band edges as Examples 21-02.1, 21-02.3 and 21-02.4.
- **Part 4.** The exact transformer bandwidths are a point or so below the small-reflection estimates (18.1% against 19.2% for one section, 49.1% against 50.6% for two).
- **Part 5.** The loss follows $10\log_{10}(1 + Q_n/Q_u)$; for 2 Ω to 50 Ω with $Q_u$ = 20, two sections minimize the total loss (0.83 dB).

## Discussion

1. **Why is the transformer bandwidth slightly below the small-reflection estimate?** The estimate keeps only single reflections at each step; the multiple reflections between steps narrow the band a little.
2. **Why does adding sections eventually increase loss?** Each section adds a lossy inductor; once each section's Q is small, the number of inductors dominates.
3. **Can any network beat Bode–Fano?** No lossless network can; a lossy one can by absorbing power, which is not a match but an attenuator.

## Optional hardware

With a hobbyist vector network analyzer and 0603 surface-mount parts on a small board, build the 25 Ω-to-50 Ω L-match of Problem 21-02.1 at a few hundred megahertz (scale L and C up for the lower frequency), terminate it in two parallel 51 Ω resistors, and measure its return loss over frequency. Compare the band with the prediction, and note how the parts' parasitics shift the center.
