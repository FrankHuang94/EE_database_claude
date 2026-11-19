# Problems 10-08 · Current Sources and Current Mirrors

Chapter: [10-08](../chapters/10-08-current-sources-and-mirrors.md) · Worked solutions: [10-08 solutions](../solutions/10-08-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** square-law MOSFETs, $r_o = 1/(\lambda I_D)$, matched devices unless stated, body effect ignored unless $g_{mb}$ is given; bipolar mirrors with $V_{BE}$ = 0.7 V; $A_{VT}$ = 3.5 mV·µm (illustrative) where needed.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 10-08.1 [A]

**Ratios.** (a) An NMOS mirror has a reference transistor of $W/L$ = 10/1 carrying 50 µA and an output transistor of 30/1 (λ = 0). Find the output current. (b) That current is the reference of a PMOS mirror with a 1:2 ratio. What current does the PMOS output source?

### Problem 10-08.2 [A]

**Headroom on 1.2 V.** NMOS and PMOS transistors have $V_{ov}$ = 0.25 V and $|V_{TH}|$ = 0.45 V. (a) Find the compliance of a basic mirror, a simple cascode mirror and a low-voltage cascode mirror. (b) A stage's output node is loaded by a basic NMOS mirror below and a basic PMOS mirror above. How much output swing is left on a 1.2 V supply? (c) What if the NMOS mirror is a simple cascode?

### Problem 10-08.3 [A]

**A scaled bipolar mirror.** A bipolar mirror's output transistor has three times the emitter area of the reference transistor; β = 80 and $I_{ref}$ = 1 mA. Show that $I_{out} = 3I_{ref}/(1 + 4/\beta)$ and evaluate it.

### Problem 10-08.4 [B]

**Channel length against error.** A process has λ = 0.1 V⁻¹ at $L$ = 0.5 µm, with λ ∝ 1/L. (a) Find λ at 2 µm. (b) Find the basic mirror's error for a 1 V drain-voltage difference at each length. (c) To keep the same current and overdrive at the longer length, by what factor must $W$ grow, and the gate area?

### Problem 10-08.5 [B]

**Degeneration or cascode?** A mirror transistor at 100 µA has $g_m$ = 1 mS and $r_o$ = 100 kΩ. (a) Find the degeneration resistance that raises the output resistance to 1 MΩ, and the compliance it costs. (b) What output resistance would a cascode give?

### Problem 10-08.6 [B]

**Cascode with the body effect.** For the cascode mirror with $g_m$ = 1 mS, $g_{mb}$ = 0.2 mS for the upper device and $r_o$ = 100 kΩ for both, find the output resistance.

### Problem 10-08.7 [B]

**A β helper with low-β transistors.** A bipolar mirror copies 200 µA with β = 40 (ignore the Early effect). Find the output current and error for the basic mirror and with a β helper.

### Problem 10-08.8 [B]

**Small transistors.** Mirror transistors of $WL$ = 4 µm² run at $V_{ov}$ = 0.15 V. (a) Find $\sigma(\Delta V_{TH})$, $\sigma(\Delta I/I)$ and the 3σ current error. (b) What area gives a 3σ error of 1%?

### Problem 10-08.9 [C]

**Degeneration and matching.** A mirror at $V_{ov}$ = 0.2 V and 100 µA ($g_m$ = 1 mS, $WL$ = 10 µm²) gets $R_S$ = 2 kΩ in both sources; the two resistors mismatch with σ = 0.1%. (a) Show that a threshold difference now causes $\Delta I/I = (g_m/I)\Delta V_{TH}/(1 + g_mR_S)$ and a resistor mismatch $\Delta I/I = -[g_mR_S/(1 + g_mR_S)]\Delta R/R$. (b) Find $\sigma(\Delta I/I)$ without degeneration, the threshold contribution with it, the resistor contribution, and the total.

### Problem 10-08.10 [C]

**The Wilson mirror's ratio.** In the Wilson mirror, Q1 (collector to Q3's base) and Q2 (diode-connected) form a mirror, Q3's emitter feeds Q2, and $I_{ref}$ enters Q1's collector node. With matched transistors and current gain β, count the currents at each node and show that $I_{out}/I_{ref} = 1 - 2/(\beta^2 + 2\beta + 2)$. Evaluate the error for β = 50.

### Problem 10-08.11 [C]

**A bias tree on 1.2 V.** A 20 µA reference is mirrored to eight blocks at 20 µA each. (a) Find the total bias current and power. (b) Each block receives a gate voltage instead of a current, and its local ground sits 5 mV above the reference's. With $V_{ov}$ = 0.2 V, by how much does that block's current change? Why do designers distribute currents instead?

### Problem 10-08.12 [B]

**Supply sensitivity.** A resistor-referenced bias on a 1.8 V supply has $V_{GS}$ ≈ 0.7 V. Estimate the reference's sensitivity to supply in %/V, and its change for a 5% (90 mV) supply variation.

---

## Objective coverage

| Learning objective (chapter 10-08) | Problems |
|---|---|
| 1. Current, output resistance, compliance | 2, 5 |
| 2. Basic MOS and bipolar mirror errors | 1, 3, 4, 7 |
| 3. Degeneration, cascode, Wilson | 5, 6, 10 |
| 4. Mismatch and area | 8, 9 |
| 5. Bias distribution and supply sensitivity | 11, 12 |
