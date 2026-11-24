# Problems 21-04 · Low-Noise Amplifiers

Chapter: [21-04](../chapters/21-04-low-noise-amplifiers.md) · Worked solutions: [21-04 solutions](../solutions/21-04-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** $R_s$ = 50 Ω and $T_0$ = 290 K unless stated; $x = \gamma/\alpha$; drain (channel) noise only, no induced gate noise; ideal transistors otherwise (no $C_{gd}$, no output resistance). Problems marked *(lab)* can be checked with `labs/21-04-lab/lna.py` or `lna_noise.cir`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 21-04.1 [A]

**A terminated input with a noisy amplifier.** A 50 Ω source is terminated in 50 Ω and followed by a high-impedance amplifier whose own noise factor, referred to a 25 Ω source, is 1.5. What is the overall noise figure?

### Problem 21-04.2 [A]

**A 5.5 GHz design.** A transistor biased at $g_m$ = 30 mS has $f_T$ = 40 GHz. Design an inductively degenerated input for 50 Ω at 5.5 GHz: find $C_{gs}$, $L_s$, $L_g$, $Q_{in}$, $G_m$ and the noise figure for $x$ = 1.

### Problem 21-04.3 [B]

**The common-gate noise factor.** Derive $F = 1 + x/(g_mR_s)$ for a common-gate stage driven from $R_s$ (KCL at the source node, then the output current from the signal and from the channel noise). Evaluate it, the input impedance and the input return loss for $g_m$ = 30 mS and $x$ = 2/3. What does the extra transconductance buy and cost?

### Problem 21-04.4 [A]

**Effective transconductance.** Show that the inductively degenerated LNA's effective transconductance at resonance is $\omega_T/(2\omega_0R_s)$, independent of the device width. Evaluate it at 2.4 GHz for $f_T$ = 12 GHz and 24 GHz.

### Problem 21-04.5 [B] *(lab)*

**How good must the gate inductor be?** For Example 21-04.2's LNA, what gate-inductor Q keeps the noise figure at 0.8 dB, with the input re-matched?

### Problem 21-04.6 [B]

**Gate loss, derived.** Derive the noise factor of the re-matched LNA with a series gate loss $r_g$ (§3.5), and evaluate it for $r_g$ = 5 Ω in Example 21-04.2's design. How far off is the shortcut that simply adds $r_g/R_s$ to the lossless result?

### Problem 21-04.7 [B]

**A linearity budget.** A device reaches its third-order intercept at a gate–source amplitude of 0.25 V. What is the LNA's input-referred IIP3 (available power from 50 Ω) if $Q_{in}$ = 2? What is the largest $Q_{in}$ that keeps IIP3 at or above −10 dBm?

### Problem 21-04.8 [B]

**Gain for a noisier mixer.** An LNA with a 1.5 dB noise figure drives a mixer with a 12 dB noise figure. What LNA gain keeps the cascade within 0.2 dB of the LNA? What is the cascade noise figure with 25 dB of gain?

### Problem 21-04.9 [B]

**Sizing a noise-cancelling LNA.** With $R_2$ = 300 Ω and $x$ = 1 (a short-channel device), what $g_{m2}$ gives a 1.0 dB noise figure at the cancelling condition? What drain current does that take at $g_m/I_D$ = 10 S/A?

### Problem 21-04.10 [C] *(lab)*

**Imperfect cancellation.** For Example 21-04.5's LNA, derive the noise factor for any $R_1$ (not just the cancelling value) and evaluate it for $R_1$ = 900 Ω, 1000 Ω and 1100 Ω. Find the $R_1$ that minimizes the noise figure in this model and explain why it is not the cancelling value. Why do real designs stay near cancellation anyway?

### Problem 21-04.11 [B] *(lab)*

**The input match's bandwidth.** For Example 21-04.2's design, find the band over which the input return loss is at least 10 dB.

### Problem 21-04.12 [C]

**On chip or off?** A 5.8 GHz LNA uses a device with $g_m$ = 25 mS and $f_T$ = 30 GHz, and must reach NF ≤ 1.5 dB ($x$ = 1). Does an on-chip gate inductor with $Q$ = 12 meet the target, with the input re-matched? What does an off-chip inductor with $Q$ = 40 give, and what would a lossless one give?

### Problem 21-04.13 [B]

**The LNA in its receiver.** Example 21-04.3's LNA with $Q_L$ = 15 (NF 1.01 dB) has 20 dB of gain and, from Example 21-04.4, an IIP3 of −8.42 dBm. It drives a mixer with 10 dB gain, a 10 dB noise figure and IIP3 = +5 dBm. Find the cascade noise figure and IIP3 (21-03).

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Resistive termination and the common-gate stage | 1, 3 |
| 2. Inductively degenerated LNA: match, $G_m$, noise | 2, 4, 11 |
| 3. Gate-inductor loss, Q, gain and linearity | 5, 6, 7, 12 |
| 4. Noise-cancelling wideband LNA | 9, 10 |
| 5. LNA gain from the following stage; LNA in a receiver | 8, 13 |
