# Lab 18-11 · Timing Leaks, Power Analysis, PUF Keys and Glitches

Chapter: [18-11 · Hardware Security](../../chapters/18-11-hardware-security.md)

## Objective

- Recover a secret through an early-exit comparison's timing, and see a constant-time comparison stop the attack.
- Run a correlation power analysis on simulated AES first-round leakage, measure how many traces it needs, and see first-order masking defeat it.
- Size the error correction of an SRAM-PUF key and check the formula by simulation.
- Estimate a glitch attack's time with and without redundant checks.

## Background

An early-exit comparison leaks how many leading bytes match (§3.5). CPA correlates Hamming-weight predictions with measurements; the right key's correlation is $\sqrt{2/(2 + \sigma^2)}$ and about $(z/\rho)^2$ traces suffice (§3.5). A repetition code fails a bit when more than half its copies flip (§3.4). A glitch attack takes $1/(pr)$ on average (§3.6).

The simulations are deliberately idealized: the leakage is exactly the Hamming weight plus Gaussian noise, and timing is exactly proportional to the bytes compared. Real devices leak less cleanly, and real attacks need trace alignment and more measurements, but the scaling laws are the same.

## Files

- `hwsec.py`: `aes_sbox` (generated from the GF(2⁸) inverse and the affine map), `expected_guesses`, `early_exit_time`, `constant_time`, `timing_attack`, `simulate_traces`, `cpa_rank`, `theoretical_rho`, `traces_needed`, `bit_failure`, `key_failure`, `smallest_repetition`, `simulate_puf`, `expected_attempts`.
- `c/ctcompare.h` and `c/ctcompare_test.c`: constant-time and early-exit comparisons in C, with a host test that counts the bytes each examines (`python tools/run_c.py 18-11`). The test checks correctness only: the byte count is set by the loop, so it cannot show a timing leak the compiler might introduce. Timing must be checked in the generated assembly or by measurement on the target (Problem 18-11.8(b)).
- `18-11-security-lab.ipynb`: the guided notebook.

## Procedure

1. **The S-box.** Generate the AES S-box and check two entries against the standard's example: S(0x00) and S(0x53).
2. **Timing.** Predict the queries needed for a 4-byte secret at 200 measurements per guess; run `timing_attack`; then reduce the measurements to 20 and 5 and watch it fail; then attack `constant_time`.
3. **CPA.** For noise 1, 3 and 6, predict the traces needed; run `cpa_rank` with 10, 30, 100, 300 and 1000 traces and note when the true key first ranks first; then run 20 000 masked traces.
4. **PUF.** Plot key-failure probability against repetition length for $p$ = 0.05, 0.15 and 0.205; find the length for $10^{-6}$ at each; simulate one point.
5. **Glitches.** Compute the expected times of Example 18-11.5 and Problem 18-11.5.

## Expected results

- Part 1: S(0x00) = 0x63 and S(0x53) = 0xED, the values in FIPS 197.
- Part 2: the secret is recovered with 153 839 queries; with too few measurements per guess some bytes are wrong; against the constant-time comparison the result is unrelated to the secret.
- Part 3: the true key first ranks first at 30, 100 and 1000 of the tested trace counts for noise 1, 3 and 6, against predictions of about 30, 111 and 385 from $(4.5/\rho)^2$ (at noise 6 it is already second at 300); with masking it stays at a random rank even with 20 000 traces.
- Part 4: repetition lengths of 19, 47 and 75 for $p$ = 0.05, 0.15 and 0.205 (128-bit key, $10^{-6}$).
- Part 5: 1000 s and 116 days; 33.3 min and 6.34 years.

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 18-11.a | S(0x00) | 0x63 | — |
| Lab 18-11.b | S(0x53) | 0xED | — |
| Lab 18-11.c | repetition length at p = 0.15 | 47 | — |
| Lab 18-11.d | predicted traces at noise 1 | 30 | — |

## Discussion

1. Why does the timing attack need many measurements per guess, and what decides how many?
2. Why does the masked implementation's correlation stay near zero however many traces are used?
3. Why is the repetition code a poor choice for a production PUF, even though it works?

## Answers

1. Each measurement's noise is much larger than one byte's worth of time difference; averaging $m$ measurements shrinks the noise by $\sqrt m$, and the right guess must beat the largest of 255 wrong ones, so the averaged noise must be several times smaller than the one-byte difference.
2. With a fresh random mask each run, the processed value is uniformly distributed whatever the key, so the Hamming-weight leakage is statistically independent of every key hypothesis; more traces only estimate a zero correlation more precisely.
3. It spends many cells per key bit (47 at $p$ = 0.15) and, with naive helper data, can leak information about the key. Stronger codes (BCH or concatenated codes) reach the same reliability with far fewer cells, and secure-sketch constructions keep the helper data from revealing the key.

## Optional hardware

With a ChipWhisperer-class setup (a target board and a scope capturing the supply current through a shunt), record power traces of an unprotected software AES on a small MCU and run the lab's `cpa_rank` on real data; compare the traces needed with this lab's idealized estimate.
